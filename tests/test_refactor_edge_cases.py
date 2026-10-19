"""Comprehensive QA Unit Tests: Edge Cases, Invariants, and Module Robustness.

Audits:
- Empty input DataFrames and arrays
- All-NaN sensor telemetry
- Zero-variance (constant) sensor values
- Out-of-range physical sensor violations
- Duplicate timestamps and irregular sampling jitter
- Single-class labels in classification evaluation
- Strict chronological walk-forward causality and no-leakage assertions
- Causal past lags and closed-left rolling feature isolation
- Multi-step persistence forecasting baseline logic
- Missing artifact actionable error handling
- SHA-256 cryptographic verification
"""

import numpy as np
import pandas as pd
import pytest

from src.anomaly import IQRAnomalyDetector, IsolationForestAnomalyDetector, ZScoreAnomalyDetector
from src.evaluation import compute_classification_metrics, compute_forecasting_metrics
from src.features.stream import (
    engineer_stream_features,
    generate_causal_lags,
    generate_cross_sensor_features,
    generate_rolling_features,
)
from src.forecasting import PersistenceForecaster
from src.io import ArtifactMissingError, compute_sha256, load_artifact, verify_sha256
from src.preprocessing import (
    DomainBoundsClipper,
    assert_no_leakage,
    audit_sensor_quality,
    clean_and_resample_stream,
    detect_temporal_gaps_and_drift,
)


# -----------------------------------------------------------------------------
# 1. Empty Input Handling
# -----------------------------------------------------------------------------
def test_empty_dataframe_handling():
    """Empty DataFrames should not trigger unhandled exceptions across feature generators."""
    empty_df = pd.DataFrame(columns=["temperature", "dissolved_oxygen", "ph", "timestamp"])

    lags = generate_causal_lags(empty_df, sensor_cols=["temperature"])
    assert lags.empty
    assert len(lags) == 0

    rolling = generate_rolling_features(empty_df, sensor_cols=["temperature"])
    assert rolling.empty

    cross = generate_cross_sensor_features(empty_df)
    assert cross.empty

    clipper = DomainBoundsClipper(bounds={"temperature": (0.0, 40.0)})
    clipped = clipper.transform(empty_df[["temperature"]])
    assert clipped.empty


def test_empty_metrics_input():
    """Evaluation functions should safely handle empty arrays without division by zero crash."""
    empty_true = np.array([])
    empty_pred = np.array([])
    metrics = compute_forecasting_metrics(empty_true, empty_pred)
    assert "mae" in metrics
    assert "rmse" in metrics


# -----------------------------------------------------------------------------
# 2. All-NaN Sensor Telemetry
# -----------------------------------------------------------------------------
def test_all_nan_sensor_handling():
    """All-NaN sensor column should be audited as 100% missing without failing pipeline."""
    dates = pd.date_range("2026-08-20 00:00", periods=24, freq="h")
    df = pd.DataFrame(
        {
            "timestamp": dates,
            "temperature": np.full(24, np.nan),
            "dissolved_oxygen": np.full(24, 7.5),
            "ph": np.full(24, 7.2),
            "conductivity": np.full(24, 400.0),
            "turbidity": np.full(24, 2.0),
            "pressure": np.full(24, 1.0),
        }
    )

    audit = audit_sensor_quality(df, ranges={"temperature": (0.0, 40.0)}, timestamp_col="timestamp")
    temp_row = audit[audit["sensor"] == "temperature"].iloc[0]
    assert temp_row["missing_pct"] == 100.0
    assert temp_row["valid_range"] == "[0.0, 40.0]"

    clipper = DomainBoundsClipper(bounds={"temperature": (0.0, 40.0)})
    transformed = clipper.transform(df[["temperature"]])
    assert transformed["temperature"].isna().all()


# -----------------------------------------------------------------------------
# 3. Constant (Zero-Variance) Sensor Handling
# -----------------------------------------------------------------------------
def test_constant_sensor_handling():
    """Sensors with zero variance should not trigger zero-division in Z-score or rolling."""
    constant_values = np.full(100, 7.0)
    z_detector = ZScoreAnomalyDetector(threshold=3.0)
    z_detector.fit(constant_values.reshape(-1, 1))

    # All identical values => 0 distance from mean => zero anomaly flags
    preds = z_detector.predict(constant_values.reshape(-1, 1))
    assert np.all(preds == 0)

    # Rolling std of constant signal should safely be 0.0 without NaN
    df_const = pd.DataFrame({"temperature": constant_values})
    roll = generate_rolling_features(df_const, sensor_cols=["temperature"], windows=[3, 6])
    assert not roll["temperature_roll_std_3"].isna().any()
    assert (roll["temperature_roll_std_3"].dropna() == 0.0).all()


