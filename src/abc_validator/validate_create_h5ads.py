import argparse
from anndata import experimental
import pandas as pd

from anndata_utils import copy_umis_and_mask_data, log2_normalize_and_save


def 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_h5ad",
        type=str,
        required=True,
        help="",
    )
    parser.add_argument(
        "--is_raw",
        type=str,
        required=True,
        help="",
    )
    parser.add_argument(
        "--raw_location",
        type=str,
        default="X",
        help="",
    )
    parser.add_argument(
        "--obs_path",
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--obs_mask_path",
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--var_path",
        type=str, required=True,
        help=""
    )
    args = parser.parse_args()

