#!/usr/bin/env bash
# ==============================================================================
# AquaGuard AI: Idempotent Day-Wise Restructuring Shell Script
# Candidate: Rajana Durga Pavan Kumar (Group C1, TIH IIT Guwahati)
# Target Repo: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
# ==============================================================================
set -e

echo "Starting repository migration to Day_X_Task_Y structure..."

# Run python migration script to handle git-safe moves and README creation
if command -v python3 &>/dev/null; then
    python3 scripts/restructure_repo.py
elif command -v python &>/dev/null; then
    python scripts/restructure_repo.py
else
    echo "Python interpreter not found!"
    exit 1
fi

# Ensure all Day_X_Task_Y folders have a README.md
python scripts/generate_task_readmes.py

echo "Validating git status..."
git status -s

echo "Restructuring completed successfully!"
