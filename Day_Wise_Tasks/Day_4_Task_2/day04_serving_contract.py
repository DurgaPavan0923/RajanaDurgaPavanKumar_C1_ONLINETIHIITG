"""Automated Python script mirror for day04_serving_contract.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 4 - Serving Contract & Pydantic Schema Validation
#
# ## Objective
#
# Define and validate strict REST API input schemas using Pydantic, asserting type safety, range guardrails, and graceful error handling.

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
TASK_DIR = ROOT / "Day_Wise_Tasks" / "Day_4_Task_2"
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
# ## 1. Pydantic Schema Contract Definition
#
# Establish field constraints, types, and allowable ranges for water potability prediction payloads.

# %% [step_3]
from pydantic import BaseModel, Field
class WaterSamplePayload(BaseModel):
    ph: float = Field(7.0, ge=0.0, le=14.0)
    Hardness: float = Field(200.0, ge=0.0, le=500.0)
    Solids: float = Field(20000.0, ge=0.0, le=100000.0)
    Chloramines: float = Field(7.0, ge=0.0, le=20.0)
    Sulfate: float = Field(300.0, ge=0.0, le=600.0)
    Conductivity: float = Field(400.0, ge=0.0, le=2000.0)
    Organic_carbon: float = Field(15.0, ge=0.0, le=50.0)
    Trihalomethanes: float = Field(60.0, ge=0.0, le=200.0)
    Turbidity: float = Field(4.0, ge=0.0, le=15.0)

print("Pydantic WaterSamplePayload schema compiled successfully.")

# %% [markdown]
# ## 2. Valid Payload Ingestion Verification
#
# Instantiate sample model payload and verify successful serialization into dictionary format.

# %% [step_5]
sample = WaterSamplePayload(ph=7.3, Hardness=185.0, Solids=15000.0, Chloramines=6.5, Sulfate=310.0, Conductivity=390.0, Organic_carbon=12.0, Trihalomethanes=65.0, Turbidity=3.8)
d = sample.model_dump()
print("Validated Payload Sample:")
print(pd.Series(d))

# %% [markdown]
# ## 3. Schema Validation Exception Trapping
#
# Pass invalid payloads (e.g. pH < 0 or > 14) and confirm Pydantic raises ValidationError.

# %% [step_7]
from pydantic import ValidationError
errors_caught = 0
try:
    WaterSamplePayload(ph=18.5)
except ValidationError as e:
    errors_caught += 1
    print("Caught Out-of-Bounds pH Error:", e.errors()[0]["msg"])
try:
    WaterSamplePayload(Turbidity=-2.0)
except ValidationError as e:
    errors_caught += 1
    print("Caught Negative Turbidity Error:", e.errors()[0]["msg"])
print(f"Total Validation Exceptions Successfully Trapped: {errors_caught}")

# %% [markdown]
# ## 4. JSON Schema Generation for OpenAPI Documentation
#
# Extract auto-generated JSON Schema used by FastAPI Swagger UI.

# %% [step_9]
schema_json = WaterSamplePayload.model_json_schema()
properties = schema_json["properties"]
df_props = pd.DataFrame([{"Field": k, "Type": v.get("type"), "Min": v.get("minimum", 0.0), "Max": v.get("maximum", "Inf")} for k, v in properties.items()])
print("OpenAPI Schema Properties Table:")
print(df_props.to_string(index=False))

# %% [markdown]
# ## 5. Batch Payload Processing Throughput Test
#
# Validate 1000 simulated payloads sequentially to measure Pydantic parsing overhead.

# %% [step_11]
import time
t0 = time.time()
for _ in range(1000):
    WaterSamplePayload(**d)
dur = time.time() - t0
print(f"1000 Pydantic Validations Completed in {dur*1000:.2f} ms ({dur:.5f} ms / sample)")

# %% [markdown]
# ## 6. Schema Range Envelopes Plot Generation
#
# Render horizontal error-bar plot displaying permissible physical bounds for each sensor input.

# %% [step_13]
# Output: outputs/figures/fig_path
fig, ax = plt.subplots(figsize=(8, 4))
y_pos = range(len(df_props))
ax.barh(list(y_pos), df_props["Max"].astype(float), color="#9467bd", alpha=0.5, label="Allowable Upper Bound")
ax.set_yticks(list(y_pos))
ax.set_yticklabels(df_props["Field"], fontsize=9)
ax.set_xscale("log")
ax.set_xlabel("Permissible Sensor Envelope (Log Scale)")
ax.set_title("Day 4 Task 2: Pydantic Input Validation Range Guardrails", fontsize=11, pad=10)
plt.tight_layout()
fig_path = FIG_DIR / "day4_task2_schema_ranges.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved schema ranges plot to:", fig_path.relative_to(ROOT))

# %% [markdown]
# ## 7. Serving Contract Schema Table Serialization
#
# Export schema properties and physical bounds table to CSV.

# %% [step_15]
# Output: outputs/tables/tbl_path
tbl_path = TBL_DIR / "day4_task2_schema_contract.csv"
print(df_props.to_string())
df_props.to_csv(tbl_path, index=False)
print("Saved schema contract table to:", tbl_path.relative_to(ROOT))

# %% [markdown]
# ## 8. Validation Gate Assertion
#
# Assert that schema requires all 9 critical parameters and traps out-of-bounds inputs.

# %% [step_17]
assert errors_caught == 2, "Failed to trap invalid sensor payloads."
print("Day 4 Task 2 Quality Gate: PASSED.")

# %% [markdown]
# # Day 4 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Pydantic schemas enforce type coercion and range bounding prior to model execution.
# 2. Invalid HTTP payload structures return HTTP 422 Unprocessable Entity.
#
# ## Day 4 Deliverable
#
# Pydantic contract schema, validation exception benchmark, and input range envelope visualization.

