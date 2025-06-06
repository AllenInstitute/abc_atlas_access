import json
from moto import mock_aws
import pytest

from .utils import (
    BaseCacheTestCase,
    create_manifest_dict,
    add_directory_to_manifest,
    add_file_to_manifest,
)
from abc_atlas_access.abc_atlas_cache.cloud_cache import S3CloudCache
from abc_atlas_access.abc_atlas_cache.file_attributes import (
    CacheFileAttributes,
)  # noqa: E501


@mock_aws
class TestCompareManifests(BaseCacheTestCase):

    def setUp(self):
        super().setUp()
        self.old_version = "20230101"
        self.new_version = "20240101"
        self.old_manifest = f"releases/{self.old_version}/manifest.json"
        self.new_manifest = f"releases/{self.new_version}/manifest.json"

    def test_compare_manifests(self):
        """Test that the expected comparison between two manifests is returned."""
        manifest_1, _, _ = create_manifest_dict(
            version=self.old_version, test_bucket_name=self.test_bucket_name
        )
        manifest_2, _, _ = create_manifest_dict(
            version=self.new_version, test_bucket_name=self.test_bucket_name
        )

        file_attr_1 = CacheFileAttributes(
            url="junk",
            version="junk",
            file_size=1234,
            local_path="junk",
            relative_path=f"expression_matrices/first_dir/{self.old_version}/data1.h5ad",  # noqa: E501
            file_type="data",
            file_hash="junk",
        )
        file_attr_2 = CacheFileAttributes(
            url="junk",
            version="junk",
            file_size=1234,
            local_path="junk",
            relative_path=f"expression_matrices/second_dir/{self.new_version}/data2.h5ad",  # noqa: E501
            file_type="data",
            file_hash="junk",
        )

        manifest_1 = add_directory_to_manifest(
            file_attribute=file_attr_1, manifest=manifest_1
        )
        manifest_2 = add_directory_to_manifest(
            file_attribute=file_attr_2, manifest=manifest_2
        )
        manifest_1 = add_file_to_manifest(
            file_attribute=file_attr_1, manifest=manifest_1
        )
        manifest_2 = add_file_to_manifest(
            file_attribute=file_attr_2, manifest=manifest_2
        )

        self.client.put_object(
            Bucket=self.test_bucket_name,
            Key=self.old_manifest,
            Body=bytes(json.dumps(manifest_1), "utf-8"),
        )
        self.client.put_object(
            Bucket=self.test_bucket_name,
            Key=self.new_manifest,
            Body=bytes(json.dumps(manifest_2), "utf-8"),
        )

        expected = {
            "directory_changes": {
                "new_dirs": ["second_dir"],
                "removed_dirs": ["first_dir"],
            },
            "metadata_changes": {
                "new_metadata": ["second_dir: data2"],
                "removed_metadata": ["first_dir: data1"],
                "changed_metadata": ["test_directory: metadata_file"],
                "manifest_error_metadata": [],
            },
            "expression_matrix_file_changes": {
                "new_expression_matrices": ["second_dir: data2/log2"],
                "removed_expression_matrices": ["first_dir: data1/log2"],
                "changed_expression_matrices": ["test_directory: data_file/log2"],
                "manifest_error_expression_matrices": [],
            },
            "image_volume_file_changes": {
                "new_image_volumes": [],
                "removed_image_volumes": [],
                "changed_image_volumes": [],
                "manifest_error_image_volumes": [],
            },
            "mapmycells_file_changes": {
                "new_mapmycells": [],
                "removed_mapmycells": [],
                "changed_mapmycells": [],
                "manifest_error_mapmycells": [],
            },
        }

        cloud_cache = S3CloudCache(self.cache_dir, self.test_bucket_name)
        cloud_cache.load_manifest(self.old_manifest)
        cloud_cache.load_manifest(self.new_manifest)

        comparison = cloud_cache.compare_manifests(
            manifest_newer_name=self.new_manifest, manifest_older_name=self.old_manifest
        )
        assert comparison == expected

    def test_compare_manifests_wrong_order(self):
        """ """
        manifest_1, _, _ = create_manifest_dict(
            version=self.old_version, test_bucket_name=self.test_bucket_name
        )
        manifest_2, _, _ = create_manifest_dict(
            version=self.new_version, test_bucket_name=self.test_bucket_name
        )

        self.client.put_object(
            Bucket=self.test_bucket_name,
            Key=self.old_manifest,
            Body=bytes(json.dumps(manifest_1), "utf-8"),
        )
        self.client.put_object(
            Bucket=self.test_bucket_name,
            Key=self.new_manifest,
            Body=bytes(json.dumps(manifest_2), "utf-8"),
        )

        cloud_cache = S3CloudCache(self.cache_dir, self.test_bucket_name)
        cloud_cache.load_manifest(self.old_manifest)
        cloud_cache.load_manifest(self.new_manifest)

        with pytest.raises(ValueError, match="The manifest input first"):
            cloud_cache.compare_manifests(
                manifest_newer_name=self.old_manifest,
                manifest_older_name=self.new_manifest,
            )
