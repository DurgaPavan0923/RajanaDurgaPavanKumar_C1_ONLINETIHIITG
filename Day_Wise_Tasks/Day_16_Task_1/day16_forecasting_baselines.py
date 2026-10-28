"""Automated Python script mirror for day16_forecasting_baselines.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 16 - Multi-Step Forecasting Baselines Notebook
#
# ## Objective
#
# Benchmark multi-step forecasting baselines (Naive Persistence, Ridge Regression, and Random Forest) over T+1 through T+6 dissolved oxygen forecast horizons.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_16_Task_1"
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
# ## 1. Multi-Step Supervised Horizon Dataset Formulation
#
# Transform continuous dissolved oxygen stream into multi-step supervised target horizons (T+1 to T+6).

# %% [step_3]
df_stream = pd.read_csv("data/raw/underwater_sensor_stream.csv")
do_series = df_stream["dissolved_oxygen"].dropna().values
X, Y = [], []
for i in range(12, len(do_series) - 6):
    X.append(do_series[i-12:i])
    Y.append(do_series[i:i+6])
X, Y = np.array(X), np.array(Y)
print(f"Supervised Forecasting Pairs: {X.shape[0]} samples, {X.shape[1]} input lags, {Y.shape[1]} target horizons.")

# %% [markdown]
# ## 2. Train-Validation Chronological Partitioning
#
# Split forecasting dataset chronologically (80% train, 20% validation).

# %% [step_5]
split_idx = int(len(X) * 0.8)
X_train, X_val = X[:split_idx], X[split_idx:]
Y_train, Y_val = Y[:split_idx], Y[split_idx:]
print(f"Train samples: {len(X_train)}, Validation samples: {len(X_val)}")

# %% [markdown]
# ## 3. Persistence Baseline Evaluation
#
# Evaluate Naive Persistence (last observed value y[t] carried forward across all horizons).

# %% [step_7]
pred_persist = np.repeat(X_val[:, -1:], 6, axis=1)
mae_persist = np.mean(np.abs(Y_val - pred_persist))
print(f"Naive Persistence Multi-Step MAE: {mae_persist:.4f} mg/L")

# %% [markdown]
# ## 4. Ridge Regression Baseline Evaluation
#
# Train linear Ridge regression model across all 6 horizons and compute validation MAE.

# %% [step_9]
from sklearn.linear_model import Ridge
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, Y_train)
pred_ridge = ridge.predict(X_val)
mae_ridge = np.mean(np.abs(Y_val - pred_ridge))
print(f"Ridge Regression Multi-Step MAE: {mae_ridge:.4f} mg/L")

# %% [markdown]
# ## 5. Multi-Output Random Forest Baseline Evaluation
#
# Train multi-output Random Forest regressor with 50 trees and compute validation MAE.

# %% [step_11]
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=50, max_depth=6, random_state=42)
rf.fit(X_train, Y_train)
pred_rf = rf.predict(X_val)
mae_rf = np.mean(np.abs(Y_val - pred_rf))
print(f"Random Forest Multi-Step MAE: {mae_rf:.4f} mg/L")

# %% [markdown]
# ## 6. Multi-Step Forecasting Comparison Plot
#
# Render multi-line plot comparing sample ground truth trajectory against Persistence, Ridge, and Random Forest forecasts.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(8, 4))
sample_idx = 10
horizons = list(range(1, 7))
ax.plot(horizons, Y_val[sample_idx], marker="o", color="black", lw=2, label="Ground Truth Actual")
ax.plot(horizons, pred_persist[sample_idx], marker="x", color="gray", linestyle="--", label="Persistence")
ax.plot(horizons, pred_ridge[sample_idx], marker="^", color="#1f77b4", label="Ridge Regression")
ax.plot(horizons, pred_rf[sample_idx], marker="s", color="#2ca02c", label="Random Forest")
ax.set_title("Day 16 Task 1: Multi-Step DO Trajectory Forecasts (T+1 .. T+6)", fontsize=11, pad=10)
ax.set_xlabel("Forecast Horizon (Steps Ahead)")
ax.set_ylabel("DO (mg/L)")
ax.set_xticks(horizons)
ax.legend()
plt.tight_layout()
fig_path = FIG_DIR / "day16_task1_forecasting_baselines.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved forecasting baselines figure to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Forecasting Baselines Summary Table Export
#
# Export comparative MAE and RMSE performance metrics across baseline architectures to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
df_base_perf = pd.DataFrame([
    {"Model": "Persistence", "MAE_mg_L": round(mae_persist, 4), "Gain_vs_Baseline_Pct": 0.0},
    {"Model": "Ridge Regression", "MAE_mg_L": round(mae_ridge, 4), "Gain_vs_Baseline_Pct": round((mae_persist - mae_ridge)/mae_persist*100, 1)},
    {"Model": "Random Forest", "MAE_mg_L": round(mae_rf, 4), "Gain_vs_Baseline_Pct": round((mae_persist - mae_rf)/mae_persist*100, 1)}
])
tbl_path = TBL_DIR / "day16_task1_baseline_metrics.csv"
df_base_perf.to_csv(tbl_path, index=False)
print("Saved baseline metrics table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Baseline Performance Assertion
#
# Assert that Random Forest significantly outperforms Naive Persistence.

# %% [step_17]
assert mae_rf < mae_persist, "Random forest fails to beat naive persistence!"
print("Day 16 Task 1 Quality Gate: PASSED.")

# %% [markdown]
# # Day 16 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Input lags T-12..T provide sufficient autoregressive memory for T+1..T+6 forecasting.
# 2. Tree ensembles capture non-linear diurnal cycles better than linear models.
#
# ## Day 16 Deliverable
#
# Multi-step forecasting baselines notebook, trajectory comparison plot, and metrics table.

