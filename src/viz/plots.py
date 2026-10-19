"""Visualization Suite: Anomaly timelines, Forecasts vs Actuals, PR Curves, and Calibration Plots."""

from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import auc, precision_recall_curve

from src.logger import get_logger

logger = get_logger("VisualizationSuite")


class VisualizationSuite:
    """Generates publication-quality diagnostic and reporting plots."""

    @staticmethod
    def plot_anomaly_timeline(
        timestamps: pd.Series,
        sensor_values: pd.Series,
        anomaly_flags: np.ndarray,
        sensor_name: str,
        output_path: str | Path | None = None,
    ) -> None:
        """Plots time-series sensor trajectory with superimposed anomaly flags."""
        plt.figure(figsize=(12, 4))
        plt.plot(
            timestamps, sensor_values, label=f"Sensor: {sensor_name}", color="#1f77b4", alpha=0.85
        )

        anom_idx = np.where(anomaly_flags == 1)[0]
        if len(anom_idx) > 0:
            plt.scatter(
                timestamps.iloc[anom_idx],
                sensor_values.iloc[anom_idx],
                color="red",
                label="Anomaly Event",
                zorder=5,
                s=40,
                edgecolor="black",
            )

        plt.title(f"Underwater Environmental Sensor Stream & Anomaly Events ({sensor_name})")
        plt.xlabel("Timestamp (UTC)")
        plt.ylabel(sensor_name)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(out, dpi=300)
            logger.info(f"Anomaly plot saved to {out}")
        plt.close()

    @staticmethod
    def plot_forecast_vs_actual(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensor_name: str,
        output_path: str | Path | None = None,
    ) -> None:
        """Plots true vs predicted sensor forecasting timeline on chronological holdout."""
        plt.figure(figsize=(10, 4))
        indices = np.arange(len(y_true))
        plt.plot(indices, y_true, label=f"Actual {sensor_name}", color="black", linewidth=1.5)
        plt.plot(
            indices,
            y_pred,
            label=f"Forecasted {sensor_name}",
            color="#ff7f0e",
            linestyle="--",
            linewidth=1.8,
        )

        plt.title(f"Chronological Forecast vs Ground Truth ({sensor_name})")
        plt.xlabel("Time Step (Holdout Steps)")
        plt.ylabel(sensor_name)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(out, dpi=300)
            logger.info(f"Forecast plot saved to {out}")
        plt.close()

    @staticmethod
    def plot_precision_recall_curve(
        y_true: np.ndarray,
        y_prob: np.ndarray,
        model_name: str,
        output_path: str | Path | None = None,
        ax: Any = None,
    ) -> None:
        """Plots Precision-Recall curve and computes PR-AUC."""
        prec, rec, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = auc(rec, prec)

        target_ax = ax
        if target_ax is None:
            _, target_ax = plt.subplots(figsize=(6, 5))

        target_ax.plot(
            rec, prec, color="#2ca02c", lw=2, label=f"{model_name} (PR-AUC = {pr_auc:.3f})"
        )
        target_ax.set_xlabel("Recall")
        target_ax.set_ylabel("Precision")
        target_ax.set_title(f"Precision-Recall Curve - {model_name}")
        target_ax.grid(True, linestyle="--", alpha=0.5)
        target_ax.legend(loc="lower left")

        if ax is None:
            plt.tight_layout()
            if output_path:
                out = Path(output_path)
                out.parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(out, dpi=300)
                logger.info(f"PR curve plot saved to {out}")
            plt.close()

    @staticmethod
    def plot_calibration_curve(
        y_true: np.ndarray,
        y_prob: np.ndarray,
        model_name: str,
        output_path: str | Path | None = None,
        ax: Any = None,
    ) -> None:
        """Plots reliability calibration curve comparing empirical probability to predicted probability."""
        prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)

        target_ax = ax
        if target_ax is None:
            _, target_ax = plt.subplots(figsize=(6, 5))

        target_ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfect Calibration")
        target_ax.plot(prob_pred, prob_true, marker="o", color="#9467bd", label=model_name)
        target_ax.set_xlabel("Mean Predicted Probability")
        target_ax.set_ylabel("Fraction of Positives (Empirical Risk)")
        target_ax.set_title(f"Reliability Calibration Curve - {model_name}")
        target_ax.grid(True, linestyle="--", alpha=0.5)
        target_ax.legend(loc="upper left")

        if ax is None:
            plt.tight_layout()
            if output_path:
                out = Path(output_path)
                out.parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(out, dpi=300)
                logger.info(f"Calibration plot saved to {out}")
            plt.close()

    @staticmethod
    def plot_feature_importances(
        feature_names: list[str],
        importances: np.ndarray,
        top_k: int = 12,
        output_path: str | Path | None = None,
        ax: Any = None,
    ) -> None:
        """Plots horizontal bar chart of top K feature importances."""
        df_imp = pd.DataFrame({"feature": feature_names, "importance": importances})
        df_imp = df_imp.sort_values(by="importance", ascending=True).tail(top_k)

        target_ax = ax
        if target_ax is None:
            _, target_ax = plt.subplots(figsize=(8, 5))

        target_ax.barh(df_imp["feature"], df_imp["importance"], color="#17becf")
        target_ax.set_xlabel("Relative Importance Metric")
        target_ax.set_title(f"Top {top_k} Most Informative Chemical Indicators")
        target_ax.grid(True, linestyle="--", alpha=0.5)

        if ax is None:
            plt.tight_layout()
            if output_path:
                out = Path(output_path)
                out.parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(out, dpi=300)
                logger.info(f"Feature importance plot saved to {out}")
            plt.close()
