from typing import Dict, List, Any, Union
import json
import pathlib
from abc_atlas_access.abc_atlas_cache.file_attributes import \
    CacheFileAttributes  # noqa: E501

"""Methods for accessing and manipulating manifest.json files associated with
the ABC atlas data. Adapted from
https://github.com/AllenInstitute/AllenSDK/blob/master/allensdk/api/cloud_cache/manifest.py  # noqa: E501
"""


class DataTypeNotInDirectory(Exception):
    pass


class Manifest(object):
    """
    A class for manipulating a manifest.json file associated with a ABC atlas
    version.

    Each Manifest instance should represent the data for 1 and only 1
    manifest.json file.

    Parameters
    ----------
    cache_dir: str or pathlib.Path
        The path to the directory where local copies of files will be stored
    json_input:
        A ''.read()''-supporting file-like object containing
        a JSON document to be deserialized (i.e. same as the
        first argument to json.load)
    """

    def __init__(
            self,
            cache_dir: Union[str, pathlib.Path],
            json_input,
    ):
        if isinstance(cache_dir, str):
            self._cache_dir = pathlib.Path(cache_dir).resolve()
        elif isinstance(cache_dir, pathlib.Path):
            self._cache_dir = cache_dir.resolve()
        else:
            raise ValueError("cache_dir must be either a str "
                             "or a pathlib.Path; "
                             f"got {type(cache_dir)}")

        self._data: Dict[str, Any] = json.load(json_input)
        if not isinstance(self._data, dict):
            raise ValueError("Expected to deserialize manifest into a dict; "
                             f"instead got {type(self._data)}")

        self._version: str = self._data['version']
        self._resource_uri: str = self._data['resource_uri']

        self._directory_list: List[str] = list(
            self._data['directory_listing'].keys()
        )
        self._directory_list.sort()

    def _list_data_in_directory(
            self,
            directory: str,
            is_metadata=False,
    ) -> List[str]:
        """
        Get a list of all files of in a directory either for metadata files or
        data files.

        Parameters
        ----------
        directory: str
            The directory to list files in.
        is_metadata: bool
            List metadata or data file only.

        Returns
        -------
        list of str
            List of all files either metadata or general data files in a
            directory.
        """
        output_data_list = []
        sub_directories = self._data['file_listing'][directory]
        if is_metadata:
            if 'metadata' not in sub_directories.keys():
                raise DataTypeNotInDirectory(
                    f"No metadata files found in directory {directory}. No "
                    "metadata sub-directory found."
                )
            output_data_list.extend(list(sub_directories['metadata'].keys()))
        else:
            for sub_dir in sub_directories.keys():
                if sub_dir == 'metadata' or sub_dir == 'mapmycells':
                    continue
                for sub_dir_key in sub_directories[sub_dir].keys():
                    # Check for files with multiple kinds (e.g. raw and log2)
                    if "files" in sub_directories[sub_dir][sub_dir_key].keys():
                        output_data_list.append(sub_dir_key)
                    else:
                        output_data_list.extend(
                            ["%s/%s" % (sub_dir_key, key)
                             for key in sub_directories[sub_dir][
                                 sub_dir_key].keys()]
                        )
        output_data_list.sort()
        if len(output_data_list) == 0 and is_metadata:
            raise DataTypeNotInDirectory(
                f"No metadata files found in directory {directory}. Metadata "
                "sub-directory is empty."
            )
        elif len(output_data_list) == 0 and not is_metadata:
            raise DataTypeNotInDirectory(
                f"No data files found in directory {directory}."
            )
        return output_data_list

    @property
    def data(self):
        """
        The raw dictionary data of the manifest file.
        """
        return self._data

    @property
    def version(self):
        """
        The version of the dataset currently loaded
        """
        return self._version

    @property
    def resource_uri(self):
        """
        The URI of the dataset currently loaded
        """
        return self._resource_uri

    @property
    def list_directories(self):
        """
        List of all directories that are part of the dataset.
        """
        return self._directory_list

    def list_metadata_files(self, directory: str) -> List[str]:
        """
        List all metadata files in the specified directory.

        Parameters
        ----------
        directory: str
            The directory to list metadata files in.

        Returns
        -------
        list of str
            List of all metadata files in the specified directory.
        """
        return self._list_data_in_directory(directory, is_metadata=True)

    def list_data_files(self, directory: str) -> List[str]:
        """
        List all data files that are not data in the specified directory.

        Parameters
        ----------
        directory: str
            The directory to list data files in.

        Returns
        -------
        list of str
            List of all data files that are not metadata in the specified
            directory.
        """
        return self._list_data_in_directory(directory, is_metadata=False)

    def get_file_attributes(
            self,
            directory: str,
            file_name: str,
    ) -> CacheFileAttributes:
        """
        Get the data file with the specified name in the specified directory.

        Parameters
        ----------
        directory: str
            The directory to look for the file in.
        file_name: str
             The name of the file to look for.

        Returns
        -------
        CacheFileAttributes
            The file attributes for the requested file.
        """
        file_name = file_name.split('/')
        if len(file_name) == 1:
            file_name = file_name[0]
            kind = None
        else:
            kind = file_name[1]
            file_name = file_name[0]
        directory_data = self._data['file_listing'][directory]

        file_attributes = None
        for sub_dir in directory_data.keys():
            if file_name in directory_data[sub_dir].keys():
                files_data = directory_data[sub_dir][file_name]
                if "files" in files_data.keys():
                    file_type = list(files_data["files"].keys())[0]
                    file_attributes = self._create_file_attributes(
                        remote_path=files_data["files"][file_type]['url'],
                        version=files_data["files"][file_type]['version'],
                        size=files_data["files"][file_type]['size'],
                        relative_path=files_data["files"][file_type][
                            'relative_path'],
                        file_type=file_type,
                        file_hash=files_data["files"][file_type]['file_hash']
                    )
                elif kind in files_data.keys():
                    file_type = list(files_data[kind]['files'].keys())[0]
                    file_attributes = self._create_file_attributes(
                        remote_path=files_data[kind]["files"][file_type][
                            'url'],
                        version=files_data[kind]["files"][file_type][
                            'version'],
                        size=files_data[kind]["files"][file_type]['size'],
                        relative_path=files_data[kind]["files"][file_type][
                            'relative_path'],
                        file_type=file_type,
                        file_hash=files_data[kind]["files"][file_type]['file_hash']  # noqa: E501
                    )
                elif kind is None and "files" not in files_data.keys():
                    raise KeyError(
                        f"File {file_name} found in directory but multiple "
                        f"files found: {list(files_data.keys())}. Please "
                        "specify the file name as one of "
                        f"{['%s/%s' % (file_name, key) for key in files_data.keys()]}"  # noqa: E501
                    )
        if file_attributes is None:
            raise KeyError(
                f"File {file_name} not found in directory {directory}."
            )

        return file_attributes

    def _create_file_attributes(self,
                                remote_path: str,
                                version: str,
                                size: int,
                                relative_path: str,
                                file_type: str,
                                file_hash: str
                                ) -> CacheFileAttributes:
        """
        Create the cache_file_attributes describing a file.
        This method does the work of assigning a local_path for a remote file.

        Parameters
        ----------
        remote_path: str
            The full URL to a file
        version: str
            The string specifying the version of the file
        size: str
            Size of the file in bytes on S3
        relative_path: str
            The relative path to the file.
        file_type: str
            The type of file (e.g. 'csv' or 'h5ad')
        file_hash: str
            The hash of the file.

        Returns
        -------
        CacheFileAttributes
        """
        # The convention of the data release tool is to have all
        # relative_paths from remote start with the project name which
        # we want to remove since we already specified a project_dir_name
        local_path = self._cache_dir / relative_path

        obj = CacheFileAttributes(
            url=remote_path,
            version=version,
            local_path=local_path,
            file_size=size,
            file_type=file_type,
            relative_path=relative_path,
            file_hash=file_hash
        )

        return obj

    def get_directory_metadata_size(
            self,
            directory: str,
    ) -> str:
        """
        Get the size of a metadata directory in GB or MB.

        Parameters
        ----------
        directory: str
            The directory to get the size of.


        Returns
        -------
        size: str
            The size of the directory in either GB or MB.
        """
        file_list = self.list_metadata_files(directory=directory)
        return self._get_directory_size(directory=directory,
                                        file_list=file_list)

    def get_directory_data_size(
            self,
            directory: str,
    ) -> str:
        """
        Get the size of a data directory in the requested in GB or MB.

        Parameters
        ----------
        directory: str
            The directory to get the size of.

        Returns
        -------
        size: str
            The size of the directory in either GB or MB.
        """
        file_list = self.list_data_files(directory=directory)
        return self._get_directory_size(directory=directory,
                                        file_list=file_list)

    def _get_directory_size(
            self,
            directory: str,
            file_list: List[str],
    ) -> str:
        """
        Get the size of a directory in the requested in GB or MB.

        Parameters
        ----------
        directory: str
            The directory to get the size of.

        Returns
        -------
        size: str
            The size of the directory in either GB or MB.
        """
        total_size = 0
        unit_size = 1024 ** 3
        unit = "GB"
        for file_name in file_list:
            file_attributes = self.get_file_attributes(
                directory=directory,
                file_name=file_name
            )
            total_size += file_attributes.file_size
        total_size /= unit_size
        if total_size < 1:
            total_size *= 1024
            unit = "MB"
        return f"{round(total_size, 2)} {unit}"
