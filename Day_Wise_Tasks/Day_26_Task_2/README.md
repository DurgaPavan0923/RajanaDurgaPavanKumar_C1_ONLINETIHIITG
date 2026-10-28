# Day 26 - Task 2: Streaming Telemetry Simulation & Latency Benchmark
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 26 / Day 28

---

## 1. Objective & Operational Scope
Simulate real-time streaming telemetry ingestion over 48 hours and benchmark P50, P95, and P99 inference latency.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day26_latency_benchmark.ipynb`](./day26_latency_benchmark.ipynb) - Executed interactive notebook with verified outputs.
- [`day26_latency_benchmark.py`](./day26_latency_benchmark.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_26_Task_2/day26_latency_benchmark.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_26_Task_2/day26_latency_benchmark.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day26_task2_latency_profile.png`](./outputs/figures/day26_task2_latency_profile.png)
  ![day26_task2_latency_profile.png](./outputs/figures/day26_task2_latency_profile.png)

### Tables Generated:
- [`day26_task2_latency_benchmark.csv`](./outputs/tables/day26_task2_latency_benchmark.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
