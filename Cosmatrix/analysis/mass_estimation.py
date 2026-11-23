"""
COSMATRIX — Mass Estimation (Suyash)
Total, baryonic, and dark matter proxy mass calculations.
"""
import pandas as pd
from analysis.physics_model import kpc_to_meters, km_s_to_m_s, kg_to_solar_mass, G

def calculate_enclosed_mass(radius_kpc, velocity_km_s):
    r = kpc_to_meters(radius_kpc)
    v = km_s_to_m_s(velocity_km_s)
    return kg_to_solar_mass((r * v**2) / G)

def calculate_baryonic_mass(radius_kpc, v_bar_km_s):
    r = kpc_to_meters(radius_kpc)
    v = km_s_to_m_s(v_bar_km_s)
    return kg_to_solar_mass((r * v**2) / G)

def calculate_dark_matter_mass(radius_kpc, v_obs_km_s, v_bar_km_s):
    extra = calculate_enclosed_mass(radius_kpc, v_obs_km_s) - calculate_baryonic_mass(radius_kpc, v_bar_km_s)
    return extra if extra >= 0 else None

def estimate_galaxy_mass(df):
    df = df.copy()
    df["Total_Mass_Solar"]      = df.apply(lambda r: calculate_enclosed_mass(r["Radius_kpc"], r["V_obs_km_s"]), axis=1)
    df["Baryonic_Mass_Solar"]   = df.apply(lambda r: calculate_baryonic_mass(r["Radius_kpc"], r["V_bar_km_s"]), axis=1)
    df["Additional_Mass_Solar"] = df.apply(lambda r: calculate_dark_matter_mass(r["Radius_kpc"], r["V_obs_km_s"], r["V_bar_km_s"]), axis=1)
    return df

