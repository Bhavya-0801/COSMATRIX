# 👤 Bhavya — COSMATRIX Dashboard

This folder contains **Bhavya's contribution** to the COSMATRIX project: the interactive Streamlit dashboard connecting Purva's data pipeline with Suyash's analysis modules.

## 🗂️ Contents

| File | Description |
|------|-------------|
| `app.py` | Streamlit dashboard entry point |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Black, White & Cobalt Blue theme |

## 🚀 Run the Dashboard

For the complete standalone deployable version, use the **`Cosmatrix/`** folder at the root of this repository.

```bash
cd ../Cosmatrix
pip install -r requirements.txt
streamlit run app.py
```

## 📋 Dashboard Features

| Tab | Description |
|-----|-------------|
| 🔭 Rotation Curves | Interactive SPARC rotation curves with error bars & anomaly highlights |
| ⚖️ Mass & Dark Matter | Enclosed total, baryonic & dark matter mass profiles |
| 📊 Statistical Metrics | Descriptive statistics, Pearson correlation heatmap, velocity distributions |
| 🚨 Kinematic Anomalies | Z-score & IQR dual-criterion anomaly detection visualizations |
| 🌐 Galaxy Cohort | Comparative side-by-side analysis of up to 8 galaxies |
| 📋 SPARC Metadata | Survey-wide distribution histograms & parameter relationships |

## 🔗 Architecture

```
Purva (data/processed/*.csv)
         ↓
    data_bridge.py   ← Bhavya (Schema Bridge)
         ↓
Suyash (analysis modules)
         ↓
    app.py           ← Bhavya (Streamlit Dashboard)
```

---
**COSMATRIX** — Bhavya Contribution 🌌
