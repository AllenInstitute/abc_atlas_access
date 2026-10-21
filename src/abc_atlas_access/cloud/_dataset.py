"""Datasets and cell selections backed by the cloud AnnData (zarr v3) stores."""
import keyword
import re
import sys
import warnings
from functools import cached_property

import numpy as np
import pandas as pd
import zarr

from ._store import load_catalog, open_zarr

#: Requests per second to expect from one X read (zarr fetches the chunks of a read concurrently).
REQUESTS_PER_SECOND = 1000
#: Concurrent range requests per read.
CONCURRENCY = 64
#: Genes per X read; larger selections are read in blocks of this many genes (with progress messages).
GENE_BLOCK = 512


def list_datasets(catalog=None):
    """The datasets in the catalog, one row each."""
    cat = load_catalog(catalog)
    rows = []
    for name, d in cat["datasets"].items():
        v = d["versions"][d["latest"]]
        rows.append({"dataset": name, "latest": d["latest"], "versions": ", ".join(d["versions"]),
                     "n_cells": v["n_cells"], "n_genes": v["n_genes"], "taxonomies": ", ".join(v["taxonomies"]),
                     "description": d["description"]})
    return pd.DataFrame(rows).set_index("dataset")


def open_dataset(name, version=None, catalog=None):
    """Open a dataset from the catalog: `open_dataset("WMB-10Xv3")`, or pin a release with `version=`."""
    cat = load_catalog(catalog)
    if name not in cat["datasets"]:
        raise KeyError(f"unknown dataset {name!r}; available: {', '.join(cat['datasets'])}")
    d = cat["datasets"][name]
    version = version or d["latest"]
    if version not in d["versions"]:
        raise KeyError(f"{name} has no version {version!r}; available: {', '.join(d['versions'])}")
    return Dataset(name, version, d["versions"][version], cat["storage"], d.get("description", ""))


def _decode(node, rows=None):
    """One AnnData obs element (zarr) -> numpy/pandas values, for all rows or the sorted `rows`.
    Categoricals are decoded from codes + categories (categories as Python strings, so pandas accepts them)."""
    take = (lambda a: a[:]) if rows is None else (lambda a: a.get_orthogonal_selection((rows,)))
    if isinstance(node, zarr.Group):
        kind = node.attrs.get("encoding-type")
        if kind == "categorical":
            categories = node["categories"][:]
            categories = categories.astype(object) if categories.dtype.kind in "OUT" else categories
            return pd.Categorical.from_codes(take(node["codes"]), categories=pd.Index(categories),
                                             ordered=bool(node.attrs.get("ordered", False)))
        if kind == "nullable-string-array":
            values = take(node["values"]).astype(object)
            values[np.asarray(take(node["mask"]), dtype=bool)] = None
            return values
        if kind in ("nullable-integer", "nullable-boolean"):
            values, mask = take(node["values"]), np.asarray(take(node["mask"]), dtype=bool)
            if kind == "nullable-integer":
                return pd.arrays.IntegerArray(np.asarray(values, dtype=np.int64), mask)
            return pd.arrays.BooleanArray(np.asarray(values, dtype=bool), mask)
        raise ValueError(f"unsupported obs element encoding {kind!r}")
    values = take(node)
    return values.astype(object) if values.dtype.kind == "T" else values  # NumPy StringDType -> str


