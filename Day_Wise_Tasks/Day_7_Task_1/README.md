# Day 7 - Task 1: Raw Ingestion & Cryptographic Verification
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 07 / Day 28

---

## 1. Objective & Operational Scope
Ingest raw environmental telemetry and tabular potability datasets, verify cryptographic SHA-256 digests, and validate initial structural schemas.

## 2. Execution Steps
1. **Raw Tabular Water Potability Ingestion**: Load raw water potability CSV and compute dimensional row and column counts.
2. **Raw Telemetry Stream Ingestion**: Load raw continuous sensor telemetry stream and check chronological range.
3. **Cryptographic Byte-Digest Attestation**: Compute SHA-256 digests on raw files and attest zero corruption relative to sealed baseline.
4. **Initial Data Types and Schema Auditing**: Audit numerical dtypes and assert that all columns conform to float64 or int64.
5. **Missing Value Quantification by Feature**: Calculate exact null counts and missing percentages for all 9 physicochemical features.
6. **Missing Value Distribution Plot**: Render a bar chart displaying missing value percentages across water quality parameters.
7. **Raw Schema Profile Table Serialization**: Save compiled raw schema profile and missingness table to CSV.
8. **Raw Ingestion Assertion**: Assert that raw datasets match expected row counts (3276 and 720).

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day07_raw_ingestion.ipynb`](./day07_raw_ingestion.ipynb) - Executed interactive notebook with verified inline plots.
- [`day07_raw_ingestion.py`](./day07_raw_ingestion.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_7_Task_1/day07_raw_ingestion.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_7_Task_1/day07_raw_ingestion.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day7_task1_missingness_profile.png`](./outputs/figures/day7_task1_missingness_profile.png)
  ![day7_task1_missingness_profile.png](./outputs/figures/day7_task1_missingness_profile.png)

### Tables Generated:
- [`day7_task1_raw_schema_profile.csv`](./outputs/tables/day7_task1_raw_schema_profile.csv)

## 6. Assumptions and Methodology
- Raw datasets are immutable and read-only.
- Missingness is restricted to pH, Sulfate, and Trihalomethanes.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
