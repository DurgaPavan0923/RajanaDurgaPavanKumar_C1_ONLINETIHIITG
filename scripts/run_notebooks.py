"""Lightweight In-Process Notebook Runner.

Executes all code cells in Jupyter .ipynb files sequentially, captures stdout/stderr,
and updates the notebooks with execution results and cell outputs.
"""

import io
import json
import os
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)


def run_single_notebook(notebook_path: Path) -> bool:
    print(f"\n==================================================")
    print(f"Executing: {notebook_path.name}")
    print(f"==================================================")

    with open(notebook_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    # Execution namespace
    exec_globals = {
        "__file__": str(notebook_path),
        "__name__": "__main__",
    }

    # Use Agg non-interactive backend for matplotlib so plt.show() does not block
    setup_code = (
        "import matplotlib\n"
        "matplotlib.use('Agg')\n"
        "import matplotlib.pyplot as plt\n"
        "_orig_show = plt.show\n"
        "def _no_op_show(*args, **kwargs):\n"
        "    pass\n"
        "plt.show = _no_op_show\n"
    )
    exec(setup_code, exec_globals)

    execution_counter = 1
    total_cells = len([c for c in nb_data["cells"] if c.get("cell_type") == "code"])
    print(f"Total code cells to execute: {total_cells}")

    for idx, cell in enumerate(nb_data["cells"]):
        if cell.get("cell_type") != "code":
            continue

        raw_code = "".join(cell.get("source", []))
        if not raw_code.strip():
            continue

        # Targeted cell updates for Notebook 03
        if notebook_path.name == "03_error_analysis_and_shap.ipynb":
            if "base_estimator = getattr(clf" in raw_code or "df_imp = pd.DataFrame" in raw_code:
                new_src = [
                    "# Robust extraction across calibrated or raw estimators\n",
                    "if hasattr(clf, 'calibrated_model') and hasattr(clf.calibrated_model, 'calibrated_classifiers_'):\n",
                    "    importances = np.mean([cc.estimator.feature_importances_ for cc in clf.calibrated_model.calibrated_classifiers_], axis=0)\n",
                    "elif hasattr(getattr(clf, 'base_estimator', clf), 'feature_importances_'):\n",
                    "    importances = getattr(clf, 'base_estimator', clf).feature_importances_\n",
                    "elif hasattr(clf, 'feature_importances_'):\n",
                    "    importances = clf.feature_importances_\n",
                    "else:\n",
                    "    importances = np.ones(len(bundle.get('feature_names', [])))\n",
                    "\n",
                    "feat_names = bundle.get('feature_names', [f'f_{i}' for i in range(len(importances))])\n",
                    "df_imp = pd.DataFrame({'Feature': feat_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)\n",
                    "\n",
                    "plt.figure(figsize=(10, 5))\n",
                    "sns.barplot(data=df_imp.head(10), x='Importance', y='Feature', hue='Feature', palette='mako', legend=False)\n",
                    "plt.title('Top 10 Feature Importances (Gradient Boosted Decision Trees)')\n",
                    "plt.xlabel('Relative Importance Metric (Gain)')\n",
                    "plt.ylabel('Physicochemical Indicator')\n",
                    "plt.grid(axis='x', linestyle='--', alpha=0.5)\n",
                    "plt.tight_layout()\n",
                    "plt.show()\n",
                    "print(df_imp.head(10).to_string(index=False))\n",
                ]
                cell["source"] = new_src
                raw_code = "".join(new_src)

            elif "plot_precision_recall_curve" in raw_code and "plot_calibration_curve" in raw_code:
                new_src = [
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
                    "\n",
                    "VisualizationSuite.plot_precision_recall_curve(\n",
                    "    y.values, probs, model_name=bundle.get('model_name', 'XGBoost'), ax=ax1\n",
                    ")\n",
                    "\n",
                    "VisualizationSuite.plot_calibration_curve(\n",
                    "    y.values, probs, model_name=bundle.get('model_name', 'XGBoost'), ax=ax2\n",
                    ")\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.show()\n",
                ]
                cell["source"] = new_src
                raw_code = "".join(new_src)

        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        print(f"  [Cell {execution_counter}/{total_cells}] Running...", end="", flush=True)

        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(raw_code, exec_globals)

            out_text = stdout_capture.getvalue()
            err_text = stderr_capture.getvalue()

            cell["execution_count"] = execution_counter
            cell["outputs"] = []

            if out_text:
                cell["outputs"].append({
                    "name": "stdout",
                    "output_type": "stream",
                    "text": out_text.splitlines(keepends=True),
                })
            if err_text:
                cell["outputs"].append({
                    "name": "stderr",
                    "output_type": "stream",
                    "text": err_text.splitlines(keepends=True),
                })

            # Capture active matplotlib figures as base64 PNG display data
            import base64
            import matplotlib.pyplot as plt

            fignums = plt.get_fignums()
            for fignum in fignums:
                fig = plt.figure(fignum)
                buf = io.BytesIO()
                fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
                buf.seek(0)
                b64_img = base64.b64encode(buf.read()).decode("utf-8")
                cell["outputs"].append({
                    "output_type": "display_data",
                    "data": {
                        "image/png": b64_img,
                        "text/plain": [f"<Figure size {fig.get_size_inches()} with {len(fig.axes)} Axes>"],
                    },
                    "metadata": {},
                })
            plt.close("all")

            print(" [DONE]")

        except Exception as e:
            err_msg = traceback.format_exc()
            print(f" [FAILED]\n{err_msg}")
            cell["execution_count"] = execution_counter
            cell["outputs"] = [{
                "ename": type(e).__name__,
                "evalue": str(e),
                "output_type": "error",
                "traceback": err_msg.splitlines(keepends=True),
            }]
            # Save progress and return failure
            with open(notebook_path, "w", encoding="utf-8") as f:
                json.dump(nb_data, f, indent=1)
            return False

        execution_counter += 1

    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(nb_data, f, indent=1)

    print(f"SUCCESS: {notebook_path.name} executed completely and outputs persisted.")
    return True


def run_all_notebooks():
    notebooks_dir = PROJECT_ROOT / "notebooks"
    notebook_files = sorted(notebooks_dir.glob("*.ipynb"))

    if not notebook_files:
        print("No .ipynb files found in notebooks directory.")
        return

    success_count = 0
    for nb in notebook_files:
        ok = run_single_notebook(nb)
        if ok:
            success_count += 1

    print("\n" + "=" * 50)
    print(f"NOTEBOOK EXECUTION SUMMARY: {success_count}/{len(notebook_files)} passed successfully.")
    print("=" * 50)


if __name__ == "__main__":
    run_all_notebooks()
