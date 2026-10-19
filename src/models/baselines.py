"""Baseline Estimators: WHO Deterministic Rules, Z-Score Outlier, and Persistence Forecaster."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin

from src.logger import get_logger

logger = get_logger("Baselines")


class WHORuleClassifier(BaseEstimator, ClassifierMixin):
    """Deterministic Domain Baseline: Classifies water potability using WHO/EPA chemical thresholds.

    Zero trainable parameters. Serves as ground-truth regulatory benchmark.
    """

    WHO_LIMITS = {
        "ph": (6.5, 8.5),
        "Hardness": (0.0, 300.0),
        "Solids": (0.0, 1000.0),
        "Chloramines": (0.0, 4.0),
        "Sulfate": (0.0, 250.0),
        "Conductivity": (0.0, 400.0),
        "Organic_carbon": (0.0, 4.0),
        "Trihalomethanes": (0.0, 80.0),
        "Turbidity": (0.0, 5.0),
    }

    def __init__(self, limits: dict[str, tuple[float, float]] | None = None) -> None:
        self.limits = limits or self.WHO_LIMITS.copy()
        self.classes_ = np.array([0, 1])

    def fit(self, X: Any, y: Any = None) -> "WHORuleClassifier":
        return self

    def predict_violations(self, X: pd.DataFrame | np.ndarray) -> list[list[str]]:
        """Returns list of specific WHO guideline violations per sample."""
        if isinstance(X, np.ndarray):
            cols = list(self.limits.keys())[: X.shape[1]]
            X_df = pd.DataFrame(X, columns=cols)
        else:
            X_df = X

        all_violations = []
        for _, row in X_df.iterrows():
            row_violations = []
            for col, (low, high) in self.limits.items():
                if col in row and pd.notna(row[col]):
                    val = float(row[col])
                    if val < low or val > high:
                        row_violations.append(f"{col}={val:.1f} out of [{low}, {high}]")
            all_violations.append(row_violations)
        return all_violations

    def predict(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Predicts potability (1 = potable, 0 = non-potable) using vectorized boolean masking."""
        if isinstance(X, np.ndarray):
            cols = list(self.limits.keys())[: X.shape[1]]
            X_df = pd.DataFrame(X, columns=cols)
        else:
            X_df = X

        compliant_mask = pd.Series(True, index=X_df.index)
        for col, (low, high) in self.limits.items():
            if col in X_df.columns:
                series = X_df[col]
                valid = series.isna() | ((series >= low) & (series <= high))
                compliant_mask &= valid
        return compliant_mask.astype(int).values

    def predict_proba(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Returns pseudo-probabilities based on fraction of compliant parameters."""
        if isinstance(X, np.ndarray):
            cols = list(self.limits.keys())[: X.shape[1]]
            X_df = pd.DataFrame(X, columns=cols)
        else:
            X_df = X

        probas = []
        for _, row in X_df.iterrows():
            total_checked = 0
            compliant = 0
            for col, (low, high) in self.limits.items():
                if col in row and pd.notna(row[col]):
                    total_checked += 1
                    val = float(row[col])
                    if low <= val <= high:
                        compliant += 1
            ratio = compliant / (total_checked + 1e-9)
            probas.append([1.0 - ratio, ratio])
        return np.array(probas)


class ZScoreAnomalyDetector(BaseEstimator):
    """Statistical Baseline Anomaly Detector using feature-wise Z-Scores."""

    def __init__(self, threshold: float = 3.0) -> None:
        self.threshold = threshold
        self.means_: np.ndarray | None = None
        self.stds_: np.ndarray | None = None

    def fit(self, X: np.ndarray | pd.DataFrame, y: Any = None) -> "ZScoreAnomalyDetector":
        X_mat = np.asarray(X, dtype=float)
        self.means_ = np.nanmean(X_mat, axis=0)
        self.stds_ = np.nanstd(X_mat, axis=0)
        self.stds_[self.stds_ < 1e-6] = 1.0  # Prevent division by zero
        return self

    def score_samples(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns maximum absolute Z-score across all features."""
        X_mat = np.asarray(X, dtype=float)
        z_scores = np.abs((X_mat - self.means_) / self.stds_)
        return np.nanmax(z_scores, axis=1)

    def predict(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Returns binary anomaly flag (1 = anomaly, 0 = normal)."""
        scores = self.score_samples(X)
        return (scores > self.threshold).astype(int)


class PersistenceForecaster(BaseEstimator):
    """Persistence baseline: forecasts that future value equals last observed value."""

    def __init__(self) -> None:
        pass

    def fit(self, X: Any, y: Any = None) -> "PersistenceForecaster":
        return self

    def predict(self, X: np.ndarray | pd.DataFrame, horizon: int = 1) -> np.ndarray:
        """Predicts last column value repeated across horizon."""
        X_mat = np.asarray(X)
        last_val = X_mat[:, -1]
        return np.tile(last_val[:, np.newaxis], (1, horizon))
