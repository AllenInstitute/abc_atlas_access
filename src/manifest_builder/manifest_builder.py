import argparse
from collections import OrderedDict
import datetime
import glob
import json
import logging
import os
from pathlib import Path, PurePosixPath
from typing import List, Union

from abc_atlas_access.abc_atlas_cache.utils import file_hash_from_path


def _validate_version(version: str) -> bool:
    try:
        datetime.datetime.strptime(version, '%Y%m%d').date()
        return True
    except ValueError:
        return False


def find_directories(
        base_dir: Union[str, Path],
        version: str,
        dirs_to_skip: List[str]
) -> dict:
    """Crawl ``base_dir`` to find all sub-directories with versions up to and
    including ``version``.

    Finds subdirectories of the form <project_name>/<version>/

    Parameters
    ----------
    base_dir: str or Path
        Base directory to look for ABC atlas release files.
    version: str
        String date format of the version. Should be of the form %Y%m%d (e.g.
        20240330)
    dirs_to_skip: list of str
        List of projects/directories to skip. Can either be full directory
        name or the first part of a data_set pattern to match. (e.g. SEAD will
        exclude all directories that start with that pattern for example,
        SEAD-taxonomy etc.)

    Returns
    -------
    release: dict
        Base release manifest dictionary with all directories populated.
    """
    find_logger = logging.getLogger("find_directories")

    release = {
        "version": version,
        "resource_uri": "s3://allen-brain-cell-atlas/",
        "directory_listing": {}
    }
    for directory in os.walk(base_dir):
        version_list = []
        # Find only directories with properly formated date version
        # subdirectories
        for subdir in directory[1]:
            if _validate_version(subdir):
                version_list.append(subdir)
        # If we find a version  select either the max version
        if version_list:
            max_version = max(version_list)
            split_dir = str(PurePosixPath(directory[0])).split('/')
            data_set = split_dir[-1]
            if any([data_set.startswith(skip) for skip in dirs_to_skip]):
                find_logger.info(f"Skipping dataset: {data_set}")
                continue
            if version < max_version and version not in version_list:
                continue
            data_kind = split_dir[-2]
            if data_set not in release['directory_listing']:
                release['directory_listing'][data_set] = {}
                release['directory_listing'][data_set]['directories'] = {}
            release['directory_listing'][data_set]['directories'][data_kind] = {
                'version': version if version < max_version else max_version
            }
    release['directory_listing'] = OrderedDict(
        sorted(release['directory_listing'].items()))
    return release


def populate_directories(
        base_dir: Union[str, Path],
        release: dict,
        bucket_prefix: str,
        browse_prefix: str
) -> dict:
    """Populate paths and urls for each dataset/directory in the release.

    Parameters
    ----------
    base_dir: str or Path
        Base directory to look for ABC atlas release files.
    release: dict
        Base release manifest dictionary with all directories populated.
    bucket_prefix: str
        Prefix to add to the bucket url.
    browse_prefix: str
        Prefix to add to the browse url.

    Returns
    -------
    release: dict
        Base release manifest dictionary with all directories, links, and paths
        populated.
    """
    dir_logger = logging.getLogger("populate_directories")
    dir_logger.info('Populating paths and urls for each dataset/directory')
    for data_set in release['directory_listing'].keys():

        dir_logger.info(f'- {data_set}')
        ds_dict = release['directory_listing'][data_set]['directories']

        for data_dir in ds_dict.keys():

            dir_logger.info(f'-- {data_dir}')
            ver_dict = ds_dict[data_dir]
            rel_path = os.path.join(data_dir, data_set, ver_dict['version'])
            full_path = os.path.join(base_dir, rel_path)
            bucket_url = bucket_prefix + rel_path + '/'
            browse_url = browse_prefix + rel_path + '/'

            if not os.path.isdir(full_path):
                raise FileNotFoundError(f"{full_path} is not a directory")

            dir_logger.debug(f'--- {rel_path}')
            dir_logger.debug(f'--- {bucket_url}')
            dir_logger.debug(f'--- {browse_url}')

            ver_dict['relative_path'] = rel_path
            ver_dict['url'] = bucket_url
            ver_dict['view_link'] = browse_url
    return release


