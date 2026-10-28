# Day 1 - Task 2: Git Repository & Workspace Protocol
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 01 / Day 28

---

## 1. Objective & Operational Scope
Audit git repository structure, track committed artifacts, verify version control ignore rules, and ensure workspace hygiene.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day01_workspace_audit.ipynb`](./day01_workspace_audit.ipynb) - Executed interactive notebook with verified outputs.
- [`day01_workspace_audit.py`](./day01_workspace_audit.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_1_Task_2/day01_workspace_audit.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_1_Task_2/day01_workspace_audit.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day1_task2_workspace_footprint.png`](./outputs/figures/day1_task2_workspace_footprint.png)
  ![day1_task2_workspace_footprint.png](./outputs/figures/day1_task2_workspace_footprint.png)

### Tables Generated:
- [`day1_task2_workspace_summary.csv`](./outputs/tables/day1_task2_workspace_summary.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
