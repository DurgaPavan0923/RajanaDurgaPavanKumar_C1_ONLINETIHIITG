"""Evaluation module: Metrics computation, bootstrap confidence intervals, and comparison leaderboards."""

from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    auc,
    brier_score_loss,
    f1_score,
    fbeta_score,
    mean_absolute_error,
    mean_squared_error,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.utils import get_logger

logger = get_logger("Evaluation")


def compute_forecasting_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """Computes MAE, RMSE, MAPE, and Mean Directional Accuracy across multi-step horizon."""
    y_t = np.asarray(y_true, dtype=float)
    y_p = np.asarray(y_pred, dtype=float)

    if len(y_t) == 0 or len(y_p) == 0:
        return {"mae": 0.0, "rmse": 0.0, "mape_pct": 0.0, "mda_pct": 0.0}

    mae = float(mean_absolute_error(y_t, y_p))
    mse = float(mean_squared_error(y_t, y_p))
    rmse = float(np.sqrt(mse))

    # Safe MAPE avoiding division by zero
    non_zero_mask = np.abs(y_t) > 1e-4
    if np.any(non_zero_mask):
        mape = float(np.mean(np.abs((y_t[non_zero_mask] - y_p[non_zero_mask]) / y_t[non_zero_mask])) * 100)
    else:
        mape = 0.0

    # Mean Directional Accuracy (sign agreement)
    if y_t.ndim > 1 and y_t.shape[1] > 1:
        diff_true = np.diff(y_t, axis=1)
        diff_pred = np.diff(y_p, axis=1)
        mda = float(np.mean((diff_true * diff_pred) > 0) * 100)
    else:
        mda = 50.0

    return {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "mape_pct": round(mape, 2),
        "mda_pct": round(mda, 2),
    }


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray | None = None,
) -> dict[str, float]:
    """Computes full classification suite: PR-AUC, ROC-AUC, F1, F2, Brier score, and accuracy."""
    y_t = np.asarray(y_true, dtype=int)
    y_p = np.asarray(y_pred, dtype=int)

    if len(y_t) == 0 or len(y_p) == 0:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "f2_score": 0.0,
            "brier_score": 0.0,
            "roc_auc": 0.5,
            "pr_auc": 0.5,
        }

    acc = float(accuracy_score(y_t, y_p))
    prec = float(precision_score(y_t, y_p, zero_division=0))
    rec = float(recall_score(y_t, y_p, zero_division=0))
    f1 = float(f1_score(y_t, y_p, zero_division=0))
    f2 = float(fbeta_score(y_t, y_p, beta=2, zero_division=0))

    metrics = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "f2_score": round(f2, 4),
    }

    if y_prob is not None:
        y_pr = np.asarray(y_prob, dtype=float)
        if y_pr.ndim > 1:
            y_pr = y_pr[:, 1]
        metrics["brier_score"] = round(float(brier_score_loss(y_t, y_pr)), 4)
        if len(np.unique(y_t)) > 1:
            metrics["roc_auc"] = round(float(roc_auc_score(y_t, y_pr)), 4)
            precision_arr, recall_arr, _ = precision_recall_curve(y_t, y_pr)
            # Area under PR curve via trapezoidal rule
            metrics["pr_auc"] = round(float(auc(recall_arr, precision_arr)), 4)
        else:
            metrics["roc_auc"] = 0.5
            metrics["pr_auc"] = 0.5

    return metrics


def bootstrap_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metric_func: Callable[[np.ndarray, np.ndarray], float],
    n_bootstraps: int = 500,
    alpha: float = 0.05,
    seed: int = 42,
) -> tuple[float, float, float]:
    """Estimates empirical metric mean and (1-alpha) confidence interval via bootstrap resampling."""
    rng = np.random.default_rng(seed)
    n = len(y_true)
    boot_scores = []

    for _ in range(n_bootstraps):
        idxs = rng.choice(n, size=n, replace=True)
        score = metric_func(y_true[idxs], y_pred[idxs])
        boot_scores.append(score)

    mean_score = float(np.mean(boot_scores))
    lower = float(np.percentile(boot_scores, 100 * (alpha / 2)))
    upper = float(np.percentile(boot_scores, 100 * (1 - alpha / 2)))

    return round(mean_score, 4), round(lower, 4), round(upper, 4)


def build_comparison_table(results_list: list[dict[str, Any]]) -> pd.DataFrame:
    """Consolidates benchmark dictionaries into structured comparative table."""
    return pd.DataFrame(results_list)
