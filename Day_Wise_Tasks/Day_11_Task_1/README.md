# Day 11 - Task 1: Temporal Preprocessing Pipeline
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 11 / Day 28

---

## 1. Objective & Operational Scope
The objective of Day 11 is to implement a reusable preprocessing pipeline for the timestamped water-quality dataset.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day11_temporal_preprocessing.ipynb`](./day11_temporal_preprocessing.ipynb) - Executed interactive notebook with verified outputs.
- [`day11_temporal_preprocessing.py`](./day11_temporal_preprocessing.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_11_Task_1/day11_temporal_preprocessing.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_11_Task_1/day11_temporal_preprocessing.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day11_temporal_split.png`](./outputs/figures/day11_temporal_split.png)
  ![day11_temporal_split.png](./outputs/figures/day11_temporal_split.png)

### Tables Generated:
- [`day11_preprocessed_summary.csv`](./outputs/tables/day11_preprocessed_summary.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
