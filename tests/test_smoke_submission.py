"""End-to-End Submission Smoke Tests for TIH IIT Guwahati Final Evaluation."""

import pandas as pd
import pytest

from src.data.schemas import TrackBWaterSample
from src.models.baselines import WHORuleClassifier
from src.serving.api import health_check, ping, predict_potability


def test_submission_smoke_ping_and_health():
    """Verify API ping and comprehensive health diagnostic responses."""
    ping_resp = ping()
    assert isinstance(ping_resp, dict)
    assert ping_resp["status"] == "ok"
    assert ping_resp["version"] == "2.1.0"

    health_resp = health_check()
    assert isinstance(health_resp, dict)
    assert health_resp["status"] == "healthy"
    assert health_resp["model_loaded"] is True
    assert "lockbox_metrics" in health_resp
    assert health_resp["lockbox_metrics"]["pr_auc"] >= 0.59


def test_submission_smoke_potability_inference():
    """Verify inference pipeline produces valid probabilities and WHO safety auditing."""
    sample = TrackBWaterSample(
        ph=7.3,
        Hardness=175.0,
        Solids=920.0,
        Chloramines=2.8,
        Sulfate=210.0,
        Conductivity=380.0,
        Organic_carbon=3.2,
        Trihalomethanes=55.0,
        Turbidity=2.8,
    )
    data = predict_potability(sample)
    assert data["potability_prediction"] in [0, 1]
    assert 0.0 <= data["potability_probability"] <= 1.0
    assert "safety_verdict" in data
    assert "who_compliant" in data


def test_submission_smoke_who_rule_override():
    """Verify deterministic safety override when chemical safety limits are breached."""
    who = WHORuleClassifier()
    # Extremely acidic sample (pH 2.1) with toxic Trihalomethanes (150 ug/L)
    toxic_df = pd.DataFrame(
        [
            {
                "ph": 2.1,
                "Hardness": 150.0,
                "Solids": 800.0,
                "Chloramines": 2.0,
                "Sulfate": 200.0,
                "Conductivity": 300.0,
                "Organic_carbon": 2.0,
                "Trihalomethanes": 150.0,
                "Turbidity": 2.0,
            }
        ]
    )
    preds = who.predict(toxic_df)
    assert preds[0] == 0  # Must be rejected as non-potable
    violations = who.predict_violations(toxic_df)[0]
    assert any("ph=" in v for v in violations)
    assert any("Trihalomethanes=" in v for v in violations)
