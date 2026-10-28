"""Patch all notebooks in Day_Wise_Tasks to robustly locate the project root."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "Day_Wise_Tasks"

OLD_TARGET = 'project_root = Path("..").resolve() if Path("..").resolve().name == "Water Potability" else Path(".").resolve()'

NEW_REPLACEMENT = """# Universal project root detection (works from any clone directory or depth)
def _find_project_root():
    curr = Path.cwd()
    for p in [curr] + list(curr.parents):
        if (p / "pyproject.toml").exists() or (p / "requirements.txt").exists():
            return p
    return curr

project_root = _find_project_root()"""

notebooks = list(TASKS_DIR.rglob("*.ipynb"))
print(f"Checking {len(notebooks)} notebooks for root anchor patching...")

patched_count = 0
for nb_path in notebooks:
    with open(nb_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    modified = False
    for cell in nb_data.get("cells", []):
        if cell.get("cell_type") == "code":
            source_lines = cell.get("source", [])
            source_text = "".join(source_lines)
            if 'Path("..").resolve().name == "Water Potability"' in source_text:
                new_source = []
                for line in source_lines:
                    if 'Path("..").resolve().name == "Water Potability"' in line:
                        new_source.extend([l + "\n" for l in NEW_REPLACEMENT.split("\n")])
                    else:
                        new_source.append(line)
                cell["source"] = new_source
                modified = True

    if modified:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb_data, f, indent=1)
        print(f"Patched root detection in: {nb_path.name}")
        patched_count += 1

print(f"Successfully patched {patched_count} notebooks!")
