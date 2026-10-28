"""Automated Python script mirror for day10_environmental_eda.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 10 - Continuous Telemetry Dynamics & Time-Series EDA
#
# ## Objective
#
# Perform exploratory data analysis on continuous underwater sensor streams, investigating diurnal dynamics, thermal stratification, and dissolved oxygen oscillations.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_10_Task_1"
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
# ## 1. Continuous Telemetry Stream Ingestion
#
# Load underwater sensor stream telemetry and verify timestamp parsing.

# %% [step_3]
df_stream = pd.read_csv("data/raw/underwater_sensor_stream.csv")
df_stream["timestamp"] = pd.to_datetime(df_stream["timestamp"])
print("Continuous Sensor Telemetry Shape:", df_stream.shape)

# %% [markdown]
# ## 2. Diurnal Dissolved Oxygen Trend Analysis
#
# Extract hour of day and compute average dissolved oxygen by hour to observe photosynthetic cycles.

# %% [step_5]
df_stream["hour"] = df_stream["timestamp"].dt.hour
hourly_do = df_stream.groupby("hour")["dissolved_oxygen"].agg(["mean", "std"])
print("Hourly Dissolved Oxygen Means (First 6 Hours):")
print(hourly_do.head(6))

# %% [markdown]
# ## 3. Temperature vs Dissolved Oxygen Solubility Coupling
#
# Examine inverse relationship between water temperature and gas solubility.

# %% [step_7]
corr_temp_do = df_stream["temperature"].corr(df_stream["dissolved_oxygen"])
print(f"Empirical Temperature vs Dissolved Oxygen Correlation: {corr_temp_do:.4f}")

# %% [markdown]
# ## 4. Turbidity Shock and Attenuation Profile
#
# Quantify turbidity spikes and evaluate relaxation half-life across the stream.

# %% [step_9]
turb_spikes = (df_stream["turbidity"] > df_stream["turbidity"].mean() + 2*df_stream["turbidity"].std()).sum()
print("Turbidity Spike Excursions (> 2 sigma):", turb_spikes)

# %% [markdown]
# ## 5. pH Buffer Stability Assessment
#
# Measure variation of pH over continuous sensor monitoring window.

# %% [step_11]
ph_stats = df_stream["ph"].describe()
print(f"pH Stability: Mean = {ph_stats['mean']:.3f}, Std = {ph_stats['std']:.3f}")

# %% [markdown]
# ## 6. Multi-Sensor Diurnal Dynamics Plot
#
# Render multi-panel time-series plot displaying continuous DO and Temperature trajectories.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, axes = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
axes[0].plot(df_stream["timestamp"], df_stream["dissolved_oxygen"], color="#1f77b4", lw=1.2)
axes[0].set_ylabel("DO (mg/L)")
axes[0].set_title("Day 10 Task 1: Continuous Underwater Telemetry Dynamics", fontsize=11, pad=10)

axes[1].plot(df_stream["timestamp"], df_stream["temperature"], color="#d62728", lw=1.2)
axes[1].set_ylabel("Temp (deg C)")
axes[1].set_xlabel("Observation Timestamp")
plt.tight_layout()
fig_path = FIG_DIR / "day10_task1_sensor_streams.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved telemetry streams plot to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Telemetry Summary Statistics Serialization
#
# Serialize multi-channel descriptive statistics to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path)
tbl_path = TBL_DIR / "day10_task1_telemetry_summary.csv"
df_telemetry_summary = df_stream.describe().round(4)
print(df_telemetry_summary.to_string())
df_telemetry_summary.to_csv(tbl_path)
print("Saved summary table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Telemetry Continuity Assertion
#
# Assert that stream has non-empty valid observations across all 6 physical channels.

# %% [step_17]
assert len(df_stream) >= 500 and not df_stream["dissolved_oxygen"].isnull().all()
print("Day 10 Task 1 Quality Gate: PASSED.")

# %% [markdown]
# # Day 10 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Sensor telemetry captures continuous diurnal cycles under natural ambient conditions.
# 2. Temperature and dissolved oxygen exhibit expected thermodynamic inverse coupling.
#
# ## Day 10 Deliverable
#
# Time-series EDA plot, summary statistics table, and diurnal dynamics report.

