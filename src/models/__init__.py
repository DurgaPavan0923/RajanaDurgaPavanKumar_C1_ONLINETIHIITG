"""Model zoo subpackage."""

from src.models.anomaly import IsolationForestAnomalyDetector, LOFAnomalyDetector
from src.models.baselines import PersistenceForecaster, WHORuleClassifier, ZScoreAnomalyDetector
from src.models.classifier import WaterPotabilityClassifier
from src.models.forecaster import WaterQualityForecaster

__all__ = [
    "WHORuleClassifier",
    "ZScoreAnomalyDetector",
    "PersistenceForecaster",
    "IsolationForestAnomalyDetector",
    "LOFAnomalyDetector",
    "WaterQualityForecaster",
    "WaterPotabilityClassifier",
]
