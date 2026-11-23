from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
METADATA_FILE = PROJECT_DIR / "data" / "raw" / "SPARC_Lelli2016c.mrt"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

METADATA_COLUMNS = [
    "Galaxy", "T", "D", "e_D", "f_D",
    "Inc", "e_Inc", "L_36", "e_L_36",
    "Reff", "SBeff", "Rdisk", "SBdisk",
    "MHI", "RHI", "Vflat", "e_Vflat", "Q", "Ref"
]


def load_galaxy_metadata():
    """
    Read the SPARC fixed-width table. read_fwf infers field boundaries
    from the fixed-width records, preserving blank fields unlike a
    whitespace-splitting parser.
    """
    if not METADATA_FILE.exists():
        raise FileNotFoundError(f"Metadata file not found: {METADATA_FILE}")

    # The first 98 lines contain title, column descriptions and references.
    metadata = pd.read_fwf(
        METADATA_FILE,
        skiprows=98,
        header=None,
        names=METADATA_COLUMNS
    )

    # Remove any completely blank lines that may occur in the table.
    metadata = metadata.dropna(how="all").reset_index(drop=True)

    # Convert numeric columns safely; text/reference fields remain strings.
    text_columns = {"Galaxy", "Ref"}
    for column in METADATA_COLUMNS:
        if column not in text_columns:
            metadata[column] = pd.to_numeric(metadata[column], errors="coerce")

    metadata["Galaxy"] = metadata["Galaxy"].astype("string").str.strip()
    metadata = metadata[metadata["Galaxy"].notna() & (metadata["Galaxy"] != "")]
    metadata = metadata.reset_index(drop=True)

    # Guard against silently saving a shifted/misparsed table.
    if metadata.empty:
        raise ValueError("No galaxy records were parsed from the SPARC metadata file.")

    first = metadata.iloc[0]
    if first["Galaxy"] != "CamB" or pd.isna(first["T"]) or pd.isna(first["D"]):
        raise ValueError(
            "Metadata parsing did not pass the first-record check. "
            f"Parsed first record: {first.to_dict()}. "
            "Do not save this file; inspect the fixed-width layout."
        )

    if int(first["T"]) != 10 or abs(float(first["D"]) - 3.36) > 0.02:
        raise ValueError(
            "Metadata columns appear misaligned. Expected CamB: T=10 and D≈3.36; "
            f"got T={first['T']} and D={first['D']}. Do not save this file."
        )

    if len(metadata) != 175:
        print(f"[WARNING] Expected 175 galaxies, parsed {len(metadata)}.")

    return metadata


def save_galaxy_metadata(metadata):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DIR / "galaxy_metadata.csv"
    metadata.to_csv(output_file, index=False)
    print("Saved metadata:", output_file)
    return output_file


if __name__ == "__main__":
    df = load_galaxy_metadata()
    print("\nMetadata loaded:", df.shape)
    print(df.head(10).to_string(index=False))
    print("\nColumn information:")
    df.info()
    save_galaxy_metadata(df)
