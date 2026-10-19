"""Anomaly detection module: Z-score, IQR fence baselines, and unsupervised Isolation Forest."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import IsolationForest

from src.utils import get_logger

logger = get_logger("Anomaly")


class ZScoreAnomalyDetector(BaseEstimator):
    """Statistical Baseline Anomaly Detector using feature-wise Z-Scores."""

    def __init__(self, threshold: float = 3.5) -> None:
        self.threshold = threshold
        self.means_: np.ndarray | None = None
        self.stds_: np.ndarray | None = None

    def fit(self, X: np.ndarray | pd.DataFrame, y: Any = None) -> "ZScoreAnomalyDetector":
        X_mat = np.asarray(X, dtype=float)
        self.means_ = np.nanmean(X_mat, axis=0)
        self.stds_ = np.nanstd(X_mat, axis=0)
        self.stds_[self.stds_ < 1e-6] = 1.0  # Avoid division by zero
        return self

    def score_samples(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns maximum absolute Z-score across features."""
        X_mat = np.asarray(X, dtype=float)
        z_scores = np.abs((X_mat - self.means_) / self.stds_)
        return np.nanmax(z_scores, axis=1)

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns 1 for anomaly, 0 for normal."""
        scores = self.score_samples(X)
        return (scores > self.threshold).astype(int)


class IQRAnomalyDetector(BaseEstimator):
    """Statistical Baseline Anomaly Detector using Tukey's 1.5 * IQR Fences."""

    def __init__(self, multiplier: float = 1.5) -> None:
        self.multiplier = multiplier
        self.q25_: np.ndarray | None = None
        self.q75_: np.ndarray | None = None
        self.iqr_: np.ndarray | None = None

    def fit(self, X: np.ndarray | pd.DataFrame, y: Any = None) -> "IQRAnomalyDetector":
        X_mat = np.asarray(X, dtype=float)
        self.q25_ = np.nanpercentile(X_mat, 25, axis=0)
        self.q75_ = np.nanpercentile(X_mat, 75, axis=0)
        self.iqr_ = self.q75_ - self.q25_
        self.iqr_[self.iqr_ < 1e-6] = 1.0
        return self

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        X_mat = np.asarray(X, dtype=float)
        lower_fence = self.q25_ - self.multiplier * self.iqr_
        upper_fence = self.q75_ + self.multiplier * self.iqr_
        viol = (X_mat < lower_fence) | (X_mat > upper_fence)
        return (np.nanmax(viol.astype(int), axis=1) > 0).astype(int)


class IsolationForestAnomalyDetector(BaseEstimator):
    """Unsupervised Isolation Forest for multivariate anomaly isolation."""

    def __init__(
        self,
        contamination: float = 0.02,
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
        """Returns normalized anomaly score (higher = more anomalous)."""
        raw_scores = -self.model.score_samples(X)
        return raw_scores

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns 1 for anomaly, 0 for normal (maps sklearn -1/1)."""
        preds = self.model.predict(X)
        return np.where(preds == -1, 1, 0)


def evaluate_anomaly_detection(
    detector: Any,
    X: np.ndarray | pd.DataFrame,
    y_true: np.ndarray | None = None,
) -> dict[str, Any]:
    """Computes anomaly detection rate, score stability, and P/R/F1 if ground truth available."""
    preds = detector.predict(X)
    detection_rate = float(np.mean(preds))
    has_scores = hasattr(detector, "score_samples")
    score_std = float(np.std(detector.score_samples(X))) if has_scores else 0.0

    metrics: dict[str, Any] = {
        "detection_rate": round(detection_rate, 4),
        "total_anomalies": int(np.sum(preds)),
        "score_std": round(score_std, 4),
    }

    if y_true is not None:
        from sklearn.metrics import f1_score, precision_score, recall_score

        metrics["precision"] = round(float(precision_score(y_true, preds, zero_division=0)), 4)
        metrics["recall"] = round(float(recall_score(y_true, preds, zero_division=0)), 4)
        metrics["f1_score"] = round(float(f1_score(y_true, preds, zero_division=0)), 4)

    return metrics
