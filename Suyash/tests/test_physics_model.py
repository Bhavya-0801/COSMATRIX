
import sys
import os

# Get the main project directory
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project directory to Python path
sys.path.append(project_path)

# Import functions from physics_model.py
from analysis.physics_model import (
    kpc_to_meters,
    km_s_to_m_s,
    kg_to_solar_mass,
    calculate_baryonic_velocity,
    calculate_additional_velocity
)


print("===== COSMATRIX PHYSICS TESTING =====\n")


# TEST 1: Distance Conversion
result = kpc_to_meters(2)

print("Test 1: Distance Conversion")
print("Input: 2 kpc")
print("Output:", result, "metres\n")


# TEST 2: Velocity Conversion
result = km_s_to_m_s(150)

print("Test 2: Velocity Conversion")
print("Input: 150 km/s")
print("Output:", result, "m/s\n")


# TEST 3: Mass Conversion
result = kg_to_solar_mass(1.98847e31)

print("Test 3: Mass Conversion")
print("Input: 1.98847e31 kg")
print("Output:", result, "Solar Masses\n")


# TEST 4: Baryonic Rotational Velocity
result = calculate_baryonic_velocity(20, 100, 40)

print("Test 4: Baryonic Velocity")
print("Gas: 20 km/s")
print("Disk: 100 km/s")
print("Bulge: 40 km/s")
print("Output:", result, "km/s\n")


# TEST 5: Additional Velocity Contribution
result = calculate_additional_velocity(150, result)

print("Test 5: Additional Velocity")
print("Observed Velocity: 150 km/s")
print("Output:", result, "km/s\n")


print("===== TESTING COMPLETED =====")

