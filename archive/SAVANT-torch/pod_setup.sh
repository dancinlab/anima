#!/usr/bin/env bash
# SAVANT torch-cuda lane — pod environment setup (run once per pod).
# Installs deps, builds the 5-lang euro corpus under /workspace (persistent).
set -euo pipefail

WS=/workspace/savant
mkdir -p "$WS"
cd "$WS"

echo "[setup] python deps ..."
pip install -q --no-input torch datasets huggingface_hub bitsandbytes 2>&1 | tail -3 || true

echo "[setup] nvidia-smi:"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader || true

# corpus build size is the first arg (MB per lang); default 80 = ~400MB total
MB_PER_LANG="${1:-80}"
echo "[setup] building 5-lang euro corpus mb_per_lang=$MB_PER_LANG ..."
python /workspace/savant/build_corpus_5lang_euro.py \
    --out "$WS/corpus_5lang.txt" --mb-per-lang "$MB_PER_LANG" --date 20231101 \
    2>&1 | tee "$WS/corpus_build.log"

echo "[setup] DONE. corpus at $WS/corpus_5lang.txt"
ls -la "$WS"
