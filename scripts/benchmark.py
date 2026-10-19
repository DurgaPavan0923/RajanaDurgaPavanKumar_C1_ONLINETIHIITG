"""System Performance Profiler and Benchmark Suite.

Measures:
1. End-to-end inference latency per sample.
2. Dynamic peak RAM consumption during batch inference.
3. Serialized artifact sizes on disk.
"""

import json
import os
import sys
from pathlib import Path
import time
import tracemalloc

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd
import joblib

from src.data.loader import DataLoader
from src.features.engineer import FeatureEngineer
from src.data.preprocessing import DataPreprocessor
from src.models.classifier import WaterPotabilityClassifier
from src.models.anomaly import IsolationForestAnomalyDetector


def run_benchmark():
    print("=" * 60)
    print("WATER MONITORING ML SYSTEM - PERFORMANCE BENCHMARK")
    print("=" * 60)

    # 1. Dataset loading benchmark
    tracemalloc.start()
    t0 = time.perf_counter()
    df, _, _ = DataLoader.load_dataset("data/01_raw/water_potability.csv", force_track="B")
    load_time = time.perf_counter() - t0
    current, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Data Loading (3,276 rows): {load_time*1000:.2f} ms | Peak RAM: {peak_mem / (1024**2):.2f} MB")

    # 2. Feature Engineering benchmark
    tracemalloc.start()
    t0 = time.perf_counter()
    df_fe = FeatureEngineer.engineer_track_b_features(df)
    fe_time = time.perf_counter() - t0
    current, peak_fe_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Feature Engineering: {fe_time*1000:.2f} ms | Peak RAM: {peak_fe_mem / (1024**2):.2f} MB")

    # 3. Model Training Benchmark
    X = df_fe.drop(columns=["Potability"])
    y = df_fe["Potability"]

    prep = DataPreprocessor(random_state=42)
    X_trans, pipeline = prep.fit_transform_train(X)

    tracemalloc.start()
    t0 = time.perf_counter()
    clf = WaterPotabilityClassifier("xgboost", calibrate=False, random_state=42)
    clf.fit(X_trans, y)
    train_time = time.perf_counter() - t0
    current, peak_train_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"XGBoost Fitting: {train_time:.2f} s | Peak RAM: {peak_train_mem / (1024**2):.2f} MB")

    # 4. Inference Latency Benchmark
    single_sample = X_trans[:1]
    latencies = []
    for _ in range(500):
        t0 = time.perf_counter()
        _ = clf.predict_proba(single_sample)
        latencies.append((time.perf_counter() - t0) * 1000.0)

    mean_lat = float(np.mean(latencies))
    p95_lat = float(np.percentile(latencies, 95))
    p99_lat = float(np.percentile(latencies, 99))

    print(f"Single-Sample Inference Latency: Mean={mean_lat:.3f} ms | P95={p95_lat:.3f} ms | P99={p99_lat:.3f} ms")

    # 5. Model Serialization Size
    bundle_path = Path("models/production/water_potability_pipeline_v1.joblib")
    bundle_size_kb = os.path.getsize(bundle_path) / 1024.0 if bundle_path.exists() else 0.0
    print(f"Production Artifact Size: {bundle_size_kb:.2f} KB ({bundle_size_kb/1024:.2f} MB)")

    benchmark_summary = {
        "load_time_ms": round(load_time * 1000.0, 2),
        "fe_time_ms": round(fe_time * 1000.0, 2),
        "train_time_sec": round(train_time, 2),
        "mean_latency_ms": round(mean_lat, 3),
        "p95_latency_ms": round(p95_lat, 3),
        "p99_latency_ms": round(p99_lat, 3),
        "peak_ram_mb": round(peak_train_mem / (1024**2), 2),
        "artifact_size_kb": round(bundle_size_kb, 2),
    }

    out_file = Path("reports/benchmark_report.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(benchmark_summary, f, indent=2)

    print(f"Benchmark summary saved to {out_file}")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
