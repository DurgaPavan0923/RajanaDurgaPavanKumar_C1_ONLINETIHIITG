"""Domain-Informed Feature Engineering for Track A (Temporal) and Track B (Tabular)."""

from pathlib import Path

import numpy as np
import pandas as pd

from src.logger import get_logger

logger = get_logger("FeatureEngineer")


class FeatureEngineer:
    """Computes prediction-time valid features and generates feature metadata catalogs."""

    @staticmethod
    def engineer_track_b_features(df: pd.DataFrame) -> pd.DataFrame:
        """Constructs domain-informed interaction, ratio, and WHO guideline distance features for Track B.

        All calculations are row-wise and causally valid at prediction time.
        """
        X = df.copy()

        # 1. Non-linear logarithmic transformation for skewed Solids (TDS)
        if "Solids" in X.columns:
            X["solids_log1p"] = np.log1p(X["Solids"].clip(lower=0.0))

        # 2. Chemical interaction and domain ratios
        if "Sulfate" in X.columns and "Conductivity" in X.columns:
            X["sulfate_to_conductivity"] = X["Sulfate"] / (X["Conductivity"] + 1e-5)

        if "Organic_carbon" in X.columns and "Solids" in X.columns:
            X["organic_to_solids"] = X["Organic_carbon"] / (X["Solids"] + 1e-5)

        if "Hardness" in X.columns and "Solids" in X.columns:
            X["hardness_to_solids"] = X["Hardness"] / (X["Solids"] + 1e-5)

        if "Chloramines" in X.columns and "Turbidity" in X.columns:
            X["chloramines_x_turbidity"] = X["Chloramines"] * X["Turbidity"]

        # 3. WHO Drinking Water Distance Metrics
        if "ph" in X.columns:
            X["ph_dev_neutral"] = (X["ph"] - 7.0).abs()
            X["ph_who_out_of_bounds"] = ((X["ph"] < 6.5) | (X["ph"] > 8.5)).astype(float)

        if "Turbidity" in X.columns:
            X["turbidity_who_excess"] = (X["Turbidity"] > 5.0).astype(float)

        if "Chloramines" in X.columns:
            X["chloramines_who_excess"] = (X["Chloramines"] > 4.0).astype(float)

        logger.info(f"Engineered Track B features: Shape evolved from {df.shape} to {X.shape}")
        return X

    @staticmethod
    def engineer_track_a_features(
        df: pd.DataFrame,
        timestamp_col: str = "timestamp",
        lags: list[int] | None = None,
        windows: list[int] | None = None,
        sensor_cols: list[str] | None = None,
    ) -> pd.DataFrame:
        """Constructs temporal lag, rolling statistics, cross-sensor ratios, and diurnal cyclical features.

        Strictly causal: uses past observations only (no future lookahead).
        """
        if lags is None:
            lags = [1, 2, 3, 6, 12, 24]
        if windows is None:
            windows = [3, 6, 12, 24]

        X = df.copy()
        X[timestamp_col] = pd.to_datetime(X[timestamp_col], errors="coerce")
        X = X.sort_values(by=timestamp_col).reset_index(drop=True)

        if sensor_cols is None:
            sensor_cols = [
                c for c in X.columns if c != timestamp_col and pd.api.types.is_numeric_dtype(X[c])
            ]

        # 1. Cyclical time-of-day features
        hours = X[timestamp_col].dt.hour
        X["hour_sin"] = np.sin(2 * np.pi * hours / 24.0)
        X["hour_cos"] = np.cos(2 * np.pi * hours / 24.0)

        # 2. Lag features
        for col in sensor_cols:
            for lag in lags:
                X[f"{col}_lag_{lag}"] = X[col].shift(lag)

        # 3. Rolling window features (closed='left' to prevent current-step leakage)
        for col in sensor_cols:
            for w in windows:
                rolling = X[col].shift(1).rolling(window=w, min_periods=1)
                X[f"{col}_roll_mean_{w}"] = rolling.mean()
                X[f"{col}_roll_std_{w}"] = rolling.std().fillna(0.0)

        # 4. Cross-sensor ratios
        if "dissolved_oxygen" in X.columns and "temperature" in X.columns:
            X["do_to_temp_ratio"] = X["dissolved_oxygen"] / (X["temperature"] + 20.0)

        if "conductivity" in X.columns and "turbidity" in X.columns:
            X["cond_to_turb_ratio"] = X["conductivity"] / (X["turbidity"] + 1e-4)

        # Drop initial rows containing NaN from maximum lag
        max_lag = max(lags)
        X_clean = X.iloc[max_lag:].reset_index(drop=True)
        logger.info(
            f"Engineered Track A features: Shape evolved from {df.shape} to {X_clean.shape}"
        )
        return X_clean

    @staticmethod
    def generate_feature_catalog_markdown(output_path: str | Path) -> None:
        """Generates FEATURE_DEFINITIONS.md documentation describing raw vs engineered features."""
        catalog = """# Feature Definitions & Predictive Lineage Documentation

## 1. Track B: Static Physicochemical Water Features

| Feature Name | Origin | Physical Unit | Domain Range | Formulation / Rationale | Available at Inference? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ph` | Raw | Dimensionless | 0.0 - 14.0 | Acid-base equilibrium. | Yes |
| `Hardness` | Raw | mg/L CaCO3 | 40 - 450 | Polyvalent cations (Ca2+, Mg2+). | Yes |
| `Solids` | Raw | ppm | 100 - 60000 | Total dissolved mineral content. | Yes |
| `Chloramines` | Raw | ppm | 0.0 - 15.0 | Disinfection byproducts. | Yes |
| `Sulfate` | Raw | mg/L | 20 - 600 | Dissolved sulfate minerals. | Yes |
| `Conductivity` | Raw | uS/cm | 50 - 1000 | Ionic mobility index. | Yes |
| `Organic_carbon` | Raw | ppm | 1.0 - 35.0 | Total dissolved organic matter. | Yes |
| `Trihalomethanes` | Raw | ug/L | 0.0 - 150.0 | Volatile halogenated byproducts. | Yes |
| `Turbidity` | Raw | NTU | 0.0 - 10.0 | Light scattering suspended matter. | Yes |
| `solids_log1p` | Engineered | log(ppm) | 4.6 - 11.0 | `log1p(Solids)` to stabilize heavy right tail. | Yes |
| `sulfate_to_conductivity` | Engineered | Ratio | 0.0 - 5.0 | `Sulfate / Conductivity` proxy for sulfate mineral fraction. | Yes |
| `organic_to_solids` | Engineered | Ratio | 0.0 - 0.01 | Dissolved carbon proportion of total solids. | Yes |
| `hardness_to_solids` | Engineered | Ratio | 0.0 - 0.5 | Hardness cation fraction. | Yes |
| `chloramines_x_turbidity`| Engineered | Interaction | 0.0 - 100.0 | Disinfectant shielding interaction. | Yes |
| `ph_dev_neutral` | Engineered | Absolute delta| 0.0 - 7.0 | `abs(ph - 7.0)` measures deviation from neutral. | Yes |
| `ph_who_out_of_bounds` | Engineered | Binary | {0, 1} | 1 if pH < 6.5 or pH > 8.5 (WHO violation). | Yes |
| `turbidity_who_excess` | Engineered | Binary | {0, 1} | 1 if Turbidity > 5.0 NTU. | Yes |
| `chloramines_who_excess`| Engineered | Binary | {0, 1} | 1 if Chloramines > 4.0 ppm. | Yes |

---

## 2. Track A: Underwater Environmental Stream Features

| Feature Name | Origin | Physical Unit | Description | Available at Inference? |
| :--- | :--- | :--- | :--- | :--- |
| `temperature` | Raw | deg C | Water sensor temperature. | Yes |
| `dissolved_oxygen` | Raw | mg/L | Dissolved oxygen concentration. | Yes |
| `pressure` | Raw | dbar | Hydrostatic water column pressure. | Yes |
| `hour_sin`, `hour_cos` | Engineered | Periodic | Diurnal Fourier encoding of timestamp hour. | Yes |
| `*_lag_k` | Engineered | Sensor units | Past observation at $t-k$ hours. | Yes |
| `*_roll_mean_w` | Engineered | Sensor units | Past rolling average over window $w$ (closed='left'). | Yes |
| `*_roll_std_w` | Engineered | Sensor units | Past rolling volatility over window $w$ (closed='left'). | Yes |
| `do_to_temp_ratio` | Engineered | Ratio | Solubility equilibrium proxy ($DO / (T + 20)$). | Yes |
"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(catalog)
        logger.info(f"Feature definitions catalog generated at {path}")
