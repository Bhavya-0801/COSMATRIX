"""
DARKVERSE — Data Bridge (Person 3)
Converts Person 1's SPARC schema → Person 2's analysis schema.

Person 1 columns : Rad, Vobs, errV, Vgas, Vdisk, Vbul, SBdisk, SBbul
Person 2 columns : Galaxy, Radius_kpc, V_obs_km_s, V_gas_km_s, V_disk_km_s, V_bulge_km_s
"""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data" / "processed"


def sparc_to_analysis_format(rotation_df: pd.DataFrame, galaxy_name: str) -> pd.DataFrame:
    return pd.DataFrame({
        "Galaxy":      galaxy_name,
        "Radius_kpc":  rotation_df["Rad"].astype(float),
        "V_obs_km_s":  rotation_df["Vobs"].astype(float),
        "V_gas_km_s":  rotation_df["Vgas"].astype(float),
        "V_disk_km_s": rotation_df["Vdisk"].astype(float),
        "V_bulge_km_s":rotation_df["Vbul"].astype(float),
        "errV":        rotation_df["errV"].astype(float),
    }).reset_index(drop=True)


def list_available_galaxies() -> list:
    return [f.stem.replace("_rotmod_cleaned","")
            for f in sorted(DATA_DIR.glob("*_rotmod_cleaned.csv"))]


def load_galaxy_for_analysis(galaxy_name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{galaxy_name}_rotmod_cleaned.csv"
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return sparc_to_analysis_format(pd.read_csv(path), galaxy_name)


def load_multiple_galaxies(galaxy_names: list) -> pd.DataFrame:
    frames = []
    for name in galaxy_names:
        try:
            frames.append(load_galaxy_for_analysis(name))
        except FileNotFoundError:
            pass
    if not frames:
        raise ValueError("No galaxy data loaded")
    return pd.concat(frames, ignore_index=True)
