#!/usr/bin/env bash
# H100-side bootstrap: install deps, run F-SHIM-V5-4 DESIGN-1 fresh-init eval, write sentinel.
# Driven by orchestrator at state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/orchestrate.bash
set -uo pipefail

WORKDIR="/workspace/clm_v4_shim_v5_4_design_1"
RESULTS="$WORKDIR/results"
mkdir -p "$RESULTS"

LOG="$WORKDIR/run.log"
echo "[h100] $(date -u +%FT%TZ) starting F-SHIM-V5-4 DESIGN-1 eval (fresh-init, no best.pt)" | tee -a "$LOG"

cd "$WORKDIR" || exit 1

# 0) HF_TOKEN injected via env file by orchestrator stage 3.
if [ -z "${HF_TOKEN:-}" ]; then
    echo "[h100] FATAL: HF_TOKEN unset" | tee -a "$LOG"
    echo "FAIL_NO_HF_TOKEN" > "$RESULTS/COMPLETE.sentinel"
    exit 2
fi
echo "[h100] HF_TOKEN length=${#HF_TOKEN}b" | tee -a "$LOG"

# 1) deps
echo "[h100] $(date -u +%FT%TZ) installing python deps" | tee -a "$LOG"
pip install --quiet --no-input "lm-eval==0.4.11" "sentencepiece==0.2.0" "tqdm" 2>&1 | tee -a "$LOG" | tail -10

# 2) HF login (only needed for hellaswag dataset download, NOT best.pt — fresh init).
echo "[h100] $(date -u +%FT%TZ) HF login" | tee -a "$LOG"
python - <<'PY' 2>&1 | tee -a "$LOG"
import os
from huggingface_hub import login
login(token=os.environ["HF_TOKEN"])
print("HF login OK")
PY

# 3) Set up legacy decoder import path.
EVAL_PY="$WORKDIR/clm_v4_shim_v5_4_design_1_eval.py"
DECODER_DIR="$WORKDIR/legacy_decoder"
mkdir -p "$DECODER_DIR"

# Orchestrator scp'd decoder_v3.py + conscious_decoder.py + tokenizer
if [ -f "$WORKDIR/decoder_v3.py" ] && [ ! -f "$DECODER_DIR/decoder_v3.py" ]; then
    cp "$WORKDIR/decoder_v3.py" "$DECODER_DIR/decoder_v3.py"
    echo "[h100] copied decoder_v3.py to $DECODER_DIR/" | tee -a "$LOG"
fi
if [ -f "$WORKDIR/conscious_decoder.py" ] && [ ! -f "$DECODER_DIR/conscious_decoder.py" ]; then
    cp "$WORKDIR/conscious_decoder.py" "$DECODER_DIR/conscious_decoder.py"
    echo "[h100] copied conscious_decoder.py to $DECODER_DIR/" | tee -a "$LOG"
fi
if [ ! -f "$DECODER_DIR/decoder_v3.py" ]; then
    echo "[h100] FATAL: legacy_decoder/decoder_v3.py missing — orchestrator must scp it" | tee -a "$LOG"
    ls -la "$WORKDIR" "$DECODER_DIR" | tee -a "$LOG"
    echo "FAIL_NO_DECODER" > "$RESULTS/COMPLETE.sentinel"
    exit 4
fi

# Patch relative-imports in decoder_v3.py to absolute (legacy_decoder is loaded
# as top-level via sys.path.insert in eval py — the .conscious_decoder relative
# form fails since the dir is not a package context). Mirror anima_clm_v4_shim.py
# convention which adds the legacy dir to sys.path and uses absolute imports.
# raw#15: this is a per-deployment patch on the H100 COPY, not the upstream source.
sed -i 's|^from \.conscious_decoder import|from conscious_decoder import|g' "$DECODER_DIR/decoder_v3.py"
echo "[h100] patched relative imports in $DECODER_DIR/decoder_v3.py:" | tee -a "$LOG"
grep -n "from conscious_decoder" "$DECODER_DIR/decoder_v3.py" | tee -a "$LOG"

# Tokenizer location check
TOK_PATH="$WORKDIR/tokenizer_64k_multilingual.model"
if [ ! -f "$TOK_PATH" ]; then
    echo "[h100] FATAL: tokenizer missing at $TOK_PATH" | tee -a "$LOG"
    echo "FAIL_NO_TOKENIZER" > "$RESULTS/COMPLETE.sentinel"
    exit 5
fi
echo "[h100] tokenizer=$TOK_PATH" | tee -a "$LOG"

# 4) run eval
echo "[h100] $(date -u +%FT%TZ) running DESIGN-1 eval (4 passes: v4_NF v4_RF v5_NF v5_RF)" | tee -a "$LOG"
cd "$WORKDIR"
export CLM_V4_DEVICE=cuda
python "$EVAL_PY" \
    --limit 200 \
    --num-fewshot 5 \
    --seed 42 \
    --init-seed 1234 \
    --fixture-path "$WORKDIR/train_avg_real.pt" \
    --outdir "$RESULTS" \
    2>&1 | tee -a "$LOG"
RC=$?

if [ $RC -ne 0 ]; then
    echo "[h100] $(date -u +%FT%TZ) eval FAILED rc=$RC" | tee -a "$LOG"
    if [ ! -f "$RESULTS/COMPLETE.sentinel" ]; then
        echo "FAIL_EVAL_RC_$RC" > "$RESULTS/COMPLETE.sentinel"
    fi
    exit $RC
fi

# 5) sentinel
if [ ! -f "$RESULTS/COMPLETE.sentinel" ]; then
    echo "$(date -u +%FT%TZ)" > "$RESULTS/COMPLETE.sentinel"
fi
echo "[h100] $(date -u +%FT%TZ) DONE; sentinel=$RESULTS/COMPLETE.sentinel" | tee -a "$LOG"
exit 0
