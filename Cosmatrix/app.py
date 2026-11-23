"""
COSMATRIX — An Intelligent Dark Matter & Galactic Behaviour Analytics Platform
Contributors:
  - Purva: SPARC Data Collection, Ingestion & Preprocessing Pipeline
  - Suyash: Kinematic & Physics-based Mathematical Modeling Modules
  - Bhavya: Unified Data Bridge & Interactive Streamlit Analytics Dashboard

Theme: Animated Deep Space & Cosmic Galaxy Atmosphere with High-Precision Scientific Glass UI
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
    page_title="COSMATRIX — Galactic Dynamics & Dark Matter Platform",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# ANIMATED GALAXY & CELESTIAL OBSERVATORY UI
# Pure CSS 60FPS Parallax Starfields, Nebula Gas Vortex & Glass HUD Panels
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ───────────────────────── GALAXY BACKGROUND SYSTEM ───────────────────────── */
.stApp {
    background-color: #05070B !important;
    color: #F1F5F9 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
    overflow-x: hidden;
}

/* Fixed Multi-Layer Cosmic Canvas */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 0;
    background: 
        radial-gradient(circle at 75% 20%, rgba(56, 189, 248, 0.12) 0%, transparent 45%),
        radial-gradient(circle at 20% 75%, rgba(139, 92, 246, 0.14) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.06) 0%, transparent 60%),
        radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.08) 0%, transparent 40%);
    animation: cosmicNebulaDrift 24s ease-in-out infinite alternate;
}

.stApp::after {
    content: "";
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    pointer-events: none;
    z-index: 0;
    background-image: 
        radial-gradient(1px 1px at 40px 60px, rgba(255, 255, 255, 0.95), rgba(0,0,0,0)),
        radial-gradient(1.5px 1.5px at 140px 190px, rgba(248, 250, 252, 0.85), rgba(0,0,0,0)),
        radial-gradient(1px 1px at 280px 80px, rgba(56, 189, 248, 0.9), rgba(0,0,0,0)),
        radial-gradient(2px 2px at 320px 300px, rgba(167, 139, 250, 0.8), rgba(0,0,0,0)),
        radial-gradient(1.2px 1.2px at 480px 220px, rgba(255, 255, 255, 0.9), rgba(0,0,0,0)),
        radial-gradient(1px 1px at 620px 140px, rgba(255, 255, 255, 0.75), rgba(0,0,0,0)),
        radial-gradient(1.8px 1.8px at 740px 380px, rgba(56, 189, 248, 0.85), rgba(0,0,0,0)),
        radial-gradient(1px 1px at 890px 260px, rgba(255, 255, 255, 0.7), rgba(0,0,0,0)),
        radial-gradient(2.2px 2.2px at 980px 120px, rgba(248, 250, 252, 0.9), rgba(0,0,0,0)),
        radial-gradient(1px 1px at 1120px 420px, rgba(167, 139, 250, 0.75), rgba(0,0,0,0)),
        radial-gradient(1.5px 1.5px at 1260px 180px, rgba(255, 255, 255, 0.8), rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 600px 600px;
    animation: galaxyVortexRotate 120s linear infinite;
    opacity: 0.85;
}

/* Cosmic Nebula & Vortex Keyframes */
@keyframes cosmicNebulaDrift {
    0% {
        transform: scale(1) translate(0, 0);
        opacity: 0.8;
    }
    50% {
        transform: scale(1.08) translate(-15px, 20px);
        opacity: 1;
    }
    100% {
        transform: scale(1.03) translate(20px, -15px);
        opacity: 0.85;
    }
}

@keyframes galaxyVortexRotate {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

/* Ensure app content stays in foreground above space layers */
.main, header, [data-testid="stSidebar"], .stApp > div {
    position: relative;
    z-index: 1;
}

/* ───────────────────────── MODERN OBSERVATORY HUD UI ───────────────────────── */

/* Sidebar: Deep Obsidian Glass */
[data-testid="stSidebar"] {
    background: rgba(5, 7, 11, 0.85) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label {
    color: #94A3B8 !important;
    font-size: 0.88rem !important;
    font-weight: 500;
}

/* Typography Hierarchy */
h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
}

p, span, div {
    color: #94A3B8;
}

/* Metric Cards: Translucent Observatory HUD Tiles */
[data-testid="metric-container"] {
    background: rgba(12, 16, 26, 0.7) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(56, 189, 248, 0.4) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    background: rgba(16, 22, 36, 0.8) !important;
    border-color: rgba(56, 189, 248, 0.6) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(56, 189, 248, 0.15) !important;
}

[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

/* Navigation Segment: Sleek Observatory Dock */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10, 14, 23, 0.75) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    color: #94A3B8 !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #F8FAFC !important;
    background: rgba(255, 255, 255, 0.05) !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(30, 41, 59, 0.7) !important;
    color: #38BDF8 !important;
    font-weight: 600 !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3), 0 0 12px rgba(56, 189, 248, 0.15) !important;
}

/* Interactive Buttons: Glowing Starlight Pills */
.stButton > button {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(56, 189, 248, 0.5) !important;
    border-radius: 9999px !important;
    padding: 8px 24px !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.3) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
    border-color: #38BDF8 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(56, 189, 248, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(0);
}

/* Dropdowns & Selectboxes */
div[data-baseweb="select"] > div {
    background: rgba(12, 16, 26, 0.75) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 14px rgba(56, 189, 248, 0.25) !important;
}

/* Data Table Surface */
div[data-testid="stDataFrame"] {
    background: rgba(12, 16, 26, 0.6) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
}

/* Dividers */
hr {
    border: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.25), transparent) !important;
    margin: 24px 0 !important;
}

/* Alerts / Expanders */
.stAlert {
    background: rgba(12, 16, 26, 0.7) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #F8FAFC !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] {
    background: rgba(12, 16, 26, 0.65) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCIENTIFIC PLOT PALETTE: Deep Space High-Resolution Spectrum
# ─────────────────────────────────────────────────────────────────────────────
COLORS = dict(
    obs="#38BDF8",        # Electric Cyan (Observed rotational velocity)
    bar="#A78BFA",        # Nebula Violet (Baryonic visible matter curve)
    gas="#34D399",        # Aurora Emerald (Gas component)
    disk="#FBBF24",       # Golden Star Amber (Stellar disk)
    bulge="#F472B6",      # Rose Quartz (Bulge component)
    dark="#60A5FA",       # Pulsar Blue (Inferred dark matter mass profile)
    anomaly="#FB923C",    # Solar Coral (Kinematic anomalies)
)

def _celestial_theme(fig, axes):
    """Styles matplotlib plots with Deep Space Obsidian backdrop and clean telemetry grid."""
    fig.patch.set_facecolor("#080B12")
    for ax in (axes if hasattr(axes, "__iter__") else [axes]):
        ax.set_facecolor("#0C101A")
        ax.tick_params(colors="#94A3B8", labelsize=9)
        ax.xaxis.label.set_color("#CBD5E1")
        ax.yaxis.label.set_color("#CBD5E1")
        ax.title.set_color("#F8FAFC")
        for s in ax.spines.values():
            s.set_edgecolor("#1E2638")
            s.set_linewidth(1.0)
        ax.grid(True, color="#1E2638", alpha=0.6, linestyle="--", linewidth=0.7)

LEG = dict(facecolor="#0C101A", edgecolor="#1E2638", labelcolor="#F8FAFC")

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
    st.markdown("""
    <div style="padding: 6px 0 10px;">
        <span style="font-size: 0.72rem; font-weight: 700; color: #38BDF8; letter-spacing: 0.1em; text-transform: uppercase;">OBSERVATORY CONTROL</span>
        <h2 style="font-size: 1.6rem; margin: 4px 0 0; color: #FFFFFF;">COSMATRIX</h2>
        <span style="font-size: 0.8rem; color: #64748B;">Galactic Dynamics Platform</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"**Archive:** {len(glist)} SPARC Galaxies")
    st.markdown("**Catalog:** Lelli et al. 2016")
    st.markdown("---")

    selected_galaxy = st.selectbox(
        "Target Galaxy",
        glist,
        index=glist.index("CamB") if "CamB" in glist else 0,
        help="Select a galaxy to analyze observational rotation curves and dark matter signatures",
    )

    compare_galaxies = st.multiselect(
        "Cohort Comparison",
        glist,
        default=glist[:3] if len(glist) >= 3 else glist,
        max_selections=8,
        help="Select up to 8 galaxies for side-by-side behavioral comparison",
    )

    st.markdown("---")
    show_error_bars = st.checkbox("Observational Uncertainties (errV)", True)
    show_components = st.checkbox("Baryonic Components (Gas/Disk/Bulge)", True)
    anomaly_method = st.radio(
        "Anomaly Detection Criteria",
        ["Both (Z-score & IQR)", "Z-score Only", "IQR Only", "None"],
    )
    st.markdown("---")
    st.caption(
        "Collaborators:\n"
        "• Purva: SPARC Data Collection & Preprocessing\n"
        "• Suyash: Physics Models & Kinematic Analytics\n"
        "• Bhavya: Data Bridge & Interactive Dashboard"
    )

