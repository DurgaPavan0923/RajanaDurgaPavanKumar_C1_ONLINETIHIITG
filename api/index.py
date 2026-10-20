"""Vercel Serverless Function entrypoint for AquaGuard AI FastAPI application."""

import json
import os
import sys
import traceback
from pathlib import Path
from urllib.parse import parse_qs, urlencode

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
    """Universal ASGI handler with path resolution and diagnostics."""
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

    if scope.get("type") == "http":
        # 1. Resolve path from query string parameter injected by Vercel rewrite
        qs = scope.get("query_string", b"").decode("utf-8")
        if "__orig_path=" in qs:
            params = parse_qs(qs, keep_blank_values=True)
            if "__orig_path" in params and params["__orig_path"]:
                orig = params.pop("__orig_path")[0]
                if not orig.startswith("/"):
                    orig = "/" + orig
                while "//" in orig:
                    orig = orig.replace("//", "/")
                scope["path"] = orig
                scope["raw_path"] = orig.encode("utf-8")
                remaining_qs = urlencode([(k, v) for k, vals in params.items() for v in vals])
                scope["query_string"] = remaining_qs.encode("utf-8")

        # 2. Fallback to matched path headers or root if path is /api/index.py
        if scope.get("path") in ("/api/index.py", "/api/index"):
            scope["path"] = "/"
            scope["raw_path"] = b"/"

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
