#!/usr/bin/env bash
# ==============================================================================
# AquaGuard AI - Repository Cleanup Protocol
# Removes stale logs, ephemeral cache directories, obsolete migration scripts,
# and empty directories while safeguarding all referenced project assets.
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

# 1. Ephemeral Python Cache & Checkpoints
echo "[1/5] Purging Python bytecode caches, Jupyter checkpoints, and pytest cache..."
find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -path "./.venv" -prune -o -path "./.git" -prune -o -name "*.pyc" -delete 2>/dev/null || true

# 2. Ephemeral OS Artifacts
echo "[2/5] Removing OS metadata artifacts (.DS_Store, Thumbs.db)..."
find . -path "./.venv" -prune -o -path "./.git" -prune -o -name ".DS_Store" -delete 2>/dev/null || true
find . -path "./.venv" -prune -o -path "./.git" -prune -o -name "Thumbs.db" -delete 2>/dev/null || true

# 3. Stale Logs in outputs/logs/
echo "[3/5] Checking stale execution logs in outputs/logs/..."
if [[ "$MODE" == "dry-run" ]]; then
    git rm -n outputs/logs/*.log 2>/dev/null || echo "No tracked logs to remove."
else
    git rm -f outputs/logs/*.log 2>/dev/null || echo "No tracked logs to remove."
fi

# 4. Obsolete Migration Scratch Scripts (organize.*, restructure.*, MIGRATION.md, etc.)
echo "[4/5] Checking obsolete migration scratch scripts..."
OBSOLETE_SCRIPTS=("organize.ps1" "organize.sh" "restructure.ps1" "restructure.sh" "MIGRATION.md" "FIXES.md" "RUN_REPORT.md")
for scr in "${OBSOLETE_SCRIPTS[@]}"; do
    if [[ -f "$scr" ]]; then
        if [[ "$MODE" == "dry-run" ]]; then
            echo "[DRY-RUN] Candidate for removal: $scr (run with --apply to remove)"
            git rm -n "$scr" 2>/dev/null || true
        else
            echo "[APPLY] Removing obsolete migration artifact: $scr"
            git rm -f "$scr" 2>/dev/null || rm -f "$scr"
        fi
    fi
done

# 5. Empty Untracked Directories
echo "[5/5] Purging empty directories..."
EMPTY_DIRS=("docs" "experiments" "notebooks")
for ed in "${EMPTY_DIRS[@]}"; do
    if [[ -d "$ed" && ! "$(ls -A "$ed" 2>/dev/null)" ]]; then
        echo "Removing empty directory: $ed"
        rm -rf "$ed"
    fi
done

echo "=============================================================================="
if [[ "$MODE" == "dry-run" ]]; then
    echo "Dry-run complete. To apply changes, execute: ./cleanup.sh --apply"
else
    echo "Cleanup Protocol Complete."
fi
echo "=============================================================================="
