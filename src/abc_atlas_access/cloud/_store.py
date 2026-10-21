"""Storage access: the dataset catalog and the zarr stores it points to (GCS, S3 or a local folder)."""
import json
import os
from functools import lru_cache
from pathlib import Path

import zarr
from obstore.store import GCSStore, LocalStore, S3Store
from zarr.storage import ObjectStore

#: The published catalog of cloud datasets; override with the ABC_ATLAS_CLOUD_CATALOG environment variable
#: (a gs://, s3:// or https:// URL, or a local path).
DEFAULT_CATALOG = "gs://abc-atlas-data-refactor/refactor/catalog.json"


def _object_store(storage, prefix=None):
    """An obstore store for a catalog `storage` block (public buckets are read without credentials)."""
    provider = storage.get("provider", "gcs")
    if provider == "gcs":
        return GCSStore(storage["bucket"], prefix=prefix, skip_signature=True)
    if provider == "s3":
        return S3Store(storage["bucket"], prefix=prefix, region=storage.get("region", "us-west-2"),
                       skip_signature=True)
    if provider == "local":
        root = Path(storage["root"])
        return LocalStore(root / prefix if prefix else root)
    raise ValueError(f"unknown storage provider {provider!r}")


def _read_catalog_text(location):
    if location.startswith(("gs://", "s3://")):
        scheme, rest = location.split("://", 1)
        bucket, key = rest.split("/", 1)
        store = _object_store({"provider": "gcs" if scheme == "gs" else "s3", "bucket": bucket})
        import obstore

        return bytes(obstore.get(store, key).bytes()).decode()
    if location.startswith(("http://", "https://")):
        from urllib.request import urlopen

        with urlopen(location) as r:  # noqa: S310 (a URL the user chose)
            return r.read().decode()
    return Path(location).read_text()


@lru_cache(maxsize=4)
def load_catalog(location=None):
    """The dataset catalog (a dict). Cached per location for the session."""
    location = location or os.environ.get("ABC_ATLAS_CLOUD_CATALOG", DEFAULT_CATALOG)
    catalog = json.loads(_read_catalog_text(str(location)))
    if catalog.get("catalog_version") != 1:
        raise ValueError(f"unsupported catalog version {catalog.get('catalog_version')} in {location}")
    if catalog["storage"].get("provider") == "local" and not Path(catalog["storage"]["root"]).is_absolute():
        # a local catalog's root is relative to the catalog file
        catalog["storage"]["root"] = str(Path(location).parent / catalog["storage"]["root"])
    return catalog


def open_zarr(storage, prefix):
    """The root group of a zarr store, read only."""
    return zarr.open_group(ObjectStore(_object_store(storage, prefix), read_only=True), mode="r")
