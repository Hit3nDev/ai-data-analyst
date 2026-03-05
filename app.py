"""
AI Data Analyst Dashboard
Flask + Pandas + Matplotlib
Session-safe, secure file handling, proper routing.
"""

import os
import uuid
import glob
import secrets

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.utils import secure_filename

from utils.data_processing import load_file, get_dataset_stats
from utils.charts import (
    save_distribution_chart,
    save_correlation_heatmap,
    save_boxplot
)
from utils.insights_engine import generate_basic_insights

# -------------------------------------------------
# App Config
# -------------------------------------------------

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['IMAGE_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def allowed_file(filename):
    """Check that the file has an allowed extension."""
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def cleanup_images(folder):
    """Remove all PNG files from the images folder between uploads."""
    for f in glob.glob(os.path.join(folder, '*.png')):
        try:
            os.remove(f)
        except OSError:
            pass


# -------------------------------------------------
# Routes
# -------------------------------------------------

@app.route('/')
def index():
    """Landing / upload page."""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Redirect /dashboard to the upload page if no file is loaded."""
    upload_path = session.get('upload_path')
    if not upload_path or not os.path.exists(upload_path):
        flash('Please upload a dataset first.', 'warning')
        return redirect(url_for('index'))
    # Re-render the dashboard from session state
    return redirect(url_for('index'))


# -------------------------------------------------
# CSV / Excel Upload + Analysis
# -------------------------------------------------

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle file upload and render the analysis dashboard."""

    if 'file' not in request.files:
        flash('No file part in the request.', 'danger')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Unsupported file type. Please upload a CSV or Excel file.', 'danger')
        return redirect(url_for('index'))

    # Save file securely
    safe_name = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    file.save(file_path)

    # Store path in session (NOT a global variable)
    session['upload_path'] = file_path

    # Load DataFrame
    df = load_file(file_path)
    if df is None:
        flash('Could not read the file. Please ensure it is a valid CSV or Excel file.', 'danger')
        return redirect(url_for('index'))

    # Dataset stats
    stats = get_dataset_stats(df, file_path)

    # Clean up old chart images before generating new ones
    cleanup_images(app.config['IMAGE_FOLDER'])

    # Generate charts
    chart_paths = []
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    try:
        # 1. Distribution histogram
        if len(numeric_cols) > 0:
            path = os.path.join(
                app.config['IMAGE_FOLDER'],
                f"dist_{uuid.uuid4().hex}.png"
            )
            saved = save_distribution_chart(df, numeric_cols[0], path)
            if saved:
                chart_paths.append('/' + saved.replace('\\', '/'))

        # 2. Correlation heatmap
        if len(numeric_cols) > 1:
            path = os.path.join(
                app.config['IMAGE_FOLDER'],
                f"corr_{uuid.uuid4().hex}.png"
            )
            saved = save_correlation_heatmap(df, path)
            if saved:
                chart_paths.append('/' + saved.replace('\\', '/'))

        # 3. Boxplot
        if len(numeric_cols) > 0:
            path = os.path.join(
                app.config['IMAGE_FOLDER'],
                f"box_{uuid.uuid4().hex}.png"
            )
            saved = save_boxplot(df, numeric_cols[0], path)
            if saved:
                chart_paths.append('/' + saved.replace('\\', '/'))

    except Exception as e:
        print("Chart generation failed:", e)

    return render_template(
        'dashboard.html',
        chart_paths=chart_paths,
        **stats
    )


# -------------------------------------------------
# Insights
# -------------------------------------------------

@app.route('/insights')
def insights():
    """AI-powered insights page — requires a previously uploaded dataset."""
    upload_path = session.get('upload_path')

    if not upload_path or not os.path.exists(upload_path):
        flash('Please upload a dataset first.', 'warning')
        return redirect(url_for('index'))

    from utils.data_processing import load_file
    df = load_file(upload_path)

    if df is None:
        flash('Could not reload dataset. Please re-upload.', 'danger')
        return redirect(url_for('index'))

    insights_html, current_date = generate_basic_insights(df)

    return render_template(
        'insights.html',
        insights_text=insights_html,
        current_date=current_date
    )


# -------------------------------------------------
# Report placeholder (redirects to insights)
# -------------------------------------------------

@app.route('/report')
def report():
    return redirect(url_for('insights'))


# -------------------------------------------------
# Error handlers
# -------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', code=404, message="Page not found."), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', code=500, message="Internal server error."), 500


@app.errorhandler(413)
def too_large(error):
    flash('File too large. Maximum allowed size is 50 MB.', 'danger')
    return redirect(url_for('index'))


# -------------------------------------------------
# Run
# -------------------------------------------------

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)
