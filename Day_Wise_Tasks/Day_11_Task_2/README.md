# Day 11 - Task 2: Hourly Resampling & Imputation Quality Audit
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 11 / Day 28

---

## 1. Objective & Operational Scope
Audit the resampling of irregular high-frequency telemetry into regular hourly intervals, evaluating imputation fidelity and variance preservation.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day11_resampling_audit.ipynb`](./day11_resampling_audit.ipynb) - Executed interactive notebook with verified outputs.
- [`day11_resampling_audit.py`](./day11_resampling_audit.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_11_Task_2/day11_resampling_audit.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_11_Task_2/day11_resampling_audit.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day11_task2_resampling_comparison.png`](./outputs/figures/day11_task2_resampling_comparison.png)
  ![day11_task2_resampling_comparison.png](./outputs/figures/day11_task2_resampling_comparison.png)

### Tables Generated:
- [`day11_task2_resampling_fidelity.csv`](./outputs/tables/day11_task2_resampling_fidelity.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
