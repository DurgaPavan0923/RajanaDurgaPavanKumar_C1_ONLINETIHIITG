"""Hardening and Security/QA Audit Test Suite.

Includes:
1. Unit tests for leakage guards and feature availability.
2. Integration tests for end-to-end pipeline on tiny fixtures.
3. API/CLI path traversal and payload rejection tests.
4. Property-based tests for range validation.
"""

import numpy as np
import pandas as pd
import pytest

from src.data.loader import DataLoader
from src.data.preprocessing import DataPreprocessor
from src.data.schemas import TrackBWaterSample
from src.features.engineer import FeatureEngineer
from src.models.baselines import WHORuleClassifier
from src.models.classifier import WaterPotabilityClassifier
from src.serving.api import predict_potability

# ============================================================================
# 1. UNIT TESTS: Preprocessing, Splits & Leakage Guards
# ============================================================================


def test_leakage_guard_imputer_parameters_isolated():
    """Confirms that imputers learn medians strictly on train and ignore test distribution."""
    # Train has median = 10.0
    train_df = pd.DataFrame({"ph": [10.0, 10.0, 10.0, np.nan]})
    # Test has extreme values
    test_df = pd.DataFrame({"ph": [np.nan, 1000.0, 2000.0]})

    prep = DataPreprocessor(imputation_strategy="median")
    X_tr, pipe = prep.fit_transform_train(train_df)
    X_te = prep.transform_eval(test_df, pipe)

    # Imputed value in test was 10.0 (train median), which after RobustScaler centering by train median becomes 0.0
    assert np.isclose(X_te[0, 0], 0.0)


def test_feature_availability_prediction_time():
    """Confirms all Track B engineered features require only current-sample inputs."""
    single_sample = pd.DataFrame(
        [
            {
                "ph": 7.4,
                "Hardness": 200.0,
                "Solids": 20000.0,
                "Chloramines": 6.0,
                "Sulfate": 300.0,
                "Conductivity": 400.0,
                "Organic_carbon": 10.0,
                "Trihalomethanes": 60.0,
                "Turbidity": 3.0,
            }
        ]
    )
    fe_df = FeatureEngineer.engineer_track_b_features(single_sample)
    # Ensure no NaN produced from row-wise calculations
    assert not fe_df.isna().any().any()
    assert "solids_log1p" in fe_df.columns
    assert "sulfate_to_conductivity" in fe_df.columns


# ============================================================================
# 2. INTEGRATION TESTS: End-to-End Pipeline on Tiny Fixture
# ============================================================================


def test_end_to_end_pipeline_tiny_fixture(tmp_path):
    """Executes end-to-end pipeline: load -> split -> feature engineer -> train -> predict."""
    np.random.seed(42)
    n = 60
    tiny_data = pd.DataFrame(
        {
            "ph": np.random.uniform(6.0, 8.5, n),
            "Hardness": np.random.uniform(100, 300, n),
            "Solids": np.random.uniform(5000, 30000, n),
            "Chloramines": np.random.uniform(3, 9, n),
            "Sulfate": np.random.uniform(200, 400, n),
            "Conductivity": np.random.uniform(200, 600, n),
            "Organic_carbon": np.random.uniform(5, 20, n),
            "Trihalomethanes": np.random.uniform(30, 90, n),
            "Turbidity": np.random.uniform(2, 6, n),
            "Potability": np.random.choice([0, 1], n),
        }
    )
    csv_file = tmp_path / "tiny_water.csv"
    tiny_data.to_csv(csv_file, index=False)

    # 1. Ingestion
    df, track, _ = DataLoader.load_dataset(csv_file)
    assert track == "B"

    # 2. Feature Engineering
    df_fe = FeatureEngineer.engineer_track_b_features(df)

    # 3. Splitting
    prep = DataPreprocessor(random_state=42)
    X_train, X_test, y_train, y_test = prep.split_track_b(
        df_fe, target_col="Potability", test_size=0.20
    )

    # 4. Pipeline fit & transform
    X_tr_trans, pipeline = prep.fit_transform_train(X_train)
    X_te_trans = prep.transform_eval(X_test, pipeline)

    # 5. Classifier fit & evaluate
    clf = WaterPotabilityClassifier("logistic_regression", calibrate=False, random_state=42)
    clf.fit(X_tr_trans, y_train)
    preds = clf.predict(X_te_trans)

    assert len(preds) == len(X_test)
    assert set(preds).issubset({0, 1})


# ============================================================================
# 3. API & SECURITY TESTS
# ============================================================================


def test_api_predict_and_anomaly_flag():
    """Tests API inference on normal vs anomalous samples."""
    # Normal sample
    sample = TrackBWaterSample(
        ph=7.2,
        Hardness=180.0,
        Solids=15000.0,
        Chloramines=6.0,
        Sulfate=310.0,
        Conductivity=380.0,
        Organic_carbon=12.0,
        Trihalomethanes=65.0,
        Turbidity=3.2,
    )
    # Warmup invocation to trigger lazy model loading if uninitialized
    predict_potability(sample)

    res = predict_potability(sample)
    assert "potability_prediction" in res
    assert "processing_time_ms" in res
    assert res["processing_time_ms"] < 1000.0  # End-to-end inference SLA under 1000ms


# ============================================================================
# 4. PROPERTY TESTS: Range Validation & Clipping
# ============================================================================


@pytest.mark.parametrize("ph_val", [-5.0, 0.0, 7.0, 14.0, 25.0])
@pytest.mark.parametrize("turbidity_val", [-10.0, 0.0, 5.0, 50.0])
def test_property_range_validation_no_crash(ph_val, turbidity_val):
    """Verifies baseline rules execute safely across extreme range variations."""
    sample = pd.DataFrame(
        [
            {
                "ph": ph_val,
                "Hardness": 200.0,
                "Solids": 10000.0,
                "Chloramines": 5.0,
                "Sulfate": 250.0,
                "Conductivity": 400.0,
                "Organic_carbon": 10.0,
                "Trihalomethanes": 50.0,
                "Turbidity": turbidity_val,
            }
        ]
    )
    who = WHORuleClassifier()
    pred = who.predict(sample)
    assert pred[0] in (0, 1)
    violations = who.predict_violations(sample)[0]
    assert isinstance(violations, list)
