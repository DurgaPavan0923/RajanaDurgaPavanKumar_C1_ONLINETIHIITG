"""Unsupervised Anomaly Detection Models: Isolation Forest and Local Outlier Factor."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from src.logger import get_logger

logger = get_logger("AnomalyDetector")


class IsolationForestAnomalyDetector(BaseEstimator):
    """Isolation Forest anomaly detection wrapper with standardized outputs."""

    def __init__(
        self,
        contamination: float = 0.05,
        n_estimators: int = 150,
        random_state: int = 42,
    ) -> None:
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            n_jobs=-1,
        )

    def fit(self, X: np.ndarray | pd.DataFrame, y: Any = None) -> "IsolationForestAnomalyDetector":
        self.model.fit(X)
        return self

    def score_samples(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns anomaly score where higher values indicate higher abnormality."""
        # Sklearn returns negative scores (lower is more anomalous); invert so higher = more anomalous
        raw_scores = self.model.score_samples(X)
        return -raw_scores

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns 1 for anomaly, 0 for inlier."""
        raw_preds = self.model.predict(X)  # 1 for inlier, -1 for outlier
        return np.where(raw_preds == -1, 1, 0)


class LOFAnomalyDetector(BaseEstimator):
    """Local Outlier Factor wrapper for density-based anomaly detection."""

    def __init__(self, n_neighbors: int = 20, contamination: float = 0.05) -> None:
        self.n_neighbors = n_neighbors
        self.contamination = contamination
        self.model = LocalOutlierFactor(
            n_neighbors=self.n_neighbors,
            contamination=self.contamination,
            novelty=True,
            n_jobs=-1,
        )

    def fit(self, X: np.ndarray | pd.DataFrame, y: Any = None) -> "LOFAnomalyDetector":
        self.model.fit(X)
        return self

    def score_samples(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns anomaly score where higher values indicate higher abnormality."""
        return -self.model.score_samples(X)

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        raw_preds = self.model.predict(X)
        return np.where(raw_preds == -1, 1, 0)
