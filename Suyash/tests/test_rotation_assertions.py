import pytest
from pathlib import Path

from analysis.rotation_analysis import (
    load_galaxy_data,
    calculate_rotation_curves,
    calculate_velocity_difference,
    calculate_percentage_difference,
    analyze_galaxy
)

DATA_PATH = Path(__file__).parent.parent / "data" / "sample_galaxy.csv"


# TEST 1: Dataset loading
def test_load_galaxy_data():
    df = load_galaxy_data(DATA_PATH)

    assert len(df) == 30
    assert df["Galaxy"].nunique() == 3
    assert "V_obs_km_s" in df.columns


# TEST 2: Baryonic velocity calculation
def test_calculate_rotation_curves():
    df = load_galaxy_data(DATA_PATH)
    df = calculate_rotation_curves(df)

    expected = (10**2 + 65**2 + 25**2)**0.5

    assert "V_bar_km_s" in df.columns
    assert df.iloc[0]["V_bar_km_s"] == pytest.approx(expected)


# TEST 3: Velocity difference
def test_calculate_velocity_difference():
    df = load_galaxy_data(DATA_PATH)
    df = calculate_rotation_curves(df)
    df = calculate_velocity_difference(df)

    expected = 85 - (10**2 + 65**2 + 25**2)**0.5

    assert df.iloc[0]["Velocity_Difference_km_s"] == pytest.approx(expected)


# TEST 4: Percentage difference
def test_calculate_percentage_difference():
    df = load_galaxy_data(DATA_PATH)
    df = calculate_rotation_curves(df)
    df = calculate_velocity_difference(df)
    df = calculate_percentage_difference(df)

    expected = (
        (85 - (10**2 + 65**2 + 25**2)**0.5) / 85
    ) * 100

    assert df.iloc[0]["per_diff"] == pytest.approx(expected)


# TEST 5: Analyze an individual galaxy
def test_analyze_galaxy():
    df = load_galaxy_data(DATA_PATH)
    result = analyze_galaxy(df, "Galaxy_A")

    assert len(result) == 10
    assert all(result["Galaxy"] == "Galaxy_A")
    assert "V_bar_km_s" in result.columns
    assert "Velocity_Difference_km_s" in result.columns
    assert "per_diff" in result.columns


# TEST 6: Invalid galaxy name
def test_analyze_nonexistent_galaxy():
    df = load_galaxy_data(DATA_PATH)

    with pytest.raises(ValueError):
        analyze_galaxy(df, "Galaxy_X")