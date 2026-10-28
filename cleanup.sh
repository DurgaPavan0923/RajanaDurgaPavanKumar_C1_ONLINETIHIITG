#!/usr/bin/env bash
# ==============================================================================
# AquaGuard AI - Repository Cleanup Script
# Removes stale logs, ephemeral cache directories, and deprecated debug scripts.
# ==============================================================================

set -euo pipefail

echo "=============================================================================="
echo "AquaGuard AI Repository Cleanup Protocol"
echo "=============================================================================="

# 1. Stale Logs Cleanup in outputs/logs/
echo "[1/4] Removing stale execution logs from git tracking..."
git rm -f outputs/logs/*.log 2>/dev/null || true

# 2. Ephemeral Python Cache & Checkpoints
echo "[2/4] Purging Python bytecode caches and Jupyter checkpoints..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# 3. Ephemeral OS Artifacts
echo "[3/4] Removing OS metadata artifacts (.DS_Store, Thumbs.db)..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true

# 4. Git status check
echo "[4/4] Verifying cleaned working tree..."
git status -s

echo "=============================================================================="
echo "Cleanup Protocol Complete."
echo "=============================================================================="
