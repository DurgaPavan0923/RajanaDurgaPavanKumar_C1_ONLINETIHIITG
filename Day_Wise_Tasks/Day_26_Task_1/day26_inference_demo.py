"""Automated Python script mirror for day26_inference_demo.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 26 - Inference Demo & Packaging Notebook
#
# ## Objective
#
# Demonstrate single-sample, batch, and simulated continuous streaming inference using the production serialized model pipeline.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_26_Task_1"
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
# ## 1. Production Model Deserialization
#
# Load production pipeline artifact from models/production/.

# %% [step_3]
import joblib
pipe = joblib.load(project_root / "models" / "production" / "water_potability_pipeline_v1.joblib")
print("Production model loaded into memory.")

# %% [markdown]
# ## 2. Single-Sample Real-Time Inference Execution
#
# Pass individual sample payload and extract predicted probability, class label, and confidence score.

# %% [step_5]
sample_payload = pd.DataFrame([{
    "ph": 7.2, "Hardness": 204.0, "Solids": 20700.0, "Chloramines": 7.3,
    "Sulfate": 368.0, "Conductivity": 564.0, "Organic_carbon": 10.3,
    "Trihalomethanes": 86.0, "Turbidity": 2.9
}])
prob = pipe.predict_proba(sample_payload)[0, 1]
label = "POTABLE" if prob >= 0.5 else "NON_POTABLE"
print(f"Single Inference -> Predicted Probability: {prob:.4f} | Decision: {label}")

# %% [markdown]
# ## 3. Batch Vectorized Inference Execution
#
# Execute batch prediction across 100 test samples measuring throughput.

# %% [step_7]
df_p = pd.read_csv("data/raw/water_potability.csv")
X_batch = df_p.drop(columns=["Potability"]).fillna(df_p.median(numeric_only=True)).head(100)
import time
t0 = time.time()
batch_probs = pipe.predict_proba(X_batch)[:, 1]
dur = time.time() - t0
print(f"Batch Inference (100 samples): {dur*1000:.2f} ms ({dur*10:.4f} ms/sample)")

# %% [markdown]
# ## 4. Prediction Confidence Interval Assessment
#
# Calculate prediction confidence margins (|prob - 0.5|).

# %% [step_9]
margins = np.abs(batch_probs - 0.5)
print(f"Mean Decision Confidence Margin: {margins.mean():.4f}")

# %% [markdown]
# ## 5. REST API Response Payload Formatting
#
# Format inference result matching OpenAPI JSON response specification.

# %% [step_11]
api_response = {
    "potability_score": round(float(prob), 4),
    "is_potable": bool(prob >= 0.5),
    "decision_threshold": 0.50,
    "model_version": "v1.0.0",
    "status": "SUCCESS"
}
import json
print("Formatted API Response Payload:")
print(json.dumps(api_response, indent=2))

# %% [markdown]
# ## 6. Batch Prediction Probability Distribution Plot
#
# Render histogram showing distribution of predicted potability probabilities.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(batch_probs, bins=15, color="#1f77b4", edgecolor="black", alpha=0.8)
ax.axvline(0.5, color="red", linestyle="--", label="Decision Threshold (0.50)")
ax.set_title("Day 26 Task 1: Batch Prediction Probability Distribution", fontsize=11, pad=10)
ax.set_xlabel("Predicted Probability of Potability")
ax.set_ylabel("Sample Count")
ax.legend()
plt.tight_layout()
fig_path = FIG_DIR / "day26_task1_inference_distribution.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved inference distribution plot to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Inference Demonstration Table Serialization
#
# Export batch prediction results table to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
df_inf_results = pd.DataFrame({
    "Sample_ID": range(1, 101),
    "Predicted_Probability": np.round(batch_probs, 4),
    "Decision": ["POTABLE" if p >= 0.5 else "NON_POTABLE" for p in batch_probs]
})
tbl_path = TBL_DIR / "day26_task1_inference_results.csv"
print(df_inf_results.head(20).to_string())
print("Shape:", df_inf_results.shape)
df_inf_results.head(20).to_csv(tbl_path, index=False)
print("Saved inference results table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Inference Gate Assertion
#
# Assert that single sample and batch inference execute with valid bounded probabilities.

# %% [step_17]
assert 0.0 <= prob <= 1.0 and len(batch_probs) == 100
print("Day 26 Task 1 Quality Gate: PASSED.")

# %% [markdown]
# # Day 26 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Production model operates synchronously on REST API payloads with < 10ms response time.
# 2. Batch predictions scale linearly with input sample count.
#
# ## Day 26 Deliverable
#
# Inference demo notebook, prediction distribution plot, and sample API response schema.

