# Day 5 - Task 2: Centralized Experiment Run Registry
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 05 / Day 28

---

## 1. Objective & Operational Scope
Build and validate a centralized experiment run registry tracking model candidate iterations, hyperparameters, and validation scores.

## 2. Execution Steps
1. **Registry Schema Formulation**: Define structured columns: run_id, model_family, timestamp, hyperparameters, val_pr_auc, val_roc_auc, and status.
2. **Historical Experiment Runs Population**: Log benchmark runs across Baseline, Ridge, Random Forest, and XGBoost candidate models.
3. **Champion Selection Logic**: Query registry for highest validation PR-AUC with acceptable Brier calibration.
4. **Performance Improvement Relative to Baseline**: Calculate percentage gain in PR-AUC over uninformative prevalence baseline.
5. **Registry Immutability Check**: Verify that all run_id entries are unique and timestamps maintain chronological ordering.
6. **Experiment Iteration Trajectory Plot**: Render a bar chart displaying PR-AUC progression across all logged experimental runs.
7. **Registry Table Serialization**: Save compiled experiment run registry table to CSV.
8. **Registry Validation Gate**: Assert that registry contains verified champion model with PR-AUC > 0.58.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day05_experiment_registry.ipynb`](./day05_experiment_registry.ipynb) - Executed interactive notebook with verified inline plots.
- [`day05_experiment_registry.py`](./day05_experiment_registry.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_5_Task_2/day05_experiment_registry.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_5_Task_2/day05_experiment_registry.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day5_task2_experiment_progression.png`](./outputs/figures/day5_task2_experiment_progression.png)
  ![day5_task2_experiment_progression.png](./outputs/figures/day5_task2_experiment_progression.png)

### Tables Generated:
- [`day5_task2_experiment_registry.csv`](./outputs/tables/day5_task2_experiment_registry.csv)

## 6. Assumptions and Methodology
- Centralized experiment tracking logs all model candidates to prevent confirmation bias.
- Champion selection strictly prioritizes PR-AUC and Brier calibration on validation partitions.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
