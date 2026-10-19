"""Leakage guard tests and edge-case validation."""

import numpy as np
import pandas as pd

from src.data.preprocessing import DataPreprocessor


def test_track_b_no_index_overlap():
    df = pd.DataFrame(
        {
            "ph": np.random.uniform(6.5, 8.5, 100),
            "Turbidity": np.random.uniform(1.0, 5.0, 100),
            "Potability": [0, 1] * 50,
        }
    )
    prep = DataPreprocessor(random_state=42)
    X_train, X_test, y_train, y_test = prep.split_track_b(
        df, target_col="Potability", test_size=0.20
    )

    # Check partition integrity
    assert len(X_train) == 80
    assert len(X_test) == 20
    assert len(set(X_train.index).intersection(set(X_test.index))) == 0


def test_scaler_leakage_guard():
    """Verifies that test statistics do not influence training scaler means."""
    X_train = pd.DataFrame({"sensor": [10.0, 20.0, 30.0]})  # mean = 20.0
    X_test = pd.DataFrame({"sensor": [1000.0, 2000.0]})  # massive values

    prep = DataPreprocessor(scaling_strategy="standard")
    X_tr_trans, pipeline = prep.fit_transform_train(X_train)
    _ = prep.transform_eval(X_test, pipeline)

    # Pipeline contains 'column_transform' -> 'numeric' -> 'scaler'
    ct = pipeline.named_steps["column_transform"]
    scaler = ct.named_transformers_["numeric"].named_steps["scaler"]
    assert np.isclose(scaler.mean_[0], 20.0)


def test_track_a_chronological_causality():
    dates = pd.date_range("2026-08-20", periods=100, freq="h")
    df = pd.DataFrame({"timestamp": dates, "temperature": np.random.uniform(15, 25, 100)})

    prep = DataPreprocessor()
    train_df, val_df, test_df = prep.split_track_a(
        df, timestamp_col="timestamp", train_ratio=0.7, val_ratio=0.15
    )

    assert train_df["timestamp"].max() < val_df["timestamp"].min()
    assert val_df["timestamp"].max() < test_df["timestamp"].min()


def test_edge_case_constant_sensor():
    """Verifies pipeline does not crash on constant invariant sensor."""
    df_train = pd.DataFrame({"constant_sensor": [5.0, 5.0, 5.0, 5.0]})
    prep = DataPreprocessor(scaling_strategy="standard")
    trans, pipeline = prep.fit_transform_train(df_train)
    assert not np.isnan(trans).any()


def test_edge_case_all_nan_column():
    """Verifies pipeline handles all-NaN columns gracefully."""
    df_train = pd.DataFrame({"all_nan": [np.nan, np.nan, np.nan], "valid": [1.0, 2.0, 3.0]})
    prep = DataPreprocessor(imputation_strategy="median")
    trans, pipeline = prep.fit_transform_train(df_train)
    # Sklearn SimpleImputer drops completely empty all-NaN columns; verify 3 rows and valid column preserved without crash
    assert trans.shape == (3, 1)
