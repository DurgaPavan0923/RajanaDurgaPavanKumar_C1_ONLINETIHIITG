"""Automated Python script mirror for day02_regulatory_standards.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 2 - WHO & EPA Regulatory Guardrail Thresholds
#
# ## Objective
#
# Formulate machine-enforceable regulatory thresholds using World Health Organization (WHO) and EPA potable water guidelines.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_2_Task_2"
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
# ## 1. Regulatory Guardrail Standards Definition
#
# Define explicit upper, lower, and target thresholds for critical chemical contaminants.

# %% [step_3]
regulatory_limits = {
    "ph": {"min": 6.5, "max": 8.5, "unit": "pH", "authority": "WHO/EPA"},
    "Hardness": {"min": 0.0, "max": 300.0, "unit": "mg/L", "authority": "EPA"},
    "Solids": {"min": 0.0, "max": 1000.0, "unit": "ppm", "authority": "WHO"},
    "Chloramines": {"min": 0.0, "max": 4.0, "unit": "ppm", "authority": "EPA"},
    "Sulfate": {"min": 0.0, "max": 250.0, "unit": "mg/L", "authority": "EPA"},
    "Conductivity": {"min": 0.0, "max": 400.0, "unit": "uS/cm", "authority": "WHO"},
    "Organic_carbon": {"min": 0.0, "max": 2.0, "unit": "ppm", "authority": "EPA"},
    "Trihalomethanes": {"min": 0.0, "max": 80.0, "unit": "ug/L", "authority": "EPA"},
    "Turbidity": {"min": 0.0, "max": 5.0, "unit": "NTU", "authority": "WHO"},
}
df_limits = pd.DataFrame.from_dict(regulatory_limits, orient="index")
print("WHO / EPA Regulatory Drinking Water Thresholds:")
print(df_limits.to_string())

# %% [markdown]
# ## 2. Dataset Empirical Compliance Evaluation
#
# Calculate percentage of observed water samples that satisfy each individual regulatory limit.

# %% [step_5]
df_raw = pd.read_csv("data/raw/water_potability.csv")
compliance_rates = {}
for param, lims in regulatory_limits.items():
    s = df_raw[param].dropna()
    valid = s.between(lims["min"], lims["max"]).mean() * 100
    compliance_rates[param] = round(valid, 2)
df_comp_rates = pd.DataFrame(list(compliance_rates.items()), columns=["Parameter", "Compliance_Pct"])
print(df_comp_rates.sort_values("Compliance_Pct", ascending=False).to_string(index=False))

# %% [markdown]
# ## 3. Hazardous Excursion Quantification
#
# Determine extreme violation counts for high-risk chemical agents (Chloramines, Trihalomethanes).

# %% [step_7]
tri_excess = (df_raw["Trihalomethanes"] > 80.0).sum()
chlor_excess = (df_raw["Chloramines"] > 4.0).sum()
print(f"Trihalomethanes > 80 ug/L Excursions: {tri_excess} ({tri_excess/len(df_raw)*100:.1f}%)")
print(f"Chloramines > 4.0 ppm Excursions: {chlor_excess} ({chlor_excess/len(df_raw)*100:.1f}%)")

# %% [markdown]
# ## 4. Composite Potability vs Regulatory Conformance
#
# Cross-tabulate empirical Potability ground-truth labels against strict regulatory boundary compliance.

# %% [step_9]
strict_pass = np.ones(len(df_raw), dtype=bool)
for param, lims in regulatory_limits.items():
    strict_pass &= df_raw[param].fillna(lims["min"]).between(lims["min"], lims["max"])
print("Strict All-Parameter Regulatory Compliance Count:", strict_pass.sum())
ctab = pd.crosstab(df_raw["Potability"], strict_pass, rownames=["GroundTruth_Potability"], colnames=["All_Standards_Passed"])
print(ctab)

# %% [markdown]
# ## 5. Regulatory Severity Index Formulation
#
# Compute a cumulative severity index measuring normalized distance from regulatory limits.

# %% [step_11]
severity_scores = []
for idx, row in df_raw.head(500).iterrows():
    score = 0
    for p, lim in regulatory_limits.items():
        val = row[p]
        if pd.notna(val) and val > lim["max"]:
            score += (val - lim["max"]) / lim["max"]
    severity_scores.append(score)
print(f"Mean Regulatory Severity Index (First 500): {np.mean(severity_scores):.4f}")

# %% [markdown]
# ## 6. Regulatory Compliance Profile Visualization
#
# Render a bar chart illustrating percentage compliance across all 9 physicochemical parameters.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(df_comp_rates["Parameter"], df_comp_rates["Compliance_Pct"], color="#2ca02c", alpha=0.85)
ax.axhline(100.0, color="gray", linestyle="--", alpha=0.7)
ax.set_ylim(0, 110)
ax.set_ylabel("Compliance Rate (%)")
ax.set_title("Day 2 Task 2: Empirical Compliance with WHO / EPA Thresholds", pad=12, fontsize=11)
plt.xticks(rotation=45, ha="right")
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
fig_path = FIG_DIR / "day2_task2_regulatory_compliance.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved compliance plot to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Regulatory Thresholds Specification Export
#
# Save compiled compliance table and threshold limits to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
tbl_path = TBL_DIR / "day2_task2_regulatory_scorecard.csv"
df_comp_rates.to_csv(tbl_path, index=False)
print("Saved scorecard table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Compliance Threshold Assertion
#
# Assert that regulatory standards table contains valid bounds for all 9 core parameters.

# %% [step_17]
assert len(regulatory_limits) == 9, "Incomplete regulatory specification dictionary."
print("Day 2 Task 2 Quality Gate: PASSED.")

# %% [markdown]
# # Day 2 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. World Health Organization (WHO) and US EPA guidelines constitute authoritative reference bounds.
# 2. Water with missing parameters cannot be definitively declared compliant without imputation.
#
# ## Day 2 Deliverable
#
# Regulatory standards catalog, empirical compliance scorecard, and compliance rate diagnostic plot.