# ─────────────────────────────────────────────────────────────────────────────
# EDITORIAL OBSERVATORY HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 8px 0 18px;'>
    <div style="font-size: 0.78rem; font-weight: 700; color: #38BDF8; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 6px;">
        SPARC OBSERVATIONAL ASTROPHYSICS ARCHIVE
    </div>
    <h1 style='font-size: 3.2rem; margin: 2px 0 10px; font-weight: 800; color: #F8FAFC; line-height: 1.1; letter-spacing: -0.035em;'>
        COSMATRIX
    </h1>
    <p style='color: #94A3B8; font-size: 1.15rem; font-weight: 400; margin: 0 0 14px; max-width: 820px; line-height: 1.6;'>
        An Intelligent Dark Matter &amp; Galactic Behaviour Analytics Platform uncovering non-baryonic gravitational signatures across 175 precision SPARC rotation curves.
    </p>
    <div style="display: flex; gap: 20px; color: #64748B; font-size: 0.85rem; font-weight: 600; padding: 4px 0;">
        <span><strong style="color: #38BDF8;">175</strong> GALAXIES</span>
        <span>•</span>
        <span><strong style="color: #A78BFA;">3.6μm</strong> SPITZER PHOTOMETRY</span>
        <span>•</span>
        <span><strong style="color: #34D399;">5</strong> ANALYTICS ENGINES</span>
        <span>•</span>
        <span><strong style="color: #F8FAFC;">100%</strong> INTEGRATED PIPELINE</span>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Overview Metrics ──────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Catalog Galaxies", len(glist))
