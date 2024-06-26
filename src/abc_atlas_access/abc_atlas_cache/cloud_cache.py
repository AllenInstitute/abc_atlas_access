from typing import List, Optional, Union
from abc import ABC, abstractmethod
from pathlib import Path
import json
import warnings
import tqdm
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from abc_atlas_access.abc_atlas_cache.manifest import (
    Manifest,
    DataTypeNotInDirectory
)
from abc_atlas_access.abc_atlas_cache.file_attributes import CacheFileAttributes  # noqa: E501
from abc_atlas_access.abc_atlas_cache.utils import file_hash_from_path


class OutdatedManifestWarning(UserWarning):
    pass


class MissingLocalManifestWarning(UserWarning):
    pass


class ReadOnlyLocalCacheWarning(UserWarning):
    pass


class BasicLocalCache(ABC):
    """
    A class to handle the loading and accessing a project's data and
    metadata from a local cache directory. Does NOT include any 'smart'
    features like:
    1. Keeping track of last loaded manifest
    2. Warning of outdated manifests

    For those features (and more) see the CloudCacheBase class

    Parameters
    ----------
    cache_dir: str or pathlib.Path
        Path to the directory where data and metadata are stored on the
        local system
    ui_class_name: Optional[str]
        Name of the class users are actually using to manipulate this
        functionality (used to populate helpful error messages)
    """

    def __init__(
        self,
        cache_dir: Union[str, Path],
        ui_class_name: Optional[str] = None
    ):
        if isinstance(cache_dir, str):
            cache_dir = Path(cache_dir)
        cache_dir.mkdir(exist_ok=True, parents=True)

        # the class users are actually interacting with
        # (for warning message purposes)
        if ui_class_name is None:
            self._user_interface_class = type(self).__name__
        else:
            self._user_interface_class = ui_class_name

        self._manifest = None
        self._manifest_name = None

        self._cache_dir = Path(cache_dir)

        self._manifest_file_names = self._list_all_manifests()

    # ====================== BasicLocalCache properties =======================

    @property
    def ui(self):
        return self._user_interface_class

    @property
    def current_manifest(self) -> Union[None, str]:
        """The name of the currently loaded manifest"""
        return self._manifest_name

    @property
    def manifest_prefix(self) -> str:
        """On-line prefix for manifest files"""
        return 'releases/'

    @property
    def version(self) -> str:
        """The version of the dataset currently loaded"""
        return self._manifest.version

    @property
    def manifest_file_names(self) -> list:
        """Sorted list of manifest file names associated with this dataset
        """
        return self._manifest_file_names

    @property
    def list_directories(self) -> List[str]:
        """List of directories associated with this dataset"""
        return self._manifest.list_directories

    @property
    def latest_manifest_file(self) -> str:
        """parses on-line available manifest files for a version/date string
        and returns the latest one
        self.manifest_file_names are assumed to be of the form
        '*/<version>/manifest.json'

        Returns
        -------
        str
            the filename whose semver string is the latest one
        """
        return max(self.manifest_file_names)

    @property
    def cache_dir(self) -> Path:
        """Return the cache directory path.

        Returns
        -------
        str
            Full cache directory path
        """
        return self._cache_dir

    # ====================== BasicLocalCache methods ==========================

    def list_metadata_files(self, directory: str) -> List[str]:
        """
        List the metadata files in a directory

        Parameters
        ----------
        directory: str
            The name of the directory containing the metadata files

        Returns
        -------
        List[str]
            List of metadata files in the directory
        """
        return self._manifest.list_metadata_files(directory)

    def list_data_files(self, directory: str) -> List[str]:
        """
        List the data files in a directory

        Parameters
        ----------
        directory: str
            The name of the directory containing the data files

        Returns
        -------
        List[str]
            List of data files in the directory
        """
        return self._manifest.list_data_files(directory)

    @abstractmethod
    def _list_all_manifests(self) -> list:
        """
        Return a list of all of the file names of the manifests associated
        with this dataset
        """
        raise NotImplementedError()

    def list_all_downloaded_manifests(self) -> list:
        """
        Return a list of all of the manifest files that have been
        downloaded for this dataset
        """
        output = [self.manifest_prefix + str(x).split('releases/')[-1]
                  for x in self.cache_dir.glob("releases/*/manifest.json")]
        output.sort()
        return output

    def _load_manifest(
        self,
        manifest_name: str,
    ) -> Manifest:
        """
        Load and return a manifest from this dataset.

        Parameters
        ----------
        manifest_name: str
            The name of the manifest to load. Must be an element in
            self.manifest_file_names

        Returns
        -------
        Manifest
        """
        if manifest_name not in self.manifest_file_names:
            raise ValueError(
                f"Manifest to load ({manifest_name}) is not one of the "
                "valid manifest names for this dataset. Valid names include:\n"
                f"{self.manifest_file_names}"
            )

        manifest_path = self._cache_dir / manifest_name

        with open(manifest_path, "r") as f:
            local_manifest = Manifest(
                cache_dir=self._cache_dir,
                json_input=f,
            )

        return local_manifest

    def load_manifest(self, manifest_name: str):
        """
        Load a manifest from this dataset.

        Parameters
        ----------
        manifest_name: str
            The name of the manifest to load. Must be an element in
            self.manifest_file_names
        """
        self._manifest = self._load_manifest(manifest_name)
        self._manifest_name = manifest_name

    def get_directory_metadata_size(self, directory: str) -> str:
        """
        Return the size of a metadata directory in gigabytes or megabytes,
        which ever is appropriate.

        Parameters
        ----------
        directory: str
            The name of the directory containing the metadata files

        Returns
        -------
        size: str
            The size of the directory in bytes
        """
        return self._manifest.get_directory_metadata_size(directory)

    def get_directory_data_size(self, directory: str) -> str:
        """
        Return the size of a data directory in gigabytes or megabytes,
        which ever is appropriate.

        Parameters
        ----------
        directory: str
            The name of the directory containing the data files

        Returns
        -------
        size: str
            The size of the directory in bytes
        """
        return self._manifest.get_directory_data_size(directory)

    def _file_exists(self, file_attributes: CacheFileAttributes) -> bool:
        """
        Given a CacheFileAttributes describing a file, assess whether or
        not that file exists locally.

        Parameters
        ----------
        file_attributes: CacheFileAttributes
            Description of the file to look for

        Returns
        -------
        bool
            True if the file exists and is valid; False otherwise

        Raises
        -----
        RuntimeError
            If file_attributes.local_path exists but is not a file.
            It would be unclear how the cache should proceed in this case.
        """
        file_exists = False

        if file_attributes.local_path.exists():
            if not file_attributes.local_path.is_file():
                raise RuntimeError(f"{file_attributes.local_path}\n"
                                   "exists, but is not a file;\n"
                                   "unsure how to proceed")

            file_exists = True

        return file_exists

    def _get_file_path(self, directory: str, file_name: str) -> dict:
        """
        Return the local path to a data file, and test for the
        file's existence.

        Parameters
        ----------
        directory: str
            The name of the directory containing the file
        file_name: str
            The name of the file to be accessed

        Returns
        -------
        dict

            'path' will be a pathlib.Path pointing to the file's location

            'exists' will be a boolean indicating if the file
            exists in a valid state

            'file_attributes' is a CacheFileAttributes describing the file
            in more detail

        Raises
        ------
        RuntimeError
            If the file cannot be downloaded
        """
        file_attributes = self._manifest.get_file_attributes(
            directory=directory,
            file_name=file_name
        )
        exists = self._file_exists(file_attributes)
        local_path = file_attributes.local_path
        output = {'local_path': local_path,
                  'exists': exists,
                  'file_attributes': file_attributes}

        return output

    def metadata_path(self, directory: str, file_name: str) -> dict:
        """
        Return the local path to a metadata file, and test for the
        file's existence

        Parameters
        ----------
        directory: str
            The name of the directory containing the metadata file
        file_name: str
            The name of the metadata file to be accessed

        Returns
        -------
        dict

            'path' will be a pathlib.Path pointing to the file's location

            'exists' will be a boolean indicating if the file
            exists in a valid state

            'file_attributes' is a CacheFileAttributes describing the file
            in more detail

        Raises
        ------
        RuntimeError
            If the file cannot be downloaded
        """
        output = self._get_file_path(directory=directory, file_name=file_name)

        return output

    def data_path(self, directory: str, file_name: str) -> dict:
        """
        Return the local path to a data file, and test for the
        file's existence

        Parameters
        ----------
        directory: str
            The name of the directory containing the metadata file
        file_name: str
            The name of the metadata file to be accessed

        Returns
        -------
        dict

            'local_path' will be a pathlib.Path pointing to the file's location

            'exists' will be a boolean indicating if the file
            exists in a valid state

            'file_attributes' is a CacheFileAttributes describing the file
            in more detail

        Raises
        ------
        RuntimeError
            If the file cannot be downloaded
        """
        output = self._get_file_path(directory=directory, file_name=file_name)

        return output


