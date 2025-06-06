from typing import Optional, Union, List
from pathlib import Path
import logging
import os
import pandas as pd
import warnings

from abc_atlas_access.abc_atlas_cache.cloud_cache import (
    S3CloudCache,
    LocalCache
)


class AbcProjectCacheVersionException(Exception):
    pass


class LargeDataSizeWarning(UserWarning):
    pass


class FileMissingWarning(UserWarning):
    pass


def version_check(manifest_version: str,
                  cmin: str,
                  cmax: str):
    if manifest_version < cmin or manifest_version >= cmax:
        estr = (f"The manifest has manifest_version {manifest_version} but "
                "but othe AbcProjectCache is compatible only with "
                f"manifest versions on or after {cmin} and bevore {cmax}. "
                "Please download a previous version of the abc_atlas_access "
                "repo if you need to access a release older than this.")
        raise AbcProjectCacheVersionException(estr)


class AbcProjectCache(object):
    MANIFEST_COMPATIBILITY = ["20230101", "20300101"]
    _bucket_name = "allen-brain-cell-atlas"
    """API for downloading data released on S3 and returning tables.

    Parameters
    ----------
    cache: S3CloudCache or LocalCache
        an instantiated S3CloudCache/LocalCache object, which has already run
        `self.load_manifest()` 
    local: bool
        Whether to operate in local mode, where no data will be downloaded
        and instead will be loaded from local
    """
    def __init__(
        self,
        cache: Union[S3CloudCache, LocalCache],
        skip_version_check: bool = False,
        local: bool = False
    ):
        self.cache = cache
        self.skip_version_check = skip_version_check
        self._local = local
        self.load_manifest()
        self._ui_class_name = self.__class__.__name__
        self.logger = logging.getLogger(self._ui_class_name)

    @property
    def latest_manifest_file(self) -> str:
        """
        Return the name of the most up-to-date data manifest
        corresponding to this dataset, checking in the cloud
        if this is a cloud-backed cache.
        """
        return self.cache.latest_manifest_file

    def load_manifest(self, manifest_name: Optional[str] = None):
        """
        Load the specified manifest file into the CloudCache

        Parameters
        ----------
        manifest_name: Optional[str]
            Name of manifest file to load. If None, load latest
            (default: None)
        """
        if manifest_name is None:
            self.cache.load_last_manifest()
        else:
            self.cache.load_manifest(manifest_name)

        if not self.skip_version_check:
            version_check(
                self.cache.version,
                cmin=self.MANIFEST_COMPATIBILITY[0],
                cmax=self.MANIFEST_COMPATIBILITY[1])

    @classmethod
    def from_s3_cache(
        cls,
        cache_dir: Union[str, Path]
    ) -> "ProjectCloudApiBase":
        """Instantiates this object with a connection to a s3 bucket and/or
        a local cache related to that bucket. Will download data from s3 and
        store it in the local cache if it is not already present.

        Parameters
        ----------
        cache_dir: str or pathlib.Path
            Path to the directory where data will be stored on the local system

        Returns
        -------
        BehaviorProjectCloudApi instance
        """
        cache = S3CloudCache(cache_dir=cache_dir,
                             bucket_name=cls._bucket_name,
                             ui_class_name=cls.__class__.__name__)
        return cls(cache)

    @classmethod
    def from_local_cache(
        cls,
        cache_dir: Union[str, Path],
    ) -> "ProjectCloudApiBase":
        """Instantiates this object with a local cache where the data has
        already been downloaded to disk via a s3 cache.

        Parameters
        ----------
        cache_dir: str or pathlib.Path
            Path to the directory where data will be stored on the local system

        Returns
        -------
        ProjectCloudApiBase instance
        """
        cache = LocalCache(
            cache_dir,
            ui_class_name=cls.__class__.__name__
        )
        return cls(cache, local=True)

    @classmethod
    def from_cache_dir(
            cls,
            cache_dir: Union[str, Path],
    ) -> "ProjectCloudApiBase":
        """Instantiate either a local_cache or s3_cache instance of the class.

        Tests if user has write access to the directory, instantiate a s3_cache
        else instantiate a local_cache.

        Parameters
        ----------
        cache_dir: str or pathlib.Path
            Path to the directory where data will be stored on the local system

        Returns
        -------
        ProjectCloudApiBase instance
        """
        cache_dir = Path(cache_dir)
        # If the directory does not exist or we have write access to it
        # we will use the s3 cache. Else we will use the local cache.
        if not cache_dir.exists() or os.access(cache_dir, os.W_OK):
            return cls.from_s3_cache(cache_dir)
        elif cache_dir.exists() and not os.access(cache_dir, os.W_OK):
            return cls.from_local_cache(cache_dir)
        else:
            raise RuntimeError("Could not access or create cache directory.")

    def compare_manifests(self,
                          manifest_newer_name: str,
                          manifest_older_name: str
                          ) -> dict:
        """
        Compare two manifests from this dataset. Return a dict
        containing the list of metadata and data files that changed
        between them

        Note: this assumes that manifest_0 predates manifest_1

        Parameters
        ----------
        manifest_newer_name: str
            Name of the newer manifest to load.
        manifest_older_name: str
            Name of the older manifest to load.

        Returns
        -------
        dict
            A dictionary summarizing all of the changes going from
            manifest_0 to manifest_1
        """
        return self.cache.compare_manifests(manifest_newer_name,
                                            manifest_older_name)

    def load_latest_manifest(self):
        """
        Load the manifest corresponding to the most up to date
        version of the dataset.
        """
        self.cache.load_latest_manifest()
        self.load_manifest(self.current_manifest)

    @property
    def latest_downloaded_manifest_file(self) -> str:
        """
        Return the name of the most up to date data manifest
        available on your local system.
        """
        return self.cache.latest_downloaded_manifest_file

    @property
    def list_all_downloaded_manifests(self) -> list:
        """
        Return a sorted list of the names of the manifest files
        that have been downloaded to this cache.
        """
        return self.cache.list_all_downloaded_manifests()

    @property
    def list_manifest_file_names(self) -> list:
        """
        Return a sorted list of the names of the manifest files
        associated with this dataset.
        """
        return self.cache.manifest_file_names

    @property
    def current_manifest(self) -> Union[None, str]:
        """
        Return the name of the dataset manifest currently being
        used by this cache.
        """
        return self.cache.current_manifest

    @property
    def list_directories(self) -> List[str]:
        """
        Return a list of the directories in the cache
        """
        return self.cache.list_directories

    def list_metadata_files(self, directory: str) -> List[str]:
        """
        Return a list of all metadata files in a directory both downloaded and
        not.
        """
        return self.cache.list_metadata_files(directory)

    def list_expression_matrix_files(self, directory: str) -> List[str]:
        """
        Return a list of all expression matrix files in a directory both
        downloaded and not.
        """
        return self.cache.list_expression_matrix_files(directory)
    
    def list_image_volume_files(self, directory: str) -> List[str]:
        """
        Return a list of all image volume files in a directory both
        downloaded and not.
        """
        return self.cache.list_image_volume_files(directory)
    
    def list_mapmycells_files(self, directory: str) -> List[str]:
        """
        Return a list of all mapmycells files in a directory both
        downloaded and not.
        """
        return self.cache.list_mapmycells_files(directory)
    
    def _get_directory_files(
            self,
            directory: str,
            data_kind: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ) -> List[Path]:
        """
        Return a list of all files in a directory. If the cache is local,
        this will return the local paths to the available files. If the cache
        is not local, this will download the files if needed and return the
        local paths to the downloaded files.

        Parameters
        ----------
        directory: str
            The directory in which the data files are stored.
        data_kind: str
            The kind of data to retrieve (e.g., 'metadata', 'data').
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.

        Returns
        -------
        data_paths: List[Path]
            List of local paths to the downloaded data files.
        """
        if self._local:
            data_files = self.cache.list_files(directory, data_kind)
            output_paths = []
            for file_name in data_files:
                try:
                    output_paths.append(self.cache.get_file_path(
                        directory=directory,
                        file_name=file_name,
                    )['local_path'])
                except FileNotFoundError:
                    warnings.warn(
                        message=f"Expected file: {file_name} in "
                                f"directory: {directory} was not found in "
                                "the local cache.",
                        category=FileMissingWarning
                    )
            return output_paths
        else:
            self._warn_directory_size(directory=directory,
                                      data_kind=data_kind)
            return self.cache.download_directory(
                directory=directory,
                data_kind=data_kind,
                force_download=force_download,
                skip_hash_check=skip_hash_check
            )

    def get_directory_metadata(
            self,
            directory: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ) -> List[Path]:
        """
        Return a list of all paths to all metadata files in a directory. If the
        cache is local, this will return the local paths to the available
        metadata files. If the cache is not local, this will download the
        metadata files if needed and return the local paths to the downloaded
        metadata files.

        Parameters
        ----------
        directory: str
            The directory in which the data files are stored.
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.


        Returns
        -------
        data_paths: List[Path]
            List of local paths to the downloaded data files.
        """
        return self._get_directory_files(
            directory=directory,
            data_kind='metadata',
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )

    def get_directory_expression_matrices(
            self,
            directory: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ) -> List[Path]:
        """
        Return a list of all expression matrix files in a directory. If the
        cache is local, this will return the local paths to the available
        expression matrix files. If the cache is not local, this will download
        the expression matrix files if needed and return the local paths to
        the downloaded expression matrix files.

        Parameters
        ----------
        directory: str
            The directory in which the data files are stored.
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.

        Returns
        -------
        data_paths: List[Path]
            List of local paths to the downloaded data files.
        """
        return self._get_directory_files(
            directory=directory,
            data_kind='expression_matrices',
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )
    
    def get_directory_image_volumes(
            self,
            directory: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ) -> List[Path]:
        """
        Return a list of all image volume files in a directory. If the
        cache is local, this will return the local paths to the available
        image volume files. If the cache is not local, this will download
        the image volume files if needed and return the local paths to
        the downloaded image volume files.

        Parameters
        ----------
        directory: str
            The directory in which the data files are stored.
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.

        Returns
        -------
        data_paths: List[Path]
            List of local paths to the downloaded data files.
        """
        return self._get_directory_files(
            directory=directory,
            data_kind='image_volumes',
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )
    
    def get_directory_mapmycells(
            self,
            directory: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ) -> List[Path]:
        """
        Return a list of all mapmycells files in a directory. If the
        cache is local, this will return the local paths to the available
        mapmycells files. If the cache is not local, this will download
        the mapmycells files if needed and return the local paths to
        the downloaded mapmycells files.

        Parameters
        ----------
        directory: str
            The directory in which the data files are stored.
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.

        Returns
        -------
        data_paths: List[Path]
            List of local paths to the downloaded data files.
        """
        return self._get_directory_files(
            directory=directory,
            data_kind='mapmycells',
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )

    def _warn_directory_size(self, directory: str, data_kind: str):
        """
        Warn the user if the directory they are downloading contains a
        significant amount of data.

        Parameters
        ----------
        directory: str
            The directory in which the data files are stored.
        is_metadata
            If True, warn about the size of the metadata directory. If False,
            warn about the size of the data directory.
        """
        size = self.get_directory_size_by_kind(
            directory=directory,
            data_kind=data_kind
        )
        unit = size.split(' ')[1]
        size = float(size.split(' ')[0])
        if unit == 'GB' and size > 10:
            warnings.warn(
                message=f'{directory} contains a significant amount of data.'
                        'Continue this download only if you are sure you have '
                        'enough space on your system.\n\n'
                        f'\tTotal directory size = {size} GB\n\n',
                category=LargeDataSizeWarning)
            
    def get_data_path(
            self,
            directory: str,
            file_name: str,
            force_download: bool = False,
            skip_hash_check: bool = False
        ):
        warnings.warn(
            "get_data_path is deprecated and will be removed in a future release. "
            "Use get_file_path instead.",
            DeprecationWarning
        )
        return self.get_file_path(
            directory=directory,
            file_name=file_name,
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )
    
    def get_metadata_path(
            self,
            directory: str,
            file_name: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ):
        warnings.warn(
            "get_metadata_path is deprecated and will be removed in a future release. "
            "Use get_file_path instead.",
            DeprecationWarning
        )
        return self.get_file_path(
            directory=directory,
            file_name=file_name,
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )
                          
            
    def get_file_path(
            self,
            directory: str,
            file_name: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ) -> dict:
        """
        Return the path to a downloaded file. Download the file if
        using a S3Cache and the file is not currently on disk.

        Parameters
        ----------
        directory: str
            The directory in which the data file is stored.
        file_name: str
            The name of the data file.
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.

        Returns
        -------
        file_path: dict
            Dictionary containing 'exists' (bool) and 'local_path' (Path) keys.
        """
        if self._local:
            return self.cache.get_file_path(
                directory=directory,
                file_name=file_name
            )['local_path']
        else:
            return self.cache.download_file(
                directory=directory,
                file_name=file_name,
                force_download=force_download,
                skip_hash_check=skip_hash_check
            )

    def get_metadata_dataframe(
            self,
            directory: str,
            file_name: str,
            force_download: bool = False,
            skip_hash_check: bool = False,
            **kwargs
    ) -> pd.DataFrame:
        """
        Get the metadata table with the given file name. Download the file if
        using a S3Cache and the file is not currently on disk.

        Parameters
        ----------
        directory: str
            The directory in which the metadata file is stored.
        file_name: str
            The name of the metadata file.
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.
        **kwargs
           Keyword arguments to pass to pandas.read_csv

        Returns
        -------
        data_frame: pandas.DataFrame
            Dataframe of the requested metadata file.
        """
        path = self.get_file_path(
            directory=directory,
            file_name=file_name,
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )
        return pd.read_csv(path, **kwargs)

    def _get_local_path(
            self,
            directory: str,
            file_name: str,
            is_metadata: bool = False
    ):
        if is_metadata:
            path = self.cache.metadata_path(
                directory=directory,
                file_name=file_name,
            )
        else:
            path = self.cache.data_path(
                directory=directory,
                file_name=file_name,
            )

        exists = path['exists']
        local_path = path['local_path']
        if not exists:
            raise FileNotFoundError(f'You started a cache without a '
                                    f'connection to s3 and {local_path} is '
                                    'not already on your system')
        return local_path
    
    def get_directory_size_by_kind(
            self,
            directory: str,
            data_kind: str
    ) -> str:
        """
        Return the size of the directory in an appropriate unit (GB or MB).

        Parameters
        ----------
        directory: str
            The directory in which the data file is stored.
        data_kind: str
            The kind of data to retrieve (e.g., 'metadata', 'data').

        Returns
        -------
        size: str
            The size of the directory in bytes.
        """
        return self.cache.get_directory_size_by_kind(directory, data_kind)

    def get_directory_metadata_size(self, directory: str) -> str:
        """
        Return the size of the metadata in the requested directory in an
        appropriate unit (GB or MB).

        Parameters
        ----------
        directory: str
            The directory in which the metadata file is stored.

        Returns
        -------
        size: str
            The size of the directory in bytes.
        """
        return self.cache.get_directory_metadata_size(directory)

    def get_directory_expression_matrix_size(self, directory: str) -> str:
        """
        Return the size of the data in the requested directory in an
        appropriate unit (GB or MB).

        Parameters
        ----------
        directory: str
            The directory in which the data file is stored.

        Returns
        -------
        size: str
            The size of the directory in bytes.
        """
        return self.cache.get_directory_expression_matrix_size(directory)
    
    def get_directory_image_volume_size(self, directory: str) -> str:
        """
        Return the size of the image volumes in the requested directory in an
        appropriate unit (GB or MB).

        Parameters
        ----------
        directory: str
            The directory in which the image volume file is stored.

        Returns
        -------
        size: str
            The size of the directory in bytes.
        """
        return self.cache.get_directory_image_volume_size(directory)
    
    def get_directory_mapmycells_size(self, directory: str) -> str:
        """
        Return the size of the mapmycells files in the requested directory in an
        appropriate unit (GB or MB).

        Parameters
        ----------
        directory: str
            The directory in which the mapmycells file is stored.

        Returns
        -------
        size: str
            The size of the directory in bytes.
        """
        return self.cache.get_directory_mapmycells_size(directory)