if not meta.empty and "D" in meta.columns:
    avg_dist = pd.to_numeric(meta["D"], errors="coerce").mean()
    c2.metric("Mean Distance", f"{avg_dist:.1f} Mpc")
else:
    c2.metric("Mean Distance", "N/A")

if not meta.empty and "Vflat" in meta.columns:
    vflat_mean = pd.to_numeric(meta["Vflat"], errors="coerce").replace(0, np.nan).mean()
    c3.metric("Mean V_flat", f"{vflat_mean:.0f} km/s")
else:
    c3.metric("Mean V_flat", "N/A")

if not meta.empty and "T" in meta.columns:
    morphologies = pd.to_numeric(meta["T"], errors="coerce").dropna().nunique()
    c4.metric("Morphology Types", morphologies)
else:
    c4.metric("Morphology Types", "N/A")
c5.metric("Analytics Engines", "5 Active")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔭 Rotation Curves",
    "⚖️ Mass & Dark Matter",
    "📊 Statistical Metrics",
    "🚨 Kinematic Anomalies",
    "🌐 Galaxy Cohort",
    "📋 SPARC Metadata",
])

# ══════════════════ TAB 1 — ROTATION CURVE ═══════════════════════════════════
with tab1:
    st.subheader(f"Kinematic Rotation Curve: {selected_galaxy}")
    try:
        df = _analyse(selected_galaxy)
        if not meta.empty:
            gm = meta[meta["Galaxy"].astype(str).str.strip() == selected_galaxy]
            if not gm.empty:
                gm = gm.iloc[0]
                mc1, mc2, mc3, mc4 = st.columns(4)
                mc1.metric("Distance (D)", f"{gm['D']:.2f} Mpc" if pd.notna(gm.get("D")) else "N/A")
                mc2.metric("Inclination (i)", f"{gm['Inc']:.0f}°" if pd.notna(gm.get("Inc")) else "N/A")
                mc3.metric(
                    "Asymptotic V_flat",
                    f"{gm['Vflat']:.0f} km/s"
                    if pd.notna(gm.get("Vflat")) and gm["Vflat"] > 0
                    else "N/A",
                )
                mc4.metric("Hubble Stage (T)", f"{int(gm['T'])}" if pd.notna(gm.get("T")) else "N/A")

        fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
        _celestial_theme(fig, axes)

        if anomaly_method == "Both (Z-score & IQR)":
            anom_mask = df["Final_Anomaly"]
        elif anomaly_method == "Z-score Only":
            anom_mask = df["Zscore_Anomaly"]
        elif anomaly_method == "IQR Only":
            anom_mask = df["IQR_Anomaly"]
        else:
            anom_mask = pd.Series(False, index=df.index)

        normal = df[~anom_mask]
        anomalies = df[anom_mask]

        # Left: Rotation Curve
        ax = axes[0]
        if show_error_bars:
            ax.errorbar(
                normal["Radius_kpc"],
                normal["V_obs_km_s"],
                yerr=normal.get("errV", 0),
                fmt="o",
                color=COLORS["obs"],
                ecolor="#64748B",
                capsize=3,
                label="Observed Velocity (V_obs)",
                markersize=5,
                alpha=0.95,
            )
        else:
            ax.scatter(
                normal["Radius_kpc"],
                normal["V_obs_km_s"],
                color=COLORS["obs"],
                label="Observed Velocity (V_obs)",
                s=32,
                alpha=0.95,
            )
        ax.plot(
            df["Radius_kpc"],
            df["V_bar_km_s"],
            color=COLORS["bar"],
            lw=2.4,
            label="Baryonic Visible Matter (V_bar)",
        )
        if show_components:
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
        if not anomalies.empty:
            ax.scatter(
                anomalies["Radius_kpc"],
                anomalies["V_obs_km_s"],
                color=COLORS["anomaly"],
                s=85,
                zorder=5,
                marker="D",
                label=f"Flagged Points ({len(anomalies)})",
            )
        ax.set_xlabel("Galactocentric Radius (kpc)")
        ax.set_ylabel("Rotational Velocity (km/s)")
        ax.set_title(f"Velocity Distribution — {selected_galaxy}")
        ax.legend(fontsize=8, **LEG)

        # Right: Velocity Residual (Dark Matter Signature)
        ax2 = axes[1]
        ax2.axhline(0, color="#64748B", lw=1.0, ls="--")
        ax2.scatter(
            df["Radius_kpc"],
            df["Velocity_Difference_km_s"],
            color=COLORS["obs"],
            s=30,
            alpha=0.9,
            label="Residual ΔV (V_obs − V_bar)",
        )
        ax2.fill_between(
            df["Radius_kpc"],
            df["Velocity_Difference_km_s"],
            alpha=0.18,
            color=COLORS["obs"],
        )
        ax2.set_xlabel("Galactocentric Radius (kpc)")
        ax2.set_ylabel("Velocity Excess ΔV (km/s)")
        ax2.set_title(f"Non-Baryonic Velocity Discrepancy — {selected_galaxy}")
        ax2.legend(fontsize=8, **LEG)
        st.pyplot(fig)
        plt.close()

        km1, km2, km3, km4 = st.columns(4)
        km1.metric("Peak V_obs", f"{df['V_obs_km_s'].max():.1f} km/s")
        km2.metric("Peak V_bar", f"{df['V_bar_km_s'].max():.1f} km/s")
        km3.metric("Mean Velocity Excess", f"{df['Velocity_Difference_km_s'].mean():.1f} km/s")
        km4.metric("Kinematic Inliers", f"{len(df) - int(df['Final_Anomaly'].sum())}/{len(df)}")

        with st.expander("Explore Processed Observational Data"):
            st.dataframe(
                df.style.format({c: "{:.3f}" for c in df.select_dtypes("float").columns}),
                use_container_width=True,
            )
    except Exception as e:
        st.error(f"Error computing rotation curves: {e}")

