import pytest
import pandas as pd

from analysis.mass_estimation import (
    calculate_enclosed_mass,
    calculate_baryonic_mass,
    calculate_dark_matter_mass,
    estimate_galaxy_mass
)


# Physical constants used for independent expected-value calculations
G = 6.67430e-11
KPC_TO_METERS = 3.085677581e19
SOLAR_MASS_KG = 1.98847e30


def expected_mass_solar(radius_kpc, velocity_km_s):
    radius_m = radius_kpc * KPC_TO_METERS
    velocity_m_s = velocity_km_s * 1000

    mass_kg = radius_m * velocity_m_s**2 / G
    return mass_kg / SOLAR_MASS_KG


# TEST 1: Enclosed mass
def test_calculate_enclosed_mass():
    result = calculate_enclosed_mass(1, 100)
    expected = expected_mass_solar(1, 100)

    assert result == pytest.approx(expected)


# TEST 2: Baryonic mass
def test_calculate_baryonic_mass():
    result = calculate_baryonic_mass(1, 80)
    expected = expected_mass_solar(1, 80)

    assert result == pytest.approx(expected)


# TEST 3: Additional mass when observed velocity exceeds baryonic
def test_calculate_dark_matter_mass_positive():
    result = calculate_dark_matter_mass(5, 150, 100)

    expected = (
        expected_mass_solar(5, 150)
        - expected_mass_solar(5, 100)
    )

    assert result == pytest.approx(expected)


# TEST 4: Additional mass should not be negative
def test_calculate_dark_matter_mass_negative():
    result = calculate_dark_matter_mass(5, 80, 100)

    assert result is None


# TEST 5: Complete mass estimation pipeline
def test_estimate_galaxy_mass():
    df = pd.DataFrame({
        "Radius_kpc": [1, 2],
        "V_obs_km_s": [100, 150],
        "V_bar_km_s": [80, 100]
    })

    result = estimate_galaxy_mass(df)

    assert "Total_Mass_Solar" in result.columns
    assert "Baryonic_Mass_Solar" in result.columns
    assert "Additional_Mass_Solar" in result.columns

    assert result.iloc[0]["Total_Mass_Solar"] == pytest.approx(
        expected_mass_solar(1, 100)
    )

    assert result.iloc[0]["Baryonic_Mass_Solar"] == pytest.approx(
        expected_mass_solar(1, 80)
    )

    assert result.iloc[0]["Additional_Mass_Solar"] == pytest.approx(
        expected_mass_solar(1, 100) - expected_mass_solar(1, 80)
    )