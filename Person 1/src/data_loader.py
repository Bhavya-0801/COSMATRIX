from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"


def load_processed_galaxy(filename):
    file_path = PROCESSED_DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Galaxy dataset not found: {file_path}")
    return pd.read_csv(file_path)


def list_processed_galaxies():
    files = sorted(PROCESSED_DATA_DIR.glob("*_rotmod_cleaned.csv"))
    return [file.name for file in files]


def load_galaxy_metadata():
    metadata_file = PROCESSED_DATA_DIR / "galaxy_metadata.csv"
    if not metadata_file.exists():
        raise FileNotFoundError(
            f"Metadata CSV not found: {metadata_file}. "
            "Run metadata_explorer.py first."
        )
    return pd.read_csv(metadata_file)


def load_galaxy_with_metadata(galaxy_name):
    metadata_df = load_galaxy_metadata()
    match = metadata_df[metadata_df["Galaxy"].astype(str).str.strip() == galaxy_name]

    if match.empty:
        raise ValueError(f"Galaxy metadata not found: {galaxy_name}")

    rotation_filename = f"{galaxy_name}_rotmod_cleaned.csv"
    rotation_df = load_processed_galaxy(rotation_filename)
    galaxy_metadata = match.iloc[0]
    return rotation_df, galaxy_metadata


def load_all_galaxies_with_metadata():
    """Return a dict of galaxy name -> (rotation DataFrame, metadata Series)."""
    metadata_df = load_galaxy_metadata()
    combined = {}
    missing_rotation_files = []

    for _, row in metadata_df.iterrows():
        name = str(row["Galaxy"]).strip()
        filename = f"{name}_rotmod_cleaned.csv"
        path = PROCESSED_DATA_DIR / filename
        if not path.exists():
            missing_rotation_files.append(name)
            continue
        combined[name] = (pd.read_csv(path), row)

    if missing_rotation_files:
        print("Metadata records without matching rotation files:",
              ", ".join(missing_rotation_files))
    return combined


if __name__ == "__main__":
    print("Processed folder:", PROCESSED_DATA_DIR)
    print("Folder exists:", PROCESSED_DATA_DIR.exists())

    names = list_processed_galaxies()
    print("\nProcessed rotation files:", len(names))

    try:
        rotation_df, metadata = load_galaxy_with_metadata("CamB")
        print("\nCamB metadata:")
        print(metadata.to_string())
        print("\nCamB rotation data:")
        print(rotation_df.head())
        print("Rotation data shape:", rotation_df.shape)
    except (FileNotFoundError, ValueError) as exc:
        print("\nIntegration test could not complete:", exc)