# ══════════════════ TAB 2 — MASS ANALYSIS ════════════════════════════════════
with tab2:
    st.subheader(f"Gravitational Mass Profile: {selected_galaxy}")
    try:
        df = _analyse(selected_galaxy)
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
        _celestial_theme(fig, axes)

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
            alpha=0.18,
            color=COLORS["dark"],
        )
        ax.set_xlabel("Radius (kpc)")
        ax.set_ylabel("Enclosed Mass (×10¹⁰ M☉)")
        ax.set_title(f"Cumulative Mass Profiles — {selected_galaxy}")
        ax.legend(fontsize=8, **LEG)

        ax2 = axes[1]
        frac = (df["Additional_Mass_Solar"].fillna(0) / df["Total_Mass_Solar"] * 100).clip(0, 100)
        ax2.plot(df["Radius_kpc"], frac, color=COLORS["dark"], lw=2.2, label="Dark Matter Ratio")
        ax2.fill_between(df["Radius_kpc"], frac, alpha=0.2, color=COLORS["dark"])
        ax2.set_xlabel("Radius (kpc)")
        ax2.set_ylabel("Dark Matter Ratio (%)")
        ax2.set_title(f"Dark Matter Fraction Radial Gradient — {selected_galaxy}")
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
    except Exception as e:
        st.error(f"Error computing mass estimates: {e}")

