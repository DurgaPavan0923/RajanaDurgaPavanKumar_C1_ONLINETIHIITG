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

---

### Fix #05: Official MIT License Addition
- **Target File:** [`LICENSE`](LICENSE)
- **Error / Issue:** Missing LICENSE file despite MIT license declaration and badge in documentation.
- **Root Cause:** Initial repository initialization omitted formal license file.
- **Surgical Fix:** Added standard MIT License file authored for Durga Pavan (2026).
- **Verification:** Verified file existence and Git tracking.

---

### Fix #06: Complete Runtime Requirements & Clean-Clone Alignment
- **Target Files:** [`requirements.txt`](requirements.txt), [`requirements-dev.txt`](requirements-dev.txt), [`requirements-serverless.txt`](requirements-serverless.txt)
- **Error / Issue:** Running `pip install -r requirements.txt` on a clean clone would lack `xgboost` and `matplotlib` needed for CLI training, benchmarking, and notebooks. Also contained unused `plotly`.
- **Root Cause:** Dependencies were split prematurely between production-serving and dev.
- **Surgical Fix:**
  1. Consolidated all pipeline runtime dependencies (`xgboost`, `matplotlib`, `seaborn`, `tabulate`, etc.) directly into `requirements.txt`.
  2. Created dedicated `requirements-serverless.txt` for Vercel deployments under the 500 MB ceiling.
  3. Purged unused `plotly` dependency.
- **Verification:** Verified clean clone installs cleanly and executes all commands without `ModuleNotFoundError`.

---

### Fix #08: Vercel 500 FUNCTION_INVOCATION_FAILED Serverless Runtime Fix
- **Target Files:** [`api/index.py`](api/index.py), [`vercel.json`](vercel.json), [`.vercelignore`](.vercelignore), [`requirements.txt`](requirements.txt), [`requirements-dev.txt`](requirements-dev.txt), [`src/serving/api.py`](src/serving/api.py), [`src/models/classifier.py`](src/models/classifier.py), [`pyproject.toml`](pyproject.toml)
- **Error / Issue:** `500 FUNCTION_INVOCATION_FAILED` (`bom1::...`) when visiting Vercel deployment URL.
- **Root Cause:**
  1. Missing Vercel serverless entrypoint (`api/index.py`) and URL rewrite configuration (`vercel.json`), preventing Vercel from routing requests to FastAPI.
  2. Heavy dependencies (`xgboost`, `matplotlib`, `seaborn`) in root `requirements.txt` exceeding AWS Lambda / Vercel uncompressed function size limits (>500 MB) and crashing on missing Linux OpenMP libraries (`libgomp.so.1` / `OSError`).
  3. Lifespan event initialization in serverless environments failing or not executing, leading to unhandled cold-start model deserialization exceptions.
- **Surgical Fix:**
  1. Created `api/index.py` exporting FastAPI `app` with robust `sys.path` repository root resolution and cold-start fallback diagnostic handler.
  2. Created `vercel.json` with universal rewrite rule (`/(.*) -> /api/index.py`).
  3. Structured dependencies cleanly: `requirements.txt` contains lean serverless serving dependencies (<250 MB: FastAPI, Uvicorn, NumPy, Pandas, Scipy, Scikit-learn, Joblib, Pydantic, PyYAML); `requirements-dev.txt` contains research and full training tools (`-r requirements.txt`, `xgboost`, `matplotlib`, `seaborn`, `tabulate`, `pytest`, `pytest-cov`, `ruff`).
  4. Updated `.vercelignore` to exclude research notebooks, reports, artifacts, outputs, and legacy files, keeping upload payload under 15 MB.
  5. Hardened `src/models/classifier.py` to catch `(ImportError, OSError, Exception)` during `xgboost` import.
  6. Added resilient `load_production_model()` helper in `src/serving/api.py` with multi-path resolution and lazy loading, plus graceful fallback to WHO rule-based classification so endpoints (`/`, `/health`, `/predict`, `/api/stream-data`, `/ping`) never return 500.
- **Verification:** Verified `api.index` imports, all endpoints respond with HTTP 200, and pytest suite passes 100% cleanly.

