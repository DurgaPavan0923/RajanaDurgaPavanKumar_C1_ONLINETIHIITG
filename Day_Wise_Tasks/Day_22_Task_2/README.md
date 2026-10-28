# Day 22 - Task 2: Production Bundle Manifest & SHA-256 Digest
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 22 / Day 28

---

## 1. Objective & Operational Scope
Compute SHA-256 cryptographic digests, record runtime environment dependencies, and certify the production model bundle manifest.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day22_package_manifest.ipynb`](./day22_package_manifest.ipynb) - Executed interactive notebook with verified outputs.
- [`day22_package_manifest.py`](./day22_package_manifest.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_22_Task_2/day22_package_manifest.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_22_Task_2/day22_package_manifest.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day22_task2_bundle_compliance.png`](./outputs/figures/day22_task2_bundle_compliance.png)
  ![day22_task2_bundle_compliance.png](./outputs/figures/day22_task2_bundle_compliance.png)

### Tables Generated:
- [`day22_task2_bundle_manifest.csv`](./outputs/tables/day22_task2_bundle_manifest.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
