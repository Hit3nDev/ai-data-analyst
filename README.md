# 📊 AI Data Analyst Dashboard

Upload a CSV or Excel file and get an instant analysis: dataset health, distributions, correlations, outliers and a written insights report — no code, no notebook.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3-000000?logo=flask&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-charts-11557c)

## What it does

| Step | Output |
|------|--------|
| **Upload** | CSV / XLSX / XLS up to 50 MB, validated and stored with a safe, unique filename |
| **Profile** | Rows, columns, size, data types, missing values, duplicates |
| **Visualise** | Distribution histograms, box plots for outliers, correlation heatmap |
| **Insights** | Rule‑based, statistics‑driven findings: skew, strong correlations, high‑missing columns, outliers |
| **Report** | Insights page summarising the full analysis (PDF export on the roadmap) |

## Engineering notes

- Session‑scoped uploads and generated charts, cleaned up automatically
- `secure_filename` + extension allow‑list + size limit for safe uploads
- Secret key from environment, never hard‑coded
- Custom 404 / 500 error pages and a friendly message for files over the size limit
- `utils/ai_insights.py` is a ready hook for plugging in an LLM summary

## Run it

```bash
git clone https://github.com/Hit3nDev/ai-data-analyst.git
cd ai-data-analyst
pip install -r requirements.txt
python app.py            # http://localhost:5000
```

## Structure

```
app.py                   Flask routes: upload → dashboard → insights → report
utils/
├── data_processing.py   load file, dataset stats
├── charts.py            distribution, box plot, correlation heatmap
├── insights_engine.py   statistical insight rules
├── report_generator.py  PDF export (planned)
└── ai_insights.py       optional LLM hook
templates/  static/      Jinja2 pages, CSS, JS
```

---

Built by [Hiten Mandhyan](https://github.com/Hit3nDev)
