"""
Chunked data readers for memory-efficient processing of large datasets.

Supports both CSV and AnnData h5ad files with consistent interface.
"""

from pathlib import Path
from typing import Iterator, Optional, Tuple
import pandas as pd
import anndata as ad


class ChunkedDataReader:
    """
    Memory-efficient chunked reader for CSV and h5ad files.

    Parameters
    ----------
    file_path : str
        Path to input file
    chunk_size : int
        Number of rows per chunk (default: 10000)
    index_col : str, optional
        Name of index column
    """

    def __init__(self, file_path: str, chunk_size: int = 10000, index_col: Optional[str] = None):
        self.file_path = Path(file_path)
        self.chunk_size = chunk_size
        self.index_col = index_col
        self._is_h5ad = str(file_path).endswith('.h5ad')
        self._total_rows = None
        self._columns = None

        if not self.file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        # Initialize and get metadata
        self._initialize()

    def _initialize(self):
        """Initialize reader and extract metadata."""
        if self._is_h5ad:
            # Use backed mode for memory-mapped access
            adata = ad.read_h5ad(self.file_path, backed='r')
            self._total_rows = adata.n_obs
            self._columns = list(adata.obs.columns)

            # Handle index column
            if self.index_col:
                if self.index_col not in self._columns:
                    # Index column might be the obs index
                    self._columns = [self.index_col] + self._columns
                    self._index_is_obs_index = True
                else:
                    self._index_is_obs_index = False
            else:
                self._index_is_obs_index = False

            # Close the backed file
            adata.file.close()
        else:
            # Get CSV metadata without loading full file
            first_chunk = pd.read_csv(self.file_path, nrows=1)
            self._columns = list(first_chunk.columns)

            # Count total rows (efficient way)
            with open(self.file_path, 'rb') as f:
                self._total_rows = sum(1 for _ in f) - 1  # Subtract header

    @property
    def total_rows(self) -> int:
        """Total number of rows in the dataset."""
        return self._total_rows

    @property
    def columns(self) -> list:
        """List of column names."""
        return self._columns

    @property
    def n_chunks(self) -> int:
        """Number of chunks the data will be split into."""
        return (self._total_rows + self.chunk_size - 1) // self.chunk_size

    def __iter__(self) -> Iterator[pd.DataFrame]:
        """
        Iterate over chunks of data.

        Yields
        ------
        pd.DataFrame
            Chunk of data with shape (chunk_size, n_columns)
        """
        if self._is_h5ad:
            yield from self._iter_h5ad()
        else:
            yield from self._iter_csv()

    def _iter_h5ad(self) -> Iterator[pd.DataFrame]:
        """Iterate over h5ad file in chunks."""
        # Read with backed mode for memory efficiency
        adata = ad.read_h5ad(self.file_path, backed='r')

        try:
            n_obs = adata.n_obs
            for start_idx in range(0, n_obs, self.chunk_size):
                end_idx = min(start_idx + self.chunk_size, n_obs)

                # Extract chunk from obs table
                chunk_df = adata.obs[start_idx:end_idx].copy()

                # Handle index column
                if self.index_col and self._index_is_obs_index:
                    chunk_df = chunk_df.reset_index()
                    if self.index_col not in chunk_df.columns:
                        chunk_df = chunk_df.rename(columns={chunk_df.columns[0]: self.index_col})

                yield chunk_df
        finally:
            # Ensure file is closed
            adata.file.close()

    def _iter_csv(self) -> Iterator[pd.DataFrame]:
        """Iterate over CSV file in chunks."""
        # Use pandas chunksize parameter for memory-efficient reading
        for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size):
            yield chunk

    def get_info(self) -> dict:
        """
        Get dataset information without loading full data.

        Returns
        -------
        dict
            Dictionary with total_rows, n_columns, columns, n_chunks
        """
        return {
            'file_path': str(self.file_path),
            'file_type': 'h5ad' if self._is_h5ad else 'csv',
            'total_rows': self._total_rows,
            'n_columns': len(self._columns),
            'columns': self._columns,
            'chunk_size': self.chunk_size,
            'n_chunks': self.n_chunks
        }


def get_dataset_info(file_path: str, index_col: Optional[str] = None) -> dict:
    """
    Get dataset information without loading full file into memory.

    Parameters
    ----------
    file_path : str
        Path to input file
    index_col : str, optional
        Name of index column

    Returns
    -------
    dict
        Dataset information
    """
    reader = ChunkedDataReader(file_path, chunk_size=10000, index_col=index_col)
    return reader.get_info()
