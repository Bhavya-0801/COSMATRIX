import pandas as pd
import numpy as np

def calculate_residuals(df):
    df["Velocity_Difference_km_s"] = (
        df["V_obs_km_s"] - df["V_bar_km_s"]
    )
    return df

def detect_zscore_anomalies(df):

    residual = df["Velocity_Difference_km_s"]

    mean = residual.mean()
    stand_dev = residual.std()

    if stand_dev == 0:
        df["Z_Score"] = 0
        df["Zscore_Anomaly"] = False
    else:
        df["Z_Score"] = (residual - mean) / stand_dev
        df["Zscore_Anomaly"] = df["Z_Score"].abs() > 3

    return df

def detect_iqr_anomalies(df):

    residual = df["Velocity_Difference_km_s"]

    Q1 = residual.quantile(0.25)
    Q3 = residual.quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    df["IQR_Anomaly"] = (
        (residual < lower_bound) |
        (residual > upper_bound)
    )

    return df

def analyze_anomalies(df):

    df = calculate_residuals(df)

    df = detect_zscore_anomalies(df)

    df = detect_iqr_anomalies(df)

    df["Anomaly_Count"] = (
        df["Zscore_Anomaly"].astype(int) +
        df["IQR_Anomaly"].astype(int)
    )

    df["Final_Anomaly"] = df["Anomaly_Count"] == 2

    return df