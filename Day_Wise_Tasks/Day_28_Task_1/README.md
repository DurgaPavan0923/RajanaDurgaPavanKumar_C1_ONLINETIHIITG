# Day 28 - Task 1: Final Technical Presentation Slide Pack
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Phase Progression: Day 28 / Day 28

---

## 1. Objective & Operational Scope
Compile the complete slide deck inventory, speaker scripts, technical exhibits, and demonstration talking points for the final review meeting.

## 2. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 3. Files in this Directory
- [`day28_presentation_pack.ipynb`](./day28_presentation_pack.ipynb) - Executed interactive notebook with verified outputs.
- [`day28_presentation_pack.py`](./day28_presentation_pack.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 4. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_28_Task_1/day28_presentation_pack.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_28_Task_1/day28_presentation_pack.ipynb
```

## 5. Output Artifacts & Verification Status
### Figures Generated:
- [`day28_task1_presentation_timeline.png`](./outputs/figures/day28_task1_presentation_timeline.png)
  ![day28_task1_presentation_timeline.png](./outputs/figures/day28_task1_presentation_timeline.png)

### Tables Generated:
- [`day28_task1_presentation_inventory.csv`](./outputs/tables/day28_task1_presentation_inventory.csv)

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
