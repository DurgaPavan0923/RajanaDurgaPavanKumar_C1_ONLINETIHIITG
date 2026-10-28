# Day 13 - Task 1: Causal Feature Engineering Pipeline
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 13 / Day 28

---

## 1. Objective & Operational Scope
Engineer 62 causal rolling features (lags T-1..T-6, rolling mean, rolling std, and WHO ratio deltas) with strict shift >= 1 leakage protection.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day13_feature_engineering.ipynb`](./day13_feature_engineering.ipynb) - Executed interactive notebook with verified outputs.
- [`day13_feature_engineering.py`](./day13_feature_engineering.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_13_Task_1/day13_feature_engineering.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_13_Task_1/day13_feature_engineering.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day13_task1_feature_dynamics.png`](./outputs/figures/day13_task1_feature_dynamics.png)
  ![day13_task1_feature_dynamics.png](./outputs/figures/day13_task1_feature_dynamics.png)

### Tables Generated:
- [`day13_task1_feature_correlations.csv`](./outputs/tables/day13_task1_feature_correlations.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
