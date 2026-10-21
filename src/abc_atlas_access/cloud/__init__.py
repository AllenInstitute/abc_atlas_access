"""Read the ABC Atlas cloud datasets (AnnData stores in zarr v3 in a public bucket) directly, without downloads.

    from abc_atlas_access.cloud import open_dataset

    ds = open_dataset("MERFISH-C57BL6J-638850-imputed")
    cells = ds.select(subclass="022 L5 ET CTX Glut", parcellation_division="Isocortex")
    adata = cells.to_anndata(genes=["Fezf2", "Bcl11b"], obsm="spatial")

Only the requested columns, cells and genes are fetched. Requires the `cloud` extra (Python 3.11 or later):
`pip install "abc_atlas_access[cloud]"`.
"""
try:
    import obstore  # noqa: F401
    import zarr  # noqa: F401
except ImportError as e:  # pragma: no cover
    raise ImportError('abc_atlas_access.cloud needs the "cloud" extra: pip install "abc_atlas_access[cloud]" '
                      "(Python 3.11 or later)") from e

from ._dataset import CellSelection, Dataset, list_datasets, open_dataset, set_colors
from ._store import DEFAULT_CATALOG, load_catalog
from ._view import View, concat, from_view_spec

__all__ = ["CellSelection", "DEFAULT_CATALOG", "Dataset", "View", "concat", "from_view_spec", "list_datasets",
           "load_catalog", "open_dataset", "set_colors"]
