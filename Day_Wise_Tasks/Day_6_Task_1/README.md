# Day 6 - Task 1: Data Governance & Partition Freeze
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 06 / Day 28

---

## 1. Objective & Operational Scope
Establish data governance boundaries, define partition freeze rules, and quarantine test data against developmental leakage.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day06_data_governance.ipynb`](./day06_data_governance.ipynb) - Executed interactive notebook with verified outputs.
- [`day06_data_governance.py`](./day06_data_governance.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_6_Task_1/day06_data_governance.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_6_Task_1/day06_data_governance.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day6_task1_partition_allocation.png`](./outputs/figures/day6_task1_partition_allocation.png)
  ![day6_task1_partition_allocation.png](./outputs/figures/day6_task1_partition_allocation.png)

### Tables Generated:
- [`day6_task1_governance_policies.csv`](./outputs/tables/day6_task1_governance_policies.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
