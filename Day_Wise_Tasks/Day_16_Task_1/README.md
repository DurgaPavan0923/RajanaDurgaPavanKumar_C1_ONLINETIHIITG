# Day 16 - Task 1: Multi-Step Forecasting Baselines Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 16 / Day 28

---

## 1. Objective & Operational Scope
Benchmark multi-step forecasting baselines (Naive Persistence, Ridge Regression, and Random Forest) over T+1 through T+6 dissolved oxygen forecast horizons.

## 2. Execution Steps
1. **Multi-Step Supervised Horizon Dataset Formulation**: Transform continuous dissolved oxygen stream into multi-step supervised target horizons (T+1 to T+6).
2. **Train-Validation Chronological Partitioning**: Split forecasting dataset chronologically (80% train, 20% validation).
3. **Persistence Baseline Evaluation**: Evaluate Naive Persistence (last observed value y[t] carried forward across all horizons).
4. **Ridge Regression Baseline Evaluation**: Train linear Ridge regression model across all 6 horizons and compute validation MAE.
5. **Multi-Output Random Forest Baseline Evaluation**: Train multi-output Random Forest regressor with 50 trees and compute validation MAE.
6. **Multi-Step Forecasting Comparison Plot**: Render multi-line plot comparing sample ground truth trajectory against Persistence, Ridge, and Random Forest forecasts.
7. **Forecasting Baselines Summary Table Export**: Export comparative MAE and RMSE performance metrics across baseline architectures to CSV.
8. **Baseline Performance Assertion**: Assert that Random Forest significantly outperforms Naive Persistence.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day16_forecasting_baselines.ipynb`](./day16_forecasting_baselines.ipynb) - Executed interactive notebook with verified inline plots.
- [`day16_forecasting_baselines.py`](./day16_forecasting_baselines.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_16_Task_1/day16_forecasting_baselines.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_16_Task_1/day16_forecasting_baselines.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day16_task1_forecasting_baselines.png`](./outputs/figures/day16_task1_forecasting_baselines.png)
  ![day16_task1_forecasting_baselines.png](./outputs/figures/day16_task1_forecasting_baselines.png)

### Tables Generated:
- [`day16_task1_baseline_metrics.csv`](./outputs/tables/day16_task1_baseline_metrics.csv)

## 6. Assumptions and Methodology
- Input lags T-12..T provide sufficient autoregressive memory for T+1..T+6 forecasting.
- Tree ensembles capture non-linear diurnal cycles better than linear models.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
