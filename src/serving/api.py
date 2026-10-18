"""Production FastAPI Inference Endpoint with Input Validation and WHO Compliance Checking."""

import time
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse

from src.data.schemas import TrackBWaterSample
from src.features.engineer import FeatureEngineer
from src.logger import get_logger
from src.models.baselines import WHORuleClassifier
from src.serving.web_ui import HTML_DASHBOARD

logger = get_logger("ServingAPI")

# Global state
MODEL_BUNDLE: dict[str, Any] = {}
WHO_CLASSIFIER = WHORuleClassifier()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads frozen pipeline and model artifacts on startup."""
    model_path = Path("models/production/water_potability_pipeline_v1.joblib")
    if not model_path.exists():
        model_path = (
            Path(__file__).resolve().parent.parent.parent
            / "models"
            / "production"
            / "water_potability_pipeline_v1.joblib"
        )
    if model_path.exists():
        try:
            logger.info(f"Loading production model bundle from {model_path}...")
            MODEL_BUNDLE["bundle"] = joblib.load(model_path)
            logger.info(
                f"Successfully loaded model bundle: {MODEL_BUNDLE['bundle'].get('model_name')} "
                f"trained at {MODEL_BUNDLE['bundle'].get('timestamp')}"
            )
        except Exception as e:
            logger.error(f"Failed to deserialize model bundle: {e}")
    else:
        logger.warning(
            f"Production model bundle not found at {model_path}. Running in uninitialized mode."
        )
    yield
    MODEL_BUNDLE.clear()


app = FastAPI(
    title="Water Potability & Underwater Environmental Monitoring API",
    description="Production REST endpoint for calibrated water potability classification and anomaly detection.",
    version="1.0.0",
    lifespan=lifespan,
)

MAX_BODY_BYTES = 1024 * 1024  # 1 MB maximum payload


@app.middleware("http")
async def limit_payload_size_middleware(request: Request, call_next):
    """Enforces maximum payload size ceiling to mitigate memory exhaustion DoS."""
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_BODY_BYTES:
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={
                "detail": f"Payload size exceeds authorized maximum limit of {MAX_BODY_BYTES} bytes."
            },
        )
    return await call_next(request)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception during request {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error encountered during telemetry inference.",
            "error": str(exc),
        },
    )


@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    """Serves the modern, clean, attractive, and professional web dashboard."""
    return HTMLResponse(content=HTML_DASHBOARD, status_code=200)


@app.get("/api/stream-data")
def get_stream_telemetry(sensor: str = "dissolved_oxygen", limit: int = 120) -> dict[str, Any]:
    """Returns continuous underwater sensor stream telemetry and anomaly flags for visualization."""
    stream_file = Path("data/01_raw/underwater_sensor_stream.csv")
    if not stream_file.exists():
        stream_file = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "01_raw"
            / "underwater_sensor_stream.csv"
        )
    valid_sensors = [
        "dissolved_oxygen",
        "temperature",
        "ph",
        "conductivity",
        "turbidity",
        "pressure",
    ]
    selected_sensor = sensor if sensor in valid_sensors else "dissolved_oxygen"

    if not stream_file.exists():
        labels = [f"T+{i}h" for i in range(72)]
        values = [9.5 - 0.5 * np.sin(i / 12 * np.pi) for i in range(72)]
        anomalies = [values[i] if i in (24, 48) else None for i in range(72)]
        return {
            "labels": labels,
            "values": values,
            "anomalies": anomalies,
            "sensor": selected_sensor,
        }

    df = pd.read_csv(stream_file).head(limit)
    labels = [pd.to_datetime(t).strftime("%m-%d %H:%M") for t in df["timestamp"]]
    values = [float(v) if pd.notna(v) else None for v in df[selected_sensor]]

    # Sensor-specific domain boundary anomaly checks
    anomalies = []
    for i, row in df.iterrows():
        val = row.get(selected_sensor)
        is_anom = False
        if pd.notna(val):
            val = float(val)
            if selected_sensor == "ph" and (val < 6.5 or val > 8.5):
                is_anom = True
            elif selected_sensor == "dissolved_oxygen" and (val < 5.0 or val > 14.0):
                is_anom = True
            elif selected_sensor == "turbidity" and val > 5.0:
                is_anom = True
            elif selected_sensor == "temperature" and (val < 4.0 or val > 30.0):
                is_anom = True
            elif selected_sensor == "conductivity" and val > 600.0:
                is_anom = True
            elif selected_sensor == "pressure" and val > 300.0:
                is_anom = True
        anomalies.append(values[i] if is_anom else None)

    return {
        "labels": labels,
        "values": values,
        "anomalies": anomalies,
        "sensor": selected_sensor,
        "total_records": len(df),
    }


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, Any]:
    """Returns service health status and active model artifact metadata."""
    is_model_loaded = "bundle" in MODEL_BUNDLE
    return {
        "status": "healthy" if is_model_loaded else "degraded",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "model_loaded": is_model_loaded,
        "model_name": MODEL_BUNDLE.get("bundle", {}).get("model_name") if is_model_loaded else None,
        "lockbox_metrics": MODEL_BUNDLE.get("bundle", {}).get("lockbox_test_metrics")
        if is_model_loaded
        else None,
    }


@app.post("/predict", status_code=status.HTTP_200_OK)
def predict_potability(sample: TrackBWaterSample) -> dict[str, Any]:
    """Performs inference: checks WHO compliance, flags anomalies, and computes calibrated potability probability."""
    t0 = time.perf_counter()

    sample_dict = sample.model_dump()
    raw_df = pd.DataFrame([sample_dict])

    # 1. Deterministic WHO Compliance Check
    violations = WHO_CLASSIFIER.predict_violations(raw_df)[0]
    who_compliant = len(violations) == 0

    if "bundle" not in MODEL_BUNDLE:
        # Fallback to pure WHO Rule Classifier if ML bundle not yet trained
        t1 = time.perf_counter()
        return {
            "mode": "fallback_who_rules",
            "who_compliant": who_compliant,
            "who_violations": violations,
            "potability_prediction": 1 if who_compliant else 0,
            "potability_probability": 1.0 if who_compliant else 0.0,
            "anomaly_flag": False,
            "anomaly_score": 0.0,
            "processing_time_ms": round((t1 - t0) * 1000.0, 3),
        }

    bundle = MODEL_BUNDLE["bundle"]
    pipeline = bundle["pipeline"]
    classifier = bundle["classifier"]
    anomaly_detector = bundle.get("anomaly_detector")

    # 2. Domain Feature Engineering
    engineered_df = FeatureEngineer.engineer_track_b_features(raw_df)

    # Align columns with training feature set
    training_cols = bundle.get("feature_names", list(engineered_df.columns))
    for col in training_cols:
        if col not in engineered_df.columns:
            engineered_df[col] = np.nan
    aligned_df = engineered_df[training_cols]

    # 3. Pipeline Transform (Imputation + Scaling)
    X_trans = pipeline.transform(aligned_df)

    # 4. Supervised Calibrated Probability & Class
    if hasattr(classifier, "predict_proba"):
        probs = classifier.predict_proba(X_trans)
        potable_prob = float(probs[0, 1])
    else:
        potable_prob = float(classifier.predict(X_trans)[0])

    potability_pred = int(potable_prob >= 0.50)

    # 5. Anomaly Detection
    anomaly_flag = False
    anomaly_score = 0.0
    if anomaly_detector is not None:
        anomaly_flag = bool(anomaly_detector.predict(X_trans)[0] == 1)
        anomaly_score = float(anomaly_detector.score_samples(X_trans)[0])

    t1 = time.perf_counter()

    return {
        "mode": "production_ml",
        "model_name": bundle.get("model_name"),
        "potability_prediction": potability_pred,
        "potability_probability": round(potable_prob, 4),
        "who_compliant": who_compliant,
        "who_violations": violations,
        "anomaly_flag": anomaly_flag,
        "anomaly_score": round(anomaly_score, 4),
        "processing_time_ms": round((t1 - t0) * 1000.0, 3),
    }
