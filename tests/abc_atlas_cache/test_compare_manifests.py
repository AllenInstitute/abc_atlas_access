from moto import mock_aws
from .utils import BaseCacheTestCase, create_manifest_dict
from abc_atlas_access.abc_atlas_cache.cloud_cache import S3CloudCache

@mock_aws
class TestCompareManifests(BaseCacheTestCase):

    def test_compare_manifests(self):
        """

        Returns
        -------

        """
        manifest_1, _, _ = create_manifest_dict(
            version='20230101',
            test_bucket_name=self.test_bucket_name
        )
        manifest_2, _, _ = create_manifest_dict(
            version='20240101',
            test_bucket_name=self.test_bucket_name
        )

