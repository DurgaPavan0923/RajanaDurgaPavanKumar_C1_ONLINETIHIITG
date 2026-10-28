# Day 6 - Task 2: Cryptographic Checksum Certification
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 06 / Day 28

---

## 1. Objective & Operational Scope
Compute and certify SHA-256 cryptographic digests for raw and processed datasets, guaranteeing byte-level immutability against corruption.

## 2. Execution Steps
1. **SHA-256 Digest Computation Engine**: Define byte-level streaming SHA-256 calculation function for arbitrary file assets.
2. **Raw Datasets Checksum Computation**: Compute cryptographic checksums for raw telemetry stream and tabular potability CSV files.
3. **Processed Dataset Partitions Checksum Audit**: Compute checksums for processed Parquet partitions in data/processed/.
4. **Cryptographic Collision Resistance Check**: Verify that all calculated digests are mutually unique and 64 hex characters in length.
5. **Dataset Tamper Resistance Simulation**: Demonstrate that modifying a single character alters the output SHA-256 avalanche effect.
6. **Checksum Certification File Profile Plot**: Render horizontal bar chart displaying byte sizes and certification status of sealed datasets.
7. **Checksum Certificate Table Serialization**: Serialize certified cryptographic manifest table to CSV.
8. **Immutability Seal Assertion**: Assert that raw datasets exist and match valid non-empty SHA-256 signatures.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day06_checksum_certification.ipynb`](./day06_checksum_certification.ipynb) - Executed interactive notebook with verified inline plots.
- [`day06_checksum_certification.py`](./day06_checksum_certification.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_6_Task_2/day06_checksum_certification.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_6_Task_2/day06_checksum_certification.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day6_task2_checksum_profile.png`](./outputs/figures/day6_task2_checksum_profile.png)
  ![day6_task2_checksum_profile.png](./outputs/figures/day6_task2_checksum_profile.png)

### Tables Generated:
- [`day6_task2_checksum_manifest.csv`](./outputs/tables/day6_task2_checksum_manifest.csv)

## 6. Assumptions and Methodology
- SHA-256 provides collision-free cryptographic hashing for dataset integrity certification.
- Sealed checksums are immutable throughout the developmental lifecycle.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
