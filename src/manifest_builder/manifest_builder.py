import argparse
from collections import OrderedDict
import datetime
import glob
import json
import os
from pathlib import Path, PurePosixPath
from typing import List, Union

from abc_atlas_access.abc_atlas_cache.utils import file_hash_from_path


BUCKET_PREFIX = 'https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/'
BROWSE_PREFIX = 'https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#'


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
        Base directory to look for ABC atlas release files. Fin
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
    release = {
        "version": version,
        "resource_uri": "s3://allen-brain-cell-atlas/",
        "directory_listing": {}
    }

    for directory in os.walk(base_dir):
        versions = []
        # Find only directories with properly formated date version
        # subdirectories
        for subdir in directory[1]:
            if not _validate_version(subdir):
                continue
        # If we find a version  select either the max version
        if versions:
            max_version = max(versions)
            split_dir = str(PurePosixPath(directory[0])).split('/')
            data_set = split_dir[-1]
            if any([data_set.startswith(skip) for skip in dirs_to_skip]):
                print(f"Skipping dataset: {data_set}")
                continue
            if version < max_version and version not in versions:
                raise ValueError(
                    "Requested version is less older than max version for "
                    f"{data_set} and specified version is not found. Please "
                    "select a valid release version. Versions "
                    f"available {versions}. Exiting."
                )
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


def populate_paths_and_urls(
        base_dir: Union[str, Path],
        release: dict,
        bucket_prefix: str,
        browse_prefix: str
) -> dict:
    """

    Parameters
    ----------
    base_dir
    release

    Returns
    -------

    """
    for data_set in release['directory_listing'].keys():

        print('-', data_set)
        ds_dict = release['directory_listing'][data_set]['directories']

        for data_dir in ds_dict.keys():

            print('--', data_dir)
            ver_dict = ds_dict[data_dir]
            rel_path = os.path.join(data_dir, data_set, ver_dict['version'])
            full_path = os.path.join(base_dir, rel_path)
            bucket_url = bucket_prefix + rel_path + '/'
            browse_url = browse_prefix + rel_path + '/'

            if not os.path.isdir(full_path):
                print("ERROR: %s not a directory" % full_path)

            print('---', rel_path)
            print('---', bucket_url)
            print('---', browse_url)

            ver_dict['relative_path'] = rel_path
            ver_dict['url'] = bucket_url
            ver_dict['view_link'] = browse_url
    return release


def populate_datasets(
        base_dir: Union[str, Path],
        release: dict,
        bucket_prefix: str,
) -> dict:
    """

    Parameters
    ----------
    base_dir
    release
    bucket_prefix

    Returns
    -------

    """
    datasets = {}

    for data_set in release['directory_listing'].keys():

        print('-', data_set)
        ds_dict = release['directory_listing'][data_set]['directories']
        datasets[data_set] = {}

        for m in ds_dict.keys():

            print('--', m)
            datasets[data_set][m] = {}
            ver_dict = ds_dict[m]

            data_dir = os.path.join(base_dir, ver_dict['relative_path'])
            # print('---',data_dir)

            total_size = 0

            for file_path in ['*', '*/*']:

                for full_path in glob.glob(
                        os.path.join(data_dir, file_path),
                        recursive=True
                ):
                    if os.path.isdir(full_path):
                        continue

                    print(full_path)
                    file_size = os.path.getsize(full_path)
                    total_size += file_size

                    rel_path = os.path.relpath(full_path, base_dir)
                    # print('--',rel_path)

                    bname = os.path.basename(full_path)
                    # print('---',bname)

                    bsplit = os.path.splitext(bname)
                    ext = bsplit[1]
                    ext = ext.replace('.', '')
                    # print('---',ext)

                    file_hash = file_hash_from_path(full_path)

                    if ext == 'csv':
                        tag = bsplit[0]
                        datasets[data_set][m][tag] = {}
                        datasets[data_set][m][tag]['files'] = {}
                        datasets[data_set][m][tag]['files'][ext] = {}
                        datasets[data_set][m][tag]['files'][ext]['version'] = \
                        ds_dict[m]['version']
                        datasets[data_set][m][tag]['files'][ext][
                            'relative_path'] = rel_path
                        datasets[data_set][m][tag]['files'][ext][
                            'url'] = bucket_prefix + rel_path
                        datasets[data_set][m][tag]['files'][ext]['size'] = file_size
                        datasets[data_set][m][tag]['files'][ext][
                            'file_hash'] = file_hash
                    elif ext == 'h5ad':

                        if '-raw.h5ad' in bname:
                            tag = bname.split('-raw.h5ad')[0]
                            norm = 'raw'
                        elif '-log2.h5ad' in bname:
                            tag = bname.split('-log2.h5ad')[0]
                            norm = 'log2'

                        if tag not in datasets[data_set][m].keys():
                            datasets[data_set][m][tag] = {}

                        datasets[data_set][m][tag][norm] = {}
                        datasets[data_set][m][tag][norm]['files'] = {}
                        datasets[data_set][m][tag][norm]['files'][ext] = {}
                        datasets[data_set][m][tag][norm]['files'][ext]['version'] = \
                        ds_dict[m]['version']
                        datasets[data_set][m][tag][norm]['files'][ext][
                            'relative_path'] = rel_path
                        datasets[data_set][m][tag][norm]['files'][ext][
                            'url'] = bucket_prefix + rel_path
                        datasets[data_set][m][tag][norm]['files'][ext][
                            'size'] = file_size
                        datasets[data_set][m][tag][norm]['files'][ext][
                            'file_hash'] = file_hash
                    elif ext == 'gz':
                        ext = 'nii.gz'
                        tag = bname.replace('.nii.gz', '')
                        datasets[data_set][m][tag] = {}
                        datasets[data_set][m][tag]['files'] = {}
                        datasets[data_set][m][tag]['files'][ext] = {}
                        datasets[data_set][m][tag]['files'][ext]['version'] = \
                        ds_dict[m]['version']
                        datasets[data_set][m][tag]['files'][ext][
                            'relative_path'] = rel_path
                        datasets[data_set][m][tag]['files'][ext][
                            'url'] = bucket_prefix + rel_path
                        datasets[data_set][m][tag]['files'][ext]['size'] = \
                            file_size
                        datasets[data_set][m][tag]['files'][ext][
                            'file_hash'] = file_hash

                ver_dict['total_size'] = total_size

    release['file_listing'] = datasets
    return release


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument(
        "--abc_atlas_staging_path",
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--output_file",
        type=argparse.FileType('w'),
        required=True,
        help=""
    )
    parser.add_argument(
        "--manifest_version",
        type=str,
        required=True,
        help=""
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
        default=['releases', 'SEAAD', 'Zhuang-C57BL6J'],
        help=""
    )
    args = parser.parse_args()

    if not _validate_version(args.manifest_version):
        raise ValueError("Invalid version format. Please use %Y%m%d format "
                         "(e.g. 20240315)")
    browse_prefix = args.bucket_prefix + 'index.html#'

    output_release = find_directories(
        base_dir=args.abc_atlas_staging_path,
        version=args.manifest_version,
        dirs_to_skip=args.datasets_to_skip
    )
    output_release = populate_paths_and_urls(
        base_dir=args.abc_atlas_staging_path,
        release=output_release,
        bucket_prefix=args.bucket_prefix,
        browse_prefix=browse_prefix
    )
    output_release = populate_datasets(

    )