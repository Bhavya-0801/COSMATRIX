# 🌌 COSMATRIX
### An Intelligent Dark Matter & Galactic Behaviour Analytics Platform

Fully integrated, deployable version connecting all three contributors.

## 🚀 Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Set **Main file path** to: `COSMATRIX/app.py`
4. Click **Deploy** ✅

## ▶️ Run Locally

```bash
cd COSMATRIX
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Structure

```
COSMATRIX/
├── app.py                  ← Dashboard entry point (Bhavya)
├── requirements.txt        ← Dependencies
├── data_bridge.py          ← Schema bridge (Bhavya)
├── analysis/               ← Physics & analytics (Suyash)
│   ├── physics_model.py
│   ├── rotation_analysis.py
│   ├── mass_estimation.py
│   ├── statistical_analysis.py
│   └── anomaly_detection.py
├── data_pipeline/          ← Data loading utilities (Purva)
│   ├── data_loader.py
│   └── preprocessing.py
└── data/
    └── processed/          ← 175 SPARC galaxy CSVs + metadata
```

## 🧪 Three-Person Integration

| | Person | Role |
|--|--------|------|
| 1️⃣ | Purva | SPARC data pipeline — loads & cleans 175 galaxy rotation-curve files |
| 2️⃣ | Suyash | Analysis modules — physics, mass estimation, statistics, anomaly detection |
| 3️⃣ | Bhavya | Schema bridge + Streamlit dashboard connecting both |

---
**COSMATRIX** — Exploring the hidden dynamics of the universe 🌌

