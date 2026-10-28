# Day 6 - Task 2: Cryptographic Checksum Certification
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 06 / Day 28

---

## 1. Objective & Operational Scope
Compute and certify SHA-256 cryptographic digests for raw and processed datasets, guaranteeing byte-level immutability against corruption.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day06_checksum_certification.ipynb`](./day06_checksum_certification.ipynb) - Executed interactive notebook with verified outputs.
- [`day06_checksum_certification.py`](./day06_checksum_certification.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_6_Task_2/day06_checksum_certification.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_6_Task_2/day06_checksum_certification.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day6_task2_checksum_profile.png`](./outputs/figures/day6_task2_checksum_profile.png)
  ![day6_task2_checksum_profile.png](./outputs/figures/day6_task2_checksum_profile.png)

### Tables Generated:
- [`day6_task2_checksum_manifest.csv`](./outputs/tables/day6_task2_checksum_manifest.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
