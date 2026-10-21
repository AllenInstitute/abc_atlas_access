"""abc_atlas_access.cloud against a small local AnnData store (offline), plus live checks of the published
bucket when ABC_REMOTE_TESTS=1."""
import json
import os
import sys

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("zarr", minversion="3.1")
pytest.importorskip("obstore")
if sys.version_info < (3, 11):  # pragma: no cover
    pytest.skip("the cloud extra needs Python 3.11 or later", allow_module_level=True)

import anndata as ad  # noqa: E402

from abc_atlas_access.cloud import concat, from_view_spec, list_datasets, load_catalog, open_dataset  # noqa: E402

N_CELLS, GENES = 40, ["Gad2", "Slc17a7", "Sst", "Pvalb", "Fezf2"]


@pytest.fixture(scope="module")
def catalog(tmp_path_factory):
    """A one-dataset catalog: 40 cells x 5 genes, X[i, j] = i + j / 10, written by anndata as zarr v3."""
    root = tmp_path_factory.mktemp("cloud")
    ad.settings.zarr_write_format = 3
    subclass = np.where(np.arange(N_CELLS) < 25, "001 A Glut", "002 B GABA")
    obs = pd.DataFrame({
        "cell_index": np.arange(N_CELLS),
        "brain_section_label": pd.Categorical(np.where(np.arange(N_CELLS) % 2, "S.2", "S.1")),
        "CCN1_subclass": pd.Categorical(subclass),
        "CCN1_subclass_color": pd.Categorical(np.where(subclass == "001 A Glut", "#ff0000", "#0000ff")),
        "parcellation_division": pd.Categorical(np.where(np.arange(N_CELLS) < 10, "HPF", "Isocortex")),
        "score": np.linspace(0, 1, N_CELLS),
        "CCN1_cluster_alias": pd.array([*range(N_CELLS - 1), None], dtype="Int64"),
        "passed_qc": np.arange(N_CELLS) < 38,
        "CCN1_in_Nbhd_A": np.arange(N_CELLS) % 4 == 0,
    }, index=pd.Index([f"cell{i}" for i in range(N_CELLS)], name="cell_label"))
    var = pd.DataFrame({"gene_symbol": GENES}, index=pd.Index([f"ENSMUSG{i:011d}" for i in range(5)],
                                                                name="gene_identifier"))
    X = (np.arange(N_CELLS)[:, None] + np.arange(5)[None, :] / 10).astype(np.float32)
    a = ad.AnnData(X=X, obs=obs, var=var, obsm={"X_umap": np.c_[np.arange(N_CELLS), -np.arange(N_CELLS)],
                                                 "X_umap_CCN1_Nbhd-A": np.ones((N_CELLS, 2))})
    a.write_zarr(root / "toy.zarr")
    cat = {"catalog_version": 1, "storage": {"provider": "local", "root": "."}, "taxonomies": {"CCN1": "toy"},
           "datasets": {"Toy": {"description": "toy", "latest": "1", "versions": {"1": {
               "store": "toy.zarr", "n_cells": N_CELLS, "n_genes": 5, "x_units": "log2", "x_chunks": [8, 2],
               "taxonomies": ["CCN1"], "column_names": {"subclass": "CCN1_subclass"},
               "plots": {"umap": "X_umap"},
               "embeddings": {"Nbhd-A": {"obsm": "X_umap_CCN1_Nbhd-A", "obs_column": "CCN1_in_Nbhd_A"}}}}}}}
    path = root / "catalog.json"
    path.write_text(json.dumps(cat))
    load_catalog.cache_clear()
    return str(path)


def test_catalog_and_columns(catalog):
    assert list(list_datasets(catalog).index) == ["Toy"]
    ds = open_dataset("Toy", catalog=catalog)
    assert ds.column("subclass") == "CCN1_subclass" and ds.column("subclass_color") == "CCN1_subclass_color"
    assert ds.categories("subclass") == ["001 A Glut", "002 B GABA"]
    assert ds.categories("subclass", pattern="GABA") == ["002 B GABA"]
    with pytest.raises(KeyError, match="did you mean"):
        ds.column("subclas")
    assert list(ds.var["gene_symbol"]) == GENES and list(ds.var["gene_index"]) == list(range(5))


def test_obs_decodes_every_encoding(catalog):
    obs = open_dataset("Toy", catalog=catalog).obs(rows=[0, 39])
    assert list(obs.index) == ["cell0", "cell39"]
    assert isinstance(obs["CCN1_subclass"].dtype, pd.CategoricalDtype)
    assert obs["CCN1_cluster_alias"].isna().tolist() == [False, True]  # nullable integer
    assert obs["passed_qc"].tolist() == [True, False]


