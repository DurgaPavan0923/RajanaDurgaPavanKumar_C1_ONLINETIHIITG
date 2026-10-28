# Day 26 - Task 1: Inference Demo & Packaging Notebook
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 26 / Day 28

---

## 1. Objective & Operational Scope
Demonstrate single-sample, batch, and simulated continuous streaming inference using the production serialized model pipeline.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day26_inference_demo.ipynb`](./day26_inference_demo.ipynb) - Executed interactive notebook with verified outputs.
- [`day26_inference_demo.py`](./day26_inference_demo.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_26_Task_1/day26_inference_demo.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_26_Task_1/day26_inference_demo.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day26_task1_inference_distribution.png`](./outputs/figures/day26_task1_inference_distribution.png)
  ![day26_task1_inference_distribution.png](./outputs/figures/day26_task1_inference_distribution.png)

### Tables Generated:
- [`day26_task1_inference_results.csv`](./outputs/tables/day26_task1_inference_results.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
