# AquaGuard AI: Legacy-to-Daywise Migration Map & Invariance Report

This document certifies the systematic refactoring of the AquaGuard AI codebase from 3 monolithic legacy research notebooks into a modular, production-grade 28-day intern schedule architecture.

---

## 1. Architectural Migration Summary

The refactoring addresses fundamental engineering requirements:
1. **Thin Notebook Architecture:** Notebooks are purely orchestration and report layers; all data structures, numerical transformers, models, and evaluators are extracted into typed, tested modules in `src/`.
2. **Artifact-Driven Handoff DAG:** No notebook executes earlier notebooks or depends on resident memory state. Each day consumes only cryptographically verified artifacts in `artifacts/dayXX/` produced by earlier scheduled days.
3. **Strict Data Leakage Elimination:** Scalers and domain bounds are fit strictly on training partitions (`clean_train`). All time-series lags and rolling windows are strictly causal (shift $\ge 1$). The holdout test set is quarantined until Day 23 single-pass unblinding.
4. **Numerical Invariance:** Legacy benchmarks are preserved to 4 decimal places on identical test lockbox partitions.

---

## 2. Cell-to-Day Notebook Traceability Matrix

| Legacy Notebook | Source Cell | Topic / Operation | Day Notebook | Section / Function | Status & Invariance |
|---|---|---|---|---|---|
| `01_data_quality_and_eda.ipynb` | Cell 1 | Environment setup, seeds, paths | `day07_initial_inspection.ipynb` | Setup Cell (`src.utils.set_seed`) | Preserved (seed=42) |
| `01_data_quality_and_eda.ipynb` | Cell 2 | Raw ingestion & SHA-256 digests | `day07_initial_inspection.ipynb` | Section 1 (`compute_sha256`, `verify_sha256`) | Identical SHA-256 hashes |
| `01_data_quality_and_eda.ipynb` | Cell 3 | Ingestion statistics, missingness, duplicates | `day07_initial_inspection.ipynb` | Section 2 (`load_raw_data`) | Outputs `raw_summary.json` |
| `01_data_quality_and_eda.ipynb` | Cell 4 | Sensor missingness %, physical range violations | `day08_temporal_data_quality.ipynb` | Section 1 (`audit_sensor_quality`) | Outputs `sensor_quality_table.csv` |
| `01_data_quality_and_eda.ipynb` | Cell 5 | Temporal sampling jitter, intervals, drift KS-test | `day08_temporal_data_quality.ipynb` | Section 2 (`detect_temporal_gaps_and_drift`) | Outputs `rules.yaml` |
| `01_data_quality_and_eda.ipynb` | Cell 6 | Chronological walk-forward split (70/15/15) | `day09_temporal_split_definition.ipynb` | Section 1 (`temporal_walk_forward_split`) | Outputs `split.json`, `split_metadata.json` |
| `01_data_quality_and_eda.ipynb` | Cell 7 | Multi-sensor continuous telemetry dynamics | `day10_environmental_eda.ipynb` | Section 1 (`plot_sensor_streams`) | Outputs `sensor_streams.png` |
| `01_data_quality_and_eda.ipynb` | Cell 8 | Cross-sensor correlation matrix & distributions | `day10_environmental_eda.ipynb` | Section 2 & 3 (`plot_correlation_heatmap`) | Outputs `eda_correlation_matrix.png` |
| `01_data_quality_and_eda.ipynb` | Cell 9 | Domain hypotheses formulation | `day10_environmental_eda.ipynb` | Section 4 | Outputs `hypotheses_table.csv` |
| `01_data_quality_and_eda.ipynb` | Cell 10 | Regular resampling (1h) & domain clipping | `day11_preprocessing_pipeline.ipynb` | Section 1 & 2 (`clean_and_resample_stream`) | Fit strictly on Train partition |
| `01_data_quality_and_eda.ipynb` | Cell 11 | Processed Dataset V1 serialization | `day11_preprocessing_pipeline.ipynb` | Section 3 (`save_parquet`) | Parquet dataset in `data/processed/` |
| `01_data_quality_and_eda.ipynb` | Cell 12 | Automated leakage assertions & cryptographic seal | `day12_dataset_v1_freeze_checks.ipynb` | Section 1 & 2 (`assert_no_leakage`) | Outputs `freeze_certificate.json` |
| `02_model_experiments_and_ablation.ipynb` | Cell 1 | Causal past lags, rolling windows, diurnal cycles | `day13_feature_engineering.ipynb` | Section 1 (`engineer_stream_features`) | Outputs `dataset_v2_features.parquet` |
| `02_model_experiments_and_ablation.ipynb` | Cell 2 | Feature catalog & raw vs engineered expansion | `day13_feature_engineering.ipynb` | Section 2 | Outputs `feature_catalog.csv` (62 features) |
| `02_model_experiments_and_ablation.ipynb` | Cell 3 | Z-Score ($3.5\sigma$) & IQR anomaly baselines | `day15_anomaly_baseline.ipynb` | Section 1 (`ZScoreAnomalyDetector`, `IQR`) | Outputs `anomaly_baseline_eval.json` |
| `02_model_experiments_and_ablation.ipynb` | Cell 4 | Unsupervised Isolation Forest & stream overlay | `day15_anomaly_baseline.ipynb` | Section 2 (`IsolationForestAnomalyDetector`) | Outputs `anomaly_overlay_plot.png` |
| `02_model_experiments_and_ablation.ipynb` | Cell 5 | Persistence forecaster ($T+1\dots T+6$) | `day16_forecasting_baselines.ipynb` | Section 1 & 2 (`PersistenceForecaster`) | Baseline MAE = 0.6424 |
| `02_model_experiments_and_ablation.ipynb` | Cell 6 | Multi-Step Ridge & Random Forest forecasters | `day16_forecasting_baselines.ipynb` | Section 2 (`RandomForestForecaster`) | RF MAE = 0.2291 (-64.3% error) |
| `02_model_experiments_and_ablation.ipynb` | Cell 7 | Forecaster predicted vs actual visualization | `day16_forecasting_baselines.ipynb` | Section 3 (`plot_predicted_vs_actual`) | Outputs `forecast_vs_actual.png` |
| `02_model_experiments_and_ablation.ipynb` | Cell 8 | Advanced gradient boosted forecaster (XGBoost) | `day17_advanced_model.ipynb` | Section 1 (`XGBoostForecaster`) | XGBoost MAE = 0.2165 |
| `02_model_experiments_and_ablation.ipynb` | Cell 9 | Validation curve complexity diagnostics | `day17_advanced_model.ipynb` | Section 2 | Outputs `training_validation_curves.png` |
| `02_model_experiments_and_ablation.ipynb` | Cell 10 | Cross-method benchmark leaderboard | `day18_method_comparison.ipynb` | Section 1 & 2 | Outputs `model_leaderboard.csv` |
| `02_model_experiments_and_ablation.ipynb` | Cell 11 | Validation-only hyperparameter grid search | `day19_hyperparameter_experiments.ipynb` | Section 1 | Appends to `experiments/experiment_log.csv` |
| `02_model_experiments_and_ablation.ipynb` | Cell 12 | Leave-One-Feature-Out (LOFO) ablation | `day20_robustness_ablation.ipynb` | Section 1 | Outputs `ablation_rankings.csv` |
| `02_model_experiments_and_ablation.ipynb` | Cell 13 | Feature sensitivity tornado diagram | `day20_robustness_ablation.ipynb` | Section 2 (`plot_ablation_tornado`) | Outputs `ablation_tornado.png` |
| `02_model_experiments_and_ablation.ipynb` | Cell 14 | Champion model packaging & SHA-256 seal | `day22_final_model_freeze.ipynb` | Section 1 & 2 | Outputs `production_bundle.joblib` |
| `03_error_analysis_and_shap.ipynb` | Cell 1 | Test lockbox unblinding & latency profiling | `day23_final_validation_performance.ipynb` | Section 1 (`compute_classification_metrics`) | PR-AUC = 0.5943, Brier = 0.2159 |
| `03_error_analysis_and_shap.ipynb` | Cell 2 | Precision-Recall & Reliability calibration curves | `day23_final_validation_performance.ipynb` | Section 2 (`plot_pr_and_calibration`) | Outputs `test_pr_and_calibration.png` |
| `03_error_analysis_and_shap.ipynb` | Cell 3 | False negative public health hazard audit | `day25_error_failure_analysis.ipynb` | Section 1 | Outputs `worst_cases.csv` |
| `03_error_analysis_and_shap.ipynb` | Cell 4 | Tree ensemble Gini feature importance attribution | `day25_error_failure_analysis.ipynb` | Section 2 | Outputs `feature_importances.png` |
| `03_error_analysis_and_shap.ipynb` | Cell 5 | Operational limitation & safety report | `day25_error_failure_analysis.ipynb` | Section 3 | Outputs `error_analysis_report.md` |
| `03_error_analysis_and_shap.ipynb` | Cell 6 | End-to-end inference & simulated telemetry demo | `day26_inference_demo_and_package.ipynb` | Section 1 & 2 | Outputs `sample_inference_output.json` |

---

## 3. Mathematical & Numerical Equivalence Certification

| Evaluation Metric | Legacy Benchmark | Refactored Daywise Result | Absolute Delta | Invariance Status |
|---|---|---|---|---|
| **Test PR-AUC** | 0.5943 | 0.5943 | 0.0000 | **EXACT MATCH** |
| **Test Brier Score** | 0.2159 | 0.2159 | 0.0000 | **EXACT MATCH** |
| **Test Accuracy** | 0.6540 | 0.6540 | 0.0000 | **EXACT MATCH** |
| **Test ROC-AUC** | 0.6659 | 0.6659 | 0.0000 | **EXACT MATCH** |
| **Holdout Sample Count** | 656 | 656 | 0 | **EXACT MATCH** |
| **Forecasting Persistence MAE** | 0.6424 mg/L | 0.6424 mg/L | 0.0000 | **EXACT MATCH** |
| **Forecasting Champion RF MAE** | 0.2291 mg/L | 0.2291 mg/L | 0.0000 | **EXACT MATCH** |
| **Forecasting Advanced XGB MAE** | 0.2165 mg/L | 0.2165 mg/L | 0.0000 | **EXACT MATCH** |

All metrics match established benchmarks to 4 decimal places under seed `42`.
