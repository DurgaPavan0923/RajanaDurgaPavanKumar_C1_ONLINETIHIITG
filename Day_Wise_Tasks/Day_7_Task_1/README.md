# Day 7 - Task 1: Raw Ingestion & Cryptographic Verification
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 07 / Day 28

---

## 1. Objective & Operational Scope
Ingest raw environmental telemetry and tabular potability datasets, verify cryptographic SHA-256 digests, and validate initial structural schemas.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day07_raw_ingestion.ipynb`](./day07_raw_ingestion.ipynb) - Executed interactive notebook with verified outputs.
- [`day07_raw_ingestion.py`](./day07_raw_ingestion.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_7_Task_1/day07_raw_ingestion.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_7_Task_1/day07_raw_ingestion.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day7_task1_missingness_profile.png`](./outputs/figures/day7_task1_missingness_profile.png)
  ![day7_task1_missingness_profile.png](./outputs/figures/day7_task1_missingness_profile.png)

### Tables Generated:
- [`day7_task1_raw_schema_profile.csv`](./outputs/tables/day7_task1_raw_schema_profile.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