def populate_datasets(
        base_dir: Union[str, Path],
        release: dict,
        bucket_prefix: str,
) -> dict:
    """Populate all files in the manifest by crawling the base directory.

    Parameters
    ----------
    base_dir: str or Path
        Staging directory of the ABC atlas release.
    release: dict
        Base release manifest dictionary with all directories populated, links,
        and paths populated.
    bucket_prefix: str
        Prefix to add to the bucket url.

    Returns
    -------
    release: dict
        Base release manifest dictionary with all directories, links, paths,
        and files populated.
    """
    dataset_logger = logging.getLogger("populate_datasets")
    dataset_logger.info("Populating files and hashes for each "
                        "dataset/directory")
    dataset_lookup = {}

    for dataset in release['directory_listing'].keys():

        dataset_logger.info(f'- {dataset}')
        ds_dict = release['directory_listing'][dataset]['directories']
        dataset_lookup[dataset] = {}

        for data_kind in ds_dict.keys():

            dataset_logger.info(f'-- {data_kind}')
            dataset_lookup[dataset][data_kind] = {}
            ver_dict = ds_dict[data_kind]

            data_dir = os.path.join(base_dir, ver_dict['relative_path'])

            total_size = 0

            for file_path in ['*', '*/*']:

                for full_path in glob.glob(
                        os.path.join(data_dir, file_path),
                        recursive=True
                ):
                    if os.path.isdir(full_path):
                        continue

                    dataset_logger.debug(full_path)
                    file_size = os.path.getsize(full_path)
                    total_size += file_size

                    rel_path = os.path.relpath(full_path, base_dir)

                    bname = os.path.basename(full_path)

                    bsplit = os.path.splitext(bname)
                    ext = bsplit[1]
                    ext = ext.replace('.', '')

                    file_hash = file_hash_from_path(full_path)

                    # Metadata for an individual file.
                    file_dict = {
                        'version': ds_dict[data_kind]['version'],
                        'relative_path': rel_path,
                        'url': bucket_prefix + rel_path,
                        'size': file_size,
                        'file_hash': file_hash
                    }

                    if ext in ['csv', 'json', 'h5']:
                        tag = bsplit[0]
                        dataset_lookup[dataset][data_kind][tag] = {}
                        dataset_lookup[dataset][data_kind][tag]['files'] = {}
                        dataset_lookup[dataset][data_kind][tag]['files'][
                            ext] = file_dict
                    elif ext == 'h5ad':

                        if '-raw.h5ad' in bname:
                            tag = bname.split('-raw.h5ad')[0]
                            norm = 'raw'
                        elif '-log2.h5ad' in bname:
                            tag = bname.split('-log2.h5ad')[0]
                            norm = 'log2'

                        if tag not in dataset_lookup[dataset][data_kind].keys():
                            dataset_lookup[dataset][data_kind][tag] = {}

                        dataset_lookup[dataset][data_kind][tag][norm] = {}
                        dataset_lookup[dataset][data_kind][tag][norm]['files'] = {}
                        dataset_lookup[dataset][data_kind][tag][norm]['files'][
                            ext] = file_dict
                    elif ext == 'gz':
                        ext = 'nii.gz'
                        tag = bname.replace('.nii.gz', '')
                        dataset_lookup[dataset][data_kind][tag] = {}
                        dataset_lookup[dataset][data_kind][tag]['files'] = {}
                        dataset_lookup[dataset][data_kind][tag]['files'][
                            ext] = file_dict

                ver_dict['total_size'] = total_size

    release['file_listing'] = dataset_lookup
    return release


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--abc_atlas_staging_path",
        type=str,
        required=True,
        help="Path to the ABC Atlas staging directory.  "
    )
    parser.add_argument(
        "--output_file",
        type=str,
        required=True,
        help="File to output the manifest to."
    )
    parser.add_argument(
        "--manifest_version",
        type=str,
        required=True,
        help="Verion of the manifest to build. Should be in the format "
             "%Y%m%d. (e.g. 20240315)"
    )
    parser.add_argument(
        "--bucket_prefix",
        type=str,
        default="https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/",
        help=""
    )
    parser.add_argument(
        "--datasets_to_skip",
        nargs='+',
        type=str,
        default=['releases', 'SEAAD-10X', 'SEAAD-MERFISH', 'SEA-AD', 'Zhuang-C57BL6J'],
        help="Skip a given project for all directories that start with the "
             "given pattern. (e.g. SEAD will exclude all directories that "
                "start with that pattern for example, SEAD-taxonomy etc.)"
    )
    parser.add_argument(
        "--logging_level",
        type=str,
        choices=['INFO', 'DEBUG'],
        default="INFO",
        help="Set the logging level."
    )
    args = parser.parse_args()
    logger = logging.getLogger(__name__)
    if args.logging_level == "DEBUG":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    base_dir = Path(args.abc_atlas_staging_path)
    version = args.manifest_version
    if not _validate_version(args.manifest_version):
        raise ValueError("Invalid version format. Please use %Y%m%d format "
                         "(e.g. 20240315)")
    bucket_prefix = args.bucket_prefix
    browse_prefix = args.bucket_prefix + 'index.html#'
    datasets_to_skip = args.datasets_to_skip

    logger.info(f"Building manifest for version: {version}")
    output_release = find_directories(
        base_dir=base_dir,
        version=version,
        dirs_to_skip=datasets_to_skip
    )
    output_release = populate_directories(
        base_dir=base_dir,
        release=output_release,
        bucket_prefix=bucket_prefix,
        browse_prefix=browse_prefix
    )
    output_release = populate_datasets(
        base_dir=base_dir,
        release=output_release,
        bucket_prefix=bucket_prefix
    )

    logger.info(f"Writing manifest to {args.output_file}")
    with open(args.output_file, 'w') as jfile:
        json.dump(output_release, jfile, indent=4)
