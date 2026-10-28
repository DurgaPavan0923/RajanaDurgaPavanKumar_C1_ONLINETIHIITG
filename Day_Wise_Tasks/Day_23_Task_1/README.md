# Day 23 - Task 1: Quarantined Test Lockbox Unblinding & Performance Audit
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 23 / Day 28

---

## 1. Objective & Operational Scope
Execute the single authorized unblinding evaluation pass on the 492 held-out test samples, calculating test PR-AUC, ROC-AUC, Brier score, and accuracy.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day23_test_evaluation.ipynb`](./day23_test_evaluation.ipynb) - Executed interactive notebook with verified outputs.
- [`day23_test_evaluation.py`](./day23_test_evaluation.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_23_Task_1/day23_test_evaluation.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_23_Task_1/day23_test_evaluation.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day23_task1_test_confusion_matrix.png`](./outputs/figures/day23_task1_test_confusion_matrix.png)
  ![day23_task1_test_confusion_matrix.png](./outputs/figures/day23_task1_test_confusion_matrix.png)

### Tables Generated:
- [`day23_task1_test_performance.csv`](./outputs/tables/day23_task1_test_performance.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
