from typing import List
import time
import pandas as pd
import numpy as np
import anndata
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache


def get_gene_data(
    abc_atlas_cache: AbcProjectCache,
    all_cells: pd.DataFrame,
    all_genes: pd.DataFrame,
    selected_genes: List[str],
    data_type: str = "log2",
    chunk_size: int = 8192
):
    """Load expression matrix data from the ABC Atlas and extract data for
    specific genes.

    Method will load all expression data required to process across multiple
    files to extract the full set of genes. This may result in downloading
    potentially ~100 GB of data.

    Parameters
    ----------
    abc_atlas_cache: AbcProjectCache
        An AbcProjectCache instance object to handle downloading and serving
        the path to the expression matrix data.
    all_cells: pandas.DataFrame
        cells metadata loaded as a pandas Dataframe from the AbcProjectCache
        indexed on cell_label.
    all_genes: pandas.DataFrame
        genes metadata loaded as a pandas Dataframe from the AbcProjectCache
        indexed on gene_identifier.
    selected_genes: list of strings
        List of gene_symbols that are a subset of those in the full genes
        DataFrame.
    data_type: str (Default: "log2")
        Kind of expression matrix to load either "log2" or "raw". Defaults to
        "log2".
    chunk_size: int (Default: 8192)
        Size of the chunk to load from the anndata files. Adjust this size if
        needed based on memory/file io. Default: 8192.

    Returns
    -------
    output_gene_data: pandas.DataFrame
        Subset of gene data indexed by cell.
    """
    # Create a mask for the requested genes.
    gene_mask = np.isin(all_genes.gene_symbol, selected_genes)
    gene_filtered = all_genes[gene_mask]
    # Initialize our output DataFrame.
    output_gene_data = pd.DataFrame(index=all_cells.index,
                                    columns=gene_filtered.index)

    num_total_cells = len(all_cells)

    # Get the names of the data in the ABC atlas that we need
    # to load.
    matrices = all_cells.groupby(
        ['dataset_label', 'feature_matrix_label']
    )[[all_cells.columns[0]]].count()
    matrices.columns = ['cell_count']

    total_start = time.process_time()
    # Loop over all data files.
    num_processed_cells = 0
    for matrix_index in matrices.index:
        directory = matrix_index[0]
        matrix_file = matrix_index[1]

        print("loading file:", matrix_file)

        file_path = abc_atlas_cache.get_data_path(
            directory=directory,
            file_name=f"{matrix_file}/{data_type}"
        )

        start = time.process_time()
        expression_data = anndata.read_h5ad(file_path, backed='r')
        obs = expression_data.obs
        # Loop over each chunk of the file, slicing by gene
        # and storing the data in the output DataFrame.
        for chunk, min_idx, max_idx in expression_data.chunked_X(
                chunk_size=chunk_size):
            cell_indexes = obs.index[min_idx:max_idx]
            cell_mask = cell_indexes.isin(all_cells.index)
            subcell_indexes = cell_indexes[cell_mask]
            num_processed_cells += len(subcell_indexes)
            output_gene_data.loc[
                    subcell_indexes, gene_filtered.index] = \
                chunk.toarray()[cell_mask][:, gene_mask]

        expression_data.file.close()
        del expression_data  # Clean up our loaded file.
        print(f" - time taken:  {time.process_time() - start}")

    output_gene_data.columns = gene_filtered.gene_symbol
    print(f"total time taken: {time.process_time() - total_start}")
    print(
        "\ttotal cells:", num_total_cells,
        "processed cells:", num_processed_cells
    )
    return output_gene_data
