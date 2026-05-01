#!/usr/bin/env python3
"""
Memory-efficient command-line tool for validating CSV and AnnData files.

Uses chunked processing to handle large datasets without loading entire files into memory.

Validates:
- Index uniqueness
- Categorical features (triplets: base, base_color, base_order)
- Hierarchical features (nested categorical features)
- Numerical features (no missing values)

Example usage:
    python validate_abc_atlas_inputs.py \\
        --input data.csv \\
        --index-col cell_id \\
        --categorical "cluster,region,class" \\
        --hierarchical "class,subclass,cluster" \\
        --output validation_report.json \\
        --chunk-size 50000
"""

import argparse
import sys
from pathlib import Path

from chunked_reader import ChunkedDataReader, get_dataset_info
from validation_functions import (
    validate_index_uniqueness_chunked,
    validate_categorical_and_hierarchical_features_chunked,
    validate_numerical_features_chunked,
    generate_validation_report
)


def detect_categorical_from_columns(columns: list) -> list:
    """
    Auto-detect categorical triplets from column names without loading data.

    Parameters
    ----------
    columns : list
        List of column names

    Returns
    -------
    list
        List of base column names that form categorical triplets
    """
    categorical_bases = []
    columns_set = set(columns)

    for col in columns:
        # Skip if it's already a _color or _order column
        if col.endswith('_color') or col.endswith('_order'):
            continue

        color_col = f"{col}_color"
        order_col = f"{col}_order"

        # Check if both companions exist
        if color_col in columns_set and order_col in columns_set:
            categorical_bases.append(col)

    return sorted(categorical_bases)


