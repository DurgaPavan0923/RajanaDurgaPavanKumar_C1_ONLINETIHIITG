"""Builder script to generate, standardize, and execute all 56 Day_X_Task_Y tasks to reference standard."""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "Day_Wise_Tasks"
TASKS_DIR.mkdir(exist_ok=True)

# Common setup code snippet for all notebooks (invariant root anchor)
COMMON_SETUP = """import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Universal project root detection
def _find_project_root():
    curr = Path.cwd()
    for p in [curr] + list(curr.parents):
        if (p / "pyproject.toml").exists() or (p / "requirements.txt").exists():
            return p
    return curr

project_root = _find_project_root()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Set global deterministic random seed
np.random.seed(42)
print("Environment initialized successfully. Root:", project_root)"""


def make_cell(cell_type: str, source: str) -> dict:
    lines = [line + "\n" for line in source.split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": lines,
        "outputs": [] if cell_type == "code" else None,
        "execution_count": None if cell_type == "code" else None,
    }


def build_task_notebook(day: int, task: int, topic: str, objective_text: str, steps: list, assumptions_text: str, deliverable_text: str) -> dict:
    cells = []
    
    # Cell 0: H1 Title and Objective
    c0 = f"""# Day {day} - {topic}

## Objective

{objective_text}"""
    cells.append(make_cell("markdown", c0))
    
    # Steps 1 to N (alternating Markdown explanation and Code cell)
    for i, step in enumerate(steps, 1):
        md_text = f"""## {i}. {step['title']}

{step['desc']}"""
        cells.append(make_cell("markdown", md_text))
        cells.append(make_cell("code", step["code"]))
        
    # Closing Cell: Assumptions and Methodology
    closing_text = f"""# Day {day} - Assumptions and Methodology

## Assumptions

{assumptions_text}

## Day {day} Deliverable

{deliverable_text}"""
    cells.append(make_cell("markdown", closing_text))
    
    clean_cells = []
    for c in cells:
        cd = {
            "cell_type": c["cell_type"],
            "metadata": c["metadata"],
            "source": c["source"],
        }
        if c["cell_type"] == "code":
            cd["outputs"] = []
            cd["execution_count"] = None
        clean_cells.append(cd)
        
    nb = {
        "cells": clean_cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.11"},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return nb


def execute_and_save_notebook(nb_dict: dict, nb_path: Path):
    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.from_dict(nb_dict)
    client = NotebookClient(nb, timeout=300, kernel_name="python3")
    try:
        client.execute()
    except Exception as e:
        print(f"Execution warning in {nb_path.name}: {e}")
        
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Saved executed notebook: {nb_path.name}")


print("Builder module initialized.")
