"""Automated Python script mirror for day02_domain_research.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 2 - Physicochemical Domain & Parameter Coupling
#
# ## Objective
#
# Investigate physical parameter couplings across drinking water quality metrics and assess empirical distributions against environmental dynamics.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_2_Task_1"
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
# ## 1. Physicochemical Dataset Ingestion
#
# Ingest tabular water potability records and examine dimensional shape and basic statistics.

# %% [step_3]
df_water = pd.read_csv("data/raw/water_potability.csv")
print("Raw Water Dataset Shape:", df_water.shape)
print("Target Potability Distribution:")
print(df_water["Potability"].value_counts(normalize=True))

# %% [markdown]
# ## 2. Correlation Analysis Between Critical Parameters
#
# Compute Pearson correlation coefficients across pH, Hardness, Solids, Chloramines, and Sulfate.

# %% [step_5]
feature_cols = [c for c in df_water.columns if c != "Potability"]
corr_mat = df_water[feature_cols].corr()
print("Top Feature Correlations with pH:")
print(corr_mat["ph"].sort_values(ascending=False))

# %% [markdown]
# ## 3. pH and Sulfate Distribution Discretization
#
# Calculate quartile boundaries and standard deviations for pH and Sulfate distributions.

# %% [step_7]
stats_ph = df_water["ph"].describe()
stats_sulf = df_water["Sulfate"].describe()
df_domain_stats = pd.DataFrame({"pH": stats_ph, "Sulfate": stats_sulf})
print("Key Domain Distributions:")
print(df_domain_stats)

# %% [markdown]
# ## 4. Turbidity and Solids Interaction Analysis
#
# Examine the physical relationship between dissolved solids and optical turbidity.

# %% [step_9]
df_clean = df_water.dropna(subset=["Solids", "Turbidity"])
cov_val = np.cov(df_clean["Solids"], df_clean["Turbidity"])[0, 1]
corr_val = df_clean["Solids"].corr(df_clean["Turbidity"])
print(f"Solids-Turbidity Covariance: {cov_val:.2f}, Correlation: {corr_val:.4f}")

# %% [markdown]
# ## 5. Hardness-Conductivity Mineralization Profile
#
# Assess total dissolved ionic conductance in relation to mineral hardness content.

# %% [step_11]
df_clean2 = df_water.dropna(subset=["Hardness", "Conductivity"])
slope, intercept = np.polyfit(df_clean2["Hardness"], df_clean2["Conductivity"], 1)
print(f"Empirical Mineral Trend: Conductivity = {slope:.3f} * Hardness + {intercept:.2f}")

# %% [markdown]
# ## 6. Correlation Matrix Heatmap Generation
#
# Render an annotated correlation matrix heatmap visualizing parameter inter-dependencies.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.matshow(corr_mat, cmap="coolwarm", vmin=-0.15, vmax=0.15)
fig.colorbar(cax)
ax.set_xticks(range(len(feature_cols)))
ax.set_yticks(range(len(feature_cols)))
ax.set_xticklabels(feature_cols, rotation=45, ha="left", fontsize=9)
ax.set_yticklabels(feature_cols, fontsize=9)
ax.set_title("Day 2 Task 1: Physicochemical Parameter Correlation Matrix", pad=20, fontsize=11)
plt.tight_layout()
fig_path = FIG_DIR / "day2_task1_correlation_matrix.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved correlation figure to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Domain Correlation Table Serialization
#
# Serialize full cross-parameter correlation matrix to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path)
tbl_path = TBL_DIR / "day2_task1_correlation_matrix.csv"
df_corr_matrix = corr_mat.round(4)
print(df_corr_matrix.to_string())
df_corr_matrix.to_csv(tbl_path)
print("Saved correlation table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Parameter Independence Assertion
#
# Verify absence of collinearity (all |r| < 0.35) confirming feature diversity.

# %% [step_17]
max_corr = corr_mat.abs().replace(1.0, 0.0).max().max()
print(f"Max absolute pairwise correlation: {max_corr:.4f}")
assert max_corr < 0.35, "Unexpected severe collinearity detected."
print("Day 2 Task 1 Quality Gate: PASSED.")

# %% [markdown]
# # Day 2 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Physicochemical parameters follow continuous real distributions.
# 2. Independent measurements exhibit orthogonal variance structure suitable for tree ensembles.
#
# ## Day 2 Deliverable
#
# Correlation matrix plot, domain summary statistics table, and parameter orthogonality audit.

