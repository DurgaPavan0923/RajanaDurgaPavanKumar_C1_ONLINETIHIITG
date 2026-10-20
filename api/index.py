"""Vercel Serverless Function entrypoint for AquaGuard AI FastAPI application."""

import json
import os
import sys
import traceback
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
except BaseException as e:
    _init_error = traceback.format_exc()

    async def fallback_asgi_app(scope, receive, send):
        if scope["type"] == "http":
            body = json.dumps(
                {
                    "status": "initialization_error",
                    "error": str(e),
                    "traceback": _init_error,
                    "sys_path": sys.path[:10],
                    "root_dir": str(ROOT_DIR),
                    "cwd": os.getcwd(),
                    "files_in_root": os.listdir(ROOT_DIR) if ROOT_DIR.exists() else [],
                    "files_in_current": os.listdir(CURRENT_DIR) if CURRENT_DIR.exists() else [],
                },
                indent=2,
            ).encode("utf-8")
            await send(
                {
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [
                        [b"content-type", b"application/json"],
                        [b"content-length", str(len(body)).encode("utf-8")],
                    ],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": body,
                }
            )

    app = fallback_asgi_app

handler = app
__all__ = ["app", "handler"]