# -----------------------------------------------------------------------------
# 4. Out-of-Range Physical Violations & Domain Clipping
# -----------------------------------------------------------------------------
def test_out_of_range_sensor_values():
    """Values violating environmental domain boundaries should be audited and strictly clipped."""
    df = pd.DataFrame(
        {
            "ph": [-10.0, 0.0, 6.5, 7.0, 8.5, 14.0, 50.0],
            "dissolved_oxygen": [-5.0, 0.0, 5.0, 8.0, 15.0, 20.0, 100.0],
        }
    )

    bounds = {"ph": (0.0, 14.0), "dissolved_oxygen": (0.0, 20.0)}
    clipper = DomainBoundsClipper(bounds=bounds)
    clipped = clipper.transform(df)

    assert clipped["ph"].min() >= 0.0
    assert clipped["ph"].max() <= 14.0
    assert clipped["dissolved_oxygen"].min() >= 0.0
    assert clipped["dissolved_oxygen"].max() <= 20.0

    # Ensure out-of-range audit flags violations
    df_full = df.copy()
    df_full["timestamp"] = pd.date_range("2026-08-20 00:00", periods=len(df), freq="h")
    audit = audit_sensor_quality(df_full, ranges=bounds, timestamp_col="timestamp")
    ph_audit = audit[audit["sensor"] == "ph"].iloc[0]
    assert ph_audit["out_of_bounds_count"] == 2  # -10 and 50


# -----------------------------------------------------------------------------
# 5. Duplicate Timestamps Handling
# -----------------------------------------------------------------------------
def test_duplicate_timestamps_handling():
    """Duplicate timestamps should be flagged by drift audit and regularized by resampling."""
    ts = pd.to_datetime(
        ["2026-08-20 00:00", "2026-08-20 00:00", "2026-08-20 01:00", "2026-08-20 02:00"]
    )
    df = pd.DataFrame(
        {
            "timestamp": ts,
            "temperature": [15.0, 15.5, 16.0, 16.5],
            "dissolved_oxygen": [8.0, 8.2, 7.9, 7.8],
        }
    )

    audit = detect_temporal_gaps_and_drift(df, timestamp_col="timestamp")
    assert audit["total_records"] == 4
    # Not strictly monotonic increasing due to duplicate at start
    assert not audit["is_monotonic"]
    assert audit["duplicate_timestamps"] == 1

    # Resampling aggregates duplicates by mean
    resampled = clean_and_resample_stream(df, timestamp_col="timestamp", freq="1h")
    assert len(resampled) == 3
    assert resampled["temperature"].iloc[0] == 15.25


# -----------------------------------------------------------------------------
# 6. Irregular Sampling Jitter & Gaps
# -----------------------------------------------------------------------------
def test_irregular_sampling_and_gap_detection():
    """Irregular telemetry intervals should be diagnosed and interpolated onto hourly grid."""
    ts = pd.to_datetime(
        [
            "2026-08-20 00:00",
            "2026-08-20 00:15",  # 15 min jitter
            "2026-08-20 02:00",  # missing 01:00
            "2026-08-20 03:00",
        ]
    )
    df = pd.DataFrame(
        {
            "timestamp": ts,
            "temperature": [15.0, 15.2, 16.0, 16.5],
            "dissolved_oxygen": [8.0, 8.1, 7.8, 7.5],
        }
    )

    audit = detect_temporal_gaps_and_drift(
        df, timestamp_col="timestamp", expected_interval_seconds=3600
    )
    assert audit["sampling_jitter_ratio"] > 0.0

    resampled = clean_and_resample_stream(df, timestamp_col="timestamp", freq="1h")
    assert len(resampled) == 4
    # Missing 01:00 interpolated linearly
    assert pd.Timestamp("2026-08-20 01:00") in resampled["timestamp"].values
    val_01 = resampled.loc[
        resampled["timestamp"] == pd.Timestamp("2026-08-20 01:00"), "temperature"
    ].values[0]
    assert 15.0 < val_01 < 16.0


