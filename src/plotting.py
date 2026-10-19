"""Plotting module: Matplotlib & Seaborn visualization suite for environmental telemetry and model diagnostics."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.calibration import calibration_curve
from sklearn.metrics import precision_recall_curve

from src.utils import ensure_dir, get_logger

logger = get_logger("Plotting")

# Set global clean aesthetic
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams["font.size"] = 10
plt.rcParams["figure.autolayout"] = True


def _save_or_show(fig: plt.Figure, save_path: str | Path | None = None) -> None:
    if save_path:
        p = Path(save_path)
        ensure_dir(p.parent)
        fig.savefig(p, dpi=300, bbox_inches="tight")
        logger.info(f"Saved figure to {p}")
        plt.close(fig)
    else:
        plt.close(fig)


def plot_sensor_streams(
    df: pd.DataFrame,
    sensors: list[str],
    timestamp_col: str = "timestamp",
    title: str = "Underwater Sensor Telemetry Time Series",
    save_path: str | Path | None = None,
) -> None:
    """Plots multi-panel time-series plots for continuous telemetry streams."""
    n_sensors = len(sensors)
    fig, axes = plt.subplots(n_sensors, 1, figsize=(12, 2.5 * n_sensors), sharex=True)
    if n_sensors == 1:
        axes = [axes]

    ts = pd.to_datetime(df[timestamp_col]) if timestamp_col in df else np.arange(len(df))

    palette = sns.color_palette("tab10", n_sensors)
    for ax, sensor, color in zip(axes, sensors, palette, strict=False):
        if sensor in df.columns:
            ax.plot(ts, df[sensor], label=sensor, color=color, linewidth=1.5)
            ax.set_ylabel(sensor, fontweight="bold")
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.legend(loc="upper right")

    axes[-1].set_xlabel("Timestamp")
    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.00)
    _save_or_show(fig, save_path)


def plot_correlation_heatmap(
    df: pd.DataFrame,
    cols: list[str] | None = None,
    title: str = "Sensor Cross-Correlation Matrix",
    save_path: str | Path | None = None,
) -> None:
    """Renders lower-triangle correlation heatmap with numerical annotations."""
    target_cols = cols or df.select_dtypes(include=[np.number]).columns
    corr = df[target_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        ax=ax,
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    _save_or_show(fig, save_path)


def plot_distributions(
    df: pd.DataFrame,
    cols: list[str],
    title: str = "Sensor Value Density Distributions",
    save_path: str | Path | None = None,
) -> None:
    """Plots KDE distribution histograms across sensor columns."""
    n = len(cols)
    cols_per_row = 3
    rows = (n + cols_per_row - 1) // cols_per_row
    fig, axes = plt.subplots(rows, cols_per_row, figsize=(14, 3.5 * rows))
    axes_flat = axes.flatten() if rows > 1 else axes

    for i, col in enumerate(cols):
        ax = axes_flat[i]
        if col in df.columns:
            sns.histplot(df[col].dropna(), kde=True, ax=ax, color="#2980b9", edgecolor="black")
            ax.set_title(f"Distribution: {col}", fontweight="bold")
            ax.grid(True, linestyle="--", alpha=0.5)

    for j in range(i + 1, len(axes_flat)):
        fig.delaxes(axes_flat[j])

    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.01)
    _save_or_show(fig, save_path)


def plot_anomalies(
    df: pd.DataFrame,
    sensor: str,
    anomaly_flags: np.ndarray,
    timestamp_col: str = "timestamp",
    title: str = "Detected Sensor Stream Anomalies",
    save_path: str | Path | None = None,
) -> None:
    """Plots sensor stream overlay with red scatter highlights on anomalous steps."""
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ts = pd.to_datetime(df[timestamp_col]) if timestamp_col in df else np.arange(len(df))
    vals = df[sensor].values

    ax.plot(ts, vals, label=sensor, color="#2c3e50", linewidth=1.2)
    anom_idx = np.where(anomaly_flags == 1)[0]
    if len(anom_idx) > 0:
        ax.scatter(
            ts.iloc[anom_idx] if hasattr(ts, "iloc") else ts[anom_idx],
            vals[anom_idx],
            color="#e74c3c",
            label=f"Anomaly (N={len(anom_idx)})",
            s=40,
            zorder=5,
        )

    ax.set_title(f"{title}: {sensor}", fontsize=12, fontweight="bold")
    ax.set_ylabel(sensor)
    ax.legend(loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.6)
    _save_or_show(fig, save_path)


def plot_predicted_vs_actual(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    sensor_name: str,
    lead_step: int = 1,
    title: str = "Forecasted vs Actual Sensor Values",
    save_path: str | Path | None = None,
) -> None:
    """Plots time-series predicted trajectory against observed sensor truth."""
    fig, ax = plt.subplots(figsize=(12, 4.5))
    yt = y_true[:, lead_step - 1] if y_true.ndim > 1 else y_true
    yp = y_pred[:, lead_step - 1] if y_pred.ndim > 1 else y_pred
    steps = np.arange(len(yt))

    ax.plot(steps, yt, label="Actual Observed", color="#34495e", linewidth=1.5)
    ax.plot(
        steps,
        yp,
        label=f"Forecast (T+{lead_step}h)",
        color="#e67e22",
        linestyle="--",
        linewidth=1.5,
    )

    ax.set_title(f"{title} ({sensor_name})", fontsize=12, fontweight="bold")
    ax.set_xlabel("Time Step")
    ax.set_ylabel(sensor_name)
    ax.legend(loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.6)
    _save_or_show(fig, save_path)


def plot_pr_and_calibration(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    model_name: str = "Classifier",
    save_path: str | Path | None = None,
) -> None:
    """Renders side-by-side Precision-Recall curve and Reliability Calibration plot."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    y_p = y_prob[:, 1] if y_prob.ndim > 1 else y_prob

    # 1. PR curve
    precision, recall, _ = precision_recall_curve(y_true, y_p)
    axes[0].plot(recall, precision, color="#2980b9", lw=2, label=f"{model_name}")
    no_skill = np.mean(y_true)
    axes[0].axhline(no_skill, color="red", linestyle="--", label=f"No Skill ({no_skill:.2f})")
    axes[0].set_xlabel("Recall")
    axes[0].set_ylabel("Precision")
    axes[0].set_title(f"Precision-Recall Curve ({model_name})", fontweight="bold")
    axes[0].legend(loc="best")
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # 2. Calibration curve
    prob_true, prob_pred = calibration_curve(y_true, y_p, n_bins=10)
    axes[1].plot(prob_pred, prob_true, marker="o", color="#27ae60", label=f"{model_name}")
    axes[1].plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfect Calibration")
    axes[1].set_xlabel("Mean Predicted Probability")
    axes[1].set_ylabel("Fraction of Positives")
    axes[1].set_title("Reliability Calibration Curve", fontweight="bold")
    axes[1].legend(loc="best")
    axes[1].grid(True, linestyle="--", alpha=0.5)

    fig.suptitle(
        f"Model Diagnostic Validation: {model_name}", fontsize=13, fontweight="bold", y=1.02
    )
    _save_or_show(fig, save_path)


def plot_ablation_tornado(
    ablation_df: pd.DataFrame,
    metric_col: str = "delta_mae",
    save_path: str | Path | None = None,
) -> None:
    """Plots horizontal bar chart ranking feature performance sensitivity."""
    fig, ax = plt.subplots(figsize=(9, 5))
    sorted_df = ablation_df.sort_values(by=metric_col, ascending=True)

    colors = ["#e74c3c" if v > 0 else "#2ecc71" for v in sorted_df[metric_col]]
    ax.barh(sorted_df["feature"], sorted_df[metric_col], color=colors, edgecolor="black")
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel(f"Sensitivity Impact ({metric_col})", fontweight="bold")
    ax.set_title(
        "Feature & Sensor Ablation Sensitivity Ranking (LOFO)", fontsize=12, fontweight="bold"
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    _save_or_show(fig, save_path)
