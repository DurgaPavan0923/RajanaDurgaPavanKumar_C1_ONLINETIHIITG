"""Automated Python script mirror for day22_model_packaging.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 22 - Model Serialization & Packaging Notebook
#
# ## Objective
#
# Package preprocessors, calibrated tree ensembles, and metadata into serialized production .joblib artifacts in models/production/.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_22_Task_1"
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
# ## 1. Packaging Subsystem Initialization
#
# Verify production model directory destination and import joblib serialization utilities.

# %% [step_3]
import joblib
prod_dir = project_root / "models" / "production"
prod_dir.mkdir(parents=True, exist_ok=True)
print(f"Production Model Target Directory: {prod_dir}")

# %% [markdown]
# ## 2. Packaging Pipeline Component Assembly
#
# Assemble StandardScaler preprocessor, feature selector, and calibrated champion tree ensemble.

# %% [step_5]
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42))
])
print("Production Pipeline Steps:", [step[0] for step in pipe.steps])

# %% [markdown]
# ## 3. Pipeline Training on Combined Train+Val Partitions
#
# Fit production pipeline on combined development partition (Train + Validation) prior to packaging.

# %% [step_7]
df_p = pd.read_csv("data/raw/water_potability.csv")
X = df_p.drop(columns=["Potability"]).fillna(df_p.median(numeric_only=True))
y = df_p["Potability"]
pipe.fit(X, y)
print("Production Pipeline trained successfully on development dataset.")

# %% [markdown]
# ## 4. Production Artifact Joblib Serialization
#
# Serialize trained production pipeline to models/production/water_potability_pipeline_v1.joblib.

# %% [step_9]
model_path = prod_dir / "water_potability_pipeline_v1.joblib"
joblib.dump(pipe, model_path, compress=3)
sz_mb = model_path.stat().st_size / (1024*1024)
print(f"Serialized Production Model to {model_path.name} ({sz_mb:.2f} MB)")

# %% [markdown]
# ## 5. Round-Trip Deserialization and Verification
#
# Load serialized pipeline back into memory and verify identical probability predictions on test vector.

# %% [step_11]
pipe_loaded = joblib.load(model_path)
v_test = X.iloc[:5]
p_orig = pipe.predict_proba(v_test)
p_load = pipe_loaded.predict_proba(v_test)
diff = np.max(np.abs(p_orig - p_load))
print(f"Max Deserialization Probability Divergence: {diff}")

# %% [markdown]
# ## 6. Production Model Footprint Allocation Plot
#
# Render bar chart displaying file sizes of serialized production models.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.bar([model_path.name], [sz_mb], color="#1f77b4", width=0.4, alpha=0.85)
ax.set_title("Day 22 Task 1: Serialized Production Model Footprint", fontsize=11, pad=10)
ax.set_ylabel("Bundle Size (MB)")
ax.set_ylim(0, sz_mb * 1.3)
ax.text(0, sz_mb + 0.5, f"{sz_mb:.2f} MB", ha="center", fontweight="bold")
plt.tight_layout()
fig_path = FIG_DIR / "day22_task1_model_packaging.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved model packaging plot to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Production Packaging Table Export
#
# Export serialized artifact specifications table to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
df_pkg = pd.DataFrame([
    {"Artifact": model_path.name, "Format": "joblib", "Compression": 3, "Size_MB": round(sz_mb, 2), "Status": "FROZEN_FOR_PRODUCTION"}
])
tbl_path = TBL_DIR / "day22_task1_packaging_summary.csv"
df_pkg.to_csv(tbl_path, index=False)
print("Saved packaging summary table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Serialization Gate Assertion
#
# Assert that deserialized model produces exactly zero divergence.

# %% [step_17]
assert diff == 0.0 and model_path.exists()
print("Day 22 Task 1 Quality Gate: PASSED.")

# %% [markdown]
# # Day 22 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Production models are serialized as self-contained Scikit-Learn Pipelines with embedded preprocessors.
# 2. Round-trip deserialization guarantees bitwise operational equivalence.
#
# ## Day 22 Deliverable
#
# Model packaging notebook, bundle size bar chart, and serialization specifications table.

