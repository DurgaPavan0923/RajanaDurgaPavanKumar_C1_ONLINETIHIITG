"""Refactor task step code in phase1_tasks.py through phase4_tasks.py.
Enforces:
- fig_path = FIG_DIR / "<filename>.png"
- tbl_path = TBL_DIR / "<filename>.csv"
- display(df) in table cells
- plt.savefig -> plt.show() -> print("Saved ... to:", fig_path.relative_to(ROOT))
- df.to_csv -> print("Saved ... to:", tbl_path.relative_to(ROOT))
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "scripts" / "tasks"


def patch_file(file_path: Path):
    text = file_path.read_text(encoding="utf-8")
    original_text = text

    # 1. Replace fig_path definitions
    text = re.sub(
        r'fig_path\s*=\s*Path\("Day_Wise_Tasks/Day_\d+_Task_\d+/outputs/figures/([^"]+)"\)',
        r'fig_path = FIG_DIR / "\1"',
        text,
    )

    # 2. Replace tbl_path definitions
    text = re.sub(
        r'tbl_path\s*=\s*Path\("Day_Wise_Tasks/Day_\d+_Task_\d+/outputs/tables/([^"]+)"\)',
        r'tbl_path = TBL_DIR / "\1"',
        text,
    )

    # 3. Remove mkdir lines
    text = re.sub(r'^[ \t]*fig_path\.parent\.mkdir\(parents=True,\s*exist_ok=True\)\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*tbl_path\.parent\.mkdir\(parents=True,\s*exist_ok=True\)\n?', '', text, flags=re.MULTILINE)

    # 4. Standardize all fig prints: e.g. print("...", fig_path)
    text = re.sub(
        r'print\((["\'].*?["\']),\s*fig_path\)',
        r'print(\1, fig_path.relative_to(ROOT))',
        text,
    )

    # 5. Standardize all table prints: e.g. print("...", tbl_path)
    text = re.sub(
        r'print\((["\'].*?["\']),\s*tbl_path\)',
        r'print(\1, tbl_path.relative_to(ROOT))',
        text,
    )

    # 6. Ensure display() is called before to_csv if not present
    def add_display(match):
        block = match.group(0)
        if "display(" in block:
            return block
        m_var = re.search(r'([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)*)\.to_csv\(tbl_path', block)
        if m_var:
            var_name = m_var.group(1)
            sub_target = f"{var_name}.to_csv(tbl_path"
            replacement = f"display({var_name})\n{var_name}.to_csv(tbl_path"
            return block.replace(sub_target, replacement, 1)
        return block

    text = re.sub(r'\"\"\"[^\"]*?tbl_path[^\"]*?\"\"\"', add_display, text, flags=re.DOTALL)

    if text != original_text:
        file_path.write_text(text, encoding="utf-8")
        print(f"Patched: {file_path.name}")
    else:
        print(f"No changes: {file_path.name}")


def main():
    for p in sorted(TASKS_DIR.glob("phase*.py")):
        patch_file(p)


if __name__ == "__main__":
    main()
