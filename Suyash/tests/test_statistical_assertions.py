import pytest
import pandas as pd

from analysis.statistical_analysis import (
    calculate_descriptive_statistics,
    calculate_correlation,
    analyze_galaxy_statistics,
    calculate_velocity_statistics,
    generate_statistical_report
)


# Create a controlled test dataset
def create_test_dataframe():
    return pd.DataFrame({
        "Galaxy": ["Galaxy_A", "Galaxy_A", "Galaxy_B", "Galaxy_B"],
        "Radius_kpc": [1, 2, 3, 4],
        "V_obs_km_s": [100, 120, 140, 160],
        "V_bar_km_s": [80, 100, 110, 130],
        "Velocity_Difference_km_s": [20, 20, 30, 30],
        "per_diff": [20, 16.666667, 21.428571, 18.75]
    })


# TEST 1: Descriptive statistics
def test_descriptive_statistics():
    df = create_test_dataframe()
    result = calculate_descriptive_statistics(df)

    assert result["Mean"]["V_obs_km_s"] == pytest.approx(130)
    assert result["Median"]["V_obs_km_s"] == pytest.approx(130)

    assert result["Minimum"]["V_obs_km_s"] == 100
    assert result["Maximum"]["V_obs_km_s"] == 160

    assert result["Mean"]["Velocity_Difference_km_s"] == pytest.approx(25)
    assert result["Median"]["Velocity_Difference_km_s"] == pytest.approx(25)


# TEST 2: Correlation matrix
def test_correlation_analysis():
    df = create_test_dataframe()
    result = calculate_correlation(df)

    assert result.shape == (5, 5)

    # Correlation of a variable with itself should be 1
    assert result.loc["V_obs_km_s", "V_obs_km_s"] == pytest.approx(1.0)

    # Correlation matrix must be symmetric
    assert result.loc["V_obs_km_s", "V_bar_km_s"] == pytest.approx(
        result.loc["V_bar_km_s", "V_obs_km_s"]
    )

    # Known correlation for our test data
    assert result.loc["V_obs_km_s", "V_bar_km_s"] == pytest.approx(
        0.9922778767
    )


# TEST 3: Galaxy-wise statistics
def test_galaxy_wise_statistics():
    df = create_test_dataframe()
    result = analyze_galaxy_statistics(df)

    assert "Galaxy_A" in result.index
    assert "Galaxy_B" in result.index

    assert result.loc["Galaxy_A", ("V_obs_km_s", "mean")] == pytest.approx(110)
    assert result.loc["Galaxy_B", ("V_obs_km_s", "mean")] == pytest.approx(150)

    assert result.loc["Galaxy_A", ("Velocity_Difference_km_s", "mean")] == pytest.approx(20)
    assert result.loc["Galaxy_B", ("Velocity_Difference_km_s", "mean")] == pytest.approx(30)


# TEST 4: Velocity statistics
def test_velocity_statistics():
    df = create_test_dataframe()
    result = calculate_velocity_statistics(df)

    assert result["Mean_Residual"] == pytest.approx(25)
    assert result["MAE"] == pytest.approx(25)
    assert result["RMSE"] == pytest.approx((650) ** 0.5)
    assert result["Correlation"] == pytest.approx(0.9922778767)


# TEST 5: Full statistical report
def test_generate_statistical_report():
    df = create_test_dataframe()
    result = generate_statistical_report(df)

    assert "Descriptive_Statistics" in result
    assert "Correlation_Analysis" in result
    assert "Galaxy_Wise_Statistics" in result
    assert "Velocity_Statistics" in result


# TEST 6: Validate report contents
def test_report_values():
    df = create_test_dataframe()
    report = generate_statistical_report(df)

    velocity_stats = report["Velocity_Statistics"]

    assert velocity_stats["MAE"] == pytest.approx(25)
    assert velocity_stats["Mean_Residual"] == pytest.approx(25)
    assert velocity_stats["RMSE"] == pytest.approx(25.49509757)