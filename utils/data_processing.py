"""
data_processing.py
Handles loading CSV/Excel files and computing dataset statistics.
"""

import os
import pandas as pd


def load_file(file_path):
    """
    Load a CSV or Excel file into a pandas DataFrame.

    Args:
        file_path (str): Absolute or relative path to the file.

    Returns:
        pd.DataFrame | None: Loaded DataFrame, or None on error.
    """
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in ('.xlsx', '.xls'):
            return pd.read_excel(file_path, engine='openpyxl')
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading file '{file_path}': {e}")
        return None


# Keep backward-compatible alias
load_csv = load_file


def _format_size(size_bytes):
    """Return a human-readable file size string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / 1024 / 1024:.2f} MB"


def get_dataset_stats(df, file_path):
    """
    Generate summary statistics for the dataset.

    Args:
        df (pd.DataFrame): The loaded dataset.
        file_path (str): Path to the uploaded file (used for size).

    Returns:
        dict: Stats including rows, columns, missing values,
              dataset_size, and table_data (HTML preview).
    """
    missing = int(df.isnull().sum().sum())
    size_bytes = os.path.getsize(file_path)

    # HTML preview of first 10 rows
    table_data = df.head(10).to_html(
        classes="table table-striped table-bordered table-hover",
        index=False,
        border=0
    )

    return {
        'rows': df.shape[0],
        'columns': df.shape[1],
        'missing_values': missing,
        'dataset_size': _format_size(size_bytes),
        'table_data': table_data,
    }
