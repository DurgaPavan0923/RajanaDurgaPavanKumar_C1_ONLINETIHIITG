# Day 15 - Task 1: Statistical Baseline Anomaly Detection Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 15 / Day 28

---

## 1. Objective & Operational Scope
Implement and evaluate statistical anomaly detection baselines (univariate Z-Score at 3.5 sigma and IQR interquartile range) across continuous telemetry channels.

## 2. Execution Steps
1. **Continuous Telemetry Stream Ingestion for Anomaly Detection**: Ingest continuous telemetry observations and sort chronologically.
2. **Univariate Z-Score Baseline Formulation**: Calculate standard Z-Scores and flag readings exceeding 3.5 standard deviations from the empirical mean.
3. **Interquartile Range (IQR) Baseline Formulation**: Compute Q1, Q3, and IQR, flagging values falling outside Q1 - 1.5*IQR and Q3 + 1.5*IQR.
4. **Z-Score vs IQR Detection Concordance**: Compute Jaccard similarity and cross-tabulation between statistical baseline anomaly detectors.
5. **Sensor Anomaly Event Duration Analysis**: Measure continuous run-length duration of flagged statistical anomaly clusters.
6. **Z-Score Anomaly Overlay Diagnostic Plot**: Render time series plot overlaying detected Z-score anomalies onto the dissolved oxygen trajectory.
7. **Statistical Anomaly Baselines Table Export**: Export baseline detection metrics and threshold parameters to CSV.
8. **Baseline Gate Assertion**: Assert that flagged anomalies remain below 2% false alarm rate on nominal telemetry.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day15_anomaly_baseline.ipynb`](./day15_anomaly_baseline.ipynb) - Executed interactive notebook with verified inline plots.
- [`day15_anomaly_baseline.py`](./day15_anomaly_baseline.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_15_Task_1/day15_anomaly_baseline.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_15_Task_1/day15_anomaly_baseline.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day15_task1_zscore_anomalies.png`](./outputs/figures/day15_task1_zscore_anomalies.png)
  ![day15_task1_zscore_anomalies.png](./outputs/figures/day15_task1_zscore_anomalies.png)

### Tables Generated:
- [`day15_task1_anomaly_baselines.csv`](./outputs/tables/day15_task1_anomaly_baselines.csv)

## 6. Assumptions and Methodology
- Normal operating telemetry approximates Gaussian distribution for Z-score thresholding.
- IQR baseline provides non-parametric robustness against skewed distributions.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
