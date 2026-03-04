import pandas as pd
import os

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def get_dataset_stats(df, file_path):
    """
    Generate summary statistics for the dataset.
    
    Args:
        df (pd.DataFrame): The dataset.
        file_path (str): Path to the CSV file (for file size).
        
    Returns:
        dict: Summary stats including rows, columns, missing values,
              dataset size, and HTML table preview.
    """
    stats = {
        'rows': df.shape[0],
        'columns': df.shape[1],
        'missing_values': df.isnull().sum().sum(),
        'dataset_size': f"{os.path.getsize(file_path)/1024/1024:.2f} MB",  # file size in MB
        'head_html': df.head().to_html(classes="table table-striped table-bordered", index=False),
        'summary_html': df.describe(include='all').to_html(classes="table table-bordered table-sm")  # optional
    }
    return stats
