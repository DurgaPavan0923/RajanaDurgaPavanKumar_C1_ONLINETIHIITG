"""Vercel Serverless Function entrypoint for AquaGuard AI FastAPI application."""

import os
import sys
from pathlib import Path

# Add project root and module directories to sys.path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent

for p in [ROOT_DIR, CURRENT_DIR, Path(os.getcwd())]:
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

try:
    from src.serving.api import app
except Exception as e:
    import traceback
    traceback.print_exc()
    # Diagnostic fallback app in case of fatal import errors during cold-start
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(title="AquaGuard AI Diagnostic")

    @app.api_route("/", methods=["GET", "POST", "PUT", "DELETE"])
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all_error(path_name: str = ""):
        return JSONResponse(
            status_code=500,
            content={
                "status": "initialization_error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "sys_path": sys.path[:6],
                "root_dir": str(ROOT_DIR),
                "cwd": os.getcwd(),
            },
        )

# Expose both app and handler for universal Vercel runtime discovery
handler = app
__all__ = ["app", "handler"]
