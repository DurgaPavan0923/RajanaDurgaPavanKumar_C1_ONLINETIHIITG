"""Master test and rerun orchestrator for all 28 days of tasks."""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "Day_Wise_Tasks"


def main():
    print("=" * 80)
    print("Master Rerun & Validation Suite: RajanaDurgaPavanKumar_C1_ONLINETIHIITG")
    print("=" * 80)

    task_dirs = sorted([d for d in TASKS_DIR.iterdir() if d.is_dir() and d.name.startswith("Day_")])
    print(f"Discovered {len(task_dirs)} task directories to execute...")

    summary_rows = []
    total_notebooks_ok = 0
    total_scripts_ok = 0
    total_figs_count = 0
    total_tables_count = 0

    for t_dir in task_dirs:
        parts = t_dir.name.split("_")
        day_num = int(parts[1])
        task_num = int(parts[3])

        nb_files = list(t_dir.glob("*.ipynb"))
        py_files = [f for f in t_dir.glob("*.py") if not f.name.startswith("verify_")]

        nb_ok = "N/A"
        if nb_files:
            nb = nb_files[0]
            # Execute notebook inplace using jupyter nbconvert or python execution
            cmd = [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--inplace",
                "--ExecutePreprocessor.timeout=1200",
                str(nb),
            ]
            res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if res.returncode == 0:
                nb_ok = "YES"
                total_notebooks_ok += 1
            else:
                nb_ok = "FAIL"
                print(f"Error executing {nb.name}: {res.stderr[:200]}")

        py_ok = "N/A"
        if py_files:
            py_f = py_files[0]
            res = subprocess.run([sys.executable, str(py_f)], cwd=ROOT, capture_output=True, text=True)
            if res.returncode == 0:
                py_ok = "YES"
                total_scripts_ok += 1
            else:
                py_ok = "FAIL"
                print(f"Error executing {py_f.name}: {res.stderr[:200]}")

        # Count figures and tables
        figs = list((t_dir / "outputs" / "figures").glob("*.png")) if (t_dir / "outputs" / "figures").exists() else []
        tables = list((t_dir / "outputs" / "tables").glob("*.csv")) if (t_dir / "outputs" / "tables").exists() else []
        total_figs_count += len(figs)
        total_tables_count += len(tables)

        summary_rows.append({
            "Day": f"Day {day_num:02d}",
            "Task": f"Task {task_num}",
            "Notebook OK": nb_ok,
            "Script OK": py_ok,
            "Figures": len(figs),
            "Tables": len(tables),
        })

    # Print markdown table
    print("\n" + "=" * 80)
    print("FINAL EXECUTION SUMMARY TABLE")
    print("=" * 80)
    print(f"| Day | Task | Notebook OK | Script OK | Figures Saved | Tables Saved |")
    print(f"| :--- | :--- | :---: | :---: | :---: | :---: |")
    for r in summary_rows:
        print(f"| {r['Day']} | {r['Task']} | {r['Notebook OK']} | {r['Script OK']} | {r['Figures']} | {r['Tables']} |")

    print("\nTotal Successful Notebooks:", total_notebooks_ok)
    print("Total Successful Scripts:", total_scripts_ok)
    print("Total Figures Saved:", total_figs_count)
    print("Total Tables Saved:", total_tables_count)


if __name__ == "__main__":
    main()
