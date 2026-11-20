import pandas as pd
import numpy as np

from analysis.physics_model import (
    kpc_to_meters,
    km_s_to_m_s,
    kg_to_solar_mass
)

G = 6.67430e-11

#to calculate total mass( of given radius)
def calculate_enclosed_mass(radius_kpc, velocity_km_s):
    radius_m = kpc_to_meters(radius_kpc)#conversion
    velocity_m_s = km_s_to_m_s(velocity_km_s)#conversion

    mass_kg=((radius_m)*(velocity_m_s**2))/G#formula

    mass_solar = kg_to_solar_mass(mass_kg)#conversion

    return mass_solar

#to calculate the baryonic mass( of the visible matter )
def calculate_baryonic_mass(radius_kpc, v_bar_km_s):
    radius_m = kpc_to_meters(radius_kpc)#conversion
    v_bar_m_s = km_s_to_m_s(v_bar_km_s)#conversion
    
    mass_kg=((radius_m)*(v_bar_m_s**2))/G#formula
    
    mass_solar = kg_to_solar_mass(mass_kg)#conversion
    
    return mass_solar

#to calculate dark matter mass
def calculate_dark_matter_mass(radius_kpc, v_obs_km_s, v_bar_km_s):

    total_mass = calculate_enclosed_mass( radius_kpc, v_obs_km_s)

    baryonic_mass = calculate_baryonic_mass(radius_kpc, v_bar_km_s)

    extra_mass = total_mass - baryonic_mass

    if extra_mass < 0:
        return None

    return extra_mass

#to calculate the galaxy mass
def estimate_galaxy_mass(df):

    # Calculate total enclosed mass
    df["Total_Mass_Solar"] = df.apply(
        lambda row: calculate_enclosed_mass(
            row["Radius_kpc"],
            row["V_obs_km_s"]
        ),
        axis=1
    )

    # Calculate baryonic mass
    df["Baryonic_Mass_Solar"] = df.apply(
        lambda row: calculate_baryonic_mass(
            row["Radius_kpc"],
            row["V_bar_km_s"]
        ),
        axis=1
    )

    # Calculate additional mass
    df["Additional_Mass_Solar"] = df.apply(
        lambda row: calculate_dark_matter_mass(
            row["Radius_kpc"],
            row["V_obs_km_s"],
            row["V_bar_km_s"]
        ),
        axis=1
    )

    return df
