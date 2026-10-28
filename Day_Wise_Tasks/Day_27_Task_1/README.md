# Day 27 - Task 1: FastAPI Deployment & Endpoint Verification
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 27 / Day 28

---

## 1. Objective & Operational Scope
Verify production FastAPI ASGI routes (/api/predict and /api/ping), test security headers, and validate live cloud deployment readiness.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day27_deployment_verification.ipynb`](./day27_deployment_verification.ipynb) - Executed interactive notebook with verified outputs.
- [`day27_deployment_verification.py`](./day27_deployment_verification.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_27_Task_1/day27_deployment_verification.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_27_Task_1/day27_deployment_verification.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day27_task1_deployment_status.png`](./outputs/figures/day27_task1_deployment_status.png)
  ![day27_task1_deployment_status.png](./outputs/figures/day27_task1_deployment_status.png)

### Tables Generated:
- [`day27_task1_endpoint_specs.csv`](./outputs/tables/day27_task1_endpoint_specs.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
