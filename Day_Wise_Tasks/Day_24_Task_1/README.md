# Day 24 - Task 1: End-to-End Reproducibility Audit Report
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 24 / Day 28

---

## 1. Objective & Operational Scope
Execute an independent end-to-end reproducibility audit verifying that retraining from raw datasets reproduces bitwise identical predictions.

## 2. Execution Steps
1. **Reproducibility Audit Harness Initialization**: Initialize independent audit session with pinned global seed 42.
2. **Replicate Training Run 1 Execution**: Train complete pipeline from scratch on development data and store prediction vector.
3. **Replicate Training Run 2 Execution**: Re-initialize environment and train identical pipeline to test for stochastic drift.
4. **Bitwise Replicate Divergence Quantification**: Compute maximum absolute difference between Run 1 and Run 2 predictions.
5. **Hash Integrity Comparison Across Runs**: Assert that serialized joblib digests match across identical runs.
6. **Reproducibility Variance Verification Plot**: Render scatter plot showing perfect 1-to-1 diagonal alignment between replicate runs.
7. **Reproducibility Audit Table Serialization**: Export reproducibility audit scorecard to CSV.
8. **Reproducibility Gate Assertion**: Assert that divergence across replicate runs is exactly 0.0.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day24_reproducibility_audit.ipynb`](./day24_reproducibility_audit.ipynb) - Executed interactive notebook with verified inline plots.
- [`day24_reproducibility_audit.py`](./day24_reproducibility_audit.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_24_Task_1/day24_reproducibility_audit.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_24_Task_1/day24_reproducibility_audit.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day24_task1_reproducibility_scatter.png`](./outputs/figures/day24_task1_reproducibility_scatter.png)
  ![day24_task1_reproducibility_scatter.png](./outputs/figures/day24_task1_reproducibility_scatter.png)

### Tables Generated:
- [`day24_task1_reproducibility_audit.csv`](./outputs/tables/day24_task1_reproducibility_audit.csv)

## 6. Assumptions and Methodology
- Deterministic seed pinning guarantees identical numerical results across independent runs.
- Zero divergence confirms absence of unseeded stochastic operations.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
