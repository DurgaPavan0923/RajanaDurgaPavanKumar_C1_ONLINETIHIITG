# Day 5 - Task 2: Centralized Experiment Run Registry
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 05 / Day 28

---

## 1. Objective & Operational Scope
Build and validate a centralized experiment run registry tracking model candidate iterations, hyperparameters, and validation scores.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day05_experiment_registry.ipynb`](./day05_experiment_registry.ipynb) - Executed interactive notebook with verified outputs.
- [`day05_experiment_registry.py`](./day05_experiment_registry.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_5_Task_2/day05_experiment_registry.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_5_Task_2/day05_experiment_registry.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day5_task2_experiment_progression.png`](./outputs/figures/day5_task2_experiment_progression.png)
  ![day5_task2_experiment_progression.png](./outputs/figures/day5_task2_experiment_progression.png)

### Tables Generated:
- [`day5_task2_experiment_registry.csv`](./outputs/tables/day5_task2_experiment_registry.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
