# Day 23 - Task 2: Precision-Recall & Platt Calibration Analysis
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 23 / Day 28

---

## 1. Objective & Operational Scope
Generate high-resolution Precision-Recall and Platt Calibration curves, confirming operational reliability of posterior probabilities.

## 2. Execution Steps
1. **Calibration Curve Computation**: Compute true positive frequency versus mean predicted probability across 5 uniform probability bins.
2. **Expected Calibration Error (ECE) Calculation**: Calculate Expected Calibration Error weighting bin residuals by sample counts.
3. **Precision-Recall Operating Curve Generation**: Extract precision-recall trajectory points across all classification thresholds.
4. **Operational Decision Threshold Selection**: Identify threshold balancing precision and recall at F1 optimum (threshold ~ 0.45).
5. **High-Recall Public Health Threshold Selection**: Identify conservative threshold achieving > 85% recall to prevent unsafe water consumption.
6. **Calibration and PR Dual-Panel Diagnostic Plot**: Render side-by-side plots displaying Platt calibration reliability diagram and precision-recall curve.
7. **Calibration Bins Table Export**: Export calibration bin probabilities and empirical frequencies table to CSV.
8. **Calibration Gate Assertion**: Assert that Expected Calibration Error is < 0.35.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day23_calibration_curves.ipynb`](./day23_calibration_curves.ipynb) - Executed interactive notebook with verified inline plots.
- [`day23_calibration_curves.py`](./day23_calibration_curves.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_23_Task_2/day23_calibration_curves.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_23_Task_2/day23_calibration_curves.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day23_task2_pr_and_calibration.png`](./outputs/figures/day23_task2_pr_and_calibration.png)
  ![day23_task2_pr_and_calibration.png](./outputs/figures/day23_task2_pr_and_calibration.png)

### Tables Generated:
- [`day23_task2_calibration_bins.csv`](./outputs/tables/day23_task2_calibration_bins.csv)

## 6. Assumptions and Methodology
- Calibrated probabilities allow stakeholders to interpret model confidence directly as empirical risk.
- Decision threshold selection balances public health safety with false alarm rates.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
