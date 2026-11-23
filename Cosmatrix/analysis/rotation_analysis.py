"""
COSMATRIX — Rotation Analysis (Suyash)
Baryonic velocity, residuals, percentage difference.
"""
import pandas as pd
from analysis.physics_model import calculate_baryonic_velocity

def calculate_rotation_curves(df):
    df = df.copy()
    df["V_bar_km_s"] = df.apply(
        lambda r: calculate_baryonic_velocity(r["V_gas_km_s"], r["V_disk_km_s"], r["V_bulge_km_s"]), axis=1)
    return df

def calculate_velocity_difference(df):
    df = df.copy()
    df["Velocity_Difference_km_s"] = df["V_obs_km_s"] - df["V_bar_km_s"]
    return df

def calculate_percentage_difference(df):
    df = df.copy()
    df["per_diff"] = ((df["V_obs_km_s"] - df["V_bar_km_s"]) / df["V_obs_km_s"]) * 100
    return df

def analyze_galaxy(df, galaxy_name):
    gdf = df[df["Galaxy"] == galaxy_name].copy()
    if gdf.empty:
        raise ValueError(f"Galaxy '{galaxy_name}' not found")
    gdf = calculate_rotation_curves(gdf)
    gdf = calculate_velocity_difference(gdf)
    gdf = calculate_percentage_difference(gdf)
    return gdf

