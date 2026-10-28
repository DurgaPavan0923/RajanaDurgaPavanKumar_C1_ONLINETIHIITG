# Day 16 - Task 2: Forecasting Benchmark Metrics & Trajectory Plot
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 16 / Day 28

---

## 1. Objective & Operational Scope
Perform exhaustive per-horizon error decomposition (T+1 to T+6) evaluating error growth dynamics and residual bias across forecast horizons.

## 2. Execution Steps
1. **Per-Horizon Error Decomposition**: Compute individual MAE values for each step from T+1 to T+6 for Random Forest forecaster.
2. **Residual Distribution Assessment Across Horizons**: Calculate mean prediction residual (bias) at each step to detect systematic drift.
3. **Variance Expansion Quantification**: Measure growth in residual standard deviation from T+1 to T+6.
4. **Directional Accuracy Calculation by Horizon**: Compute Mean Directional Accuracy (MDA) per horizon to verify trend directionality.
5. **Forecast Uncertainty Envelope Formulation**: Establish 95% confidence intervals (+/- 1.96 * std) for each horizon.
6. **Per-Horizon Error Growth Curve Plot**: Render error growth curve displaying MAE and 95% uncertainty interval bounds across horizons.
7. **Horizon Decomposition Table Export**: Export per-horizon MAE, bias, and variance metrics table to CSV.
8. **Horizon Quality Gate Assertion**: Assert that T+1 MAE remains strictly below 0.35 mg/L.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day16_horizon_benchmarks.ipynb`](./day16_horizon_benchmarks.ipynb) - Executed interactive notebook with verified inline plots.
- [`day16_horizon_benchmarks.py`](./day16_horizon_benchmarks.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_16_Task_2/day16_horizon_benchmarks.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_16_Task_2/day16_horizon_benchmarks.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day16_task2_horizon_error_growth.png`](./outputs/figures/day16_task2_horizon_error_growth.png)
  ![day16_task2_horizon_error_growth.png](./outputs/figures/day16_task2_horizon_error_growth.png)

### Tables Generated:
- [`day16_task2_horizon_metrics.csv`](./outputs/tables/day16_task2_horizon_metrics.csv)

## 6. Assumptions and Methodology
- Forecasting error exhibits expected monotonic expansion across temporal horizons.
- Mean residual bias near zero confirms absence of systematic drift.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
