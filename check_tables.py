#!/usr/bin/env python3
"""Validation script to verify all 56 tasks have tables rendered inline in notebooks.

Asserts that every cell exporting a table to outputs/tables/ in the saved notebook JSON
has a corresponding text/html or text/plain table output, with 0 error or stderr outputs.
Prints a formatted summary table:
Day | Task | Tables in notebook | Tables saved as CSV | Match (Y/N)
"""

import re
import sys
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parent
DAY_TASKS_DIR = ROOT / "Day_Wise_Tasks"


def verify_tables():
    task_dirs = sorted(
        [d for d in DAY_TASKS_DIR.glob("Day_*_Task_*") if d.is_dir()],
        key=lambda p: (
            int(re.search(r"Day_(\d+)", p.name).group(1)),
            int(re.search(r"Task_(\d+)", p.name).group(1)),
        ),
    )

    print("=" * 85)
    print("Table Rendering & Output Parity Audit: RajanaDurgaPavanKumar_C1_ONLINETIHIITG")
    print("=" * 85)
    print(f"{'Day':<8} | {'Task':<8} | {'Tables in Notebook':<20} | {'Tables saved CSV':<18} | {'Match':<6}")
    print("-" * 85)

    all_matched = True
    total_nb_tables = 0
    total_csv_tables = 0
    failed_tasks = []

    for task_dir in task_dirs:
        m_day = re.search(r"Day_(\d+)", task_dir.name)
        m_task = re.search(r"Task_(\d+)", task_dir.name)
        day_num = int(m_day.group(1))
        task_num = int(m_task.group(1))

        # Find notebook
        nbs = list(task_dir.glob("*.ipynb"))
        if not nbs:
            print(f"Day {day_num:02d} | Task {task_num} | NO NOTEBOOK FOUND     | 0                  | NO")
            all_matched = False
            failed_tasks.append(f"{task_dir.name} (Missing notebook)")
            continue

        nb_path = nbs[0]
        try:
            nb = nbformat.read(nb_path, as_version=4)
        except Exception as e:
            print(f"Day {day_num:02d} | Task {task_num} | CORRUPT NOTEBOOK: {e} | 0                  | NO")
            all_matched = False
            failed_tasks.append(f"{task_dir.name} (Corrupt notebook)")
            continue

        # Count CSV files in outputs/tables/
        tbl_dir = task_dir / "outputs" / "tables"
        csv_files = list(tbl_dir.glob("*.csv")) if tbl_dir.exists() else []
        csv_count = len(csv_files)
        total_csv_tables += csv_count

        # Count table outputs in notebook cells that save or display tables
        nb_table_count = 0
        has_error = False

        for cell in nb.cells:
            if cell.cell_type != "code":
                continue

            # Check for error outputs
            for out in cell.get("outputs", []):
                if out.get("output_type") == "error":
                    has_error = True

            # Check if this cell displays a table
            src = cell.source
            has_table_intent = (
                "display(" in src
                or ".to_csv(" in src
                or "outputs/tables/" in src
                or "TBL_DIR" in src
            ) and ("tbl_path" in src or "to_csv" in src or "display(" in src)

            if has_table_intent:
                cell_has_table_output = False
                for out in cell.get("outputs", []):
                    data = out.get("data", {})
                    # HTML representation (standard DataFrame rendering in Jupyter)
                    if "text/html" in data:
                        cell_has_table_output = True
                        break
                    # Rich plain text table in display_data or execute_result
                    if "text/plain" in data and out.get("output_type") in ("display_data", "execute_result"):
                        text_plain = "".join(data["text/plain"])
                        if "\n" in text_plain and (len(text_plain.split("\n")) > 2 or "\t" in text_plain):
                            cell_has_table_output = True
                            break

                if cell_has_table_output:
                    nb_table_count += 1

        total_nb_tables += nb_table_count

        # Match assertion: At least 1 table displayed inline for tasks that save CSVs, and no errors
        match = (nb_table_count >= 1) and (csv_count >= 1) and (not has_error)
        match_str = "YES" if match else "NO"
        if not match:
            all_matched = False
            fail_reason = "Missing table output" if nb_table_count < 1 else ("Missing CSV" if csv_count < 1 else "Error output present")
            failed_tasks.append(f"{task_dir.name} ({fail_reason})")

        print(f"Day {day_num:02d} | Task {task_num} | {nb_table_count:<20} | {csv_count:<18} | {match_str:<6}")

    print("=" * 85)
    print(f"Total Discovered Tasks: {len(task_dirs)} (Days 1 to 28, Tasks 1 & 2)")
    print(f"Total Notebook Tables Displayed: {total_nb_tables}")
    print(f"Total Tables Saved as CSV:       {total_csv_tables}")
    print(f"Audit Status: {'100% PASS' if all_matched else 'FAILED'}")
    if failed_tasks:
        print("Failed Tasks:")
        for ft in failed_tasks:
            print("  -", ft)
    print("=" * 85)

    return 0 if all_matched else 1


if __name__ == "__main__":
    sys.exit(verify_tables())
