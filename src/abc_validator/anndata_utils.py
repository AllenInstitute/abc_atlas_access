from anndata import experimental
import anndata
import h5py
import numpy as np
import os
import pandas as pd
from pathlib import Path
from scipy.sparse import csr_matrix
import tqdm
from multiprocessing import Pool, cpu_count

from cell_type_mapper.utils.anndata_manipulation import amalgamate_csr_to_x

def mask_data(
        input_array: np.ndarray,
        mask: np.ndarray,
        enforce_type: str = None
) -> csr_matrix:
    """
    Normalize a 2D array into log2 values and return a csr_matrix.

    Enforce typing of the input array.

    Parameters
    ----------
    input_array: np.ndarray
        2D array to normalize by row.
    norm_value: float
        Value to normalize by.

    Returns
    -------
    csr_matrix:
        Normalized csr_matrix.
    """
    masked_array = input_array[mask]
    if enforce_type is not None:
        masked_array = masked_array.astype(enforce_type)
    return csr_matrix(masked_array)


def _process_chunk_copy_umis(args):
    """
    Worker function for parallel processing of chunks in copy_umis_and_mask_data.
    Must be a top-level function to be picklable.
    """
    (chunk_idx, idx_min, idx_max, input_h5ad, output_dir,
     obs_mask_slice, full_obs_df_slice, obs_df_index,
     enforce_type, raw_location) = args

    # Open a connection to the input h5ad file in this worker process
    input_anndata = experimental.read_lazy(input_h5ad)

    # Copy the specific information needed by anndata.
    sub_mask = obs_mask_slice
    sub_obs_df = full_obs_df_slice

    if np.all(sub_mask != sub_obs_df.index.isin(obs_df_index)):
        raise RuntimeError(f"Mismatched masking for chunk: {chunk_idx}")

    if sub_mask.sum() == 0:
        return chunk_idx, 0, 0  # chunk_idx, rows_processed, max_value

    if raw_location is None:
        input_row = input_anndata.X[idx_min:idx_max].__array__()
    else:
        input_row = input_anndata.layers['UMIs'][idx_min:idx_max].__array__()

    row_max = input_row.max()

    normed_csr = mask_data(
        input_row,
        mask=sub_mask,
        enforce_type=enforce_type
    )

    # Write to chunk file
    output_file_path = output_dir / f'chunk_{str(chunk_idx).zfill(6)}'
    with h5py.File(output_file_path, 'w') as output_file:
        for dataset_name in ['data', 'indices', 'indptr']:
            output_file.create_dataset(
                data=normed_csr.__getattribute__(dataset_name),
                name=dataset_name,
                shape=normed_csr.__getattribute__(dataset_name).shape,
                dtype=normed_csr.__getattribute__(dataset_name).dtype,
                chunks=True,
                compression='gzip',
                compression_opts=4,
            )

    return chunk_idx, sub_mask.sum(), row_max


def copy_umis_and_mask_data(
        obs_dataframe_csv: Path,
        var_dataframe_csv: Path,
        mask_dataframe_csv: Path,
        input_h5ad: Path,
        output_h5ad: Path,
        output_dir: Path,
        obs_index='cell_label',
        var_index='gene_identifier',
        n_chunks: int = 128,
        enforce_type: str = None,
        raw_location: str = None,
        n_cpus: int = None
):
    if n_cpus is None:
        n_cpus = cpu_count()

    full_obs_df = pd.read_csv(
        obs_dataframe_csv,
        dtype={obs_index: str,
               'alignment_job_id': str}
    ).set_index(obs_index)
    var_df = pd.read_csv(
        var_dataframe_csv,
        dtype={var_index: str,
               'gene_symbol': str}
    ).set_index(var_index)
    obs_df = pd.read_csv(
        mask_dataframe_csv,
        dtype={obs_index: str,
               'alignment_job_id': str}
    ).set_index('cell_label')

    obs_mask = full_obs_df.index.isin(obs_df.index)

    # input_anndata = anndata.read_h5ad(input_h5ad, backed='r')
    input_anndata = experimental.read_lazy(input_h5ad)
    open_anndata = anndata.AnnData(
        obs=obs_df,
        var=var_df,
    )
    open_anndata.write_h5ad(output_h5ad)
    print('Created base h5ad file...')

    pbar = tqdm.tqdm(desc='Number of rows processed',
                     total=len(obs_df),
                     unit='rows')
    final_x_shape = (
        len(obs_df),
        input_anndata.layers['UMIs'].shape[1]
    )

    output_dir.mkdir(exist_ok=True)
    indices = np.linspace(start=0, stop=input_anndata.X.shape[0], num=n_chunks, dtype=int)

    # Prepare arguments for parallel processing
    chunk_args = []
    for chunk_idx, (idx_min, idx_max) in enumerate(zip(indices[:-1], indices[1:])):
        obs_mask_slice = obs_mask[idx_min:idx_max]
        full_obs_df_slice = full_obs_df.iloc[idx_min:idx_max]

        chunk_args.append((
            chunk_idx, idx_min, idx_max, input_h5ad, output_dir,
            obs_mask_slice, full_obs_df_slice, obs_df.index,
            enforce_type, raw_location
        ))

    # Process chunks in parallel
    max_value = 0
    with Pool(processes=n_cpus) as pool:
        for chunk_idx, rows_processed, row_max in pool.imap_unordered(_process_chunk_copy_umis, chunk_args):
            if rows_processed == 0:
                print('Empty row for chunk:', chunk_idx)
            else:
                if row_max > max_value:
                    max_value = row_max
            pbar.update(rows_processed)

    pbar.close()

    print('max_value:', max_value)
    src_path_list = sorted(output_dir.glob('chunk_*'))
    amalgamate_csr_to_x(src_path_list=src_path_list,
                        dst_path=output_h5ad,
                        final_shape=final_x_shape,
                        compression=True)


