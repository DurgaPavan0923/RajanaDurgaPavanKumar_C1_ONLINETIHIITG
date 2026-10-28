# Day 15 - Task 1: Statistical Baseline Anomaly Detection Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 15 / Day 28

---

## 1. Objective & Operational Scope
Implement and evaluate statistical anomaly detection baselines (univariate Z-Score at 3.5 sigma and IQR interquartile range) across continuous telemetry channels.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day15_anomaly_baseline.ipynb`](./day15_anomaly_baseline.ipynb) - Executed interactive notebook with verified outputs.
- [`day15_anomaly_baseline.py`](./day15_anomaly_baseline.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_15_Task_1/day15_anomaly_baseline.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_15_Task_1/day15_anomaly_baseline.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day15_task1_zscore_anomalies.png`](./outputs/figures/day15_task1_zscore_anomalies.png)
  ![day15_task1_zscore_anomalies.png](./outputs/figures/day15_task1_zscore_anomalies.png)

### Tables Generated:
- [`day15_task1_anomaly_baselines.csv`](./outputs/tables/day15_task1_anomaly_baselines.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
