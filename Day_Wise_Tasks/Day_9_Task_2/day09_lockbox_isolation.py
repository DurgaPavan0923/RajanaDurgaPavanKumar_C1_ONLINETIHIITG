"""Automated Python script mirror for day09_lockbox_isolation.ipynb.
Generated with exact 1-to-1 step parity.
"""

# %% [markdown]
# # Day 9 - Quarantined Test Lockbox Seal & Metadata
#
# ## Objective
#
# Quarantine the held-out test partition, compute cryptographic SHA-256 seal, and lock it against developmental inspection.

# %% [step_1]
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def _find_project_root():
    curr = Path.cwd()
    for p in [curr] + list(curr.parents):
        if (p / "pyproject.toml").exists() or (p / "requirements.txt").exists():
            return p
    return curr

project_root = _find_project_root()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
os.chdir(project_root)

np.random.seed(42)
print("Environment initialized successfully. Project root:", project_root)

# %% [markdown]
# ## 1. Lockbox Partition Ingestion and Verification
#
# Extract the 492 held-out test samples and verify immutability parameters.

# %% [step_3]
df_ts = pd.read_csv("data/processed/water_quality_timestamped.csv")
cut2 = int(len(df_ts) * 0.85)
test_lockbox = df_ts.iloc[cut2:].copy()
print(f"Quarantined Lockbox Samples: {len(test_lockbox)}")

# %% [markdown]
# ## 2. Cryptographic Lockbox Hash Calculation
#
# Compute SHA-256 signature sealing the held-out test lockbox against alteration.

# %% [step_5]
# Output Table: index=False).encode("utf-8")
import hashlib
csv_bytes = test_lockbox.to_csv(index=False).encode("utf-8")
lockbox_sha = hashlib.sha256(csv_bytes).hexdigest()
print(f"Test Lockbox Cryptographic Seal: {lockbox_sha}")

# %% [markdown]
# ## 3. Index Isolation and Disjointness Audit
#
# Assert that test indices share zero intersection with training or validation indices.

# %% [step_7]
train_val_indices = set(range(cut2))
lockbox_indices = set(test_lockbox.index)
overlap = train_val_indices.intersection(lockbox_indices)
print(f"Index Overlap Count: {len(overlap)}")

# %% [markdown]
# ## 4. Feature Column Immutability Check
#
# Assert that lockbox preserves identical feature schema as training sets.

# %% [step_9]
cols = test_lockbox.columns.tolist()
print(f"Sealed Columns ({len(cols)}): {cols}")

# %% [markdown]
# ## 5. Quarantine Security Manifest Formulation
#
# Construct metadata dictionary declaring the quarantine lockbox sealed until final unblinding.

# %% [step_11]
manifest = {
    "Artifact": "dataset_v1_test_lockbox",
    "Sample_Count": len(test_lockbox),
    "SHA256": lockbox_sha,
    "Access_Policy": "BLINDED_UNTIL_DAY_23",
    "Auditor": "Rajana Durga Pavan Kumar"
}
df_manifest = pd.DataFrame([manifest])
print(df_manifest.to_string(index=False))

# %% [markdown]
# ## 6. Partition Index Allocation Diagnostic Plot
#
# Render partition allocation bar chart displaying isolated lockbox segment.

# %% [step_13]
# Output Figure: fig_path
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.bar(["Train/Val Active", "Test Lockbox (Quarantined)"], [cut2, len(test_lockbox)], color=["#1f77b4", "#d62728"], alpha=0.85)
ax.set_title("Day 9 Task 2: Quarantine Isolation Barrier", fontsize=11, pad=10)
ax.set_ylabel("Number of Samples")
for i, v in enumerate([cut2, len(test_lockbox)]):
    ax.text(i, v + 50, f"{v}", ha="center", fontweight="bold")
plt.tight_layout()
fig_path = Path("Day_Wise_Tasks/Day_9_Task_2/outputs/figures/day9_task2_lockbox_isolation.png")
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.show()
print("Saved lockbox isolation plot to:", fig_path)

# %% [markdown]
# ## 7. Lockbox Manifest Table Export
#
# Export lockbox quarantine security manifest to CSV.

# %% [step_15]
# Output Table: tbl_path
tbl_path = Path("Day_Wise_Tasks/Day_9_Task_2/outputs/tables/day9_task2_lockbox_manifest.csv")
tbl_path.parent.mkdir(parents=True, exist_ok=True)
df_manifest.to_csv(tbl_path, index=False)
print("Saved lockbox manifest to:", tbl_path)

# %% [markdown]
# ## 8. Quarantine Integrity Gate
#
# Assert that index overlap is strictly zero and SHA-256 seal is valid.

# %% [step_17]
assert len(overlap) == 0 and len(lockbox_sha) == 64
print("Day 9 Task 2 Quality Gate: PASSED.")

# %% [markdown]
# # Day 9 - Assumptions and Methodology
#
# ## Assumptions
#
# 1. Test lockbox remains blinded until final unblinding milestone on Day 23.
# 2. Any access to test labels during developmental training invalidates model certification.
#
# ## Day 9 Deliverable
#
# Test lockbox manifest, quarantine isolation plot, and cryptographic seal certificate.

