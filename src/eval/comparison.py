"""Model Comparison Engine: Unifies Statistical Metrics, Latency, and Memory Footprint."""

import os
import tempfile
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.eval.metrics import EvaluationMetrics
from src.logger import get_logger

logger = get_logger("ModelComparisonEngine")


class ModelComparisonEngine:
    """Builds unified multi-model comparison matrices covering accuracy, latency, and artifact size."""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    @staticmethod
    def measure_artifact_size_kb(model_object: Any) -> float:
        """Serializes model temporarily to calculate exact disk size in kilobytes."""
        with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            joblib.dump(model_object, tmp_path)
            size_kb = os.path.getsize(tmp_path) / 1024.0
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        return round(size_kb, 2)

    def add_model_evaluation(
        self,
        model_name: str,
        track: str,
        task: str,
        metrics: dict[str, float],
        model_object: Any,
        X_sample: Any,
    ) -> None:
        """Measures latency, artifact size, and compiles record."""
        speed_stats = EvaluationMetrics.measure_inference_speed(model_object, X_sample)
        size_kb = self.measure_artifact_size_kb(model_object)

        entry = {
            "model_name": model_name,
            "track": track,
            "task": task,
            **metrics,
            "latency_ms_per_sample": speed_stats["per_sample_latency_ms"],
            "model_size_kb": size_kb,
        }
        self.records.append(entry)

    def get_comparison_dataframe(self) -> pd.DataFrame:
        """Returns consolidated Pandas DataFrame."""
        return pd.DataFrame(self.records)

    def export_comparison(self, output_prefix: str | Path) -> tuple[Path, Path]:
        """Exports comparison to CSV and Markdown tables."""
        prefix = Path(output_prefix)
        prefix.parent.mkdir(parents=True, exist_ok=True)

        csv_path = prefix.with_suffix(".csv")
        md_path = prefix.with_suffix(".md")

        df = self.get_comparison_dataframe()
        df.to_csv(csv_path, index=False)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Model Performance, Latency & Artifact Size Leaderboard\n\n")
            f.write(df.to_markdown(index=False))
            f.write("\n")

        logger.info(f"Comparison leaderboard exported to {csv_path} and {md_path}")
        return csv_path, md_path
