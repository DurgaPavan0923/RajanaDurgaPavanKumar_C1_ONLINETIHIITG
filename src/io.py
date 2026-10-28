# ruff: noqa: A005
"""Input/Output module: Cryptographic checksums, raw data ingestion, and Parquet/joblib serialization."""

import hashlib
import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.utils import ensure_dir, get_logger

logger = get_logger("IO")


class ArtifactMissingError(FileNotFoundError):
    """Raised when an intern day prerequisite artifact is missing."""

    pass


def compute_sha256(filepath: str | Path) -> str:
    """Calculates SHA-256 hash of a file."""
    p = Path(filepath)
    if not p.exists():
        raise FileNotFoundError(f"File not found for hash calculation: {p}")
    hasher = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest().upper()


def verify_sha256(filepath: str | Path, expected_hash: str) -> bool:
    """Verifies that file matches expected SHA-256 hash with cross-platform line-ending resilience."""
    actual = compute_sha256(filepath)
    match = actual.lower() == expected_hash.strip().lower()
    if not match:
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            crlf_hash = hashlib.sha256(content.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest()
            lf_hash = hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest()
            if expected_hash.strip().lower() in (crlf_hash.lower(), lf_hash.lower()):
                match = True
        except Exception:
            pass
    if match:
        logger.info(f"Cryptographic hash verified for {filepath}")
    else:
        logger.error(
            f"Hash mismatch for {filepath}. Expected: {expected_hash}, Actual: {actual}"
        )
    return match


def load_raw_data(filepath: str | Path) -> pd.DataFrame:
    """Loads raw CSV dataset and performs initial validation."""
    p = Path(filepath)
    if not p.exists():
        # Check parent if executing from inside notebooks/
        p = Path("..") / filepath
    if not p.exists():
        raise FileNotFoundError(f"Raw dataset not found: {filepath}")
    df = pd.read_csv(p)
    logger.info(f"Loaded raw data from {p}: {len(df)} rows, {len(df.columns)} columns")
    return df


def save_parquet(df: pd.DataFrame, filepath: str | Path) -> None:
    """Saves DataFrame as Parquet with parent directory auto-creation and fallback."""
    p = Path(filepath)
    ensure_dir(p.parent)
    try:
        df.to_parquet(p, index=False)
    except (ImportError, ValueError):
        df.to_pickle(p)
    logger.info(f"Saved Parquet dataset: {p} ({len(df)} rows)")


def load_parquet(filepath: str | Path, required_by_day: str = "an earlier day") -> pd.DataFrame:
    """Loads Parquet dataset with clear error naming the missing prerequisite day and engine fallback."""
    p = Path(filepath)
    if not p.exists():
        p = Path("..") / filepath
    if not p.exists():
        raise ArtifactMissingError(
            f"Missing required dataset: '{filepath}'. "
            f"Please run the notebook for {required_by_day} first to produce this artifact."
        )
    try:
        df = pd.read_parquet(p)
    except (ImportError, ValueError):
        df = pd.read_pickle(p)
    logger.info(f"Loaded Parquet dataset from {p}: {len(df)} rows")
    return df


def save_artifact(obj: Any, filepath: str | Path) -> None:
    """Saves Python object (joblib, json, or text) to specified path."""
    p = Path(filepath)
    ensure_dir(p.parent)
    if p.suffix == ".json":
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, default=str)
    elif p.suffix in (".joblib", ".pkl"):
        joblib.dump(obj, p)
    elif p.suffix in (".yaml", ".yml"):
        import yaml

        with open(p, "w", encoding="utf-8") as f:
            yaml.dump(obj, f, default_flow_style=False)
    else:
        with open(p, "w", encoding="utf-8") as f:
            f.write(str(obj))
    logger.info(f"Saved artifact to {p}")


def load_artifact(filepath: str | Path, required_by_day: str = "an earlier day") -> Any:
    """Loads serialized artifact with actionable missing-day error messaging."""
    p = Path(filepath)
    if not p.exists():
        p = Path("..") / filepath
    if not p.exists():
        raise ArtifactMissingError(
            f"Missing prerequisite artifact: '{filepath}'. "
            f"Please run the notebook for {required_by_day} first to generate it."
        )
    if p.suffix == ".json":
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    elif p.suffix in (".joblib", ".pkl"):
        return joblib.load(p)
    elif p.suffix in (".yaml", ".yml"):
        import yaml

        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        with open(p, encoding="utf-8") as f:
            return f.read()
