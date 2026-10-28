# Day 24 - Task 1: End-to-End Reproducibility Audit Report
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 24 / Day 28

---

## 1. Objective & Operational Scope
Execute an independent end-to-end reproducibility audit verifying that retraining from raw datasets reproduces bitwise identical predictions.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day24_reproducibility_audit.ipynb`](./day24_reproducibility_audit.ipynb) - Executed interactive notebook with verified outputs.
- [`day24_reproducibility_audit.py`](./day24_reproducibility_audit.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_24_Task_1/day24_reproducibility_audit.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_24_Task_1/day24_reproducibility_audit.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day24_task1_reproducibility_scatter.png`](./outputs/figures/day24_task1_reproducibility_scatter.png)
  ![day24_task1_reproducibility_scatter.png](./outputs/figures/day24_task1_reproducibility_scatter.png)

### Tables Generated:
- [`day24_task1_reproducibility_audit.csv`](./outputs/tables/day24_task1_reproducibility_audit.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
