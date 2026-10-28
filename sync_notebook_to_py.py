"""Script to auto-generate and synchronize .py mirrors from all .ipynb notebooks in Day_Wise_Tasks."""

import os
import sys
from pathlib import Path

try:
    import nbformat
except ImportError:
    print("Error: nbformat is required. Install with pip install nbformat.")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "Day_Wise_Tasks"


def notebook_to_py(nb_path: Path) -> Path:
    nb_path = nb_path.resolve()
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    py_name = nb_path.stem + ".py"
    py_path = nb_path.parent / py_name

    lines = []
    lines.append(f'"""Automated Python script mirror for {nb_path.name}.')
    lines.append("Generated with exact 1-to-1 step parity.")
    lines.append('"""\n')

    fig_outputs_found = 0
    tbl_outputs_found = 0

    for cell_idx, cell in enumerate(nb.cells):
        if cell.cell_type == "markdown":
            lines.append("# %% [markdown]")
            for src_line in cell.source.splitlines():
                lines.append(f"# {src_line}" if src_line else "#")
            lines.append("")
        elif cell.cell_type == "code":
            lines.append(f"# %% [step_{cell_idx}]")
            code_text = cell.source.strip()

            # Strip any unconditional matplotlib.use("Agg")
            code_text = code_text.replace('matplotlib.use("Agg")', '')
            code_text = code_text.replace("matplotlib.use('Agg')", '')

            # Handle %matplotlib inline by replacing with conditional headless backend check
            if "%matplotlib inline" in code_text:
                headless_check = (
                    "# %matplotlib inline\n"
                    "import os, matplotlib\n"
                    "if os.environ.get('DISPLAY', '') == '' and os.name != 'nt' or os.environ.get('MPLBACKEND') == 'Agg':\n"
                    "    matplotlib.use('Agg')"
                )
                code_text = code_text.replace("%matplotlib inline", headless_check)

            # Check for embedded outputs to tag
            if "savefig(" in code_text:
                for cl in code_text.splitlines():
                    if "savefig(" in cl:
                        parts = cl.split("savefig(")
                        if len(parts) > 1:
                            sub = parts[1].split(",")[0].strip("\"' ")
                            # Extract clean basename if path was variable
                            if "/" in sub:
                                sub = sub.split("/")[-1].strip("\"' ")
                            lines.append(f"# Output: outputs/figures/{sub}")
                            fig_outputs_found += 1
            if "to_csv(" in code_text:
                for cl in code_text.splitlines():
                    if "to_csv(" in cl:
                        parts = cl.split("to_csv(")
                        if len(parts) > 1:
                            sub = parts[1].split(",")[0].strip("\"' ")
                            if "/" in sub:
                                sub = sub.split("/")[-1].strip("\"' ")
                            lines.append(f"# Output: outputs/tables/{sub}")
                            tbl_outputs_found += 1

            # Translate display(df) to print(df.to_string()) for parity with notebook table rendering
            import re
            code_lines = []
            for cl in code_text.splitlines():
                m_disp = re.match(r"^(\s*)display\((.*)\)\s*$", cl)
                if m_disp:
                    indent = m_disp.group(1)
                    arg = m_disp.group(2).strip()
                    if arg.endswith(".head(20)"):
                        code_lines.append(f"{indent}print({arg}.to_string())")
                    elif re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", arg):
                        code_lines.append(f"{indent}print({arg}.to_string())")
                    else:
                        code_lines.append(f"{indent}print({arg}.to_string() if hasattr({arg}, 'to_string') else {arg})")
                else:
                    code_lines.append(cl)
            code_text = "\n".join(code_lines)

            lines.append(code_text)
            lines.append("")

    content = "\n".join(lines) + "\n"
    py_path.write_text(content, encoding="utf-8")
    try:
        rel = py_path.relative_to(ROOT)
    except Exception:
        rel = py_path.name
    print(f"Synced mirror: {rel} ({fig_outputs_found} fig tags, {tbl_outputs_found} tbl tags)")
    return py_path


def main():
    if not TASKS_DIR.exists():
        print(f"Directory {TASKS_DIR} does not exist!")
        sys.exit(1)

    notebooks = sorted(list(TASKS_DIR.rglob("*.ipynb")))
    print(f"Found {len(notebooks)} notebooks to synchronize into Python mirrors...")

    synced = 0
    for nb in notebooks:
        try:
            notebook_to_py(nb)
            synced += 1
        except Exception as e:
            print(f"FAILED to sync {nb}: {e}")
            sys.exit(1)

    print("=" * 60)
    print(f"Parity Complete: All {synced} notebooks have 1-to-1 matching Python scripts.")
    print("=" * 60)


if __name__ == "__main__":
    main()
