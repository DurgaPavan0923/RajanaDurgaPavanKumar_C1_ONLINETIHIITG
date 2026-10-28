"""Audit and verification script for the sequential ordering of Day 1 to Day 28 tasks.
Verifies:
- All 28 days exist (Day 1 to Day 28)
- Every day has Task 1 and Task 2 (56 total tasks)
- No missing days or tasks
- No duplicate or misnamed folders
- Natural sort order confirmation
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "Day_Wise_Tasks"


def natural_sort_key(name: str):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", name)]


def main():
    print("=" * 80)
    print("Sequential Order Verification: Days 1 to 28 (56 Mandated Tasks)")
    print("=" * 80)

    if not TASKS_DIR.exists():
        print(f"Error: {TASKS_DIR} does not exist.")
        sys.exit(1)

    folders = [d for d in TASKS_DIR.iterdir() if d.is_dir() and d.name.startswith("Day_")]
    sorted_folders = sorted(folders, key=lambda p: natural_sort_key(p.name))

    print(f"Total discovered Day folders: {len(sorted_folders)}")

    expected_tasks = [(day, task) for day in range(1, 29) for task in (1, 2)]
    found_tasks = set()
    invalid_folders = []

    for f in sorted_folders:
        m = re.match(r"^Day_(\d+)_Task_(\d+)$", f.name)
        if m:
            d_num = int(m.group(1))
            t_num = int(m.group(2))
            found_tasks.add((d_num, t_num))
        else:
            invalid_folders.append(f.name)

    missing = [t for t in expected_tasks if t not in found_tasks]
    duplicates = len(sorted_folders) - len(found_tasks)

    print("\n--- Natural Sort Order (Day 1 to Day 28) ---")
    for idx, f in enumerate(sorted_folders, 1):
        nb_count = len(list(f.glob("*.ipynb")))
        py_count = len(list(f.glob("*.py")))
        print(f"[{idx:02d}/56] {f.name:<20} | Notebooks: {nb_count} | Scripts: {py_count}")

    print("\n" + "=" * 80)
    print("VERIFICATION AUDIT RESULTS")
    print("=" * 80)
    print(f"Expected Tasks:    56 (Days 1 to 28, Tasks 1 & 2)")
    print(f"Discovered Tasks:  {len(found_tasks)}")
    print(f"Missing Tasks:     {len(missing)}")
    print(f"Duplicate Tasks:   {duplicates}")
    print(f"Invalid Folders:   {len(invalid_folders)}")

    if missing:
        print("\nMissing Task Combinations:")
        for d, t in missing:
            print(f"  - Day {d} Task {t} (Day_{d}_Task_{t})")

    if invalid_folders:
        print("\nInvalid / Non-Standard Folders:")
        for inv in invalid_folders:
            print(f"  - {inv}")

    if not missing and duplicates == 0 and not invalid_folders and len(found_tasks) == 56:
        print("\nVERDICT: 100% PASS - All 28 days and 56 tasks verified in complete sequential order.")
        print("=" * 80)
        sys.exit(0)
    else:
        print("\nVERDICT: FAIL - Discrepancies detected.")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
