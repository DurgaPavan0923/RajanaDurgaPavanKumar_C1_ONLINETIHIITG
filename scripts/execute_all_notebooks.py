"""Script to execute all 56 notebooks and save outputs directly into .ipynb files."""

import sys
import time
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "Day_Wise_Tasks"

def execute_single_notebook(nb_path: Path):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Ensure source is a clean string
    for cell in nb.cells:
        if isinstance(cell.source, list):
            cell.source = "".join(cell.source)

    client = NotebookClient(nb, timeout=120, kernel_name="python3")
    client.execute()

    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)


def main():
    print("=" * 80)
    print("Executing all 56 Jupyter Notebooks to populate outputs...")
    print("=" * 80)

    notebooks = sorted(list(TASKS_DIR.rglob("*.ipynb")))
    print(f"Found {len(notebooks)} notebooks to execute...")

    passed = 0
    failed = 0

    for idx, nb in enumerate(notebooks, 1):
        rel = nb.relative_to(ROOT)
        t0 = time.time()
        try:
            execute_single_notebook(nb)
            dur = time.time() - t0
            print(f"[{idx:02d}/{len(notebooks)}] [PASS] {rel} ({dur:.2f}s)")
            passed += 1
        except Exception as e:
            dur = time.time() - t0
            print(f"[{idx:02d}/{len(notebooks)}] [FAIL] {rel} ({dur:.2f}s): {e}")
            failed += 1

    print("=" * 80)
    print(f"Notebook Execution Complete: {passed} PASSED, {failed} FAILED.")
    print("=" * 80)


if __name__ == "__main__":
    main()
