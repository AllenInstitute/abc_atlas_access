from typing import Optional
import boto3
from moto import mock_aws
import unittest
import tempfile
from pathlib import Path


def create_bucket(region_name: str,
                  bucket_name='test_bucket') -> boto3.client:
    conn = boto3.resource('s3', region_name=region_name)
    conn.create_bucket(Bucket=bucket_name, ACL='public-read')
    return boto3.client('s3', region_name=region_name)


def create_manifest_dict(version: str,
                         test_bucket_name: str = 'test_bucket',
                         data_file: str = 'data_file.h5ad',
                         metadata_file: str = 'metadata_file.csv',
                         test_directory: str = 'test_directory',
                         file_hash: Optional[str] = None,
                         location: str = 'us-east-1') -> dict:
    """
    Create a manifest dictionary for testing.

    Parameters
    ----------
    version: str
        The version of the test manifest.
    test_bucket_name: str
        The name of the test bucket.

    Returns
    -------
    test_manifest: dict
        Dictionary of test manifest values.
    """
    if file_hash is None:
        file_hash = f'abcd{version}'
    metadata_path = f"metadata/{test_directory}/{version}/{metadata_file}"
    data_path = f"expression_matrices/{test_directory}/{version}/{data_file}"
    test_manifest = {
        "version": version,
        "resource_uri": f"s3://{test_bucket_name}/",
        "directory_listing": {
            f"{test_directory}": {
                "directories": {
                    "expression_matrices": {
                        "version": version,
                        "relative_path": f"expression_matrices/{test_directory}/{version}",
                        "url": f"https://{test_bucket_name}.s3.{location}.amazonaws.com/expression_matrices/{test_directory}/{version}/",
                        "view_link": f"https://{test_bucket_name}.s3.{location}.amazonaws.com/index.html#expression_matrices/{test_directory}/{version}/",
                        "total_size": 1234
                    },
                    "metadata": {
                        "version": version,
                        "relative_path": f"metadata/{test_directory}/{version}",
                        "url": f"https://{test_bucket_name}.s3.{location}.amazonaws.com/metadata/{test_directory}/{version}/",
                        "view_link": f"https://{test_bucket_name}.s3.{location}.amazonaws.com/index.html#metadata/{test_directory}/{version}/",
                        "total_size": 5678
                    }
                }
            }
        },
        "file_listing": {
            f"{test_directory}": {
                "expression_matrices": {
                    data_file.split('.')[0]: {
                        "log2": {
                            "files": {
                                data_file.split('.')[1]: {
                                    "version": version,
                                    "relative_path": data_path,
                                    "url": f"https://{test_bucket_name}.s3.{location}.amazonaws.com/{data_path}",
                                    "size": 1234,
                                    "file_hash": file_hash
                                }
                            }
                        }
                    }
                },
                "metadata": {
                    metadata_file.split('.')[0]: {
                        "files": {
                            metadata_file.split('.')[1]: {
                                "version": version,
                                "relative_path": metadata_path,
                                "url": f"https://{test_bucket_name}.s3.{location}.amazonaws.com/{metadata_path}",
                                "size": 5678,
                                "file_hash": file_hash
                            }
                        }
                    }
                }
            }
        }
    }
    return test_manifest, metadata_path, data_path


@mock_aws
class BaseCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.test_bucket_name = 'abc_atlas_test_bucket'
        self.tmpdir = tempfile.TemporaryDirectory()
        self.cache_dir = Path(self.tmpdir.name).resolve()
        self._region = 'us-east-1'
        self.client = create_bucket(region_name=self._region,
                                    bucket_name=self.test_bucket_name)

    def tearDown(self):
        self.tmpdir.cleanup()