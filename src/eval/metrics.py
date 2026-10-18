"""Comprehensive Evaluation Metrics for Classification, Forecasting, and Anomaly Detection."""

import time
from typing import Any

import numpy as np
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


class EvaluationMetrics:
    """Calculates statistical, domain, and operational performance metrics."""

    @staticmethod
    def evaluate_classification(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: np.ndarray | None = None,
    ) -> dict[str, float]:
        """Calculates classification metrics: Precision, Recall, F1, F2, PR-AUC, ROC-AUC, Brier score."""
        y_t = np.asarray(y_true).astype(int)
        y_p = np.asarray(y_pred).astype(int)

        metrics = {
            "accuracy": round(float(accuracy_score(y_t, y_p)), 4),
            "precision": round(float(precision_score(y_t, y_p, zero_division=0)), 4),
            "recall": round(float(recall_score(y_t, y_p, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_t, y_p, zero_division=0)), 4),
            "f2_score": round(float(fbeta_score(y_t, y_p, beta=2.0, zero_division=0)), 4),
        }

        if y_prob is not None:
            prob_pos = np.asarray(y_prob)
            if prob_pos.ndim > 1:
                prob_pos = prob_pos[:, 1]

            metrics["brier_score"] = round(float(brier_score_loss(y_t, prob_pos)), 4)
            try:
                metrics["roc_auc"] = round(float(roc_auc_score(y_t, prob_pos)), 4)
            except ValueError:
                metrics["roc_auc"] = 0.5

            prec, rec, _ = precision_recall_curve(y_t, prob_pos)
            metrics["pr_auc"] = round(float(auc(rec, prec)), 4)

        return metrics

    @staticmethod
    def evaluate_forecasting(
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> dict[str, float]:
        """Calculates regression metrics: MAE, RMSE, sMAPE, Directional Accuracy."""
        y_t = np.asarray(y_true).astype(float)
        y_p = np.asarray(y_pred).astype(float)

        mae = float(mean_absolute_error(y_t, y_p))
        rmse = float(np.sqrt(mean_squared_error(y_t, y_p)))

        # Symmetric Mean Absolute Percentage Error (sMAPE)
        denominator = (np.abs(y_t) + np.abs(y_p)) / 2.0
        diff = np.abs(y_p - y_t)
        valid = denominator > 1e-6
        smape = float(np.mean(diff[valid] / denominator[valid]) * 100.0) if np.any(valid) else 0.0

        # Directional accuracy
        if len(y_t) > 1:
            true_dir = np.sign(np.diff(y_t))
            pred_dir = np.sign(np.diff(y_p))
            dir_acc = float(np.mean(true_dir == pred_dir))
        else:
            dir_acc = 1.0

        return {
            "mae": round(mae, 4),
            "rmse": round(rmse, 4),
            "smape_pct": round(smape, 2),
            "directional_accuracy": round(dir_acc, 4),
        }

    @staticmethod
    def measure_inference_speed(
        model: Any,
        X_sample: np.ndarray,
        num_runs: int = 100,
    ) -> dict[str, float]:
        """Measures per-sample inference latency and throughput."""
        times = []
        for _ in range(num_runs):
            t0 = time.perf_counter()
            if hasattr(model, "predict_proba"):
                _ = model.predict_proba(X_sample)
            else:
                _ = model.predict(X_sample)
            t1 = time.perf_counter()
            times.append(t1 - t0)

        mean_batch_time_ms = float(np.mean(times) * 1000.0)
        per_sample_latency_ms = mean_batch_time_ms / max(1, len(X_sample))

        return {
            "batch_time_ms": round(mean_batch_time_ms, 3),
            "per_sample_latency_ms": round(per_sample_latency_ms, 4),
        }
