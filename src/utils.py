"""Core utility functions: seed setting, config loading, logging, and experiment tracking."""

import logging
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

UTC = timezone.utc

import numpy as np
import yaml


def set_seed(seed: int = 42) -> None:
    """Sets deterministic seeds across Python, NumPy, and system environments."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def get_logger(name: str = "AquaGuardAI") -> logging.Logger:
    """Configures and returns a structured console logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


logger = get_logger("Utils")


def ensure_dir(path: str | Path) -> Path:
    """Ensures directory exists and returns Path object."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_config(config_path: str | Path = "configs/config.yaml") -> dict[str, Any]:
    """Loads configuration YAML from relative path."""
    p = Path(config_path)
    if not p.exists():
        # Fallback to look one level up if inside notebooks directory
        p = Path("..") / config_path
    if not p.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(p, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def append_experiment_log(
    log_path: str | Path,
    entry: dict[str, Any],
) -> None:
    """Appends an experiment run dictionary to persistent CSV log."""
    import pandas as pd

    p = Path(log_path)
    ensure_dir(p.parent)

    record = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        **entry,
    }
    df_record = pd.DataFrame([record])
    if not p.exists():
        df_record.to_csv(p, index=False)
    else:
        df_record.to_csv(p, mode="a", header=False, index=False)
    logger.info(f"Experiment log updated at {p}")
