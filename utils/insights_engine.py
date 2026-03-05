"""
insights_engine.py
Rule-based, statistics-driven insights generator.
Returns an HTML string and the current date string.
"""

import numpy as np
import pandas as pd
from datetime import datetime


def generate_basic_insights(df):
    """
    Analyse a DataFrame and return a structured HTML insights report.

    Returns:
        tuple[str, str]: (insights_html, formatted_date)
    """
    insights = []
    rows, cols = df.shape

    # --- Dataset shape ---
    insights.append(("Dataset Size", f"Contains <strong>{rows:,} rows</strong> and <strong>{cols} columns</strong>."))

    # --- Missing values ---
    missing = int(df.isnull().sum().sum())
    total_cells = rows * cols
    completeness = (1 - missing / max(total_cells, 1)) * 100
    insights.append((
        "Data Completeness",
        f"Data is <strong>{completeness:.1f}% complete</strong> — {missing:,} missing value(s) detected."
    ))

    # --- Column type breakdown ---
    num_numeric = len(df.select_dtypes(include='number').columns)
    num_categorical = len(df.select_dtypes(include=['object', 'category']).columns)
    num_datetime = len(df.select_dtypes(include='datetime').columns)
    insights.append((
        "Column Types",
        f"<strong>{num_numeric}</strong> numeric, "
        f"<strong>{num_categorical}</strong> categorical, "
        f"<strong>{num_datetime}</strong> datetime column(s)."
    ))

    # --- Numeric summary ---
    numeric_df = df.select_dtypes(include='number')

    if not numeric_df.empty:
        means = numeric_df.mean()
        top_mean_col = means.idxmax()
        insights.append((
            "Highest Average",
            f"Column <strong>'{top_mean_col}'</strong> has the highest average value "
            f"(<strong>{means[top_mean_col]:,.2f}</strong>)."
        ))

        # --- Variance / spread ---
        stds = numeric_df.std()
        top_std_col = stds.idxmax()
        insights.append((
            "Most Variable Column",
            f"<strong>'{top_std_col}'</strong> shows the most spread "
            f"(std dev = <strong>{stds[top_std_col]:,.2f}</strong>)."
        ))

    # --- Correlation ---
    if numeric_df.shape[1] >= 2:
        corr = numeric_df.corr(numeric_only=True).abs()
        np.fill_diagonal(corr.values, 0)   # remove self-correlation
        max_corr = corr.max().max()
        if max_corr > 0:
            pair = corr.stack().idxmax()
            insights.append((
                "Strongest Correlation",
                f"Highest correlation found between <strong>'{pair[0]}'</strong> and "
                f"<strong>'{pair[1]}'</strong> "
                f"(r&nbsp;=&nbsp;<strong>{max_corr:.2f}</strong>)."
            ))

    # --- Outliers (IQR) — cap at top 3 columns ---
    outlier_findings = []
    for col in list(numeric_df.columns)[:10]:          # examine up to 10 cols
        q1 = numeric_df[col].quantile(0.25)
        q3 = numeric_df[col].quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_outliers = int(((numeric_df[col] < lower) | (numeric_df[col] > upper)).sum())
        if n_outliers > 0:
            pct = n_outliers / rows * 100
            outlier_findings.append((n_outliers, col, pct))

    # Report top 3 outlier-heavy columns only
    outlier_findings.sort(reverse=True)
    for n_out, col, pct in outlier_findings[:3]:
        insights.append((
            f"Outliers in '{col}'",
            f"Detected <strong>{n_out} potential outlier(s)</strong> "
            f"(<strong>{pct:.1f}%</strong> of rows) via IQR method."
        ))

    # --- Missing-per-column (top 3 worst) ---
    col_missing = df.isnull().sum()
    col_missing = col_missing[col_missing > 0].sort_values(ascending=False)
    for col, n in col_missing.head(3).items():
        pct = n / rows * 100
        insights.append((
            f"Missing Data: '{col}'",
            f"<strong>{n:,} missing value(s)</strong> ({pct:.1f}%) in column <strong>'{col}'</strong>."
        ))

    # --- Build HTML ---
    html = '<div class="insights-list">'
    for title, body in insights:
        html += (
            f'<div class="insight-item">'
            f'<span class="insight-title">{title}</span>'
            f'<p class="insight-body">{body}</p>'
            f'</div>'
        )
    html += '</div>'

    return html, datetime.now().strftime("%B %d, %Y")
