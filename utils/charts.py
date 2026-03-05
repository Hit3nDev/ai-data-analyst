"""
charts.py
All matplotlib chart generation for the dashboard.
Saves images to static/images/ and returns the saved path.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')   # non-interactive backend — required for Flask
import matplotlib.pyplot as plt
import pandas as pd

# Apply a clean style to all charts
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor':   '#f9fafb',
    'axes.edgecolor':   '#e5e7eb',
    'axes.grid':        True,
    'grid.color':       '#e5e7eb',
    'grid.linewidth':   0.8,
    'font.family':      'sans-serif',
    'font.size':        11,
    'axes.titlesize':   13,
    'axes.titleweight': 'bold',
})


# -------------------------------------------------
# Distribution / Histogram
# -------------------------------------------------

def save_distribution_chart(df, column, save_path):
    """Save a styled histogram for a numeric column."""
    if column not in df.columns:
        return None

    series = df[column].dropna()

    if not pd.api.types.is_numeric_dtype(series):
        return None

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(series, bins=30, color='#2563eb', edgecolor='white', linewidth=0.5, alpha=0.85)
    ax.set_xlabel(column, labelpad=8)
    ax.set_ylabel("Frequency", labelpad=8)
    ax.set_title(f"Distribution of {column}")
    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.close(fig)
    return save_path


# -------------------------------------------------
# Correlation Heatmap
# -------------------------------------------------

def save_correlation_heatmap(df, save_path):
    """Save an annotated correlation heatmap with diverging colormap."""
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(max(6, len(corr.columns)), max(5, len(corr.columns) - 1)))
    im = ax.imshow(corr.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(corr.columns, fontsize=9)
    ax.set_title("Correlation Heatmap")

    # Annotate each cell with its value
    for i in range(len(corr)):
        for j in range(len(corr.columns)):
            val = corr.values[i, j]
            text_color = 'white' if abs(val) > 0.6 else 'black'
            ax.text(j, i, f"{val:.2f}", ha='center', va='center',
                    fontsize=8, color=text_color)

    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.close(fig)
    return save_path


# -------------------------------------------------
# Boxplot
# -------------------------------------------------

def save_boxplot(df, column, save_path):
    """Save a styled boxplot for outlier detection."""
    if column not in df.columns:
        return None

    series = df[column].dropna()

    if not pd.api.types.is_numeric_dtype(series):
        return None

    fig, ax = plt.subplots(figsize=(5, 5))
    bp = ax.boxplot(
        series,
        vert=True,
        patch_artist=True,
        widths=0.5,
        boxprops=dict(facecolor='#dbeafe', color='#2563eb', linewidth=1.5),
        medianprops=dict(color='#dc2626', linewidth=2),
        whiskerprops=dict(color='#6b7280', linewidth=1.2),
        capprops=dict(color='#6b7280', linewidth=1.2),
        flierprops=dict(marker='o', color='#dc2626', alpha=0.5, markersize=4),
    )
    ax.set_title(f"Boxplot of {column}")
    ax.set_ylabel(column)
    ax.set_xticks([])
    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.close(fig)
    return save_path
