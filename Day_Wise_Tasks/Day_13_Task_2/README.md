# Day 13 - Task 2: Feature Expansion Catalog & Traceability Report
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 13 / Day 28

---

## 1. Objective & Operational Scope
Construct a comprehensive feature catalog cataloging all 62 engineered features with transformation mathematical formulas and variance statistics.

## 2. Execution Steps
1. **Feature Classification Hierarchy**: Group features into 4 distinct functional tiers: Base Physicochemical, Temporal Lags, Rolling Volatility, and Domain Ratios.
2. **Feature Catalog Metadata Compilation**: Compile detailed feature catalog entries: name, parent_feature, window_size, formula, and physical units.
3. **Feature Total Count Verification**: Assert that total engineered catalog comprises exactly 62 features.
4. **Feature Importance Ranking Simulation**: Simulate feature importance scores to assess potential discriminative power.
5. **Feature Invariance and Lineage Verification**: Assert that every feature traces back to valid raw inputs without orphaned dependencies.
6. **Feature Category Breakdown Plot**: Render a bar chart displaying feature allocation across functional tiers.
7. **Feature Catalog Table Export**: Export compiled feature catalog dictionary to CSV.
8. **Catalog Completeness Assertion**: Assert that total feature count matches 62 exactly.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day13_feature_catalog.ipynb`](./day13_feature_catalog.ipynb) - Executed interactive notebook with verified inline plots.
- [`day13_feature_catalog.py`](./day13_feature_catalog.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_13_Task_2/day13_feature_catalog.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_13_Task_2/day13_feature_catalog.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day13_task2_feature_catalog_breakdown.png`](./outputs/figures/day13_task2_feature_catalog_breakdown.png)
  ![day13_task2_feature_catalog_breakdown.png](./outputs/figures/day13_task2_feature_catalog_breakdown.png)

### Tables Generated:
- [`day13_task2_feature_catalog.csv`](./outputs/tables/day13_task2_feature_catalog.csv)

## 6. Assumptions and Methodology
- 62 engineered features provide complete coverage across temporal and physicochemical interactions.
- Feature catalog serves as immutable reference dictionary for production inference.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
