# Day 20 - Task 1: Leave-One-Feature-Out (LOFO) Robustness Ablation
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 20 / Day 28

---

## 1. Objective & Operational Scope
Conduct Leave-One-Feature-Out (LOFO) ablation testing across all sensor and engineered feature groups to quantify marginal predictive value.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day20_lofo_ablation.ipynb`](./day20_lofo_ablation.ipynb) - Executed interactive notebook with verified outputs.
- [`day20_lofo_ablation.py`](./day20_lofo_ablation.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_20_Task_1/day20_lofo_ablation.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_20_Task_1/day20_lofo_ablation.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day20_task1_lofo_ablation.png`](./outputs/figures/day20_task1_lofo_ablation.png)
  ![day20_task1_lofo_ablation.png](./outputs/figures/day20_task1_lofo_ablation.png)

### Tables Generated:
- [`day20_task1_lofo_results.csv`](./outputs/tables/day20_task1_lofo_results.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