# -----------------------------------------------------------------------------
# 7. Single-Class Labels Evaluation
# -----------------------------------------------------------------------------
def test_single_class_labels_evaluation():
    """Classification metrics must not raise ValueError when holdout contains single class."""
    # Only negative class
    y_true_zeros = np.zeros(50, dtype=int)
    y_pred = np.zeros(50, dtype=int)
    y_prob = np.full((50, 2), [0.8, 0.2])

    metrics_zero = compute_classification_metrics(y_true_zeros, y_pred, y_prob)
    assert metrics_zero["accuracy"] == 1.0
    assert metrics_zero["roc_auc"] == 0.5
    assert metrics_zero["pr_auc"] == 0.5

    # Only positive class
    y_true_ones = np.ones(50, dtype=int)
    metrics_one = compute_classification_metrics(y_true_ones, y_pred, y_prob)
    assert metrics_one["accuracy"] == 0.0
    assert metrics_one["roc_auc"] == 0.5


# -----------------------------------------------------------------------------
# 8. Temporal Leakage Assertions
# -----------------------------------------------------------------------------
def test_temporal_leakage_assertion():
    """assert_no_leakage must raise AssertionError if partitions violate temporal order."""
    dates_train = pd.date_range("2026-08-20", periods=50, freq="h")
    dates_val = pd.date_range("2026-08-21", periods=20, freq="h")  # OVERLAPPING with train!
    dates_test = pd.date_range("2026-08-25", periods=20, freq="h")

    df_train = pd.DataFrame({"timestamp": dates_train, "val": range(50)})
    df_val = pd.DataFrame({"timestamp": dates_val, "val": range(20)})
    df_test = pd.DataFrame({"timestamp": dates_test, "val": range(20)})

    with pytest.raises(AssertionError, match="Temporal Leakage Detected"):
        assert_no_leakage(df_train, df_val, df_test, timestamp_col="timestamp")

    # Chronologically valid partitions should pass cleanly
    dates_val_valid = pd.date_range("2026-08-23", periods=20, freq="h")
    df_val_valid = pd.DataFrame(
        {"timestamp": dates_val_valid, "val": range(20)}, index=range(50, 70)
    )
    df_test_valid = pd.DataFrame({"timestamp": dates_test, "val": range(20)}, index=range(70, 90))
    res = assert_no_leakage(df_train, df_val_valid, df_test_valid, timestamp_col="timestamp")
    assert res["no_train_val_overlap"] is True
    assert res["no_val_test_overlap"] is True
    assert res["disjoint_indices"] is True


# -----------------------------------------------------------------------------
# 9. Causal Lags & Closed-Left Rolling Window Lookahead Prevention
# -----------------------------------------------------------------------------
def test_causal_lags_and_rolling_lookahead_prevention():
    """Features at row t must depend strictly on observations <= t-1, never on t or t+1."""
    df = pd.DataFrame({"temperature": [10.0, 20.0, 30.0, 40.0, 50.0]})

    lags = generate_causal_lags(df, sensor_cols=["temperature"], lags=[1, 2])
    # Lag 1 at index 1 must equal value at index 0 (10.0), not index 1 (20.0)
    assert lags.loc[1, "temperature_lag_1"] == 10.0
    assert np.isnan(lags.loc[0, "temperature_lag_1"])

    # Closed-left rolling mean at index 2 (window 2) must average indices 0 and 1 (10 and 20 => 15.0)
    rolling = generate_rolling_features(df, sensor_cols=["temperature"], windows=[2])
    assert rolling.loc[2, "temperature_roll_mean_2"] == 15.0
    # Must NOT include observation at index 2 (30.0)
    assert rolling.loc[2, "temperature_roll_mean_2"] != (20.0 + 30.0) / 2.0


# -----------------------------------------------------------------------------
# 10. Multi-Step Persistence Forecaster Logic
# -----------------------------------------------------------------------------
def test_persistence_forecaster():
    """PersistenceForecaster must replicate observation at T across horizon steps T+1...T+H."""
    X = np.array([[10.0, 1.0], [20.0, 2.0], [30.0, 3.0]])
    persist = PersistenceForecaster(target_col_idx=0, horizon=6)
    persist.fit(X)
    preds = persist.predict(X)

    assert preds.shape == (3, 6)
    # Target column index 0 had values 10, 20, 30
    assert (preds[0] == 10.0).all()
    assert (preds[1] == 20.0).all()
    assert (preds[2] == 30.0).all()


# -----------------------------------------------------------------------------
# 11. Missing Artifact Actionable Error
# -----------------------------------------------------------------------------
def test_missing_day_artifact_actionable_error():
    """load_artifact must fail with an actionable error specifying the required prerequisite day."""
    with pytest.raises(ArtifactMissingError) as exc_info:
        load_artifact("artifacts/day99/non_existent.json", required_by_day="Day 09")

    err_msg = str(exc_info.value)
    assert "Day 09" in err_msg
    assert "Please run the notebook for Day 09 first" in err_msg


