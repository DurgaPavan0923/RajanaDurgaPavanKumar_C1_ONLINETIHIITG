# Day 13 - Task 1: Causal Feature Engineering Pipeline
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 13 / Day 28

---

## 1. Objective & Operational Scope
Engineer 62 causal rolling features (lags T-1..T-6, rolling mean, rolling std, and WHO ratio deltas) with strict shift >= 1 leakage protection.

## 2. Execution Steps
1. **Timestamped Ingestion for Feature Engineering**: Load timestamped water quality dataset and establish chronological order.
2. **Causal Past Lags Construction**: Construct past lags T-1, T-2, T-3, T-6 for dissolved solids and pH with shift >= 1.
3. **Causal Rolling Statistics Generation**: Compute rolling means and standard deviations over 3-sample and 6-sample windows using shifted series.
4. **Physicochemical Domain Ratios Formulation**: Engineer domain ratios: Sulfate-to-Solids, Chloramines-to-Trihalomethanes, and Hardness-to-Conductivity.
5. **WHO Regulatory Boundary Delta Features**: Compute absolute deltas from optimal WHO neutral bounds (pH - 7.0, Chloramines - 4.0).
6. **Engineered Features Dynamics Plot**: Render multi-line plot showing raw parameter alongside causal rolling mean and past lag.
7. **Engineered Features Correlation Table Export**: Export correlation between engineered features and target Potability to CSV.
8. **Causal Feature Quality Gate Assertion**: Assert that shifted rolling feature at index 0 is NaN, proving causal shift >= 1.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day13_feature_engineering.ipynb`](./day13_feature_engineering.ipynb) - Executed interactive notebook with verified inline plots.
- [`day13_feature_engineering.py`](./day13_feature_engineering.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_13_Task_1/day13_feature_engineering.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_13_Task_1/day13_feature_engineering.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day13_task1_feature_dynamics.png`](./outputs/figures/day13_task1_feature_dynamics.png)
  ![day13_task1_feature_dynamics.png](./outputs/figures/day13_task1_feature_dynamics.png)

### Tables Generated:
- [`day13_task1_feature_correlations.csv`](./outputs/tables/day13_task1_feature_correlations.csv)

## 6. Assumptions and Methodology
- All rolling features apply shift >= 1 to prevent current-step label leakage.
- Physicochemical ratios illuminate non-linear chemical interactions.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
