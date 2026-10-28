# Day 27 - Task 2: Cloud Latency & Serverless Bundle Audit
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 27 / Day 28

---

## 1. Objective & Operational Scope
Audit serverless bundle size, cold-start latency mitigation, and runtime dependency constraints on Vercel.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day27_bundle_audit.ipynb`](./day27_bundle_audit.ipynb) - Executed interactive notebook with verified outputs.
- [`day27_bundle_audit.py`](./day27_bundle_audit.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_27_Task_2/day27_bundle_audit.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_27_Task_2/day27_bundle_audit.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day27_task2_bundle_breakdown.png`](./outputs/figures/day27_task2_bundle_breakdown.png)
  ![day27_task2_bundle_breakdown.png](./outputs/figures/day27_task2_bundle_breakdown.png)

### Tables Generated:
- [`day27_task2_bundle_audit.csv`](./outputs/tables/day27_task2_bundle_audit.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
