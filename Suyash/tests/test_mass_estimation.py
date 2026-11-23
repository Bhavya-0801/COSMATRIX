
import sys
import os

# Get the main project directory
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project directory to Python path
sys.path.append(project_path)
from analysis.mass_estimation import calculate_enclosed_mass

mass = calculate_enclosed_mass(5, 170)

print("Enclosed Mass:", mass, "Solar Masses")