import json
from moto import mock_aws
import os
from unittest.mock import patch
import pytest

from .utils import (
    BaseCacheTestCase,
    create_manifest_dict,
    add_directory_to_manifest,
    add_file_to_manifest,
    hash_data
)
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache
from abc_atlas_access.abc_atlas_cache.file_attributes import \
    CacheFileAttributes
from abc_atlas_access.abc_atlas_cache.cloud_cache import (
    LocalCache,
    S3CloudCache
)


@mock_aws
class TestAbcProjectCache(BaseCacheTestCase):

    def setUp(self):
        super().setUp()

        self.new_version = "20240101"
        self.old_version = "20230101"
        self.new_file = "new_data/log2"
        self.old_file = "old_data/log2"
        self.data_file = "data_file/log2"

        old_data = b'11235813kjlssergwesvsdd'
        old_checksum = hash_data(old_data)

        new_data = b'8675309jenny'
        new_checksum = hash_data(new_data)

        self.old_manifest, self.old_metadata_path, self.old_data_path = create_manifest_dict(  # noqa: E501
            version=self.old_version,
            test_bucket_name=self.test_bucket_name,
            file_hash=old_checksum
        )
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.old_metadata_path,
                               Body=old_data)
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.old_data_path,
                               Body=old_data)

        self.new_manifest, self.new_metadata_path, self.new_data_path = create_manifest_dict(  # noqa: E501
            version=self.new_version,
            test_bucket_name=self.test_bucket_name,
            file_hash=new_checksum
        )
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.new_metadata_path,
                               Body=new_data)
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.new_data_path,
                               Body=new_data)

        old_file = b'skibbitybeebopSkatmansworld'
        old_file_checksum = hash_data(old_file)

        new_file = b'sendingoutanSOS'
        new_file_checksum = hash_data(new_file)

        self.old_file_attr = CacheFileAttributes(
            url='junk',
            version=self.old_version,
            file_size=1234,
            local_path='junk',
            relative_path=f'expression_matrices/first_dir/{self.old_version}/{self.old_file.split("/")[0]}.h5ad',  # noqa: E501
            file_type='data',
            file_hash=old_file_checksum
        )
        self.new_file_attr = CacheFileAttributes(
            url='junk',
            version=self.new_version,
            file_size=90210,
            local_path='junk',
            relative_path=f'expression_matrices/second_dir/{self.new_version}/{self.new_file.split("/")[0]}.h5ad',  # noqa: E501
            file_type='data',
            file_hash=new_file_checksum
        )
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.old_file_attr.relative_path,
                               Body=old_file)
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.new_file_attr.relative_path,
                               Body=new_file)

        self.old_manifest = add_directory_to_manifest(
            file_attribute=self.old_file_attr,
            manifest=self.old_manifest
        )
        self.new_manifest = add_directory_to_manifest(
            file_attribute=self.new_file_attr,
            manifest=self.new_manifest
        )
        self.old_manifest = add_file_to_manifest(
            file_attribute=self.old_file_attr,
            manifest=self.old_manifest
        )
        self.new_manifest = add_file_to_manifest(
            file_attribute=self.new_file_attr,
            manifest=self.new_manifest
        )

        self.client.put_object(
            Bucket=self.test_bucket_name,
            Key=f'releases/{self.old_version}/manifest.json',
            Body=bytes(json.dumps(self.old_manifest), 'utf-8')
        )
        self.client.put_object(
            Bucket=self.test_bucket_name,
            Key=f'releases/{self.new_version}/manifest.json',
            Body=bytes(json.dumps(self.new_manifest), 'utf-8')
        )

    def test_abc_project_cache_s3(self):
        """Run a suite of integration tests on the AbcProjectCache class
        from_s3_cache.
        """
        # Initialize the cache, overwriting the bucket name.
        AbcProjectCache._bucket_name = self.test_bucket_name
        cache = AbcProjectCache.from_s3_cache(self.cache_dir)

        # Test that the expected manifests are available and the directories
        # are as expected.
        assert cache.current_manifest == f'releases/{self.new_version}/manifest.json'  # noqa: E501
        assert cache.list_all_downloaded_manifests == [
            f'releases/{self.new_version}/manifest.json'
        ]
        assert cache.list_manifest_file_names == [
            f'releases/{self.old_version}/manifest.json',
            f'releases/{self.new_version}/manifest.json'
        ]
        assert cache.list_directories == ["second_dir", "test_directory"]
        assert cache.list_expression_matrix_files("second_dir") == [self.new_file]
        assert cache.list_expression_matrix_files("test_directory") == [self.data_file]
        assert cache.list_metadata_files("test_directory") == [
            "metadata_file"
        ]
        # Test the directory from the older manifest is not available.
        with pytest.raises(KeyError, match="first_dir"):
            cache.list_expression_matrix_files("first_dir")

        # Download data and test that the downloaded file exists on disk.
        data_path = cache.get_file_path(directory="second_dir",
                                        file_name=self.new_file)
        assert data_path.exists()
        assert data_path == self.cache_dir / self.new_file_attr.relative_path
        data_path = cache.get_file_path(directory="test_directory",
                                        file_name="data_file/log2")
        assert data_path.exists()
        assert data_path == self.cache_dir / self.new_data_path
        metadata_path = cache.get_file_path(directory="test_directory",
                                            file_name="metadata_file")
        assert metadata_path.exists()
        assert metadata_path == self.cache_dir / self.new_metadata_path

        # Load an older manifest and test the expected returns regarding
        # the loaded and downloaded manifests.
        cache.load_manifest(f'releases/{self.old_version}/manifest.json')
        assert cache.current_manifest == f'releases/{self.old_version}/manifest.json'  # noqa: E501
        assert cache.latest_downloaded_manifest_file == f'releases/{self.new_version}/manifest.json'  # noqa: E501
        assert cache.list_all_downloaded_manifests == [
            f'releases/{self.old_version}/manifest.json',
            f'releases/{self.new_version}/manifest.json'
        ]
        assert cache.list_directories == ["first_dir", "test_directory"]
        assert cache.list_expression_matrix_files("first_dir") == [self.old_file]
        assert cache.list_expression_matrix_files("test_directory") == [self.data_file]
        assert cache.list_metadata_files("test_directory") == [
            "metadata_file"
        ]
        # Test that the newer manifest's directory is not present.
        with pytest.raises(KeyError, match="second_dir"):
            cache.list_expression_matrix_files("second_dir")

        # Download the older files and test for their expected paths.
        data_paths = cache.get_directory_expression_matrices(directory="first_dir")
        assert data_paths[0].exists()
        assert data_paths == [
            self.cache_dir / self.old_file_attr.relative_path
        ]
        data_paths = cache.get_directory_expression_matrices(directory="test_directory")
        assert data_paths[0].exists()
        assert data_paths == [self.cache_dir / self.old_data_path]
        metadata_paths = cache.get_directory_metadata(
            directory="test_directory"
        )
        assert metadata_paths[0].exists()
        assert metadata_paths == [self.cache_dir / self.old_metadata_path]

        # Reload the most recent manifest and test that is as expected.
        cache.load_latest_manifest()
        assert cache.current_manifest == f'releases/{self.new_version}/manifest.json'  # noqa: E501

    def test_abc_project_cache_local_cache(self):
        """Run a suite of integration tests on the AbcProjectCache class
        from_local_cache.
        """
        AbcProjectCache._bucket_name = self.test_bucket_name
        cache = AbcProjectCache.from_s3_cache(self.cache_dir)

        # Download data into the local cache.
        cache.get_file_path(directory="second_dir",
                            file_name=self.new_file)
        cache.get_file_path(directory="test_directory",
                            file_name=self.data_file)
        cache.get_file_path(directory="test_directory",
                            file_name="metadata_file")

        # Remove the previous cache object.
        del cache

        # Initialize a new cache object from the local cache.
        cache = AbcProjectCache.from_local_cache(self.cache_dir)
        assert cache.current_manifest == f'releases/{self.new_version}/manifest.json'  # noqa: E501
        assert cache.list_all_downloaded_manifests == [
            f'releases/{self.new_version}/manifest.json'
        ]
        assert cache.list_manifest_file_names == [
            f'releases/{self.new_version}/manifest.json'
        ]
        assert cache.list_directories == ["second_dir", "test_directory"]
        assert cache.list_expression_matrix_files("second_dir") == [self.new_file]
        assert cache.list_expression_matrix_files("test_directory") == [self.data_file]
        assert cache.list_metadata_files("test_directory") == [
            "metadata_file"
        ]
        with pytest.raises(KeyError, match="first_dir"):
            cache.list_expression_matrix_files("first_dir")

        data_path = cache.get_file_path(directory="second_dir",
                                        file_name=self.new_file)
        assert data_path.exists()
        assert data_path == self.cache_dir / self.new_file_attr.relative_path
        data_path = cache.get_file_path(directory="test_directory",
                                        file_name=self.data_file)
        assert data_path.exists()
        assert data_path == self.cache_dir / self.new_data_path
        metadata_path = cache.get_file_path(directory="test_directory",
                                            file_name="metadata_file")
        assert metadata_path.exists()
        assert metadata_path == self.cache_dir / self.new_metadata_path

        data_paths = cache.get_directory_expression_matrices(directory="test_directory")
        assert data_paths == [self.cache_dir / self.new_data_path]
        metadata_paths = cache.get_directory_metadata(
            directory="test_directory"
        )
        assert metadata_paths == [self.cache_dir / self.new_metadata_path]

    def test_abc_project_cache_from_cache_dir(self):
        """Run test that caches are initialized from the cache directory
        correctly as either a S3CloudCache or LocalCache object when
        appropreate.
        """
        AbcProjectCache._bucket_name = self.test_bucket_name
        cache = AbcProjectCache.from_cache_dir(self.cache_dir)
        assert isinstance(cache.cache, S3CloudCache)

        # Download data into the local cache.
        cache.get_file_path(directory="second_dir",
                            file_name=self.new_file)
        cache.get_file_path(directory="test_directory",
                            file_name=self.data_file)
        cache.get_file_path(directory="test_directory",
                            file_name="metadata_file")

        # Remove the previous cache object.
        del cache

        # Initialize a new read only object from the local cache.
        with patch('os.access', return_value=False):
            cache = AbcProjectCache.from_cache_dir(self.cache_dir)
        assert isinstance(cache.cache, LocalCache)