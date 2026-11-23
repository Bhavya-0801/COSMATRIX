"""
COSMATRIX — Interactive Galactic Behaviour Analytics Platform
Contributors:
  - Purva: SPARC Data Collection, Ingestion & Preprocessing Pipeline
  - Suyash: Kinematic & Physics-based Mathematical Modeling Modules
  - Bhavya: Unified Data Bridge & Interactive Streamlit Analytics Dashboard

Theme: 80% Black (#000000), 15% White (#FFFFFF), 5% Cobalt Blue (#2C3480)
"""

import sys
from pathlib import Path

# ── Ensure local sibling modules are importable ──
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ── COSMATRIX modules ─────────────────────────────────────────────────────────
from data_bridge import (
    list_available_galaxies,
    load_galaxy_for_analysis,
    load_multiple_galaxies,
)
from data_pipeline.data_loader import load_galaxy_metadata
from analysis.rotation_analysis import (
    calculate_rotation_curves,
    calculate_velocity_difference,
    calculate_percentage_difference,
)
from analysis.mass_estimation import estimate_galaxy_mass
from analysis.statistical_analysis import (
    calculate_descriptive_statistics,
    calculate_correlation,
    calculate_velocity_statistics,
)
from analysis.anomaly_detection import analyze_anomalies

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COSMATRIX — Galactic Analytics",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 80/15/5 THEME: 80% Black (#000000), 15% White (#FFFFFF), 5% Cobalt Blue (#2C3480)
# Clean, modern, scientific instrument aesthetic with physical micro-interactions
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* 80% Black Baseline: Solid deep black surfaces */
.stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* Sidebar: 80% Black depth with subtle cobalt division */
[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid #161622 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label {
    color: #CCCCCC !important;
}

/* 15% White Typography & Contrast Elements */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    letter-spacing: -0.015em !important;
}

p, span, div {
    color: #EEEEEE;
}

