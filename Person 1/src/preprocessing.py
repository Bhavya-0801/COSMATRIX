import pandas as pd

ROTATION_COLUMNS = [
    "Rad", "Vobs", "errV", "Vgas",
    "Vdisk", "Vbul", "SBdisk", "SBbul"
]

ESSENTIAL_COLUMNS = ["Rad", "Vobs", "errV"]


def inspect_data_quality(df, label="Dataset"):
    """Print a compact quality report without changing the input."""
    print(f"\n========== {label.upper()} QUALITY REPORT ==========")
    print("Shape:", df.shape)
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values:")
    print(df.isna().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("====================================================")


def clean_data(df):
    """
    Conservative cleaning for rotation-curve observations.
    Keeps rows when optional component/surface-brightness values are missing.
    Does not impute scientific measurements or remove velocity outliers.
    """
    missing_columns = [c for c in ROTATION_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    cleaned = df.copy()
    for column in ROTATION_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.dropna(subset=ESSENTIAL_COLUMNS)
    cleaned = cleaned[cleaned["Rad"] > 0]
    cleaned = cleaned[cleaned["errV"] >= 0]
    cleaned = cleaned.reset_index(drop=True)
    return cleaned


def validate_rotation_data(df):
    """Return a list of validation warnings; does not modify the data."""
    warnings = []
    if df.empty:
        warnings.append("Dataset is empty.")
    if "Rad" in df and (df["Rad"] <= 0).any():
        warnings.append("Non-positive radius values found.")
    if "errV" in df and (df["errV"] < 0).any():
        warnings.append("Negative measurement uncertainties found.")
    if "Rad" in df and not df["Rad"].is_monotonic_increasing:
        warnings.append("Radius values are not sorted in increasing order.")
    return warnings
