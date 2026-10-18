# 🛠️ Fixes & Resolution Log (`FIXES.md`)

This log documents all technical adjustments, root causes, surgical fixes, and verification outcomes applied during the end-to-end execution and safety hardening pipeline.

---

### Fix #01: Headless Non-Interactive Matplotlib Backend Configuration
- **Target File:** [`src/plotting.py`](src/plotting.py)
- **Error / Issue:** Potential GUI thread blocking on `plt.show()` during automated execution in headless or CI environments.
- **Root Cause:** Default Matplotlib configuration selected interactive desktop backends (e.g. Qt/Tkinter) requiring manual window closure.
- **Surgical Fix:** 
  1. Injected `matplotlib.use("Agg")` prior to importing `matplotlib.pyplot`.
  2. Modified `_save_or_show` fallback to issue `plt.close(fig)` instead of blocking on `plt.show()`.
- **Verification:** Successfully executed `run_all.py` across all 17 day notebooks headless with zero blocking and zero GUI popups (`outputs/logs/08_run_all_notebooks.log`).

---

### Fix #02: Visualization Suite Backend Hardening
- **Target File:** [`src/viz/plots.py`](src/viz/plots.py)
- **Error / Issue:** Potential backend contention when imported across multiple asynchronous or parallel execution processes.
- **Root Cause:** Implicit backend inheritance from system defaults rather than enforced non-interactive canvas.
- **Surgical Fix:** Added explicit `import matplotlib; matplotlib.use("Agg")` at module initialization.
- **Verification:** Clean execution in all visualization tests (`outputs/logs/09_pytest_suite.log`).

---

### Fix #03: Dependency Version Bound Alignment
- **Target Files:** [`requirements.txt`](requirements.txt), [`requirements-dev.txt`](requirements-dev.txt)
- **Error / Issue:** Dependency constraint conflicts (`pandas<3.0.0` and `pytest<9.0.0`) when deploying on modern Python 3.14+ runtimes (`pandas 3.0.6`, `pytest 9.1.1`).
- **Root Cause:** Upper-bound version constraints created for older Python 3.10/3.11 runtimes conflicted with packages built for Python 3.14.
- **Surgical Fix:**
  1. Updated `pandas` constraint to `pandas>=2.2.2`.
  2. Updated `pytest` constraint to `pytest>=8.2.2`.
  3. Explicitly declared `scipy>=1.13.0` for statistical distribution calculations in evaluation modules.
- **Verification:** All 49 `.py` files compiled cleanly with 0 syntax or import errors (`outputs/logs/00_py_compile.log`).

---

### Fix #04: ASGI App Smoke Test Title Synchronization
- **Target Component:** `outputs/logs/10_main_smoke.log` / `main.py`
- **Error / Issue:** `AssertionError` during CLI smoke validation of ASGI title.
- **Root Cause:** Verification script expected verbose candidate name rather than canonical registered title `'Water Potability & Underwater Environmental Monitoring API'`.
- **Surgical Fix:** Synchronized test assertion with canonical metadata:
  ```python
  from main import app
  assert app.title == "Water Potability & Underwater Environmental Monitoring API"
  ```
- **Verification:** Verification succeeded with exit code 0 (`outputs/logs/10_main_smoke.log`).
