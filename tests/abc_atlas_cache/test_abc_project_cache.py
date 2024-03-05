import hashlib
import json
import pytest
from pathlib import Path
from unittest import mock
from moto import mock_aws
from .utils import (
    BaseCacheTestCase,
    create_manifest_dict,
    add_directory_to_manifest,
    add_file_to_manifest
)
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache
from abc_atlas_access.abc_atlas_cache.file_attributes import \
    CacheFileAttributes


@mock_aws
class TestAbcProjectCache(BaseCacheTestCase):

    def setUp(self):
        super().setUp()

        self.new_version = "20240101"
        self.old_version = "20230101"

        hasher = hashlib.md5()
        old_data = b'11235813kjlssergwesvsdd'
        hasher.update(old_data)
        old_checksum = hasher.hexdigest()

        hasher = hashlib.md5()
        new_data = b'8675309jenny'
        hasher.update(new_data)
        new_checksum = hasher.hexdigest()

        self.manifest_1, self.old_metadata_path, self.old_data_path = create_manifest_dict(  # noqa: E501
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

        self.manifest_2, self.new_metadata_path, self.new_data_path = create_manifest_dict(  # noqa: E501
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

        hasher = hashlib.md5()
        file_1 = b'skibbitybeebopSkatmansworld'
        hasher.update(file_1)
        file_1_checksum = hasher.hexdigest()

        hasher = hashlib.md5()
        file_2 = b'sendingoutanSOS'
        hasher.update(file_2)
        file_2_checksum = hasher.hexdigest()

        self.file_attr_1 = CacheFileAttributes(
            url='junk',
            version=self.old_version,
            file_size=1234,
            local_path='junk',
            relative_path='expression_matrices/first_dir/20230101/data1.h5ad',
            file_type='data',
            file_hash=file_1_checksum
        )
        self.file_attr_2 = CacheFileAttributes(
            url='junk',
            version=self.new_version,
            file_size=90210,
            local_path='junk',
            relative_path='expression_matrices/second_dir/20240101/data2.h5ad',
            file_type='data',
            file_hash=file_2_checksum
        )
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.file_attr_1.relative_path,
                               Body=file_1)
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.file_attr_2.relative_path,
                               Body=file_2)

        self.manifest_1 = add_directory_to_manifest(
            file_attribute=self.file_attr_1,
            manifest=self.manifest_1
        )
        self.manifest_2 = add_directory_to_manifest(
            file_attribute=self.file_attr_2,
            manifest=self.manifest_2
        )
        self.manifest_1 = add_file_to_manifest(
            file_attribute=self.file_attr_1,
            manifest=self.manifest_1
        )
        self.manifest_2 = add_file_to_manifest(
            file_attribute=self.file_attr_2,
            manifest=self.manifest_2
        )

        self.client.put_object(
            Bucket=self.test_bucket_name,
            Key=f'releases/{self.old_version}/manifest.json',
            Body=bytes(json.dumps(self.manifest_1), 'utf-8')
        )
        self.client.put_object(
            Bucket=self.test_bucket_name,
            Key=f'releases/{self.new_version}/manifest.json',
            Body=bytes(json.dumps(self.manifest_2), 'utf-8')
        )

    def test_abc_projet_cache_s3(self):
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
        assert cache.list_data_files("second_dir") == ["data2/log2"]
        assert cache.list_data_files("test_directory") == ["data_file/log2"]
        assert cache.list_metadata_files("test_directory") == [
            "metadata_file"
        ]
        # Test the directory from the older manifest is not available.
        with pytest.raises(KeyError, match="first_dir"):
            assert cache.list_data_files("first_dir")

        # Download data and test that the downloaded file exists on disk.
        data_path = cache.get_data_path(directory="second_dir",
                                        file_name="data2/log2")
        assert data_path.exists()
        assert data_path == self.cache_dir / self.file_attr_2.relative_path
        data_path = cache.get_data_path(directory="test_directory",
                                        file_name="data_file/log2")
        assert data_path.exists()
        assert data_path == self.cache_dir / self.new_data_path
        metadata_path = cache.get_metadata_path(directory="test_directory",
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
        assert cache.list_data_files("first_dir") == ["data1/log2"]
        assert cache.list_data_files("test_directory") == ["data_file/log2"]
        assert cache.list_metadata_files("test_directory") == [
            "metadata_file"
        ]
        # Test that the newer manifest's directory is not present.
        with pytest.raises(KeyError, match="second_dir"):
            assert cache.list_data_files("second_dir")

        # Download the older files and test for their expected paths.
        data_paths = cache.get_directory_data(directory="first_dir")
        assert data_paths[0].exists()
        assert data_paths == [self.cache_dir / self.file_attr_1.relative_path]
        data_paths = cache.get_directory_data(directory="test_directory")
        assert data_paths[0].exists()
        assert data_paths == [self.cache_dir / self.old_data_path]
        metadata_paths = cache.get_directory_metadata(
            directory="test_directory"
        )
        assert metadata_paths[0].exists()
        assert metadata_paths == [self.cache_dir / self.old_metadata_path]

        # Reload the most recent manifest and test that is as as expected.
        cache.load_latest_manifest()
        assert cache.current_manifest == f'releases/{self.new_version}/manifest.json'  # noqa: E501

    def test_abc_projet_cache_local_cache(self):
        """Run a suite of integration tests on the AbcProjectCache class
        from_local_cache.
        """
        AbcProjectCache._bucket_name = self.test_bucket_name
        cache = AbcProjectCache.from_s3_cache(self.cache_dir)

        # Download data into the local cache.
        cache.get_data_path(directory="second_dir",
                            file_name="data2/log2")
        cache.get_data_path(directory="test_directory",
                            file_name="data_file/log2")
        cache.get_metadata_path(directory="test_directory",
                                file_name="metadata_file")

        # Remove the previous cache object.
        del cache

        # Initialize a new cache object from the local cache.
        cache = AbcProjectCache.from_local_cache(self.cache_dir)
        assert cache.current_manifest == f'releases/{self.new_version}/manifest.json'
        assert cache.list_all_downloaded_manifests == [
            f'releases/{self.new_version}/manifest.json'
        ]

        data_path = cache.get_data_path(directory="second_dir",
                                        file_name="data2/log2")
        assert data_path.exists()
        assert data_path == self.cache_dir / self.file_attr_2.relative_path
        data_path = cache.get_data_path(directory="test_directory",
                                        file_name="data_file/log2")
        assert data_path.exists()
        assert data_path == self.cache_dir / self.new_data_path
        metadata_path = cache.get_metadata_path(directory="test_directory",
                                                file_name="metadata_file")
        assert metadata_path.exists()
        assert metadata_path == self.cache_dir / self.new_metadata_path

        data_paths = cache.get_directory_data(directory="test_directory")
        assert data_paths == [self.cache_dir / self.new_data_path]
        metadata_paths = cache.get_directory_metadata(
            directory="test_directory"
        )
        assert metadata_paths == [self.cache_dir / self.new_metadata_path]
