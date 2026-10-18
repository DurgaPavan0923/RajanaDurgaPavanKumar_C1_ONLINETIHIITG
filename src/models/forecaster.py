"""Forecasting Models for Track A Continuous Underwater Telemetry Streams."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge

try:
    import xgboost as xgb
except ImportError:
    xgb = None

from src.logger import get_logger

logger = get_logger("WaterQualityForecaster")


class WaterQualityForecaster(BaseEstimator):
    """Multi-model Forecaster supporting Ridge, Random Forest, and XGBoost for multi-step predictions."""

    SUPPORTED_MODELS = ["ridge", "random_forest", "xgboost"]

    def __init__(
        self,
        model_type: str = "xgboost",
        params: dict[str, Any] | None = None,
        random_state: int = 42,
    ) -> None:
        self.model_type = model_type.lower()
        self.params = params or {}
        self.random_state = random_state
        self.model: Any = None
        self._init_model()

    def _init_model(self) -> None:
        if self.model_type == "ridge":
            alpha = self.params.get("alpha", 1.0)
            self.model = Ridge(alpha=alpha, random_state=self.random_state)
        elif self.model_type == "random_forest":
            n_est = self.params.get("n_estimators", 150)
            depth = self.params.get("max_depth", 8)
            self.model = RandomForestRegressor(
                n_estimators=n_est,
                max_depth=depth,
                random_state=self.random_state,
                n_jobs=-1,
            )
        elif self.model_type == "xgboost":
            if xgb is None:
                raise ImportError(
                    "XGBoost is not installed in this environment. "
                    "Install xgboost or select 'random_forest' / 'ridge'."
                )
            n_est = self.params.get("n_estimators", 200)
            depth = self.params.get("max_depth", 5)
            lr = self.params.get("learning_rate", 0.05)
            self.model = xgb.XGBRegressor(
                n_estimators=n_est,
                max_depth=depth,
                learning_rate=lr,
                random_state=self.random_state,
                n_jobs=-1,
            )
        else:
            raise ValueError(
                f"Unsupported model_type: {self.model_type}. Must be one of {self.SUPPORTED_MODELS}"
            )

    def fit(
        self, X: np.ndarray | pd.DataFrame, y: np.ndarray | pd.Series
    ) -> "WaterQualityForecaster":
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

    @staticmethod
    def prepare_forecasting_targets(
        df: pd.DataFrame,
        target_col: str,
        horizon_steps: int = 6,
    ) -> tuple[pd.DataFrame, pd.Series]:
        """Aligns feature matrix with target shifted by horizon_steps into the future.

        y(t) = target_col(t + horizon_steps)
        """
        y = df[target_col].shift(-horizon_steps)
        valid_idx = ~y.isna()
        X_aligned = df.loc[valid_idx].copy()
        y_aligned = y.loc[valid_idx].copy()
        return X_aligned, y_aligned
