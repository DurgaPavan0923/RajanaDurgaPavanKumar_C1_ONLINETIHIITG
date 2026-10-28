#!/usr/bin/env bash
# ==============================================================================
# organize.sh: Idempotent script to consolidate Day_X_Task_Y folders into Day_Wise_Tasks/
# Candidate: Rajana Durga Pavan Kumar (Group C1, TIH IIT Guwahati)
# ==============================================================================
set -e

TARGET_DIR="Day_Wise_Tasks"
mkdir -p "$TARGET_DIR"

echo "Consolidating day folders into $TARGET_DIR/..."

for folder in Day_*_Task_*; do
    if [ -d "$folder" ] && [ "$folder" != "$TARGET_DIR" ]; then
        if [ -e "$TARGET_DIR/$folder" ]; then
            echo "Skipping (already exists in $TARGET_DIR): $folder"
        else
            echo "Moving $folder -> $TARGET_DIR/$folder"
            git mv "$folder" "$TARGET_DIR/$folder"
        fi
    fi
done

echo "Verifying contents of $TARGET_DIR/..."
count=$(ls -d "$TARGET_DIR"/Day_*_Task_* 2>/dev/null | wc -l || echo 0)
echo "Total task folders in $TARGET_DIR: $count"

echo "Checking for any missing Days 1 to 28..."
missing=0
for day in $(seq 1 28); do
    for task in 1 2; do
        expected="$TARGET_DIR/Day_${day}_Task_${task}"
        if [ ! -d "$expected" ]; then
            echo "MISSING: $expected"
            missing=$((missing + 1))
        fi
    done
done

if [ "$missing" -eq 0 ]; then
    echo "SUCCESS: All 56 Day_X_Task_Y folders across Days 1 to 28 are verified present."
else
    echo "WARNING: $missing folders are missing."
fi

echo "Repository structure at level 2:"
if command -v tree &>/dev/null; then
    tree -L 2 -d
else
    find . -maxdepth 2 -type d | sort
fi
