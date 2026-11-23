import numpy as np
import pandas as pd

from analysis.physics_model import calculate_baryonic_velocity

def load_galaxy_data(file_path):
    data=pd.read_csv(file_path)
    return data

def calculate_rotation_curves(df):
    df["V_bar_km_s"] = df.apply(
        lambda row: calculate_baryonic_velocity(
            row["V_gas_km_s"],
            row["V_disk_km_s"],
            row["V_bulge_km_s"]
        ),
        axis=1
    )
    return df

def calculate_velocity_difference(df):
    df["Velocity_Difference_km_s"] = (
        df["V_obs_km_s"] - df["V_bar_km_s"]
    )
    return df

def calculate_percentage_difference(df):
    df["per_diff"] = (
       (( df["V_obs_km_s"] - df["V_bar_km_s"])/ df["V_obs_km_s"])*100
    )
    return df

def analyze_galaxy(df,galaxy_name):
    galaxy_data = df[df["Galaxy"] == galaxy_name].copy()
  
    if galaxy_data.empty:
        raise ValueError("Galaxy not found")

    galaxy_data = calculate_rotation_curves(galaxy_data)
    galaxy_data = calculate_velocity_difference(galaxy_data)
    galaxy_data = calculate_percentage_difference(galaxy_data)
    return galaxy_data