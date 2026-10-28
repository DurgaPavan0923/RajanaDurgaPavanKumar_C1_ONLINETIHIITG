# Day 3 - Task 1: Classification Metric Strategy (PR-AUC vs ROC-AUC)
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 03 / Day 28

---

## 1. Objective & Operational Scope
Formulate evaluation metrics for class-imbalanced water potability, establishing PR-AUC as primary ranking metric and Brier score for calibration.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day03_metric_strategy.ipynb`](./day03_metric_strategy.ipynb) - Executed interactive notebook with verified outputs.
- [`day03_metric_strategy.py`](./day03_metric_strategy.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_3_Task_1/day03_metric_strategy.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_3_Task_1/day03_metric_strategy.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day3_task1_roc_vs_pr.png`](./outputs/figures/day3_task1_roc_vs_pr.png)
  ![day3_task1_roc_vs_pr.png](./outputs/figures/day3_task1_roc_vs_pr.png)

### Tables Generated:
- [`day3_task1_metric_strategy.csv`](./outputs/tables/day3_task1_metric_strategy.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
