# Day 18 - Task 1: Cross-Method Benchmark Evaluation Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 18 / Day 28

---

## 1. Objective & Operational Scope
Conduct comprehensive benchmark comparing Persistence, Ridge, Random Forest, and XGBoost on validation partitions across MAE, RMSE, R2, and latency.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day18_method_comparison.ipynb`](./day18_method_comparison.ipynb) - Executed interactive notebook with verified outputs.
- [`day18_method_comparison.py`](./day18_method_comparison.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_18_Task_1/day18_method_comparison.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_18_Task_1/day18_method_comparison.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day18_task1_method_comparison.png`](./outputs/figures/day18_task1_method_comparison.png)
  ![day18_task1_method_comparison.png](./outputs/figures/day18_task1_method_comparison.png)

### Tables Generated:
- [`day18_task1_benchmark_summary.csv`](./outputs/tables/day18_task1_benchmark_summary.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
