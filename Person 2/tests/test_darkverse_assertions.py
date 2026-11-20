import pytest

from analysis.physics_model import (
    kpc_to_meters,
    km_s_to_m_s,
    kg_to_solar_mass,
    calculate_baryonic_velocity,
    calculate_additional_velocity
)


def test_kpc_to_meters():
    result = kpc_to_meters(1)
    assert result == pytest.approx(3.085677581e19)


def test_km_s_to_m_s():
    result = km_s_to_m_s(100)
    assert result == 100000


def test_kg_to_solar_mass():
    result = kg_to_solar_mass(1.98847e30)
    assert result == pytest.approx(1.0)


def test_calculate_baryonic_velocity():
    result = calculate_baryonic_velocity(20, 100, 40)
    expected = (20**2 + 100**2 + 40**2)**0.5

    assert result == pytest.approx(expected)


def test_calculate_additional_velocity():
    result = calculate_additional_velocity(150, 100)
    expected = (150**2 - 100**2)**0.5

    assert result == pytest.approx(expected)


def test_additional_velocity_returns_none():
    result = calculate_additional_velocity(90, 100)

    assert result is None


def test_negative_distance_raises_error():
    with pytest.raises(ValueError):
        kpc_to_meters(-5)


def test_negative_mass_raises_error():
    with pytest.raises(ValueError):
        kg_to_solar_mass(-100)