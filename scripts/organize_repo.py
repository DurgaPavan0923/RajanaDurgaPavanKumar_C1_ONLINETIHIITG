"""Organize Day_X_Task_Y folders into Day_Wise_Tasks/ using git mv."""

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = ROOT / "Day_Wise_Tasks"
TARGET_DIR.mkdir(exist_ok=True)

folders = sorted([d for d in ROOT.iterdir() if d.is_dir() and d.name.startswith("Day_") and d.name != "Day_Wise_Tasks"])

print(f"Found {len(folders)} day folders to organize into Day_Wise_Tasks/...")

for folder in folders:
    dest = TARGET_DIR / folder.name
    if dest.exists():
        print(f"Skipping (already exists in target): {folder.name}")
        continue
    # Use git mv
    res = subprocess.run(["git", "mv", str(folder), str(dest)], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"git mv: {folder.name} -> Day_Wise_Tasks/{folder.name}")
    else:
        print(f"git mv failed ({res.stderr.strip()}), falling back to os.rename...")
        os.rename(folder, dest)
        subprocess.run(["git", "add", str(dest)])

print("Validating Day_Wise_Tasks/...")
moved = sorted([d.name for d in TARGET_DIR.iterdir() if d.is_dir()])
print(f"Total folders in Day_Wise_Tasks/: {len(moved)}")

missing = []
for d in range(1, 29):
    for t in [1, 2]:
        name = f"Day_{d}_Task_{t}"
        if name not in moved:
            missing.append(name)

if missing:
    print(f"WARNING: Missing folders: {missing}")
else:
    print("ALL 56 Day_X_Task_Y folders from Day 1 to Day 28 are present and accounted for!")
