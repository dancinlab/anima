#!/usr/bin/env bash
# run_lane_p_3b_fire.sh — Lane P ~3B ENGINE GPU fire glue (on-pod).
#  substrate = GPU-torch (Lane P) · H100 sm_90. NOT Lane G (forge).
#  Builds the scaled wiki corpus, trains the 3.07B CLMConvMoE (d4096 L30 E30),
#  emits result JSON + periodic ckpt/.clm (a_fire_recover_complete).
#
#  ENV (override as needed):
#    REPO_DIR   default ~/anima   (git checkout of origin/main with Stage0+1 landed)
#    WORK       default ~/lanep_3b
#    BYTES_LANG default 250000000 (250MB/lang × 12 = ~3GB clean corpus)
#    STEPS      default 24000
#    SEQ        default 512
#    BATCH      default 8
#    ACCUM      default 4   (effective batch 32 × 512 = 16384 tok/step)
set -uo pipefail

REPO_DIR="${REPO_DIR:-$HOME/anima}"
WORK="${WORK:-$HOME/lanep_3b}"
BYTES_LANG="${BYTES_LANG:-250000000}"
STEPS="${STEPS:-24000}"
SEQ="${SEQ:-512}"
BATCH="${BATCH:-8}"
ACCUM="${ACCUM:-4}"
WARMUP="${WARMUP:-500}"
LOG_EVERY="${LOG_EVERY:-100}"
CKPT_EVERY="${CKPT_EVERY:-2000}"
LANGS="${LANGS:-en,zh,ru,ja,ko,de,fr,es,it,pt,nl,pl}"

mkdir -p "$WORK"
echo "[fire] $(date -u) REPO_DIR=$REPO_DIR WORK=$WORK bytes/lang=$BYTES_LANG steps=$STEPS"

# 0) env — torch (CUDA) + corpus deps. Pod image usually ships torch; ensure deps.
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())" \
  || pip install -q torch
python3 -c "import pyarrow, huggingface_hub" 2>/dev/null \
  || pip install -q pyarrow huggingface_hub

nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv,noheader || true

# 1) repo @ origin/main (Stage0+1 landed). Refresh if present.
if [ -d "$REPO_DIR/.git" ]; then
  git -C "$REPO_DIR" fetch origin -q && git -C "$REPO_DIR" checkout -q origin/main 2>/dev/null || true
else
  git clone -q https://github.com/dancinlab/anima "$REPO_DIR"
fi
echo "[fire] repo HEAD=$(git -C "$REPO_DIR" rev-parse --short HEAD)"

CORPUS="$WORK/wiki_3b.txt"
# 2) build the scaled clean corpus. Build to a .partial then atomic-rename so an
#    interrupted build never leaves a truncated CORPUS the trainer would read
#    (the prior run died mid-build leaving a 0-byte corpus -> root-cause fix).
if [ -s "$CORPUS" ] && [ -s "$CORPUS.card.json" ]; then
  echo "[fire] corpus exists ($(stat -c%s "$CORPUS") bytes) + card — reuse"
else
  echo "[fire] building corpus → $CORPUS"
  python3 -u "$REPO_DIR/CLM/corpus/build_wiki_3b_corpus.py" "$CORPUS.partial" "$BYTES_LANG" "$WORK/cbuild" "$LANGS" \
    2>&1 | tee "$WORK/corpus_build.log"
  if [ -s "$CORPUS.partial" ] && [ -s "$CORPUS.partial.card.json" ]; then
    mv -f "$CORPUS.partial" "$CORPUS"
    mv -f "$CORPUS.partial.card.json" "$CORPUS.card.json"
    echo "[fire] corpus build complete ($(stat -c%s "$CORPUS") bytes)"
  else
    echo "[fire] FATAL corpus build incomplete (no .partial/card)"; exit 4
  fi
fi
sha256sum "$CORPUS" | tee "$WORK/corpus.sha256"

# 3) train the 3.07B rung (bf16, periodic ckpt). expandable_segments avoids the
#    allocator fragmentation that otherwise wastes a few GB at 61.5GB peak.
echo "[fire] training 3.07B (d4096 L30 E30) …"
PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}" \
CLM_NO_CUDNN="${CLM_NO_CUDNN:-1}" python3 -u "$REPO_DIR/CLM/train/train_lane_p_3b.py" \
  --d-model 4096 --n-trunk-layers 30 --n-experts 30 --kernel-size 3 \
  --steps "$STEPS" --seq-len "$SEQ" --batch-size "$BATCH" --grad-accum "$ACCUM" \
  --lr 2e-4 --warmup "$WARMUP" --bf16 \
  --corpus "$CORPUS" \
  --ckpt-out "$WORK/clm_3b.pt" \
  --clm-out "$WORK/clm_3b.clm" \
  --json-out "$WORK/result_3b.json" \
  --log-every "$LOG_EVERY" --ckpt-every "$CKPT_EVERY" \
  2>&1 | tee "$WORK/train_3b.log"

echo "[fire] DONE $(date -u). artifacts in $WORK:"
ls -la "$WORK"/clm_3b.* "$WORK"/result_3b.json 2>/dev/null
