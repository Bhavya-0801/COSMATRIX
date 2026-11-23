from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from data_loader import load_galaxy_metadata, load_all_galaxies_with_metadata

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
FIGURES_DIR = PROCESSED_DIR / "figures"


def create_metadata_summary():
    metadata = load_galaxy_metadata()
    print("\n========== GALAXY METADATA SUMMARY ==========")
    print("Number of galaxies:", len(metadata))
    print("\nNumeric summary:")
    print(metadata.describe(include="all").to_string())
    print("\nMissing values:")
    print(metadata.isna().sum().to_string())
    return metadata.describe(include="all")


def plot_galaxy_distance_distribution():
    metadata = load_galaxy_metadata()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    distances = pd.to_numeric(metadata["D"], errors="coerce").dropna()
    plt.figure(figsize=(8, 5))
    plt.hist(distances, bins=20)
    plt.xlabel("Distance (Mpc)")
    plt.ylabel("Number of galaxies")
    plt.title("SPARC Galaxy Distance Distribution")
    plt.tight_layout()

    output = FIGURES_DIR / "galaxy_distance_distribution.png"
    plt.savefig(output, dpi=150)
    plt.close()
    print("Saved plot:", output)


def plot_rotation_curve(galaxy_name="CamB"):
    combined = load_all_galaxies_with_metadata()
    if galaxy_name not in combined:
        raise ValueError(f"No matching rotation dataset for {galaxy_name}")

    rotation_df, metadata = combined[galaxy_name]
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.errorbar(
        rotation_df["Rad"],
        rotation_df["Vobs"],
        yerr=rotation_df["errV"],
        fmt="o",
        capsize=3,
        label="Observed velocity"
    )
    plt.xlabel("Radius (kpc)")
    plt.ylabel("Observed rotational velocity (km/s)")
    plt.title(f"Rotation Curve: {galaxy_name}")
    plt.legend()
    plt.tight_layout()

    output = FIGURES_DIR / f"{galaxy_name}_rotation_curve.png"
    plt.savefig(output, dpi=150)
    plt.close()
    print("Saved plot:", output)


if __name__ == "__main__":
    create_metadata_summary()
    plot_galaxy_distance_distribution()
    plot_rotation_curve("CamB")
