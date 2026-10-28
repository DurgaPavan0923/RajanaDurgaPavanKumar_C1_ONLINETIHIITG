# Day 23 - Task 1: Quarantined Test Lockbox Unblinding & Performance Audit
### Technology Innovation Hub (TIH), IIT Guwahati - AI/ML Internship (Cohort 4)
- Candidate: Rajana Durga Pavan Kumar
- Group: C1
- Target Repository: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
- Assigned Mentor: [Sushil Meher](https://www.linkedin.com/in/nightcoder44332211/), Teaching Assistant at Indian Institute of Technology, Guwahati
- Phase Progression: Day 23 / Day 28

---

## 1. Objective & Operational Scope
Execute the single authorized unblinding evaluation pass on the 492 held-out test samples, calculating test PR-AUC, ROC-AUC, Brier score, and accuracy.

## 2. Execution Steps
1. **Single-Pass Test Lockbox Unblinding**: Unblind and ingest the quarantined test lockbox dataset for final evaluation.
2. **Production Model Deserialization for Test Pass**: Load serialized champion pipeline from models/production/.
3. **Test Probability Prediction Generation**: Generate predicted potability probabilities on unblinded test samples.
4. **Core Evaluation Metrics Computation**: Compute final test PR-AUC, ROC-AUC, Brier score, and accuracy at 0.5 threshold.
5. **Validation vs Test Generalization Gap Analysis**: Compare validation PR-AUC (0.595) against test PR-AUC to confirm zero degradation.
6. **Test Confusion Matrix Rendering**: Render confusion matrix heatmap displaying true positives, true negatives, and false alarms on test set.
7. **Test Performance Metrics Table Serialization**: Export finalized unblinded test metrics table to CSV.
8. **Final Test Audit Gate Assertion**: Assert that PR-AUC exceeds 0.58 and Brier score is < 0.22.

## 3. Methodology & Safeguards
- Reproducibility Guarantee: Deterministic execution pinned via random seed 42 across NumPy, Scikit-learn, and XGBoost.
- Data Leakage Immunity: Temporal causality strictly preserved (`shift >= 1` causal rolling windows); preprocessing fit solely on training folds.
- Regulatory Framework: World Health Organization (WHO 4th Edition) & EPA primary drinking water benchmarks.

## 4. Files in this Directory
- [`day23_test_evaluation.ipynb`](./day23_test_evaluation.ipynb) - Executed interactive notebook with verified inline plots.
- [`day23_test_evaluation.py`](./day23_test_evaluation.py) - Full 1-to-1 Python script mirror.
- [`outputs/figures/`](./outputs/figures/) - Directory containing visual diagnostics and plots.
- [`outputs/tables/`](./outputs/tables/) - Directory containing serialized metric tables.

## 5. How to Run / Verify
Execute either the notebook or the Python script directly from the repository root:

```bash
# Run Python script mirror
python Day_Wise_Tasks/Day_23_Task_1/day23_test_evaluation.py

# Or execute notebook inplace
jupyter nbconvert --to notebook --execute --inplace Day_Wise_Tasks/Day_23_Task_1/day23_test_evaluation.ipynb
```

## 6. Output Artifacts & Verification Status
### Figures Generated:
- [`day23_task1_test_confusion_matrix.png`](./outputs/figures/day23_task1_test_confusion_matrix.png)
  ![day23_task1_test_confusion_matrix.png](./outputs/figures/day23_task1_test_confusion_matrix.png)

### Tables Generated:
- [`day23_task1_test_performance.csv`](./outputs/tables/day23_task1_test_performance.csv)

## 6. Assumptions and Methodology
- Test unblinding occurs exactly once without iterative post-test tuning.
- Generalization gap under 0.03 confirms absence of data leakage or overfitting.

- Audit Verdict: PASSED & VERIFIED
- Test Integrity: Monitored and validated via `pytest tests/ -v`.
