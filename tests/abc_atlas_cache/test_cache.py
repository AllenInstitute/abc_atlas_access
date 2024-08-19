import datetime
import hashlib
import warnings

import pytest
from pathlib import Path
from moto import mock_aws
import json

from abc_atlas_access.abc_atlas_cache.file_attributes import \
    CacheFileAttributes
from abc_atlas_access.abc_atlas_cache.cloud_cache import (
    S3CloudCache,
    OutdatedManifestWarning
)
from .utils import create_manifest_dict, BaseCacheTestCase, hash_data


@mock_aws
class TestCache(BaseCacheTestCase):

    def setUp(self):
        super().setUp()
        self.old_version = "20230101"
        self.new_version = "20240101"
        self.old_manifest_string = f'releases/{self.old_version}/manifest.json'
        self.new_manifest_string = f'releases/{self.new_version}/manifest.json'

    def create_manifests(self, manifest_count):
        manifest_list = []
        for day in range(manifest_count):
            version = (datetime.date(year=2020, month=1, day=1)
                       + datetime.timedelta(days=day)).strftime('%Y%m%d')
            manifest, _, _ = create_manifest_dict(
                version=version,
                test_bucket_name=self.test_bucket_name
            )
            manifest_string = f'releases/{version}/manifest.json'
            self.client.put_object(
                Bucket=self.test_bucket_name,
                Key=manifest_string,
                Body=json.dumps(manifest)
            )
            manifest_list.append(manifest_string)
        return manifest_list

    def test_list_all_manifests(self):
        """
        Test that S3CloudCache.list_al_manifests() returns the correct result
        """
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.old_manifest_string,
                               Body=b'123456')
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.new_manifest_string,
                               Body=b'123456')
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key='junk.txt',
                               Body=b'123456')

        cache = S3CloudCache(cache_dir=self.cache_dir,
                             bucket_name=self.test_bucket_name)

        assert cache.manifest_file_names == [
            self.old_manifest_string,
            self.new_manifest_string
        ]

    def test_list_all_manifests_many(self):
        """
        Test the extreme case when there are more manifests than
        list_objects_v2 can return at a time
        """
        expected = self.create_manifests(manifest_count=2000)
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key='junk.txt',
                               Body=b'123456')

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)
        expected.sort()
        assert cache.manifest_file_names == expected

    def test_loading_manifest(self):
        """
        Test loading manifests with S3CloudCache
        """
        manifest_1, _, _ = create_manifest_dict(
            version=self.old_version,
            test_bucket_name=self.test_bucket_name
        )
        manifest_2, _, _ = create_manifest_dict(
            version=self.new_version,
            test_bucket_name=self.test_bucket_name
        )

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.old_manifest_string,
                               Body=bytes(json.dumps(manifest_1), 'utf-8'))

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.new_manifest_string,
                               Body=bytes(json.dumps(manifest_2), 'utf-8'))

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)
        assert cache.current_manifest is None
        cache.load_manifest(self.old_manifest_string)
        assert cache._manifest._data == manifest_1
        assert cache.version == self.old_version
        assert cache.current_manifest == self.old_manifest_string

        cache.load_manifest(self.new_manifest_string)
        assert cache._manifest._data == manifest_2
        assert cache.version == self.new_version
        assert cache.current_manifest == self.new_manifest_string

        with pytest.raises(ValueError) as context:
            cache.load_manifest('releases/20200101/manifest.json')
        msg = 'is not one of the valid manifest names'
        assert msg in context.value.args[0]

    def test_file_exists(self):
        """
        Test that cache._file_exists behaves correctly
        """
        data = b'aakderasjklsafetss77123523asf'
        true_checksum = hash_data(data)
        test_file_path = self.cache_dir / 'junk.txt'
        with open(test_file_path, 'wb') as out_file:
            out_file.write(data)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        # should be true
        good_attribute = CacheFileAttributes(url='http://silly.url.com',
                                             version=self.new_version,
                                             file_size=1234,
                                             local_path=test_file_path,
                                             relative_path='junk.txt',
                                             file_type='txt',
                                             file_hash=true_checksum)
        assert cache._file_exists(good_attribute)

        # test when file path is wrong
        bad_path = Path('definitely/not/a/file.txt')
        bad_attribute = CacheFileAttributes(url='http://silly.url.com',
                                            version=self.new_version,
                                            file_size=1234,
                                            local_path=bad_path,
                                            relative_path='junk.txt',
                                            file_type='txt',
                                            file_hash=true_checksum)

        assert not cache._file_exists(bad_attribute)

        # test when path exists but is not a file
        bad_attribute = CacheFileAttributes(url='http://silly.url.com',
                                            version=self.new_version,
                                            file_size=1234,
                                            local_path=self.cache_dir,
                                            relative_path='junk.txt',
                                            file_type='txt',
                                            file_hash=true_checksum)
        with pytest.raises(RuntimeError, match='but is not a file'):
            cache._file_exists(bad_attribute)

    def test_download_file(self):
        """
        Test that S3CloudCache._download_file behaves as expected
        """
        data = b'11235813kjlssergwesvsdd'
        true_checksum = hash_data(data)
        relative_path = 'data/data_file.txt'

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key='data/data_file.txt',
                               Body=data)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        expected_path = self.cache_dir / 'data/data_file.txt'

        url = f'http://{self.test_bucket_name}.s3.amazonaws.com/data/data_file.txt'  # noqa: E501
        good_attributes = CacheFileAttributes(url=url,
                                              version=self.new_version,
                                              file_size=1234,
                                              local_path=expected_path,
                                              relative_path=relative_path,
                                              file_type='txt',
                                              file_hash=true_checksum)

        assert not expected_path.exists()
        cache._download_file(good_attributes)
        assert expected_path.exists()
        hasher = hashlib.md5()
        with open(expected_path, 'rb') as in_file:
            hasher.update(in_file.read())
        assert hasher.hexdigest() == true_checksum

    def test_re_download_file(self):
        """
        Test that S3CloudCache._download_file will re-download a file
        when it has been removed from the local system
        """
        data = b'11235813kjlssergwesvsdd'
        true_checksum = hash_data(data)
        relative_path = 'data/data_file.txt'

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=relative_path,
                               Body=data)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        expected_path = self.cache_dir / relative_path

        url = f'http://{self.test_bucket_name}.s3.amazonaws.com/data/data_file.txt'  # noqa: E501
        good_attributes = CacheFileAttributes(url=url,
                                              version=self.new_version,
                                              file_size=1234,
                                              local_path=expected_path,
                                              relative_path=relative_path,
                                              file_type='txt',
                                              file_hash=true_checksum)

        assert not expected_path.exists()
        cache._download_file(good_attributes)
        assert expected_path.exists()
        hasher = hashlib.md5()
        with open(expected_path, 'rb') as in_file:
            hasher.update(in_file.read())
        assert hasher.hexdigest() == true_checksum

        # now, remove the file, and see if it gets re-downloaded
        expected_path.unlink()
        assert not expected_path.exists()

        cache._download_file(good_attributes)
        assert expected_path.exists()
        hasher = hashlib.md5()
        with open(expected_path, 'rb') as in_file:
            hasher.update(in_file.read())
        assert hasher.hexdigest() == true_checksum

    def test_download_data(self):
        """
        Test that S3CloudCache.download_data() returns a correctly formatted
        CacheFileAttributes object.
        """
        data = b'11235813kjlssergwesvsdd'
        true_checksum = hash_data(data)

        version = self.new_version
        manifest, metadata_path, data_path = create_manifest_dict(
            version=version,
            test_bucket_name=self.test_bucket_name,
            file_hash=true_checksum
        )

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=metadata_path,
                               Body=data)
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=data_path,
                               Body=data)

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.new_manifest_string,
                               Body=bytes(json.dumps(manifest), 'utf-8'))

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        cache.load_manifest(self.new_manifest_string)

        expected_path = (self.cache_dir / data_path)
        assert not expected_path.exists()

        # test data_path
        directory = data_path.split('/')[1]
        attr = cache.data_path(
            directory=directory,
            file_name=f"{data_path.split('/')[-1].split('.')[0]}/log2"
        )
        assert attr['local_path'] == expected_path
        assert not attr['exists']

        expected_path = self.cache_dir / metadata_path
        assert not expected_path.exists()

        directory = metadata_path.split('/')[1]
        attr = cache.metadata_path(
            directory,
            metadata_path.split('/')[-1].split('.')[0]
        )
        assert attr['local_path'] == expected_path
        assert not attr['exists']

    def test_latest_manifest(self):
        """
        Test that the methods which return the latest and latest downloaded
        manifest file names work correctly
        """
        manifest_list = self.create_manifests(manifest_count=5)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        assert cache.latest_downloaded_manifest_file == ''

        cache.load_manifest(manifest_list[2])
        cache.load_manifest(manifest_list[0])
        cache.load_manifest(manifest_list[1])

        assert cache.latest_manifest_file == manifest_list[-1]

        expected = manifest_list[2]
        assert cache.latest_downloaded_manifest_file == expected

    def test_outdated_manifest_warning(self):
        """
        Test that a warning is raised the first time you try to load an
        outdated manifest
        """
        manifest_list = self.create_manifests(manifest_count=5)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        m_warn_type = 'OutdatedManifestWarning'

        with pytest.warns(
                OutdatedManifestWarning,
                match='The manifest file you are loading is not the most up '
                      'to date manifest file'
        ):
            cache.load_manifest(manifest_list[0])

        # assert no warning is raised the second time by catching
        # any warnings that are emitted.
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            cache.load_manifest(manifest_list[2])

    def test_list_all_downloaded(self):
        """
        Test that list_all_downloaded_manifests works
        """
        manifest_list = self.create_manifests(manifest_count=5)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        assert cache.list_all_downloaded_manifests() == []

        cache.load_manifest(manifest_list[3])
        assert cache.current_manifest == manifest_list[3]
        cache.load_manifest(manifest_list[0])
        assert cache.current_manifest == manifest_list[0]
        cache.load_manifest(manifest_list[2])
        assert cache.current_manifest == manifest_list[2]

        expected = {manifest_list[3],
                    manifest_list[0],
                    manifest_list[2]}
        downloaded = set(cache.list_all_downloaded_manifests())
        assert downloaded == expected

    def test_latest_manifest_warning(self):
        """
        Test that the correct warning is emitted when the user tries
        to load_latest_manifest but that has not been downloaded yet
        """
        manifest_list = self.create_manifests(manifest_count=5)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        cache.load_manifest(manifest_list[1])

        with pytest.warns(OutdatedManifestWarning) as warn:
            cache.load_latest_manifest()
        assert len(warn) == 1
        msg = str(warn[0].message)
        assert manifest_list[1] in msg
        assert manifest_list[-1] in msg
        assert 'It is possible that some data files' in msg
        cmd = f"S3CloudCache.load_manifest('{manifest_list[1]}')"
        assert cmd in msg

    def test_load_last_manifest(self):
        """
        Test that load_last_manifest works
        """
        manifest_list = self.create_manifests(manifest_count=5)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        # check that load_last_manifest in a new cache loads the
        # latest manifest without emitting a warning
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            cache.load_last_manifest()
        assert cache.current_manifest == manifest_list[-1]

        cache.load_manifest(manifest_list[2])

        del cache

        # check that load_last_manifest on an old cache emits the
        # expected warning and loads the correct manifest
        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)
        expected = ('A more up to date version of the '
                    f'dataset -- {manifest_list[-1]} '
                    '-- exists online')
        with pytest.warns(OutdatedManifestWarning,
                          match=expected):
            cache.load_last_manifest()

        assert cache.current_manifest == manifest_list[2]
        cache.load_manifest(manifest_list[0])
        del cache

        # repeat the above test, making sure the correct manifest is
        # loaded again
        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)
        expected = ('A more up to date version of the '
                    f'dataset -- {manifest_list[-1]} '
                    '-- exists online')
        with pytest.warns(OutdatedManifestWarning,
                          match=expected):
            cache.load_last_manifest()

        assert cache.current_manifest == manifest_list[0]

    def test_corrupted_load_last_manifest(self):
        """
        Test that load_last_manifest works when the record of the last
        manifest has been corrupted
        """
        manifest_list = self.create_manifests(manifest_count=5)

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)
        cache.load_manifest(manifest_list[-2])
        fname = cache._manifest_last_used.resolve()
        del cache
        with open(fname, 'w') as out_file:
            out_file.write('babababa')
        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)
        expected = f'Loading latest version -- {manifest_list[-1]}'
        with pytest.warns(UserWarning, match=expected):
            cache.load_last_manifest()
        assert cache.current_manifest == manifest_list[-1]

    def test_download_directory(self):
        """
        Test that S3CloudCache.download_directory() correctly downloads files
        from S3.
        """
        data = b'11235813kjlssergwesvsdd'
        true_checksum = hash_data(data)

        version = self.new_version
        manifest, metadata_path, data_path = create_manifest_dict(
            version=version,
            test_bucket_name=self.test_bucket_name,
            file_hash=true_checksum
        )

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=metadata_path,
                               Body=data)
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=data_path,
                               Body=data)

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.new_manifest_string,
                               Body=bytes(json.dumps(manifest), 'utf-8'))

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        cache.load_manifest(self.new_manifest_string)

        expected_data_path = (self.cache_dir / data_path)
        assert not expected_data_path.exists()
        expected_metadata_path = (self.cache_dir / metadata_path)
        assert not expected_metadata_path.exists()

        # test data_path
        directory = data_path.split('/')[1]
        data_path_list = cache.download_directory_data(
            directory=directory
        )
        assert data_path_list == [expected_data_path]
        assert expected_data_path.exists()

        expected_path = self.cache_dir / metadata_path
        assert not expected_path.exists()

        directory = metadata_path.split('/')[1]
        metadata_path_list = cache.download_directory_metadata(
            directory
        )
        assert metadata_path_list == [expected_path]
        assert expected_path.exists()

    def test_hashing_check(self):
        """
        Test that the hash check works correctly.
        """
        data = b'11235813kjlssergwesvsdd'

        version = self.new_version
        manifest, metadata_path, data_path = create_manifest_dict(
            version=version,
            test_bucket_name=self.test_bucket_name,
            file_hash='junk'
        )

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=metadata_path,
                               Body=data)
        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=data_path,
                               Body=data)

        self.client.put_object(Bucket=self.test_bucket_name,
                               Key=self.new_manifest_string,
                               Body=bytes(json.dumps(manifest), 'utf-8'))

        cache = S3CloudCache(self.cache_dir, self.test_bucket_name)

        cache.load_manifest(self.new_manifest_string)

        expected_data_path = (self.cache_dir / data_path)
        assert not expected_data_path.exists()
        expected_metadata_path = (self.cache_dir / metadata_path)
        assert not expected_metadata_path.exists()

        # test data_path fails on bad hash.
        directory = data_path.split('/')[1]
        with pytest.raises(RuntimeError,
                           match=f"Could not download {data_path}"):
            cache.download_data(
                directory=directory,
                file_name=f"{data_path.split('/')[-1].split('.')[0]}/log2"
            )
        assert not expected_data_path.exists()
        # test download_metadta fails on bad hash.
        with pytest.raises(RuntimeError,
                           match=f"Could not download {metadata_path}"):
            cache.download_metadata(
                directory=directory,
                file_name=metadata_path.split('/')[-1].split('.')[0]
            )
        assert not expected_metadata_path.exists()

        full_data_path = cache.download_data(
            directory=directory,
            file_name=f"{data_path.split('/')[-1].split('.')[0]}/log2",
            skip_hash_check=True
        )
        assert full_data_path.exists()
        assert full_data_path == expected_data_path
        full_metadata_path = cache.download_metadata(
            directory=directory,
            file_name=metadata_path.split('/')[-1].split('.')[0],
            skip_hash_check=True
        )
        assert full_metadata_path.exists()
        assert full_metadata_path == expected_metadata_path
