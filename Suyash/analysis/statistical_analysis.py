import numpy as np
import pandas as pd

def calculate_descriptive_statistics(df):

    column = df[
        ['V_obs_km_s', 'V_bar_km_s',
         'Velocity_Difference_km_s', 'per_diff']
    ]

    statistics = {
        "Mean": column.mean(),
        "Median": column.median(),
        "Standard Deviation": column.std(),
        "Variance": column.var(),
        "Maximum": column.max(),
        "Minimum": column.min()
    }

    return statistics


def calculate_correlation(df):

    # Select relevant numerical columns
    columns = df[
        [
            "Radius_kpc",
            "V_obs_km_s",
            "V_bar_km_s",
            "Velocity_Difference_km_s",
            "per_diff"
        ]
    ]

    # Calculate Pearson correlation
    correlation = columns.corr(method="pearson")

    return correlation
def analyze_galaxy_statistics(df):

    columns = [
        "V_obs_km_s",
        "V_bar_km_s",
        "Velocity_Difference_km_s",
        "per_diff"
    ]

    grouped = df.groupby("Galaxy")[columns].agg(
        ["mean", "median", "std", "min", "max"]
    )

    return grouped

def calculate_velocity_statistics(df):

    residual = df["Velocity_Difference_km_s"]

    statistics = {
        "Mean_Residual": residual.mean(),
        "MAE": residual.abs().mean(),
        "RMSE": np.sqrt((residual ** 2).mean()),
        "Correlation": df["V_obs_km_s"].corr(df["V_bar_km_s"])
    }

    return statistics

def generate_statistical_report(df):
    report = {
        "Descriptive_Statistics": calculate_descriptive_statistics(df),
        "Correlation_Analysis": calculate_correlation(df),
        "Galaxy_Wise_Statistics": analyze_galaxy_statistics(df),
        "Velocity_Statistics": calculate_velocity_statistics(df)
    }

    return report