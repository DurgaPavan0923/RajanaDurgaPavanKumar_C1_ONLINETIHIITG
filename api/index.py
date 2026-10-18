"""Vercel Serverless Function entrypoint for AquaGuard AI FastAPI application."""

import sys
from pathlib import Path

# Add project root directory to sys.path so 'src' and root modules are discoverable in Vercel Lambda
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from src.serving.api import app
except Exception as e:
    # Diagnostic fallback app in case of fatal import errors during cold-start
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(title="AquaGuard AI Diagnostic")

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all_error(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "status": "initialization_error",
                "error": str(e),
                "sys_path": sys.path[:5],
                "root_dir": str(ROOT_DIR),
            },
        )

__all__ = ["app"]
