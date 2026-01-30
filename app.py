"""
AI Data Analyst Dashboard - Sample Flask Application
This file demonstrates how to integrate the frontend templates with Flask.
"""

from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """
    Upload page - Landing page for file uploads
    """
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Handle file upload and redirect to dashboard
    In production, this would process the file and store results
    """
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    # In production, you would:
    # 1. Validate file type (CSV, Excel)
    # 2. Save the file securely
    # 3. Process the data (pandas, analysis)
    # 4. Store results in session or database
    # 5. Generate charts
    
    # For demo purposes, redirect to dashboard with sample data
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """
    Dashboard page - Display dataset overview and statistics
    """
    # Sample data - replace with actual analysis results
    data = {
        'rows': 1250,
        'columns': 18,
        'missing_values': 42,
        'dataset_size': '2.5 MB',
        
        # Sample HTML table (in production, generate from pandas DataFrame)
        'table_data': '''
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>City</th>
                        <th>Salary</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td>John Doe</td>
                        <td>28</td>
                        <td>New York</td>
                        <td>$75,000</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>Jane Smith</td>
                        <td>34</td>
                        <td>San Francisco</td>
                        <td>$95,000</td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>Bob Johnson</td>
                        <td>45</td>
                        <td>Chicago</td>
                        <td>$82,000</td>
                    </tr>
                    <tr>
                        <td>4</td>
                        <td>Alice Williams</td>
                        <td>29</td>
                        <td>Boston</td>
                        <td>$88,000</td>
                    </tr>
                    <tr>
                        <td>5</td>
                        <td>Charlie Brown</td>
                        <td>52</td>
                        <td>Seattle</td>
                        <td>$105,000</td>
                    </tr>
                </tbody>
            </table>
        ''',
        
        # Sample chart paths (in production, generate actual charts)
        'chart_paths': [
            'https://via.placeholder.com/600x400/3b82f6/ffffff?text=Distribution+Chart',
            'https://via.placeholder.com/600x400/10b981/ffffff?text=Correlation+Heatmap',
            'https://via.placeholder.com/600x400/f59e0b/ffffff?text=Time+Series+Analysis',
            'https://via.placeholder.com/600x400/6366f1/ffffff?text=Category+Breakdown'
        ]
    }
    
    return render_template('dashboard.html', **data)

@app.route('/insights')
def insights():
    """
    Insights page - Display AI-generated insights
    """
    # Sample insights - replace with actual AI-generated content
    insights_data = {
        'insights_text': '''
            <h3>Executive Summary</h3>
            <p>Based on comprehensive analysis of your dataset containing 1,250 rows and 18 columns, 
            several key patterns and insights have been identified that warrant immediate attention.</p>
            
            <h4>1. Data Quality Assessment</h4>
            <p>The dataset shows <strong>96.6% completeness</strong> with only 42 missing values spread 
            across 3 columns. The missing data pattern appears to be random (MCAR), suggesting that 
            simple imputation methods would be appropriate.</p>
            
            <ul>
                <li><strong>Age column:</strong> 15 missing values (1.2%)</li>
                <li><strong>Salary column:</strong> 18 missing values (1.4%)</li>
                <li><strong>City column:</strong> 9 missing values (0.7%)</li>
            </ul>
            
            <h4>2. Distribution Insights</h4>
            <p>The data exhibits interesting distribution patterns:</p>
            <ul>
                <li>Age distribution follows a normal curve with mean of 37.5 years</li>
                <li>Salary shows right-skewed distribution with median $82,000</li>
                <li>Geographic distribution concentrated in 5 major cities</li>
            </ul>
            
            <h4>3. Key Correlations Discovered</h4>
            <p>Correlation analysis reveals several significant relationships:</p>
            <ul>
                <li><strong>Age vs. Salary:</strong> Strong positive correlation (r = 0.72)</li>
                <li><strong>Experience vs. Salary:</strong> Very strong correlation (r = 0.85)</li>
                <li><strong>City vs. Salary:</strong> Moderate correlation showing geographic pay differences</li>
            </ul>
            
            <h4>4. Anomaly Detection</h4>
            <p>Statistical analysis identified 23 potential outliers (1.8% of data) that may require 
            further investigation:</p>
            <ul>
                <li>12 cases with unusually high salary for given experience level</li>
                <li>8 cases with age-experience mismatches</li>
                <li>3 cases with extreme salary values requiring validation</li>
            </ul>
            
            <h4>5. Recommendations</h4>
            <p>Based on this analysis, we recommend the following actions:</p>
            <ol>
                <li><strong>Data Cleaning:</strong> Address the 42 missing values using median imputation for numerical fields</li>
                <li><strong>Outlier Review:</strong> Manually verify the 23 flagged outliers before including in final analysis</li>
                <li><strong>Feature Engineering:</strong> Consider creating derived features like "salary per year of experience"</li>
                <li><strong>Segmentation:</strong> Perform cluster analysis to identify distinct employee segments</li>
                <li><strong>Predictive Modeling:</strong> The strong correlations suggest good potential for salary prediction models</li>
            </ol>
            
            <h4>6. Business Impact</h4>
            <p>These insights can drive several business decisions:</p>
            <ul>
                <li>Salary benchmarking and compensation strategy</li>
                <li>Talent acquisition planning by geography</li>
                <li>Career progression pathway definition</li>
                <li>Budget forecasting for compensation expenses</li>
            </ul>
            
            <h4>Next Steps</h4>
            <p>To maximize value from this analysis:</p>
            <ol>
                <li>Schedule a review meeting with stakeholders to discuss findings</li>
                <li>Prioritize addressing data quality issues</li>
                <li>Define specific business questions for deeper analysis</li>
                <li>Consider collecting additional data points for enhanced insights</li>
            </ol>
        ''',
        'current_date': 'January 29, 2026'
    }
    
    return render_template('insights.html', **insights_data)

@app.route('/report')
def report():
    """
    Report page - Placeholder for report generation
    For now, redirects to insights
    """
    return redirect(url_for('insights'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
