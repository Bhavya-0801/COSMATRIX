# 🌌 DARKVERSE
### An Intelligent Dark Matter & Galactic Behaviour Analytics Platform

Fully integrated, deployable version connecting all three contributors.

## 🚀 Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Set **Main file path** to: `Darkverse/app.py`
4. Click **Deploy** ✅

## ▶️ Run Locally

```bash
cd Darkverse
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Structure

```
Darkverse/
├── app.py                  ← Dashboard entry point (Person 3)
├── requirements.txt        ← Dependencies
├── data_bridge.py          ← Schema bridge (Person 3)
├── analysis/               ← Physics & analytics (Person 2)
│   ├── physics_model.py
│   ├── rotation_analysis.py
│   ├── mass_estimation.py
│   ├── statistical_analysis.py
│   └── anomaly_detection.py
├── data_pipeline/          ← Data loading utilities (Person 1)
│   ├── data_loader.py
│   └── preprocessing.py
└── data/
    └── processed/          ← 175 SPARC galaxy CSVs + metadata
```

## 🧪 Three-Person Integration

| | Person | Role |
|--|--------|------|
| 1️⃣ | Person 1 | SPARC data pipeline — loads & cleans 175 galaxy rotation-curve files |
| 2️⃣ | Person 2 | Analysis modules — physics, mass estimation, statistics, anomaly detection |
| 3️⃣ | Person 3 | Schema bridge + Streamlit dashboard connecting both |

---
**DARKVERSE** — Exploring the hidden dynamics of the universe 🌌
