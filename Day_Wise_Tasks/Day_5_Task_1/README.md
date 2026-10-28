# Day 5 - Task 1: Deterministic Experiment Protocol & Seed Control
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 05 / Day 28

---

## 1. Objective & Operational Scope
Enforce deterministic execution across NumPy, Python, Scikit-learn, and XGBoost, verifying zero random drift across multiple model runs.

## 2. Execution Steps
1. **Global Deterministic Random Seed Pinning**: Configure random seed 42 globally across all stochastic libraries.
2. **Stochastic Variance Test Across Seeds**: Run Random Forest models across differing random seeds to measure metric variance.
3. **Bitwise Deterministic Invariance Verification**: Execute identical training operations with seed=42 twice and confirm identical output arrays.
4. **Platform Thread Concurrency Control**: Audit OMP_NUM_THREADS and thread allocation to guarantee reproducibility across multi-core systems.
5. **Seed Stability Scorecard Generation**: Construct comparison scorecard evaluating deterministic stability.
6. **Deterministic Stability Curve Plot**: Render plot visualizing identical training trajectories under pinned seed=42.
7. **Deterministic Governance Table Serialization**: Export seed stability scorecard table to CSV.
8. **Zero Drift Assertion**: Assert that bitwise difference across identical seeded runs is exactly zero.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day05_experiment_protocol.ipynb`](./day05_experiment_protocol.ipynb) - Executed interactive notebook with verified inline plots.
- [`day05_experiment_protocol.py`](./day05_experiment_protocol.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_5_Task_1/day05_experiment_protocol.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_5_Task_1/day05_experiment_protocol.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day5_task1_seed_stability.png`](./outputs/figures/day5_task1_seed_stability.png)
  ![day5_task1_seed_stability.png](./outputs/figures/day5_task1_seed_stability.png)

### Tables Generated:
- [`day5_task1_seed_governance.csv`](./outputs/tables/day5_task1_seed_governance.csv)

## 6. Assumptions and Methodology
- Random seed 42 is pinned across all pipeline execution steps.
- Bitwise reproducibility is required for regulatory auditability.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
