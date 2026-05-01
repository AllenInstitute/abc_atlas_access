import argparse
from anndata import experimental
import pandas as pd
import time


def build_bextl_output(
        input_obs_path: str,
        input_col_type: str,
        input_col_name: str,
        output_dir: str,
        output_project_name: str
):
    time.tzset()
    date = time.strftime('%Y-%m-%d')
    obs = pd.read_csv(input_obs_path)
    if input_col_name == 'barcoded_cell_sample':
        output_bextl = pd.DataFrame(
            data=[
                {
                    "mode": "lims_10x_selected_barcoded_cell_samples",
                    "library_package_name": output_project_name,
                    "sequencing_center_id": output_project_name,
                    "library_package_submission_date": date,
                    "input_barcoded_cell_sample_list": load_name
                } for load_name in sorted(obs['input_col_name'].unique())
            ]
        )
    elif input_col_name == 'library_aliquot':
        output_bextl = pd.DataFrame(
            data=[
                {
                    "mode": "lims_10x_selected_aliquots",
                    "library_package_name": output_project_name,
                    "sequencing_center_id": output_project_name,
                    "library_package_submission_date": date,
                    "project_identifier": "N/A",
                    "library_pool_tag": "N/A",
                    "input_library_aliquot_list": load_name
                } for load_name in sorted(obs['input_col_name'].unique())
            ]
        )
    elif input_col_name == 'library_label':
        raise("Library label not implemented. Exiting.")
        output_bextl = pd.DataFrame(
            data=[
                {
                    "mode": "lims_10x_selected_aliquots",
                    "library_package_name": output_project_name,
                    "sequencing_center_id": output_project_name,
                    "library_package_submission_date": date,
                    "project_identifier": "N/A",
                    "library_pool_tag": "N/A",
                    "input_library_aliquot_list": load_name
                } for load_name in sorted(obs['input_col_name'].unique())
            ]
        )
    output_bextl.to_csv(
        output_path,
        index=False
    )


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

    build_bextl_output(
        input_obs_path=args['input_obs_path'],
        input_col_type=args['input_col_type'],
        input_col_name=args['input_col_name'],
        output_dir=args['output_dir'],
        output_project_name=args['output_project_name']
    )