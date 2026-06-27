# ⚙️ Mining Process Quality Monitoring Platform

> **Real-time flotation plant analytics, quality prediction, and process intelligence — powered by XGBoost and Streamlit.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Machine Learning Models](#machine-learning-models)
- [Dataset](#dataset)
- [Pages & Modules](#pages--modules)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Mining Process Quality Monitoring Platform** is an industrial-grade web application designed for real-time monitoring, prediction, and analytics of a flotation plant's mineral separation process.

Flotation plants process raw ore to separate iron from silica. Maintaining low silica concentrate levels in the final product is critical to ore quality. This platform provides:

- **Live KPI dashboards** with instant visibility into plant health
- **ML-powered predictions** of silica and iron concentrate levels
- **1-hour-ahead forecasting** to enable proactive process control
- **Historical analytics** for trend identification and root-cause analysis
- **Automated alarm management** with threshold-based alerting
- **Exportable reports** in CSV and HTML formats

---

## Features

| Feature | Description |
|---|---|
| 🏠 **Dashboard** | Real-time KPIs, silica/iron trend charts, heatmaps, and air flow distribution |
| 🔮 **Live Prediction** | Predict silica or iron concentrate from manually entered process parameters |
| 📡 **Future Prediction** | 1-hour-ahead silica forecast with residual error analysis and operational recommendations |
| 📊 **Historical Analytics** | Filterable trends, distributions, correlation matrices, scatter analysis, and outlier detection |
| 🏭 **Process Monitoring** | Control-room style parameter status table, column air flow gauges, and alarm panel |
| 🔬 **Feature Analysis** | Feature importance rankings, variable relationship explorer, and statistical distributions |
| 🤖 **Model Performance** | Model architecture details, importance comparison across models, Sankey inference pipeline |
| 📄 **Reports** | One-click CSV and styled HTML report generation |

---

## Tech Stack

| Technology | Role |
|---|---|
| **Python 3.x** | Core language |
| **Streamlit** | Interactive web application framework |
| **XGBoost** | Gradient boosted tree regression models |
| **Pandas / NumPy** | Data wrangling and numerical computation |
| **Plotly** | Interactive charts, gauges, Sankey diagrams, heatmaps |
| **Scikit-learn** | ML utilities and preprocessing |
| **Joblib** | Model serialisation and caching |

---

## Project Structure

```
project-root/
│
├── app/
│   └── app.py                  # Main Streamlit application
│
├── data/
│   ├── raw/
│   │   └── MiningProcess_Flotation_Plant_Database.csv
│   └── processed/
│       └── mining_hourly_processed.csv
│
├── models/
│   ├── model_with_iron.pkl      # Silica prediction (with iron feature)
│   ├── model_without_iron.pkl   # Silica prediction (without iron feature)
│   └── model_1h_ahead.pkl       # 1-hour ahead silica forecast
│
├── assets/
│   └── feature_importance.csv   # Pre-computed feature importances
│
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/your-username/mining-process-qm.git
cd mining-process-qm
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Verify your data and models are in place**

Ensure the following files exist before launching:

```
data/raw/MiningProcess_Flotation_Plant_Database.csv
data/processed/mining_hourly_processed.csv
models/model_with_iron.pkl
models/model_without_iron.pkl
models/model_1h_ahead.pkl
assets/feature_importance.csv
```

---

## Usage

Run the Streamlit application from the project root:

```bash
streamlit run app/app.py
```

The app will open in your browser at `http://localhost:8501`.

Navigate between pages using the sidebar. All data loading is cached automatically for performance.

---

## Machine Learning Models

Three XGBoost Regressor models are included, each serving a distinct operational purpose:

### `model_with_iron` — Silica Concentrate Predictor
Predicts the percentage of silica in the concentrate using all available process features, **including** the iron concentrate measurement. Use this when all sensor readings are available for the highest accuracy prediction.

### `model_without_iron` — Silica Concentrate Predictor (Iron-free)
Predicts silica concentrate **without** relying on an iron concentrate reading. Suitable for scenarios where the iron measurement is delayed or unavailable, enabling earlier quality estimates in the process pipeline.

### `model_1h_ahead` — One-Hour Ahead Forecast
A temporally-aware model that forecasts silica concentrate **one hour into the future** using lag and rolling window features. Enables proactive intervention before quality deviations occur.

### Feature Engineering

The processed dataset includes engineered temporal features to support the forecasting model:

| Feature Type | Examples |
|---|---|
| Lag features | `silica_lag_1`, `silica_lag_2`, `silica_lag_4`, `silica_lag_24` |
| Rolling statistics | `silica_roll_mean_3`, `silica_roll_mean_6`, `silica_roll_mean_24` |
| Time features | `hour`, `day`, `month`, `day_of_week` |

### Risk Thresholds

Silica concentrate predictions are classified into three risk levels:

| Level | Range | Colour |
|---|---|---|
| 🟢 LOW | < 1.5% | Green |
| 🟡 MEDIUM | 1.5% – 2.5% | Amber |
| 🔴 HIGH | > 2.5% | Red |

---

## Dataset

**Source:** MiningProcess Flotation Plant Database

The raw dataset contains over **737,000 sensor readings** from a real industrial flotation plant, captured at 20-second intervals and aggregated to **hourly resolution** for modelling.

### Key Variables

| Variable | Description |
|---|---|
| `% Iron Feed` | Iron percentage in the raw ore input |
| `% Silica Feed` | Silica percentage in the raw ore input |
| `Starch Flow` | Starch reagent flow rate (m³/h) — depressant |
| `Amina Flow` | Amine reagent flow rate (m³/h) — collector |
| `Ore Pulp Flow` | Ore pulp volumetric flow (t/h) |
| `Ore Pulp pH` | Pulp acidity/alkalinity |
| `Ore Pulp Density` | Pulp density (g/cm³) |
| `Flotation Column XX Air Flow` | Air flow per flotation column (7 columns) |
| `Flotation Column XX Level` | Froth level per flotation column (7 columns) |
| `% Iron Concentrate` | **Target** — Iron grade of final concentrate |
| `% Silica Concentrate` | **Target** — Silica contamination in final concentrate |

---

## Pages & Modules

### 🏠 Dashboard
The main overview screen. Displays eight live KPI cards (iron feed, silica output, iron recovery, process stability, starch flow, pH, ore flow, plant status), 72-hour trend charts, a silica gauge, an air flow donut chart, and a silica heatmap by hour-of-day and day-of-week.

### 🔮 Live Prediction
A configurable input form pre-filled from the latest sensor readings. Supports prediction of either silica or iron concentrate. Outputs a gauge chart, top feature influences bar chart, and a quality alert banner.

### 📡 Future Prediction
Applies the 1-hour ahead model to recent data to produce a scrollable forecast window (12–96 hours). Displays actual vs. predicted overlay, forecast error area chart, and context-aware operational recommendations.

### 📊 Historical Analytics
Full dataset explorer with date range and silica concentration filters. Five tabs: Trends, Distributions, Correlation matrix, Scatter analysis with OLS trendline, and IQR-based Outlier detection. Includes CSV download.

### 🏭 Process Monitoring
Control-room style view. Parameter status table with colour-coded rows, per-column air flow metrics, and a live alarm panel that highlights out-of-range parameters.

### 🔬 Feature Analysis
Feature importance bar chart and treemap, interactive scatter plot with marginal histograms, correlation-with-target bar chart, and per-feature histogram, box plot, and descriptive statistics.

### 🤖 Model Performance
Model architecture cards for all three models, side-by-side feature importance comparison, and a Sankey diagram illustrating the full inference pipeline from raw data to alert system.

### 📄 Reports
One-click export of a KPI summary (CSV), last 48 hours of hourly data (CSV), and a fully self-contained styled HTML report with recommendations.

---

## Configuration

Key thresholds and parameters are defined in `app.py` and can be adjusted without retraining:

```python
# Silica risk classification (page_live_prediction, page_future_prediction)
def silica_risk_level(val):
    if val < 1.5:   return ("LOW",    ...)
    elif val < 2.5: return ("MEDIUM", ...)
    else:           return ("HIGH",   ...)

# Process parameter normal operating ranges (page_process_monitoring)
THRESHOLDS = {
    '% Iron Feed':          (50, 65, "% Fe"),
    '% Silica Feed':        (5,  20, "% SiO₂"),
    'Starch Flow':          (1500, 4000, "m³/h"),
    'Ore Pulp pH':          (8.0, 11.0, "pH"),
    '% Silica Concentrate': (0,   2.0,  "% SiO₂"),
    # ...
}
```

---

## Requirements

A minimal `requirements.txt`:

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.26.0
plotly>=5.20.0
xgboost>=2.0.0
scikit-learn>=1.4.0
joblib>=1.3.0
```

---

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

<div align="center">
  Built for industrial analytics demonstration &nbsp;·&nbsp; XGBoost + Streamlit + Plotly
</div>