def main():
    """Main entry point for the validation tool."""
    parser = argparse.ArgumentParser(
        description='Validate data columns in CSV or AnnData files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--input',
        required=True,
        help='Path to input CSV or h5ad file'
    )

    parser.add_argument(
        '--index-col',
        required=True,
        help='Name of the index column to validate for uniqueness'
    )

    parser.add_argument(
        '--categorical',
        default='',
        help='Comma-separated list of categorical base column names. '
             'For each base name, expects base_color and base_order columns. '
             'If not specified, will auto-detect based on column naming patterns.'
    )

    parser.add_argument(
        '--hierarchical',
        default='',
        help='Comma-separated list of hierarchical base column names. '
             'Must be a subset of --categorical. These columns should form nested hierarchies.'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='Path to output JSON validation report'
    )

    parser.add_argument(
        '--n-cpus',
        type=int,
        default=None,
        help='Number of CPUs to use for parallel processing (default: all available)'
    )

    parser.add_argument(
        '--chunk-size',
        type=int,
        default=10000,
        help='Chunk size for processing large dataframes (default: 10000)'
    )

    args = parser.parse_args()

    try:
        # Get dataset info without loading full data
        print(f"Inspecting dataset: {args.input}")
        dataset_info = get_dataset_info(args.input, args.index_col)
        print(f"  File type: {dataset_info['file_type']}")
        print(f"  Total rows: {dataset_info['total_rows']:,}")
        print(f"  Total columns: {dataset_info['n_columns']}")
        print(f"  Chunk size: {args.chunk_size}")
        print(f"  Number of chunks: {dataset_info['n_chunks']}")

        # Parse categorical and hierarchical columns
        if args.categorical:
            categorical = [c.strip() for c in args.categorical.split(',') if c.strip()]
            print(f"\nUsing user-specified categorical columns: {categorical}")
        else:
            # Auto-detect categorical triplets from column names
            print(f"\nAuto-detecting categorical triplets...")
            categorical = detect_categorical_from_columns(dataset_info['columns'])
            if categorical:
                print(f"  Detected {len(categorical)} categorical triplet(s): {categorical}")
            else:
                print(f"  No categorical triplets detected")

        hierarchical = [h.strip() for h in args.hierarchical.split(',') if h.strip()]

        # Validate that hierarchical is subset of categorical
        if hierarchical:
            if not categorical:
                print("Error: --hierarchical specified but no categorical columns found/specified")
                sys.exit(1)

            invalid_hier = [h for h in hierarchical if h not in categorical]
            if invalid_hier:
                print(f"Error: Hierarchical columns must be subset of categorical columns. "
                      f"Invalid: {invalid_hier}")
                sys.exit(1)

        print(f"\nValidation configuration:")
        print(f"  Index column: {args.index_col}")
        print(f"  Categorical columns: {categorical if categorical else 'None'}")
        print(f"  Hierarchical columns: {hierarchical if hierarchical else 'None'}")
        print(f"  Memory-efficient chunked processing enabled")
        print()

        # Run validations with chunked processing
        results = {}

        # Create chunked data reader
        data_reader = ChunkedDataReader(
            args.input,
            chunk_size=args.chunk_size,
            index_col=args.index_col
        )

        # 1. Validate index uniqueness
        print("=" * 60)
        print("Validating index uniqueness...")
        print("=" * 60)
        results['index'] = validate_index_uniqueness_chunked(
            iter(data_reader),
            args.index_col,
            data_reader.total_rows
        )
        if results['index']['is_valid']:
            print("✓ Index validation passed")
        else:
            dup_count = results['index'].get('count', 0)
            print(f"✗ Index validation failed: {dup_count} duplicate values found")

        # 2. Validate categorical and hierarchical features in a SINGLE pass
        non_hierarchical_categorical = [c for c in categorical if c not in hierarchical]

        if non_hierarchical_categorical or hierarchical:
            print("\n" + "=" * 60)
            if non_hierarchical_categorical and hierarchical:
                print("Validating categorical and hierarchical features (single pass)...")
            elif hierarchical:
                print("Validating hierarchical features...")
            else:
                print("Validating categorical features...")
            print("=" * 60)

            # Single pass validation for both categorical and hierarchical features
            results['categorical'], results['hierarchical'] = validate_categorical_and_hierarchical_features_chunked(
                data_reader, non_hierarchical_categorical, hierarchical, args.index_col
            )

            # Report categorical results
            if non_hierarchical_categorical:
                passed = sum(1 for v in results['categorical'].values() if v.get('is_valid', False))
                total = len(non_hierarchical_categorical)
                if passed == total:
                    print(f"✓ All {total} categorical features passed validation")
                else:
                    print(f"✗ {passed}/{total} categorical features passed validation")

            # Report hierarchical results
            if hierarchical:
                if results['hierarchical']['is_valid']:
                    print("✓ Hierarchical validation passed")
                    print(f"  Detected hierarchy order: {results['hierarchical'].get('hierarchy_order', [])}")
                    print(f"  Generated {len(results['hierarchical'].get('hierarchy_tables', []))} hierarchy entries")
                else:
                    print("✗ Hierarchical validation failed")
                    hier_errors = len(results['hierarchical'].get('hierarchy_errors', []))
                    order_errors = len(results['hierarchical'].get('order_preservation_errors', []))
                    print(f"  Hierarchy errors: {hier_errors}")
                    print(f"  Order preservation errors: {order_errors}")

        # 4. Validate numerical features
        print("\n" + "=" * 60)
        print("Validating numerical features...")
        print("=" * 60)

        # Build exclude list: index + all categorical triplets
        exclude = [args.index_col]
        for base in categorical:
            exclude.extend([base, f"{base}_color", f"{base}_order"])

        results['numerical'] = validate_numerical_features_chunked(
            iter(data_reader),
            exclude,
            args.index_col,
            data_reader.total_rows,
            data_reader.columns
        )

        if results['numerical']['is_valid']:
            print("✓ Numerical validation passed (no missing values)")
        else:
            cols_with_missing = len(results['numerical']['columns'])
            print(f"✗ Numerical validation failed: {cols_with_missing} columns have missing values")

        # Generate report
        print("\n" + "=" * 60)
        print("Generating validation report...")
        print("=" * 60)
        generate_validation_report(results, args.output)
        print(f"✓ Report saved to: {args.output}")

        # Print summary
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        # Check overall validity
        # - Non-hierarchical categorical features
        categorical_valid = True
        if 'categorical' in results:
            categorical_valid = all(v.get('is_valid', False)
                                   for v in results['categorical'].values())

        # - Hierarchical features (includes categorical validation for hierarchical features)
        hierarchical_valid = True
        if 'hierarchical' in results:
            hierarchical_valid = results['hierarchical']['is_valid']

        overall_valid = (
            results['index']['is_valid'] and
            results['numerical']['is_valid'] and
            categorical_valid and
            hierarchical_valid
        )

        if overall_valid:
            print("✓ ALL VALIDATIONS PASSED")
            return 0
        else:
            print("✗ VALIDATION FAILED - See report for details")
            return 1

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
