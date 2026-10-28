# Day 05: Experiment Tracking & Logging Protocol
- **Phase:** Phase 1: Ingestion & Governance
- **Deliverable:** Centralized experiment logging schema (`experiments/experiment_log.csv`), seed pinning protocol, and parameter tracking standards.

---

## 1. Experiment Schema Specification
All model exploration runs (Baselines, Ridge, Random Forest, XGBoost) append to `experiments/experiment_log.csv`:
```csv
timestamp_utc,track,model_name,hyperparameters,cv_metric_name,cv_metric_val,val_loss,execution_time_sec,artifact_path
```

## 2. Seed Control Protocol
- Primary Seed: `42`
- Initialized in all scripts and notebooks via `src.utils.set_seed(42)`.
- Enforces determinism across Python `random`, `numpy.random`, and multi-threaded estimators (`n_jobs=-1`, `random_state=42`).

## 3. Handoff to Day 06
Finalize data governance boundaries and Lockbox quarantine before beginning data processing.