class CloudCacheBase(BasicLocalCache):
    """
    A class to handle the downloading and accessing of data served from a cloud
    storage system

    Parameters
    ----------
    cache_dir: str or pathlib.Path
        Path to the directory where data will be stored on the local system

    ui_class_name: Optional[str]
        Name of the class users are actually using to manipulate this
        functionality (used to populate helpful error messages)
    """

    _bucket_name = None

    def __init__(self,
                 cache_dir: Union[str, Path],
                 ui_class_name: Optional[str] = None):
        super().__init__(cache_dir=cache_dir,
                         ui_class_name=ui_class_name)

        # what latest_manifest was the last time an OutdatedManifestWarning
        # was emitted
        self._manifest_last_warned_on = None

        c_path = Path(self._cache_dir)

        # self._manifest_last_used contains the name of the manifest
        # last loaded from this cache dir (if applicable)
        self._manifest_last_used = c_path / '_manifest_last_used.txt'

        # self._downloaded_data_path is where we will keep a JSONized
        # dict mapping paths to downloaded files to their file_hashes;
        # this will be used when determining if a downloaded file
        # can instead be a symlink
        self._downloaded_data_path = c_path / '_downloaded_data.json'

        # if the local manifest is missing but there are
        # data files in cache_dir, emit a warning.
        if not self._downloaded_data_path.exists():
            file_list = c_path.glob('**/*')
            has_files = False
            for fname in file_list:
                # If the file exists ignore it if it is a json file
                # the last used manifest file, or a .DS_Store file for Mac
                # compatibility.
                if fname.is_file() \
                        and 'json' not in fname.name \
                        and '_manifest_last_used' not in fname.name \
                        and 'DS_Store' not in fname.name:
                    has_files = True
                    break
            if has_files:
                msg = (
                    'This cache directory appears to '
                    'contain data files, but it has no '
                    'record of what those files are. '
                    'Unless running as a LocalCache, files will be '
                    're-downloaded.'
                )
                warnings.warn(msg, MissingLocalManifestWarning)

    def _update_list_of_downloads(self,
                                  file_attributes: CacheFileAttributes
                                  ) -> None:
        """
        Update the local file that keeps track of files that have actually
        been downloaded to reflect a newly downloaded file.

        Parameters
        ----------
        file_attributes: CacheFileAttributes
            Description of the file that was downloaded

        Returns
        -------
        None
        """
        if not file_attributes.local_path.exists():
            # This file does not exist; there is nothing to do
            return None

        if self._downloaded_data_path.exists():
            with open(self._downloaded_data_path, 'rb') as in_file:
                downloaded_data = set(json.load(in_file))
        else:
            downloaded_data = set()

        abs_path = str(file_attributes.local_path.resolve())
        if abs_path in downloaded_data:
            return None

        downloaded_data.add(abs_path)
        with open(self._downloaded_data_path, 'w') as out_file:
            out_file.write(json.dumps(list(downloaded_data),
                                      indent=2,
                                      sort_keys=True))
        return None

    def _remove_download_from_list(self,
                                   file_attributes: CacheFileAttributes
                                   ) -> None:
        """
        Remove a file name from the list of downloads. This is used when
        the force_download flag is set to True when downloading

        Parameters
        ----------
        file_attributes: CacheFileAttributes
            Description of the file that was downloaded

        Returns
        -------
        None
        """
        if not file_attributes.local_path.exists():
            # This file does not exist; there is nothing to do
            return None

        if self._downloaded_data_path.exists():
            with open(self._downloaded_data_path, 'rb') as in_file:
                downloaded_data = set(json.load(in_file))
        else:
            downloaded_data = set()

        abs_path = str(file_attributes.local_path.resolve())
        if abs_path in downloaded_data:
            downloaded_data.remove(abs_path)
            with open(self._downloaded_data_path, 'w') as out_file:
                out_file.write(json.dumps(list(downloaded_data),
                                          indent=2,
                                          sort_keys=True))
        return None

    def _warn_of_outdated_manifest(self, manifest_name: str) -> None:
        """
        Warn that manifest_name is not the latest manifest available

        Parameters
        ----------
        manifest_name: str
            The name of the manifest to load. Must be an element in
            self.manifest_file_names
        """
        if self._manifest_last_warned_on is not None:
            if self.latest_manifest_file == self._manifest_last_warned_on:
                return None

        self._manifest_last_warned_on = self.latest_manifest_file

        msg = '\n\n'
        msg += 'The manifest file you are loading is not the '
        msg += 'most up to date manifest file available for '
        msg += 'this dataset. The most up to data manifest file '
        msg += 'available for this dataset is \n\n'
        msg += f'{self.latest_manifest_file}\n\n'
        msg += 'To see the differences between these manifests,'
        msg += 'run\n\n'
        msg += f"{self.ui}.compare_manifests('{self.latest_manifest_file}', "
        msg += f"'{manifest_name}')\n\n"
        msg += "To see all of the manifest files currently downloaded "
        msg += "onto your local system, run\n\n"
        msg += "self.list_all_downloaded_manifests()\n\n"
        msg += "If you just want to load the latest manifest, run\n\n"
        msg += "self.load_latest_manifest()\n\n"
        warnings.warn(msg, OutdatedManifestWarning)
        return None

    @property
    def latest_downloaded_manifest_file(self) -> str:
        """parses downloaded available manifest files for a version/date string
        and returns the latest one
        self.manifest_file_names are assumed to be of the form
        'releases/<version>/manifest.json'

        Returns
        -------
        str
            the filename whose semver string is the latest one
        """
        file_list = self.list_all_downloaded_manifests()
        if len(file_list) == 0:
            return ''
        return max(self.list_all_downloaded_manifests())

    def load_last_manifest(self):
        """
        If this Cache was used previously, load the last manifest
        used in this cache. If this cache has never been used, load
        the latest manifest.
        """
        if not self._manifest_last_used.exists():
            self.load_latest_manifest()
            return None

        with open(self._manifest_last_used, 'r') as in_file:
            to_load = in_file.read()

        latest = self.latest_manifest_file

        if to_load not in self.manifest_file_names:
            msg = 'The manifest version recorded as last used '
            msg += f'for this cache -- {to_load}-- '
            msg += 'is not a valid manifest for this dataset. '
            msg += f'Loading latest version -- {latest} -- '
            msg += 'instead.'
            warnings.warn(msg, UserWarning)
            self.load_latest_manifest()
            return None

        if latest != to_load:
            self._manifest_last_warned_on = self.latest_manifest_file
            msg = f"You are loading {to_load}. A more up to date "
            msg += f"version of the dataset -- {latest} -- exists "
            msg += "online. To see the changes between the two "
            msg += "versions of the dataset, run\n"
            msg += f"{self.ui}.compare_manifests('{to_load}',"
            msg += f" '{latest}')\n"
            msg += "To load another version of the dataset, run\n"
            msg += f"{self.ui}.load_manifest('{latest}')"
            warnings.warn(msg, OutdatedManifestWarning)
        self.load_manifest(to_load)
        return None

    def load_latest_manifest(self):
        latest_downloaded = self.latest_downloaded_manifest_file
        latest = self.latest_manifest_file
        if latest != latest_downloaded and latest_downloaded != '':
            msg = f'You are loading\n{self.latest_manifest_file}\n'
            msg += 'which is newer than the most recent manifest '
            msg += 'file you have previously been working with\n'
            msg += f'{latest_downloaded}\n'
            msg += 'It is possible that some data files have changed '
            msg += 'between these two data releases, which will '
            msg += 'force you to re-download those data files '
            msg += '(currently downloaded files will not be overwritten).'
            msg += f' To continue using {latest_downloaded}, run\n'
            msg += f"{self.ui}.load_manifest('{latest_downloaded}')"
            warnings.warn(msg, OutdatedManifestWarning)
        self.load_manifest(self.latest_manifest_file)

    @abstractmethod
    def _download_manifest(self,
                           manifest_name: str):
        """
        Download a manifest from the dataset

        Parameters
        ----------
        manifest_name: str
            The name of the manifest to load. Must be an element in
            self.manifest_file_names
        """
        raise NotImplementedError()

    @abstractmethod
    def _download_file(self,
                       file_attributes: CacheFileAttributes,
                       force_download: bool = False,
                       skip_hash_check: bool = False
                       ) -> bool:
        """
        Check if a file exists locally. If it does not, download it and
        return True. Return False otherwise.

        Parameters
        ----------
        file_attributes: CacheFileAttributes
            Describes the file to download
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally
        skip_hash_check: bool
            If True, skip the file hash check

        Returns
        -------
        bool
            True if the file was downloaded; False otherwise

        Raises
        ------
        RuntimeError
            If the path to the directory where the file is to be saved
            points to something that is not a directory.

        RuntimeError
            If it is not able to successfully download the file after
            10 iterations
        """
        raise NotImplementedError()

    def load_manifest(self, manifest_name: str):
        """
        Load a manifest from this dataset.

        Parameters
        ----------
        manifest_name: str
            The name of the manifest to load. Must be an element in
            self.manifest_file_names
        """
        if manifest_name not in self.manifest_file_names:
            raise ValueError(
                f"Manifest to load ({manifest_name}) is not one of the "
                "valid manifest names for this dataset. Valid names include:\n"
                f"{self.manifest_file_names}"
            )

        if manifest_name != self.latest_manifest_file:
            self._warn_of_outdated_manifest(manifest_name)

        # If desired manifest does not exist, try to download it
        manifest_path = self._cache_dir / manifest_name
        if not manifest_path.exists():
            self._download_manifest(manifest_name)

        self._manifest = self._load_manifest(manifest_name)

        # Keep track of the newly loaded manifest
        self._save_last_used_manifest(manifest_name)

        self._manifest_name = manifest_name

    def _save_last_used_manifest(self, manifest_name: str):
        """
        Save the name of the last manifest used in this cache.
        """
        with open(self._manifest_last_used, 'w') as out_file:
            out_file.write(manifest_name)

    def _file_exists(self, file_attributes: CacheFileAttributes) -> bool:
        """
        Given a CacheFileAttributes describing a file, assess whether that
        file exists locally.

        Parameters
        ----------
        file_attributes: CacheFileAttributes
            Description of the file to look for

        Returns
        -------
        bool
            True if the file exists and is valid; False otherwise

        Raises
        -----
        RuntimeError
            If file_attributes.local_path exists but is not a file.
            It would be unclear how the cache should proceed in this case.
        """
        file_exists = False

        if file_attributes.local_path.exists():
            if not file_attributes.local_path.is_file():
                raise RuntimeError(f"{file_attributes.local_path}\n"
                                   "exists, but is not a file;\n"
                                   "unsure how to proceed")
            file_exists = True

        return file_exists

    def _check_successful_download(self,
                                   file_attributes: CacheFileAttributes
                                   ) -> bool:
        """
        Check to see if the file is listed in the set of successfully
        downloaded files. If it is, return True.


        Else return False

        Parameters
        ----------
        file_attributes: CacheFileAttributes
            The file we are considering downloading

        Returns
        -------
        bool
        """
        if not self._downloaded_data_path.exists():
            return False

        with open(self._downloaded_data_path, 'rb') as in_file:
            available_files = set(json.load(in_file))
        if str(file_attributes.local_path.resolve()) in available_files:
            return True

        return False

    def download_data(
        self,
        directory: str,
        file_name: str,
        force_download: bool = False,
        skip_hash_check: bool = False
    ) -> Path:
        """
        Return the local path to a data file, downloading the file
        if necessary

        Parameters
        ----------
        directory: str
            The name of the directory containing the data file
        file_name: str
            The name of the data file to be accessed
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally
        skip_hash_check: bool
            If True, skip the file hash check

        Returns
        -------
        pathlib.Path
            The path indicating where the file is stored on the
            local system

        Raises
        ------
        RuntimeError
            If the file cannot be downloaded
        """
        super_attributes = self.data_path(directory=directory,
                                          file_name=file_name)
        file_attributes = super_attributes['file_attributes']
        # If the file exists, check that it was downloaded successfully.
        if super_attributes['exists'] \
                and not self._check_successful_download(
                        file_attributes=super_attributes['file_attributes']):
            force_download = True
        self._download_file(
            file_attributes=file_attributes,
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )
        return file_attributes.local_path

    def download_metadata(self,
                          directory: str,
                          file_name: str,
                          force_download: bool = False,
                          skip_hash_check: bool = False) -> Path:
        """
        Return the local path to a metadata file, downloading the
        file if necessary

        Parameters
        ----------
        directory: str
            The name of the directory containing the metadata file
        file_name: str
            The name of the metadata file to be accessed
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally
        skip_hash_check: bool
            If True, skip the file hash check

        Returns
        -------
        pathlib.Path
            The path indicating where the file is stored on the
            local system

        Raises
        ------
        RuntimeError
            If the file cannot be downloaded
        """
        super_attributes = self.metadata_path(
            directory=directory, file_name=file_name)
        # If the file exists, check that it was downloaded successfully.
        if super_attributes['exists'] \
                and not self._check_successful_download(
                    file_attributes=super_attributes['file_attributes']):
            force_download = True
        file_attributes = super_attributes['file_attributes']
        self._download_file(
            file_attributes=file_attributes,
            force_download=force_download,
            skip_hash_check=skip_hash_check
        )
        return file_attributes.local_path

    def download_directory_metadata(
            self,
            directory: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ) -> List[Path]:
        """
        Download all of the metadata files in a directory.

        Parameters
        ----------
        directory: str
            The name of the directory containing the metadata files
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.

        Returns
        -------
        output_paths: list Paths
            List of paths to the downloaded metadata files
        """
        metadata_list = self.list_metadata_files(directory)
        output_metadata = []
        for file_name in metadata_list:
            output_metadata.append(
                self.download_metadata(
                    directory=directory,
                    file_name=file_name,
                    force_download=force_download,
                    skip_hash_check=skip_hash_check
                )
            )
        return output_metadata

    def download_directory_data(
            self,
            directory: str,
            force_download: bool = False,
            skip_hash_check: bool = False
    ) -> List[Path]:
        """
        Download all of the data files in a directory.

        Parameters
        ----------
        directory: str
            The name of the directory containing the data files
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally.
        skip_hash_check: bool
            If True, skip the file hash check for file integrity.

        Returns
        -------
        output_paths: list Paths
            List of paths to the downloaded data files
        """
        data_list = self.list_data_files(directory)
        output_data = []
        for file_name in data_list:
            output_data.append(
                self.download_data(
                    directory=directory,
                    file_name=file_name,
                    force_download=force_download,
                    skip_hash_check=skip_hash_check
                )
            )
        return output_data

    def _compare_directories(
        self,
        manifest_0: Manifest,
        manifest_1: Manifest
    ) -> dict:
        """
        Compare two manifests from this dataset. Return a dict of new and
        removed manifests.

        Parameters
        ----------
        manifest_0: Manifest
            Manifest object for manifest_0. Nominally the newer of the two.
        manifest_1: Manifest
            Manifest object for manifest_1. Nominally the older of the two.

        Returns
        -------
        output_dict: dict
            output_dict['new_dirs'] is a list of directories that were added
            output_dict['removed_dirs'] is a list of directories that were
                removed.
        """
        output_dict = {}
        dirs_0 = set(manifest_0.list_directories)
        dirs_1 = set(manifest_1.list_directories)

        output_dict['new_dirs'] = list(dirs_0.difference(dirs_1))
        output_dict['new_dirs'].sort()
        output_dict['removed_dirs'] = list(dirs_1.difference(dirs_0))
        output_dict['removed_dirs'].sort()

        return output_dict

    def _compare_files(
        self,
        manifest_0: Manifest,
        manifest_1: Manifest,
        is_metadata: bool = False
    ) -> dict:
        """
        Compare two manifests from this dataset. Return a dict of new and
        removed metadata files as well as any differences in the file metadata.

        Parameters
        ----------
        manifest_0: abc_atlas_cache.manifest.Manifest
            "new" manifest to compare to "old"
        manifest_1: abc_atlas_cache.manifest.Manifest
            "old" manifest to compare to "new"
        is_metadata: bool
            If True, compare metadata files. If False, compare data files.

        Returns
        -------
        output_dict: dict
            Dictionary of new, removed, and changed files. Also shows potential
            manifest errors where the file version is consistent between
            manifests but other information on the file has changed.
            <file_kind> is either metadata or data_file.

            Keys are:
            - output_dict['new_<file_kind>'] is a list of files that
              were added
            - output_dict['removed_<file_kind>''] is a list of files
              that were removed.
            - output_dict['changed_<file_kind>'] is a list of files
              that were changed between the two manifests.
            - output_dict['manifest_error_<file_kind>'] is a list of
              files that were changed between the two manifests, but the
              version number did not change.
        """
        file_kind = 'metadata' if is_metadata else 'data_file'
        output_dict = {}

        file_list0 = []
        for directory in manifest_0.list_directories:
            try:
                file_list0 += [
                    '%s: %s' % (directory, file_name)
                    for file_name in manifest_0._list_data_in_directory(
                        directory=directory,
                        is_metadata=is_metadata
                    )
                ]
            except DataTypeNotInDirectory:
                continue
        file_list1 = []
        for directory in manifest_1.list_directories:
            try:
                file_list1 += [
                    '%s: %s' % (directory, file_name)
                    for file_name in manifest_1._list_data_in_directory(
                        directory=directory,
                        is_metadata=is_metadata
                    )
                ]
            except DataTypeNotInDirectory:
                continue

        file_list0 = set(file_list0)
        file_list1 = set(file_list1)

        output_dict[f'new_{file_kind}'] = list(
            file_list0.difference(file_list1)
        )
        output_dict[f'new_{file_kind}'].sort()
        output_dict[f'removed_{file_kind}'] = list(
            file_list1.difference(file_list0)
        )
        output_dict[f'removed_{file_kind}'].sort()

        output_dict[f'changed_{file_kind}'] = []
        output_dict[f'manifest_error_{file_kind}'] = []
        for file_name in file_list0.intersection(file_list1):
            directory, metadata_file = file_name.split(': ')
            file_attr_0 = manifest_0.get_file_attributes(directory,
                                                         metadata_file)
            file_attr_1 = manifest_1.get_file_attributes(directory,
                                                         metadata_file)

            if file_attr_0 != file_attr_1 and \
                    file_attr_0.version == file_attr_1.version:
                output_dict[f'manifest_error_{file_kind}'].append(file_name)
            elif file_attr_0 != file_attr_1 and \
                    file_attr_0.version != file_attr_1.version:
                output_dict[f'changed_{file_kind}'].append(file_name)
        output_dict[f'changed_{file_kind}'].sort()
        output_dict[f'manifest_error_{file_kind}'].sort()

        return output_dict

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
        output_dict: dict
        """
        results = {}
        if manifest_older_name > manifest_newer_name:
            raise ValueError(
                f"The manifest input first ({manifest_newer_name}) is older "
                f"than the manifest input second ({manifest_older_name}). "
                "Please reverse the order of the input."
            )
        manifest_0 = self._load_manifest(manifest_newer_name)
        manifest_1 = self._load_manifest(manifest_older_name)

        results['directory_changes'] = self._compare_directories(
            manifest_0=manifest_0,
            manifest_1=manifest_1
        )
        results['metadata_changes'] = self._compare_files(
            manifest_0=manifest_0,
            manifest_1=manifest_1,
            is_metadata=True
        )
        results['data_file_changes'] = self._compare_files(
            manifest_0=manifest_0,
            manifest_1=manifest_1,
            is_metadata=False
        )

        return results


class S3CloudCache(CloudCacheBase):
    """
    A class to handle the downloading and accessing of data served from
    an S3-based storage system

    Parameters
    ----------
    cache_dir: str or pathlib.Path
        Path to the directory where data will be stored on the local system

    bucket_name: str
        for example, if bucket URI is 's3://mybucket' this value should be
        'mybucket'

    ui_class_name: Optional[str]
        Name of the class users are actually using to maniuplate this
        functionality (used to populate helpful error messages)
    """

    def __init__(self,
                 cache_dir: Union[str, Path],
                 bucket_name: str,
                 ui_class_name=None):
        self._manifest = None
        self._bucket_name = bucket_name

        super().__init__(cache_dir=cache_dir,
                         ui_class_name=ui_class_name)

    _s3_client = None

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def s3_client(self):
        if self._s3_client is None:
            s3_config = Config(signature_version=UNSIGNED)
            self._s3_client = boto3.client('s3',
                                           config=s3_config)
        return self._s3_client

    def _list_all_manifests(self) -> list:
        """
        Return a list of all of the file names of the manifests associated
        with this dataset
        """
        paginator = self.s3_client.get_paginator('list_objects_v2')
        subset_iterator = paginator.paginate(
            Bucket=self._bucket_name,
            Prefix=self.manifest_prefix
        )

        output = []
        for subset in subset_iterator:
            if 'Contents' in subset:
                for obj in subset['Contents']:
                    output.append(obj['Key'])

        output.sort()
        return output

    def _download_manifest(self,
                           manifest_name: str):
        """
        Download a manifest from the dataset

        Parameters
        ----------
        manifest_name: str
            The name of the manifest to load. Must be an element in
            self.manifest_file_names
        """
        response = self.s3_client.get_object(Bucket=self._bucket_name,
                                             Key=manifest_name)

        filepath = self._cache_dir / manifest_name
        filepath.parents[0].mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb') as f:
            for chunk in response['Body'].iter_chunks():
                f.write(chunk)

    def _download_file(self,
                       file_attributes: CacheFileAttributes,
                       force_download: bool = False,
                       skip_hash_check: bool = False
                       ) -> bool:
        """
        Check if a file exists locally. If it does not, download it
        and return True. Return False otherwise.

        Parameters
        ----------
        file_attributes: CacheFileAttributes
            Describes the file to download
        force_download: bool
            If True, force the file to be downloaded even if it already exists
            locally
        skip_hash_check: bool
            If True, skip the file hash check. Not recommended as this
            verifies that the file was downloaded successfully.

        Returns
        -------
        bool
            True if the file was downloaded; False otherwise

        Raises
        ------
        RuntimeError
            If the path to the directory where the file is to be saved
            points to something that is not a directory.

        RuntimeError
            If it is not able to successfully download the file after
            10 iterations
        """
        was_downloaded = False
        if force_download:
            # Remove the file from the list of successfully downloaded files.
            self._remove_download_from_list(file_attributes)
            if file_attributes.local_path.exists():
                file_attributes.local_path.unlink()

        local_path = file_attributes.local_path

        local_dir = local_path.parents[0]
        local_dir.mkdir(parents=True, exist_ok=True)
        if not local_dir.is_dir():
            raise RuntimeError(f"{local_dir}\n"
                               "is not a directory")
        obj_key = file_attributes.relative_path

        n_iter = 0
        max_iter = 10  # maximum number of times to try download

        pbar = None
        if not self._file_exists(file_attributes):
            response = self.s3_client.list_objects_v2(Bucket=self._bucket_name,
                                                      Prefix=str(obj_key))
            object_info = response['Contents'][0]
            pbar = tqdm.tqdm(desc=object_info["Key"].split("/")[-1],
                             total=object_info["Size"],
                             unit_scale=True,
                             unit_divisor=1000.,
                             unit="MB")

        while not self._file_exists(file_attributes):
            n_iter += 1
            was_downloaded = True
            response = self.s3_client.get_object(Bucket=self._bucket_name,
                                                 Key=str(obj_key))

            if 'Body' in response:
                with open(local_path, 'wb') as out_file:
                    for chunk in response['Body'].iter_chunks():
                        out_file.write(chunk)
                        pbar.update(len(chunk))

            # Verify the hash of the downloaded file
            if not skip_hash_check:
                test_checksum = file_hash_from_path(file_attributes.local_path)
                if test_checksum != file_attributes.file_hash:
                    file_attributes.local_path.unlink(missing_ok=True)

            if n_iter > max_iter:
                pbar.close()
                raise RuntimeError("Could not download\n"
                                   f"{file_attributes}\n"
                                   "In {max_iter} iterations")

            if file_attributes.local_path.exists():
                self._update_list_of_downloads(file_attributes=file_attributes)

        if pbar is not None:
            pbar.close()

        return was_downloaded


class LocalCache(CloudCacheBase):
    """A class to handle accessing of data that has already been downloaded
    locally. Supports multiple manifest versions from a given dataset.

    Parameters
    ----------
    cache_dir: str or pathlib.Path
        Path to the directory where data will be stored on the local system

    ui_class_name: Optional[str]
        Name of the class users are actually using to maniuplate this
        functionality (used to populate helpful error messages)
    """
    def __init__(self, cache_dir, ui_class_name=None):
        super().__init__(cache_dir=cache_dir,
                         ui_class_name=ui_class_name)

    def _list_all_manifests(self) -> list:
        return self.list_all_downloaded_manifests()

    def _download_manifest(self, manifest_name: str):
        raise NotImplementedError()

    def _download_file(self,
                       file_attributes: CacheFileAttributes,
                       force_download: bool = False,
                       skip_hash_check: bool = False) -> bool:
        raise NotImplementedError()

    def _save_last_used_manifest(self, manifest_name: str):
        """
        """
        try:
            with open(self._manifest_last_used, 'w') as out_file:
                out_file.write(manifest_name)
        except OSError:
            warnings.warn(
                f"""LocalCache is a read only directory and cannot
                save the last used manifest.
                Current Manifest: {manifest_name}""",
                ReadOnlyLocalCacheWarning
            )