# Day 7 - Task 2: Raw Schema Profile & Missingness Extraction
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 07 / Day 28

---

## 1. Objective & Operational Scope
Perform deep missingness mechanism profiling, testing for Missing Completely at Random (MCAR) vs Missing at Random (MAR) across water quality attributes.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day07_schema_profiling.ipynb`](./day07_schema_profiling.ipynb) - Executed interactive notebook with verified outputs.
- [`day07_schema_profiling.py`](./day07_schema_profiling.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_7_Task_2/day07_schema_profiling.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_7_Task_2/day07_schema_profiling.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day7_task2_missingness_corr.png`](./outputs/figures/day7_task2_missingness_corr.png)
  ![day7_task2_missingness_corr.png](./outputs/figures/day7_task2_missingness_corr.png)

### Tables Generated:
- [`day7_task2_missingness_profile.csv`](./outputs/tables/day7_task2_missingness_profile.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
