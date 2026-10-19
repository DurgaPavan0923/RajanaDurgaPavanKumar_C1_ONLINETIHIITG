"""Preprocessing module: Sensor quality auditing, chronological splitting, resampling, and leakage assertion."""

from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.base import BaseEstimator, TransformerMixin

from src.utils import get_logger

logger = get_logger("Preprocessing")


class DomainBoundsClipper(BaseEstimator, TransformerMixin):
    """Clips sensor values to physical bounds without throwing exceptions."""

    def __init__(self, bounds: dict[str, tuple[float, float]] | None = None) -> None:
        self.bounds = bounds or {}

    def fit(self, X: pd.DataFrame | np.ndarray, y: Any = None) -> "DomainBoundsClipper":
        return self

    def transform(self, X: pd.DataFrame | np.ndarray) -> pd.DataFrame:
        if isinstance(X, np.ndarray):
            X_df = pd.DataFrame(X)
        else:
            X_df = X.copy()
        for col, (b_low, b_high) in self.bounds.items():
            if col in X_df.columns:
                X_df[col] = X_df[col].clip(lower=b_low, upper=b_high)
        return X_df


def audit_sensor_quality(
    df: pd.DataFrame,
    ranges: dict[str, list[float] | tuple[float, float]] | None = None,
    timestamp_col: str | None = None,
) -> pd.DataFrame:
    """Calculates missingness %, out-of-range count, IQR outliers, and summary statistics."""
    total_rows = len(df)
    records = []
    effective_ranges = ranges or {}

    for col in df.columns:
        if col == timestamp_col:
            continue
        series = df[col]
        missing_count = int(series.isna().sum())
        missing_pct = round((missing_count / total_rows) * 100, 2) if total_rows > 0 else 0.0

        valid_min, valid_max = effective_ranges.get(col, (-np.inf, np.inf))
        numeric_series = pd.to_numeric(series.dropna(), errors="coerce")
        out_of_bounds_count = int(
            ((numeric_series < valid_min) | (numeric_series > valid_max)).sum()
        )

        q25 = float(numeric_series.quantile(0.25)) if len(numeric_series) else 0.0
        q75 = float(numeric_series.quantile(0.75)) if len(numeric_series) else 0.0
        iqr = q75 - q25
        iqr_outliers = int(
            ((numeric_series < (q25 - 1.5 * iqr)) | (numeric_series > (q75 + 1.5 * iqr))).sum()
        )

        records.append(
            {
                "sensor": col,
                "missing_count": missing_count,
                "missing_pct": missing_pct,
                "out_of_bounds_count": out_of_bounds_count,
                "iqr_outliers": iqr_outliers,
                "valid_range": f"[{valid_min}, {valid_max}]",
                "mean": round(float(numeric_series.mean()), 3) if len(numeric_series) else None,
                "std": round(float(numeric_series.std()), 3) if len(numeric_series) else None,
                "min": round(float(numeric_series.min()), 3) if len(numeric_series) else None,
                "max": round(float(numeric_series.max()), 3) if len(numeric_series) else None,
            }
        )
    return pd.DataFrame(records)


def detect_temporal_gaps_and_drift(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
    expected_interval_seconds: int = 3600,
) -> dict[str, Any]:
    """Audits temporal sampling regularity, identifies gaps, and measures distribution drift."""
    raw_ts = pd.to_datetime(df[timestamp_col], errors="coerce").dropna()
    duplicate_count = int(raw_ts.duplicated().sum())
    is_strictly_monotonic = bool(raw_ts.is_monotonic_increasing and duplicate_count == 0)
    ts = raw_ts.sort_values()
    deltas = ts.diff().dt.total_seconds().dropna()

    mean_delta = float(deltas.mean()) if len(deltas) else 0.0
    std_delta = float(deltas.std()) if len(deltas) else 0.0
    jitter_ratio = round(std_delta / (mean_delta + 1e-9), 4)

    gap_threshold = expected_interval_seconds * 3
    large_gaps = int((deltas > gap_threshold).sum())

    drift_stats = {}
    numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != timestamp_col]
    half = len(df) // 2
    for col in numeric_cols:
        s1 = df[col].iloc[:half].dropna()
        s2 = df[col].iloc[half:].dropna()
        if len(s1) > 20 and len(s2) > 20:
            ks_stat, p_val = stats.ks_2samp(s1, s2)
            drift_stats[col] = {
                "ks_statistic": round(float(ks_stat), 4),
                "p_value": round(float(p_val), 4),
                "drift_flag": bool(p_val < 0.01),
            }

    return {
        "total_records": len(df),
        "mean_sampling_interval_seconds": round(mean_delta, 1),
        "sampling_jitter_ratio": jitter_ratio,
        "large_gap_count": large_gaps,
        "is_monotonic": is_strictly_monotonic,
        "duplicate_timestamps": duplicate_count,
        "drift_analysis": drift_stats,
    }


