"""
Validation functions for CSV and AnnData files.

This module provides memory-efficient validation with multiprocessing support for:
- Index uniqueness
- Categorical features (base, color, order triplets)
- Hierarchical features (nested categorical features)
- Numerical features (no missing values)
"""

import json
import re
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Any, Tuple, Optional

import numpy as np
import pandas as pd
from tqdm import tqdm


def detect_categorical_triplets(df: pd.DataFrame) -> List[str]:
    """
    Auto-detect categorical triplets in a dataframe.

    Looks for columns that have both {base}_color and {base}_order companions.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe

    Returns
    -------
    list of str
        List of base column names that form categorical triplets
    """
    categorical_bases = []
    columns = set(df.columns)

    # Check each column to see if it's a base column with color and order companions
    for col in df.columns:
        # Skip if it's already a _color or _order column
        if col.endswith('_color') or col.endswith('_order'):
            continue

        color_col = f"{col}_color"
        order_col = f"{col}_order"

        # Check if both companions exist
        if color_col in columns and order_col in columns:
            categorical_bases.append(col)

    return sorted(categorical_bases)


def validate_index_uniqueness(df: pd.DataFrame, index_col: str) -> Dict[str, Any]:
    """
    Validate that all values in the index column are unique.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    index_col : str
        Name of the index column

    Returns
    -------
    dict
        Dictionary with 'is_valid' and 'duplicates' keys
    """
    if index_col not in df.columns:
        return {
            'is_valid': False,
            'error': f"Index column '{index_col}' not found in dataframe",
            'duplicates': []
        }

    index_values = df[index_col]
    duplicates = index_values[index_values.duplicated(keep=False)]

    if len(duplicates) == 0:
        return {'is_valid': True, 'duplicates': []}

    # Group by duplicate value to show all indices where each duplicate appears
    duplicate_groups = {}
    for dup_val in duplicates.unique():
        indices = df[df[index_col] == dup_val].index.tolist()
        duplicate_groups[str(dup_val)] = indices

    return {
        'is_valid': False,
        'duplicates': duplicate_groups,
        'count': len(duplicates.unique())
    }


def _is_valid_hex_color(color: str) -> bool:
    """Check if a string is a valid hex color code."""
    if pd.isna(color):
        return False
    color_str = str(color).strip()
    # Must start with # and have exactly 6 hex digits
    return bool(re.match(r'^#[0-9A-Fa-f]{6}$', color_str))


