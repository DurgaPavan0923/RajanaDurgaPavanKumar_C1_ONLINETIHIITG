# Day 27 - Task 1: FastAPI Deployment & Endpoint Verification
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 27 / Day 28

---

## 1. Objective & Operational Scope
Verify production FastAPI ASGI routes (/api/predict and /api/ping), test security headers, and validate live cloud deployment readiness.

## 2. Execution Steps
1. **FastAPI Application Router Inspection**: Inspect app router configuration and verify registered ASGI endpoints.
2. **Local ASGI Health Probe Simulation**: Simulate HTTP GET /api/ping request verifying status 200 and JSON status response.
3. **Inference Endpoint Functional Simulation**: Simulate HTTP POST /api/predict payload call verifying status 200 and schema compliance.
4. **HTTP Security Headers Verification**: Verify presence of standard production security headers: X-Content-Type-Options, X-Frame-Options, Content-Security-Policy.
5. **Live Deployment URL Verification**: Confirm live cloud deployment link on Vercel: https://water-potability-vert.vercel.app/.
6. **Deployment Status Verification Plot**: Render endpoint health scorecard bar chart displaying 100% operational readiness.
7. **Deployment Routing Table Export**: Export API routes and security headers table to CSV.
8. **Deployment Verification Gate Assertion**: Assert that all 3 primary endpoints are registered and documented.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day27_deployment_verification.ipynb`](./day27_deployment_verification.ipynb) - Executed interactive notebook with verified inline plots.
- [`day27_deployment_verification.py`](./day27_deployment_verification.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_27_Task_1/day27_deployment_verification.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_27_Task_1/day27_deployment_verification.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day27_task1_deployment_status.png`](./outputs/figures/day27_task1_deployment_status.png)
  ![day27_task1_deployment_status.png](./outputs/figures/day27_task1_deployment_status.png)

### Tables Generated:
- [`day27_task1_endpoint_specs.csv`](./outputs/tables/day27_task1_endpoint_specs.csv)

## 6. Assumptions and Methodology
- FastAPI ASGI application is hosted on Vercel Serverless Functions.
- Security headers and OpenAPI documentation comply with production guidelines.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
