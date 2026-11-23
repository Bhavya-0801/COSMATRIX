# 👤 Person 3 — DARKVERSE Dashboard

This folder contains **Person 3's contribution** to the DARKVERSE project: the interactive Streamlit dashboard that connects Person 1's data pipeline with Person 2's analysis modules.

## 🗂️ Contents

| File | Description |
|------|-------------|
| `app.py` | Streamlit dashboard entry point |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Dark space theme configuration |

## 🚀 Run the Dashboard

For the full standalone deployable version, use the **`Darkverse/`** folder at the root of this repository.

```bash
cd ../Darkverse
pip install -r requirements.txt
streamlit run app.py
```

## 📋 Dashboard Features

| Tab | Description |
|-----|-------------|
| 🔭 Rotation Curve | Interactive SPARC rotation curves with error bars & anomaly highlights |
| ⚖️ Mass Analysis | Total, baryonic & dark matter mass profiles |
| 📊 Statistical Analysis | Descriptive stats, Pearson correlation heatmap, distributions |
| 🚨 Anomaly Detection | Z-score & IQR anomaly detection visualizations |
| 🌐 Galaxy Comparison | Side-by-side comparison of up to 8 galaxies |
| 📋 Dataset Overview | SPARC dataset-wide distribution plots |

## 🔗 Integration

```
Person 1 (data/processed/*.csv)
         ↓
    data_bridge.py   ← Person 3 schema bridge
         ↓
Person 2 (analysis modules)
         ↓
    app.py           ← Person 3 dashboard
```

---
**DARKVERSE** — Person 3 Contribution 🌌

