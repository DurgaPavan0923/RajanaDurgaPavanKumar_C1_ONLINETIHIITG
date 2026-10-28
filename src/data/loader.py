"""Robust Data Loader with SHA-256 Checksum Verification and Auto-Routing."""

import hashlib
from pathlib import Path

import pandas as pd

from src.exceptions import DataIntegrityError, InvalidTrackError
from src.logger import get_logger

logger = get_logger("DataLoader")


class DataLoader:
    """Loads datasets, validates cryptographic integrity, and detects Track A vs Track B."""

    TIMESTAMP_CANDIDATES = ["timestamp", "datetime", "Date", "Time", "ts"]

    @staticmethod
    def compute_sha256(filepath: str | Path) -> str:
        """Computes SHA-256 hash of a file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    @classmethod
    def verify_checksum(cls, filepath: str | Path, expected_hash: str) -> bool:
        """Verifies file matches expected cryptographic hash with cross-platform line-ending resilience."""
        actual_hash = cls.compute_sha256(filepath)
        if actual_hash.lower() == expected_hash.lower():
            logger.info(f"Cryptographic SHA-256 checksum verified for {filepath}")
            return True

        # Cross-platform line-ending resilience (CRLF vs LF across Windows and Linux)
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            crlf_hash = hashlib.sha256(content.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest()
            lf_hash = hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest()
            if expected_hash.lower() in (crlf_hash.lower(), lf_hash.lower()):
                logger.info(f"Cryptographic SHA-256 checksum verified for {filepath} (cross-platform EOL match)")
                return True
        except Exception:
            pass

        logger.error(
            f"Checksum mismatch for {filepath}. Expected: {expected_hash}, Actual: {actual_hash}"
        )
        return False

    @classmethod
    def detect_track(cls, df: pd.DataFrame) -> tuple[str, str | None]:
        """Detects whether dataset is Track A (Temporal Stream) or Track B (Tabular).

        Rules:
            - If valid monotonic datetime column exists -> Track A
            - If 9 physicochemical columns without timestamps -> Track B
            - Strictly forbids synthesizing timestamps.

        Returns:
            Tuple of (track_name, timestamp_column_name_or_None)
        """
        # Check for timestamp candidate columns
        matched_ts = None
        for col in cls.TIMESTAMP_CANDIDATES:
            if col in df.columns:
                matched_ts = col
                break

        if matched_ts is not None:
            # Attempt datetime parsing
            try:
                parsed_series = pd.to_datetime(df[matched_ts], errors="coerce")
                if parsed_series.isna().sum() / len(df) > 0.10:
                    logger.warning(
                        f"Column '{matched_ts}' present but >10% values failed datetime parsing. Falling back to Track B."
                    )
                    return "B", None

                # Check monotonicity
                diffs = parsed_series.dropna().diff().iloc[1:]
                positive_steps = (diffs > pd.Timedelta(0)).sum()
                if positive_steps / len(diffs) > 0.85:
                    logger.info(
                        f"Auto-detected Track A (Temporal Stream) via column '{matched_ts}'."
                    )
                    return "A", matched_ts
                else:
                    logger.warning(
                        f"Timestamp column '{matched_ts}' is not monotonic. Dataset may be shuffled. Routing to Track B."
                    )
                    return "B", None
            except Exception as e:
                logger.warning(
                    f"Failed timestamp parsing on '{matched_ts}': {e}. Routing to Track B."
                )
                return "B", None

        # Check for Kaggle 9 features (Track B)
        kaggle_cols = {
            "ph",
            "Hardness",
            "Solids",
            "Chloramines",
            "Sulfate",
            "Conductivity",
            "Turbidity",
        }
        if kaggle_cols.issubset(set(df.columns)):
            logger.info("Auto-detected Track B (Static Tabular Water Potability).")
            return "B", None

        # Generic tabular fallback
        logger.info("Dataset has no timestamp column. Defaulting to Track B (Tabular).")
        return "B", None

    @classmethod
    def load_dataset(
        cls,
        filepath: str | Path,
        expected_sha256: str | None = None,
        force_track: str | None = None,
    ) -> tuple[pd.DataFrame, str, str | None]:
        """Loads dataset from path, checks hash integrity, and executes track detection.

        Args:
            filepath: Path to raw CSV file.
            expected_sha256: Optional expected SHA-256 checksum string.
            force_track: Optional override ('A' or 'B').

        Returns:
            Tuple of (DataFrame, detected_track, timestamp_column_name)
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Dataset path does not exist: {path}")

        if expected_sha256:
            if not cls.verify_checksum(path, expected_sha256):
                raise DataIntegrityError(
                    f"Raw data file {path} failed SHA-256 integrity verification."
                )

        df = pd.read_csv(path)
        logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns from {path}")

        if force_track:
            if force_track not in ("A", "B"):
                raise InvalidTrackError(f"Invalid forced track: {force_track}. Must be 'A' or 'B'.")
            ts_col = "timestamp" if force_track == "A" and "timestamp" in df.columns else None
            return df, force_track, ts_col

        detected_track, ts_col = cls.detect_track(df)
        return df, detected_track, ts_col