class Dataset:
    """One cloud dataset: an AnnData store in zarr. Nothing is read until it is needed.

    `select(...)` picks cells; `obs()`, `var`, `root` and `X` give direct access to the underlying data.
    Column names can be the stored ones (`CCN20230722_subclass`) or the short names used by the ABC Atlas
    view spec (`subclass`), which map to this dataset's taxonomy."""

    def __init__(self, name, version, info, storage, description=""):
        self.name, self.version, self.info, self.storage, self.description = name, version, info, storage, description

    def __repr__(self):
        return (f"<Dataset {self.name} {self.version}: {self.info['n_cells']:,} cells x {self.info['n_genes']:,} "
                f"genes, taxonomies {', '.join(self.info['taxonomies'])}>")

    # --- the underlying store -------------------------------------------------------------------
    @cached_property
    def root(self):
        """The zarr group of the AnnData store (obs, var, X, obsm, uns)."""
        return open_zarr(self.storage, self.info["store"])

    @property
    def X(self):
        """The expression matrix (zarr array, cells x genes, log2(CPM + 1)); index it to read."""
        return self.root["X"]

    @cached_property
    def columns(self):
        """The stored obs columns, in order."""
        return list(self.root["obs"].attrs["column-order"])

    @cached_property
    def var(self):
        """The gene table (pandas), indexed by Ensembl id, with gene_symbol and gene_index (column of X)."""
        g = self.root["var"]
        var = pd.DataFrame({c: _decode(g[c]) for c in g.attrs["column-order"]},
                           index=pd.Index(_decode(g[g.attrs["_index"]]), name=g.attrs["_index"]))
        var.insert(0, "gene_index", np.arange(len(var)))
        return var

    @property
    def embeddings(self):
        """Neighborhood -> {"obsm": embedding key, "obs_column": membership flag}."""
        return self.info.get("embeddings", {})

    @property
    def obsm_keys(self):
        return sorted(self.root["obsm"].array_keys())

    # --- columns and values -----------------------------------------------------------------------
    def column(self, name):
        """The stored obs column for a stored or short (view-spec) column name."""
        names = self.info.get("column_names", {})
        stored = names.get(name, name)
        for suffix in ("_label", "_color", "_order"):  # companions follow their column: supertype_color
            if stored not in self.columns and name.endswith(suffix) and name[: -len(suffix)] in names:
                stored = names[name[: -len(suffix)]] + suffix
        if stored not in self.columns:
            close = [c for c in self.columns if name.lower() in c.lower()][:8]
            raise KeyError(f"{self.name} has no column {name!r}" + (f"; did you mean one of {close}?" if close else ""))
        return stored

    def cell_labels(self, rows=None):
        """The cell ids (obs index) for all cells or the sorted integer `rows`."""
        obs = self.root["obs"]
        return pd.Index(_decode(obs[obs.attrs["_index"]], rows), name=obs.attrs["_index"])

    def obs(self, columns=None, rows=None, index=None):
        """Cell metadata (pandas), indexed by cell label: the given columns (default: all) for all cells or
        for the sorted integer `rows`."""
        obs = self.root["obs"]
        cols = self.columns if columns is None else [self.column(c) for c in columns]
        if rows is not None:
            rows = np.asarray(rows, dtype=np.int64)
        index = self.cell_labels(rows) if index is None else index
        return pd.DataFrame({c: _decode(obs[c], rows) for c in cols}, index=index)

    def categories(self, column, pattern=None):
        """The values of a categorical column (optionally only those matching a regular expression)."""
        node = self.root["obs"][self.column(column)]
        if not isinstance(node, zarr.Group):
            raise TypeError(f"{column} is not categorical")
        values = [str(v) for v in node["categories"][:]]
        return [v for v in values if re.search(pattern, v)] if pattern else values

    def gene_index(self, genes):
        """Sorted 0-based columns of X for gene symbols or Ensembl ids (raises on unknown genes)."""
        genes = [genes] if isinstance(genes, str) else list(genes)
        var = self.var
        by_id = pd.Series(var["gene_index"].to_numpy(), index=var.index)
        by_symbol = pd.Series(var["gene_index"].to_numpy(), index=var["gene_symbol"].astype(str))
        idx, missing = [], []
        for g in genes:
            if g in by_id.index:
                idx.append(int(by_id[g]))
            elif g in by_symbol.index:
                hit = by_symbol[g]
                idx.extend(np.atleast_1d(hit).tolist())
            else:
                missing.append(g)
        if missing:
            raise KeyError(f"genes not in {self.name}: {missing}")
        return np.unique(np.asarray(idx, dtype=np.int64))

    # --- selecting cells ------------------------------------------------------------------------
    def select(self, where=None, *, ranges=None, embedding=None, sections=None, passed_qc=True, **filters):
        """Select cells, with the same logic as the ABC Atlas filters.

        Keyword filters are AND-ed and a list of values is OR-ed: `select(subclass=["a", "b"],
        parcellation_division="HPF")`. `where` adds clauses that OR across columns, as the app does within one
        hierarchy: `where=[{"class": ["18 TH Glut"], "subclass": ["149 PVT-PT Ntrk1 Glut"]}]`.
        `ranges` keeps cells with min <= value <= max (None for open ends), for genes or numeric columns:
        `ranges={"Fezf2": (2, None)}`. `embedding` keeps the cells of a neighborhood with its own UMAP;
        `sections` keeps the given brain sections; `passed_qc=False` also keeps cells that failed QC.
        Columns named like Python keywords take a trailing underscore: `select(class_="30 Astro-Epen")`."""
        clauses = [[(k[:-1] if k.endswith("_") and keyword.iskeyword(k[:-1]) else k, v)] for k, v in filters.items()]
        for clause in ([where] if isinstance(where, dict) else where or []):
            clauses.append(list(clause.items()))
        if sections is not None:
            clauses.append([("brain_section_label", sections)])
        flags = []
        if embedding is not None:
            if embedding not in self.embeddings:
                raise KeyError(f"{self.name} has no embedding {embedding!r}; available: {list(self.embeddings)}")
            flags.append(self.embeddings[embedding]["obs_column"])
        if passed_qc:
            flags.append("passed_qc")
        obs = self.root["obs"]
        keep = np.ones(self.info["n_cells"], dtype=bool)
        for flag in flags:
            keep &= np.asarray(obs[flag][:], dtype=bool)
        for clause in clauses:
            keep &= self._clause_mask(clause)
        gene_ranges = {}
        for key, (lo, hi) in (ranges or {}).items():
            try:
                col = self.column(key)
            except KeyError:
                gene_ranges[key] = (lo, hi)
                continue
            values = pd.to_numeric(pd.Series(_decode(obs[col])), errors="coerce").to_numpy(dtype=float)
            keep &= _in_range(values, lo, hi)
        rows = np.flatnonzero(keep)
        if gene_ranges:
            expr = CellSelection(self, rows, embedding).expression(list(gene_ranges))
            ok = np.ones(len(rows), dtype=bool)
            for gene, (lo, hi) in gene_ranges.items():
                values = expr.loc[:, expr.columns == gene].to_numpy(dtype=float).max(axis=1)
                ok &= _in_range(values, lo, hi)
            rows = rows[ok]
        return CellSelection(self, rows, embedding)

    def _clause_mask(self, clause):
        """Cells matching any (column, values) pair of a clause; compares integer codes for categoricals."""
        obs = self.root["obs"]
        mask = np.zeros(self.info["n_cells"], dtype=bool)
        for name, values in clause:
            values = [values] if isinstance(values, (str, int, float)) else list(values)
            node = obs[self.column(name)]
            if isinstance(node, zarr.Group) and node.attrs.get("encoding-type") == "categorical":
                cats = pd.Index([str(c) for c in node["categories"][:]])
                wanted = cats.get_indexer([str(v) for v in values])
                unknown = [v for v, i in zip(values, wanted) if i < 0]
                if unknown:
                    warnings.warn(f"{name}: no cells with {unknown} in {self.name}; see Dataset.categories("
                                  f"{name!r})", stacklevel=3)
                mask |= np.isin(node["codes"][:], wanted[wanted >= 0])
            else:
                col = _decode(node)
                mask |= pd.Series(col).astype(str).isin([str(v) for v in values]).to_numpy()
        return mask


