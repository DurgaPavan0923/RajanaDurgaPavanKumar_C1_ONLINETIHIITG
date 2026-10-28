# Day 9 - Task 2: Quarantined Test Lockbox Seal & Metadata
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 09 / Day 28

---

## 1. Objective & Operational Scope
Quarantine the held-out test partition, compute cryptographic SHA-256 seal, and lock it against developmental inspection.

## 2. Execution Steps
1. **Lockbox Partition Ingestion and Verification**: Extract the 492 held-out test samples and verify immutability parameters.
2. **Cryptographic Lockbox Hash Calculation**: Compute SHA-256 signature sealing the held-out test lockbox against alteration.
3. **Index Isolation and Disjointness Audit**: Assert that test indices share zero intersection with training or validation indices.
4. **Feature Column Immutability Check**: Assert that lockbox preserves identical feature schema as training sets.
5. **Quarantine Security Manifest Formulation**: Construct metadata dictionary declaring the quarantine lockbox sealed until final unblinding.
6. **Partition Index Allocation Diagnostic Plot**: Render partition allocation bar chart displaying isolated lockbox segment.
7. **Lockbox Manifest Table Export**: Export lockbox quarantine security manifest to CSV.
8. **Quarantine Integrity Gate**: Assert that index overlap is strictly zero and SHA-256 seal is valid.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day09_lockbox_isolation.ipynb`](./day09_lockbox_isolation.ipynb) - Executed interactive notebook with verified inline plots.
- [`day09_lockbox_isolation.py`](./day09_lockbox_isolation.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_9_Task_2/day09_lockbox_isolation.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_9_Task_2/day09_lockbox_isolation.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day9_task2_lockbox_isolation.png`](./outputs/figures/day9_task2_lockbox_isolation.png)
  ![day9_task2_lockbox_isolation.png](./outputs/figures/day9_task2_lockbox_isolation.png)

### Tables Generated:
- [`day9_task2_lockbox_manifest.csv`](./outputs/tables/day9_task2_lockbox_manifest.csv)

## 6. Assumptions and Methodology
- Test lockbox remains blinded until final unblinding milestone on Day 23.
- Any access to test labels during developmental training invalidates model certification.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
