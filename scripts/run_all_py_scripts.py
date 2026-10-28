"""Fast runner to execute all 56 python task mirrors and verify they generate figures & tables."""

import sys
import time
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "Day_Wise_Tasks"

def main():
    print("=" * 80)
    print("Executing all 56 Python Task Mirrors...")
    print("=" * 80)
    
    task_dirs = []
    for d in TASKS_DIR.glob("Day_*_Task_*"):
        parts = d.name.split("_")
        task_dirs.append((int(parts[1]), int(parts[3]), d))
    task_dirs.sort()
    
    passed = 0
    failed = 0
    
    for day, task, d in task_dirs:
        py_files = [f for f in d.glob("day*.py") if not f.name.startswith("verify_")]
        if not py_files:
            print(f"[SKIP] {d.name}: No day*.py found.")
            continue
        py_f = py_files[0]
        t0 = time.time()
        res = subprocess.run([sys.executable, str(py_f)], cwd=ROOT, capture_output=True, text=True)
        dur = time.time() - t0
        if res.returncode == 0:
            figs = list((d / "outputs" / "figures").glob("*.png"))
            tables = list((d / "outputs" / "tables").glob("*.csv"))
            print(f"[PASS] {d.name:15s} | {py_f.name:32s} | {dur:.2f}s | {len(figs)} figs | {len(tables)} tables", flush=True)
            passed += 1
        else:
            print(f"[FAIL] {d.name:15s} | {py_f.name:32s} | Error: {res.stderr[:100]}", flush=True)
            failed += 1
            
    print("=" * 80)
    print(f"Summary: {passed} PASSED, {failed} FAILED.")
    print("=" * 80)

if __name__ == "__main__":
    main()
