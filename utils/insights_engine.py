"""
insights_engine.py
Rule-based insights generator using pandas statistics.
No AI/LLM yet.
"""

import pandas as pd
from datetime import datetime


def generate_basic_insights(df):
    insights = []

    rows, cols = df.shape

    # -------------------------
    # Dataset size
    # -------------------------
    insights.append(f"Dataset contains {rows:,} rows and {cols} columns.")

    # -------------------------
    # Missing values
    # -------------------------
    missing = df.isnull().sum().sum()
    total_cells = rows * cols
    completeness = (1 - missing / total_cells) * 100

    insights.append(
        f"Data completeness is {completeness:.2f}% with {missing} missing values."
    )

    # -------------------------
    # Numeric summary
    # -------------------------
    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        means = numeric_df.mean()

        top_mean_col = means.idxmax()
        insights.append(
            f"'{top_mean_col}' has the highest average value ({means[top_mean_col]:.2f})."
        )

    # -------------------------
    # Correlation
    # -------------------------
    if numeric_df.shape[1] >= 2:
        corr = numeric_df.corr(numeric_only=True).abs()

        corr.values[[range(len(corr))]*2] = 0  # remove diagonal

        max_corr = corr.max().max()

        if max_corr > 0:
            pair = corr.stack().idxmax()
            insights.append(
                f"Strongest correlation found between '{pair[0]}' and '{pair[1]}' (r = {max_corr:.2f})."
            )

    # -------------------------
    # Outlier detection (IQR)
    # -------------------------
    for col in numeric_df.columns:
        q1 = numeric_df[col].quantile(0.25)
        q3 = numeric_df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = ((numeric_df[col] < lower) | (numeric_df[col] > upper)).sum()

        if outliers > 0:
            insights.append(
                f"Detected {outliers} potential outliers in '{col}'."
            )

    # -------------------------
    # Convert to HTML
    # -------------------------
    html = "<ul>"
    for item in insights:
        html += f"<li>{item}</li>"
    html += "</ul>"

    return html, datetime.now().strftime("%B %d, %Y")
