# forecast_alerting

## 📌 Overview
This project implements a reproducible **forecasting + anomaly detection pipeline** on daily multi-site operations data.  
It forecasts **14 days of units produced and power consumption (kWh)**, detects downtime anomalies, and exposes results via a **CLI + FastAPI API**.

---

## ⚙️ Environment
- Python 3.10+
- Allowed libraries only:
  - `pandas`, `numpy`, `scikit-learn`, `statsmodels`
  - `prophet` (baseline model)
  - `xgboost` (improved model)
  - `fastapi`, `typer`, `pydantic`

No paid/external APIs used. Fully reproducible with fixed seeds.

---

## 📂 Project Structure
forecast_alert_pipeline/
│
├── data/
│ └── ops_data.csv # Input dataset
├── outputs/
│ ├── forecast.csv # 14-day forecasts (baseline + improved)
│ ├── alerts.csv # Detected anomalies
│ └── run_info.json # Seeds + versions
├── src/
│ ├── preprocessing.py # Cleaning + feature engineering
│ ├── forecast_prophet.py # Prophet baseline model
│ ├── forecast_xgb.py # XGBoost improved model
│ ├── anomaly.py # Anomaly detection rules
│ └── api.py # FastAPI app
├── cli.py # Typer CLI entrypoint
├── requirements.txt
└── exec_brief.md # 1-page executive brief

---

## 🚀 Setup & Run

### 1. Create Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

### 📊 Outputs

forecast.csv → site, date, baseline forecast, improved forecast, MAE, MAPE

alerts.csv → site, date, metric, value, anomaly_type, score
