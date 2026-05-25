#!/usr/bin/env bash
# H100-side bootstrap: install deps, run OPT-C eval, write sentinel.
# Driven by the orchestrator at state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05/orchestrate.bash
set -uo pipefail

WORKDIR="/workspace/clm_v4_shim_v5_opt_c"
RESULTS="$WORKDIR/results"
mkdir -p "$RESULTS"

LOG="$WORKDIR/run.log"
echo "[h100] $(date -u +%FT%TZ) starting OPT-C eval" | tee -a "$LOG"

cd "$WORKDIR" || exit 1

# 0) HF_TOKEN already injected via env file by orchestrator stage 3.
if [ -z "${HF_TOKEN:-}" ]; then
    echo "[h100] FATAL: HF_TOKEN unset" | tee -a "$LOG"
    echo "FAIL_NO_HF_TOKEN" > "$RESULTS/COMPLETE.sentinel"
    exit 2
fi
echo "[h100] HF_TOKEN length=${#HF_TOKEN}b" | tee -a "$LOG"

# 1) deps
echo "[h100] $(date -u +%FT%TZ) installing python deps" | tee -a "$LOG"
pip install --quiet --no-input "lm-eval==0.4.11" "sentencepiece==0.2.0" "tqdm" 2>&1 | tee -a "$LOG" | tail -10
# transformers + torch should be in the pytorch image already

# 2) HF login + warm up base mirror cache via hf-cli
echo "[h100] $(date -u +%FT%TZ) HF login + cache warm" | tee -a "$LOG"
python - <<'PY' 2>&1 | tee -a "$LOG"
import os
from huggingface_hub import snapshot_download, login
login(token=os.environ["HF_TOKEN"])
p = snapshot_download(
    repo_id="need-singularity/clm-v4-base-mirror",
    revision="856278beb59c5b39f16485cc8f3a46dcdaf9d1e3",
    allow_patterns=["best.pt"],
    cache_dir=os.path.expanduser("~/.cache/huggingface/hub"),
)
print("snapshot_dir=", p)
PY

# 3) tokenizer download (need-singularity/clm-v4-base-mirror has no tokenizer file at that revision;
# fall back to mirror at separate dataset path used in baseline_eval) — workaround: clone the
# tokenizer file from the mirror's separate dataset OR locate it in the snapshot dir.
echo "[h100] $(date -u +%FT%TZ) locating tokenizer" | tee -a "$LOG"
SNAP=$(find ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror -type d -name "856278be*" 2>/dev/null | head -1)
echo "[h100] snapshot dir: $SNAP" | tee -a "$LOG"
ls -la "$SNAP" 2>&1 | tee -a "$LOG" || true

# Tokenizer comes from p9_path_b_sanity_probe_v2 — also published as part of the mirror
# Prefer the orchestrator-supplied tokenizer (scp'd into WORKDIR) — most reliable path.
# Falls back to snapshot dir, then a full-mirror snapshot pull, before failing.
TOK_PATH=""
if [ -f "$WORKDIR/tokenizer_64k_multilingual.model" ]; then
    TOK_PATH="$WORKDIR/tokenizer_64k_multilingual.model"
    echo "[h100] using orchestrator-supplied tokenizer: $TOK_PATH" | tee -a "$LOG"
fi
if [ -z "$TOK_PATH" ]; then
    for cand in "$SNAP/tokenizer_64k_multilingual.model" "$SNAP/tokenizer.model"; do
        if [ -f "$cand" ]; then TOK_PATH="$cand"; break; fi
    done
fi
if [ -z "$TOK_PATH" ]; then
    echo "[h100] tokenizer not in snapshot — pulling full mirror" | tee -a "$LOG"
    python - <<'PY' 2>&1 | tee -a "$LOG"
import os
from huggingface_hub import snapshot_download
p = snapshot_download(
    repo_id="need-singularity/clm-v4-base-mirror",
    revision="856278beb59c5b39f16485cc8f3a46dcdaf9d1e3",
    cache_dir=os.path.expanduser("~/.cache/huggingface/hub"),
)
print("full_snapshot_dir=", p)
import os
for f in sorted(os.listdir(p)):
    print("  ", f, os.path.getsize(os.path.join(p, f)))
