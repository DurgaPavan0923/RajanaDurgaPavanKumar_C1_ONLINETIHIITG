"""Unit tests for FastAPI endpoints and serving functions."""

import pytest
from pydantic import ValidationError

from src.data.schemas import TrackBWaterSample
from src.serving.api import health_check, predict_potability


def test_health_endpoint():
    res = health_check()
    assert isinstance(res, dict)
    assert "status" in res
    assert "timestamp_utc" in res


def test_predict_endpoint_valid_sample():
    sample = TrackBWaterSample(
        ph=7.3,
        Hardness=204.8,
        Solids=20791.3,
        Chloramines=7.3,
        Sulfate=368.5,
        Conductivity=564.3,
        Organic_carbon=10.3,
        Trihalomethanes=86.9,
        Turbidity=2.9,
    )
    res = predict_potability(sample)
    assert isinstance(res, dict)
    assert "potability_prediction" in res
    assert "who_compliant" in res
    assert "processing_time_ms" in res


def test_predict_endpoint_schema_rejection():
    # Negative hardness is physically impossible and rejected by Pydantic
    with pytest.raises(ValidationError):
        TrackBWaterSample(
            ph=7.0,
            Hardness=-50.0,
            Solids=1000.0,
            Chloramines=3.0,
            Conductivity=400.0,
            Organic_carbon=5.0,
            Turbidity=2.0,
        )
