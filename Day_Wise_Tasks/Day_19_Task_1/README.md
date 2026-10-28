# Day 19 - Task 1: Validation Hyperparameter Grid Search Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 19 / Day 28

---

## 1. Objective & Operational Scope
Execute a systematic hyperparameter grid search optimizing n_estimators, max_depth, and min_samples_split strictly on validation folds.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day19_hyperparameter_search.ipynb`](./day19_hyperparameter_search.ipynb) - Executed interactive notebook with verified outputs.
- [`day19_hyperparameter_search.py`](./day19_hyperparameter_search.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_19_Task_1/day19_hyperparameter_search.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_19_Task_1/day19_hyperparameter_search.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day19_task1_hyperparameter_surface.png`](./outputs/figures/day19_task1_hyperparameter_surface.png)
  ![day19_task1_hyperparameter_surface.png](./outputs/figures/day19_task1_hyperparameter_surface.png)

### Tables Generated:
- [`day19_task1_hparam_tuning_results.csv`](./outputs/tables/day19_task1_hparam_tuning_results.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
