"""
DARKVERSE — Anomaly Detection (Person 2)
Z-score and IQR-based anomaly detection on velocity residuals.
"""
import pandas as pd

def calculate_residuals(df):
    df = df.copy()
    df["Velocity_Difference_km_s"] = df["V_obs_km_s"] - df["V_bar_km_s"]
    return df

def detect_zscore_anomalies(df):
    df = df.copy()
    r = df["Velocity_Difference_km_s"]
    mean, std = r.mean(), r.std()
    if std == 0:
        df["Z_Score"] = 0; df["Zscore_Anomaly"] = False
    else:
        df["Z_Score"] = (r - mean) / std
        df["Zscore_Anomaly"] = df["Z_Score"].abs() > 3
    return df

def detect_iqr_anomalies(df):
    df = df.copy()
    r = df["Velocity_Difference_km_s"]
    Q1, Q3 = r.quantile(0.25), r.quantile(0.75)
    IQR = Q3 - Q1
    df["IQR_Anomaly"] = (r < Q1 - 1.5*IQR) | (r > Q3 + 1.5*IQR)
    return df

def analyze_anomalies(df):
    df = calculate_residuals(df)
    df = detect_zscore_anomalies(df)
    df = detect_iqr_anomalies(df)
    df["Anomaly_Count"] = df["Zscore_Anomaly"].astype(int) + df["IQR_Anomaly"].astype(int)
    df["Final_Anomaly"]  = df["Anomaly_Count"] == 2
    return df
