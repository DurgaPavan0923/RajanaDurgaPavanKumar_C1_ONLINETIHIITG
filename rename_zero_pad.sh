#!/usr/bin/env bash
# ==============================================================================
# Optional Script: Rename Day Folders to Zero-Padded Format (Day_01_Task_01)
# ==============================================================================
# CAUTION: Zero-padding deviates from the mandated naming convention (Day_X_Task_Y)
# required by TIH IIT Guwahati and will break portal checks unless all references,
# paths, and submissions are updated.
#
# This script is strictly OPTIONAL and OFF BY DEFAULT.
# To execute renames, explicitly invoke with: ./rename_zero_pad.sh --apply
# ==============================================================================

set -euo pipefail

APPLY=false
if [[ "${1:-}" == "--apply" ]]; then
    APPLY=true
fi

echo "=============================================================================="
echo "Zero-Padding Evaluation for Day_Wise_Tasks Folders"
echo "=============================================================================="

if [[ "$APPLY" != true ]]; then
    echo "[INFO] Running in DRY-RUN mode. No changes made."
    echo "[NOTICE] Zero-padding deviates from the programme-mandated naming convention (Day_X_Task_Y)."
    echo "[NOTICE] All portal rules require Day_1_Task_1 ... Day_28_Task_N without leading zeros."
    echo ""
    echo "To force rename anyway (at your own risk), run: ./rename_zero_pad.sh --apply"
    exit 0
fi

echo "[APPLYING] Executing git mv renames to Day_0X_Task_0Y format..."

cd Day_Wise_Tasks

for day in {1..9}; do
    for task in 1 2; do
        SRC="Day_${day}_Task_${task}"
        DST="Day_0${day}_Task_0${task}"
        if [[ -d "$SRC" ]]; then
            echo "git mv '$SRC' -> '$DST'"
            git mv "$SRC" "$DST"
        fi
    done
done

for day in {10..28}; do
    for task in 1 2; do
        SRC="Day_${day}_Task_${task}"
        DST="Day_${day}_Task_0${task}"
        if [[ -d "$SRC" ]]; then
            echo "git mv '$SRC' -> '$DST'"
            git mv "$SRC" "$DST"
        fi
    done
done

echo "=============================================================================="
echo "Renames applied. Please update all relative links and test paths."
echo "=============================================================================="
