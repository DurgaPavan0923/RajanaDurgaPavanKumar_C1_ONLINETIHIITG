# Day 14 - Task 1: Milestone 1 Architecture & Progress Review
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 14 / Day 28

---

## 1. Objective & Operational Scope
Conduct comprehensive mid-internship Milestone 1 technical review synthesizing ingestion, data quality, splits, and feature engineering achievements.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day14_milestone1_review.ipynb`](./day14_milestone1_review.ipynb) - Executed interactive notebook with verified outputs.
- [`day14_milestone1_review.py`](./day14_milestone1_review.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_14_Task_1/day14_milestone1_review.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_14_Task_1/day14_milestone1_review.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day14_task1_milestone1_progress.png`](./outputs/figures/day14_task1_milestone1_progress.png)
  ![day14_task1_milestone1_progress.png](./outputs/figures/day14_task1_milestone1_progress.png)

### Tables Generated:
- [`day14_task1_milestone1_summary.csv`](./outputs/tables/day14_task1_milestone1_summary.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
