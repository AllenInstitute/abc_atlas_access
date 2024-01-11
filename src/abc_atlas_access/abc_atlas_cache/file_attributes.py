import pathlib
from pydantic import BaseModel


class CacheFileAttributes(BaseModel):
    url: str
    version: str
    file_size: int
    local_path: pathlib.Path
    relative_path: str  # path relative to cache_dir/bucket_name
    file_type: str
    file_hash: str
