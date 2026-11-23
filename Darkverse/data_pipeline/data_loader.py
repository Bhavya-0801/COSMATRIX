"""
DARKVERSE — Data Pipeline: Data Loader (Person 1)
Loads processed galaxy CSVs and metadata.
"""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

def list_processed_galaxies():
    return [f.stem.replace("_rotmod_cleaned","") for f in sorted(DATA_DIR.glob("*_rotmod_cleaned.csv"))]

def load_processed_galaxy(filename):
    p = DATA_DIR / filename
    if not p.exists(): raise FileNotFoundError(f"Not found: {p}")
    return pd.read_csv(p)

def load_galaxy_metadata():
    p = DATA_DIR / "galaxy_metadata.csv"
    if not p.exists(): raise FileNotFoundError(f"Metadata not found: {p}")
    return pd.read_csv(p)

def load_galaxy_with_metadata(galaxy_name):
    meta = load_galaxy_metadata()
    match = meta[meta["Galaxy"].astype(str).str.strip() == galaxy_name]
    if match.empty: raise ValueError(f"Galaxy not found: {galaxy_name}")
    rot = load_processed_galaxy(f"{galaxy_name}_rotmod_cleaned.csv")
    return rot, match.iloc[0]

