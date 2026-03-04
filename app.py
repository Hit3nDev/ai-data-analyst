"""
AI Data Analyst Dashboard - Production Version
Flask + Pandas + Matplotlib
Real CSV upload → real stats → real charts
Resume-quality clean architecture
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from utils.insights_engine import generate_basic_insights

# utils
from utils.data_processing import load_csv, get_dataset_stats
from utils.charts import (
    save_distribution_chart,
    save_correlation_heatmap,
    save_boxplot
)

# -------------------------------------------------
# App Config
# -------------------------------------------------

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['IMAGE_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

latest_df = None


# -------------------------------------------------
# Routes
# -------------------------------------------------

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


# -------------------------------------------------
# CSV Upload + Analysis
# -------------------------------------------------

@app.route('/analyze', methods=['POST'])
def analyze():

    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    # -----------------------------
    # Save file securely
    # -----------------------------
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    file.save(file_path)

    # -----------------------------
    # Load DataFrame
    # -----------------------------
    df = load_csv(file_path)
    global latest_df
    latest_df = df

    if df is None:
        return "Invalid CSV file", 400

    # -----------------------------
    # Dataset stats
    # -----------------------------
    stats = get_dataset_stats(df, file_path)

    # -----------------------------
    # Generate charts
    # -----------------------------
    chart_paths = []

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    try:

        # 1️⃣ Distribution
        if len(numeric_cols) > 0:
            path = os.path.join(
                app.config['IMAGE_FOLDER'],
                f"dist_{uuid.uuid4().hex}.png"
            )

            saved = save_distribution_chart(df, numeric_cols[0], path)

            if saved:
                chart_paths.append('/' + saved)

        # 2️⃣ Correlation heatmap
        if len(numeric_cols) > 1:
            path = os.path.join(
                app.config['IMAGE_FOLDER'],
                f"corr_{uuid.uuid4().hex}.png"
            )

            saved = save_correlation_heatmap(df, path)

            if saved:
                chart_paths.append('/' + saved)

        # 3️⃣ Boxplot (NEW – looks professional on dashboard)
        if len(numeric_cols) > 0:
            path = os.path.join(
                app.config['IMAGE_FOLDER'],
                f"box_{uuid.uuid4().hex}.png"
            )

            saved = save_boxplot(df, numeric_cols[0], path)

            if saved:
                chart_paths.append('/' + saved)

    except Exception as e:
        print("Chart generation failed:", e)

    # -----------------------------
    # Render dashboard
    # -----------------------------
    return render_template(
        'dashboard.html',
        chart_paths=chart_paths,
        **stats
    )


# -------------------------------------------------
# Insights (AI coming next)
# -------------------------------------------------

@app.route('/insights')
def insights():

    global latest_df

    if latest_df is None:
        return redirect(url_for('index'))

    insights_html, current_date = generate_basic_insights(latest_df)

    return render_template(
        'insights.html',
        insights_text=insights_html,
        current_date=current_date
    )



# -------------------------------------------------
# Report placeholder
# -------------------------------------------------

@app.route('/report')
def report():
    return redirect(url_for('insights'))


# -------------------------------------------------
# Error handlers
# -------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500


# -------------------------------------------------
# Run
# -------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
