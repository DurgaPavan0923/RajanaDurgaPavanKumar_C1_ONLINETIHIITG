# Day 4 - Task 1: Dual-Track System Architecture
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 04 / Day 28

---

## 1. Objective & Operational Scope
Formalize the dual-track system architecture decoupling Track A (continuous telemetry stream forecasting) from Track B (static physicochemical potability classification).

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day04_system_architecture.ipynb`](./day04_system_architecture.ipynb) - Executed interactive notebook with verified outputs.
- [`day04_system_architecture.py`](./day04_system_architecture.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_4_Task_1/day04_system_architecture.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_4_Task_1/day04_system_architecture.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day4_task1_architecture_latency.png`](./outputs/figures/day4_task1_architecture_latency.png)
  ![day4_task1_architecture_latency.png](./outputs/figures/day4_task1_architecture_latency.png)

### Tables Generated:
- [`day4_task1_architecture_specs.csv`](./outputs/tables/day4_task1_architecture_specs.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
