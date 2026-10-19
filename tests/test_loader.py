"""Unit tests for DataLoader, cryptographic checksums, and track detection."""

import pandas as pd

from src.data.loader import DataLoader


def test_track_b_auto_detection():
    df = pd.DataFrame(
        {
            "ph": [7.0, 8.0],
            "Hardness": [200.0, 210.0],
            "Solids": [20000.0, 21000.0],
            "Chloramines": [7.0, 7.5],
            "Sulfate": [300.0, 310.0],
            "Conductivity": [400.0, 420.0],
            "Turbidity": [3.0, 3.2],
        }
    )
    track, ts_col = DataLoader.detect_track(df)
    assert track == "B"
    assert ts_col is None


def test_track_a_auto_detection():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-08-20", periods=50, freq="h"),
            "temperature": [18.0 + i * 0.1 for i in range(50)],
            "dissolved_oxygen": [9.0 for _ in range(50)],
        }
    )
    track, ts_col = DataLoader.detect_track(df)
    assert track == "A"
    assert ts_col == "timestamp"


def test_shuffled_timestamps_fallback_to_track_b():
    # Non-monotonic shuffled timestamps
    dates = ["2026-08-25", "2026-08-20", "2026-08-22", "2026-08-10"]
    df = pd.DataFrame({"timestamp": dates, "val": [1, 2, 3, 4]})
    track, ts_col = DataLoader.detect_track(df)
    assert track == "B"
    assert ts_col is None


def test_checksum_verification(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("water quality test payload", encoding="utf-8")
    actual_sha = DataLoader.compute_sha256(test_file)
    assert DataLoader.verify_checksum(test_file, actual_sha) is True
    assert DataLoader.verify_checksum(test_file, "wrong_hash") is False
