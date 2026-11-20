import sys
import os

# Get the main project directory
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project directory to Python path
sys.path.append(project_path)


from analysis.rotation_analysis import (
    load_galaxy_data,
    calculate_rotation_curves
)

from analysis.mass_estimation import estimate_galaxy_mass

# Load dataset
df = load_galaxy_data("data/sample_galaxy.csv")

# Calculate baryonic velocity first
df = calculate_rotation_curves(df)

# Estimate galaxy masses
df = estimate_galaxy_mass(df)

# Display results
print("\nDARKVERSE - Mass Estimation")

print(df[[
    "Galaxy",
    "Radius_kpc",
    "Total_Mass_Solar",
    "Baryonic_Mass_Solar",
    "Additional_Mass_Solar"
]])

print("\nMass estimation completed!")
