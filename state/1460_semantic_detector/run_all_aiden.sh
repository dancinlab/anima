#!/usr/bin/env bash
# H_1460 — decode + dual-detector re-score for every available G6 ckpt on aiden GPU.
# Runs base + each trained lens; writes one combined log. $0 pool GPU (a_engine_native_learning
# DIRECTIONAL: torch-mouth decode — engine-native follow-on registered).
set -u
cd ~/h1460_g6 || exit 1
export H1456_PROBES="$PWD/probes" G6_PROBES="$PWD/probes"
OUT=out/h1460_dual_rescore.log
: > "$OUT"
for pair in "BASE:ckpt/base.pt" \
            "H1441_CONTRASTIVE:ckpt/h1441_contrastive.pt" \
            "H1441_SHUFFLE_CTRL:ckpt/h1441_shuffle.pt"; do
    label="${pair%%:*}"; ckpt="${pair##*:}"
    if [ ! -f "$ckpt" ]; then
        echo "[skip] $label — $ckpt MISSING" | tee -a "$OUT"; continue
    fi
    echo "######## $label ($ckpt) ########" | tee -a "$OUT"
    python3 rescore_dual.py --decode "$ckpt" --label "$label" 2>&1 | tee -a "$OUT"
done
echo "ALL_DONE" | tee -a "$OUT"
