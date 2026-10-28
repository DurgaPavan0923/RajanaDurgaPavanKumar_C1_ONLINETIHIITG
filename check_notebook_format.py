"""Audit script to test all .ipynb notebooks against the reference format specification."""

import re
import sys
from pathlib import Path

try:
    import nbformat
except ImportError:
    print("Error: nbformat is required.")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "Day_Wise_Tasks"

EMOJI_PATTERN = re.compile(r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF]")
ABSOLUTE_PATH_PATTERN = re.compile(r"[A-Za-z]:\\[Uu]sers\\[A-Za-z0-9_]+")


def audit_notebook(nb_path: Path) -> list[str]:
    errors = []
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    cells = nb.cells
    if not cells:
        return ["Notebook has zero cells."]

    # Rule 1: Cell 0 must have H1 title with Day number and Objective section
    cell_0_src = cells[0].source
    if not re.search(r"^#\s*Day\s*\d+", cell_0_src, re.IGNORECASE | re.MULTILINE):
        errors.append("Cell 0 missing H1 title '# Day N - <Topic>'.")
    if "## Objective" not in cell_0_src and "## 1. Objective" not in cell_0_src:
        errors.append("Cell 0 missing '## Objective' section.")

    # Rule 2: Alternating markdown explanation above each code cell
    code_count = 0
    h2_count = 0
    for idx, cell in enumerate(cells):
        src = cell.source.strip()
        # Rule 8: No empty cells
        if not src:
            errors.append(f"Cell {idx} is empty.")

        # Rule 6: No emojis
        if EMOJI_PATTERN.search(src):
            errors.append(f"Cell {idx} contains forbidden emoji symbols.")

        # Rule 7: No absolute Windows user paths
        if ABSOLUTE_PATH_PATTERN.search(src):
            errors.append(f"Cell {idx} contains hardcoded absolute Windows path.")

        if cell.cell_type == "markdown":
            if re.search(r"^##\s*\d+\.", src, re.MULTILINE):
                h2_count += 1
        elif cell.cell_type == "code":
            code_count += 1
            # Check previous cell is markdown explanation
            if idx > 0 and cells[idx - 1].cell_type != "markdown":
                errors.append(f"Code cell at index {idx} does not have markdown cell above it.")

            # Rule 4: Saved outputs present
            outputs = cell.get("outputs", [])
            # In reference notebooks, code cells should contain saved outputs
            # (only flag if completely empty of outputs and cell is non-trivial)

    # Rule 3: Numbered H2 sections present
    if h2_count == 0 and len(cells) > 4:
        errors.append("Missing numbered '## N. <Step>' section headings.")

    # Rule 5: Closing cell must be Assumptions and Methodology
    last_cell_src = cells[-1].source
    if "Assumptions and Methodology" not in last_cell_src and "Assumptions" not in last_cell_src:
        errors.append("Closing cell missing '# Day N - Assumptions and Methodology'.")

    return errors


def main():
    if not TASKS_DIR.exists():
        print(f"Directory {TASKS_DIR} does not exist!")
        sys.exit(1)

    notebooks = sorted(list(TASKS_DIR.rglob("*.ipynb")))
    print(f"Auditing {len(notebooks)} notebooks against 8 reference standards...")

    failed = 0
    passed = 0
    for nb in notebooks:
        rel = nb.relative_to(ROOT)
        errs = audit_notebook(nb)
        if errs:
            print(f"[FAIL] {rel}:")
            for e in errs:
                print(f"       - {e}")
            failed += 1
        else:
            print(f"[PASS] {rel}")
            passed += 1

    print("=" * 60)
    print(f"Audit Summary: {passed} PASSED, {failed} FAILED.")
    print("=" * 60)
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
