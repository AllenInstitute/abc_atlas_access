import json
import pathlib
from pydantic import BaseModel


class CacheFileAttributes(BaseModel):
    url: str
    version: str
    file_size: int
    local_path: pathlib.Path
    file_type: str
