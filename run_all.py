"""Master Automated Notebook Runner for AquaGuard AI (28-Day Schedule).

Executes all day-aligned notebooks sequentially, validates prerequisite handoffs,
captures cell outputs, and records runtime benchmarks.
"""

import io
import json
import os
import sys
import time
import traceback
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# Anchor to project root
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)


def run_single_notebook(notebook_path: Path) -> tuple[bool, float, str]:
    t0 = time.perf_counter()
    with open(notebook_path, encoding="utf-8") as f:
        nb_data = json.load(f)

    exec_globals = {
        "__file__": str(notebook_path),
        "__name__": "__main__",
    }

    # Headless matplotlib Agg backend
    setup_code = (
        "import matplotlib\n"
        "matplotlib.use('Agg')\n"
        "import matplotlib.pyplot as plt\n"
        "def _no_op_show(*args, **kwargs):\n"
        "    pass\n"
        "plt.show = _no_op_show\n"
    )
    exec(setup_code, exec_globals)

    exec_count = 1
    error_msg = ""
    success = True

    for idx, cell in enumerate(nb_data.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue

        source_code = "".join(cell.get("source", []))
        if not source_code.strip():
            continue

        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()

        try:
            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                exec(source_code, exec_globals)

            cell_outputs = []
            out_txt = stdout_buf.getvalue()
            if out_txt:
                cell_outputs.append({
                    "output_type": "stream",
                    "name": "stdout",
                    "text": [line + "\n" for line in out_txt.splitlines()],
                })

            err_txt = stderr_buf.getvalue()
            if err_txt:
                cell_outputs.append({
                    "output_type": "stream",
                    "name": "stderr",
                    "text": [line + "\n" for line in err_txt.splitlines()],
                })

            cell["outputs"] = cell_outputs
            cell["execution_count"] = exec_count
            exec_count += 1

        except Exception as e:
            success = False
            tb_str = traceback.format_exc()
            error_msg = f"Cell {idx} failed: {e}\n{tb_str}"
            cell["outputs"] = [{
                "output_type": "error",
                "ename": type(e).__name__,
                "evalue": str(e),
                "traceback": tb_str.splitlines(),
            }]
            cell["execution_count"] = exec_count
            break

    # Save notebook with updated cell outputs
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(nb_data, f, indent=1)

    t1 = time.perf_counter()
    return success, round(t1 - t0, 2), error_msg


def main() -> int:
    notebook_files = sorted(Path("notebooks").glob("day*.ipynb"))
    if not notebook_files:
        print("No day-wise notebooks found in notebooks/!")
        return 1

    print("=" * 60)
    print(f"Starting Sequential Execution of {len(notebook_files)} Day Notebooks")
    print("=" * 60)

    results = []
    overall_success = True

    for nb_path in notebook_files:
        print(f"\n---> Running {nb_path.name} ... ", end="", flush=True)
        ok, elapsed, err = run_single_notebook(nb_path)
        if ok:
            print(f"PASSED ({elapsed}s)")
            results.append({"notebook": nb_path.name, "status": "PASSED", "time_sec": elapsed})
        else:
            print(f"FAILED ({elapsed}s)")
            print(err)
            results.append({"notebook": nb_path.name, "status": "FAILED", "time_sec": elapsed, "error": err})
            overall_success = False
            break  # Strict DAG requirement: halt if prerequisite day fails

    print("\n" + "=" * 60)
    print("Execution Summary:")
    print("=" * 60)
    for r in results:
        print(f"  {r['notebook']:<42} : {r['status']} ({r['time_sec']}s)")

    if overall_success:
        print("\nAll day-wise notebooks executed successfully with zero errors!")
        return 0
    else:
        print("\nExecution halted due to an error in a prerequisite notebook.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
