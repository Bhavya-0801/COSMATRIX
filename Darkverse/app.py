"""
DARKVERSE — Interactive Dashboard  (Person 3)
Fully integrated Streamlit app connecting Person 1 & Person 2 modules.

Deploy on Streamlit Community Cloud:
  Main file path: Darkverse/app.py

Run locally:
  streamlit run app.py
"""

import sys
from pathlib import Path

# ── Make sure sibling packages are importable when running from repo root ──
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

# ── DARKVERSE modules ─────────────────────────────────────────────────────────
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
    page_title="DARKVERSE",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DARK SPACE THEME
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0a0a1a 0%,#0d1b2a 50%,#0a0a1a 100%);color:#e0e0ff}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1b2a,#0a0f1e);border-right:1px solid #1e3a5f}
h1,h2,h3{color:#7ec8e3!important}
h1{text-shadow:0 0 20px #7ec8e3}
[data-testid="metric-container"]{background:rgba(14,30,60,.7);border:1px solid #1e4a7f;border-radius:8px;padding:12px}
[data-testid="metric-container"] [data-testid="stMetricLabel"]{color:#a0c4e8!important}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#7ec8e3!important}
.stTabs [data-baseweb="tab-list"]{background-color:rgba(10,20,40,.8);border-radius:8px}
.stTabs [data-baseweb="tab"]{color:#a0c4e8}
.stTabs [aria-selected="true"]{background-color:rgba(30,74,127,.5);color:#7ec8e3!important}
.stButton>button{background:linear-gradient(135deg,#1e3a5f,#0d4f8a);color:#e0e0ff;border:1px solid #3a7abd;border-radius:6px}
.stButton>button:hover{background:linear-gradient(135deg,#0d4f8a,#1565c0);border-color:#7ec8e3}
hr{border-color:#1e3a5f}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
COLORS = dict(obs="#00bfff", bar="#ff6b6b", gas="#51cf66",
              disk="#ffd43b", bulge="#cc5de8", dark="#ff922b", anomaly="#ff4757")

def _dark(fig, axes):
    fig.patch.set_facecolor("#0a0a1a")
    for ax in (axes if hasattr(axes, "__iter__") else [axes]):
        ax.set_facecolor("#0a0f1e")
        ax.tick_params(colors="#a0c4e8")
        ax.xaxis.label.set_color("#a0c4e8")
        ax.yaxis.label.set_color("#a0c4e8")
        ax.title.set_color("#7ec8e3")
        for s in ax.spines.values(): s.set_edgecolor("#1e3a5f")
        ax.grid(True, color="#1e3a5f", alpha=0.4)

LEG = dict(facecolor="#0a0f1e", edgecolor="#1e3a5f", labelcolor="#e0e0ff")

@st.cache_data
def _galaxies(): return list_available_galaxies()

@st.cache_data
def _meta():
    try:    return load_galaxy_metadata()
    except: return pd.DataFrame()

@st.cache_data
def _analyse(name):
    df = load_galaxy_for_analysis(name)
    for fn in [calculate_rotation_curves, calculate_velocity_difference,
               calculate_percentage_difference, estimate_galaxy_mass, analyze_anomalies]:
        df = fn(df)
    return df

@st.cache_data
def _multi(names_tuple):
    df = load_multiple_galaxies(list(names_tuple))
    for fn in [calculate_rotation_curves, calculate_velocity_difference,
               calculate_percentage_difference, estimate_galaxy_mass, analyze_anomalies]:
        df = fn(df)
    return df

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
glist = _galaxies()
meta  = _meta()

with st.sidebar:
    st.markdown("## 🌌 DARKVERSE")
    st.markdown("*Dark Matter & Galactic Behaviour Analytics*")
    st.markdown("---")
    st.markdown(f"**📊 Dataset:** {len(glist)} SPARC galaxies")
    st.markdown("**🔭 Source:** Lelli et al. 2016")
    st.markdown("---")

    st.markdown("### 🔭 Galaxy Explorer")
    sel = st.selectbox("Select Galaxy", glist,
                       index=glist.index("CamB") if "CamB" in glist else 0)

    st.markdown("### 📡 Multi-Galaxy Compare")
    cmp = st.multiselect("Compare Galaxies", glist, default=glist[:3], max_selections=8)

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    show_err   = st.checkbox("Show Error Bars", True)
    show_comp  = st.checkbox("Show Velocity Components", True)
    anom_mode  = st.radio("Anomaly Highlight",
                          ["Both (Z-score & IQR)","Z-score Only","IQR Only","None"])
    st.markdown("---")
    st.caption("Person 3 — Integration & Dashboard\nPerson 1 — Data Pipeline\nPerson 2 — Analysis Modules")

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:20px 0 10px'>
<h1 style='font-size:3em;letter-spacing:.1em'>🌌 DARKVERSE</h1>
<p style='color:#a0c4e8;font-size:1.1em'>
An Intelligent Dark Matter &amp; Galactic Behaviour Analytics Platform</p>
</div>""", unsafe_allow_html=True)
st.markdown("---")

# ── Overview metrics ──────────────────────────────────────────────────────────
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("🌠 Galaxies", len(glist))
if not meta.empty:
    d  = pd.to_numeric(meta.get("D"), errors="coerce")
    vf = pd.to_numeric(meta.get("Vflat"), errors="coerce").replace(0,np.nan)
    t  = pd.to_numeric(meta.get("T"), errors="coerce")
    c2.metric("📏 Avg Distance", f"{d.mean():.1f} Mpc"  if d.notna().any() else "N/A")
    c3.metric("⚡ Avg V_flat",   f"{vf.mean():.0f} km/s" if vf.notna().any() else "N/A")
    c4.metric("🌀 Morphologies", f"{t.dropna().nunique()}" if t.notna().any() else "N/A")
else:
    c2.metric("📏 Avg Distance","N/A"); c3.metric("⚡ Avg V_flat","N/A"); c4.metric("🌀 Morphologies","N/A")
c5.metric("🔬 Modules", "5")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
t1,t2,t3,t4,t5,t6 = st.tabs([
    "🔭 Rotation Curve","⚖️ Mass Analysis","📊 Statistics",
    "🚨 Anomaly Detection","🌐 Galaxy Comparison","📋 Dataset Overview"])

# ══════════════════ TAB 1 — ROTATION CURVE ═══════════════════════════════════
with t1:
    st.header(f"🔭 Rotation Curve: {sel}")
    try:
        df = _analyse(sel)
        # metadata row
        if not meta.empty:
            gm = meta[meta["Galaxy"].astype(str).str.strip()==sel]
            if not gm.empty:
                gm = gm.iloc[0]
                m1,m2,m3,m4 = st.columns(4)
                m1.metric("Distance",    f"{gm['D']:.2f} Mpc"   if pd.notna(gm.get('D'))     else "N/A")
                m2.metric("Inclination", f"{gm['Inc']:.0f}°"    if pd.notna(gm.get('Inc'))   else "N/A")
                m3.metric("V_flat",      f"{gm['Vflat']:.0f} km/s" if pd.notna(gm.get('Vflat')) and gm['Vflat']>0 else "N/A")
                m4.metric("Type (T)",    f"{int(gm['T'])}"       if pd.notna(gm.get('T'))     else "N/A")

        fig,axes = plt.subplots(1,2,figsize=(14,5)); _dark(fig,axes)

        # anomaly masks
        if   anom_mode=="Both (Z-score & IQR)": amask = df["Final_Anomaly"]
        elif anom_mode=="Z-score Only":          amask = df["Zscore_Anomaly"]
        elif anom_mode=="IQR Only":              amask = df["IQR_Anomaly"]
        else:                                    amask = pd.Series(False, index=df.index)
        norm = df[~amask]; anom = df[amask]

        ax = axes[0]
        if show_err:
            ax.errorbar(norm["Radius_kpc"],norm["V_obs_km_s"],yerr=norm.get("errV",0),
                        fmt="o",color=COLORS["obs"],capsize=3,label="V_obs",markersize=4,alpha=.85)
        else:
            ax.scatter(norm["Radius_kpc"],norm["V_obs_km_s"],color=COLORS["obs"],label="V_obs",s=25,alpha=.85)
        ax.plot(df["Radius_kpc"],df["V_bar_km_s"],color=COLORS["bar"],lw=2,label="V_bar (Baryonic)")
        if show_comp:
            ax.plot(df["Radius_kpc"],df["V_gas_km_s"],  color=COLORS["gas"],  lw=1,ls="--",label="V_gas",  alpha=.7)
            ax.plot(df["Radius_kpc"],df["V_disk_km_s"], color=COLORS["disk"], lw=1,ls="--",label="V_disk", alpha=.7)
            ax.plot(df["Radius_kpc"],df["V_bulge_km_s"],color=COLORS["bulge"],lw=1,ls="--",label="V_bulge",alpha=.7)
        if not anom.empty:
            ax.scatter(anom["Radius_kpc"],anom["V_obs_km_s"],
                       color=COLORS["anomaly"],s=80,zorder=5,marker="*",label=f"Anomalies ({len(anom)})")
        ax.set_xlabel("Radius (kpc)"); ax.set_ylabel("Velocity (km/s)")
        ax.set_title(f"Rotation Curve: {sel}"); ax.legend(fontsize=7,**LEG)

        ax2 = axes[1]
        ax2.axhline(0,color="#fff",lw=.8,ls="--",alpha=.5)
        ax2.scatter(df["Radius_kpc"],df["Velocity_Difference_km_s"],color=COLORS["obs"],s=25,alpha=.75)
        ax2.fill_between(df["Radius_kpc"],df["Velocity_Difference_km_s"],alpha=.15,color=COLORS["obs"])
        ax2.set_xlabel("Radius (kpc)"); ax2.set_ylabel("Residual (km/s)")
        ax2.set_title(f"Velocity Residual: {sel}")
        st.pyplot(fig); plt.close()

        km1,km2,km3,km4 = st.columns(4)
        km1.metric("Max V_obs",    f"{df['V_obs_km_s'].max():.1f} km/s")
        km2.metric("Max V_bar",    f"{df['V_bar_km_s'].max():.1f} km/s")
        km3.metric("Mean Residual",f"{df['Velocity_Difference_km_s'].mean():.1f} km/s")
        km4.metric("Anomalies",    f"{df['Final_Anomaly'].sum()}")

        with st.expander("📄 Raw Data"):
            st.dataframe(df.style.format({c:"{:.3f}" for c in df.select_dtypes("float").columns}),
                         use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

# ══════════════════ TAB 2 — MASS ANALYSIS ════════════════════════════════════
with t2:
    st.header(f"⚖️ Mass Analysis: {sel}")
    try:
        df = _analyse(sel)
        fig,axes = plt.subplots(1,2,figsize=(14,5)); _dark(fig,axes)

        ax = axes[0]
        ax.plot(df["Radius_kpc"],df["Total_Mass_Solar"]/1e10,     color=COLORS["obs"], lw=2,label="Total Mass")
        ax.plot(df["Radius_kpc"],df["Baryonic_Mass_Solar"]/1e10,  color=COLORS["bar"], lw=2,label="Baryonic Mass")
        dm = df["Additional_Mass_Solar"].dropna()
        ax.plot(df.loc[dm.index,"Radius_kpc"],dm/1e10,
                color=COLORS["dark"],lw=2,ls="--",label="Dark Matter Proxy")
        ax.fill_between(df.loc[dm.index,"Radius_kpc"],dm/1e10,alpha=.2,color=COLORS["dark"])
        ax.set_xlabel("Radius (kpc)"); ax.set_ylabel("Mass (×10¹⁰ M☉)")
        ax.set_title(f"Mass Profiles: {sel}"); ax.legend(fontsize=8,**LEG)

        ax2 = axes[1]
        frac = (df["Additional_Mass_Solar"].fillna(0)/df["Total_Mass_Solar"]*100).clip(0,100)
        ax2.plot(df["Radius_kpc"],frac,color=COLORS["dark"],lw=2)
        ax2.fill_between(df["Radius_kpc"],frac,alpha=.3,color=COLORS["dark"])
        ax2.set_xlabel("Radius (kpc)"); ax2.set_ylabel("Dark Matter Fraction (%)")
        ax2.set_title(f"DM Fraction vs Radius: {sel}"); ax2.set_ylim(0,100)
        st.pyplot(fig); plt.close()

        last = df.iloc[-1]
        mm1,mm2,mm3,mm4 = st.columns(4)
        mm1.metric("Total Mass",    f"{last['Total_Mass_Solar']/1e10:.2f} ×10¹⁰ M☉")
        mm2.metric("Baryonic Mass", f"{last['Baryonic_Mass_Solar']/1e10:.2f} ×10¹⁰ M☉")
        dm_v = last.get("Additional_Mass_Solar")
        mm3.metric("DM Proxy",      f"{dm_v/1e10:.2f} ×10¹⁰ M☉" if pd.notna(dm_v) and dm_v else "N/A")
        mm4.metric("DM Fraction",   f"{dm_v/last['Total_Mass_Solar']*100:.1f}%" if pd.notna(dm_v) and dm_v else "0.0%")

        with st.expander("📄 Mass Table"):
            cols = ["Radius_kpc","V_obs_km_s","V_bar_km_s","Total_Mass_Solar","Baryonic_Mass_Solar","Additional_Mass_Solar"]
            st.dataframe(df[cols].style.format("{:.3e}",
                subset=["Total_Mass_Solar","Baryonic_Mass_Solar","Additional_Mass_Solar"]
            ).format("{:.3f}",subset=["Radius_kpc","V_obs_km_s","V_bar_km_s"]),use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

# ══════════════════ TAB 3 — STATISTICS ═══════════════════════════════════════
with t3:
    st.header(f"📊 Statistical Analysis: {sel}")
    try:
        df = _analyse(sel)
        desc = calculate_descriptive_statistics(df)
        corr = calculate_correlation(df)
        vs   = calculate_velocity_statistics(df)

        st.subheader("⚡ Velocity Residual Metrics")
        v1,v2,v3,v4 = st.columns(4)
        v1.metric("Mean Residual",        f"{vs['Mean_Residual']:.2f} km/s")
        v2.metric("MAE",                  f"{vs['MAE']:.2f} km/s")
        v3.metric("RMSE",                 f"{vs['RMSE']:.2f} km/s")
        v4.metric("Corr(V_obs,V_bar)",    f"{vs['Correlation']:.4f}")

        ca,cb = st.columns(2)
        with ca:
            st.subheader("📋 Descriptive Statistics")
            st.dataframe(pd.DataFrame(desc).T.style.format("{:.3f}"),use_container_width=True)
        with cb:
            st.subheader("🔗 Correlation Heatmap")
            fig,ax = plt.subplots(figsize=(6,4)); _dark(fig,ax)
            sns.heatmap(corr,annot=True,fmt=".2f",cmap="coolwarm",ax=ax,
                        linewidths=.5,cbar_kws={"shrink":.8},annot_kws={"size":8})
            ax.set_title(f"Correlation: {sel}",pad=10)
            plt.tight_layout(); st.pyplot(fig); plt.close()

        st.subheader("📈 Velocity Distributions")
        fig2,axes2 = plt.subplots(1,3,figsize=(14,4)); _dark(fig2,axes2)
        for ax_,col_,clr_,lbl_ in zip(axes2,
            ["V_obs_km_s","V_bar_km_s","Velocity_Difference_km_s"],
            [COLORS["obs"],COLORS["bar"],COLORS["dark"]],
            ["V_obs (km/s)","V_bar (km/s)","Residual (km/s)"]):
            ax_.hist(df[col_].dropna(),bins=15,color=clr_,alpha=.8,edgecolor="#0a0a1a")
            ax_.axvline(df[col_].mean(),color="white",ls="--",lw=1)
            ax_.set_xlabel(lbl_); ax_.set_ylabel("Count"); ax_.set_title(lbl_)
        st.pyplot(fig2); plt.close()
    except Exception as e:
        st.error(f"Error: {e}")

# ══════════════════ TAB 4 — ANOMALY DETECTION ════════════════════════════════
with t4:
    st.header(f"🚨 Anomaly Detection: {sel}")
    try:
        df = _analyse(sel)
        zc  = int(df["Zscore_Anomaly"].sum())
        ic  = int(df["IQR_Anomaly"].sum())
        fc  = int(df["Final_Anomaly"].sum())
        tot = len(df)

        a1,a2,a3,a4 = st.columns(4)
        a1.metric("Total Points",   tot)
        a2.metric("Z-score Flags",  zc)
        a3.metric("IQR Flags",      ic)
        a4.metric("🚨 Final Anomalies", fc, delta=f"{fc/tot*100:.1f}%", delta_color="inverse")

        fig,axes = plt.subplots(1,2,figsize=(14,5)); _dark(fig,axes)
        ax = axes[0]
        nm = ~df["Zscore_Anomaly"]
        ax.scatter(df.loc[nm,"Radius_kpc"],df.loc[nm,"Z_Score"],
                   color=COLORS["obs"],s=25,alpha=.75,label="Normal")
        if df["Zscore_Anomaly"].any():
            ax.scatter(df.loc[df["Zscore_Anomaly"],"Radius_kpc"],
                       df.loc[df["Zscore_Anomaly"],"Z_Score"],
                       color=COLORS["anomaly"],s=80,marker="*",zorder=5,label=f"Anomaly ({zc})")
        ax.axhline(3, color="#ffd43b",ls="--",lw=1,label="+3σ")
        ax.axhline(-3,color="#ffd43b",ls="--",lw=1,label="−3σ")
        ax.set_xlabel("Radius (kpc)"); ax.set_ylabel("Z-score")
        ax.set_title(f"Z-score: {sel}"); ax.legend(fontsize=7,**LEG)

        ax2 = axes[1]
        r = df["Velocity_Difference_km_s"]
        Q1,Q3 = r.quantile(.25),r.quantile(.75)
        IQR = Q3-Q1; lb,ub = Q1-1.5*IQR, Q3+1.5*IQR
        nm2 = ~df["IQR_Anomaly"]
        ax2.scatter(df.loc[nm2,"Radius_kpc"],r[nm2],color=COLORS["obs"],s=25,alpha=.75,label="Normal")
        if df["IQR_Anomaly"].any():
            ax2.scatter(df.loc[df["IQR_Anomaly"],"Radius_kpc"],r[df["IQR_Anomaly"]],
                        color=COLORS["anomaly"],s=80,marker="*",zorder=5,label=f"Anomaly ({ic})")
        ax2.axhline(ub,color="#ffd43b",ls="--",lw=1,label=f"Upper ({ub:.1f})")
        ax2.axhline(lb,color="#ffd43b",ls=":",lw=1, label=f"Lower ({lb:.1f})")
        ax2.set_xlabel("Radius (kpc)"); ax2.set_ylabel("Residual (km/s)")
        ax2.set_title(f"IQR: {sel}"); ax2.legend(fontsize=7,**LEG)
        st.pyplot(fig); plt.close()

        if fc>0:
            st.warning(f"⚠️ {fc} point(s) flagged by both methods.")
            with st.expander("🔍 Anomaly Details"):
                cols = ["Radius_kpc","V_obs_km_s","V_bar_km_s","Velocity_Difference_km_s",
                        "Z_Score","Zscore_Anomaly","IQR_Anomaly","Final_Anomaly"]
                st.dataframe(df[df["Final_Anomaly"]][cols],use_container_width=True)
        else:
            st.success("✅ No significant anomalies detected.")
    except Exception as e:
        st.error(f"Error: {e}")

# ══════════════════ TAB 5 — GALAXY COMPARISON ════════════════════════════════
with t5:
    st.header("🌐 Multi-Galaxy Comparison")
    if len(cmp)<2:
        st.info("👈 Select at least 2 galaxies in the sidebar.")
    else:
        try:
            cdf = _multi(tuple(cmp))
            pal = plt.cm.tab10.colors
            fig,axes = plt.subplots(2,2,figsize=(14,10)); _dark(fig,axes.flatten())

            # Rotation curves
            ax = axes[0,0]
            for i,g in enumerate(cmp):
                gdf=cdf[cdf["Galaxy"]==g]
                ax.plot(gdf["Radius_kpc"],gdf["V_obs_km_s"],color=pal[i%10],lw=1.5,label=g,alpha=.85)
            ax.set_xlabel("Radius (kpc)"); ax.set_ylabel("V_obs (km/s)")
            ax.set_title("Observed Rotation Curves"); ax.legend(fontsize=7,**LEG)

            # V_obs vs V_bar
            ax2=axes[0,1]
            for i,g in enumerate(cmp):
                gdf=cdf[cdf["Galaxy"]==g]
                ax2.scatter(gdf["V_bar_km_s"],gdf["V_obs_km_s"],color=pal[i%10],s=20,label=g,alpha=.75)
            vm=cdf[["V_obs_km_s","V_bar_km_s"]].max().max()
            ax2.plot([0,vm],[0,vm],"w--",lw=.8,alpha=.5,label="V_obs=V_bar")
            ax2.set_xlabel("V_bar (km/s)"); ax2.set_ylabel("V_obs (km/s)")
            ax2.set_title("Observed vs Baryonic"); ax2.legend(fontsize=7,**LEG)

            # Residuals
            ax3=axes[1,0]
            for i,g in enumerate(cmp):
                gdf=cdf[cdf["Galaxy"]==g]
                ax3.plot(gdf["Radius_kpc"],gdf["Velocity_Difference_km_s"],color=pal[i%10],lw=1.5,label=g,alpha=.85)
            ax3.axhline(0,color="white",ls="--",lw=.8,alpha=.4)
            ax3.set_xlabel("Radius (kpc)"); ax3.set_ylabel("V_obs−V_bar (km/s)")
            ax3.set_title("Velocity Residuals"); ax3.legend(fontsize=7,**LEG)

            # DM fraction bar chart
            ax4=axes[1,1]
            names_,fracs_,clrs_ = [],[],[]
            for i,g in enumerate(cmp):
                gdf=cdf[cdf["Galaxy"]==g]
                if gdf.empty: continue
                lr=gdf.iloc[-1]
                dm=lr.get("Additional_Mass_Solar",np.nan)
                f=max((dm/lr["Total_Mass_Solar"]*100) if pd.notna(dm) and lr["Total_Mass_Solar"]>0 else 0,0)
                names_.append(g); fracs_.append(f); clrs_.append(pal[i%10])
            bars=ax4.barh(names_,fracs_,color=clrs_,alpha=.85,edgecolor="#0a0a1a")
            ax4.set_xlabel("DM Fraction (%)"); ax4.set_title("Dark Matter Fraction (outer)")
            ax4.set_xlim(0,100)
            for b,v in zip(bars,fracs_):
                ax4.text(b.get_width()+1,b.get_y()+b.get_height()/2,f"{v:.1f}%",
                         va="center",ha="left",fontsize=8,color="#e0e0ff")
            plt.tight_layout(pad=2); st.pyplot(fig); plt.close()

            st.subheader("📋 Summary Table")
            rows=[]
            for g in cmp:
                gdf=cdf[cdf["Galaxy"]==g]
                if gdf.empty: continue
                rows.append({"Galaxy":g,"Points":len(gdf),
                             "Max V_obs":gdf["V_obs_km_s"].max(),"Max V_bar":gdf["V_bar_km_s"].max(),
                             "Mean Residual":gdf["Velocity_Difference_km_s"].mean(),
                             "Anomalies":int(gdf["Final_Anomaly"].sum())})
            st.dataframe(pd.DataFrame(rows).style.format(
                {"Max V_obs":"{:.1f}","Max V_bar":"{:.1f}","Mean Residual":"{:.1f}"}),
                use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

# ══════════════════ TAB 6 — DATASET OVERVIEW ═════════════════════════════════
with t6:
    st.header("📋 SPARC Dataset Overview")
    if meta.empty:
        st.warning("Galaxy metadata not available.")
    else:
        oc1,oc2,oc3 = st.columns(3)
        oc1.metric("Total Galaxies", len(meta))
        d=pd.to_numeric(meta["D"],errors="coerce").dropna()
        oc2.metric("Distance Range", f"{d.min():.1f} – {d.max():.1f} Mpc")
        oc3.metric("Avg Inclination",f"{pd.to_numeric(meta['Inc'],errors='coerce').mean():.1f}°")

        fig,axes=plt.subplots(2,2,figsize=(14,9)); _dark(fig,axes.flatten())

        d.hist(ax=axes[0,0],bins=25,color=COLORS["obs"],edgecolor="#0a0a1a",alpha=.85)
        axes[0,0].set_xlabel("Distance (Mpc)"); axes[0,0].set_ylabel("Count")
        axes[0,0].set_title("Galaxy Distance Distribution")

        vf=pd.to_numeric(meta["Vflat"],errors="coerce").replace(0,np.nan).dropna()
        vf.hist(ax=axes[0,1],bins=25,color=COLORS["bar"],edgecolor="#0a0a1a",alpha=.85)
        axes[0,1].set_xlabel("V_flat (km/s)"); axes[0,1].set_ylabel("Count")
        axes[0,1].set_title("V_flat Distribution")

        t_=pd.to_numeric(meta["T"],errors="coerce").dropna().value_counts().sort_index()
        axes[1,0].bar(t_.index,t_.values,color=COLORS["gas"],alpha=.85,edgecolor="#0a0a1a")
        axes[1,0].set_xlabel("Morphological Type (T)"); axes[1,0].set_ylabel("Count")
        axes[1,0].set_title("Morphological Type Distribution")

        v=meta[["D","Vflat","T"]].copy()
        for col in ["D","Vflat","T"]:
            v[col]=pd.to_numeric(v[col],errors="coerce")
        v["Vflat"]=v["Vflat"].replace(0,np.nan); v=v.dropna()
        sc=axes[1,1].scatter(v["D"],v["Vflat"],c=v["T"],cmap="plasma",s=30,alpha=.8)
        plt.colorbar(sc,ax=axes[1,1],label="Type (T)")
        axes[1,1].set_xlabel("Distance (Mpc)"); axes[1,1].set_ylabel("V_flat (km/s)")
        axes[1,1].set_title("Distance vs V_flat")
        plt.tight_layout(pad=2); st.pyplot(fig); plt.close()

        with st.expander("🗂️ Full Metadata Table"):
            st.dataframe(meta,use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#506e8a;font-size:.85em;padding:10px 0'>
<b>DARKVERSE</b> — An Intelligent Dark Matter &amp; Galactic Behaviour Analytics Platform<br>
Data: SPARC (Lelli et al. 2016) · Person 1: Data Pipeline · Person 2: Analysis · Person 3: Dashboard
</div>""", unsafe_allow_html=True)
