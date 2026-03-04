"""
charts.py
Handles all matplotlib chart generation for the dashboard.
Saves images into static/images and returns paths.
"""

import matplotlib.pyplot as plt
import pandas as pd


# -------------------------------------------------
# Distribution / Histogram
# -------------------------------------------------

def save_distribution_chart(df, column, save_path):
    """
    Save histogram distribution for a numeric column.
    """

    if column not in df.columns:
        return None

    series = df[column].dropna()

    if not pd.api.types.is_numeric_dtype(series):
        return None

    plt.figure(figsize=(6, 4))

    plt.hist(series, bins=30)
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.title(f"Distribution of {column}")

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path


# -------------------------------------------------
# Correlation Heatmap
# -------------------------------------------------

def save_correlation_heatmap(df, save_path):
    """
    Save correlation heatmap for numeric columns only.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr(numeric_only=True)

    plt.figure(figsize=(8, 6))

    plt.imshow(corr)
    plt.colorbar()

    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)

    plt.title("Correlation Heatmap")

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path


# -------------------------------------------------
# (Optional) Boxplot — great for dashboards
# -------------------------------------------------

def save_boxplot(df, column, save_path):
    """
    Boxplot for outlier detection.
    """

    if column not in df.columns:
        return None

    series = df[column].dropna()

    if not pd.api.types.is_numeric_dtype(series):
        return None

    plt.figure(figsize=(4, 5))

    plt.boxplot(series, vert=True)
    plt.title(f"Boxplot of {column}")

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path
