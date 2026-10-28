"""Automated Python script mirror for day17_xgboost_forecaster.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 17 - Advanced XGBoost Forecaster Notebook
#
# ## Objective
#
# Implement an advanced multi-output gradient boosted decision tree (XGBoost) forecaster optimizing multi-horizon dissolved oxygen prediction.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_17_Task_1"
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
# ## 1. Supervised Data Ingestion for XGBoost
#
# Ingest supervised lag-target pairs for multi-output gradient boosting.

# %% [step_3]
import xgboost as xgb
print(f"XGBoost Version: {xgb.__version__}")
df_stream = pd.read_csv("data/raw/underwater_sensor_stream.csv")
do_series = df_stream["dissolved_oxygen"].dropna().values
X, Y = [], []
for i in range(12, len(do_series) - 6):
    X.append(do_series[i-12:i])
    Y.append(do_series[i:i+6])
X, Y = np.array(X), np.array(Y)
split_idx = int(len(X) * 0.8)
X_train, X_val = X[:split_idx], X[split_idx:]
Y_train, Y_val = Y[:split_idx], Y[split_idx:]
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=50, max_depth=6, random_state=42)
rf.fit(X_train, Y_train)
pred_rf = rf.predict(X_val)
mae_rf = float(np.mean(np.abs(Y_val - pred_rf)))
horizon_maes = [float(np.mean(np.abs(Y_val[:, h] - pred_rf[:, h]))) for h in range(6)]
from sklearn.multioutput import MultiOutputRegressor
xgb_reg = MultiOutputRegressor(xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42))
print("Multi-Output XGBoost Forecaster Architecture Initialized.")

# %% [markdown]
# ## 2. Model Training Execution
#
# Train multi-output XGBoost model on chronological training partition.

# %% [step_5]
xgb_reg.fit(X_train, Y_train)
print("XGBoost Forecaster training complete.")

# %% [markdown]
# ## 3. Validation Set Multi-Horizon Inference
#
# Generate predictions on held-out validation set and evaluate overall MAE.

# %% [step_7]
pred_xgb = xgb_reg.predict(X_val)
mae_xgb = np.mean(np.abs(Y_val - pred_xgb))
rmse_xgb = np.sqrt(np.mean((Y_val - pred_xgb)**2))
print(f"XGBoost Multi-Step Validation MAE:  {mae_xgb:.4f} mg/L")
print(f"XGBoost Multi-Step Validation RMSE: {rmse_xgb:.4f} mg/L")

# %% [markdown]
# ## 4. Per-Horizon Performance Breakdown
#
# Compute individual step MAE across horizons T+1 to T+6 for XGBoost.

# %% [step_9]
xgb_h_maes = [np.mean(np.abs(Y_val[:, h] - pred_xgb[:, h])) for h in range(6)]
for h, m in enumerate(xgb_h_maes, 1):
    print(f"XGBoost T+{h} MAE: {m:.4f} mg/L")

# %% [markdown]
# ## 5. Comparison with Random Forest Baseline
#
# Compute relative error reduction between Random Forest and XGBoost.

# %% [step_11]
delta_mae = mae_rf - mae_xgb
print(f"MAE Delta (RF vs XGBoost): {delta_mae:.4f} mg/L")

# %% [markdown]
# ## 6. XGBoost Actual vs Predicted Trajectory Plot
#
# Render trajectory plot comparing actual dissolved oxygen against XGBoost multi-step forecasts.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(8, 4))
sample_idx = 15
ax.plot(range(1, 7), Y_val[sample_idx], marker="o", color="black", lw=2, label="Actual Trajectory")
ax.plot(range(1, 7), pred_xgb[sample_idx], marker="s", color="#d62728", lw=2, label="XGBoost Predicted")
ax.set_title("Day 17 Task 1: XGBoost Multi-Step Forecast (Sample 15)", fontsize=11, pad=10)
ax.set_xlabel("Forecast Horizon (Steps Ahead)")
ax.set_ylabel("DO (mg/L)")
ax.set_xticks(range(1, 7))
ax.legend()
plt.tight_layout()
fig_path = FIG_DIR / "day17_task1_xgboost_forecast.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved XGBoost trajectory plot to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. XGBoost Evaluation Metrics Table Serialization
#
# Export comprehensive multi-horizon XGBoost performance table to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
df_xgb_metrics = pd.DataFrame({
    "Horizon": [f"T+{h}" for h in range(1, 7)],
    "XGBoost_MAE": np.round(xgb_h_maes, 4),
    "Baseline_RF_MAE": np.round(horizon_maes, 4)
})
tbl_path = TBL_DIR / "day17_task1_xgboost_metrics.csv"
print(df_xgb_metrics.to_string())
df_xgb_metrics.to_csv(tbl_path, index=False)
print("Saved XGBoost metrics table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. XGBoost Forecaster Quality Gate
#
# Assert that XGBoost achieves validation MAE < 0.35 mg/L.

# %% [step_17]
assert mae_xgb < 0.35, "XGBoost validation error exceeds threshold."
print("Day 17 Task 1 Quality Gate: PASSED.")

# %% [markdown]
# # Day 17 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Gradient boosting decision trees effectively model non-linear sensor interactions.
# 2. MultiOutputRegressor provides independent optimal tree structures for each horizon.
#
# ## Day 17 Deliverable
#
# XGBoost forecaster notebook, trajectory forecast plot, and metrics evaluation table.