def test_select_semantics(catalog):
    ds = open_dataset("Toy", catalog=catalog)
    # AND across keywords, OR within a list; failed-QC cells (38, 39) are dropped by default
    assert ds.select(subclass="002 B GABA").rows.tolist() == list(range(25, 38))
    assert ds.select(subclass="002 B GABA", passed_qc=False).n_cells == 15
    assert ds.select(**{"subclass": "002 B GABA"}).n_cells == ds.select(subclass="002 B GABA").n_cells
    assert ds.select(subclass="001 A Glut", parcellation_division="HPF").rows.tolist() == list(range(10))
    # where: OR across columns inside one clause (as within one hierarchy in the app)
    either = ds.select(where=[{"subclass": ["002 B GABA"], "parcellation_division": ["HPF"]}])
    assert either.rows.tolist() == list(range(10)) + list(range(25, 38))
    assert ds.select(sections=["S.2"]).rows.tolist() == list(range(1, 38, 2))
    assert ds.select(embedding="Nbhd-A").rows.tolist() == list(range(0, 38, 4))
    # ranges: numeric columns and genes, inclusive, open ends
    assert ds.select(ranges={"score": (None, 0.1)}).rows.tolist() == [0, 1, 2, 3]
    assert ds.select(ranges={"Sst": (30, None)}).rows.tolist() == list(range(30, 38))  # Sst = row + 0.2
    with pytest.warns(UserWarning, match="no cells with"):
        assert ds.select(subclass="003 Typo").n_cells == 0


def test_expression_and_anndata(catalog):
    ds = open_dataset("Toy", catalog=catalog)
    cells = ds.select(subclass="001 A Glut") & ds.select(parcellation_division="Isocortex")
    assert cells.rows.tolist() == list(range(10, 25))
    expr = cells.expression(["Fezf2", "ENSMUSG00000000001"])  # symbols or Ensembl ids
    assert list(expr.columns) == ["Slc17a7", "Fezf2"]  # in X order
    np.testing.assert_allclose(expr["Fezf2"].to_numpy(), np.arange(10, 25) + 0.4, rtol=1e-6)
    assert expr.index[0] == "cell10"
    est = cells.estimate(["Gad2", "Fezf2"])
    rows_per_chunk, genes_per_chunk = ds.X.chunks  # requests = distinct row blocks x distinct gene blocks
    assert est["requests"] == len({r // rows_per_chunk for r in range(10, 25)}) * len({0 // genes_per_chunk,
                                                                                    4 // genes_per_chunk})
    a = cells.to_anndata(genes=["Sst"], obs_columns=["subclass"])
    assert a.shape == (15, 1) and list(a.var_names) == ["ENSMUSG00000000002"]
    assert a.uns["CCN1_subclass_colors"] == ["#ff0000"]
    np.testing.assert_array_equal(a.obsm["X_umap"][:, 0], np.arange(10, 25))
    with pytest.raises(KeyError, match="genes not in"):
        cells.expression(["NotAGene"])


def test_view_spec_and_concat(catalog):
    spec = {"spec_version": "0.1.0", "dataset": "Toy", "plot": {"type": "umap", "embedding": "Nbhd-A"},
            "filters": [{"any_of": [{"column": "subclass", "values": ["001 A Glut"]}]}],
            "range_filters": [{"gene": "Gad2", "min": 4, "max": 20}], "color_by": {"column": "subclass"}}
    view = from_view_spec(spec, catalog=catalog)
    assert view.cells.rows.tolist() == [4, 8, 12, 16, 20]
    assert view.obsm == "X_umap_CCN1_Nbhd-A" and view.genes == ["Gad2"] and view.color_column == "CCN1_subclass"
    a, b = view.to_anndata(["subclass"]), open_dataset("Toy", catalog=catalog).select(
        subclass="002 B GABA").to_anndata(genes=["Gad2", "Sst"], obs_columns=["subclass"], obsm="X_umap_CCN1_Nbhd-A")
    combined = concat({"one": a, "two": b})
    assert combined.shape == (5 + 13, 1)  # inner join on Ensembl id: Gad2 only
    assert combined.obs["dataset"].value_counts().to_dict() == {"two": 13, "one": 5}
    assert combined.uns["CCN1_subclass_colors"] == ["#ff0000", "#0000ff"]


remote = pytest.mark.skipif(os.environ.get("ABC_REMOTE_TESTS") != "1", reason="set ABC_REMOTE_TESTS=1 to read the bucket")


@remote
def test_published_merfish():
    load_catalog.cache_clear()
    ds = open_dataset("MERFISH-C57BL6J-638850-imputed")
    cells = ds.select(parcellation_division="HPF", neurotransmitter="GABA")
    assert cells.n_cells == 23_989
    a = cells.subsample(500).to_anndata(genes=["Sst", "Pvalb"], obs_columns=["supertype"], obsm="spatial")
    assert a.shape == (500, 2) and "CCN20230722_supertype_colors" in a.uns


@remote
def test_published_l5et_concat():
    load_catalog.cache_clear()
    parts = {}
    for name in ["WMB-10Xv3", "Consensus-WMB-Macosko-10X"]:
        ds = open_dataset(name)
        cells = ds.select(CCN20251031_subclass=ds.categories("CCN20251031_subclass", r"L5-ET-CTX"))
        parts[name] = cells.to_anndata(genes=["Chrna6"], obs_columns=["CCN20251031_supertype"],
                                       obsm="X_umap_CCN20251031_Pallium-Glut")
    combined = concat(parts)
    assert combined.obs["dataset"].value_counts().to_dict() == {"Consensus-WMB-Macosko-10X": 28_403, "WMB-10Xv3": 5_880}
