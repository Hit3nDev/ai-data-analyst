"""
report_generator.py
Placeholder for PDF/Markdown report generation.
"""


def generate_report(df, insights_html, output_path):
    """
    Export a PDF or Markdown report combining dataset stats and insights.

    Future implementation using fpdf2:
        pip install fpdf2
        from fpdf import FPDF
        ...

    Args:
        df (pd.DataFrame): The dataset.
        insights_html (str): Rendered insights HTML.
        output_path (str): Where to save the report file.

    Returns:
        str | None: Path to the generated report, or None on failure.
    """
    # TODO: Implement PDF export with fpdf2 or weasyprint
    return None
