# Day 20 - Task 2: Ablation Tornado Plot & Feature Sensitivity Rankings
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 20 / Day 28

---

## 1. Objective & Operational Scope
Synthesize LOFO findings into an authoritative Feature Sensitivity Ranking and generate an executive sensitivity Tornado Diagram.

## 2. Execution Steps
1. **Sensitivity Score Normalization**: Normalize LOFO impact deltas into a 0-100 feature sensitivity index.
2. **Cumulative Sensitivity Concentration Analysis**: Calculate cumulative sensitivity captured by top-k features (Pareto principle check).
3. **Sensor Calibration Priority Assignment**: Assign hardware calibration maintenance priorities (Tier 1: pH, Sulfate; Tier 2: Chloramines, Hardness).
4. **Robustness Against Single Sensor Failure**: Assess system graceful degradation if lowest-priority sensor (Turbidity) fails in deployment.
5. **Sensitivity Stability Metric Check**: Confirm that rank ordering is invariant across alternative decision thresholds.
6. **Executive Ablation Tornado Diagram Generation**: Render horizontal tornado plot illustrating feature sensitivity rankings.
7. **Sensitivity Rankings Table Export**: Export authoritative feature sensitivity rankings table to CSV.
8. **Sensitivity Gate Assertion**: Assert that top 3 features account for at least 50% of aggregate sensitivity.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day20_sensitivity_rankings.ipynb`](./day20_sensitivity_rankings.ipynb) - Executed interactive notebook with verified inline plots.
- [`day20_sensitivity_rankings.py`](./day20_sensitivity_rankings.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_20_Task_2/day20_sensitivity_rankings.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_20_Task_2/day20_sensitivity_rankings.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day20_task2_ablation_tornado.png`](./outputs/figures/day20_task2_ablation_tornado.png)
  ![day20_task2_ablation_tornado.png](./outputs/figures/day20_task2_ablation_tornado.png)

### Tables Generated:
- [`day20_task2_sensitivity_rankings.csv`](./outputs/tables/day20_task2_sensitivity_rankings.csv)

## 6. Assumptions and Methodology
- Relative sensitivity scores guide hardware telemetry maintenance and calibration schedules.
- System exhibits graceful operational degradation under minor sensor outages.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
