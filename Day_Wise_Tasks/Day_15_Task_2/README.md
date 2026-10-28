# Day 15 - Task 2: Isolation Forest Model & Telemetry Overlay Plot
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 15 / Day 28

---

## 1. Objective & Operational Scope
Deploy multivariate Isolation Forest anomaly detection to isolate multi-sensor excursion interactions in high-dimensional telemetry space.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day15_isolation_forest.ipynb`](./day15_isolation_forest.ipynb) - Executed interactive notebook with verified outputs.
- [`day15_isolation_forest.py`](./day15_isolation_forest.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_15_Task_2/day15_isolation_forest.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_15_Task_2/day15_isolation_forest.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day15_task2_isolation_forest.png`](./outputs/figures/day15_task2_isolation_forest.png)
  ![day15_task2_isolation_forest.png](./outputs/figures/day15_task2_isolation_forest.png)

### Tables Generated:
- [`day15_task2_isolation_forest_summary.csv`](./outputs/tables/day15_task2_isolation_forest_summary.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
