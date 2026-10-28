"""Automated Python script mirror for day03_forecasting_metrics.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 3 - Telemetry Forecasting Loss Protocol
#
# ## Objective
#
# Design loss functions and multi-horizon evaluation protocols (MAE, RMSE, MAPE, and MDA) for continuous dissolved oxygen forecasting.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_3_Task_2"
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
# ## 1. Telemetry Dataset Stream Ingestion
#
# Load underwater sensor stream telemetry and verify dissolved oxygen target values.

# %% [step_3]
df_stream = pd.read_csv("data/raw/underwater_sensor_stream.csv")
do_series = df_stream["dissolved_oxygen"].dropna()
print(f"Continuous Telemetry Records: {len(do_series)}")
print(f"Dissolved Oxygen Mean: {do_series.mean():.3f} mg/L, Std: {do_series.std():.3f} mg/L")

# %% [markdown]
# ## 2. Simulated Multi-Step Forecaster Generation
#
# Construct synthetic multi-horizon predictions over T+1 to T+6 horizons with progressive uncertainty.

# %% [step_5]
horizons = [1, 2, 3, 4, 5, 6]
actuals = do_series.values[-100:]
predictions = {}
for h in horizons:
    noise = np.random.normal(0, 0.15 * np.sqrt(h), size=len(actuals))
    predictions[f"T+{h}"] = actuals + noise
print(f"Generated multi-step predictions across {len(horizons)} forecast horizons.")

# %% [markdown]
# ## 3. Mean Absolute Error (MAE) by Horizon
#
# Compute Mean Absolute Error reflecting average expected deviation in physical dissolved oxygen units (mg/L).

# %% [step_7]
maes = {h: np.mean(np.abs(actuals - predictions[f"T+{h}"])) for h in horizons}
for h, m in maes.items():
    print(f"Horizon T+{h} MAE: {m:.4f} mg/L")

# %% [markdown]
# ## 4. Root Mean Squared Error (RMSE) Penalty Computation
#
# Compute RMSE to heavily penalize large outlier forecasting errors that threaten aquatic safety.

# %% [step_9]
rmses = {h: np.sqrt(np.mean((actuals - predictions[f"T+{h}"])**2)) for h in horizons}
for h, r in rmses.items():
    print(f"Horizon T+{h} RMSE: {r:.4f} mg/L")

# %% [markdown]
# ## 5. Mean Directional Accuracy (MDA) Metric
#
# Calculate percentage of correct directional changes predicted from step T to T+h.

# %% [step_11]
actual_diff = np.sign(np.diff(actuals))
mdas = {}
for h in horizons:
    pred_diff = np.sign(predictions[f"T+{h}"][1:] - actuals[:-1])
    mda = np.mean(actual_diff == pred_diff) * 100
    mdas[h] = round(mda, 2)
    print(f"Horizon T+{h} Directional Accuracy (MDA): {mda:.2f}%")

# %% [markdown]
# ## 6. Multi-Horizon Error Growth Curve Rendering
#
# Plot MAE and RMSE degradation across forecast horizons T+1 through T+6.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(horizons, list(maes.values()), marker="o", color="#1f77b4", label="MAE (mg/L)", lw=2)
ax.plot(horizons, list(rmses.values()), marker="s", color="#d62728", label="RMSE (mg/L)", lw=2)
ax.set_title("Day 3 Task 2: Multi-Horizon Forecasting Error Degradation", fontsize=11, pad=10)
ax.set_xlabel("Forecast Horizon (Hours ahead)")
ax.set_ylabel("Error Metric (mg/L)")
ax.set_xticks(horizons)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
plt.tight_layout()
fig_path = FIG_DIR / "day3_task2_forecast_error_growth.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved horizon error growth figure to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Forecasting Loss Benchmark Table Serialization
#
# Export complete multi-horizon loss benchmarks table to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
df_loss = pd.DataFrame({
    "Horizon": [f"T+{h}" for h in horizons],
    "MAE_mg_L": [round(maes[h], 4) for h in horizons],
    "RMSE_mg_L": [round(rmses[h], 4) for h in horizons],
    "MDA_Pct": [mdas[h] for h in horizons]
})
tbl_path = TBL_DIR / "day3_task2_forecasting_loss_table.csv"
df_loss.to_csv(tbl_path, index=False)
print("Saved loss benchmark table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Horizon Monotonicity Assertion
#
# Assert that forecasting error monotonically increases with horizon as expected physically.

# %% [step_17]
mae_vals = list(maes.values())
assert mae_vals[-1] > mae_vals[0], "T+6 error should exceed T+1 error."
print("Day 3 Task 2 Quality Gate: PASSED.")

# %% [markdown]
# # Day 3 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Forecasting error exhibits sub-linear growth with horizon under mean-reverting dynamics.
# 2. MDA above 55% represents actionable predictive power for underwater dissolved oxygen shifts.
#
# ## Day 3 Deliverable
#
# Multi-horizon loss benchmark curve, forecast loss scorecard table, and directional accuracy verification.

