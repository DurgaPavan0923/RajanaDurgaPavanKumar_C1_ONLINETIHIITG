# Day 3 - Task 2: Telemetry Forecasting Loss Protocol
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 03 / Day 28

---

## 1. Objective & Operational Scope
Design loss functions and multi-horizon evaluation protocols (MAE, RMSE, MAPE, and MDA) for continuous dissolved oxygen forecasting.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day03_forecasting_metrics.ipynb`](./day03_forecasting_metrics.ipynb) - Executed interactive notebook with verified outputs.
- [`day03_forecasting_metrics.py`](./day03_forecasting_metrics.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_3_Task_2/day03_forecasting_metrics.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_3_Task_2/day03_forecasting_metrics.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day3_task2_forecast_error_growth.png`](./outputs/figures/day3_task2_forecast_error_growth.png)
  ![day3_task2_forecast_error_growth.png](./outputs/figures/day3_task2_forecast_error_growth.png)

### Tables Generated:
- [`day3_task2_forecasting_loss_table.csv`](./outputs/tables/day3_task2_forecasting_loss_table.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
