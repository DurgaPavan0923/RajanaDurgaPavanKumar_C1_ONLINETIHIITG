# Day 1 - Task 2: Git Repository & Workspace Protocol
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 01 / Day 28

---

## 1. Objective & Operational Scope
Audit git repository structure, track committed artifacts, verify version control ignore rules, and ensure workspace hygiene.

## 2. Execution Steps
1. **Repository Directory Hierarchy Scan**: Index root directories and count nested files to monitor workspace complexity.
2. **Version Control Ignore Protocol Validation**: Verify that .gitignore properly covers virtual environments, credentials, caches, and large binary models.
3. **Git Remote & Branch Identity Verification**: Audit git branch state and confirm remote alignment to RajanaDurgaPavanKumar_C1_ONLINETIHIITG.
4. **Source Code Volume and Line Count Profiling**: Measure total lines of source code across Python modules, notebooks, and documentation.
5. **Disk Allocation Distribution Audit**: Quantify disk footprint of raw data, processed assets, production models, and documentation.
6. **Workspace Subsystem Distribution Plot**: Render a distribution donut chart visualizing disk allocation across repository subsystems.
7. **Workspace Audit Metrics Serialization**: Save workspace hierarchy summary and subsystem metrics to CSV.
8. **Repository Health Assertion**: Verify that zero untracked credentials or bloated binaries exceed safety limits.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day01_workspace_audit.ipynb`](./day01_workspace_audit.ipynb) - Executed interactive notebook with verified inline plots.
- [`day01_workspace_audit.py`](./day01_workspace_audit.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_1_Task_2/day01_workspace_audit.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_1_Task_2/day01_workspace_audit.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day1_task2_workspace_footprint.png`](./outputs/figures/day1_task2_workspace_footprint.png)
  ![day1_task2_workspace_footprint.png](./outputs/figures/day1_task2_workspace_footprint.png)

### Tables Generated:
- [`day1_task2_workspace_summary.csv`](./outputs/tables/day1_task2_workspace_summary.csv)

## 6. Assumptions and Methodology
- Git repository is initialized with main as default development branch.
- Local git working tree contains standard submodules and ignores virtual environment artifacts.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
