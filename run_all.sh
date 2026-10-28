#!/usr/bin/env bash
# ==============================================================================
# run_all.sh: Master script to execute all 28 days of tasks in order
# ==============================================================================
set -e

echo "Starting master rerun across all 28 days..."
python run_all.py

echo "Master rerun completed successfully!"
