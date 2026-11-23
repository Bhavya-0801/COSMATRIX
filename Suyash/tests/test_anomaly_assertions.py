import pandas as pd

from analysis.anomaly_detection import (
    calculate_residuals,
    detect_zscore_anomalies,
    detect_iqr_anomalies,
    analyze_anomalies
)


# Helper: Create a dataframe with known residuals
def create_test_dataframe(residuals):
    return pd.DataFrame({
        "V_obs_km_s": residuals,
        "V_bar_km_s": [0] * len(residuals)
    })


# TEST 1: Residual calculation
def test_calculate_residuals():
    df = pd.DataFrame({
        "V_obs_km_s": [100, 150, 200],
        "V_bar_km_s": [80, 100, 120]
    })

    result = calculate_residuals(df)

    expected = [20, 50, 80]

    assert result["Velocity_Difference_km_s"].tolist() == expected


# TEST 2: Z-score detects an extreme outlier
def test_zscore_detects_outlier():
    residuals = [10] * 19 + [200]
    df = create_test_dataframe(residuals)

    df = calculate_residuals(df)
    result = detect_zscore_anomalies(df)

    assert result["Zscore_Anomaly"].sum() == 1
    assert result.iloc[-1]["Zscore_Anomaly"] == True


# TEST 3: Z-score handles zero standard deviation
def test_zscore_zero_standard_deviation():
    residuals = [10, 10, 10, 10, 10]
    df = create_test_dataframe(residuals)

    df = calculate_residuals(df)
    result = detect_zscore_anomalies(df)

    assert (result["Z_Score"] == 0).all()
    assert not result["Zscore_Anomaly"].any()


# TEST 4: IQR detects an extreme outlier
def test_iqr_detects_outlier():
    residuals = [10, 11, 12, 13, 14, 15, 200]
    df = create_test_dataframe(residuals)

    df = calculate_residuals(df)
    result = detect_iqr_anomalies(df)

    assert result["IQR_Anomaly"].sum() == 1
    assert result.iloc[-1]["IQR_Anomaly"] == True


# TEST 5: Combined anomaly detection
def test_combined_anomaly_detection():
    residuals = [10] * 19 + [200]
    df = create_test_dataframe(residuals)

    result = analyze_anomalies(df)

    assert result["Final_Anomaly"].sum() == 1
    assert result.iloc[-1]["Final_Anomaly"] == True
    assert result.iloc[-1]["Anomaly_Count"] == 2


# TEST 6: Normal data should not be flagged
def test_normal_data_no_anomalies():
    residuals = [10, 11, 12, 13, 14, 15]
    df = create_test_dataframe(residuals)

    result = analyze_anomalies(df)

    assert not result["Final_Anomaly"].any()