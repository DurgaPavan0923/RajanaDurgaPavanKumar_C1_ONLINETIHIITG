# Day 10 - Task 2: Correlation Heatmap & Domain Hypotheses
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 10 / Day 28

---

## 1. Objective & Operational Scope
Quantify cross-sensor correlation matrices, formulate testable physical hypotheses, and evaluate multi-channel collinearity.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day10_correlation_analysis.ipynb`](./day10_correlation_analysis.ipynb) - Executed interactive notebook with verified outputs.
- [`day10_correlation_analysis.py`](./day10_correlation_analysis.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_10_Task_2/day10_correlation_analysis.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_10_Task_2/day10_correlation_analysis.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day10_task2_correlation_matrix.png`](./outputs/figures/day10_task2_correlation_matrix.png)
  ![day10_task2_correlation_matrix.png](./outputs/figures/day10_task2_correlation_matrix.png)

### Tables Generated:
- [`day10_task2_hypotheses_table.csv`](./outputs/tables/day10_task2_hypotheses_table.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
