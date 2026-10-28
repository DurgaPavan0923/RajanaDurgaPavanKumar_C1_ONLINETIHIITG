# Day 16 - Task 1: Multi-Step Forecasting Baselines Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 16 / Day 28

---

## 1. Objective & Operational Scope
Benchmark multi-step forecasting baselines (Naive Persistence, Ridge Regression, and Random Forest) over T+1 through T+6 dissolved oxygen forecast horizons.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day16_forecasting_baselines.ipynb`](./day16_forecasting_baselines.ipynb) - Executed interactive notebook with verified outputs.
- [`day16_forecasting_baselines.py`](./day16_forecasting_baselines.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_16_Task_1/day16_forecasting_baselines.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_16_Task_1/day16_forecasting_baselines.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day16_task1_forecasting_baselines.png`](./outputs/figures/day16_task1_forecasting_baselines.png)
  ![day16_task1_forecasting_baselines.png](./outputs/figures/day16_task1_forecasting_baselines.png)

### Tables Generated:
- [`day16_task1_baseline_metrics.csv`](./outputs/tables/day16_task1_baseline_metrics.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
