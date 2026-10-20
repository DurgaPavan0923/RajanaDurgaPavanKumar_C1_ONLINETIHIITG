"""Forecasting module: Multi-step persistence baseline, Ridge regression, and ensemble regressors."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.multioutput import MultiOutputRegressor

try:
    import xgboost as xgb
except (ImportError, OSError, Exception):
    xgb = None

from src.utils import get_logger

logger = get_logger("Forecasting")


def create_forecasting_dataset(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "dissolved_oxygen",
    horizon: int = 6,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generates (X_t, Y_{t+1 ... t+H}) supervised time-series pairs."""
    X_list, Y_list = [], []
    valid_df = df.dropna().reset_index(drop=True)
    n = len(valid_df)

    for i in range(n - horizon):
        X_list.append(valid_df.loc[i, feature_cols].values)
        Y_list.append(valid_df.loc[i + 1 : i + horizon, target_col].values)

    X_df = pd.DataFrame(X_list, columns=feature_cols)
    y_cols = [f"{target_col}_lead_{h}" for h in range(1, horizon + 1)]
    Y_df = pd.DataFrame(Y_list, columns=y_cols)

    return X_df, Y_df


class PersistenceForecaster(BaseEstimator):
    """Persistence Baseline: Predicts that future values equal the latest known observation."""

    def __init__(self, target_col_idx: int = 0, horizon: int = 6) -> None:
        self.target_col_idx = target_col_idx
        self.horizon = horizon

    def fit(self, X: Any, y: Any = None) -> "PersistenceForecaster":
        return self

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        X_mat = np.asarray(X)
        last_val = X_mat[:, self.target_col_idx]
        return np.tile(last_val[:, np.newaxis], (1, self.horizon))


class LinearRegressionForecaster(BaseEstimator):
    """Multi-output regularized Ridge regression forecaster."""

    def __init__(self, alpha: float = 1.0, random_state: int = 42) -> None:
        self.alpha = alpha
        self.random_state = random_state
        self.model = MultiOutputRegressor(Ridge(alpha=self.alpha, random_state=self.random_state))

    def fit(self, X: np.ndarray | pd.DataFrame, y: np.ndarray | pd.DataFrame) -> "LinearRegressionForecaster":
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)


class RandomForestForecaster(BaseEstimator):
    """Multi-output Random Forest ensemble forecaster."""

    def __init__(
        self,
        n_estimators: int = 150,
        max_depth: int = 8,
        random_state: int = 42,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            random_state=self.random_state,
            n_jobs=-1,
        )

    def fit(self, X: np.ndarray | pd.DataFrame, y: np.ndarray | pd.DataFrame) -> "RandomForestForecaster":
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)


class XGBoostForecaster(BaseEstimator):
    """Multi-output XGBoost gradient boosting forecaster with safe fallback."""

    def __init__(
        self,
        n_estimators: int = 150,
        max_depth: int = 5,
        learning_rate: float = 0.05,
        random_state: int = 42,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.random_state = random_state

        if xgb is not None:
            base = xgb.XGBRegressor(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                learning_rate=self.learning_rate,
                random_state=self.random_state,
                tree_method="hist",
                n_jobs=1,
            )
            self.model: Any = MultiOutputRegressor(base, n_jobs=-1)
        else:
            logger.warning("XGBoost not installed; falling back to RandomForestRegressor")
            self.model = RandomForestRegressor(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                random_state=self.random_state,
                n_jobs=-1,
            )

    def fit(self, X: np.ndarray | pd.DataFrame, y: np.ndarray | pd.DataFrame) -> "XGBoostForecaster":
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)
