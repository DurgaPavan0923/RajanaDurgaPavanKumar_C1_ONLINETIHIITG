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

_init_error = None
try:
    from src.serving.api import app as fastapi_app
    fastapi_app.debug = True
except BaseException as e:
    _init_error = traceback.format_exc()
    fastapi_app = None


async def app(scope, receive, send):
    """Universal ASGI handler with full error diagnostics for serverless runtime."""
    if _init_error is not None:
        if scope.get("type") == "http":
            body = (
                f"AquaGuard AI - Cold Start Initialization Error\n\n"
                f"Traceback:\n{_init_error}\n\n"
                f"sys.path: {sys.path[:6]}\n"
                f"ROOT_DIR: {ROOT_DIR}\n"
                f"CWD: {os.getcwd()}\n"
            ).encode("utf-8")
            await send(
                {
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [
                        [b"content-type", b"text/plain; charset=utf-8"],
                        [b"content-length", str(len(body)).encode("utf-8")],
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
        return

    try:
        await fastapi_app(scope, receive, send)
    except BaseException as exc:
        tb = traceback.format_exc()
        if scope.get("type") == "http":
            body = (
                f"AquaGuard AI - Runtime Invocation Error: {exc}\n\n"
                f"Traceback:\n{tb}\n"
            ).encode("utf-8")
            await send(
                {
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [
                        [b"content-type", b"text/plain; charset=utf-8"],
                        [b"content-length", str(len(body)).encode("utf-8")],
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
        else:
            raise exc


handler = app
__all__ = ["app", "handler"]
