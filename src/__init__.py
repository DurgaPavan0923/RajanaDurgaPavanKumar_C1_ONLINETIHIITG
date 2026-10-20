"""AquaGuard AI: Water Potability & Underwater Environmental Monitoring Package."""

__version__ = "2.0.0"

from src import anomaly, evaluation, features, forecasting, io, preprocessing, utils

try:
    from src import plotting
except (ImportError, Exception):
    plotting = None

__all__ = [
    "anomaly",
    "evaluation",
    "features",
    "forecasting",
    "io",
    "plotting",
    "preprocessing",
    "utils",
]
