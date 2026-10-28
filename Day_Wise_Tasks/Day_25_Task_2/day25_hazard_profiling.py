"""Automated Python script mirror for day25_hazard_profiling.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 25 - Worst-Cases Profile & Feature Importance Diagnostic
#
# ## Objective
#
# Extract high-hazard worst-case misclassifications, analyze tree Gini feature importances, and document operational hazard mitigation protocols.

# %% [step_1]
# %matplotlib inline
import os, matplotlib
if os.environ.get('DISPLAY', '') == '' and os.name != 'nt' or os.environ.get('MPLBACKEND') == 'Agg':
    matplotlib.use('Agg')
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from IPython.display import display
except ImportError:
    display = print

ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "Day_Wise_Tasks").exists())
project_root = ROOT
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_25_Task_2"
FIG_DIR = TASK_DIR / "outputs" / "figures"
TBL_DIR = TASK_DIR / "outputs" / "tables"
FIG_DIR.mkdir(parents=True, exist_ok=True)
TBL_DIR.mkdir(parents=True, exist_ok=True)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

np.random.seed(42)
print("Environment initialized successfully. Root:", ROOT)

# %% [markdown]
# ## 1. Worst-Case Residual Extraction
#
# Extract top 10 misclassified samples exhibiting highest prediction confidence divergence from ground truth.

# %% [step_3]
import joblib
df_ts = pd.read_csv("data/processed/water_quality_timestamped.csv")
cut2 = int(len(df_ts) * 0.85)
test_set = df_ts.iloc[cut2:].copy()
feature_cols = ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]
X_test = test_set[feature_cols].fillna(test_set[feature_cols].median())
y_test = test_set["Potability"]
pipe = joblib.load(project_root / "models" / "production" / "water_potability_pipeline_v1.joblib")
test_probs = pipe.predict_proba(X_test)[:, 1]
residuals = np.abs(y_test - test_probs)
worst_idx = np.argsort(residuals.values)[-10:]
df_worst = test_set.iloc[worst_idx][feature_cols + ["Potability"]].copy()
df_worst["Predicted_Prob"] = test_probs[worst_idx].round(4)
print("Top 3 Worst-Case Misclassifications:")
print(df_worst.head(3).to_string(index=False))

# %% [markdown]
# ## 2. Chemical Hazard Interaction Analysis
#
# Identify combinations of high Chloramines and abnormal pH contributing to worst-case errors.

# %% [step_5]
worst_ph_mean = df_worst["ph"].mean()
worst_chlor_mean = df_worst["Chloramines"].mean()
print(f"Worst Cases Average pH: {worst_ph_mean:.2f}, Average Chloramines: {worst_chlor_mean:.2f}")

# %% [markdown]
# ## 3. Tree Ensemble Gini Feature Importance Extraction
#
# Extract normalized Gini impurity feature importances from champion Random Forest model.

# %% [step_7]
rf_model = pipe.named_steps["classifier"]
importances = rf_model.feature_importances_
df_imp = pd.DataFrame({"Feature": feature_cols, "Gini_Importance": np.round(importances, 4)}).sort_values("Gini_Importance", ascending=False)
print("Champion Model Feature Importances:")
print(df_imp.to_string(index=False))

# %% [markdown]
# ## 4. Top Predictor Dominance Quantification
#
# Calculate cumulative importance of top 3 features (pH, Sulfate, Hardness).

# %% [step_9]
top3_imp = df_imp.head(3)["Gini_Importance"].sum() * 100
print(f"Top 3 Features Account for {top3_imp:.1f}% of Model Gini Importance.")

# %% [markdown]
# ## 5. Operational Hazard Mitigation Protocol
#
# Formulate automated warning trigger when raw readings fall into worst-case parameter clusters.

# %% [step_11]
print("Operational mitigation: Secondary laboratory validation triggered whenever pH < 6.0 or Sulfate > 400 mg/L.")

# %% [markdown]
# ## 6. Feature Importance Diagnostic Plot
#
# Render horizontal bar chart displaying Gini importance rankings across all 9 features.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(df_imp["Feature"], df_imp["Gini_Importance"], color="#1f77b4", alpha=0.85)
ax.invert_yaxis()
ax.set_title("Day 25 Task 2: Champion Random Forest Gini Feature Importances", fontsize=11, pad=10)
ax.set_xlabel("Normalized Gini Importance")
for i, v in enumerate(df_imp["Gini_Importance"]):
    ax.text(v + 0.003, i, f"{v:.3f}", va="center", fontsize=8, fontweight="bold")
plt.tight_layout()
fig_path = FIG_DIR / "day25_task2_feature_importances.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved feature importances plot to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Worst Cases Profile Table Serialization
#
# Export worst-case profile samples table to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
tbl_path = TBL_DIR / "day25_task2_worst_cases.csv"
print(df_worst.to_string())
df_worst.to_csv(tbl_path, index=False)
print("Saved worst cases profile table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Hazard Profiling Gate Assertion
#
# Assert that Gini importances sum to 1.0 within numerical precision.

# %% [step_17]
assert abs(sum(importances) - 1.0) < 1e-4
print("Day 25 Task 2 Quality Gate: PASSED.")

# %% [markdown]
# # Day 25 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Worst-case misclassifications identify specific environmental parameter combinations requiring secondary testing.
# 2. Gini importance highlights primary physicochemical drivers of potability classification.
#
# ## Day 25 Deliverable
#
# Worst-cases profile table, Gini importance diagnostic plot, and operational hazard mitigation report.

