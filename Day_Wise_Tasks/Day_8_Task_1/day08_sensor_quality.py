"""Automated Python script mirror for day08_sensor_quality.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 8 - Sensor Operating Envelopes & Range Auditing
#
# ## Objective
#
# Audit physical sensor operating ranges across multi-channel telemetry, detecting out-of-bound spikes, sensor clipping, and impossible values.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_8_Task_1"
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
# ## 1. Telemetry Physical Envelopes Specification
#
# Define authoritative physical sensor operating ranges for underwater telemetry channels.

# %% [step_3]
sensor_envelopes = {
    "temperature": {"min": -2.0, "max": 40.0, "unit": "degC"},
    "dissolved_oxygen": {"min": 0.0, "max": 15.0, "unit": "mg/L"},
    "ph": {"min": 0.0, "max": 14.0, "unit": "pH"},
    "conductivity": {"min": 0.0, "max": 2000.0, "unit": "uS/cm"},
    "turbidity": {"min": 0.0, "max": 100.0, "unit": "NTU"},
    "pressure": {"min": 0.0, "max": 1000.0, "unit": "dbar"}
}
df_env = pd.DataFrame.from_dict(sensor_envelopes, orient="index")
print("Physical Sensor Operating Envelopes:")
print(df_env.to_string())

# %% [markdown]
# ## 2. Continuous Telemetry Range Ingestion
#
# Load raw underwater telemetry stream and extract descriptive range extrema.

# %% [step_5]
df_stream = pd.read_csv("data/raw/underwater_sensor_stream.csv")
stream_stats = df_stream.describe().T[["min", "mean", "max"]]
print("Empirical Telemetry Extrema:")
print(stream_stats.round(3))

# %% [markdown]
# ## 3. Out-of-Bounds Sensor Excursion Detection
#
# Identify records where observed readings breach physical operating limits.

# %% [step_7]
excursions = {}
for col, bounds in sensor_envelopes.items():
    if col in df_stream.columns:
        s = df_stream[col]
        invalid = ((s < bounds["min"]) | (s > bounds["max"])).sum()
        excursions[col] = invalid
df_exc = pd.DataFrame(list(excursions.items()), columns=["Sensor", "Excursion_Count"])
print("Physical Excursions Count:")
print(df_exc.to_string(index=False))

# %% [markdown]
# ## 4. Rate-of-Change Spike Identification
#
# Compute first-order temporal differences to flag unphysical sensor jump anomalies.

# %% [step_9]
jump_thresholds = {"dissolved_oxygen": 2.0, "temperature": 3.0, "ph": 1.0}
jumps = {}
for col, thresh in jump_thresholds.items():
    diffs = df_stream[col].diff().abs()
    jumps[col] = (diffs > thresh).sum()
print("Rate-of-Change Spike Violations:", jumps)

# %% [markdown]
# ## 5. Sensor Channel Reliability Scoring
#
# Compute composite reliability index across sensor channels based on valid measurement percentages.

# %% [step_11]
reliability = []
for col in sensor_envelopes:
    if col in df_stream.columns:
        valid_pct = (1.0 - (excursions[col] / len(df_stream))) * 100
        reliability.append({"Sensor": col, "Reliability_Score": round(valid_pct, 2)})
df_rel = pd.DataFrame(reliability)
print(df_rel.to_string(index=False))

# %% [markdown]
# ## 6. Sensor Range Envelope Diagnostic Plot
#
# Render multi-panel boxplots illustrating empirical telemetry ranges relative to operating limits.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(8, 4))
df_stream[["temperature", "dissolved_oxygen", "ph", "turbidity"]].boxplot(ax=ax)
ax.set_title("Day 8 Task 1: Continuous Telemetry Operating Range Distributions", fontsize=11, pad=10)
ax.set_ylabel("Measured Sensor Value")
plt.tight_layout()
fig_path = FIG_DIR / "day8_task1_sensor_distributions.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved sensor distributions plot to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Sensor Range Quality Table Export
#
# Export sensor envelopes and empirical range statistics table to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
tbl_path = TBL_DIR / "day8_task1_sensor_quality_table.csv"
print(df_rel.to_string())
df_rel.to_csv(tbl_path, index=False)
print("Saved sensor quality table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Physical Range Verification Assertion
#
# Assert that total out-of-bounds physical excursions remain strictly below 1% of stream.

# %% [step_17]
assert sum(excursions.values()) < 0.01 * len(df_stream)
print("Day 8 Task 1 Quality Gate: PASSED.")

# %% [markdown]
# # Day 8 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Sensors operate within marine CTD physical limits.
# 2. Transient spikes exceeding physical acceleration limits are sensor artifacts.
#
# ## Day 8 Deliverable
#
# Sensor range validation report, operating distribution boxplot, and quality scorecard table.

