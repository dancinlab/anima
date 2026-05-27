#!/usr/bin/env bash
# SAVANT.md §12.5 path 1 — base-rate audit of all 27 verify_gz_*.py scripts.
# Runs each, captures stdout, prints a per-script summary line.

set -u
TECS_DIR="/Users/ghost/core/archive-TECS-L"
OUT_DIR="/Users/ghost/core/anima/state/savant_containment_audit_2026_05_14/raw_outputs"
mkdir -p "$OUT_DIR"

cd "$TECS_DIR" || exit 1

for f in verify/verify_gz_*.py; do
    base=$(basename "$f" .py)
    out_file="$OUT_DIR/$base.out"
    err_file="$OUT_DIR/$base.err"
    start=$(python3 -c "import time;print(time.time())")
    PYTHONPATH=. timeout 120 python3 "$f" >"$out_file" 2>"$err_file"
    rc=$?
    end=$(python3 -c "import time;print(time.time())")
    wall=$(python3 -c "print(f'{${end}-${start}:.2f}')")
    bytes=$(wc -c < "$out_file" | tr -d ' ')
    err_bytes=$(wc -c < "$err_file" | tr -d ' ')
    printf "%-50s  rc=%-3s  wall=%6ss  out=%8sB  err=%6sB\n" "$base" "$rc" "$wall" "$bytes" "$err_bytes"
done
