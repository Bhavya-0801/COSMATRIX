
import numpy as np
import pandas as pd

# Gravitational constant
G = 6.67430e-11

# Conversion constants
KPC_TO_METERS = 3.085677581e19
SOLAR_MASS_KG = 1.98847e30


# 1. Convert kiloparsecs to metres
def kpc_to_meters(distance_kpc):
    if distance_kpc < 0:
        raise ValueError("Distance cannot be negative")

    return distance_kpc * KPC_TO_METERS


# 2. Convert kilometres per second to metres per second
def km_s_to_m_s(velocity_km_s):
    return velocity_km_s * 1000


# 3. Convert kilograms to solar masses
def kg_to_solar_mass(mass_kg):
    if mass_kg < 0:
        raise ValueError("Mass cannot be negative")

    return mass_kg / SOLAR_MASS_KG

# Calculate baryonic rotational velocity
def calculate_baryonic_velocity(v_gas,v_disk,v_bulge):

    v_bar=(v_gas**2 + v_disk**2 + v_bulge**2)**0.5

    return v_bar

#Calculate additional velocity contribution
def calculate_additional_velocity(v_obs,v_bar):
    if v_obs>=v_bar:
        v_extra=( v_obs**2 - v_bar**2)**0.5
        return v_extra
    else:
       return None
