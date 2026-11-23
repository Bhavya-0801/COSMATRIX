import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import pandas as pd

from analysis.rotation_analysis import (
    load_galaxy_data,
    calculate_rotation_curves,
    calculate_velocity_difference,
    calculate_percentage_difference
)

from analysis.mass_estimation import estimate_galaxy_mass

from analysis.statistical_analysis import generate_statistical_report

from analysis.anomaly_detection import analyze_anomalies


def main():

    print("=" * 60)
    print("         COSMATRIX - INTEGRATION TEST")
    print("=" * 60)

    # 1. Load dataset
    df = load_galaxy_data("data/sample_galaxy.csv")
    print("\n[1] Dataset loaded successfully")
    print(f"Total observations: {len(df)}")
    print(f"Galaxies: {df['Galaxy'].nunique()}")

    # 2. Rotation analysis
    df = calculate_rotation_curves(df)
    df = calculate_velocity_difference(df)
    df = calculate_percentage_difference(df)

    print("\n[2] Rotation analysis completed")

    # 3. Mass estimation
    df = estimate_galaxy_mass(df)

    print("\n[3] Mass estimation completed")

    # 4. Statistical analysis
    report = generate_statistical_report(df)

    print("\n[4] Statistical analysis completed")

    for section, result in report.items():
        print("\n" + "-" * 60)
        print(section)
        print("-" * 60)
        print(result)

    # 5. Anomaly detection
    df = analyze_anomalies(df)

    print("\n[5] Anomaly detection completed")

    print("\nAnomaly Summary:")
    print("Z-score anomalies:", df["Zscore_Anomaly"].sum())
    print("IQR anomalies:", df["IQR_Anomaly"].sum())
    print("Final anomalies:", df["Final_Anomaly"].sum())

    # Display flagged observations
    anomalies = df[df["Final_Anomaly"] == True]

    print("\nFlagged Anomalies:")
    if anomalies.empty:
        print("No observations were flagged by both methods.")
    else:
        print(
            anomalies[
                [
                    "Galaxy",
                    "Radius_kpc",
                    "V_obs_km_s",
                    "V_bar_km_s",
                    "Velocity_Difference_km_s",
                    "Z_Score",
                    "Anomaly_Count"
                ]
            ]
        )

    # Final result
    print("\n" + "=" * 60)
    print("COSMATRIX INTEGRATION TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
