# Day 18 - Task 2: Master Leaderboard & Champion Selection
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 18 / Day 28

---

## 1. Objective & Operational Scope
Build the formal Master Model Leaderboard and officially designate the Champion architecture for production deployment.

## 2. Execution Steps
1. **Master Leaderboard Construction**: Construct ranked leaderboard incorporating accuracy, calibration, inference speed, and bundle size.
2. **Champion Selection Formal Declaration**: Extract and formalize champion selection parameters for Track A and Track B.
3. **Production Deployment Feasibility Verification**: Confirm that champion model latencies comply with < 10ms serverless SLA.
4. **Calibration Attestation for Track B**: Assert that Brier score < 0.22 confirming well-calibrated posterior probabilities.
5. **Champion Selection Rationale Documentation**: Document engineering justification for champion model choices.
6. **Leaderboard Comparison Diagnostic Plot**: Render horizontal bar chart displaying ranked leaderboard models and their performance metrics.
7. **Master Leaderboard Table Serialization**: Export master model leaderboard to CSV.
8. **Leaderboard Gate Assertion**: Assert that both Track A and Track B have confirmed Champion models.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day18_leaderboard_champion.ipynb`](./day18_leaderboard_champion.ipynb) - Executed interactive notebook with verified inline plots.
- [`day18_leaderboard_champion.py`](./day18_leaderboard_champion.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_18_Task_2/day18_leaderboard_champion.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_18_Task_2/day18_leaderboard_champion.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day18_task2_master_leaderboard.png`](./outputs/figures/day18_task2_master_leaderboard.png)
  ![day18_task2_master_leaderboard.png](./outputs/figures/day18_task2_master_leaderboard.png)

### Tables Generated:
- [`day18_task2_master_leaderboard.csv`](./outputs/tables/day18_task2_master_leaderboard.csv)

## 6. Assumptions and Methodology
- Champion models satisfy both primary accuracy metric and operational latency budget.
- Leaderboard rankings are immutable following validation freeze.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
