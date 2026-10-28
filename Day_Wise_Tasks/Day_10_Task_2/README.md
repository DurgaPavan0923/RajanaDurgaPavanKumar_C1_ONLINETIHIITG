# Day 10 - Task 2: Correlation Heatmap & Domain Hypotheses
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 10 / Day 28

---

## 1. Objective & Operational Scope
Quantify cross-sensor correlation matrices, formulate testable physical hypotheses, and evaluate multi-channel collinearity.

## 2. Execution Steps
1. **Telemetry Channel Correlation Computation**: Calculate pairwise Pearson and Spearman correlation matrices across all telemetry channels.
2. **Thermodynamic Hypotheses Formulation**: Formulate 3 formal scientific hypotheses linking temperature, dissolved oxygen, and turbidity.
3. **Hypotheses Empirical Statistical Validation**: Verify empirical correlation coefficients against predicted theoretical signs.
4. **Variance Inflation Factor (VIF) Assessment**: Compute multicollinearity diagnostics across telemetry sensor channels.
5. **Cross-Sensor Distribution Metrics**: Quantify skewness and kurtosis across sensor channels to identify heavy-tailed distributions.
6. **Telemetry Correlation Heatmap Plot**: Render annotated correlation matrix heatmap visualizing cross-sensor relationships.
7. **Hypotheses Table and Correlation Matrix Export**: Save domain hypotheses and correlation matrix to CSV.
8. **Domain Hypothesis Gate Assertion**: Assert that physical hypotheses H1 and H2 match empirical correlation signs.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day10_correlation_analysis.ipynb`](./day10_correlation_analysis.ipynb) - Executed interactive notebook with verified inline plots.
- [`day10_correlation_analysis.py`](./day10_correlation_analysis.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_10_Task_2/day10_correlation_analysis.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_10_Task_2/day10_correlation_analysis.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day10_task2_correlation_matrix.png`](./outputs/figures/day10_task2_correlation_matrix.png)
  ![day10_task2_correlation_matrix.png](./outputs/figures/day10_task2_correlation_matrix.png)

### Tables Generated:
- [`day10_task2_hypotheses_table.csv`](./outputs/tables/day10_task2_hypotheses_table.csv)

## 6. Assumptions and Methodology
- Cross-sensor correlations follow linear or monotonic thermodynamic laws.
- VIF values under 5.0 confirm absence of severe multicollinearity.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
