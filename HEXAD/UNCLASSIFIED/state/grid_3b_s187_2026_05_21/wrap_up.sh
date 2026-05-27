#!/bin/bash
# Pull eval results from ubu-1 → Mac, generate report, commit + push.
set -e
WORK_DIR=/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21
EVAL_OUT_DIR=$WORK_DIR/eval_out
mkdir -p "$EVAL_OUT_DIR"

echo "[wrap_up] pulling eval JSONs from ubu-1 ..."
rsync -av aiden@192.168.50.119:~/s187_eval/out/ "$EVAL_OUT_DIR/"
ls -la "$EVAL_OUT_DIR/"

echo "[wrap_up] regenerating report ..."
cd "$WORK_DIR"
python3 write_report.py

echo "[wrap_up] EVAL_REPORT.md generated ($(wc -l < EVAL_REPORT.md) lines)"
ls -la EVAL_REPORT.md