PY
    SNAP=$(find ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror -type d -name "856278be*" | head -1)
    for cand in "$SNAP/tokenizer_64k_multilingual.model" "$SNAP/tokenizer.model"; do
        if [ -f "$cand" ]; then TOK_PATH="$cand"; break; fi
    done
fi

if [ -z "$TOK_PATH" ]; then
    echo "[h100] FATAL: tokenizer not found anywhere (orchestrator-supplied, snapshot, full mirror all empty)" | tee -a "$LOG"
    ls -la "$WORKDIR" | tee -a "$LOG"
    ls -la "$SNAP" | tee -a "$LOG"
    echo "FAIL_NO_TOKENIZER" > "$RESULTS/COMPLETE.sentinel"
    exit 3
fi
echo "[h100] tokenizer=$TOK_PATH" | tee -a "$LOG"

# 4) Set up legacy decoder_v2 import path (script expects /home/aiden/anima/...; H100 differs).
#    We patch the script in-place to use BASE_PATH = $SNAP/best.pt and TOKENIZER_PATH = $TOK_PATH.
EVAL_PY="$WORKDIR/clm_v4_shim_v5_opt_c_eval.py"
DECODER_DIR="$WORKDIR/legacy_decoder"
mkdir -p "$DECODER_DIR"

# Orchestrator scp'd conscious_decoder.py + tokenizer_64k_multilingual.model from Mac
# (state/p9_base_validation_h100_2026_05_04/clm_v4_hf/) into /workspace/clm_v4_shim_v5_opt_c/
# We move conscious_decoder.py into legacy_decoder/ and use the tokenizer as TOK_PATH.
if [ -f "$WORKDIR/conscious_decoder.py" ] && [ ! -f "$DECODER_DIR/conscious_decoder.py" ]; then
    cp "$WORKDIR/conscious_decoder.py" "$DECODER_DIR/conscious_decoder.py"
    echo "[h100] copied conscious_decoder.py to $DECODER_DIR/" | tee -a "$LOG"
fi
if [ ! -f "$DECODER_DIR/conscious_decoder.py" ]; then
    echo "[h100] FATAL: legacy_decoder/conscious_decoder.py missing — orchestrator must scp it" | tee -a "$LOG"
    ls -la "$WORKDIR" "$DECODER_DIR" | tee -a "$LOG"
    echo "FAIL_NO_DECODER" > "$RESULTS/COMPLETE.sentinel"
    exit 4
fi
# Patch eval script: replace anima imports with H100 layout
sed -i \
    -e "s|/home/aiden/anima/anima/core|$DECODER_DIR|g" \
    -e "s|/home/aiden/anima/models|$DECODER_DIR|g" \
    -e "s|BASE_PATH = .*|BASE_PATH = '$SNAP/best.pt'|g" \
    -e "s|TOKENIZER_PATH = .*|TOKENIZER_PATH = '$TOK_PATH'|g" \
    "$EVAL_PY"
echo "[h100] eval script patched — head check:" | tee -a "$LOG"
grep -E "^(BASE_PATH|TOKENIZER_PATH|sys.path)" "$EVAL_PY" | tee -a "$LOG"

# 5) run eval
echo "[h100] $(date -u +%FT%TZ) running OPT-C eval (pass A no-fixture, pass B with-fixture)" | tee -a "$LOG"
cd "$WORKDIR"
export CLM_V4_DEVICE=cuda
python "$EVAL_PY" \
    --limit 200 \
    --num-fewshot 5 \
    --seed 42 \
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

# 6) sentinel
if [ ! -f "$RESULTS/COMPLETE.sentinel" ]; then
    echo "$(date -u +%FT%TZ)" > "$RESULTS/COMPLETE.sentinel"
fi
echo "[h100] $(date -u +%FT%TZ) DONE; sentinel=$RESULTS/COMPLETE.sentinel" | tee -a "$LOG"
exit 0
