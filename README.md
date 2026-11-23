# 🌌 COSMATRIX
### An Intelligent Dark Matter & Galactic Behaviour Analytics Platform

**COSMATRIX** is a Python-based astronomical data analytics platform engineered to explore the mysteries of dark matter and galactic dynamics using real SPARC (Spitzer Photometry & Accurate Rotation Curves) astronomical datasets (Lelli et al. 2016).

The platform analyzes galaxy rotation curves, contrasts observed rotational velocities with velocities expected from visible baryonic matter, calculates gravitational mass distributions, and pinpoints kinematic anomalies through an interactive Streamlit dashboard.

---

## 🎨 Design System

**Deep Cosmic Obsidian & Celestial Starlight**:
- **Canvas (`#0A0D14`)**: Deep midnight space obsidian backdrop with subtle celestial nebular dust.
- **Tiles & Panels (`#10141E`)**: Elevated frosted midnight glass with micro-borders (`#1E2638`).
- **Typography (`#F8FAFC`)**: Luminescent white headers and numerical values for pristine readability.
- **Electric Cyan (`#38BDF8`)**: Primary instrument accent, observed rotation curve points and key actions.
- **Nebula Violet (`#A78BFA`)**: Baryonic visible-matter theoretical profiles.
- **Muted Starlight (`#94A3B8`)**: Secondary labels, units, and axis metadata.

---

## 👥 Project Team & Contributors

| Contributor | Role | Core Deliverables |
|-------------|------|-------------------|
| **Purva** | Data Pipeline Engineer | Raw SPARC `.dat` ingestion, validation, cleaning routines, fixed-width metadata parsing |
| **Suyash** | Kinematic & Physics Modeler | Baryonic velocity calculations, spherical enclosed mass estimation, Z-score/IQR anomaly detection algorithms |
| **Bhavya** | Dashboard & Integration Lead | Schema conversion bridge (`data_bridge.py`), interactive multi-view Streamlit analytics dashboard (`app.py`) |

---

## 📁 Repository Architecture

```text
COSMATRIX/
│
├── Purva/                       ← Purva's contribution (SPARC Data Pipeline)
│   ├── src/                     ← Preprocessing, metadata parser & data loader
│   ├── data/                    ← Raw & processed galaxy datasets
│   └── main.py                  ← Pipeline execution script
│
├── Suyash/                      ← Suyash's contribution (Physics & Analytics)
│   ├── analysis/                ← Physics models, mass estimation, statistics, anomaly detection
│   ├── tests/                   ← Unit & integration test suites
│   └── data/sample_galaxy.csv   ← Benchmark galaxy observations
│
├── Bhavya/                      ← Bhavya's contribution (Dashboard Entry Point)
│   ├── app.py                   ← Dashboard runner
│   ├── requirements.txt         ← Dependencies
│   └── .streamlit/config.toml   ← 80/15/5 Theme configuration
│
└── Cosmatrix/                   ← Fully Integrated Deployable Platform
    ├── app.py                   ← Master Streamlit dashboard (6 analysis views)
    ├── data_bridge.py           ← Schema bridge connecting Purva & Suyash modules
    ├── analysis/                ← Core kinematic analytics engines
    ├── data_pipeline/           ← Data loading & validation utilities
    ├── data/processed/          ← 175 SPARC galaxy rotation curves & survey metadata
    ├── requirements.txt         ← Production dependencies
    └── .streamlit/config.toml   ← Theme configuration
```

---

## 🚀 Quick Start & Deployment

### Run Locally

```bash
# Navigate to the deployable directory
cd Cosmatrix

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

### Free Deployment on Streamlit Community Cloud

1. Fork or push this repository to GitHub (`Bhavya-0801/COSMATRIX`)
2. Log in to [share.streamlit.io](https://share.streamlit.io) with GitHub
3. Select **New app**, choose repository `COSMATRIX`, branch `main`
4. Set **Main file path** to: `Cosmatrix/app.py`
5. Click **Deploy!** 🚀

---

## 🔭 Dashboard Capabilities

1. **Kinematic Rotation Curves**: Observed velocity distribution with observational uncertainties, baryonic curves, and velocity residuals.
2. **Gravitational Mass & Halo Modeling**: Cumulative dynamic mass profiles, baryonic mass, and dark matter fraction radial gradients.
3. **Statistical Modeling & Diagnostics**: Pearson correlation matrices, descriptive dispersion metrics, and velocity histograms.
4. **Kinematic Anomaly Identification**: Combined dual-criterion statistical evaluation using standardized Z-scores and Tukey IQR bounds.
5. **Multi-Galaxy Cohort Comparison**: Cross-galaxy velocity comparisons, baryonic ratios, and peripheral halo dominance rankings.
6. **SPARC Catalog Global Survey**: Global distributions of distance, morphological classifications, and characteristic flat rotational velocities ($V_{flat}$).

---

## 🔬 Scientific Methodology

- **Baryonic Rotational Velocity**:
  $$V_{bar} = \sqrt{V_{gas}^2 + V_{disk}^2 + V_{bulge}^2}$$

- **Kinematic Residual (Dark Matter Signature)**:
  $$\Delta V = V_{observed} - V_{bar}$$

- **Dynamic Enclosed Mass (Spherical Approximation)**:
  $$M(r) = \frac{r \cdot v^2}{G}$$

---

**COSMATRIX — Exploring the hidden dynamics of the universe.** 🌌
