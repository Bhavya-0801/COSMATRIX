"""
DARKVERSE — Statistical Analysis (Person 2)
Descriptive stats, correlation, velocity residual metrics.
"""
import numpy as np
import pandas as pd

def calculate_descriptive_statistics(df):
    cols = df[['V_obs_km_s','V_bar_km_s','Velocity_Difference_km_s','per_diff']]
    return {"Mean": cols.mean(), "Median": cols.median(),
            "Standard Deviation": cols.std(), "Variance": cols.var(),
            "Maximum": cols.max(), "Minimum": cols.min()}

def calculate_correlation(df):
    return df[["Radius_kpc","V_obs_km_s","V_bar_km_s",
               "Velocity_Difference_km_s","per_diff"]].corr(method="pearson")

def analyze_galaxy_statistics(df):
    return df.groupby("Galaxy")[["V_obs_km_s","V_bar_km_s",
        "Velocity_Difference_km_s","per_diff"]].agg(["mean","median","std","min","max"])

def calculate_velocity_statistics(df):
    r = df["Velocity_Difference_km_s"]
    return {"Mean_Residual": r.mean(), "MAE": r.abs().mean(),
            "RMSE": np.sqrt((r**2).mean()),
            "Correlation": df["V_obs_km_s"].corr(df["V_bar_km_s"])}

def generate_statistical_report(df):
    return {"Descriptive_Statistics": calculate_descriptive_statistics(df),
            "Correlation_Analysis": calculate_correlation(df),
            "Galaxy_Wise_Statistics": analyze_galaxy_statistics(df),
            "Velocity_Statistics": calculate_velocity_statistics(df)}

