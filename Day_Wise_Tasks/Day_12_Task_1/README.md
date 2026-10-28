# Day 12 - Task 1: Zero-Leakage Invariance Verification Test Suite
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 12 / Day 28

---

## 1. Objective & Operational Scope
Execute an automated five-point data leakage assertion test suite verifying complete temporal isolation between train, validation, and test datasets.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day12_zero_leakage_checks.ipynb`](./day12_zero_leakage_checks.ipynb) - Executed interactive notebook with verified outputs.
- [`day12_zero_leakage_checks.py`](./day12_zero_leakage_checks.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_12_Task_1/day12_zero_leakage_checks.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_12_Task_1/day12_zero_leakage_checks.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day12_task1_leakage_audit.png`](./outputs/figures/day12_task1_leakage_audit.png)
  ![day12_task1_leakage_audit.png](./outputs/figures/day12_task1_leakage_audit.png)

### Tables Generated:
- [`day12_task1_leakage_audit.csv`](./outputs/tables/day12_task1_leakage_audit.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
