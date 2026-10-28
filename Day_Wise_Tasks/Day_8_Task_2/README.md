# Day 8 - Task 2: Validation Rules Matrix & Quality Scorecard
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 08 / Day 28

---

## 1. Objective & Operational Scope
Formulate machine-enforceable YAML validation rules and construct a unified data quality scorecard across all sensor feeds.

## 2. Execution Steps
1. **Machine-Enforceable Rule Matrix Definition**: Construct rule matrix encoding check types: non-null, minimum, maximum, and monotonic time.
2. **Timestamp Sampling Interval and Jitter Audit**: Calculate delta between successive telemetry timestamps to assess temporal jitter.
3. **Rule Matrix Automated Execution**: Execute validation rules across telemetry stream and log pass/fail status for each rule.
4. **Unified Quality Scorecard Compilation**: Synthesize completeness, validity, and timeliness scores into an aggregate data quality index.
5. **Temporal Gap Identification**: Identify any temporal gap exceeding 3 times the median sampling interval.
6. **Validation Rule Pass Rate Radar/Bar Plot**: Render bar chart displaying compliance percentage across all defined validation rules.
7. **Unified Quality Scorecard Export**: Save compiled validation rules matrix and scorecard table to CSV.
8. **Rule Verification Gate**: Assert that all validation rules achieve PASS status.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day08_validation_rules.ipynb`](./day08_validation_rules.ipynb) - Executed interactive notebook with verified inline plots.
- [`day08_validation_rules.py`](./day08_validation_rules.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_8_Task_2/day08_validation_rules.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_8_Task_2/day08_validation_rules.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day8_task2_validation_pass_rates.png`](./outputs/figures/day8_task2_validation_pass_rates.png)
  ![day8_task2_validation_pass_rates.png](./outputs/figures/day8_task2_validation_pass_rates.png)

### Tables Generated:
- [`day8_task2_quality_scorecard.csv`](./outputs/tables/day8_task2_quality_scorecard.csv)

## 6. Assumptions and Methodology
- Telemetry arrives with strictly monotonic timestamps.
- Jitter is bounded and conforms to steady stream expectations.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
