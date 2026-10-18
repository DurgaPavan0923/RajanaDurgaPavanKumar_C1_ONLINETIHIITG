"""Supervised Water Potability Classification with Calibrated Probabilities."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

try:
    import xgboost as xgb
except ImportError:
    xgb = None

from src.logger import get_logger

logger = get_logger("WaterPotabilityClassifier")


class WaterPotabilityClassifier(BaseEstimator, ClassifierMixin):
    """Classifier wrapper supporting Logistic Regression, Random Forest, and XGBoost with Platt probability calibration."""

    SUPPORTED_MODELS = ["logistic_regression", "random_forest", "xgboost"]

    def __init__(
        self,
        model_name: str = "xgboost",
        params: dict[str, Any] | None = None,
        calibrate: bool = True,
        calibration_method: str = "sigmoid",
        random_state: int = 42,
    ) -> None:
        self.model_name = model_name.lower()
        self.params = params or {}
        self.calibrate = calibrate
        self.calibration_method = calibration_method
        self.random_state = random_state
        self.base_estimator: Any = None
        self.calibrated_model: Any = None
        self._init_base_estimator()

    def _init_base_estimator(self) -> None:
        if self.model_name == "logistic_regression":
            c = self.params.get("C", 1.0)
            max_iter = self.params.get("max_iter", 1000)
            self.base_estimator = LogisticRegression(
                C=c,
                max_iter=max_iter,
                class_weight="balanced",
                random_state=self.random_state,
            )
        elif self.model_name == "random_forest":
            n_est = self.params.get("n_estimators", 200)
            depth = self.params.get("max_depth", 8)
            min_samples = self.params.get("min_samples_leaf", 5)
            self.base_estimator = RandomForestClassifier(
                n_estimators=n_est,
                max_depth=depth,
                min_samples_leaf=min_samples,
                class_weight="balanced",
                random_state=self.random_state,
                n_jobs=-1,
            )
        elif self.model_name == "xgboost":
            if xgb is None:
                raise ImportError(
                    "XGBoost is not installed in this environment. "
                    "Install xgboost or select 'random_forest' / 'logistic_regression'."
                )
            n_est = self.params.get("n_estimators", 200)
            depth = self.params.get("max_depth", 4)
            lr = self.params.get("learning_rate", 0.05)
            subsample = self.params.get("subsample", 0.8)
            colsample = self.params.get("colsample_bytree", 0.8)
            scale_pos = self.params.get("scale_pos_weight", 1.56)
            self.base_estimator = xgb.XGBClassifier(
                n_estimators=n_est,
                max_depth=depth,
                learning_rate=lr,
                subsample=subsample,
                colsample_bytree=colsample,
                scale_pos_weight=scale_pos,
                random_state=self.random_state,
                eval_metric="logloss",
                n_jobs=-1,
            )
        else:
            raise ValueError(
                f"Unsupported model_name: {self.model_name}. Must be in {self.SUPPORTED_MODELS}"
            )

    def fit(
        self, X: np.ndarray | pd.DataFrame, y: np.ndarray | pd.Series
    ) -> "WaterPotabilityClassifier":
        if self.calibrate:
            # Calibrate probabilities using 5-fold internal cross-validation
            self.calibrated_model = CalibratedClassifierCV(
                estimator=self.base_estimator,
                method=self.calibration_method,
                cv=5,
            )
            self.calibrated_model.fit(X, y)
        else:
            self.base_estimator.fit(X, y)
        return self

    def predict(self, X: np.ndarray | pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        """Predicts binary potability using custom threshold."""
        probas = self.predict_proba(X)[:, 1]
        return (probas >= threshold).astype(int)

    def predict_proba(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns well-calibrated class probabilities [P(non-potable), P(potable)]."""
        if self.calibrate and self.calibrated_model is not None:
            return self.calibrated_model.predict_proba(X)
        return self.base_estimator.predict_proba(X)

    @property
    def classes_(self) -> np.ndarray:
        return np.array([0, 1])