/* Subtle Realistic Micro-Interaction Animations */
@keyframes entranceFade {
    0% {
        opacity: 0;
        transform: translateY(5px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.stMetric, .stAlert, [data-testid="stExpander"], div[data-testid="stPlotlyChart"], .element-container {
    animation: entranceFade 0.3s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* Metric Cards: Black surface (#0C0C0E) + 5% Cobalt Top Accent (#2C3480) */
[data-testid="metric-container"] {
    background-color: #0C0C0E !important;
    border: 1px solid #1C1C24 !important;
    border-top: 2px solid #2C3480 !important;
    border-radius: 6px !important;
    padding: 14px 18px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.6) !important;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    border-color: #2C3480 !important;
    box-shadow: 0 4px 16px rgba(44, 52, 128, 0.25) !important;
}

[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #AAAAAA !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
}

/* Tab Navigation: Black with Cobalt (#2C3480) Active Indicator */
.stTabs [data-baseweb="tab-list"] {
    background-color: #0C0C0E !important;
    border: 1px solid #1C1C24 !important;
    border-radius: 6px !important;
    padding: 4px !important;
    gap: 3px !important;
}

.stTabs [data-baseweb="tab"] {
    color: #888888 !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 8px 16px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    transition: color 0.15s ease, background-color 0.15s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #FFFFFF !important;
    background-color: #161620 !important;
}

.stTabs [aria-selected="true"] {
    background-color: #2C3480 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* 5% Cobalt Blue Interactive Buttons */
.stButton > button {
    background-color: #2C3480 !important;
    color: #FFFFFF !important;
    border: 1px solid #3B46A3 !important;
    border-radius: 5px !important;
    padding: 7px 18px !important;
    font-weight: 500 !important;
    transition: background-color 0.2s ease, border-color 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
}

.stButton > button:hover {
    background-color: #38429C !important;
    border-color: #505ECC !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(44, 52, 128, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0);
}

/* Selectbox and Input Surfaces */
div[data-baseweb="select"] > div {
    background-color: #0C0C0E !important;
    border: 1px solid #20202C !important;
    border-radius: 5px !important;
    color: #FFFFFF !important;
    transition: border-color 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {
    border-color: #2C3480 !important;
}

/* Data Table Container */
div[data-testid="stDataFrame"] {
    background-color: #0C0C0E !important;
    border: 1px solid #1C1C24 !important;
    border-radius: 6px !important;
}

/* Dividers */
hr {
    border: 0 !important;
    height: 1px !important;
    background-color: #1C1C24 !important;
    margin: 20px 0 !important;
}

/* Alerts / Expanders */
.stAlert {
    background-color: #0C0C0E !important;
    border: 1px solid #20202C !important;
    color: #EEEEEE !important;
    border-radius: 6px !important;
}

[data-testid="stExpander"] {
    background-color: #0C0C0E !important;
    border: 1px solid #1C1C24 !important;
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCIENTIFIC PLOT COLOR PALETTE: Black Canvas, White Elements, Cobalt Accents
# ─────────────────────────────────────────────────────────────────────────────
COLORS = dict(
    obs="#FFFFFF",        # White (Observed rotational velocity)
    bar="#3E4AB8",        # Cobalt Blue Accent (Baryonic visible matter)
    gas="#7E8BA8",        # Muted Slate Blue (Gas component)
    disk="#B0C2DE",       # Light Ice Blue (Stellar disk)
    bulge="#9DA8BA",      # Cool Taupe (Bulge component)
    dark="#4A56C4",       # Vivid Cobalt Light (Dark matter halo proxy)
    anomaly="#E84A5F",    # Vermilion Red (Kinematic anomalies)
)

def _black_theme(fig, axes):
    """Styles matplotlib plots with 80% Black canvas, White typography, and subtle cobalt borders."""
    fig.patch.set_facecolor("#000000")
    for ax in (axes if hasattr(axes, "__iter__") else [axes]):
        ax.set_facecolor("#0A0A0D")
        ax.tick_params(colors="#DDDDDD", labelsize=9)
        ax.xaxis.label.set_color("#FFFFFF")
        ax.yaxis.label.set_color("#FFFFFF")
        ax.title.set_color("#FFFFFF")
        for s in ax.spines.values():
            s.set_edgecolor("#20202C")
            s.set_linewidth(1.0)
        ax.grid(True, color="#1A1A24", alpha=0.6, linestyle="--", linewidth=0.7)

LEG = dict(facecolor="#0A0A0D", edgecolor="#20202C", labelcolor="#FFFFFF")

@st.cache_data
def _galaxies():
    return list_available_galaxies()

@st.cache_data
def _meta():
    try:
        return load_galaxy_metadata()
    except Exception:
        return pd.DataFrame()

@st.cache_data
def _analyse(name):
    df = load_galaxy_for_analysis(name)
    for fn in [
        calculate_rotation_curves,
        calculate_velocity_difference,
        calculate_percentage_difference,
        estimate_galaxy_mass,
        analyze_anomalies,
    ]:
        df = fn(df)
    return df

@st.cache_data
def _multi(names_tuple):
    df = load_multiple_galaxies(list(names_tuple))
    for fn in [
        calculate_rotation_curves,
        calculate_velocity_difference,
        calculate_percentage_difference,
        estimate_galaxy_mass,
        analyze_anomalies,
    ]:
        df = fn(df)
    return df

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
glist = _galaxies()
meta = _meta()

with st.sidebar:
    st.markdown("## 🌌 COSMATRIX")
    st.caption("Dark Matter & Galactic Dynamics Analytics Platform")
    st.markdown("---")
    st.markdown(f"**Dataset:** {len(glist)} SPARC Galaxies")
    st.markdown("**Catalog:** Lelli et al. 2016")
    st.markdown("---")

    st.markdown("### 🔭 Galaxy Target")
    sel = st.selectbox(
        "Select Target",
        glist,
        index=glist.index("CamB") if "CamB" in glist else 0,
        help="Select a galaxy to analyze observational rotation curves and dark matter signatures",
    )

    st.markdown("### 📡 Multi-Galaxy Cohort")
    cmp = st.multiselect(
        "Cohort Comparison",
        glist,
        default=glist[:3] if len(glist) >= 3 else glist,
        max_selections=8,
        help="Select up to 8 galaxies for side-by-side behavioral comparison",
    )

    st.markdown("---")
    st.markdown("### ⚙️ Analytical Settings")
    show_err = st.checkbox("Measurement Uncertainties (errV)", True)
    show_comp = st.checkbox("Baryonic Components (Gas/Disk/Bulge)", True)
    anom_mode = st.radio(
        "Anomaly Detection Criteria",
        ["Both (Z-score & IQR)", "Z-score Only", "IQR Only", "None"],
    )
    st.markdown("---")
    st.caption(
        "Project Contributors:\n"
        "• Purva: SPARC Data Collection & Preprocessing\n"
        "• Suyash: Physics Models & Kinematic Analytics\n"
        "• Bhavya: Data Bridge & Interactive Dashboard"
    )

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 8px 0 16px;'>
    <h1 style='font-size: 2.4rem; margin-bottom: 4px; color: #FFFFFF;'>COSMATRIX</h1>
    <p style='color: #CCCCCC; font-size: 1.05rem; margin-top: 0;'>
        An Intelligent Dark Matter &amp; Galactic Behaviour Analytics Platform
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Overview Metrics ──────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Catalog Galaxies", len(glist))
if not meta.empty:
    d = pd.to_numeric(meta.get("D"), errors="coerce")
    vf = pd.to_numeric(meta.get("Vflat"), errors="coerce").replace(0, np.nan)
    t = pd.to_numeric(meta.get("T"), errors="coerce")
    c2.metric("Mean Distance", f"{d.mean():.1f} Mpc" if d.notna().any() else "N/A")
    c3.metric("Mean V_flat", f"{vf.mean():.0f} km/s" if vf.notna().any() else "N/A")
    c4.metric("Morphology Types", f"{t.dropna().nunique()}" if t.notna().any() else "N/A")
else:
    c2.metric("Mean Distance", "N/A")
    c3.metric("Mean V_flat", "N/A")
    c4.metric("Morphology Types", "N/A")
c5.metric("Analysis Engines", "5 Active")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
t1, t2, t3, t4, t5, t6 = st.tabs([
    "🔭 Rotation Curves",
    "⚖️ Mass & Dark Matter",
    "📊 Statistical Metrics",
    "🚨 Kinematic Anomalies",
    "🌐 Galaxy Cohort",
    "📋 SPARC Metadata",
])

# ══════════════════ TAB 1 — ROTATION CURVE ═══════════════════════════════════
with t1:
    st.subheader(f"Kinematic Rotation Curve: {sel}")
    try:
        df = _analyse(sel)
        if not meta.empty:
            gm = meta[meta["Galaxy"].astype(str).str.strip() == sel]
            if not gm.empty:
                gm = gm.iloc[0]
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Distance (D)", f"{gm['D']:.2f} Mpc" if pd.notna(gm.get("D")) else "N/A")
                m2.metric("Inclination (i)", f"{gm['Inc']:.0f}°" if pd.notna(gm.get("Inc")) else "N/A")
                m3.metric(
                    "Asymptotic V_flat",
                    f"{gm['Vflat']:.0f} km/s"
                    if pd.notna(gm.get("Vflat")) and gm["Vflat"] > 0
                    else "N/A",
                )
                m4.metric("Hubble Stage (T)", f"{int(gm['T'])}" if pd.notna(gm.get("T")) else "N/A")

        fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
        _black_theme(fig, axes)

        if anom_mode == "Both (Z-score & IQR)":
            amask = df["Final_Anomaly"]
        elif anom_mode == "Z-score Only":
            amask = df["Zscore_Anomaly"]
        elif anom_mode == "IQR Only":
            amask = df["IQR_Anomaly"]
        else:
            amask = pd.Series(False, index=df.index)
        norm = df[~amask]
        anom = df[amask]

        # Left: Rotation Curve
        ax = axes[0]
        if show_err:
            ax.errorbar(
                norm["Radius_kpc"],
                norm["V_obs_km_s"],
                yerr=norm.get("errV", 0),
                fmt="o",
                color=COLORS["obs"],
                capsize=3,
                label="Observed Velocity (V_obs)",
                markersize=4.5,
                alpha=0.95,
            )
        else:
            ax.scatter(
                norm["Radius_kpc"],
                norm["V_obs_km_s"],
                color=COLORS["obs"],
                label="Observed Velocity (V_obs)",
                s=28,
                alpha=0.95,
            )
        ax.plot(
            df["Radius_kpc"],
            df["V_bar_km_s"],
            color=COLORS["bar"],
            lw=2.2,
            label="Baryonic Visible Matter (V_bar)",
        )
        if show_comp:
            ax.plot(
                df["Radius_kpc"],
                df["V_gas_km_s"],
                color=COLORS["gas"],
                lw=1.2,
                ls="--",
                label="Gas Component",
                alpha=0.8,
            )
            ax.plot(
                df["Radius_kpc"],
                df["V_disk_km_s"],
                color=COLORS["disk"],
                lw=1.2,
                ls="--",
                label="Stellar Disk",
                alpha=0.8,
            )
            ax.plot(
                df["Radius_kpc"],
                df["V_bulge_km_s"],
                color=COLORS["bulge"],
                lw=1.2,
                ls="--",
                label="Bulge Component",
                alpha=0.8,
            )
        if not anom.empty:
            ax.scatter(
                anom["Radius_kpc"],
                anom["V_obs_km_s"],
                color=COLORS["anomaly"],
                s=90,
                zorder=5,
                marker="x",
                linewidths=2,
                label=f"Flagged Points ({len(anom)})",
            )
        ax.set_xlabel("Galactocentric Radius (kpc)")
        ax.set_ylabel("Rotational Velocity (km/s)")
        ax.set_title(f"Velocity Distribution — {sel}")
        ax.legend(fontsize=8, **LEG)

        # Right: Velocity Residual (Dark Matter Signature)
        ax2 = axes[1]
        ax2.axhline(0, color="#666677", lw=1.0, ls="--")
        ax2.scatter(
            df["Radius_kpc"],
            df["Velocity_Difference_km_s"],
            color=COLORS["bar"],
            s=28,
            alpha=0.85,
            label="Residual ΔV (V_obs − V_bar)",
        )
        ax2.fill_between(
            df["Radius_kpc"],
            df["Velocity_Difference_km_s"],
            alpha=0.2,
            color=COLORS["bar"],
        )
        ax2.set_xlabel("Galactocentric Radius (kpc)")
        ax2.set_ylabel("Velocity Excess ΔV (km/s)")
        ax2.set_title(f"Non-Baryonic Velocity Discrepancy — {sel}")
        ax2.legend(fontsize=8, **LEG)
        st.pyplot(fig)
        plt.close()

        km1, km2, km3, km4 = st.columns(4)
        km1.metric("Peak V_obs", f"{df['V_obs_km_s'].max():.1f} km/s")
        km2.metric("Peak V_bar", f"{df['V_bar_km_s'].max():.1f} km/s")
        km3.metric("Mean Velocity Excess", f"{df['Velocity_Difference_km_s'].mean():.1f} km/s")
        km4.metric("Statistical Anomalies", f"{int(df['Final_Anomaly'].sum())}")

        with st.expander("Explore Processed Observational Data"):
            st.dataframe(
                df.style.format({c: "{:.3f}" for c in df.select_dtypes("float").columns}),
                use_container_width=True,
            )
    except Exception as e:
        st.error(f"Error computing rotation curves: {e}")

# ══════════════════ TAB 2 — MASS ANALYSIS ════════════════════════════════════
with t2:
    st.subheader(f"Gravitational Mass Profile: {sel}")
    try:
        df = _analyse(sel)
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
        _black_theme(fig, axes)

        ax = axes[0]
        ax.plot(
            df["Radius_kpc"],
            df["Total_Mass_Solar"] / 1e10,
            color=COLORS["obs"],
            lw=2.2,
            label="Enclosed Dynamic Mass",
        )
        ax.plot(
            df["Radius_kpc"],
            df["Baryonic_Mass_Solar"] / 1e10,
            color=COLORS["bar"],
            lw=2.2,
            label="Enclosed Baryonic Mass",
        )
        dm = df["Additional_Mass_Solar"].dropna()
        ax.plot(
            df.loc[dm.index, "Radius_kpc"],
            dm / 1e10,
            color=COLORS["dark"],
            lw=2.2,
            ls="--",
            label="Inferred Dark Matter Halo",
        )
        ax.fill_between(
            df.loc[dm.index, "Radius_kpc"],
            dm / 1e10,
            alpha=0.2,
            color=COLORS["dark"],
        )
        ax.set_xlabel("Radius (kpc)")
        ax.set_ylabel("Enclosed Mass (×10¹⁰ M☉)")
        ax.set_title(f"Cumulative Mass Profiles — {sel}")
        ax.legend(fontsize=8, **LEG)

        ax2 = axes[1]
        frac = (df["Additional_Mass_Solar"].fillna(0) / df["Total_Mass_Solar"] * 100).clip(0, 100)
        ax2.plot(df["Radius_kpc"], frac, color=COLORS["dark"], lw=2.2, label="Dark Matter Ratio")
        ax2.fill_between(df["Radius_kpc"], frac, alpha=0.25, color=COLORS["dark"])
        ax2.set_xlabel("Radius (kpc)")
        ax2.set_ylabel("Dark Matter Ratio (%)")
        ax2.set_title(f"Dark Matter Fraction Radial Gradient — {sel}")
        ax2.set_ylim(0, 100)
        ax2.legend(fontsize=8, **LEG)
        st.pyplot(fig)
        plt.close()

        last = df.iloc[-1]
        mm1, mm2, mm3, mm4 = st.columns(4)
        mm1.metric("Total Outer Mass", f"{last['Total_Mass_Solar']/1e10:.2f} ×10¹⁰ M☉")
        mm2.metric("Baryonic Outer Mass", f"{last['Baryonic_Mass_Solar']/1e10:.2f} ×10¹⁰ M☉")
        dm_v = last.get("Additional_Mass_Solar")
        mm3.metric(
            "Dark Matter Proxy",
            f"{dm_v/1e10:.2f} ×10¹⁰ M☉" if pd.notna(dm_v) and dm_v else "N/A",
        )
        mm4.metric(
            "Outer DM Dominance",
            f"{dm_v/last['Total_Mass_Solar']*100:.1f}%" if pd.notna(dm_v) and dm_v else "0.0%",
        )

        with st.expander("Inspect Mass Model Quantities"):
            cols = [
                "Radius_kpc",
                "V_obs_km_s",
                "V_bar_km_s",
                "Total_Mass_Solar",
                "Baryonic_Mass_Solar",
                "Additional_Mass_Solar",
            ]
            st.dataframe(
                df[cols]
                .style.format(
                    "{:.3e}",
                    subset=["Total_Mass_Solar", "Baryonic_Mass_Solar", "Additional_Mass_Solar"],
                )
                .format("{:.3f}", subset=["Radius_kpc", "V_obs_km_s", "V_bar_km_s"]),
                use_container_width=True,
            )
    except Exception as e:
        st.error(f"Error computing mass estimates: {e}")

# ══════════════════ TAB 3 — STATISTICS ═══════════════════════════════════════
with t3:
    st.subheader(f"Statistical Modeling & Diagnostics: {sel}")
    try:
        df = _analyse(sel)
        desc = calculate_descriptive_statistics(df)
        corr = calculate_correlation(df)
        vs = calculate_velocity_statistics(df)

        v1, v2, v3, v4 = st.columns(4)
        v1.metric("Mean Residual ΔV", f"{vs['Mean_Residual']:.2f} km/s")
        v2.metric("Mean Absolute Error", f"{vs['MAE']:.2f} km/s")
        v3.metric("Root Mean Square Error", f"{vs['RMSE']:.2f} km/s")
        v4.metric("Pearson Corr (V_obs, V_bar)", f"{vs['Correlation']:.4f}")

        ca, cb = st.columns(2)
        with ca:
            st.markdown("##### Descriptive Statistics")
            st.dataframe(pd.DataFrame(desc).T.style.format("{:.3f}"), use_container_width=True)
        with cb:
            st.markdown("##### Correlation Matrix")
            fig, ax = plt.subplots(figsize=(6, 4))
            _black_theme(fig, ax)
            sns.heatmap(
                corr,
                annot=True,
                fmt=".2f",
                cmap="mako",
                ax=ax,
                linewidths=0.5,
                linecolor="#1C1C24",
                cbar_kws={"shrink": 0.8},
                annot_kws={"size": 8, "color": "#FFFFFF"},
            )
            ax.set_title(f"Parameter Correlation — {sel}", pad=10)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        st.markdown("##### Empirical Velocity Distributions")
        fig2, axes2 = plt.subplots(1, 3, figsize=(14, 4))
        _black_theme(fig2, axes2)
        for ax_, col_, clr_, lbl_ in zip(
            axes2,
            ["V_obs_km_s", "V_bar_km_s", "Velocity_Difference_km_s"],
            [COLORS["obs"], COLORS["bar"], COLORS["dark"]],
            ["V_obs (km/s)", "V_bar (km/s)", "Residual ΔV (km/s)"],
        ):
            ax_.hist(df[col_].dropna(), bins=14, color=clr_, alpha=0.85, edgecolor="#000000")
            ax_.axvline(df[col_].mean(), color="#FFFFFF", ls="--", lw=1.2, label="Mean")
            ax_.set_xlabel(lbl_)
            ax_.set_ylabel("Frequency")
            ax_.set_title(lbl_)
            ax_.legend(fontsize=7, **LEG)
        st.pyplot(fig2)
        plt.close()
    except Exception as e:
        st.error(f"Error computing statistics: {e}")

# ══════════════════ TAB 4 — ANOMALY DETECTION ════════════════════════════════
with t4:
    st.subheader(f"Kinematic Anomaly Detection: {sel}")
    try:
        df = _analyse(sel)
        zc = int(df["Zscore_Anomaly"].sum())
        ic = int(df["IQR_Anomaly"].sum())
        fc = int(df["Final_Anomaly"].sum())
        tot = len(df)

        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Evaluated Data Points", tot)
        a2.metric("Z-Score Threshold Exceeded", zc)
        a3.metric("IQR Boundary Outliers", ic)
        a4.metric("Confirmed Dual Anomalies", fc, delta=f"{fc/tot*100:.1f}%", delta_color="inverse")

        fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
        _black_theme(fig, axes)

        # Z-Score
        ax = axes[0]
        nm = ~df["Zscore_Anomaly"]
        ax.scatter(
            df.loc[nm, "Radius_kpc"],
            df.loc[nm, "Z_Score"],
            color=COLORS["bar"],
            s=28,
            alpha=0.85,
            label="In-Distribution Data",
        )
        if df["Zscore_Anomaly"].any():
            ax.scatter(
                df.loc[df["Zscore_Anomaly"], "Radius_kpc"],
                df.loc[df["Zscore_Anomaly"], "Z_Score"],
                color=COLORS["anomaly"],
                s=90,
                marker="x",
                linewidths=2,
                zorder=5,
                label=f"Z-Score Outlier (|Z| > 3)",
            )
        ax.axhline(3, color="#FFFFFF", ls="--", lw=1, label="+3σ Limit")
        ax.axhline(-3, color="#FFFFFF", ls="--", lw=1, label="−3σ Limit")
        ax.set_xlabel("Radius (kpc)")
        ax.set_ylabel("Standardized Z-Score")
        ax.set_title(f"Standardized Residual Dispersion — {sel}")
        ax.legend(fontsize=7, **LEG)

        # IQR Outliers
        ax2 = axes[1]
        r = df["Velocity_Difference_km_s"]
        Q1, Q3 = r.quantile(0.25), r.quantile(0.75)
        IQR = Q3 - Q1
        lb, ub = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        nm2 = ~df["IQR_Anomaly"]
        ax2.scatter(
            df.loc[nm2, "Radius_kpc"],
            r[nm2],
            color=COLORS["bar"],
            s=28,
            alpha=0.85,
            label="Quartile Inliers",
        )
        if df["IQR_Anomaly"].any():
            ax2.scatter(
                df.loc[df["IQR_Anomaly"], "Radius_kpc"],
                r[df["IQR_Anomaly"]],
                color=COLORS["anomaly"],
                s=90,
                marker="x",
                linewidths=2,
                zorder=5,
                label=f"Tukey Outliers ({ic})",
            )
        ax2.axhline(ub, color="#FFFFFF", ls="--", lw=1, label=f"Upper Bound ({ub:.1f})")
        ax2.axhline(lb, color="#FFFFFF", ls=":", lw=1, label=f"Lower Bound ({lb:.1f})")
        ax2.set_xlabel("Radius (kpc)")
        ax2.set_ylabel("Residual ΔV (km/s)")
        ax2.set_title(f"Interquartile Range Bounds — {sel}")
        ax2.legend(fontsize=7, **LEG)
        st.pyplot(fig)
        plt.close()

        if fc > 0:
            st.warning(
                f"{fc} observation(s) meet both Z-score and IQR anomaly criteria. "
                "Investigate observational quality flags or non-circular dynamics."
            )
            with st.expander("View Anomaly Records"):
                cols = [
                    "Radius_kpc",
                    "V_obs_km_s",
                    "V_bar_km_s",
                    "Velocity_Difference_km_s",
                    "Z_Score",
                    "Zscore_Anomaly",
                    "IQR_Anomaly",
                    "Final_Anomaly",
                ]
                st.dataframe(df[df["Final_Anomaly"]][cols], use_container_width=True)
        else:
            st.info("No significant kinematic anomalies detected under standard criteria.")
    except Exception as e:
        st.error(f"Error executing anomaly detection: {e}")

# ══════════════════ TAB 5 — GALAXY COMPARISON ════════════════════════════════
with t5:
    st.subheader("Multi-Galaxy Kinematic Cohort Comparison")
    if len(cmp) < 2:
        st.info("Select at least 2 galaxies from the sidebar to generate cohort comparisons.")
    else:
        try:
            cdf = _multi(tuple(cmp))
            cohort_palette = ["#FFFFFF", "#3E4AB8", "#7E8BA8", "#B0C2DE", "#505ECC", "#8E9BC4", "#A4B1D6", "#323B99"]
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            _black_theme(fig, axes.flatten())

            # Rotation curves
            ax = axes[0, 0]
            for i, g in enumerate(cmp):
                gdf = cdf[cdf["Galaxy"] == g]
                ax.plot(
                    gdf["Radius_kpc"],
                    gdf["V_obs_km_s"],
                    color=cohort_palette[i % len(cohort_palette)],
                    lw=1.8,
                    label=g,
                    alpha=0.9,
                )
            ax.set_xlabel("Radius (kpc)")
            ax.set_ylabel("V_obs (km/s)")
            ax.set_title("Observed Rotation Velocity Curves")
            ax.legend(fontsize=7, **LEG)

            # V_obs vs V_bar
            ax2 = axes[0, 1]
            for i, g in enumerate(cmp):
                gdf = cdf[cdf["Galaxy"] == g]
                ax2.scatter(
                    gdf["V_bar_km_s"],
                    gdf["V_obs_km_s"],
                    color=cohort_palette[i % len(cohort_palette)],
                    s=22,
                    label=g,
                    alpha=0.85,
                )
            vm = cdf[["V_obs_km_s", "V_bar_km_s"]].max().max()
            ax2.plot([0, vm], [0, vm], color="#666677", ls="--", lw=1, label="1:1 Ratio (No DM)")
            ax2.set_xlabel("V_bar (km/s)")
            ax2.set_ylabel("V_obs (km/s)")
            ax2.set_title("Observed vs Baryonic Dynamic Ratio")
            ax2.legend(fontsize=7, **LEG)

            # Residuals
            ax3 = axes[1, 0]
            for i, g in enumerate(cmp):
                gdf = cdf[cdf["Galaxy"] == g]
                ax3.plot(
                    gdf["Radius_kpc"],
                    gdf["Velocity_Difference_km_s"],
                    color=cohort_palette[i % len(cohort_palette)],
                    lw=1.8,
                    label=g,
                    alpha=0.9,
                )
            ax3.axhline(0, color="#666677", ls="--", lw=1)
            ax3.set_xlabel("Radius (kpc)")
            ax3.set_ylabel("Velocity Excess ΔV (km/s)")
            ax3.set_title("Kinematic Excess Profiles")
            ax3.legend(fontsize=7, **LEG)

            # DM fraction bar chart
            ax4 = axes[1, 1]
            names_, fracs_, clrs_ = [], [], []
            for i, g in enumerate(cmp):
                gdf = cdf[cdf["Galaxy"] == g]
                if gdf.empty:
                    continue
                lr = gdf.iloc[-1]
                dm = lr.get("Additional_Mass_Solar", np.nan)
                f = max((dm / lr["Total_Mass_Solar"] * 100) if pd.notna(dm) and lr["Total_Mass_Solar"] > 0 else 0, 0)
                names_.append(g)
                fracs_.append(f)
                clrs_.append(cohort_palette[i % len(cohort_palette)])
            bars = ax4.barh(names_, fracs_, color=clrs_, alpha=0.9, edgecolor="#000000")
            ax4.set_xlabel("Outer Dark Matter Ratio (%)")
            ax4.set_title("Peripheral Halo Dominance Ratio")
            ax4.set_xlim(0, 100)
            for b, v in zip(bars, fracs_):
                ax4.text(
                    b.get_width() + 1.2,
                    b.get_y() + b.get_height() / 2,
                    f"{v:.1f}%",
                    va="center",
                    ha="left",
                    fontsize=8,
                    color="#FFFFFF",
                )
            plt.tight_layout(pad=2.2)
            st.pyplot(fig)
            plt.close()

            st.markdown("##### Cohort Analytical Summary")
            rows = []
            for g in cmp:
                gdf = cdf[cdf["Galaxy"] == g]
                if gdf.empty:
                    continue
                rows.append({
                    "Galaxy": g,
                    "Data Points": len(gdf),
                    "Max V_obs (km/s)": gdf["V_obs_km_s"].max(),
                    "Max V_bar (km/s)": gdf["V_bar_km_s"].max(),
                    "Mean ΔV Excess": gdf["Velocity_Difference_km_s"].mean(),
                    "Anomalies": int(gdf["Final_Anomaly"].sum()),
                })
            st.dataframe(
                pd.DataFrame(rows).style.format(
                    {"Max V_obs (km/s)": "{:.1f}", "Max V_bar (km/s)": "{:.1f}", "Mean ΔV Excess": "{:.1f}"}
                ),
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Error computing cohort analytics: {e}")

# ══════════════════ TAB 6 — DATASET OVERVIEW ═════════════════════════════════
with t6:
    st.subheader("SPARC Galaxy Survey Global Overview")
    if meta.empty:
        st.warning("Survey metadata table not found.")
    else:
        oc1, oc2, oc3 = st.columns(3)
        oc1.metric("Catalog Size", f"{len(meta)} Galaxies")
        d = pd.to_numeric(meta["D"], errors="coerce").dropna()
        oc2.metric("Distance Range", f"{d.min():.1f} – {d.max():.1f} Mpc")
        oc3.metric("Mean Inclination Angle", f"{pd.to_numeric(meta['Inc'], errors='coerce').mean():.1f}°")

        fig, axes = plt.subplots(2, 2, figsize=(14, 9))
        _black_theme(fig, axes.flatten())

        d.hist(ax=axes[0, 0], bins=24, color=COLORS["bar"], edgecolor="#000000", alpha=0.9)
        axes[0, 0].set_xlabel("Distance (Mpc)")
        axes[0, 0].set_ylabel("Galaxy Count")
        axes[0, 0].set_title("Distance Distribution")

        vf = pd.to_numeric(meta["Vflat"], errors="coerce").replace(0, np.nan).dropna()
        vf.hist(ax=axes[0, 1], bins=24, color=COLORS["obs"], edgecolor="#000000", alpha=0.9)
        axes[0, 1].set_xlabel("Flat Rotation Velocity (km/s)")
        axes[0, 1].set_ylabel("Galaxy Count")
        axes[0, 1].set_title("V_flat Characteristic Velocity Distribution")

        t_ = pd.to_numeric(meta["T"], errors="coerce").dropna().value_counts().sort_index()
        axes[1, 0].bar(t_.index, t_.values, color=COLORS["dark"], alpha=0.9, edgecolor="#000000")
        axes[1, 0].set_xlabel("Hubble Morphological Stage (T)")
        axes[1, 0].set_ylabel("Galaxy Count")
        axes[1, 0].set_title("Morphological Classification")

        v = meta[["D", "Vflat", "T"]].copy()
        for col in ["D", "Vflat", "T"]:
            v[col] = pd.to_numeric(v[col], errors="coerce")
        v["Vflat"] = v["Vflat"].replace(0, np.nan)
        v = v.dropna()
        sc = axes[1, 1].scatter(
            v["D"],
            v["Vflat"],
            c=v["T"],
            cmap="Blues_r",
            s=32,
            alpha=0.9,
            edgecolors="#000000",
        )
        cbar = plt.colorbar(sc, ax=axes[1, 1])
        cbar.set_label("Hubble Type (T)", color="#FFFFFF")
        cbar.ax.yaxis.set_tick_params(color="#FFFFFF")
        plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="#FFFFFF")
        axes[1, 1].set_xlabel("Distance (Mpc)")
        axes[1, 1].set_ylabel("V_flat (km/s)")
        axes[1, 1].set_title("Distance vs Characteristic Rotational Velocity")
        plt.tight_layout(pad=2.2)
        st.pyplot(fig)
        plt.close()

        with st.expander("View Complete SPARC Catalog Metadata"):
            st.dataframe(meta, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888899; font-size: 0.85rem; padding: 12px 0;'>
    <b>COSMATRIX</b> — An Intelligent Dark Matter &amp; Galactic Behaviour Analytics Platform<br>
    Observational Data: SPARC (Lelli et al. 2016) · Theme: Black (#000000) 80%, White (#FFFFFF) 15%, Cobalt Blue (#2C3480) 5%<br>
    Purva (Data Pipeline) · Suyash (Physics Modeling) · Bhavya (Dashboard &amp; Integration)
</div>
""", unsafe_allow_html=True)
