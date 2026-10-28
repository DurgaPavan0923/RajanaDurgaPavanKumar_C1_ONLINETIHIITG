# Day 17 - Task 1: Advanced XGBoost Forecaster Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 17 / Day 28

---

## 1. Objective & Operational Scope
Implement an advanced multi-output gradient boosted decision tree (XGBoost) forecaster optimizing multi-horizon dissolved oxygen prediction.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day17_xgboost_forecaster.ipynb`](./day17_xgboost_forecaster.ipynb) - Executed interactive notebook with verified outputs.
- [`day17_xgboost_forecaster.py`](./day17_xgboost_forecaster.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_17_Task_1/day17_xgboost_forecaster.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_17_Task_1/day17_xgboost_forecaster.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day17_task1_xgboost_forecast.png`](./outputs/figures/day17_task1_xgboost_forecast.png)
  ![day17_task1_xgboost_forecast.png](./outputs/figures/day17_task1_xgboost_forecast.png)

### Tables Generated:
- [`day17_task1_xgboost_metrics.csv`](./outputs/tables/day17_task1_xgboost_metrics.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
