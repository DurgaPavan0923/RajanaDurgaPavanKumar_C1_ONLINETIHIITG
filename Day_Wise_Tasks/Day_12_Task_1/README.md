# Day 12 - Task 1: Zero-Leakage Invariance Verification Test Suite
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 12 / Day 28

---

## 1. Objective & Operational Scope
Execute an automated five-point data leakage assertion test suite verifying complete temporal isolation between train, validation, and test datasets.

## 2. Execution Steps
1. **Dataset V1 Partitions Ingestion**: Load chronological train, validation, and test partitions from data/processed/.
2. **Test 1: Index Disjointness Assertion**: Assert that index sets for train, validation, and test partitions are completely mutually exclusive.
3. **Test 2: Chronological Ordering Monotonicity**: Assert that maximum train timestamp precedes minimum validation timestamp.
4. **Test 3: Preprocessor Scaler Fitting Isolation**: Assert that StandardScaler is fitted exclusively on train fold without knowledge of validation mean.
5. **Test 4: Target Imbalance Invariance Across Folds**: Assert that target positive class prevalence remains within 10% bounds across partitions.
6. **Zero-Leakage Five-Point Verification Grid Plot**: Render scorecard plot displaying results of the automated zero-leakage test suite.
7. **Zero-Leakage Audit Table Serialization**: Serialize automated leakage test scorecard to CSV.
8. **Zero Leakage Gate Assertion**: Assert that all 5 zero-leakage tests achieve PASS status.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day12_zero_leakage_checks.ipynb`](./day12_zero_leakage_checks.ipynb) - Executed interactive notebook with verified inline plots.
- [`day12_zero_leakage_checks.py`](./day12_zero_leakage_checks.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_12_Task_1/day12_zero_leakage_checks.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_12_Task_1/day12_zero_leakage_checks.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day12_task1_leakage_audit.png`](./outputs/figures/day12_task1_leakage_audit.png)
  ![day12_task1_leakage_audit.png](./outputs/figures/day12_task1_leakage_audit.png)

### Tables Generated:
- [`day12_task1_leakage_audit.csv`](./outputs/tables/day12_task1_leakage_audit.csv)

## 6. Assumptions and Methodology
- Data leakage invalidates all downstream generalization claims.
- Preprocessors must be fit exclusively on training data.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