def log2_normalize_row(
        input_array: np.ndarray,
        norm_value: float = 1000000
) -> csr_matrix:
    """
    Normalize a 2D array into log2 values and return a csr_matrix.

    Enforce typing of the input array.

    Parameters
    ----------
    input_array: np.ndarray
        2D array to normalize by row.
    norm_value: float
        Value to normalize by.

    Returns
    -------
    csr_matrix:
        Normalized csr_matrix.
    """
    normalized_array = np.log2(
        input_array / input_array.sum(axis=1)[:, np.newaxis]
        * np.float32(norm_value) + 1
    ).astype('float32', copy=False)
    return csr_matrix(normalized_array)


def _process_chunk_log2_normalize(args):
    """
    Worker function for parallel processing of chunks in log2_normalize_and_save.
    Must be a top-level function to be picklable.
    """
    chunk_idx, input_h5ad, output_dir, chunk_size, norm_value, idx_min, idx_max = args

    # Open a connection to the input h5ad file in this worker process
    input_anndata = anndata.read_h5ad(input_h5ad, backed='r')

    # Read the chunk
    input_row = input_anndata.X[idx_min:idx_max]

    # Normalize
    normed_csr = log2_normalize_row(
        input_row.toarray(),
        norm_value
    )

    # Write to chunk file
    output_file_path = output_dir / f'chunk_{str(chunk_idx).zfill(6)}'
    with h5py.File(output_file_path, 'w') as output_file:
        for dataset_name in ['data', 'indices', 'indptr']:
            output_file.create_dataset(
                data=normed_csr.__getattribute__(dataset_name),
                name=dataset_name,
                shape=normed_csr.__getattribute__(dataset_name).shape,
                dtype=normed_csr.__getattribute__(dataset_name).dtype,
                chunks=True,
                compression='gzip',
                compression_opts=4,
            )

    return chunk_idx, idx_max - idx_min


def log2_normalize_and_save(
        obs_dataframe_csv: Path,
        var_dataframe_csv: Path,
        input_h5ad: Path,
        output_h5ad: Path,
        output_dir: Path,
        obs_index='cell_label',
        var_index='gene_identifier',
        chunk_size: int = 8192,
        norm_value: float = 1000000,
        n_cpus: int = None
):

    if n_cpus is None:
        n_cpus = cpu_count()

    obs_df = pd.read_csv(
        obs_dataframe_csv,
        dtype={obs_index: str}
    ).set_index(obs_index)
    if 'alignment_job_id' in obs_df.columns:
        obs_df = obs_df.astype({'alignment_job_id': 'str'})
    var_df = pd.read_csv(
        var_dataframe_csv,
        dtype={var_index: str,
               'gene_symbol': str}
    ).set_index(var_index)

    input_anndata = anndata.read_h5ad(input_h5ad, backed='r')
    open_anndata = anndata.AnnData(
        obs=obs_df,
        var=var_df,
    )
    open_anndata.write_h5ad(output_h5ad)
    print('Created base h5ad file...')

    pbar = tqdm.tqdm(desc='Number of rows processed',
                     total=input_anndata.shape[0],
                     unit='rows')
    x_shape = input_anndata.X.shape

    output_dir.mkdir(exist_ok=True)

    # Prepare chunk arguments for parallel processing
    chunk_args = []
    chunk_idx = 0
    for idx_min in range(0, x_shape[0], chunk_size):
        idx_max = min(idx_min + chunk_size, x_shape[0])
        chunk_args.append((
            chunk_idx, input_h5ad, output_dir, chunk_size, norm_value, idx_min, idx_max
        ))
        chunk_idx += 1

    # Process chunks in parallel
    with Pool(processes=n_cpus) as pool:
        for chunk_idx, rows_processed in pool.imap_unordered(_process_chunk_log2_normalize, chunk_args):
            pbar.update(rows_processed)

    pbar.close()

    src_path_list = sorted(output_dir.glob('chunk_*'))
    amalgamate_csr_to_x(src_path_list=src_path_list,
                        dst_path=output_h5ad,
                        final_shape=x_shape,
                        compression=True)