# ══════════════════ TAB 3 — STATISTICS ═══════════════════════════════════════
with tab3:
    st.subheader(f"Statistical Modeling & Diagnostics: {selected_galaxy}")
    try:
        df = _analyse(selected_galaxy)
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
            _celestial_theme(fig, ax)
            sns.heatmap(
                corr,
                annot=True,
                fmt=".2f",
                cmap="mako",
                ax=ax,
                linewidths=0.5,
                linecolor="#1E2536",
                cbar_kws={"shrink": 0.8},
                annot_kws={"size": 8, "color": "#F8FAFC"},
            )
            ax.set_title(f"Parameter Correlation — {selected_galaxy}", pad=10)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        st.markdown("##### Empirical Velocity Distributions")
        fig2, axes2 = plt.subplots(1, 3, figsize=(14, 4))
        _celestial_theme(fig2, axes2)
        for ax_, col_, clr_, lbl_ in zip(
            axes2,
            ["V_obs_km_s", "V_bar_km_s", "Velocity_Difference_km_s"],
            [COLORS["obs"], COLORS["bar"], COLORS["dark"]],
            ["V_obs (km/s)", "V_bar (km/s)", "Residual ΔV (km/s)"],
        ):
            ax_.hist(df[col_].dropna(), bins=14, color=clr_, alpha=0.85, edgecolor="#080B12")
            ax_.axvline(df[col_].mean(), color="#F8FAFC", ls="--", lw=1.2, label="Mean")
            ax_.set_xlabel(lbl_)
            ax_.set_ylabel("Frequency")
            ax_.set_title(lbl_)
            ax_.legend(fontsize=7, **LEG)
        st.pyplot(fig2)
        plt.close()
    except Exception as e:
        st.error(f"Error computing statistics: {e}")

