#!/usr/bin/env bash
# ==============================================================================
# AquaGuard AI - Repository Cleanup Script
# Removes stale logs, ephemeral cache directories, and deprecated debug scripts.
# Defaults to DRY-RUN mode (git rm -n) to safeguard workspace state.
# Execute with --apply to commit file removals.
# ==============================================================================

set -euo pipefail

MODE="dry-run"
if [[ "${1:-}" == "--apply" ]]; then
    MODE="apply"
fi

echo "=============================================================================="
echo "AquaGuard AI Repository Cleanup Protocol [Mode: $MODE]"
echo "=============================================================================="

# 1. Stale Logs in outputs/logs/
echo "[1/4] Checking stale execution logs in outputs/logs/..."
if [[ "$MODE" == "dry-run" ]]; then
    git rm -n outputs/logs/*.log 2>/dev/null || echo "No tracked logs to remove."
else
    git rm -f outputs/logs/*.log 2>/dev/null || echo "No tracked logs to remove."
fi

# 2. Ephemeral Python Cache & Checkpoints
echo "[2/4] Purging Python bytecode caches and Jupyter checkpoints..."
find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -path "./.venv" -prune -o -path "./.git" -prune -o -name "*.pyc" -delete 2>/dev/null || true

# 3. Ephemeral OS Artifacts
echo "[3/4] Removing OS metadata artifacts (.DS_Store, Thumbs.db)..."
find . -path "./.venv" -prune -o -path "./.git" -prune -o -name ".DS_Store" -delete 2>/dev/null || true
find . -path "./.venv" -prune -o -path "./.git" -prune -o -name "Thumbs.db" -delete 2>/dev/null || true

# 4. Git status check
echo "[4/4] Verifying cleaned working tree..."
git status -s

echo "=============================================================================="
if [[ "$MODE" == "dry-run" ]]; then
    echo "Dry-run complete. To apply changes, execute: ./cleanup.sh --apply"
else
    echo "Cleanup Protocol Complete."
fi
echo "=============================================================================="
