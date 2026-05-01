"""
Memory-efficient ETL for processing cell metadata with LIMS validation.

This module processes input tables (CSV or h5ad obs) and combines them with
flattened LIMS metadata to produce normalized output files: cell_metadata.csv,
donor.csv, and library.csv.
"""
import argparse
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import multiprocessing as mp
from functools import partial

import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MetadataETL:
    """ETL processor for cell metadata with LIMS validation."""

    # Required columns for each output table
    REQUIRED_CELL_METADATA = {
        'cell_label', 'cell_barcode', 'barcoded_cell_sample_label',
        'donor_label', 'library_label', 'alignment_job_id'
    }

    REQUIRED_DONOR = {
        'donor_label', 'donor_species', 'donor_sex', 'donor_age',
        'donor_age_value', 'donor_age_unit'
    }

    REQUIRED_LIBRARY = {
        'library_label', 'library_method', 'barcoded_cell_sample_label',
        'cell_specimen_type', 'donor_label'
    }

    # Column name mappings (LIMS local_name -> output label)
    COLUMN_MAPPINGS = {
        'donor_local_name': 'donor_label',
        'library_local_name': 'library_label',
        'barcoded_cell_sample_local_name': 'barcoded_cell_sample_label',
        'enriched_cell_sample_local_name': 'enriched_cell_sample_label',
        'tissue_sample_local_name': 'tissue_sample_label',
        'dissociated_cell_sample_local_name': 'dissociated_cell_sample_label',
        'library_technique': 'library_method',
        'biological_sex': 'donor_sex',
        'donor_species': 'donor_species',
        'age_at_death_value': 'donor_age_value',
        'age_at_death_unit': 'donor_age_unit',
        'age_at_death_description': 'donor_age',
        'enrichment_population': 'enrichment_population',
        'roi_local_name': 'region_of_interest_label',
        'roi_id': 'roi_id',
    }

    # Species mappings
    SPECIES_MAPPINGS = {
        'NCBITaxon:9606': {
            'scientific_name': 'Homo sapiens',
            'genus': 'Human'
        },
        'NCBITaxon:9544': {
            'scientific_name': 'Macaca mulatta',
            'genus': 'Macaque'
        },
        'NCBITaxon:9545': {
            'scientific_name': 'Macaca nemestrina',
            'genus': 'Macaque'
        },
        'NCBITaxon:9483': {
            'scientific_name': 'Callithrix jacchus',
            'genus': 'Marmoset'
        }
    }

    def __init__(
        self,
        input_path: str,
        lims_dir: str,
        output_dir: str,
        cell_label_col: str = 'cell_label',
        donor_label_col: str = 'donor_label',
        library_label_col: str = 'library_label',
        barcoded_cell_sample_col: str = 'barcoded_cell_sample_label',
        chunk_size: int = 100000
    ):
        """
        Initialize the ETL processor.

        Args:
            input_path: Path to input CSV or h5ad file
            lims_dir: Directory containing LIMS data (summary.csv and csv/ subdirectory)
            output_dir: Directory for output files
            cell_label_col: Column name for cell labels in input
            donor_label_col: Column name for donor labels in input
            library_label_col: Column name for library labels in input
            barcoded_cell_sample_col: Column name for barcoded_cell_sample labels in input
            chunk_size: Number of rows to process at once for memory efficiency
        """
        self.input_path = Path(input_path)
        self.lims_dir = Path(lims_dir)
        self.output_dir = Path(output_dir)
        self.cell_label_col = cell_label_col
        self.donor_label_col = donor_label_col
        self.library_label_col = library_label_col
        self.barcoded_cell_sample_col = barcoded_cell_sample_col
        self.chunk_size = chunk_size

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.validation_errors = []
        self.validation_warnings = []

    def get_input_iterator(self):
        """
        Get an iterator for chunked reading of input data.
        Note: Creates a new iterator each time it's called.

        Returns:
            Iterator yielding DataFrames in chunks
        """
        if self.input_path.suffix == '.csv':
            return pd.read_csv(self.input_path, chunksize=self.chunk_size)
        elif self.input_path.suffix in ['.h5ad', '.h5']:
            import anndata
            logger.info(f"Loading h5ad file: {self.input_path}")
            adata = anndata.read_h5ad(self.input_path)
            obs_df = adata.obs.copy()
            # Create a generator that yields chunks
            def chunk_generator():
                for i in range(0, len(obs_df), self.chunk_size):
                    yield obs_df.iloc[i:i+self.chunk_size]
            return chunk_generator()
        else:
            raise ValueError(f"Unsupported input format: {self.input_path.suffix}")

    def get_unique_labels_from_input(self):
        """
        Extract unique donor, library, and sample labels from input without loading all data.

        Returns:
            Dictionary with unique label sets
        """
        logger.info("Extracting unique labels from input data")

        unique_labels = {
            'donors': set(),
            'libraries': set(),
            'samples': set()
        }

        row_count = 0
        for chunk in self.get_input_iterator():
            row_count += len(chunk)
            if self.donor_label_col in chunk.columns:
                unique_labels['donors'].update(chunk[self.donor_label_col].dropna().unique())
            if self.library_label_col in chunk.columns:
                unique_labels['libraries'].update(chunk[self.library_label_col].dropna().unique())
            if self.barcoded_cell_sample_col in chunk.columns:
                unique_labels['samples'].update(chunk[self.barcoded_cell_sample_col].dropna().unique())

        logger.info(f"Scanned {row_count:,} rows from input")
        logger.info(f"Found {len(unique_labels['donors'])} unique donors")
        logger.info(f"Found {len(unique_labels['libraries'])} unique libraries")
        logger.info(f"Found {len(unique_labels['samples'])} unique samples")

        return unique_labels, row_count

    def load_lims_metadata(self) -> Dict[str, pd.DataFrame]:
        """
        Load LIMS metadata from summary.csv and csv/ directory.

        Returns:
            Dictionary mapping table names to DataFrames
        """
        logger.info("Loading LIMS metadata")
        lims_data = {}

        # Load summary.csv
        summary_path = self.lims_dir / 'summary.csv'
        if summary_path.exists():
            logger.info(f"Loading {summary_path}")
            lims_data['summary'] = pd.read_csv(summary_path, low_memory=False)

        # Load CSV directory tables
        csv_dir = self.lims_dir / 'csv'
        if csv_dir.exists():
            for csv_file in csv_dir.glob('*.csv'):
                table_name = csv_file.stem
                logger.info(f"Loading {csv_file}")
                lims_data[table_name] = pd.read_csv(csv_file, low_memory=False)

        return lims_data

    def apply_column_mappings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply column name mappings (local_name -> label).

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with renamed columns
        """
        rename_dict = {
            col: self.COLUMN_MAPPINGS[col]
            for col in df.columns
            if col in self.COLUMN_MAPPINGS
        }

        if rename_dict:
            logger.info(f"Renaming columns: {rename_dict}")
            df = df.rename(columns=rename_dict)

        return df

    def validate_labels(
        self,
        unique_labels: Dict[str, set],
        lims_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, List[str]]:
        """
        Validate donor, library, and barcoded_cell_sample labels against LIMS.

        Args:
            unique_labels: Dictionary of unique label sets from input
            lims_data: LIMS metadata tables

        Returns:
            Dictionary of validation results
        """
        logger.info("Validating labels against LIMS data")
        validation_results = {
            'missing_donors': [],
            'missing_libraries': [],
            'missing_barcoded_cell_samples': [],
            'overlapping_values': []
        }

        # Check against LIMS data
        if 'donor' in lims_data:
            lims_donors = set(lims_data['donor']['donor_local_name'].dropna().unique())
            missing = unique_labels['donors'] - lims_donors
            if missing:
                validation_results['missing_donors'] = list(missing)
                self.validation_errors.append(f"Missing donors in LIMS: {len(missing)} donors")

        if 'library' in lims_data:
            lims_libraries = set(lims_data['library']['library_local_name'].dropna().unique())
            missing = unique_labels['libraries'] - lims_libraries
            if missing:
                validation_results['missing_libraries'] = list(missing)
                self.validation_errors.append(f"Missing libraries in LIMS: {len(missing)} libraries")

        if 'barcoded_cell_sample' in lims_data and unique_labels['samples']:
            lims_samples = set(lims_data['barcoded_cell_sample']['barcoded_cell_sample_local_name'].dropna().unique())
            missing = unique_labels['samples'] - lims_samples
            if missing:
                validation_results['missing_barcoded_cell_samples'] = list(missing)
                self.validation_errors.append(f"Missing barcoded cell samples in LIMS: {len(missing)} samples")

        return validation_results

    def build_lims_lookups(self, lims_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Build lookup tables from LIMS data for efficient merging.

        Args:
            lims_data: LIMS metadata tables

        Returns:
            Dictionary of processed LIMS lookup tables
        """
        lookups = {}

        # Process and store each LIMS table with column mappings applied
        for table_name, df in lims_data.items():
            df_mapped = self.apply_column_mappings(df.copy())

            # Convert key columns to string for consistent merging
            for col in ['donor_label', 'library_label', 'barcoded_cell_sample_label']:
                if col in df_mapped.columns:
                    df_mapped[col] = df_mapped[col].astype(str)

            lookups[table_name] = df_mapped

        # Build component linkages
        if 'barcoded_cell_sample_component' in lims_data:
            comp_df = lims_data['barcoded_cell_sample_component']
            lookups['bcs_to_enriched'] = {}
            for _, row in comp_df.iterrows():
                if pd.notna(row.get('barcoded_cell_sample_local_name')) and pd.notna(row.get('enriched_cell_sample_local_name')):
                    lookups['bcs_to_enriched'][row['barcoded_cell_sample_local_name']] = row['enriched_cell_sample_local_name']

        if 'dissociated_cell_sample_component' in lims_data:
            comp_df = lims_data['dissociated_cell_sample_component']
            lookups['enriched_to_dcs'] = {}
            lookups['dcs_to_tissue'] = {}
            for _, row in comp_df.iterrows():
                if pd.notna(row.get('enriched_cell_sample_local_name')) and pd.notna(row.get('dissociated_cell_sample_local_name')):
                    lookups['enriched_to_dcs'][row['enriched_cell_sample_local_name']] = row['dissociated_cell_sample_local_name']
                if pd.notna(row.get('dissociated_cell_sample_local_name')) and pd.notna(row.get('tissue_sample_local_name')):
                    lookups['dcs_to_tissue'][row['dissociated_cell_sample_local_name']] = row['tissue_sample_local_name']

        return lookups

    def merge_chunk_with_lims(
        self,
        chunk: pd.DataFrame,
        lims_lookups: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        """
        Merge a chunk of input data with LIMS metadata.

        Args:
            chunk: Input data chunk
            lims_lookups: Pre-processed LIMS lookup tables

        Returns:
            Merged DataFrame
        """
        merged = chunk.copy()

        # First, rename input columns to standard names
        input_renames = {}
        if self.cell_label_col in merged.columns and self.cell_label_col != 'cell_label':
            input_renames[self.cell_label_col] = 'cell_label'
        if self.donor_label_col in merged.columns and self.donor_label_col != 'donor_label':
            input_renames[self.donor_label_col] = 'donor_label'
        if self.library_label_col in merged.columns and self.library_label_col != 'library_label':
            input_renames[self.library_label_col] = 'library_label'
        if self.barcoded_cell_sample_col in merged.columns and self.barcoded_cell_sample_col != 'barcoded_cell_sample_label':
            input_renames[self.barcoded_cell_sample_col] = 'barcoded_cell_sample_label'

        # Handle common barcode column names
        if 'bc' in merged.columns and 'cell_barcode' not in merged.columns:
            input_renames['bc'] = 'cell_barcode'

        # Handle ar_id as alignment_job_id
        if 'ar_id' in merged.columns:
            input_renames['ar_id'] = 'alignment_job_id'

        if input_renames:
            merged = merged.rename(columns=input_renames)

        # Convert key columns to string to avoid type mismatch during merges
        for col in ['donor_label', 'library_label', 'barcoded_cell_sample_label', 'cell_label']:
            if col in merged.columns:
                merged[col] = merged[col].astype(str)

        # Apply LIMS column mappings
        merged = self.apply_column_mappings(merged)

        # Merge with donor data
        if 'donor' in lims_lookups and 'donor_label' in merged.columns:
            donor_df = lims_lookups['donor']
            merged = merged.merge(
                donor_df,
                left_on='donor_label',
                right_on='donor_label',
                how='left',
                suffixes=('', '_donor')
            )

        # Merge library data using library_label
        if 'library' in lims_lookups and 'library_label' in merged.columns:
            library_df = lims_lookups['library']
            merged = merged.merge(
                library_df,
                on='library_label',
                how='left',
                suffixes=('', '_library')
            )

        return merged

    def merge_with_lims(
        self,
        input_df: pd.DataFrame,
        lims_data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        """
        Merge input data with LIMS metadata.

        Args:
            input_df: Input data
            lims_data: LIMS metadata tables

        Returns:
            Merged DataFrame
        """
        logger.info("Merging input data with LIMS metadata")

        merged = input_df.copy()

        # Apply column mappings to input
        merged = self.apply_column_mappings(merged)

        # Merge with summary if available
        if 'summary' in lims_data:
            summary = self.apply_column_mappings(lims_data['summary'].copy())

            # Determine merge keys based on available columns
            merge_keys = []
            if 'library_label' in merged.columns and 'library_label' in summary.columns:
                merge_keys.append('library_label')
            if 'donor_label' in merged.columns and 'donor_label' in summary.columns:
                merge_keys.append('donor_label')

            if merge_keys:
                logger.info(f"Merging with summary on: {merge_keys}")
                merged = merged.merge(
                    summary,
                    on=merge_keys,
                    how='left',
                    suffixes=('', '_lims')
                )

        # Merge with specific LIMS tables
        if 'donor' in lims_data and 'donor_label' in merged.columns:
            donor_df = self.apply_column_mappings(lims_data['donor'].copy())
            merged = merged.merge(
                donor_df,
                on='donor_label',
                how='left',
                suffixes=('', '_donor')
            )

        if 'library' in lims_data and 'library_label' in merged.columns:
            library_df = self.apply_column_mappings(lims_data['library'].copy())
            merged = merged.merge(
                library_df,
                on='library_label',
                how='left',
                suffixes=('', '_library')
            )

        if 'barcoded_cell_sample' in lims_data and 'barcoded_cell_sample_label' in merged.columns:
            sample_df = self.apply_column_mappings(lims_data['barcoded_cell_sample'].copy())
            merged = merged.merge(
                sample_df,
                on='barcoded_cell_sample_label',
                how='left',
                suffixes=('', '_sample')
            )

        # Merge enriched_cell_sample information if available
        if 'enriched_cell_sample' in lims_data:
            enriched_df = self.apply_column_mappings(lims_data['enriched_cell_sample'].copy())

            # First try to link via barcoded_cell_sample to enriched_cell_sample
            if 'barcoded_cell_sample' in lims_data:
                bcs_df = lims_data['barcoded_cell_sample'].copy()
                # Check if barcoded_cell_sample links to enriched_cell_sample
                if 'barcoded_cell_sample_source_type' in bcs_df.columns:
                    # Get the linkage - many barcoded samples may come from one enriched sample
                    bcs_to_enriched = {}
                    if 'barcoded_cell_sample_component' in lims_data:
                        # Use component table to find linkages
                        comp_df = lims_data['barcoded_cell_sample_component'].copy()
                        for _, row in comp_df.iterrows():
                            if pd.notna(row.get('barcoded_cell_sample_local_name')) and pd.notna(row.get('enriched_cell_sample_local_name')):
                                bcs_to_enriched[row['barcoded_cell_sample_local_name']] = row['enriched_cell_sample_local_name']

                    # Add enriched sample linkage to barcoded_cell_sample data
                    if bcs_to_enriched and 'barcoded_cell_sample_label' in merged.columns:
                        merged['enriched_cell_sample_label'] = merged['barcoded_cell_sample_label'].map(bcs_to_enriched)

                        # Merge enriched cell sample metadata
                        merge_cols = ['enriched_cell_sample_label'] + [
                            col for col in enriched_df.columns
                            if col not in merged.columns and col != 'enriched_cell_sample_label'
                        ]
                        if len(merge_cols) > 1:
                            merged = merged.merge(
                                enriched_df[merge_cols],
                                on='enriched_cell_sample_label',
                                how='left',
                                suffixes=('', '_enriched')
                            )

        # Merge dissociated_cell_sample to get cell prep type
        if 'dissociated_cell_sample' in lims_data:
            dcs_df = self.apply_column_mappings(lims_data['dissociated_cell_sample'].copy())

            # Link via enriched_cell_sample if available
            if 'enriched_cell_sample_label' in merged.columns and 'dissociated_cell_sample_component' in lims_data:
                comp_df = lims_data['dissociated_cell_sample_component'].copy()
                enriched_to_dcs = {}
                for _, row in comp_df.iterrows():
                    if pd.notna(row.get('enriched_cell_sample_local_name')) and pd.notna(row.get('dissociated_cell_sample_local_name')):
                        enriched_to_dcs[row['enriched_cell_sample_local_name']] = row['dissociated_cell_sample_local_name']

                if enriched_to_dcs:
                    merged['dissociated_cell_sample_label'] = merged['enriched_cell_sample_label'].map(enriched_to_dcs)

                    # Merge dissociated cell sample metadata
                    merge_cols = ['dissociated_cell_sample_label'] + [
                        col for col in dcs_df.columns
                        if col not in merged.columns and col != 'dissociated_cell_sample_label'
                    ]
                    if len(merge_cols) > 1:
                        merged = merged.merge(
                            dcs_df[merge_cols],
                            on='dissociated_cell_sample_label',
                            how='left',
                            suffixes=('', '_dissociated')
                        )

        # Merge tissue information if available
        if 'tissue_sample' in lims_data:
            tissue = lims_data['tissue_sample'].copy()

            # Merge with structure if available BEFORE applying column mappings
            if 'tissue_sample_structure' in lims_data:
                tissue_struct = lims_data['tissue_sample_structure'].copy()
                tissue = tissue.merge(
                    tissue_struct,
                    on='tissue_sample_local_name',
                    how='left'
                )
                # Rename structure to parcellation_term_identifier if needed
                if 'structure' in tissue.columns and 'parcellation_term_identifier' not in tissue.columns:
                    tissue = tissue.rename(columns={'structure': 'parcellation_term_identifier'})

            # Apply column mappings AFTER merging with structure
            tissue = self.apply_column_mappings(tissue)

            # Link tissue to dissociated_cell_sample
            if 'dissociated_cell_sample_label' in merged.columns and 'dissociated_cell_sample_component' in lims_data:
                comp_df = lims_data['dissociated_cell_sample_component'].copy()
                dcs_to_tissue = {}
                for _, row in comp_df.iterrows():
                    if pd.notna(row.get('dissociated_cell_sample_local_name')) and pd.notna(row.get('tissue_sample_local_name')):
                        dcs_to_tissue[row['dissociated_cell_sample_local_name']] = row['tissue_sample_local_name']

                if dcs_to_tissue:
                    merged['tissue_sample_label'] = merged['dissociated_cell_sample_label'].map(dcs_to_tissue)

                    # Merge tissue metadata
                    merge_cols = ['tissue_sample_label'] + [
                        col for col in tissue.columns
                        if col not in merged.columns and col != 'tissue_sample_label'
                    ]
                    if len(merge_cols) > 1 and 'tissue_sample_label' in tissue.columns:
                        merged = merged.merge(
                            tissue[merge_cols],
                            on='tissue_sample_label',
                            how='left',
                            suffixes=('', '_tissue')
                        )

        return merged

    def extract_donor_metadata(self, merged_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract donor metadata table.

        Args:
            merged_df: Merged data

        Returns:
            Donor metadata DataFrame
        """
        logger.info("Extracting donor metadata")

        donor_cols = [col for col in merged_df.columns if col.startswith('donor_') or col in ['species', 'donor_label']]
        donor_cols = list(set(donor_cols + ['donor_label']))

        available_cols = [col for col in donor_cols if col in merged_df.columns]

        donor_df = merged_df[available_cols].drop_duplicates(subset=['donor_label'])

        # Ensure required columns exist
        for req_col in self.REQUIRED_DONOR:
            if req_col not in donor_df.columns:
                logger.warning(f"Required donor column missing: {req_col}")
                donor_df[req_col] = None

        # Create donor_age from value and unit if missing
        if 'donor_age' not in donor_df.columns and 'donor_age_value' in donor_df.columns and 'donor_age_unit' in donor_df.columns:
            donor_df['donor_age'] = donor_df.apply(
                lambda row: f"{row['donor_age_value']} {row['donor_age_unit']}" if pd.notna(row['donor_age_value']) else None,
                axis=1
            )

        # Add species scientific name and genus if missing
        if 'donor_species' in donor_df.columns:
            if 'species_scientific_name' not in donor_df.columns:
                donor_df['species_scientific_name'] = donor_df['donor_species'].map(
                    lambda x: self.SPECIES_MAPPINGS.get(x, {}).get('scientific_name') if pd.notna(x) else None
                )
            if 'species_genus' not in donor_df.columns:
                donor_df['species_genus'] = donor_df['donor_species'].map(
                    lambda x: self.SPECIES_MAPPINGS.get(x, {}).get('genus') if pd.notna(x) else None
                )

        return donor_df

    def extract_library_metadata(self, merged_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract library metadata table.

        Args:
            merged_df: Merged data

        Returns:
            Library metadata DataFrame
        """
        logger.info("Extracting library metadata")

        library_cols = [col for col in merged_df.columns if col.startswith('library_') or col in [
            'barcoded_cell_sample_label', 'donor_label', 'enrichment_population',
            'barcoded_cell_sample_technique', 'parcellation_term_identifier',
            'region_of_interest_name', 'region_of_interest_label',
            'anatomical_division_label', 'specimen_dissected_roi_label',
            'specimen_dissected_roi_nhash_id', 'slab_label', 'slab_nhash_id'
        ]]
        library_cols = list(set(library_cols + ['library_label', 'barcoded_cell_sample_label', 'donor_label']))

        available_cols = [col for col in library_cols if col in merged_df.columns]

        library_df = merged_df[available_cols].drop_duplicates(subset=['library_label'])

        # Ensure required columns exist
        for req_col in self.REQUIRED_LIBRARY:
            if req_col not in library_df.columns:
                logger.warning(f"Required library column missing: {req_col}")
                library_df[req_col] = None

        # Infer cell_specimen_type from enrichment_population or technique if missing
        if 'cell_specimen_type' not in library_df.columns:
            library_df['cell_specimen_type'] = None

        # Fill in cell_specimen_type if missing
        if library_df['cell_specimen_type'].isna().any():
            if 'enrichment_population' in library_df.columns:
                # If enrichment mentions NeuN or is nuclear, it's likely Nuclei
                def infer_specimen_type(pop):
                    if pd.isna(pop):
                        return None
                    pop_str = str(pop)
                    if 'NeuN' in pop_str or 'OLIG' in pop_str or 'Nurr' in pop_str:
                        return 'Nuclei'
                    return None

                mask = library_df['cell_specimen_type'].isna()
                library_df.loc[mask, 'cell_specimen_type'] = library_df.loc[mask, 'enrichment_population'].apply(infer_specimen_type)

            # Use technique to infer specimen type if still missing
            if 'barcoded_cell_sample_technique' in library_df.columns:
                mask = library_df['cell_specimen_type'].isna()
                library_df.loc[mask, 'cell_specimen_type'] = 'Nuclei'

        return library_df

    def extract_cell_metadata(self, merged_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract cell metadata table.

        Args:
            merged_df: Merged data

        Returns:
            Cell metadata DataFrame
        """
        logger.info("Extracting cell metadata")

        # Ensure required columns exist
        for req_col in self.REQUIRED_CELL_METADATA:
            if req_col not in merged_df.columns:
                logger.warning(f"Required cell metadata column missing: {req_col}")
                merged_df[req_col] = None

        # Select cell-level columns
        cell_cols = list(self.REQUIRED_CELL_METADATA)

        # Add optional columns that are cell-specific
        optional_cell_cols = [
            'doublet_score', 'umi_count', 'feature_matrix_label',
            'dataset_label', 'abc_sample_id'
        ]

        for col in optional_cell_cols:
            if col in merged_df.columns:
                cell_cols.append(col)

        # Add any other columns that vary per cell
        for col in merged_df.columns:
            if col not in cell_cols and col not in ['donor_label', 'library_label']:
                # Check if column varies per cell
                if merged_df.groupby('cell_label')[col].nunique().max() > 1:
                    cell_cols.append(col)

        available_cols = [col for col in cell_cols if col in merged_df.columns]
        cell_df = merged_df[available_cols].copy()

        return cell_df


    def write_validation_report(self, validation_results: Dict[str, List[str]]):
        """
        Write validation report to file.

        Args:
            validation_results: Validation results dictionary
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("VALIDATION REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")

        if self.validation_errors:
            report_lines.append("ERRORS:")
            for error in self.validation_errors:
                report_lines.append(f"  - {error}")
            report_lines.append("")

        if self.validation_warnings:
            report_lines.append("WARNINGS:")
            for warning in self.validation_warnings:
                report_lines.append(f"  - {warning}")
            report_lines.append("")

        for key, values in validation_results.items():
            if values:
                report_lines.append(f"{key.upper()}: {len(values)} items")
                for value in values[:10]:
                    report_lines.append(f"  - {value}")
                if len(values) > 10:
                    report_lines.append(f"  ... and {len(values) - 10} more")
                report_lines.append("")

        if not self.validation_errors and not self.validation_warnings:
            report_lines.append("No validation errors or warnings found.")

        report_path = self.output_dir / 'validation_report.txt'
        report_path.write_text('\n'.join(report_lines))
        logger.info(f"Wrote validation_report.txt")

    def write_outputs(
        self,
        donor_df: pd.DataFrame,
        library_df: pd.DataFrame,
        cell_df: pd.DataFrame,
        validation_results: Dict[str, List[str]]
    ):
        """
        Write output CSV files.

        Args:
            donor_df: Donor metadata
            library_df: Library metadata
            cell_df: Cell metadata
            validation_results: Validation results
        """
        logger.info(f"Writing outputs to {self.output_dir}")

        # Write main tables
        donor_df.to_csv(self.output_dir / 'donor.csv', index=False)
        logger.info(f"Wrote donor.csv ({len(donor_df)} rows)")

        library_df.to_csv(self.output_dir / 'library.csv', index=False)
        logger.info(f"Wrote library.csv ({len(library_df)} rows)")

        cell_df.to_csv(self.output_dir / 'cell_metadata.csv', index=False)
        logger.info(f"Wrote cell_metadata.csv ({len(cell_df)} rows)")

        # Write validation report
        self.write_validation_report(validation_results)

    def run(self):
        """Run the complete ETL process with chunked data processing."""
        logger.info("Starting metadata ETL with chunked processing")

        # Load LIMS data (small, can fit in memory)
        lims_data = self.load_lims_metadata()
        logger.info(f"Loaded {len(lims_data)} LIMS tables")

        # Get unique labels from input without loading all data
        unique_labels, total_rows = self.get_unique_labels_from_input()

        # Validate labels
        validation_results = self.validate_labels(unique_labels, lims_data)

        # Build lookup tables from LIMS for efficient merging
        logger.info("Building LIMS lookup tables")
        lims_lookups = self.build_lims_lookups(lims_data)

        # Process input data in chunks and write cell metadata incrementally
        logger.info(f"Processing {total_rows:,} rows in chunks of {self.chunk_size:,}")

        cell_output_path = self.output_dir / 'cell_metadata.csv'
        first_chunk = True
        processed_rows = 0

        # Collect unique donor and library records
        donor_records = {}
        library_records = {}

        for chunk_num, chunk in enumerate(self.get_input_iterator(), 1):
            logger.info(f"Processing chunk {chunk_num} ({len(chunk):,} rows)")

            # Merge chunk with LIMS data
            merged_chunk = self.merge_chunk_with_lims(chunk, lims_lookups)

            # Extract cell metadata from this chunk
            cell_chunk = self.extract_cell_metadata(merged_chunk)

            # Write cell metadata (append mode after first chunk)
            cell_chunk.to_csv(
                cell_output_path,
                mode='w' if first_chunk else 'a',
                header=first_chunk,
                index=False
            )
            first_chunk = False
            processed_rows += len(chunk)

            # Collect unique donor and library records (use standardized column names)
            for _, row in merged_chunk.iterrows():
                if 'donor_label' in row and pd.notna(row['donor_label']):
                    donor_label = row['donor_label']
                    if donor_label not in donor_records:
                        donor_records[donor_label] = row.to_dict()

                if 'library_label' in row and pd.notna(row['library_label']):
                    library_label = row['library_label']
                    if library_label not in library_records:
                        library_records[library_label] = row.to_dict()

            if chunk_num % 10 == 0:
                logger.info(f"Progress: {processed_rows:,}/{total_rows:,} rows ({100*processed_rows/total_rows:.1f}%)")

        logger.info(f"Processed all {processed_rows:,} rows")
        logger.info(f"Writing cell_metadata.csv ({processed_rows:,} rows)")

        # Create donor and library DataFrames from collected records
        logger.info("Creating donor and library tables")
        donor_df = pd.DataFrame(list(donor_records.values()))
        library_df = pd.DataFrame(list(library_records.values()))

        # Extract and clean donor metadata
        donor_df_clean = self.extract_donor_metadata(donor_df)
        library_df_clean = self.extract_library_metadata(library_df)

        # Write donor and library tables
        donor_df_clean.to_csv(self.output_dir / 'donor.csv', index=False)
        logger.info(f"Wrote donor.csv ({len(donor_df_clean)} rows)")

        library_df_clean.to_csv(self.output_dir / 'library.csv', index=False)
        logger.info(f"Wrote library.csv ({len(library_df_clean)} rows)")

        # Write validation report
        self.write_validation_report(validation_results)

        logger.info("ETL complete")

        if self.validation_errors:
            logger.error(f"Completed with {len(self.validation_errors)} validation errors")
        else:
            logger.info("Completed successfully with no validation errors")


def main():
    """Main entry point for the ETL."""
    parser = argparse.ArgumentParser(
        description='Process cell metadata with LIMS validation'
    )

    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Path to input CSV or h5ad file'
    )

    parser.add_argument(
        '--lims-dir',
        type=str,
        required=True,
        help='Directory containing LIMS data (with summary.csv and csv/ subdirectory)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        required=True,
        help='Directory for output files'
    )

    parser.add_argument(
        '--cell-label-col',
        type=str,
        default='cell_label',
        help='Column name for cell labels (default: cell_label)'
    )

    parser.add_argument(
        '--donor-label-col',
        type=str,
        default='donor_label',
        help='Column name for donor labels (default: donor_label)'
    )

    parser.add_argument(
        '--library-label-col',
        type=str,
        default='library_label',
        help='Column name for library labels (default: library_label)'
    )

    parser.add_argument(
        '--barcoded-cell-sample-col',
        type=str,
        default='barcoded_cell_sample_label',
        help='Column name for barcoded cell sample labels (default: barcoded_cell_sample_label)'
    )

    parser.add_argument(
        '--chunk-size',
        type=int,
        default=100000,
        help='Chunk size for processing (default: 100000)'
    )

    args = parser.parse_args()

    etl = MetadataETL(
        input_path=args.input,
        lims_dir=args.lims_dir,
        output_dir=args.output_dir,
        cell_label_col=args.cell_label_col,
        donor_label_col=args.donor_label_col,
        library_label_col=args.library_label_col,
        barcoded_cell_sample_col=args.barcoded_cell_sample_col,
        chunk_size=args.chunk_size
    )

    etl.run()


if __name__ == '__main__':
    main()
