from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from dataset_explorer import process_all_galaxies
from metadata_explorer import load_galaxy_metadata, save_galaxy_metadata
from data_loader import load_all_galaxies_with_metadata
from analysis import create_metadata_summary, plot_galaxy_distance_distribution, plot_rotation_curve


def main():
    print("\n========== COSMATRIX DATA PIPELINE ==========")

    print("\n[1/5] Processing raw rotation-curve files...")
    process_all_galaxies()

    print("\n[2/5] Extracting and validating galaxy metadata...")
    metadata = load_galaxy_metadata()
    save_galaxy_metadata(metadata)

    print("\n[3/5] Integrating metadata and rotation curves...")
    combined = load_all_galaxies_with_metadata()
    print("Galaxies successfully matched:", len(combined))

    print("\n[4/5] Creating summary and visualizations...")
    create_metadata_summary()
    plot_galaxy_distance_distribution()
    if "CamB" in combined:
        plot_rotation_curve("CamB")

    print("\n[5/5] Pipeline complete.")
    print("Processed data folder:", PROJECT_DIR / "data" / "processed")
    print("=============================================")


if __name__ == "__main__":
    main()
