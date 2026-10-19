"""Unit tests for models: WHO baseline, Isolation Forest, Classifier, and Forecaster."""

import numpy as np
import pandas as pd

from src.models.anomaly import IsolationForestAnomalyDetector
from src.models.baselines import WHORuleClassifier
from src.models.classifier import WaterPotabilityClassifier


def test_who_baseline_deterministic_logic():
    who = WHORuleClassifier()
    # Sample compliant with all limits
    good_sample = pd.DataFrame(
        [
            {
                "ph": 7.2,
                "Hardness": 150.0,
                "Solids": 500.0,
                "Chloramines": 2.0,
                "Sulfate": 200.0,
                "Conductivity": 300.0,
                "Organic_carbon": 2.0,
                "Trihalomethanes": 50.0,
                "Turbidity": 2.0,
            }
        ]
    )
    # Sample violating pH and Turbidity
    bad_sample = pd.DataFrame(
        [
            {
                "ph": 3.5,
                "Hardness": 150.0,
                "Solids": 500.0,
                "Chloramines": 2.0,
                "Sulfate": 200.0,
                "Conductivity": 300.0,
                "Organic_carbon": 2.0,
                "Trihalomethanes": 50.0,
                "Turbidity": 12.0,
            }
        ]
    )

    assert who.predict(good_sample)[0] == 1
    assert who.predict(bad_sample)[0] == 0
    violations = who.predict_violations(bad_sample)[0]
    assert len(violations) == 2


def test_isolation_forest_anomaly_detector():
    X_train = np.random.normal(0, 1, (100, 4))
    iso = IsolationForestAnomalyDetector(contamination=0.05, random_state=42)
    iso.fit(X_train)

    # An obvious outlier
    X_test = np.array([[100.0, 100.0, 100.0, 100.0], [0.1, -0.2, 0.05, 0.1]])
    preds = iso.predict(X_test)
    scores = iso.score_samples(X_test)

    assert preds[0] == 1  # outlier
    assert preds[1] == 0  # inlier
    assert scores[0] > scores[1]


def test_classifier_calibrated_probabilities():
    X = np.random.normal(0, 1, (120, 5))
    y = np.random.choice([0, 1], size=120)

    clf = WaterPotabilityClassifier("logistic_regression", calibrate=True, random_state=42)
    clf.fit(X, y)
    probs = clf.predict_proba(X)

    assert probs.shape == (120, 2)
    assert np.all((probs >= 0.0) & (probs <= 1.0))
    assert np.allclose(probs.sum(axis=1), 1.0)
