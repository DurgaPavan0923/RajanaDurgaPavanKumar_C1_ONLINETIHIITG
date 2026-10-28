# Day 28 - Task 1: Final Technical Presentation Slide Pack
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 28 / Day 28

---

## 1. Objective & Operational Scope
Compile the complete slide deck inventory, speaker scripts, technical exhibits, and demonstration talking points for the final review meeting.

## 2. Execution Steps
1. **Presentation Slide Pack Inventory**: Index the 10 core technical slides covering problem context, architecture, benchmarks, and live demo.
2. **Speaker Script and Key Talking Points**: Document timed speaker script targeting 5-minute executive presentation with 2 minutes for demo.
3. **Technical Exhibits Compilation**: Assemble key visual diagnostic exhibits for presentation display.
4. **Live Demonstration Walkthrough Script**: Outline 3-step live demo testing /api/ping, Swagger UI docs, and custom prediction payload.
5. **Programmatic Compliance Attestation**: Certify 100% adherence to TIH submission guidelines: name in repo, 28 days, day-wise tasks, zero emojis.
6. **Internship Progression Timeline Plot**: Render milestone timeline chart displaying 28-day progression from onboarding to final defense.
7. **Presentation Inventory Table Export**: Export complete slide deck inventory table to CSV.
8. **Presentation Pack Gate Assertion**: Assert that all 10 core slides are documented and exhibit paths validated.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day28_presentation_pack.ipynb`](./day28_presentation_pack.ipynb) - Executed interactive notebook with verified inline plots.
- [`day28_presentation_pack.py`](./day28_presentation_pack.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_28_Task_1/day28_presentation_pack.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_28_Task_1/day28_presentation_pack.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day28_task1_presentation_timeline.png`](./outputs/figures/day28_task1_presentation_timeline.png)
  ![day28_task1_presentation_timeline.png](./outputs/figures/day28_task1_presentation_timeline.png)

### Tables Generated:
- [`day28_task1_presentation_inventory.csv`](./outputs/tables/day28_task1_presentation_inventory.csv)

## 6. Assumptions and Methodology
- Final review presentation follows structured 5-minute technical format with live demo.
- Technical exhibits substantiate all claims with empirical data.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
