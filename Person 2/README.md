# 🌌 DARKVERSE
### An Intelligent Dark Matter & Galactic Behaviour Analytics Platform

DARKVERSE is a Python-based astronomical data analysis project designed to study galaxy rotational behaviour, analyze observed and baryonic velocities, estimate mass distributions, perform statistical analysis, and identify unusual rotational patterns that may indicate additional gravitational contributions beyond visible matter.

The project combines physics-based calculations, data analysis, statistical methods, and anomaly detection to investigate galactic dynamics.

---

## 🚀 Project Objectives

- Analyze galaxy rotation curves.
- Compare observed rotational velocity with baryonic velocity.
- Calculate velocity residuals and percentage differences.
- Estimate total, baryonic, and additional mass.
- Perform statistical analysis on galactic data.
- Detect unusual observations using Z-score and IQR methods.
- Visualize galaxy rotational behaviour.

---

## 📁 Project Structure

```text
cosmatrix/
│
├── analysis/
│   ├── __init__.py
│   ├── physics_model.py
│   ├── rotation_analysis.py
│   ├── mass_estimation.py
│   ├── statistical_analysis.py
│   └── anomaly_detection.py
│
├── data/
│   └── sample_galaxy.csv
│
└── README.md
```

---

## 🧪 Analysis Modules

### 1. Physics Model
Contains fundamental calculations and conversions used throughout the project.

- Kiloparsecs to meters
- Kilometers per second to meters per second
- Kilograms to solar masses
- Baryonic velocity calculation
- Additional velocity contribution calculation

### 2. Rotation Analysis
Processes galaxy datasets and analyzes rotational behaviour.

- Load galaxy data
- Calculate baryonic rotational velocity
- Calculate velocity residuals
- Calculate percentage differences
- Analyze individual galaxies

### 3. Mass Estimation
Estimates galactic mass-related quantities.

- Enclosed total mass
- Baryonic mass
- Additional mass contribution
- Galaxy mass analysis

### 4. Statistical Analysis
Performs statistical analysis on galaxy observations.

- Mean
- Median
- Standard deviation
- Variance
- Minimum and maximum
- Correlation analysis
- MAE
- RMSE
- Galaxy-wise statistical summaries

### 5. Anomaly Detection
Identifies unusual rotational observations using:

- Z-score method
- Interquartile Range (IQR) method
- Combined anomaly classification

---

## 📊 Dataset

The current project uses a sample synthetic galaxy dataset.

The dataset includes:

| Column | Description |
|---|---|
| Galaxy | Galaxy identifier |
| Radius_kpc | Distance from galaxy center in kiloparsecs |
| V_obs_km_s | Observed rotational velocity |
| V_gas_km_s | Gas contribution |
| V_disk_km_s | Stellar disk contribution |
| V_bulge_km_s | Bulge contribution |

> **Note:** The current dataset is synthetic and is used for software testing and demonstration. It is not real astronomical observation data.

---

## ⚙️ Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Statistical analysis
- Physics-based mathematical modelling

---

## 🔬 Scientific Methodology

DARKVERSE calculates the baryonic velocity using the gas, disk, and bulge contributions:

\[
V_{bar}=\sqrt{V_{gas}^{2}+V_{disk}^{2}+V_{bulge}^{2}}
\]

The velocity residual is calculated as:

\[
V_{residual}=V_{observed}-V_{bar}
\]

When the observed velocity is greater than the baryonic velocity, the additional velocity contribution is estimated as:

\[
V_{extra}=\sqrt{V_{observed}^{2}-V_{bar}^{2}}
\]

The enclosed mass is estimated using the spherical-equivalent approximation:

\[
M=\frac{rv^{2}}{G}
\]

These calculations help investigate discrepancies between observed rotational behaviour and the simplified visible-matter model.

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/DARKVERSE.git
```

Navigate into the project:

```bash
cd DARKVERSE
```

Install dependencies:

```bash
pip install numpy pandas matplotlib
```

---

## ▶️ Usage

Import the analysis modules into your Python script:

```python
from analysis.rotation_analysis import load_galaxy_data
from analysis.rotation_analysis import calculate_rotation_curves
from analysis.rotation_analysis import calculate_velocity_difference

# Load dataset
df = load_galaxy_data("data/sample_galaxy.csv")

# Calculate baryonic velocity
df = calculate_rotation_curves(df)

# Calculate velocity residual
df = calculate_velocity_difference(df)

print(df.head())
```

---

## 📈 Visualization

The processed data can be visualized using Matplotlib to generate:

- Observed vs. baryonic rotation curves
- Velocity residual plots
- Observed vs. baryonic velocity comparisons
- Statistical plots
- Anomaly visualizations

---

## 🧠 Anomaly Detection

DARKVERSE uses statistical methods to identify unusual data points.

### Z-score

Measures how far a residual deviates from the mean in terms of standard deviations.

### IQR (Interquartile Range)

Identifies values outside the statistical range defined by quartiles.

Observations flagged by both methods can be classified as final anomalies.

---

## ⚠️ Scientific Limitations

- The current dataset is synthetic.
- Anomaly detection identifies statistical deviations, not dark matter directly.
- The baryonic velocity model is simplified.
- Mass estimates use a spherical-equivalent approximation.
- Real astronomical data and observational uncertainties are required for scientifically meaningful conclusions.

---

## 🔮 Future Scope

- Integration of real astronomical galaxy datasets.
- Interactive visualization dashboard.
- Improved baryonic mass modelling.
- Statistical uncertainty analysis.
- Advanced anomaly detection.
- Galaxy-to-galaxy comparison.
- Machine learning-based rotational behaviour analysis.

---

## 👥 Project Team

Developed as a collaborative academic project focused on astronomy, data science, Python programming, and statistical modelling.

---

## 📜 Disclaimer

DARKVERSE is an educational and research-oriented analytical project. It investigates rotational discrepancies in galaxy data and does not directly detect or confirm dark matter.

---

**DARKVERSE — Exploring the hidden dynamics of the universe.** 🌌