# -----------------------------------------------------------------------------
# 12. SHA-256 Checksum Verification
# -----------------------------------------------------------------------------
def test_sha256_cryptographic_verification(tmp_path):
    """Cryptographic attestation must verify genuine files and reject corrupted ones."""
    test_file = tmp_path / "telemetry_test.txt"
    test_file.write_text("AquaGuard AI Telemetry Data 2026", encoding="utf-8")

    digest = compute_sha256(test_file)
    assert len(digest) == 64
    assert verify_sha256(test_file, digest) is True
    assert verify_sha256(test_file, "INVALID_OR_TAMPERED_HASH_0000000000000000") is False


# -----------------------------------------------------------------------------
# 13. End-to-End Feature Pipelines
# -----------------------------------------------------------------------------
def test_stream_and_tabular_feature_pipelines():
    """Validates end-to-end Track A streaming and Track B tabular feature engineering pipelines."""
    # Track A
    dates = pd.date_range("2026-08-20 00:00", periods=50, freq="h")
    df_stream = pd.DataFrame(
        {
            "timestamp": dates,
            "temperature": np.linspace(15, 25, 50),
            "dissolved_oxygen": np.linspace(9, 6, 50),
            "ph": np.linspace(7.1, 7.8, 50),
            "conductivity": np.linspace(350, 420, 50),
            "turbidity": np.linspace(1.5, 3.2, 50),
            "pressure": np.linspace(1.0, 1.1, 50),
        }
    )

    fe_stream = engineer_stream_features(df_stream)
    assert len(fe_stream) == 50
    assert fe_stream.shape[1] > df_stream.shape[1]
    assert not fe_stream.isna().any().any()

    # Track B
    df_tab = pd.DataFrame(
        {
            "ph": [7.2, 6.1, 8.9],
            "Hardness": [200.0, 150.0, 220.0],
            "Solids": [20000.0, 18000.0, 25000.0],
            "Chloramines": [7.0, 3.5, 4.5],
            "Sulfate": [300.0, 250.0, 320.0],
            "Conductivity": [400.0, 380.0, 420.0],
            "Organic_carbon": [15.0, 12.0, 18.0],
            "Trihalomethanes": [60.0, 50.0, 75.0],
            "Turbidity": [4.0, 2.5, 5.5],
        }
    )
    from src.features.stream import engineer_tabular_features

    fe_tab = engineer_tabular_features(df_tab)
    assert "solids_log1p" in fe_tab.columns
    assert "sulfate_to_conductivity" in fe_tab.columns
    assert "ph_who_out_of_bounds" in fe_tab.columns
    assert fe_tab["ph_who_out_of_bounds"].sum() == 2.0  # 6.1 and 8.9


# -----------------------------------------------------------------------------
# 14. Forecasters: Ridge, RF, XGBoost
# -----------------------------------------------------------------------------
def test_all_forecaster_implementations():
    """Validates fit and multi-step predict contracts across all forecaster models."""
    from src.forecasting import (
        LinearRegressionForecaster,
        RandomForestForecaster,
        XGBoostForecaster,
    )

    X = np.random.RandomState(42).randn(40, 10)
    Y = np.random.RandomState(42).randn(40, 6)

    # Ridge
    ridge = LinearRegressionForecaster()
    ridge.fit(X, Y)
    p_ridge = ridge.predict(X)
    assert p_ridge.shape == (40, 6)

    # Random Forest
    rf = RandomForestForecaster(n_estimators=10, max_depth=3, random_state=42)
    rf.fit(X, Y)
    p_rf = rf.predict(X)
    assert p_rf.shape == (40, 6)

    # XGBoost
    xgb_f = XGBoostForecaster(n_estimators=10, max_depth=3, random_state=42)
    xgb_f.fit(X, Y)
    p_xgb = xgb_f.predict(X)
    assert p_xgb.shape == (40, 6)


# -----------------------------------------------------------------------------
# 15. Anomaly Detectors: IQR, Isolation Forest, Evaluation
# -----------------------------------------------------------------------------
def test_anomaly_detectors_and_evaluation():
    """Tests IQR, Isolation Forest, and anomaly evaluation helper."""
    from src.anomaly import evaluate_anomaly_detection

    X = np.random.RandomState(42).randn(60, 4)
    # Inject 2 extreme outliers
    X[0] = [10.0, 10.0, 10.0, 10.0]
    X[1] = [-10.0, -10.0, -10.0, -10.0]

    iqr = IQRAnomalyDetector(multiplier=1.5)
    iqr.fit(X)
    flags_iqr = iqr.predict(X)
    assert flags_iqr[0] == 1
    assert flags_iqr[1] == 1

    iso = IsolationForestAnomalyDetector(contamination=0.05, random_state=42)
    iso.fit(X)
    eval_iso = evaluate_anomaly_detection(iso, X)
    assert eval_iso["detection_rate"] > 0.0
    assert "score_std" in eval_iso
    assert "total_anomalies" in eval_iso


