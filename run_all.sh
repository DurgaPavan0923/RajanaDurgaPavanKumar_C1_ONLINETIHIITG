#!/usr/bin/env bash
# ==============================================================================
# AquaGuard AI - Master Rerun Script
# ==============================================================================
set -euo pipefail

echo "Executing Master Verification Runner across Days 1 to 28..."
export MPLBACKEND="Agg"
python run_all.py
