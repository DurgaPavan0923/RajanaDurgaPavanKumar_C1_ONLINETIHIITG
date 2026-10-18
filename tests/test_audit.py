"""Unit tests for DataQualityAuditor."""

import pandas as pd

from src.data.audit import DataQualityAuditor


def test_audit_tabular_bounds_and_missingness():
    df = pd.DataFrame(
        {
            "ph": [7.0, -1.0, 15.0, None],  # -1.0 and 15.0 out of [0, 14], 1 missing
            "Turbidity": [1.0, 2.0, 30.0, 4.0],  # 30.0 out of [0, 25]
            "Potability": [0, 1, 0, 1],
        }
    )
    auditor = DataQualityAuditor()
    res = auditor.audit_tabular(df, target_col="Potability")

    assert res["total_rows"] == 4
    table = res["sensor_table"].set_index("sensor_or_feature")

    assert table.loc["ph", "missing_count"] == 1
    assert table.loc["ph", "out_of_bounds_count"] == 2
    assert table.loc["Turbidity", "out_of_bounds_count"] == 1


def test_audit_temporal_jitter_and_gaps():
    ts = pd.date_range("2026-08-20", periods=10, freq="h").tolist()
    # Introduce a 5-hour gap
    ts.append(ts[-1] + pd.Timedelta(hours=5))
    df = pd.DataFrame(
        {
            "timestamp": ts,
            "temperature": [20.0] * len(ts),
        }
    )

    auditor = DataQualityAuditor()
    res = auditor.audit_temporal(df, timestamp_col="timestamp", expected_interval_seconds=3600)

    assert res["total_timesteps"] == 11
    assert res["sampling_gaps_count"] == 1
    assert res["max_gap_hours"] == 5.0
