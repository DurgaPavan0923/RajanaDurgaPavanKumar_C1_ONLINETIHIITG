# Day 2 - Task 2: WHO & EPA Regulatory Guardrail Thresholds
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 02 / Day 28

---

## 1. Objective & Operational Scope
Formulate machine-enforceable regulatory thresholds using World Health Organization (WHO) and EPA potable water guidelines.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day02_regulatory_standards.ipynb`](./day02_regulatory_standards.ipynb) - Executed interactive notebook with verified outputs.
- [`day02_regulatory_standards.py`](./day02_regulatory_standards.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_2_Task_2/day02_regulatory_standards.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_2_Task_2/day02_regulatory_standards.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day2_task2_regulatory_compliance.png`](./outputs/figures/day2_task2_regulatory_compliance.png)
  ![day2_task2_regulatory_compliance.png](./outputs/figures/day2_task2_regulatory_compliance.png)

### Tables Generated:
- [`day2_task2_regulatory_scorecard.csv`](./outputs/tables/day2_task2_regulatory_scorecard.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
