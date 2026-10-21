"""ABC Atlas view specs (the JSON the web app exports) as cell selections, and combining datasets."""
import json
from dataclasses import dataclass, field
from pathlib import Path

from ._dataset import CellSelection, Dataset, open_dataset, set_colors


@dataclass
class View:
    """An ABC Atlas view: its dataset, the selected cells, and how it is drawn."""

    dataset: Dataset
    cells: CellSelection
    spec: dict
    #: obsm key of the plot (a UMAP or spatial section coordinates)
    obsm: str
    #: genes the view uses (coloring, range filters, extra genes)
    genes: list = field(default_factory=list)

    @property
    def color_column(self):
        """The stored obs column the view is colored by (None when colored by a gene)."""
        col = self.spec["color_by"].get("column")
        return self.dataset.column(col) if col else None

    @property
    def color_gene(self):
        return self.spec["color_by"].get("gene")

    def to_anndata(self, obs_columns=None):
        """AnnData of the view's cells with its genes, the plot embedding and color palettes."""
        return self.cells.to_anndata(genes=self.genes, obs_columns=obs_columns, obsm=self.obsm)


def from_view_spec(spec, catalog=None):
    """A View from an ABC Atlas view spec (a dict, a JSON string or a path to a .json file)."""
    if isinstance(spec, (str, Path)) and not str(spec).lstrip().startswith("{"):
        spec = Path(spec).read_text()
    if isinstance(spec, str):
        spec = json.loads(spec)
    ds = open_dataset(spec["dataset"], catalog=catalog)
    plot = spec["plot"]
    where = [{s["column"]: s["values"] for s in clause["any_of"]} for clause in spec.get("filters") or []]
    ranges = {rf.get("gene") or rf["column"]: (rf.get("min"), rf.get("max")) for rf in spec.get("range_filters") or []}
    cells = ds.select(where, ranges=ranges, embedding=plot.get("embedding"), sections=plot.get("sections"))
    color = spec["color_by"]
    genes = list(dict.fromkeys(([color["gene"]] if color.get("gene") else [])
                               + [rf["gene"] for rf in spec.get("range_filters") or [] if rf.get("gene")]
                               + list(spec.get("genes") or [])))
    obsm = cells.default_obsm if plot.get("embedding") else ds.info["plots"][plot["type"]]
    return View(ds, cells, spec, obsm, genes)


def concat(parts, label="dataset", join="inner"):
    """Concatenate AnnData objects from different datasets ({name: adata}): genes are matched by Ensembl id
    (join="inner" keeps the shared genes), a `label` column records each cell's dataset, and the color
    palettes are rebuilt for the combined categories. Columns named after a taxonomy (CCN..._subclass) line
    up across datasets that carry that taxonomy."""
    import anndata as ad

    combined = ad.concat(parts, label=label, join=join, merge="same", index_unique="-")
    return set_colors(combined)
