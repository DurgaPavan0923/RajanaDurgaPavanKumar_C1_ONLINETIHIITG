# Day 10 - Task 1: Continuous Telemetry Dynamics & Time-Series EDA
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 10 / Day 28

---

## 1. Objective & Operational Scope
Perform exploratory data analysis on continuous underwater sensor streams, investigating diurnal dynamics, thermal stratification, and dissolved oxygen oscillations.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day10_environmental_eda.ipynb`](./day10_environmental_eda.ipynb) - Executed interactive notebook with verified outputs.
- [`day10_environmental_eda.py`](./day10_environmental_eda.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_10_Task_1/day10_environmental_eda.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_10_Task_1/day10_environmental_eda.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day10_task1_sensor_streams.png`](./outputs/figures/day10_task1_sensor_streams.png)
  ![day10_task1_sensor_streams.png](./outputs/figures/day10_task1_sensor_streams.png)

### Tables Generated:
- [`day10_task1_telemetry_summary.csv`](./outputs/tables/day10_task1_telemetry_summary.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
