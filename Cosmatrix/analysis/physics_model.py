"""
COSMATRIX — Physics Model (Suyash)
Fundamental physics calculations and unit conversions.
"""
import numpy as np

G = 6.67430e-11
KPC_TO_METERS = 3.085677581e19
SOLAR_MASS_KG  = 1.98847e30

def kpc_to_meters(d):
    if d < 0: raise ValueError("Distance cannot be negative")
    return d * KPC_TO_METERS

def km_s_to_m_s(v):
    return v * 1000

def kg_to_solar_mass(m):
    if m < 0: raise ValueError("Mass cannot be negative")
    return m / SOLAR_MASS_KG

def calculate_baryonic_velocity(v_gas, v_disk, v_bulge):
    return (v_gas**2 + v_disk**2 + v_bulge**2) ** 0.5

def calculate_additional_velocity(v_obs, v_bar):
    if v_obs >= v_bar:
        return (v_obs**2 - v_bar**2) ** 0.5
    return None

