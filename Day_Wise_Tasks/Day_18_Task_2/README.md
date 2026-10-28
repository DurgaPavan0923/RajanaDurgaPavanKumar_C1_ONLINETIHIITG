# Day 18 - Task 2: Master Leaderboard & Champion Selection
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 18 / Day 28

---

## 1. Objective & Operational Scope
Build the formal Master Model Leaderboard and officially designate the Champion architecture for production deployment.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day18_leaderboard_champion.ipynb`](./day18_leaderboard_champion.ipynb) - Executed interactive notebook with verified outputs.
- [`day18_leaderboard_champion.py`](./day18_leaderboard_champion.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_18_Task_2/day18_leaderboard_champion.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_18_Task_2/day18_leaderboard_champion.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day18_task2_master_leaderboard.png`](./outputs/figures/day18_task2_master_leaderboard.png)
  ![day18_task2_master_leaderboard.png](./outputs/figures/day18_task2_master_leaderboard.png)

### Tables Generated:
- [`day18_task2_master_leaderboard.csv`](./outputs/tables/day18_task2_master_leaderboard.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
