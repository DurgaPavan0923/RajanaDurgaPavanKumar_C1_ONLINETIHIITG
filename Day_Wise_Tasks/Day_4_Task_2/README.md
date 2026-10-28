# Day 4 - Task 2: Serving Contract & Pydantic Schema Validation
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 04 / Day 28

---

## 1. Objective & Operational Scope
Define and validate strict REST API input schemas using Pydantic, asserting type safety, range guardrails, and graceful error handling.

## 2. Execution Steps
1. **Pydantic Schema Contract Definition**: Establish field constraints, types, and allowable ranges for water potability prediction payloads.
2. **Valid Payload Ingestion Verification**: Instantiate sample model payload and verify successful serialization into dictionary format.
3. **Schema Validation Exception Trapping**: Pass invalid payloads (e.g. pH < 0 or > 14) and confirm Pydantic raises ValidationError.
4. **JSON Schema Generation for OpenAPI Documentation**: Extract auto-generated JSON Schema used by FastAPI Swagger UI.
5. **Batch Payload Processing Throughput Test**: Validate 1000 simulated payloads sequentially to measure Pydantic parsing overhead.
6. **Schema Range Envelopes Plot Generation**: Render horizontal error-bar plot displaying permissible physical bounds for each sensor input.
7. **Serving Contract Schema Table Serialization**: Export schema properties and physical bounds table to CSV.
8. **Validation Gate Assertion**: Assert that schema requires all 9 critical parameters and traps out-of-bounds inputs.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day04_serving_contract.ipynb`](./day04_serving_contract.ipynb) - Executed interactive notebook with verified inline plots.
- [`day04_serving_contract.py`](./day04_serving_contract.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_4_Task_2/day04_serving_contract.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_4_Task_2/day04_serving_contract.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day4_task2_schema_ranges.png`](./outputs/figures/day4_task2_schema_ranges.png)
  ![day4_task2_schema_ranges.png](./outputs/figures/day4_task2_schema_ranges.png)

### Tables Generated:
- [`day4_task2_schema_contract.csv`](./outputs/tables/day4_task2_schema_contract.csv)

## 6. Assumptions and Methodology
- Pydantic schemas enforce type coercion and range bounding prior to model execution.
- Invalid HTTP payload structures return HTTP 422 Unprocessable Entity.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
