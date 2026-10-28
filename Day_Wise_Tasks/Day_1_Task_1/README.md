# Day 1 - Task 1: Environment & Dependency Verification
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 01 / Day 28

---

## 1. Objective & Operational Scope
Verify the Python 3.11+ runtime environment, audit critical numerical and machine learning packages, and test dependency parity for AquaGuard AI.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day01_env_verification.ipynb`](./day01_env_verification.ipynb) - Executed interactive notebook with verified outputs.
- [`day01_env_verification.py`](./day01_env_verification.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_1_Task_1/day01_env_verification.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_1_Task_1/day01_env_verification.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day1_task1_env_health.png`](./outputs/figures/day1_task1_env_health.png)
  ![day1_task1_env_health.png](./outputs/figures/day1_task1_env_health.png)

### Tables Generated:
- [`day1_task1_env_specs.csv`](./outputs/tables/day1_task1_env_specs.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
