from pathlib import Path
import pandas as pd

from preprocessing import ROTATION_COLUMNS, clean_data, inspect_data_quality, validate_rotation_data

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"


def process_all_galaxies():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    galaxy_files = sorted(RAW_DATA_DIR.glob("*_rotmod.dat"))

    if not galaxy_files:
        raise FileNotFoundError(
            f"No *_rotmod.dat files found in {RAW_DATA_DIR}. "
            "Check that the SPARC rotation files are extracted into data/raw/."
        )

    successful, failed = 0, 0
    failures = []

    print(f"Found {len(galaxy_files)} raw galaxy files.")

    for sample_file in galaxy_files:
        try:
            raw_df = pd.read_csv(
                sample_file,
                sep=r"\s+",
                comment="#",
                header=None,
                names=ROTATION_COLUMNS
            )

            cleaned_df = clean_data(raw_df)
            warnings = validate_rotation_data(cleaned_df)

            output_file = PROCESSED_DATA_DIR / f"{sample_file.stem}_cleaned.csv"
            cleaned_df.to_csv(output_file, index=False)

            successful += 1
            print(f"[OK] {sample_file.name}: {len(raw_df)} raw rows -> "
                  f"{len(cleaned_df)} cleaned rows")
            for warning in warnings:
                print(f"  [WARNING] {warning}")

        except Exception as exc:
            failed += 1
            failures.append((sample_file.name, str(exc)))
            print(f"[FAILED] {sample_file.name}: {exc}")

    print("\n========== BATCH PROCESSING REPORT ==========")
    print("Files found:", len(galaxy_files))
    print("Successfully processed:", successful)
    print("Failed:", failed)
    print("=============================================")

    if failures:
        print("\nFailure details:")
        for name, reason in failures:
            print(f"- {name}: {reason}")

    return successful, failed


if __name__ == "__main__":
    process_all_galaxies()
