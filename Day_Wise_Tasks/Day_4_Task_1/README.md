# Day 4 - Task 1: Dual-Track System Architecture
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 04 / Day 28

---

## 1. Objective & Operational Scope
Formalize the dual-track system architecture decoupling Track A (continuous telemetry stream forecasting) from Track B (static physicochemical potability classification).

## 2. Execution Steps
1. **Architecture Subsystem Invariant Definitions**: Formalize technical boundary parameters: latency budgets, throughput targets, and update frequencies.
2. **Input Schema Contract Validation**: Verify required sensor and physicochemical feature counts for each subsystem.
3. **Decoupled Serving Boundary Inspection**: Confirm FastAPI router configuration separates telemetry streaming from static batch prediction.
4. **Shared Serialization Storage Footprint**: Measure production model artifact footprints in models/production/.
5. **Subsystem Ingestion Throughput Simulation**: Simulate concurrent requests across both tracks to verify throughput decoupling.
6. **Architecture Latency Budget Profile Plot**: Render a bar chart comparing latency budgets across dual-track endpoints.
7. **Architecture Contract Table Export**: Serialize dual-track architecture specifications table to CSV.
8. **Architecture Independence Assertion**: Assert that Track A and Track B input feature sets are completely defined.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day04_system_architecture.ipynb`](./day04_system_architecture.ipynb) - Executed interactive notebook with verified inline plots.
- [`day04_system_architecture.py`](./day04_system_architecture.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_4_Task_1/day04_system_architecture.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_4_Task_1/day04_system_architecture.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day4_task1_architecture_latency.png`](./outputs/figures/day4_task1_architecture_latency.png)
  ![day4_task1_architecture_latency.png](./outputs/figures/day4_task1_architecture_latency.png)

### Tables Generated:
- [`day4_task1_architecture_specs.csv`](./outputs/tables/day4_task1_architecture_specs.csv)

## 6. Assumptions and Methodology
- Track A operates on high-frequency streaming sensor telemetry with bounded drift.
- Track B handles point-in-time physicochemical water potability evaluations.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