def _in_range(values, lo, hi):
    ok = ~np.isnan(values)
    if lo is not None:
        ok &= values >= lo
    if hi is not None:
        ok &= values <= hi
    return ok


class CellSelection:
    """A set of cells of one dataset (sorted rows of X), with ways to read their data."""

    def __init__(self, dataset, rows, embedding=None):
        self.dataset = dataset
        self.rows = np.asarray(rows, dtype=np.int64)
        self.embedding = embedding

    def __len__(self):
        return len(self.rows)

    @property
    def n_cells(self):
        return len(self.rows)

    def __repr__(self):
        return f"<CellSelection {self.n_cells:,} cells of {self.dataset.name}>"

    def _combine(self, other, op):
        if other.dataset is not self.dataset:
            raise ValueError("cell selections of different datasets cannot be combined")
        return CellSelection(self.dataset, op(self.rows, other.rows), self.embedding or other.embedding)

    def __and__(self, other):
        return self._combine(other, np.intersect1d)

    def __or__(self, other):
        return self._combine(other, np.union1d)

    def subsample(self, n, seed=0):
        """At most n cells drawn from this selection (cheap to read: they stay within its row blocks)."""
        if n >= self.n_cells:
            return self
        rng = np.random.default_rng(seed)
        return CellSelection(self.dataset, np.sort(rng.choice(self.rows, n, replace=False)), self.embedding)

    @cached_property
    def cell_labels(self):
        """The cell ids of the selected cells."""
        return self.dataset.cell_labels(self.rows)

    def obs(self, columns=None):
        """Metadata of the selected cells (pandas), indexed by cell label; default: all columns."""
        return self.dataset.obs(columns, rows=self.rows, index=self.cell_labels)

    def estimate(self, genes):
        """Approximate cost of reading `genes` for these cells: requests, seconds and compressed GB."""
        gene_index = self.dataset.gene_index(genes)
        chunk_rows, chunk_genes = self.dataset.X.chunks
        requests = len(np.unique(self.rows // chunk_rows)) * len(np.unique(gene_index // chunk_genes))
        return {"cells": self.n_cells, "genes": len(gene_index), "requests": requests,
                "seconds": round(requests / REQUESTS_PER_SECOND, 1),
                "approx_gb": round(requests * chunk_rows * chunk_genes * 4 / 3 / 1e9, 2)}  # ~3x compression

    def expression(self, genes, progress=True):
        """Expression (log2) of `genes` (symbols or Ensembl ids) for these cells, as a pandas DataFrame
        (cells x gene symbols, indexed by cell label). Reads only the chunks that hold them."""
        gene_index = self.dataset.gene_index(genes)
        est = self.estimate(self.dataset.var.index[gene_index])
        if est["seconds"] > 120:
            warnings.warn(f"reading {est['genes']:,} genes for {est['cells']:,} cells is ~{est['requests']:,} "
                          f"requests (~{est['seconds'] / 60:.0f} min); consider fewer genes or cells", stacklevel=2)
        X = self.dataset.X
        blocks = [gene_index[i:i + GENE_BLOCK] for i in range(0, len(gene_index), GENE_BLOCK)]
        out = np.empty((self.n_cells, len(gene_index)), dtype=np.float32)
        with zarr.config.set({"async.concurrency": CONCURRENCY}):
            for k, block in enumerate(blocks):
                start = k * GENE_BLOCK
                out[:, start:start + len(block)] = X.get_orthogonal_selection((self.rows, block))
                if progress and len(blocks) > 1:
                    print(f"  read genes {start + len(block):,}/{len(gene_index):,}", file=sys.stderr, flush=True)
        var = self.dataset.var.iloc[gene_index]
        return pd.DataFrame(out, index=self.cell_labels, columns=var["gene_symbol"].astype(str).to_numpy())

    def embedding_coords(self, key=None):
        """Coordinates of these cells in an obsm embedding (default: this selection's neighborhood UMAP, else the
        dataset's main plot: X_umap or spatial)."""
        key = key or self.default_obsm
        arr = self.dataset.root["obsm"][key]
        return arr.get_orthogonal_selection((self.rows, slice(None)))

    @property
    def default_obsm(self):
        if self.embedding:
            return self.dataset.embeddings[self.embedding]["obsm"]
        plots = self.dataset.info.get("plots", {})
        return plots.get("umap") or plots.get("spatial") or self.dataset.obsm_keys[0]

    def to_anndata(self, genes=None, obs_columns=None, obsm=None):
        """An in-memory AnnData of these cells: obs (default: all columns), X for `genes` (default: none),
        var indexed by Ensembl id, the embeddings in `obsm` (a key, a list of keys, or default the selection's
        main embedding), and scanpy palettes (uns['<column>_colors']) from the stored colors."""
        import anndata as ad

        if obs_columns is not None:  # bring each column's stored colors along, for the palettes
            cols = [self.dataset.column(c) for c in obs_columns]
            obs_columns = list(dict.fromkeys(cols + [f"{c}_color" for c in cols if f"{c}_color" in self.dataset.columns]))
        obs = self.obs(obs_columns)
        if genes is not None and len(genes):
            gene_index = self.dataset.gene_index(genes)
            X = self.expression(self.dataset.var.index[gene_index]).to_numpy()
            var = self.dataset.var.iloc[gene_index].drop(columns="gene_index")
        else:
            X, var = None, self.dataset.var.iloc[:0].drop(columns="gene_index")
        keys = [self.default_obsm] if obsm is None else ([obsm] if isinstance(obsm, str) else list(obsm))
        adata = ad.AnnData(X=X, obs=obs, var=var, obsm={k: self.embedding_coords(k) for k in keys})
        set_colors(adata)
        adata.uns["abc_atlas"] = {"dataset": self.dataset.name, "version": self.dataset.version,
                                  "x_units": self.dataset.info.get("x_units", "log2")}
        return adata


def set_colors(adata, columns=None):
    """scanpy palettes (uns['<column>_colors']) for categorical obs columns that have a '<column>_color'
    companion, in category order (call again after subsetting or concatenating)."""
    for col in columns or [c for c in adata.obs.columns if f"{c}_color" in adata.obs.columns]:
        values = adata.obs[col]
        if not isinstance(values.dtype, pd.CategoricalDtype):
            adata.obs[col] = values = values.astype("category")
        values = values.cat.remove_unused_categories()
        adata.obs[col] = values
        lookup = (adata.obs[[col, f"{col}_color"]].dropna().drop_duplicates(col).set_index(col)[f"{col}_color"]
                  .astype(str))
        adata.uns[f"{col}_colors"] = [lookup.get(c, "#808080") for c in values.cat.categories]
    return adata
