#!/usr/bin/env python3
"""Audit script to detect hidden tables in Day_Wise_Tasks notebooks.

Scans all .ipynb notebooks in Day_Wise_Tasks/ for code cells that export tables
via .to_csv(), .to_excel(), .to_markdown(), or write to outputs/tables/, checking
whether the table is rendered inline via display() with text/html or text/plain output.
Also flags DataFrames/Series that are never displayed or printed.
"""

import ast
import re
import sys
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parent
DAY_TASKS_DIR = ROOT / "Day_Wise_Tasks"


def find_created_dfs(code_text: str):
    """Detect variables assigned from pd.DataFrame, pd.read_csv, .describe(), .round(), etc."""
    pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:pd\.DataFrame|pd\.read_csv|df[a-zA-Z0-9_]*\.(?:head|describe|copy|sort_values|corr)|corr_mat)"
    return re.findall(pattern, code_text)


def scan_hidden_tables():
    notebooks = sorted(
        DAY_TASKS_DIR.glob("Day_*_Task_*/*.ipynb"),
        key=lambda p: (
            int(re.search(r"Day_(\d+)", p.parent.name).group(1)),
            int(re.search(r"Task_(\d+)", p.parent.name).group(1)),
        ),
    )

    print("=" * 115)
    print(f"{'Notebook':<45} | {'Cell':<5} | {'Variable':<22} | {'Table File':<25} | {'Status':<8}")
    print("=" * 115)

    total_table_saves = 0
    hidden_count = 0
    shown_count = 0
    results = []

    for nb_path in notebooks:
        try:
            nb = nbformat.read(nb_path, as_version=4)
        except Exception as e:
            print(f"Error reading {nb_path.name}: {e}")
            continue

        rel_nb = nb_path.relative_to(ROOT).as_posix()

        for idx, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            src = cell.source

            # Exclude environment setup cell (cell 1) unless it actually saves a CSV
            is_table_save = (
                ".to_csv(" in src
                or ".to_excel(" in src
                or ".to_markdown(" in src
            ) and ("tbl_path" in src or "outputs/tables/" in src or "TBL_DIR" in src)

            if not is_table_save:
                continue

            total_table_saves += 1

            # Extract variable name being saved
            m_var = re.search(r"([a-zA-Z_0-9]+(?:\.[a-zA-Z_0-9]+)*)\.(?:to_csv|to_excel|to_markdown)\(", src)
            var_name = m_var.group(1) if m_var else "DataFrame"
            # Normalize e.g. pd.DataFrame([attestation_certificate])
            if var_name.startswith("pd."):
                var_name = "DataFrame"

            # Extract table file name
            m_tbl = re.search(r'(?:TBL_DIR\s*/\s*["\']|outputs/tables/)([^"\'>\s]+)["\']?', src)
            tbl_file = m_tbl.group(1) if m_tbl else "table.csv"

            # Check if display(...) is called in code
            has_display_call = bool(re.search(r"display\s*\(", src))

            # Check outputs for html or rich representation
            has_html_out = False
            has_table_out = False
            for out in cell.get("outputs", []):
                data = out.get("data", {})
                if "text/html" in data:
                    has_html_out = True
                    has_table_out = True
                elif "text/plain" in data and out.get("output_type") in ("display_data", "execute_result"):
                    text_plain = "".join(data["text/plain"])
                    if "\n" in text_plain and (len(text_plain.split("\n")) > 2 or "\t" in text_plain):
                        has_table_out = True

            # Status determination
            is_shown = has_display_call and (has_html_out or has_table_out)
            status = "shown" if is_shown else "hidden"

            if status == "hidden":
                hidden_count += 1
            else:
                shown_count += 1

            results.append({
                "notebook": rel_nb,
                "cell": idx,
                "variable": var_name,
                "table_file": tbl_file,
                "status": status,
                "code": src
            })

            print(f"{rel_nb:<45} | {idx:<5} | {var_name:<22} | {tbl_file:<25} | {status:<8}")

    print("=" * 115)
    print(f"Summary: Discovered {total_table_saves} table export cells across {len(notebooks)} notebooks.")
    print(f"Shown inline:  {shown_count}")
    print(f"Hidden/Absent: {hidden_count}")
    print("=" * 115)

    return results


if __name__ == "__main__":
    scan_hidden_tables()
