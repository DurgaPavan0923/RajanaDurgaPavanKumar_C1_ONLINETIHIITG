# Day 25 - Task 1: Error & Failure Analysis Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 25 / Day 28

---

## 1. Objective & Operational Scope
Perform exhaustive public health failure mode analysis, categorizing false negatives (toxic water misclassified as potable) versus false positives.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day25_error_analysis.ipynb`](./day25_error_analysis.ipynb) - Executed interactive notebook with verified outputs.
- [`day25_error_analysis.py`](./day25_error_analysis.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_25_Task_1/day25_error_analysis.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_25_Task_1/day25_error_analysis.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day25_task1_error_breakdown.png`](./outputs/figures/day25_task1_error_breakdown.png)
  ![day25_task1_error_breakdown.png](./outputs/figures/day25_task1_error_breakdown.png)

### Tables Generated:
- [`day25_task1_failure_modes.csv`](./outputs/tables/day25_task1_failure_modes.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