def temporal_walk_forward_split(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Performs strict chronological walk-forward split (e.g. 70% Train, 15% Val, 15% Test)."""
    df_sorted = df.sort_values(by=timestamp_col).reset_index(drop=True)
    n = len(df_sorted)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df_sorted.iloc[:train_end].copy()
    val_df = df_sorted.iloc[train_end:val_end].copy()
    test_df = df_sorted.iloc[val_end:].copy()

    # Verify no temporal overlap
    assert_no_leakage(train_df, val_df, test_df, timestamp_col=timestamp_col)
    logger.info(
        f"Chronological split: Train={len(train_df)}, Val={len(val_df)}, Test Lockbox={len(test_df)}"
    )
    return train_df, val_df, test_df


def clean_and_resample_stream(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
    freq: str = "1h",
    max_ffill: int = 3,
) -> pd.DataFrame:
    """Sets regular datetime index, interpolates small gaps, and attaches missingness indicators."""
    df_clean = df.copy()
    df_clean[timestamp_col] = pd.to_datetime(df_clean[timestamp_col], errors="coerce")
    df_clean = df_clean.dropna(subset=[timestamp_col]).sort_values(by=timestamp_col)
    # Aggregate duplicate timestamps by mean to incorporate all telemetry packets
    df_clean = df_clean.groupby(timestamp_col).mean(numeric_only=True)

    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    # Resample to regular frequency
    resampled = df_clean[numeric_cols].resample(freq).mean()

    # Interpolate bounded gaps
    interpolated = resampled.interpolate(method="time", limit=max_ffill)
    # Forward fill remaining short gaps
    interpolated = interpolated.ffill(limit=max_ffill).bfill(limit=1)

    result = interpolated.reset_index()
    logger.info(
        f"Cleaned & resampled stream from {len(df)} to {len(result)} regular '{freq}' steps"
    )
    return result


def assert_no_leakage(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    test_df: pd.DataFrame,
    timestamp_col: str = "timestamp",
) -> dict[str, bool]:
    """Asserts that temporal causality is preserved and partition boundaries do not overlap."""
    t_train_max = pd.to_datetime(train_df[timestamp_col]).max()
    t_val_min = pd.to_datetime(val_df[timestamp_col]).min()
    t_val_max = pd.to_datetime(val_df[timestamp_col]).max()
    t_test_min = pd.to_datetime(test_df[timestamp_col]).min()

    no_train_val_overlap = bool(t_train_max < t_val_min)
    no_val_test_overlap = bool(t_val_max < t_test_min)

    idx_overlap = bool(
        len(set(train_df.index).intersection(val_df.index)) == 0
        and len(set(val_df.index).intersection(test_df.index)) == 0
    )

    if not (no_train_val_overlap and no_val_test_overlap):
        raise AssertionError(
            f"Temporal Leakage Detected! Train max ({t_train_max}) >= Val min ({t_val_min}) "
            f"or Val max ({t_val_max}) >= Test min ({t_test_min})"
        )

    return {
        "no_train_val_overlap": no_train_val_overlap,
        "no_val_test_overlap": no_val_test_overlap,
        "disjoint_indices": idx_overlap,
    }
