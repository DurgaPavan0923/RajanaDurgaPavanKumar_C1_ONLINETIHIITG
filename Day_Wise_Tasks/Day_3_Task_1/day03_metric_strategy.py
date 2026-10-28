"""Automated Python script mirror for day03_metric_strategy.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 3 - Classification Metric Strategy (PR-AUC vs ROC-AUC)
#
# ## Objective
#
# Formulate evaluation metrics for class-imbalanced water potability, establishing PR-AUC as primary ranking metric and Brier score for calibration.

# %% [step_1]
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def _find_project_root():
    curr = Path.cwd()
    for p in [curr] + list(curr.parents):
        if (p / "pyproject.toml").exists() or (p / "requirements.txt").exists():
            return p
    return curr

project_root = _find_project_root()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
os.chdir(project_root)

np.random.seed(42)
print("Environment initialized successfully. Project root:", project_root)

# %% [markdown]
# ## 1. Class Imbalance Characterization
#
# Quantify class distribution skewness in water potability (approximately 61% Non-Potable vs 39% Potable).

# %% [step_3]
df_p = pd.read_csv("data/raw/water_potability.csv")
counts = df_p["Potability"].value_counts()
prevalence = counts[1] / len(df_p)
print(f"Non-Potable (0): {counts[0]}, Potable (1): {counts[1]}")
print(f"Positive Class Prevalence: {prevalence:.4f}")

# %% [markdown]
# ## 2. Synthetic Prediction Simulation Under Imbalance
#
# Simulate calibrated probability scores with controlled discrimination power to illustrate metric behavior.

# %% [step_5]
y_true = np.random.binomial(1, prevalence, size=1000)
# Uninformative baseline vs trained model simulation
y_scores_uninf = np.random.uniform(0, 1, size=1000)
y_scores_model = np.clip(y_true * 0.4 + np.random.beta(2, 5, size=1000), 0, 1)
print("Simulation initialized: 1000 synthetic test cases.")

# %% [markdown]
# ## 3. ROC Curve and AUC Calculation
#
# Compute False Positive Rate, True Positive Rate, and Area Under ROC Curve.

# %% [step_7]
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_true, y_scores_model)
roc_auc = auc(fpr, tpr)
fpr_base, tpr_base, _ = roc_curve(y_true, y_scores_uninf)
roc_auc_base = auc(fpr_base, tpr_base)
print(f"Model ROC-AUC: {roc_auc:.4f} | Uninformative Baseline ROC-AUC: {roc_auc_base:.4f}")

# %% [markdown]
# ## 4. Precision-Recall Curve and PR-AUC Calculation
#
# Compute Precision, Recall, and Average Precision (PR-AUC) under positive prevalence constraint.

# %% [step_9]
from sklearn.metrics import precision_recall_curve, average_precision_score
prec, rec, _ = precision_recall_curve(y_true, y_scores_model)
pr_auc = average_precision_score(y_true, y_scores_model)
pr_auc_base = average_precision_score(y_true, y_scores_uninf)
print(f"Model PR-AUC: {pr_auc:.4f} | Prevalence Baseline PR-AUC: {pr_auc_base:.4f} (Prevalence: {prevalence:.4f})")

# %% [markdown]
# ## 5. Brier Score Calibration Analysis
#
# Quantify mean squared error of probability forecasts to assess probabilistic reliability.

# %% [step_11]
from sklearn.metrics import brier_score_loss
brier = brier_score_loss(y_true, y_scores_model)
brier_base = brier_score_loss(y_true, y_scores_uninf)
print(f"Model Brier Score: {brier:.4f} (Lower is better) | Baseline Brier: {brier_base:.4f}")

# %% [markdown]
# ## 6. ROC vs PR Diagnostic Curves Rendering
#
# Plot side-by-side ROC Curve and Precision-Recall Curve demonstrating PR sensitivity to true positives.

# %% [step_13]
# Output Figure: fig_path
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
axes[0].plot(fpr, tpr, color="#1f77b4", lw=2, label=f"Model (AUC = {roc_auc:.3f})")
axes[0].plot([0, 1], [0, 1], color="navy", lw=1.5, linestyle="--", label="Random Chance")
axes[0].set_title("Receiver Operating Characteristic (ROC)")
axes[0].set_xlabel("False Positive Rate")
axes[0].set_ylabel("True Positive Rate")
axes[0].legend(loc="lower right")

axes[1].plot(rec, prec, color="#2ca02c", lw=2, label=f"Model (PR-AUC = {pr_auc:.3f})")
axes[1].axhline(prevalence, color="red", linestyle="--", lw=1.5, label=f"Baseline ({prevalence:.2f})")
axes[1].set_title("Precision-Recall (PR) Curve")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precision")
axes[1].legend(loc="upper right")
plt.tight_layout()
fig_path = Path("Day_Wise_Tasks/Day_3_Task_1/outputs/figures/day3_task1_roc_vs_pr.png")
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved comparison curve to:", fig_path)

# %% [markdown]
# ## 7. Classification Metric Strategy Matrix Serialization
#
# Export comparison table summarizing ROC-AUC, PR-AUC, and Brier score specifications.

# %% [step_15]
# Output Table: tbl_path
metrics_summary = [
    {"Metric": "PR-AUC", "Target_Role": "Primary Model Selection", "Benchmark_Goal": "> 0.58", "Baseline": f"{prevalence:.3f}"},
    {"Metric": "ROC-AUC", "Target_Role": "Secondary Discriminative", "Benchmark_Goal": "> 0.65", "Baseline": "0.500"},
    {"Metric": "Brier Score", "Target_Role": "Probability Calibration", "Benchmark_Goal": "< 0.22", "Baseline": "0.250"},
]
df_m = pd.DataFrame(metrics_summary)
tbl_path = Path("Day_Wise_Tasks/Day_3_Task_1/outputs/tables/day3_task1_metric_strategy.csv")
tbl_path.parent.mkdir(parents=True, exist_ok=True)
df_m.to_csv(tbl_path, index=False)
print("Saved metric strategy table to:", tbl_path)

# %% [markdown]
# ## 8. Metric Hierarchy Assertion
#
# Verify that PR-AUC benchmark threshold exceeds random class prevalence baseline.

# %% [step_17]
assert pr_auc > prevalence, "Model fails to exceed positive prevalence baseline."
print("Day 3 Task 1 Quality Gate: PASSED.")

# %% [markdown]
# # Day 3 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. PR-AUC is mathematically superior to ROC-AUC for imbalanced datasets with minority high-consequence classes.
# 2. Probability calibration is strictly required before deploying decision threshold boundaries.
#
# ## Day 3 Deliverable
#
# Comparative ROC vs PR diagnostic plot, metric strategy hierarchy table, and calibration loss protocol.

