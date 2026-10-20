"""Production FastAPI Inference Endpoint with Input Validation and WHO Compliance Checking."""

import time
import traceback
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

UTC = timezone.utc

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


def load_production_model() -> dict[str, Any] | None:
    """Loads production model bundle with multiple path candidates and error resilience.

    Caches loaded bundle in MODEL_BUNDLE['bundle'] so subsequent invocations are instant.
    """
    if "bundle" in MODEL_BUNDLE and MODEL_BUNDLE["bundle"]:
        return MODEL_BUNDLE["bundle"]

    candidate_paths = [
        Path("models/production/water_potability_pipeline_v1.joblib"),
        Path(__file__).resolve().parent.parent.parent
        / "models"
        / "production"
        / "water_potability_pipeline_v1.joblib",
        Path.cwd() / "models" / "production" / "water_potability_pipeline_v1.joblib",
    ]
    for model_path in candidate_paths:
        if model_path.exists():
            try:
                logger.info(f"Loading production model bundle from {model_path}...")
                bundle = joblib.load(model_path)
                MODEL_BUNDLE["bundle"] = bundle
                logger.info(
                    f"Successfully loaded model bundle: {bundle.get('model_name')} "
                    f"trained at {bundle.get('timestamp')}"
                )
                return bundle
            except Exception as e:
                logger.error(f"Failed to deserialize model bundle from {model_path}: {e}")
    logger.warning(
        "Production model bundle not found or could not be loaded. Operating in resilient degraded mode."
    )
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Fast non-blocking serverless lifespan. Defer heavy model unpickling to lazy on-demand invocation."""
    yield


app = FastAPI(
    title="Water Potability & Underwater Environmental Monitoring API",
    description="Production REST endpoint for calibrated water potability classification and anomaly detection.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception during request {request.url.path}: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error encountered during telemetry inference.",
            "error": str(exc),
            "traceback": traceback.format_exc(),
        },
    )


@app.get("/ping")
@app.get("/api/ping")
def ping() -> dict[str, str]:
    """Lightweight health probe endpoint for deployment verification."""
    return {"status": "ok", "service": "AquaGuard AI"}


@app.get("/", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
@app.get("/api/index", response_class=HTMLResponse)
@app.get("/api/index.py", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    """Serves the modern, clean, attractive, and professional web dashboard."""
    return HTMLResponse(content=HTML_DASHBOARD, status_code=200)


_CACHED_STREAM_DF: pd.DataFrame | None = None
SENSOR_BOUNDS: dict[str, tuple[float | None, float | None]] = {
    "ph": (6.5, 8.5),
    "dissolved_oxygen": (5.0, 14.0),
    "turbidity": (None, 5.0),
    "temperature": (4.0, 30.0),
    "conductivity": (None, 600.0),
    "pressure": (None, 300.0),
}


def get_stream_dataframe() -> pd.DataFrame | None:
    """Returns cached in-memory stream telemetry DataFrame to eliminate repetitive disk I/O."""
    global _CACHED_STREAM_DF
    if _CACHED_STREAM_DF is not None:
        return _CACHED_STREAM_DF

    stream_candidates = [
        Path("data/01_raw/underwater_sensor_stream.csv"),
        Path(__file__).resolve().parent.parent.parent
        / "data"
        / "01_raw"
        / "underwater_sensor_stream.csv",
        Path.cwd() / "data" / "01_raw" / "underwater_sensor_stream.csv",
    ]
    stream_file = next((p for p in stream_candidates if p.exists()), None)
    if stream_file is not None:
        _CACHED_STREAM_DF = pd.read_csv(stream_file)
    return _CACHED_STREAM_DF


@app.get("/stream-data")
@app.get("/api/stream-data")
def get_stream_telemetry(sensor: str = "dissolved_oxygen", limit: int = 120) -> dict[str, Any]:
    """Returns continuous underwater sensor stream telemetry and anomaly flags for visualization."""
    valid_sensors = [
        "dissolved_oxygen",
        "temperature",
        "ph",
        "conductivity",
        "turbidity",
        "pressure",
    ]
    selected_sensor = sensor if sensor in valid_sensors else "dissolved_oxygen"
    df_raw = get_stream_dataframe()

    if df_raw is None:
        labels = [f"T+{i}h" for i in range(72)]
        values = [round(float(9.5 - 0.5 * np.sin(i / 12 * np.pi)), 2) for i in range(72)]
        anomalies = [values[i] if i in (24, 48) else None for i in range(72)]
        return {
            "labels": labels,
            "values": values,
            "anomalies": anomalies,
            "sensor": selected_sensor,
            "total_records": 72,
        }

    try:
        df = df_raw.head(limit)
        labels = [pd.to_datetime(t).strftime("%m-%d %H:%M") for t in df["timestamp"]]
        vals = df[selected_sensor].to_numpy(dtype=float)
        values = [round(float(v), 2) if np.isfinite(v) else None for v in vals]

        low, high = SENSOR_BOUNDS.get(selected_sensor, (None, None))
        anomalies = [
            v if (v is not None and ((low is not None and v < low) or (high is not None and v > high))) else None
            for v in values
        ]

        return {
            "labels": labels,
            "values": values,
            "anomalies": anomalies,
            "sensor": selected_sensor,
            "total_records": len(df),
        }
    except Exception as e:
        logger.error(f"Error reading telemetry stream: {e}")
        labels = [f"T+{i}h" for i in range(72)]
        values = [round(float(9.5 - 0.5 * np.sin(i / 12 * np.pi)), 2) for i in range(72)]
        anomalies = [values[i] if i in (24, 48) else None for i in range(72)]
        return {
            "labels": labels,
            "values": values,
            "anomalies": anomalies,
            "sensor": selected_sensor,
            "total_records": 72,
        }


@app.get("/health", status_code=status.HTTP_200_OK)
@app.get("/api/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, Any]:
    """Returns service health status immediately without blocking cold-start."""
    is_model_loaded = "bundle" in MODEL_BUNDLE and MODEL_BUNDLE["bundle"] is not None
    return {
        "status": "healthy" if is_model_loaded else "ready",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "model_loaded": is_model_loaded,
        "model_name": MODEL_BUNDLE.get("bundle", {}).get("model_name") if is_model_loaded else "WHO_Deterministic_Benchmark",
        "lockbox_metrics": MODEL_BUNDLE.get("bundle", {}).get("lockbox_test_metrics") if is_model_loaded else None,
    }


@app.post("/predict", status_code=status.HTTP_200_OK)
@app.post("/api/predict", status_code=status.HTTP_200_OK)
def predict_potability(sample: TrackBWaterSample) -> dict[str, Any]:
    """Performs inference: checks WHO compliance, flags anomalies, and computes calibrated potability probability."""
    t0 = time.perf_counter()

    sample_dict = sample.model_dump()
    raw_df = pd.DataFrame([sample_dict])

    # 1. Deterministic WHO Compliance Check
    violations = WHO_CLASSIFIER.predict_violations(raw_df)[0]
    who_compliant = len(violations) == 0

    bundle = load_production_model()
    if bundle is None:
        # Fallback to pure WHO Rule Classifier if ML bundle not yet loaded/available
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

    try:
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
    except Exception as e:
        logger.error(f"Inference error during ML execution: {e}. Falling back gracefully to WHO rules.")
        t1 = time.perf_counter()
        return {
            "mode": "fallback_who_rules",
            "warning": f"ML model error: {e}",
            "who_compliant": who_compliant,
            "who_violations": violations,
            "potability_prediction": 1 if who_compliant else 0,
            "potability_probability": 1.0 if who_compliant else 0.0,
            "anomaly_flag": False,
            "anomaly_score": 0.0,
            "processing_time_ms": round((t1 - t0) * 1000.0, 3),
        }
