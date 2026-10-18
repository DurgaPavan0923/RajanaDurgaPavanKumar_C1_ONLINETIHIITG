"""Data Quality Audit Module for Water Monitoring Telemetry and Tabular Datasets."""

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from src.logger import get_logger

logger = get_logger("DataQualityAuditor")


class DataQualityAuditor:
    """Performs rigorous sensor-wise data quality audits, range checks, gap analysis, and drift metrics."""

    DEFAULT_RANGES = {
        "ph": (0.0, 14.0),
        "Hardness": (10.0, 500.0),
        "Solids": (100.0, 100000.0),
        "Chloramines": (0.0, 25.0),
        "Sulfate": (10.0, 800.0),
        "Conductivity": (10.0, 2000.0),
        "Organic_carbon": (0.0, 50.0),
        "Trihalomethanes": (0.0, 250.0),
        "Turbidity": (0.0, 25.0),
        "temperature": (-5.0, 50.0),
        "dissolved_oxygen": (0.0, 25.0),
        "pressure": (0.0, 600.0),
    }

    def __init__(self, custom_ranges: dict[str, tuple[float, float]] | None = None) -> None:
        self.ranges = self.DEFAULT_RANGES.copy()
        if custom_ranges:
            self.ranges.update(custom_ranges)

    def audit_tabular(self, df: pd.DataFrame, target_col: str | None = None) -> dict[str, Any]:
        """Audits tabular dataset (Track B or static features)."""
        total_rows = len(df)
        total_duplicates = int(df.duplicated().sum())

        sensor_metrics = []
        for col in df.columns:
            if col == target_col:
                continue

            series = df[col]
            missing_count = int(series.isna().sum())
            missing_pct = round((missing_count / total_rows) * 100, 2)

            valid_min, valid_max = self.ranges.get(col, (-np.inf, np.inf))
            numeric_series = pd.to_numeric(series.dropna(), errors="coerce")

            invalid_bound_count = int(
                ((numeric_series < valid_min) | (numeric_series > valid_max)).sum()
            )

            # IQR Outlier count
            q25 = float(numeric_series.quantile(0.25)) if len(numeric_series) else 0.0
            q75 = float(numeric_series.quantile(0.75)) if len(numeric_series) else 0.0
            iqr = q75 - q25
            lower_fence = q25 - 1.5 * iqr
            upper_fence = q75 + 1.5 * iqr
            outlier_count = int(
                ((numeric_series < lower_fence) | (numeric_series > upper_fence)).sum()
            )

            # Drift check: KS-statistic between first half and second half
            half = len(numeric_series) // 2
            if half > 20:
                ks_stat, p_val = stats.ks_2samp(
                    numeric_series.iloc[:half], numeric_series.iloc[half:]
                )
                ks_stat = round(float(ks_stat), 4)
                p_val = round(float(p_val), 4)
            else:
                ks_stat, p_val = 0.0, 1.0

            sensor_metrics.append(
                {
                    "sensor_or_feature": col,
                    "missing_count": missing_count,
                    "missing_pct": missing_pct,
                    "out_of_bounds_count": invalid_bound_count,
                    "iqr_outlier_count": outlier_count,
                    "mean": round(float(numeric_series.mean()), 3) if len(numeric_series) else None,
                    "std": round(float(numeric_series.std()), 3) if len(numeric_series) else None,
                    "min": round(float(numeric_series.min()), 3) if len(numeric_series) else None,
                    "max": round(float(numeric_series.max()), 3) if len(numeric_series) else None,
                    "half_split_ks_stat": ks_stat,
                    "half_split_p_val": p_val,
                }
            )

        audit_table = pd.DataFrame(sensor_metrics)
        return {
            "total_rows": total_rows,
            "duplicate_rows": total_duplicates,
            "sensor_table": audit_table,
            "target_distribution": df[target_col].value_counts(normalize=True).to_dict()
            if target_col and target_col in df
            else None,
        }

    def audit_temporal(
        self,
        df: pd.DataFrame,
        timestamp_col: str,
        expected_interval_seconds: int = 3600,
    ) -> dict[str, Any]:
        """Audits temporal stream (Track A) including sampling jitter and gap detection."""
        tabular_summary = self.audit_tabular(df, target_col=timestamp_col)

        ts = pd.to_datetime(df[timestamp_col], errors="coerce").dropna().sort_values()
        deltas = ts.diff().dt.total_seconds().dropna()

        mean_delta = float(deltas.mean()) if len(deltas) else 0.0
        std_delta = float(deltas.std()) if len(deltas) else 0.0
        jitter_ratio = round(std_delta / (mean_delta + 1e-9), 4)

        # Detect gaps > 2x expected interval
        gaps = deltas[deltas > (2 * expected_interval_seconds)]
        gap_count = len(gaps)
        max_gap_hours = round(float(deltas.max() / 3600.0), 2) if len(deltas) else 0.0

        temporal_summary = {
            **tabular_summary,
            "timestamp_start": str(ts.iloc[0]) if len(ts) else None,
            "timestamp_end": str(ts.iloc[-1]) if len(ts) else None,
            "total_timesteps": len(ts),
            "mean_interval_sec": round(mean_delta, 1),
            "interval_jitter_ratio": jitter_ratio,
            "sampling_gaps_count": gap_count,
            "max_gap_hours": max_gap_hours,
        }
        return temporal_summary

    @staticmethod
    def export_reports(
        audit_result: dict[str, Any], output_prefix: str | Path
    ) -> tuple[Path, Path]:
        """Exports audit summary to CSV and Markdown tables."""
        prefix = Path(output_prefix)
        prefix.parent.mkdir(parents=True, exist_ok=True)

        csv_path = prefix.with_suffix(".csv")
        md_path = prefix.with_suffix(".md")

        sensor_table: pd.DataFrame = audit_result["sensor_table"]
        sensor_table.to_csv(csv_path, index=False)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Water Quality Telemetry & Sensor Audit Report\n\n")
            f.write(f"- **Total Rows Evaluated:** {audit_result['total_rows']}\n")
            f.write(f"- **Duplicate Rows:** {audit_result['duplicate_rows']}\n")
            if "total_timesteps" in audit_result:
                f.write(
                    f"- **Temporal Duration:** {audit_result.get('timestamp_start')} to {audit_result.get('timestamp_end')}\n"
                )
                f.write(
                    f"- **Mean Sampling Interval:** {audit_result.get('mean_interval_sec')} sec (Jitter ratio: {audit_result.get('interval_jitter_ratio')})\n"
                )
                f.write(
                    f"- **Sampling Gaps (>2x interval):** {audit_result.get('sampling_gaps_count')} (Max gap: {audit_result.get('max_gap_hours')} hrs)\n"
                )
            if audit_result.get("target_distribution"):
                f.write(f"- **Target Class Distribution:** {audit_result['target_distribution']}\n")

            f.write("\n## Sensor & Feature Integrity Metrics\n\n")
            f.write(sensor_table.to_markdown(index=False))
            f.write("\n")

        logger.info(f"Audit reports successfully exported to {csv_path} and {md_path}")
        return csv_path, md_path