# ══════════════════ TAB 4 — ANOMALY DETECTION ════════════════════════════════
with tab4:
    st.subheader(f"Kinematic Anomaly Detection: {selected_galaxy}")
    try:
        df = _analyse(selected_galaxy)
        zc = int(df["Zscore_Anomaly"].sum())
        ic = int(df["IQR_Anomaly"].sum())
        fc = int(df["Final_Anomaly"].sum())
        tot = len(df)

        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Evaluated Data Points", tot)
        a2.metric("Z-Score Threshold Exceeded", zc)
        a3.metric("IQR Boundary Outliers", ic)
        a4.metric("Confirmed Dual Anomalies", fc, delta=f"{fc/tot*100:.1f}%", delta_color="off")

        fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
        _celestial_theme(fig, axes)

        # Z-Score
        ax = axes[0]
        nm = ~df["Zscore_Anomaly"]
        ax.scatter(
            df.loc[nm, "Radius_kpc"],
            df.loc[nm, "Z_Score"],
            color=COLORS["obs"],
            s=30,
            alpha=0.85,
            label="In-Distribution Data",
        )
        if df["Zscore_Anomaly"].any():
            ax.scatter(
                df.loc[df["Zscore_Anomaly"], "Radius_kpc"],
                df.loc[df["Zscore_Anomaly"], "Z_Score"],
                color=COLORS["anomaly"],
                s=90,
                marker="D",
                zorder=5,
                label=f"Z-Score Outlier (|Z| > 3)",
            )
        ax.axhline(3, color="#94A3B8", ls="--", lw=1, label="+3σ Limit")
        ax.axhline(-3, color="#94A3B8", ls="--", lw=1, label="−3σ Limit")
        ax.set_xlabel("Radius (kpc)")
        ax.set_ylabel("Standardized Z-Score")
        ax.set_title(f"Standardized Residual Dispersion — {selected_galaxy}")
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
            color=COLORS["obs"],
            s=30,
            alpha=0.85,
            label="Quartile Inliers",
        )
        if df["IQR_Anomaly"].any():
            ax2.scatter(
                df.loc[df["IQR_Anomaly"], "Radius_kpc"],
                r[df["IQR_Anomaly"]],
                color=COLORS["anomaly"],
                s=90,
                marker="D",
                zorder=5,
                label=f"Tukey Outliers ({ic})",
            )
        ax2.axhline(ub, color="#94A3B8", ls="--", lw=1, label=f"Upper Bound ({ub:.1f})")
        ax2.axhline(lb, color="#94A3B8", ls=":", lw=1, label=f"Lower Bound ({lb:.1f})")
        ax2.set_xlabel("Radius (kpc)")
        ax2.set_ylabel("Residual ΔV (km/s)")
        ax2.set_title(f"Interquartile Range Bounds — {selected_galaxy}")
        ax2.legend(fontsize=7, **LEG)
        st.pyplot(fig)
        plt.close()

        if fc > 0:
            st.info(
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
            st.success("No significant kinematic anomalies detected under standard criteria.")
    except Exception as e:
        st.error(f"Error executing anomaly detection: {e}")

# ══════════════════ TAB 5 — GALAXY COMPARISON ════════════════════════════════
with tab5:
    st.subheader("Multi-Galaxy Kinematic Cohort Comparison")
    if len(compare_galaxies) < 2:
        st.info("Select at least 2 galaxies from the sidebar to generate cohort comparisons.")
    else:
        try:
            cdf = _multi(tuple(compare_galaxies))
            cohort_palette = ["#38BDF8", "#A78BFA", "#34D399", "#FBBF24", "#F472B6", "#60A5FA", "#FB923C", "#E2E8F0"]
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            _celestial_theme(fig, axes.flatten())

            # Rotation curves
            ax = axes[0, 0]
            for i, g in enumerate(compare_galaxies):
                gdf = cdf[cdf["Galaxy"] == g]
                ax.plot(
                    gdf["Radius_kpc"],
                    gdf["V_obs_km_s"],
                    color=cohort_palette[i % len(cohort_palette)],
                    lw=2.0,
                    label=g,
                    alpha=0.9,
                )
            ax.set_xlabel("Radius (kpc)")
            ax.set_ylabel("V_obs (km/s)")
            ax.set_title("Observed Rotation Velocity Curves")
            ax.legend(fontsize=7, **LEG)

            # V_obs vs V_bar
            ax2 = axes[0, 1]
            for i, g in enumerate(compare_galaxies):
                gdf = cdf[cdf["Galaxy"] == g]
                ax2.scatter(
                    gdf["V_bar_km_s"],
                    gdf["V_obs_km_s"],
                    color=cohort_palette[i % len(cohort_palette)],
                    s=24,
                    label=g,
                    alpha=0.85,
                )
            vm = cdf[["V_obs_km_s", "V_bar_km_s"]].max().max()
            ax2.plot([0, vm], [0, vm], color="#64748B", ls="--", lw=1, alpha=0.6, label="1:1 Ratio (No DM)")
            ax2.set_xlabel("V_bar (km/s)")
            ax2.set_ylabel("V_obs (km/s)")
            ax2.set_title("Observed vs Baryonic Dynamic Ratio")
            ax2.legend(fontsize=7, **LEG)

            # Residuals
            ax3 = axes[1, 0]
            for i, g in enumerate(compare_galaxies):
                gdf = cdf[cdf["Galaxy"] == g]
                ax3.plot(
                    gdf["Radius_kpc"],
                    gdf["Velocity_Difference_km_s"],
                    color=cohort_palette[i % len(cohort_palette)],
                    lw=2.0,
                    label=g,
                    alpha=0.9,
                )
            ax3.axhline(0, color="#64748B", ls="--", lw=1, alpha=0.6)
            ax3.set_xlabel("Radius (kpc)")
            ax3.set_ylabel("Velocity Excess ΔV (km/s)")
            ax3.set_title("Kinematic Excess Profiles")
            ax3.legend(fontsize=7, **LEG)

            # DM fraction bar chart
            ax4 = axes[1, 1]
            names_, fracs_, clrs_ = [], [], []
            for i, g in enumerate(compare_galaxies):
                gdf = cdf[cdf["Galaxy"] == g]
                if gdf.empty:
                    continue
                lr = gdf.iloc[-1]
                dm = lr.get("Additional_Mass_Solar", np.nan)
                f = max((dm / lr["Total_Mass_Solar"] * 100) if pd.notna(dm) and lr["Total_Mass_Solar"] > 0 else 0, 0)
                names_.append(g)
                fracs_.append(f)
                clrs_.append(cohort_palette[i % len(cohort_palette)])
            bars = ax4.barh(names_, fracs_, color=clrs_, alpha=0.9, edgecolor="#080B12")
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
                    color="#F8FAFC",
                )
            plt.tight_layout(pad=2.2)
            st.pyplot(fig)
            plt.close()

            st.markdown("##### Cohort Analytical Summary")
            rows = []
            for g in compare_galaxies:
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
with tab6:
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
        _celestial_theme(fig, axes.flatten())

        d.hist(ax=axes[0, 0], bins=24, color=COLORS["obs"], edgecolor="#080B12", alpha=0.9)
        axes[0, 0].set_xlabel("Distance (Mpc)")
        axes[0, 0].set_ylabel("Galaxy Count")
        axes[0, 0].set_title("Distance Distribution")

        vf = pd.to_numeric(meta["Vflat"], errors="coerce").replace(0, np.nan).dropna()
        vf.hist(ax=axes[0, 1], bins=24, color=COLORS["bar"], edgecolor="#080B12", alpha=0.9)
        axes[0, 1].set_xlabel("Flat Rotation Velocity (km/s)")
        axes[0, 1].set_ylabel("Galaxy Count")
        axes[0, 1].set_title("V_flat Characteristic Velocity Distribution")

        t_ = pd.to_numeric(meta["T"], errors="coerce").dropna().value_counts().sort_index()
        axes[1, 0].bar(t_.index, t_.values, color=COLORS["gas"], alpha=0.9, edgecolor="#080B12")
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
            cmap="viridis",
            s=34,
            alpha=0.9,
            edgecolors="#080B12",
        )
        cbar = plt.colorbar(sc, ax=axes[1, 1])
        cbar.set_label("Hubble Type (T)", color="#94A3B8")
        cbar.ax.yaxis.set_tick_params(color="#94A3B8")
        plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="#94A3B8")
        axes[1, 1].set_xlabel("Distance (Mpc)")
        axes[1, 1].set_ylabel("V_flat (km/s)")
        axes[1, 1].set_title("Distance vs Characteristic Rotational Velocity")
        plt.tight_layout(pad=2.2)
        st.pyplot(fig)
        plt.close()

        with st.expander("View Complete SPARC Catalog Metadata"):
            st.dataframe(meta, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# EDITORIAL FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; font-size: 0.85rem; padding: 14px 0;'>
    <b>COSMATRIX</b> — An Intelligent Dark Matter &amp; Galactic Behaviour Analytics Platform<br>
    Observational Data: SPARC (Lelli et al. 2016) • Theme: Animated Galactic Vortex &amp; Cosmic Glass HUD<br>
    Purva (Data Pipeline) • Suyash (Physics Modeling) • Bhavya (Dashboard &amp; Integration)
</div>
""", unsafe_allow_html=True)
