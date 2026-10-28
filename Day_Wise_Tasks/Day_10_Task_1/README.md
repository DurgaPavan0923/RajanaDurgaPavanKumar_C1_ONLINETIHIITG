# Day 10 - Task 1: Continuous Telemetry Dynamics & Time-Series EDA
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 10 / Day 28

---

## 1. Objective & Operational Scope
Perform exploratory data analysis on continuous underwater sensor streams, investigating diurnal dynamics, thermal stratification, and dissolved oxygen oscillations.

## 2. Execution Steps
1. **Continuous Telemetry Stream Ingestion**: Load underwater sensor stream telemetry and verify timestamp parsing.
2. **Diurnal Dissolved Oxygen Trend Analysis**: Extract hour of day and compute average dissolved oxygen by hour to observe photosynthetic cycles.
3. **Temperature vs Dissolved Oxygen Solubility Coupling**: Examine inverse relationship between water temperature and gas solubility.
4. **Turbidity Shock and Attenuation Profile**: Quantify turbidity spikes and evaluate relaxation half-life across the stream.
5. **pH Buffer Stability Assessment**: Measure variation of pH over continuous sensor monitoring window.
6. **Multi-Sensor Diurnal Dynamics Plot**: Render multi-panel time-series plot displaying continuous DO and Temperature trajectories.
7. **Telemetry Summary Statistics Serialization**: Serialize multi-channel descriptive statistics to CSV.
8. **Telemetry Continuity Assertion**: Assert that stream has non-empty valid observations across all 6 physical channels.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day10_environmental_eda.ipynb`](./day10_environmental_eda.ipynb) - Executed interactive notebook with verified inline plots.
- [`day10_environmental_eda.py`](./day10_environmental_eda.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_10_Task_1/day10_environmental_eda.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_10_Task_1/day10_environmental_eda.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day10_task1_sensor_streams.png`](./outputs/figures/day10_task1_sensor_streams.png)
  ![day10_task1_sensor_streams.png](./outputs/figures/day10_task1_sensor_streams.png)

### Tables Generated:
- [`day10_task1_telemetry_summary.csv`](./outputs/tables/day10_task1_telemetry_summary.csv)

## 6. Assumptions and Methodology
- Sensor telemetry captures continuous diurnal cycles under natural ambient conditions.
- Temperature and dissolved oxygen exhibit expected thermodynamic inverse coupling.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
