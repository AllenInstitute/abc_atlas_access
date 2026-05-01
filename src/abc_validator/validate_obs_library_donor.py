import argparse
from anndata import experimental
import pandas as pd

import frictionless


def build_obs_library_donor():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_obs_path",
        type=str,
        required=True,
        help="",
    )
    parser.add_argument(
        "--input_col_type",
        type=str,
        choices=['barcoded_cell_sample', 'library_aliquot', 'library_label'],
        required=True,
        help="",
    )
    parser.add_argument(
        "--input_col_name",
        type=str,
        required=True,
        help="",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="",
    )
    parser.add_argument(
        "--output_project_name",
        type=str,
        required=True,
        help="",
    )
    args = parser.parse_args()

    build_obs_library_donor()