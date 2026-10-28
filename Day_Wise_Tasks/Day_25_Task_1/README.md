# Day 25 - Task 1: Error & Failure Analysis Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 25 / Day 28

---

## 1. Objective & Operational Scope
Perform exhaustive public health failure mode analysis, categorizing false negatives (toxic water misclassified as potable) versus false positives.

## 2. Execution Steps
1. **Test Error Partition Ingestion**: Extract test misclassifications and compute false negative versus false positive counts.
2. **Public Health Hazard Asymmetry Assessment**: Quantify risk penalty: false negatives carry 5x higher severity than false positives in drinking water systems.
3. **False Negative Feature Profile Analysis**: Examine mean parameter values for false negative cases to identify failure patterns.
4. **Decision Threshold Adjustment Simulation**: Simulate lower decision threshold (e.g. 0.40) to reduce false negative rate by 40%.
5. **Failure Mode Mitigation Protocol Formulation**: Establish dual-tier alerting protocol: automatic flag when predicted probability falls in uncertain [0.40, 0.55] band.
6. **Public Health Error Breakdown Diagnostic Plot**: Render bar chart comparing false negatives versus false positives under standard and conservative thresholds.
7. **Failure Modes Summary Table Serialization**: Export failure modes profile table to CSV.
8. **Public Health Safety Gate Assertion**: Assert that lowering threshold to 0.40 reduces false negatives significantly.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day25_error_analysis.ipynb`](./day25_error_analysis.ipynb) - Executed interactive notebook with verified inline plots.
- [`day25_error_analysis.py`](./day25_error_analysis.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_25_Task_1/day25_error_analysis.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_25_Task_1/day25_error_analysis.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day25_task1_error_breakdown.png`](./outputs/figures/day25_task1_error_breakdown.png)
  ![day25_task1_error_breakdown.png](./outputs/figures/day25_task1_error_breakdown.png)

### Tables Generated:
- [`day25_task1_failure_modes.csv`](./outputs/tables/day25_task1_failure_modes.csv)

## 6. Assumptions and Methodology
- In potable water systems, false-negative errors represent severe public health hazards.
- Adjustable decision thresholds allow balancing false negative suppression with false alarms.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