# -----------------------------------------------------------------------------
# 16. Serialization & Deserialization Round-Trip
# -----------------------------------------------------------------------------
def test_io_serialization_roundtrip(tmp_path):
    """Verifies roundtrip persistence of Parquet, JSON, Joblib, and YAML artifacts."""
    from src.io import load_parquet, save_artifact, save_parquet

    df = pd.DataFrame({"col_a": [1.0, 2.0], "col_b": ["x", "y"]})
    p_parquet = tmp_path / "test.parquet"
    save_parquet(df, p_parquet)
    loaded_df = load_parquet(p_parquet)
    pd.testing.assert_frame_equal(df, loaded_df)

    # JSON
    p_json = tmp_path / "test.json"
    data = {"metric": 0.95, "name": "AquaGuard"}
    save_artifact(data, p_json)
    assert load_artifact(p_json) == data

    # Joblib
    p_joblib = tmp_path / "test.joblib"
    save_artifact(data, p_joblib)
    assert load_artifact(p_joblib) == data

    # YAML
    p_yaml = tmp_path / "test.yaml"
    save_artifact(data, p_yaml)
    assert load_artifact(p_yaml) == data


# -----------------------------------------------------------------------------
# 17. Headless Plotting Suite Execution
# -----------------------------------------------------------------------------
def test_headless_plotting_suite(tmp_path):
    """Verifies all plotting functions render headlessly and export valid image files."""
    from src.plotting import (
        plot_ablation_tornado,
        plot_anomalies,
        plot_correlation_heatmap,
        plot_distributions,
        plot_pr_and_calibration,
        plot_predicted_vs_actual,
        plot_sensor_streams,
    )

    dates = pd.date_range("2026-08-20", periods=30, freq="h")
    df = pd.DataFrame(
        {
            "timestamp": dates,
            "temperature": np.sin(np.linspace(0, 5, 30)) + 15,
            "dissolved_oxygen": np.cos(np.linspace(0, 5, 30)) + 8,
        }
    )

    # Sensor streams
    p1 = tmp_path / "streams.png"
    plot_sensor_streams(df, sensors=["temperature", "dissolved_oxygen"], save_path=p1)
    assert p1.exists() and p1.stat().st_size > 0

    # Correlation heatmap
    p2 = tmp_path / "corr.png"
    plot_correlation_heatmap(df, cols=["temperature", "dissolved_oxygen"], save_path=p2)
    assert p2.exists() and p2.stat().st_size > 0

    # Distributions
    p3 = tmp_path / "dist.png"
    plot_distributions(df, cols=["temperature", "dissolved_oxygen"], save_path=p3)
    assert p3.exists() and p3.stat().st_size > 0

    # Anomalies overlay
    p4 = tmp_path / "anom.png"
    plot_anomalies(df, sensor="temperature", anomaly_flags=np.zeros(30), save_path=p4)
    assert p4.exists() and p4.stat().st_size > 0

    # Predicted vs actual
    p5 = tmp_path / "pred_vs_act.png"
    y_true = np.ones((30, 6))
    y_pred = np.ones((30, 6)) * 1.05
    plot_predicted_vs_actual(y_true, y_pred, sensor_name="dissolved_oxygen", save_path=p5)
    assert p5.exists() and p5.stat().st_size > 0

    # Ablation tornado
    p6 = tmp_path / "tornado.png"
    df_abl = pd.DataFrame({"feature": ["feat1", "feat2"], "delta_mae": [0.05, -0.02]})
    plot_ablation_tornado(df_abl, metric_col="delta_mae", save_path=p6)
    assert p6.exists() and p6.stat().st_size > 0

    # PR & calibration
    p7 = tmp_path / "pr_cal.png"
    y_binary = np.array([0, 1, 0, 1, 0, 1, 0, 0, 1, 1])
    probs = np.array([[0.8, 0.2], [0.3, 0.7]] * 5)
    plot_pr_and_calibration(y_binary, probs, save_path=p7)
    assert p7.exists() and p7.stat().st_size > 0
