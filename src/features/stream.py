"""Temporal feature engineering module: Causal lags, rolling statistics, diurnal cycles, and physical interactions."""

from typing import Any

import numpy as np
import pandas as pd

from src.utils import get_logger

logger = get_logger("Features")


def generate_causal_lags(
    df: pd.DataFrame,
    sensor_cols: list[str],
    lags: list[int] | None = None,
) -> pd.DataFrame:
    """Generates strictly causal past lags (shift >= 1) to prevent lookahead leakage."""
    if lags is None:
        lags = [1, 2, 3, 6, 12, 24]
    out = pd.DataFrame(index=df.index)
    for col in sensor_cols:
        if col in df.columns:
            for lag in lags:
                out[f"{col}_lag_{lag}"] = df[col].shift(lag)
    return out


def generate_rolling_features(
    df: pd.DataFrame,
    sensor_cols: list[str],
    windows: list[int] | None = None,
) -> pd.DataFrame:
    """Computes closed-left rolling mean, std, min, max using shift(1) to avoid target contamination."""
    if windows is None:
        windows = [3, 6, 12, 24]
    out = pd.DataFrame(index=df.index)
    for col in sensor_cols:
        if col in df.columns:
            # Shift by 1 step so current row is never in rolling window
            shifted = df[col].shift(1)
            for w in windows:
                out[f"{col}_roll_mean_{w}"] = shifted.rolling(w, min_periods=max(1, w // 2)).mean()
                out[f"{col}_roll_std_{w}"] = shifted.rolling(w, min_periods=max(2, w // 2)).std().fillna(0.0)
                out[f"{col}_roll_min_{w}"] = shifted.rolling(w, min_periods=max(1, w // 2)).min()
                out[f"{col}_roll_max_{w}"] = shifted.rolling(w, min_periods=max(1, w // 2)).max()
    return out


def generate_cyclical_time_features(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
) -> pd.DataFrame:
    """Encodes diurnal (24h) and seasonal periodic cycles using sine and cosine transformations."""
    out = pd.DataFrame(index=df.index)
    if timestamp_col in df.columns:
        ts = pd.to_datetime(df[timestamp_col], errors="coerce")
        hour = ts.dt.hour
        dayofweek = ts.dt.dayofweek

        out["sin_hour"] = np.sin(2 * np.pi * hour / 24.0)
        out["cos_hour"] = np.cos(2 * np.pi * hour / 24.0)
        out["sin_day"] = np.sin(2 * np.pi * dayofweek / 7.0)
        out["cos_day"] = np.cos(2 * np.pi * dayofweek / 7.0)
    return out


def generate_cross_sensor_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes aquatic physical and chemical interaction metrics."""
    out = pd.DataFrame(index=df.index)
    cols = df.columns

    # 1. Temperature & Dissolved Oxygen saturation coupling (DO decreases with Temp)
    if "temperature" in cols and "dissolved_oxygen" in cols:
        out["temp_x_do"] = df["temperature"] * df["dissolved_oxygen"]
        out["do_temp_ratio"] = df["dissolved_oxygen"] / (df["temperature"].clip(lower=0.1))

    # 2. pH distance from neutral (7.0)
    if "ph" in cols:
        out["ph_dev_neutral"] = (df["ph"] - 7.0).abs()
        out["ph_acidic_flag"] = (df["ph"] < 6.5).astype(float)
        out["ph_alkaline_flag"] = (df["ph"] > 8.5).astype(float)

    # 3. Conductivity to Turbidity interaction
    if "conductivity" in cols and "turbidity" in cols:
        out["conduct_to_turbidity"] = df["conductivity"] / (df["turbidity"] + 0.1)

    return out


def engineer_stream_features(
    df: pd.DataFrame,
    config: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """End-to-end Track A feature engineering pipeline combining lags, rollings, cycles, and physical interactions."""
    cfg = config or {}
    track_a_cfg = cfg.get("track_a", {})
    sensor_cols = track_a_cfg.get(
        "sensor_columns",
        ["temperature", "dissolved_oxygen", "ph", "conductivity", "turbidity", "pressure"],
    )
    ts_col = track_a_cfg.get("timestamp_column", "timestamp")
    lags = track_a_cfg.get("features", {}).get("lags", [1, 2, 3, 6, 12, 24])
    windows = track_a_cfg.get("features", {}).get("rolling_windows", [3, 6, 12, 24])

    df_base = df.copy()
    parts = [df_base]

    # Generate feature components
    lag_df = generate_causal_lags(df_base, sensor_cols, lags=lags)
    roll_df = generate_rolling_features(df_base, sensor_cols, windows=windows)
    time_df = generate_cyclical_time_features(df_base, timestamp_col=ts_col)
    cross_df = generate_cross_sensor_features(df_base)

    parts.extend([lag_df, roll_df, time_df, cross_df])
    res = pd.concat(parts, axis=1)

    # Forward-fill initial NaN rows caused by lag shifting, then backward-fill residual
    res = res.ffill().bfill()
    logger.info(
        f"Stream features engineered: shape evolved from {df.shape} to {res.shape} "
        f"({res.shape[1] - df.shape[1]} engineered features)"
    )
    return res


def engineer_tabular_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineers physicochemical domain features for Track B static benchmark."""
    res = df.copy()
    if "Solids" in res.columns:
        res["solids_log1p"] = np.log1p(res["Solids"].clip(lower=0))
    if "Sulfate" in res.columns and "Conductivity" in res.columns:
        res["sulfate_to_conductivity"] = res["Sulfate"] / (res["Conductivity"] + 1e-5)
    if "Organic_carbon" in res.columns and "Solids" in res.columns:
        res["organic_to_solids"] = res["Organic_carbon"] / (res["Solids"] + 1e-5)
    if "Hardness" in res.columns and "Solids" in res.columns:
        res["hardness_to_solids"] = res["Hardness"] / (res["Solids"] + 1e-5)
    if "Chloramines" in res.columns and "Turbidity" in res.columns:
        res["chloramines_x_turbidity"] = res["Chloramines"] * res["Turbidity"]
    if "ph" in res.columns:
        res["ph_dev_neutral"] = (res["ph"] - 7.0).abs()
        res["ph_who_out_of_bounds"] = ((res["ph"] < 6.5) | (res["ph"] > 8.5)).astype(float)
    if "Turbidity" in res.columns:
        res["turbidity_who_excess"] = (res["Turbidity"] > 5.0).astype(float)
    if "Chloramines" in res.columns:
        res["chloramines_who_excess"] = (res["Chloramines"] > 4.0).astype(float)
    return res
