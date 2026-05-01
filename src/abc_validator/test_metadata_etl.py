"""
Test script for metadata ETL process.
"""
import sys
import tempfile
from pathlib import Path
import pandas as pd

from metadata_etl import MetadataETL

def create_test_input():
    """Create a minimal test input CSV."""
    test_data = {
        'cell_label': ['CELL_001', 'CELL_002', 'CELL_003'],
        'cell_barcode': ['AAACAGCC', 'AAACAGCT', 'AAACAGGG'],
        'donor_label': ['H21.33.018', 'H21.33.018', 'H21.33.032'],
        'library_label': ['L8XR_231130_21_C02', 'L8XR_231130_21_C02', 'L8XR_231207_01_H07'],
        'barcoded_cell_sample_label': ['1963_B06', '1963_B06', '1981_C09'],
        'alignment_job_id': ['job123', 'job123', 'job124'],
        'doublet_score': [0.027, 0.054, 0.0],
        'umi_count': [15259, 20645, 2551]
    }

    df = pd.DataFrame(test_data)
    return df

def test_basic_etl():
    """Test basic ETL functionality."""
    print("Testing metadata ETL...")

    # Create test input
    test_df = create_test_input()

    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Write test input
        input_path = tmpdir / 'test_input.csv'
        test_df.to_csv(input_path, index=False)
        print(f"Created test input: {input_path}")

        # Output directory
        output_dir = tmpdir / 'output'
        output_dir.mkdir()

        # LIMS directory
        lims_dir = Path('/data/allen-brain-cell-atlas-staging/abc_kb_ingest/SEA-AD/UC5-SEA-AD-20_260226/lims')

        if not lims_dir.exists():
            print(f"ERROR: LIMS directory not found: {lims_dir}")
            print("Please provide a valid LIMS directory path")
            return False

        # Run ETL
        try:
            etl = MetadataETL(
                input_path=str(input_path),
                lims_dir=str(lims_dir),
                output_dir=str(output_dir)
            )

            etl.run()

            # Check outputs
            print("\nOutput files created:")
            for output_file in output_dir.glob('*.csv'):
                df = pd.read_csv(output_file)
                print(f"  {output_file.name}: {len(df)} rows, {len(df.columns)} columns")

            # Display sample of each output
            print("\nSample outputs:")

            donor_path = output_dir / 'donor.csv'
            if donor_path.exists():
                donor_df = pd.read_csv(donor_path)
                print(f"\nDonor table ({len(donor_df)} rows):")
                print(donor_df.head())

            library_path = output_dir / 'library.csv'
            if library_path.exists():
                library_df = pd.read_csv(library_path)
                print(f"\nLibrary table ({len(library_df)} rows):")
                print(library_df.head())

            cell_path = output_dir / 'cell_metadata.csv'
            if cell_path.exists():
                cell_df = pd.read_csv(cell_path)
                print(f"\nCell metadata table ({len(cell_df)} rows):")
                print(cell_df.head())

            # Display validation report
            report_path = output_dir / 'validation_report.txt'
            if report_path.exists():
                print("\nValidation report:")
                print(report_path.read_text())

            print("\nTest completed successfully!")
            return True

        except Exception as e:
            print(f"\nERROR: Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = test_basic_etl()
    sys.exit(0 if success else 1)