def validate_categorical_triplet(
    df: pd.DataFrame,
    base_name: str,
    index_col: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate a categorical triplet (base, base_color, base_order).

    Checks:
    - Each base value has a unique color/order pair
    - Colors are valid hex codes
    - Orders are integers and unique per base value
    - Reports indices where base is NaN/NULL (in separate output)
    - Reports base values where color/order is not set or not unique

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    base_name : str
        Base name of the categorical feature
    index_col : str, optional
        Name of index column for reporting (uses actual index values if provided)

    Returns
    -------
    dict
        Validation results with failures
    """
    color_col = f"{base_name}_color"
    order_col = f"{base_name}_order"

    # Check if columns exist
    missing_cols = []
    if base_name not in df.columns:
        missing_cols.append(base_name)
    if color_col not in df.columns:
        missing_cols.append(color_col)
    if order_col not in df.columns:
        missing_cols.append(order_col)

    if missing_cols:
        return {
            'is_valid': False,
            'error': f"Missing columns: {missing_cols}",
            'base_name': base_name
        }

    # Helper function to get index value (actual index column value or row index)
    def get_index_value(row_idx):
        if index_col and index_col in df.columns:
            return df.loc[row_idx, index_col]
        return int(row_idx)

    failures = {
        'base_name': base_name,
        'invalid_colors': [],
        'invalid_orders': [],
        'non_unique_color_order': []
    }

    # Separate output for NaN base values
    nan_base_info = {
        'base_name': base_name,
        'nan_indices': []
    }

    # Find NaN/NULL in base column
    nan_mask = df[base_name].isna()
    if nan_mask.any():
        nan_indices = [get_index_value(idx) for idx in df[nan_mask].index]
        nan_base_info['nan_indices'] = nan_indices

    # Work with non-NaN base values
    valid_df = df[~nan_mask].copy()

    if len(valid_df) == 0:
        failures['is_valid'] = True
        failures['nan_base_info'] = nan_base_info
        return failures

    # Validate colors and orders for each unique base value
    # Also collect order information in the same loop for efficiency
    base_value_orders = {}

    for base_value in valid_df[base_name].unique():
        mask = valid_df[base_name] == base_value
        subset = valid_df[mask]

        # Check colors
        colors = subset[color_col]
        orders = subset[order_col]

        # Validate hex colors
        for idx, color in zip(subset.index, colors):
            if not _is_valid_hex_color(color):
                failures['invalid_colors'].append({
                    'index': get_index_value(idx),
                    'base_value': str(base_value),
                    'color': str(color)
                })

        # Validate orders are integers and collect valid orders
        valid_orders = []
        for idx, order in zip(subset.index, orders):
            if pd.isna(order):
                failures['invalid_orders'].append({
                    'index': get_index_value(idx),
                    'base_value': str(base_value),
                    'order': None,
                    'error': 'missing'
                })
            else:
                try:
                    int_order = int(order)
                    if int_order != float(order):
                        failures['invalid_orders'].append({
                            'index': get_index_value(idx),
                            'base_value': str(base_value),
                            'order': str(order),
                            'error': 'not_integer'
                        })
                    else:
                        valid_orders.append(int_order)
                except (ValueError, TypeError):
                    failures['invalid_orders'].append({
                        'index': get_index_value(idx),
                        'base_value': str(base_value),
                        'order': str(order),
                        'error': 'cannot_convert_to_int'
                    })

        # Check that each base value has exactly ONE unique color/order pair
        # (the pair should be the same across all rows with this base value)
        unique_pairs = set()
        pair_to_indices = {}

        for idx, (color, order) in zip(subset.index, zip(colors, orders)):
            pair_key = (str(color), str(order))
            unique_pairs.add(pair_key)
            if pair_key not in pair_to_indices:
                pair_to_indices[pair_key] = []
            pair_to_indices[pair_key].append(get_index_value(idx))

        # If there's more than one unique pair for this base value, that's an error
        if len(unique_pairs) > 1:
            failures['non_unique_color_order'].append({
                'base_value': str(base_value),
                'error': 'multiple_color_order_pairs',
                'pairs_found': [
                    {
                        'color': pair[0],
                        'order': pair[1],
                        'indices': pair_to_indices[pair]
                    }
                    for pair in unique_pairs
                ]
            })

    # Determine if validation passed
    is_valid = all(
        len(failures[key]) == 0
        for key in ['invalid_colors', 'invalid_orders', 'non_unique_color_order']
    )
    failures['is_valid'] = is_valid
    failures['nan_base_info'] = nan_base_info

    return failures


def _validate_categorical_worker(args: Tuple) -> Dict[str, Any]:
    """Worker function for parallel categorical validation."""
    df, base_name, index_col = args
    return validate_categorical_triplet(df, base_name, index_col)


def validate_all_categorical_features(
    df: pd.DataFrame,
    categorical_bases: List[str],
    n_cpus: Optional[int] = None,
    index_col: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate multiple categorical features in parallel.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    categorical_bases : list of str
        List of base names for categorical features
    n_cpus : int, optional
        Number of CPUs to use
    index_col : str, optional
        Name of index column for reporting

    Returns
    -------
    dict
        Results for each categorical feature
    """
    if n_cpus is None:
        n_cpus = cpu_count()

    if not categorical_bases:
        return {}

    # Prepare arguments for parallel processing
    args_list = [(df, base_name, index_col) for base_name in categorical_bases]

    results = {}

    if len(categorical_bases) == 1 or n_cpus == 1:
        # Serial processing
        for base_name in tqdm(categorical_bases, desc="Validating categorical features"):
            results[base_name] = validate_categorical_triplet(df, base_name, index_col)
    else:
        # Parallel processing
        with Pool(processes=min(n_cpus, len(categorical_bases))) as pool:
            pbar = tqdm(total=len(categorical_bases), desc="Validating categorical features")
            for result in pool.imap_unordered(_validate_categorical_worker, args_list):
                results[result['base_name']] = result
                pbar.update(1)
            pbar.close()

    return results


def build_hierarchy_from_data(
    df: pd.DataFrame,
    hierarchical_bases: List[str]
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Auto-detect hierarchy relationships from data.

    Builds hierarchy by analyzing which values nest within others.
    Detects the hierarchy order automatically.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    hierarchical_bases : list of str
        List of column base names that should form hierarchies

    Returns
    -------
    tuple
        (hierarchy_tables, validation_errors)
    """
    errors = []

    # Get unique combinations of all hierarchical columns
    hier_cols = []
    order_cols = []
    for base in hierarchical_bases:
        if base in df.columns:
            hier_cols.append(base)
            order_col = f"{base}_order"
            if order_col in df.columns:
                order_cols.append(order_col)

    if not hier_cols:
        return {}, [{'error': 'No hierarchical columns found in dataframe'}]

    # Drop rows with any NaN in hierarchical columns
    valid_df = df[hier_cols + order_cols].dropna()

    # Get unique combinations
    unique_combos = valid_df[hier_cols].drop_duplicates()

    # Detect hierarchy order by analyzing relationships
    # Strategy: columns with more unique values are likely deeper in hierarchy
    hierarchy_order = sorted(
        hier_cols,
        key=lambda col: len(valid_df[col].unique())
    )

    # Build hierarchy tables - one table per leaf value
    hierarchy_tables = []

    # The deepest level (most unique values) is the leaf
    leaf_col = hierarchy_order[-1]

    for leaf_value in valid_df[leaf_col].unique():
        leaf_rows = valid_df[valid_df[leaf_col] == leaf_value]

        # Check if this leaf has multiple parents at any level
        for parent_col in hierarchy_order[:-1]:
            parent_values = leaf_rows[parent_col].unique()
            if len(parent_values) > 1:
                errors.append({
                    'error': 'multiple_parents',
                    'leaf_column': leaf_col,
                    'leaf_value': str(leaf_value),
                    'parent_column': parent_col,
                    'parent_values': [str(v) for v in parent_values]
                })

        # Get the first row (they should all be the same if hierarchy is valid)
        row_data = leaf_rows.iloc[0]

        # Build hierarchy entry
        hier_entry = {'leaf_column': leaf_col, 'leaf_value': str(leaf_value)}

        for col in hierarchy_order:
            hier_entry[col] = str(row_data[col])
            order_col = f"{col}_order"
            if order_col in row_data:
                hier_entry[order_col] = row_data[order_col]

        hierarchy_tables.append(hier_entry)

    return {
        'hierarchy_order': hierarchy_order,
        'tables': hierarchy_tables
    }, errors


def validate_hierarchical_features(
    df: pd.DataFrame,
    hierarchical_bases: List[str],
    n_cpus: Optional[int] = None,
    index_col: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate hierarchical categorical features.

    Performs categorical validation plus hierarchy-specific checks:
    - No child should have multiple parents
    - Order preservation when sorted by leaf order

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    hierarchical_bases : list of str
        List of base names for hierarchical features
    n_cpus : int, optional
        Number of CPUs to use
    index_col : str, optional
        Name of index column

    Returns
    -------
    dict
        Validation results including hierarchy tables
    """
    results = {
        'categorical_validation': {},
        'hierarchy_errors': [],
        'hierarchy_tables': [],
        'order_preservation_errors': []
    }

    # First, validate as categorical features
    results['categorical_validation'] = validate_all_categorical_features(
        df, hierarchical_bases, n_cpus, index_col
    )

    # Build and validate hierarchy
    hierarchy_data, hierarchy_errors = build_hierarchy_from_data(df, hierarchical_bases)
    results['hierarchy_errors'] = hierarchy_errors

    if 'tables' in hierarchy_data:
        results['hierarchy_tables'] = hierarchy_data['tables']
        results['hierarchy_order'] = hierarchy_data.get('hierarchy_order', [])

        # Validate order preservation
        # When sorted by leaf order, parent orders should be consistent
        if hierarchy_data.get('hierarchy_order'):
            leaf_col = hierarchy_data['hierarchy_order'][-1]
            leaf_order_col = f"{leaf_col}_order"

            # Create a dataframe from hierarchy tables
            hier_df = pd.DataFrame(hierarchy_data['tables'])

            if leaf_order_col in hier_df.columns:
                # Sort by leaf order
                hier_df_sorted = hier_df.sort_values(leaf_order_col)

                # Check each parent level
                for parent_col in hierarchy_data['hierarchy_order'][:-1]:
                    parent_order_col = f"{parent_col}_order"
                    if parent_order_col in hier_df_sorted.columns:
                        # Group by parent value and check if orders are consistent
                        for parent_val, group in hier_df_sorted.groupby(parent_col):
                            orders = group[parent_order_col].unique()
                            if len(orders) > 1:
                                results['order_preservation_errors'].append({
                                    'parent_column': parent_col,
                                    'parent_value': str(parent_val),
                                    'inconsistent_orders': [int(o) for o in orders]
                                })

    # Overall validity
    results['is_valid'] = (
        len(results['hierarchy_errors']) == 0 and
        len(results['order_preservation_errors']) == 0 and
        all(v.get('is_valid', False)
            for v in results['categorical_validation'].values())
    )

    return results


def _validate_numerical_chunk_worker(args: Tuple) -> Dict[str, List]:
    """Worker function for parallel numerical validation."""
    chunk_df, numerical_cols, index_col = args

    # Helper function to get index value (actual index column value or row index)
    def get_index_value(row_idx):
        if index_col and index_col in chunk_df.columns:
            return chunk_df.loc[row_idx, index_col]
        return int(row_idx)

    results = {}
    for col in numerical_cols:
        missing_mask = chunk_df[col].isna()
        if missing_mask.any():
            # Get actual index values (from index column or row indices)
            missing_indices = [get_index_value(idx) for idx in chunk_df[missing_mask].index]
            results[col] = missing_indices
        else:
            results[col] = []

    return results


def validate_numerical_features(
    df: pd.DataFrame,
    exclude_cols: List[str],
    n_cpus: Optional[int] = None,
    chunk_size: int = 10000,
    index_col: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate that numerical columns have no missing values.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    exclude_cols : list of str
        Columns to exclude from validation
    n_cpus : int, optional
        Number of CPUs to use
    chunk_size : int
        Size of chunks for parallel processing
    index_col : str, optional
        Name of index column for reporting (uses actual index values if provided)

    Returns
    -------
    dict
        Indices where values are missing for each column
    """
    if n_cpus is None:
        n_cpus = cpu_count()

    # Helper function to get index value (actual index column value or row index)
    def get_index_value(row_idx):
        if index_col and index_col in df.columns:
            return df.loc[row_idx, index_col]
        return int(row_idx)

    # Identify numerical columns (exclude specified columns)
    numerical_cols = [
        col for col in df.columns
        if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])
    ]

    if not numerical_cols:
        return {'is_valid': True, 'columns': {}}

    results = {col: [] for col in numerical_cols}

    # Process in chunks for memory efficiency
    n_rows = len(df)
    n_chunks = max(1, n_rows // chunk_size)

    if n_chunks == 1 or n_cpus == 1:
        # Serial processing
        for col in tqdm(numerical_cols, desc="Validating numerical features"):
            missing_mask = df[col].isna()
            if missing_mask.any():
                results[col] = [get_index_value(idx) for idx in df[missing_mask].index]
    else:
        # Parallel processing by chunks
        chunk_args = []
        for i in range(n_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, n_rows)
            chunk_df = df.iloc[start_idx:end_idx]
            chunk_args.append((chunk_df, numerical_cols, index_col))

        with Pool(processes=min(n_cpus, n_chunks)) as pool:
            pbar = tqdm(total=n_chunks, desc="Validating numerical features")
            for chunk_result in pool.imap_unordered(_validate_numerical_chunk_worker, chunk_args):
                for col, indices in chunk_result.items():
                    results[col].extend(indices)
                pbar.update(1)
            pbar.close()

    # Check if any column has missing values
    is_valid = all(len(indices) == 0 for indices in results.values())

    return {
        'is_valid': is_valid,
        'columns': {col: indices for col, indices in results.items() if len(indices) > 0}
    }


def _convert_to_json_serializable(obj):
    """Convert numpy/pandas types to JSON-serializable Python types."""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, (np.str_, str)):
        return str(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: _convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_convert_to_json_serializable(item) for item in obj]
    elif pd.isna(obj):
        return None
    else:
        return obj


# =============================================================================
# CHUNKED VALIDATION FUNCTIONS (Memory-Efficient)
# =============================================================================

def validate_index_uniqueness_chunked(
    data_iterator,
    index_col: str,
    total_rows: Optional[int] = None
) -> Dict[str, Any]:
    """
    Validate index uniqueness using chunked data iterator.

    Parameters
    ----------
    data_iterator : iterator
        Iterator yielding pandas DataFrames
    index_col : str
        Name of the index column
    total_rows : int, optional
        Total number of rows for progress bar

    Returns
    -------
    dict
        Validation results with duplicates
    """
    seen_indices = {}  # {index_value: [list of row numbers where it appears]}
    current_row = 0

    pbar = tqdm(total=total_rows, desc="Validating index uniqueness") if total_rows else None

    for chunk in data_iterator:
        if index_col not in chunk.columns:
            if pbar:
                pbar.close()
            return {
                'is_valid': False,
                'error': f"Index column '{index_col}' not found in dataframe",
                'duplicates': []
            }

        for idx, value in enumerate(chunk[index_col]):
            row_num = current_row + idx
            if pd.notna(value):
                if value not in seen_indices:
                    seen_indices[value] = []
                seen_indices[value].append(row_num)

        current_row += len(chunk)
        if pbar:
            pbar.update(len(chunk))

    if pbar:
        pbar.close()

    # Find duplicates
    duplicate_groups = {
        str(val): rows for val, rows in seen_indices.items() if len(rows) > 1
    }

    if duplicate_groups:
        return {
            'is_valid': False,
            'duplicates': duplicate_groups,
            'count': len(duplicate_groups)
        }
    else:
        return {'is_valid': True, 'duplicates': []}


def validate_categorical_triplet_chunked(
    data_iterator,
    base_name: str,
    index_col: Optional[str] = None,
    total_rows: Optional[int] = None
) -> Dict[str, Any]:
    """
    Validate categorical triplet using chunked data iterator.

    Uses a two-pass approach:
    1. Collect unique (base_value, color, order) combinations
    2. Validate consistency

    Parameters
    ----------
    data_iterator : iterator
        Iterator yielding pandas DataFrames
    base_name : str
        Base name of categorical feature
    index_col : str, optional
        Name of index column for reporting
    total_rows : int, optional
        Total number of rows for progress bar

    Returns
    -------
    dict
        Validation results
    """
    color_col = f"{base_name}_color"
    order_col = f"{base_name}_order"

    # Helper function to get index value
    def get_index_value(chunk_df, row_idx):
        if index_col and index_col in chunk_df.columns:
            return chunk_df.iloc[row_idx][index_col]
        return int(chunk_df.index[row_idx])

    # Storage for validation
    base_value_info = defaultdict(lambda: {
        'colors': set(),
        'orders': set(),
        'pairs': set(),
        'indices': []
    })
    nan_base_indices = []
    invalid_colors = []
    invalid_orders = []

    pbar = tqdm(total=total_rows, desc=f"Validating {base_name}") if total_rows else None

    # Pass 1: Collect data from all chunks
    for chunk in data_iterator:
        # Check if columns exist
        missing_cols = []
        if base_name not in chunk.columns:
            missing_cols.append(base_name)
        if color_col not in chunk.columns:
            missing_cols.append(color_col)
        if order_col not in chunk.columns:
            missing_cols.append(order_col)

        if missing_cols:
            if pbar:
                pbar.close()
            return {
                'is_valid': False,
                'error': f"Missing columns: {missing_cols}",
                'base_name': base_name
            }

        for row_idx in range(len(chunk)):
            base_value = chunk[base_name].iloc[row_idx]
            color = chunk[color_col].iloc[row_idx]
            order = chunk[order_col].iloc[row_idx]
            idx_value = get_index_value(chunk, row_idx)

            # Track NaN base values
            if pd.isna(base_value):
                nan_base_indices.append(idx_value)
                continue

            base_value_str = str(base_value)

            # Track index for this base value
            base_value_info[base_value_str]['indices'].append(idx_value)

            # Validate color
            if not _is_valid_hex_color(color):
                invalid_colors.append({
                    'index': idx_value,
                    'base_value': base_value_str,
                    'color': str(color)
                })

            # Validate order
            if pd.isna(order):
                invalid_orders.append({
                    'index': idx_value,
                    'base_value': base_value_str,
                    'order': None,
                    'error': 'missing'
                })
            else:
                try:
                    int_order = int(order)
                    if int_order != float(order):
                        invalid_orders.append({
                            'index': idx_value,
                            'base_value': base_value_str,
                            'order': str(order),
                            'error': 'not_integer'
                        })
                    else:
                        base_value_info[base_value_str]['orders'].add(int_order)
                except (ValueError, TypeError):
                    invalid_orders.append({
                        'index': idx_value,
                        'base_value': base_value_str,
                        'order': str(order),
                        'error': 'cannot_convert_to_int'
                    })

            # Track color/order pairs
            base_value_info[base_value_str]['colors'].add(str(color))
            base_value_info[base_value_str]['pairs'].add((str(color), str(order)))

        if pbar:
            pbar.update(len(chunk))

    if pbar:
        pbar.close()

    # Pass 2: Validate consistency
    non_unique_color_order = []

    for base_value, info in base_value_info.items():
        # Check if base value has multiple color/order pairs
        if len(info['pairs']) > 1:
            pair_details = []
            for pair in info['pairs']:
                pair_details.append({
                    'color': pair[0],
                    'order': pair[1],
                    'indices': info['indices']  # All indices for this base value
                })
            non_unique_color_order.append({
                'base_value': base_value,
                'error': 'multiple_color_order_pairs',
                'pairs_found': pair_details
            })

    # Build result
    failures = {
        'base_name': base_name,
        'invalid_colors': invalid_colors,
        'invalid_orders': invalid_orders,
        'non_unique_color_order': non_unique_color_order
    }

    nan_base_info = {
        'base_name': base_name,
        'nan_indices': nan_base_indices
    }

    is_valid = all(
        len(failures[key]) == 0
        for key in ['invalid_colors', 'invalid_orders', 'non_unique_color_order']
    )

    failures['is_valid'] = is_valid
    failures['nan_base_info'] = nan_base_info

    return failures


def validate_all_categorical_features_chunked(
    data_reader,
    categorical_bases: List[str],
    index_col: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate multiple categorical features using chunked reading.

    NOTE: This function is now a wrapper around validate_categorical_and_hierarchical_features_chunked.
    For new code that validates both categorical and hierarchical features, use the combined function
    directly for better performance (single data pass instead of two).

    Parameters
    ----------
    data_reader : ChunkedDataReader
        Chunked data reader instance
    categorical_bases : list of str
        List of base names for categorical features
    index_col : str, optional
        Name of index column for reporting

    Returns
    -------
    dict
        Results for each categorical feature
    """
    if not categorical_bases:
        return {}

    # Delegate to the combined function
    categorical_results, _ = validate_categorical_and_hierarchical_features_chunked(
        data_reader, categorical_bases, [], index_col
    )
    return categorical_results


def validate_categorical_and_hierarchical_features_chunked(
    data_reader,
    categorical_bases: List[str],
    hierarchical_bases: List[str],
    index_col: Optional[str] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Validate both categorical and hierarchical features in a SINGLE pass.

    Parameters
    ----------
    data_reader : ChunkedDataReader
        Chunked data reader instance
    categorical_bases : list of str
        List of base names for categorical-only features (non-hierarchical)
    hierarchical_bases : list of str
        List of base names for hierarchical features
    index_col : str, optional
        Name of index column

    Returns
    -------
    tuple
        (categorical_results, hierarchical_results)
    """
    # Combine all features to validate
    all_bases = list(set(categorical_bases + hierarchical_bases))

    if not all_bases:
        return {}, {}

    # Helper function to get index value
    def get_index_value(chunk_df, row_idx):
        if index_col and index_col in chunk_df.columns:
            return chunk_df.iloc[row_idx][index_col]
        return int(chunk_df.index[row_idx])

    # Initialize storage for ALL categorical features (both types)
    all_categorical_results = {}
    for base_name in all_bases:
        all_categorical_results[base_name] = {
            'base_name': base_name,
            'base_value_info': defaultdict(lambda: {
                'colors': set(),
                'orders': set(),
                'pairs': set(),
                'indices': []
            }),
            'nan_base_indices': [],
            'invalid_colors': [],
            'invalid_orders': []
        }

    # Setup hierarchy collection (only for hierarchical features)
    hier_cols = []
    order_cols = []
    for base in hierarchical_bases:
        hier_cols.append(base)
        order_cols.append(f"{base}_order")

    unique_combos = set()
    total_rows = data_reader.total_rows

    pbar = tqdm(total=total_rows, desc="Validating categorical & hierarchical features") if total_rows else None

    # SINGLE PASS: Process all categorical and hierarchical features together
    for chunk in data_reader:
        # Check that all required columns exist
        all_required_cols = set()
        for base_name in all_bases:
            all_required_cols.add(base_name)
            all_required_cols.add(f"{base_name}_color")
            all_required_cols.add(f"{base_name}_order")

        missing = [col for col in all_required_cols if col not in chunk.columns]
        if missing:
            if pbar:
                pbar.close()
            # Return error results
            error_categorical = {
                base: {'is_valid': False, 'error': f'Missing columns: {missing}', 'base_name': base}
                for base in categorical_bases
            }
            error_hierarchical = {
                'hierarchy_errors': [{'error': f'Missing columns: {missing}'}],
                'is_valid': False,
                'categorical_validation': {
                    base: {'is_valid': False, 'error': f'Missing columns: {missing}', 'base_name': base}
                    for base in hierarchical_bases
                }
            }
            return error_categorical, error_hierarchical

        # Collect hierarchy combinations from valid rows (only if we have hierarchical features)
        if hierarchical_bases:
            valid_chunk = chunk[hier_cols + order_cols].dropna()
            for _, row in valid_chunk.iterrows():
                combo = tuple(row[hier_cols + order_cols].values)
                unique_combos.add(combo)

        # Process all rows in this chunk for ALL features simultaneously
        for row_idx in range(len(chunk)):
            idx_value = get_index_value(chunk, row_idx)

            # Validate ALL categorical features (both hierarchical and non-hierarchical)
            for base_name in all_bases:
                color_col = f"{base_name}_color"
                order_col = f"{base_name}_order"

                base_value = chunk[base_name].iloc[row_idx]
                color = chunk[color_col].iloc[row_idx]
                order = chunk[order_col].iloc[row_idx]

                feature_data = all_categorical_results[base_name]

                # Track NaN base values
                if pd.isna(base_value):
                    feature_data['nan_base_indices'].append(idx_value)
                    continue

                base_value_str = str(base_value)

                # Track index for this base value
                feature_data['base_value_info'][base_value_str]['indices'].append(idx_value)

                # Validate color
                if not _is_valid_hex_color(color):
                    feature_data['invalid_colors'].append({
                        'index': idx_value,
                        'base_value': base_value_str,
                        'color': str(color)
                    })

                # Validate order
                if pd.isna(order):
                    feature_data['invalid_orders'].append({
                        'index': idx_value,
                        'base_value': base_value_str,
                        'order': None,
                        'error': 'missing'
                    })
                else:
                    try:
                        int_order = int(order)
                        if int_order != float(order):
                            feature_data['invalid_orders'].append({
                                'index': idx_value,
                                'base_value': base_value_str,
                                'order': str(order),
                                'error': 'not_integer'
                            })
                        else:
                            feature_data['base_value_info'][base_value_str]['orders'].add(int_order)
                    except (ValueError, TypeError):
                        feature_data['invalid_orders'].append({
                            'index': idx_value,
                            'base_value': base_value_str,
                            'order': str(order),
                            'error': 'cannot_convert_to_int'
                        })

                # Track color/order pairs
                feature_data['base_value_info'][base_value_str]['colors'].add(str(color))
                feature_data['base_value_info'][base_value_str]['pairs'].add((str(color), str(order)))

        if pbar:
            pbar.update(len(chunk))

    if pbar:
        pbar.close()

    # Post-process: Validate consistency for each feature
    for base_name in all_bases:
        feature_data = all_categorical_results[base_name]
        non_unique_color_order = []

        for base_value, info in feature_data['base_value_info'].items():
            # Check if base value has multiple color/order pairs
            if len(info['pairs']) > 1:
                pair_details = []
                for pair in info['pairs']:
                    pair_details.append({
                        'color': pair[0],
                        'order': pair[1],
                        'indices': info['indices']
                    })
                non_unique_color_order.append({
                    'base_value': base_value,
                    'error': 'multiple_color_order_pairs',
                    'pairs_found': pair_details
                })

        # Build final result for this feature
        failures = {
            'base_name': base_name,
            'invalid_colors': feature_data['invalid_colors'],
            'invalid_orders': feature_data['invalid_orders'],
            'non_unique_color_order': non_unique_color_order
        }

        nan_base_info = {
            'base_name': base_name,
            'nan_indices': feature_data['nan_base_indices']
        }

        is_valid = all(
            len(failures[key]) == 0
            for key in ['invalid_colors', 'invalid_orders', 'non_unique_color_order']
        )

        failures['is_valid'] = is_valid
        failures['nan_base_info'] = nan_base_info

        all_categorical_results[base_name] = failures

    # Split results into categorical-only and hierarchical
    categorical_results = {
        base: all_categorical_results[base]
        for base in categorical_bases
    }

    # Build hierarchical results
    hierarchical_results = {
        'categorical_validation': {
            base: all_categorical_results[base]
            for base in hierarchical_bases
        },
        'hierarchy_errors': [],
        'hierarchy_tables': [],
        'order_preservation_errors': []
    }

    # Process hierarchy combinations (only if we have hierarchical features)
    if not hierarchical_bases:
        hierarchical_results['is_valid'] = True
    elif not unique_combos:
        hierarchical_results['hierarchy_errors'].append({'error': 'No valid hierarchical data found'})
        hierarchical_results['is_valid'] = False
    else:
        # Convert to DataFrame for processing
        unique_df = pd.DataFrame(list(unique_combos), columns=hier_cols + order_cols)

        # Detect hierarchy order by analyzing relationships
        hierarchy_order = sorted(
            hier_cols,
            key=lambda col: len(unique_df[col].unique())
        )

        # Build hierarchy tables
        hierarchy_tables = []
        leaf_col = hierarchy_order[-1]
        errors = []

        for leaf_value in unique_df[leaf_col].unique():
            leaf_rows = unique_df[unique_df[leaf_col] == leaf_value]

            # Check if this leaf has multiple parents at any level
            for parent_col in hierarchy_order[:-1]:
                parent_values = leaf_rows[parent_col].unique()
                if len(parent_values) > 1:
                    errors.append({
                        'error': 'multiple_parents',
                        'leaf_column': leaf_col,
                        'leaf_value': str(leaf_value),
                        'parent_column': parent_col,
                        'parent_values': [str(v) for v in parent_values]
                    })

            # Get the first row (they should all be the same if hierarchy is valid)
            row_data = leaf_rows.iloc[0]

            # Build hierarchy entry
            hier_entry = {'leaf_column': leaf_col, 'leaf_value': str(leaf_value)}
            for col in hierarchy_order:
                hier_entry[col] = str(row_data[col])
                order_col = f"{col}_order"
                if order_col in row_data:
                    hier_entry[order_col] = row_data[order_col]

            hierarchy_tables.append(hier_entry)

        hierarchical_results['hierarchy_errors'] = errors
        hierarchical_results['hierarchy_tables'] = hierarchy_tables
        hierarchical_results['hierarchy_order'] = hierarchy_order

        # Validate order preservation
        if hierarchy_tables and hierarchy_order:
            leaf_order_col = f"{leaf_col}_order"
            hier_df = pd.DataFrame(hierarchy_tables)

            if leaf_order_col in hier_df.columns:
                hier_df_sorted = hier_df.sort_values(leaf_order_col)

                # Check each parent level
                for parent_col in hierarchy_order[:-1]:
                    parent_order_col = f"{parent_col}_order"
                    if parent_order_col in hier_df_sorted.columns:
                        for parent_val, group in hier_df_sorted.groupby(parent_col):
                            orders = group[parent_order_col].unique()
                            if len(orders) > 1:
                                hierarchical_results['order_preservation_errors'].append({
                                    'parent_column': parent_col,
                                    'parent_value': str(parent_val),
                                    'inconsistent_orders': [int(o) for o in orders]
                                })

        # Overall validity for hierarchical
        hierarchical_results['is_valid'] = (
            len(hierarchical_results['hierarchy_errors']) == 0 and
            len(hierarchical_results['order_preservation_errors']) == 0 and
            all(v.get('is_valid', False)
                for v in hierarchical_results['categorical_validation'].values())
        )

    return categorical_results, hierarchical_results


def validate_hierarchical_features_chunked(
    data_reader,
    hierarchical_bases: List[str],
    index_col: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate hierarchical features using chunked reading.

    NOTE: This function is now a wrapper around validate_categorical_and_hierarchical_features_chunked.
    For new code, consider using the combined function directly for better performance when
    validating both categorical and hierarchical features.

    Parameters
    ----------
    data_reader : ChunkedDataReader
        Chunked data reader instance
    hierarchical_bases : list of str
        List of base names for hierarchical features
    index_col : str, optional
        Name of index column

    Returns
    -------
    dict
        Validation results including hierarchy tables
    """
    # Delegate to the combined function
    _, hierarchical_results = validate_categorical_and_hierarchical_features_chunked(
        data_reader, [], hierarchical_bases, index_col
    )
    return hierarchical_results


def validate_numerical_features_chunked(
    data_iterator,
    exclude_cols: List[str],
    index_col: Optional[str] = None,
    total_rows: Optional[int] = None,
    columns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Validate numerical features using chunked data iterator.

    Parameters
    ----------
    data_iterator : iterator
        Iterator yielding pandas DataFrames
    exclude_cols : list of str
        Columns to exclude from validation
    index_col : str, optional
        Name of index column for reporting
    total_rows : int, optional
        Total number of rows for progress bar
    columns : list of str, optional
        List of all columns (to determine numerical cols upfront)

    Returns
    -------
    dict
        Validation results
    """
    # Helper function to get index value
    def get_index_value(chunk_df, row_idx):
        if index_col and index_col in chunk_df.columns:
            return chunk_df.iloc[row_idx][index_col]
        return int(chunk_df.index[row_idx])

    results = {}
    numerical_cols = None

    pbar = tqdm(total=total_rows, desc="Validating numerical features") if total_rows else None

    for chunk in data_iterator:
        # Determine numerical columns from first chunk
        if numerical_cols is None:
            numerical_cols = [
                col for col in chunk.columns
                if col not in exclude_cols and pd.api.types.is_numeric_dtype(chunk[col])
            ]
            # Initialize results
            for col in numerical_cols:
                results[col] = []

        if not numerical_cols:
            if pbar:
                pbar.close()
            return {'is_valid': True, 'columns': {}}

        # Validate each numerical column in this chunk
        for col in numerical_cols:
            missing_mask = chunk[col].isna()
            if missing_mask.any():
                missing_indices = [
                    get_index_value(chunk, idx)
                    for idx in range(len(chunk))
                    if missing_mask.iloc[idx]
                ]
                results[col].extend(missing_indices)

        if pbar:
            pbar.update(len(chunk))

    if pbar:
        pbar.close()

    # Check if any column has missing values
    is_valid = all(len(indices) == 0 for indices in results.values())

    return {
        'is_valid': is_valid,
        'columns': {col: indices for col, indices in results.items() if len(indices) > 0}
    }


def generate_validation_report(
    results: Dict[str, Any],
    output_path: str
) -> None:
    """
    Generate a JSON validation report.

    Parameters
    ----------
    results : dict
        Validation results from all checks
    output_path : str
        Path to save JSON report
    """
    # Build summary
    summary = {
        'index_validation': results.get('index', {}).get('is_valid', True),
        'categorical_validation': True,
        'hierarchical_validation': True,
        'numerical_validation': results.get('numerical', {}).get('is_valid', True)
    }

    # Check categorical validation (non-hierarchical)
    categorical_valid = True
    if 'categorical' in results:
        categorical_valid = all(
            v.get('is_valid', False) for v in results['categorical'].values()
        )

    # Check hierarchical validation (includes categorical validation for hierarchical features)
    hierarchical_valid = True
    hierarchical_categorical_valid = True
    if 'hierarchical' in results:
        hierarchical_valid = results['hierarchical'].get('is_valid', False)
        # Also check categorical validation within hierarchical results
        if 'categorical_validation' in results['hierarchical']:
            hierarchical_categorical_valid = all(
                v.get('is_valid', False)
                for v in results['hierarchical']['categorical_validation'].values()
            )

    # Combine categorical validation from both non-hierarchical and hierarchical features
    summary['categorical_validation'] = categorical_valid and hierarchical_categorical_valid
    summary['hierarchical_validation'] = hierarchical_valid

    summary['overall_valid'] = all(summary.values())

    report = {
        'summary': summary,
        'details': _convert_to_json_serializable(results)
    }

    # Write report
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
