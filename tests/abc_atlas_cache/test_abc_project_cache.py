from pathlib import Path
from moto import mock_aws
from .utils import create_manifest_dict, BaseCacheTestCase


@mock_aws
class TestAbcProjectCache(BaseCacheTestCase):
    pass