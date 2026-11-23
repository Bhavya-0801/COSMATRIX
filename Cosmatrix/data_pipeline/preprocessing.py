"""
COSMATRIX — Data Pipeline: Preprocessing (Purva)
Cleans and validates raw SPARC rotation-curve data files.
"""
import pandas as pd

ROTATION_COLUMNS = ["Rad","Vobs","errV","Vgas","Vdisk","Vbul","SBdisk","SBbul"]
ESSENTIAL_COLUMNS = ["Rad","Vobs","errV"]

def clean_data(df):
    missing = [c for c in ROTATION_COLUMNS if c not in df.columns]
    if missing: raise ValueError(f"Missing columns: {missing}")
    cleaned = df.copy()
    for col in ROTATION_COLUMNS:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.dropna(subset=ESSENTIAL_COLUMNS)
    cleaned = cleaned[cleaned["Rad"] > 0]
    cleaned = cleaned[cleaned["errV"] >= 0]
    return cleaned.reset_index(drop=True)

def validate_rotation_data(df):
    warns = []
    if df.empty: warns.append("Dataset is empty.")
    if "Rad" in df and (df["Rad"] <= 0).any(): warns.append("Non-positive radius values found.")
    if "errV" in df and (df["errV"] < 0).any(): warns.append("Negative uncertainties found.")
    if "Rad" in df and not df["Rad"].is_monotonic_increasing: warns.append("Radius not sorted.")
    return warns

