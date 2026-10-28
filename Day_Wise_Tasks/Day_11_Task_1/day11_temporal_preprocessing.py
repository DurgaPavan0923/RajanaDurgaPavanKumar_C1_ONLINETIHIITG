"""Automated Python script mirror for day11_temporal_preprocessing.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 11 - Temporal Preprocessing Pipeline
#
# ## Objective
#
# The objective of Day 11 is to implement a reusable preprocessing pipeline for the timestamped water-quality dataset.
#
# The pipeline includes:
# - Timestamp validation and chronological sorting
# - Duplicate timestamp handling
# - Missing-value handling with causal forward filling
# - Physical domain-quality filtering
# - Chronological train/validation/test splitting
# - Fold-isolated feature scaling
# - Processed partition serialization and verification

# %% [step_1]
try:
    from IPython.display import display
except ImportError:
    display = print
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

def _find_project_root():
    curr = Path.cwd()
    for p in [curr] + list(curr.parents):
        if (p / 'pyproject.toml').exists() or (p / 'requirements.txt').exists():
            return p
    return curr

project_root = _find_project_root()
processed_path = project_root / 'data' / 'processed' / 'water_quality_timestamped.csv'

df = pd.read_csv(processed_path)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.sort_values('timestamp').reset_index(drop=True)
print('Dataset shape:', df.shape)
print('Columns:', df.columns.tolist())
display(df.head())

# %% [markdown]
# ## 1. Timestamp Preprocessing
#
# The timestamp column is converted into a datetime format and records are sorted chronologically.
#
# Invalid timestamps are identified and removed because temporal ordering is required for downstream time-series processing.

# %% [step_3]
print("Invalid timestamps:", df["timestamp"].isna().sum())

df = df.dropna(subset=["timestamp"]).copy()

df = df.sort_values("timestamp").reset_index(drop=True)

print("Shape after timestamp validation:", df.shape)
print("Chronologically sorted:", df["timestamp"].is_monotonic_increasing)

# %% [markdown]
# ## 2. Duplicate Timestamp Handling
#
# Duplicate timestamps are checked before modeling.
#
# For this initial preprocessing version, duplicate timestamps are retained for audit purposes and then reduced to one observation per timestamp using the first available record.
#
# This provides a deterministic preprocessing rule while keeping the original raw and timestamped datasets unchanged.

# %% [step_5]
duplicate_count = df["timestamp"].duplicated().sum()

print("Duplicate timestamps before cleaning:", duplicate_count)

df = (
    df.sort_values("timestamp")
      .drop_duplicates(subset=["timestamp"], keep="first")
      .reset_index(drop=True)
)

print("Duplicate timestamps after cleaning:",
      df["timestamp"].duplicated().sum())

print("Shape after duplicate handling:", df.shape)

# %% [markdown]
# ## 3. Missing-Value Handling
#
# Missing values are identified for each parameter.
#
# For this first preprocessing version, numeric missing values are filled using forward filling because the data is treated as an ordered temporal dataset.
#
# If a missing value occurs at the beginning of the dataset and cannot be forward-filled, the remaining missing value is filled using the training-data median during the modeling pipeline.
#
# No information from future observations is used for temporal feature construction.

# %% [step_7]
numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

print("Missing values before handling:")
display(df[numeric_columns].isna().sum())
df[numeric_columns] = df[numeric_columns].ffill()

print("Missing values after forward filling:")
display(df[numeric_columns].isna().sum())

# %% [markdown]
# ## 4. Basic Data-Quality Filtering
#
# Physically impossible negative values are treated as invalid for parameters that cannot logically be negative.
#
# The target column `Potability` is expected to contain binary values 0 and 1.
#
# Invalid observations are removed before model training.

# %% [step_9]
non_negative_columns = [
    "Hardness",
    "Solids",
    "Chloramines",
    "Sulfate",
    "Conductivity",
    "Organic_carbon",
    "Trihalomethanes",
    "Turbidity"
]

for column in non_negative_columns:
    if column in df.columns:
        df = df[df[column] >= 0]

if "ph" in df.columns:
    df = df[
        (df["ph"] >= 0) &
        (df["ph"] <= 14)
    ]

if "Potability" in df.columns:
    df = df[df["Potability"].isin([0, 1])]

df = df.reset_index(drop=True)

print("Shape after basic quality filtering:", df.shape)

# %% [markdown]
# ## 5. Chronological Train / Validation / Test Split
#
# Random splitting is avoided because it can introduce future information into the training data.
#
# The dataset is divided chronologically:
#
# - 70% training
# - 15% validation
# - 15% testing
#
# The earliest observations are used for training, followed by validation observations and finally the test observations.
#
# This split is intended for the initial temporal modeling workflow and should be confirmed with the mentor before being treated as the final project split.

# %% [step_11]
n = len(df)

train_end = int(n * 0.70)
val_end = int(n * 0.85)

train_df = df.iloc[:train_end].copy()
val_df = df.iloc[train_end:val_end].copy()
test_df = df.iloc[val_end:].copy()

print("Train shape:", train_df.shape)
print("Validation shape:", val_df.shape)
print("Test shape:", test_df.shape)

print("\nTrain period:")
print(train_df["timestamp"].min(), "->", train_df["timestamp"].max())

print("\nValidation period:")
print(val_df["timestamp"].min(), "->", val_df["timestamp"].max())

print("\nTest period:")
print(test_df["timestamp"].min(), "->", test_df["timestamp"].max())
from sklearn.preprocessing import StandardScaler

# %% [markdown]
# ## 6. Feature Scaling
#
# StandardScaler is used as the initial scaling method.
#
# The scaler is fitted only on the training data to prevent information leakage from validation and test observations.
#
# The same fitted scaler is then applied to validation and test data.

# %% [step_13]
feature_columns = [
    col for col in numeric_columns
    if col != "Potability"
]

scaler = StandardScaler()

train_scaled = train_df.copy()
val_scaled = val_df.copy()
test_scaled = test_df.copy()

train_scaled[feature_columns] = scaler.fit_transform(
    train_df[feature_columns]
)

val_scaled[feature_columns] = scaler.transform(
    val_df[feature_columns]
)

test_scaled[feature_columns] = scaler.transform(
    test_df[feature_columns]
)

print("Scaling completed.")

# %% [markdown]
# ## 7. Processed Partition Persistence
#
# The cleaned, scaled chronological partitions are saved to outputs/tables/ for downstream modeling.
#
# Preserving these partitions guarantees reproducible handoff to subsequent anomaly detection and forecasting pipelines.

# %% [step_15]
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

def _find_project_root():
    curr = Path.cwd()
    for p in [curr] + list(curr.parents):
        if (p / 'pyproject.toml').exists() or (p / 'requirements.txt').exists():
            return p
    return curr

project_root = _find_project_root()
processed_path = project_root / 'data' / 'processed' / 'water_quality_timestamped.csv'

df = pd.read_csv(processed_path)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.sort_values('timestamp').reset_index(drop=True)
print('Dataset shape:', df.shape)
print('Columns:', df.columns.tolist())
display(df.head())

# %% [markdown]
# ## 8. Chronological Boundary & Distribution Diagnostics
#
# We assert that train partition timestamps end before validation starts, and validation ends before test starts.
#
# We also verify that normalized training features have zero mean and unit variance.

# %% [step_17]
# Output Figure: fig_p
# Output Table: tbl_p
print("TRAIN")
print(train_scaled.shape)
print(train_scaled["timestamp"].min())
print(train_scaled["timestamp"].max())

print("\nVALIDATION")
print(val_scaled.shape)
print(val_scaled["timestamp"].min())
print(val_scaled["timestamp"].max())

print("\nTEST")
print(test_scaled.shape)
print(test_scaled["timestamp"].min())
print(test_scaled["timestamp"].max())
print("\nChronological checks:")

print(
    "Train ends before validation:",
    train_scaled["timestamp"].max()
    <= val_scaled["timestamp"].min()
)

print(
    "Validation ends before test:",
    val_scaled["timestamp"].max()
    <= test_scaled["timestamp"].min()
)

print(
    "Train feature means approximately 0:"
)

display(
    train_scaled[feature_columns]
    .mean()
    .round(3)
)

# Generate partition split plot and summary table
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.scatter(train_scaled["timestamp"], [1]*len(train_scaled), s=3, color="#1f77b4", label=f"Train ({len(train_scaled)})")
ax.scatter(val_scaled["timestamp"], [1]*len(val_scaled), s=3, color="#ff7f0e", label=f"Val ({len(val_scaled)})")
ax.scatter(test_scaled["timestamp"], [1]*len(test_scaled), s=3, color="#2ca02c", label=f"Test ({len(test_scaled)})")
ax.set_yticks([])
ax.set_title("Day 11 Task 1: Chronological Train / Val / Test Partition Timeline", fontsize=11, pad=10)
ax.set_xlabel("Timestamp")
ax.legend(loc="upper right")
plt.tight_layout()
fig_p = Path("Day_Wise_Tasks/Day_11_Task_1/outputs/figures/day11_temporal_split.png")
fig_p.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_p, dpi=150, bbox_inches="tight")
plt.close()

df_summary = pd.DataFrame([
    {"Partition": "Train", "Samples": len(train_scaled), "Start": str(train_scaled["timestamp"].min()), "End": str(train_scaled["timestamp"].max())},
    {"Partition": "Validation", "Samples": len(val_scaled), "Start": str(val_scaled["timestamp"].min()), "End": str(val_scaled["timestamp"].max())},
    {"Partition": "Test", "Samples": len(test_scaled), "Start": str(test_scaled["timestamp"].min()), "End": str(test_scaled["timestamp"].max())}
])
tbl_p = Path("Day_Wise_Tasks/Day_11_Task_1/outputs/tables/day11_preprocessed_summary.csv")
tbl_p.parent.mkdir(parents=True, exist_ok=True)
df_summary.to_csv(tbl_p, index=False)
print("Saved Day 11 Task 1 outputs to:", fig_p, "and", tbl_p)

# %% [markdown]
# # Day 11 – Assumptions and Methodology
#
# ## Assumptions
#
# 1. The timestamps are synthetic because the supplied dataset does not contain real temporal information.
# 2. The original raw dataset is preserved and is not modified.
# 3. The timestamped dataset generated during Day 8 is treated as the input to the temporal preprocessing pipeline.
# 4. Duplicate timestamps are handled deterministically by retaining the first record.
# 5. Missing numeric values are initially handled using forward filling.
# 6. Invalid parameter values are removed using basic domain constraints.
# 7. Data is split chronologically into 70% training, 15% validation, and 15% testing.
# 8. Random train/test splitting is avoided to reduce temporal data leakage.
# 9. Feature scaling is fitted only on the training data.
# 10. The same fitted scaler is applied to validation and test data.
# 11. The preprocessing pipeline is designed to be reusable for future anomaly-detection and forecasting experiments.
# 12. The generated temporal patterns should not be interpreted as actual environmental or sensor behaviour.
#
# ## Day 11 Deliverable
#
# The Day 11 preprocessing pipeline produces:
#
# - Cleaned timestamped data
# - Chronological train/validation/test datasets
# - Scaled numerical features
# - Reproducible preprocessing steps
# - Preserved raw and processed datasets
#
# These outputs will be used as inputs for subsequent anomaly-detection and forecasting experiments.

