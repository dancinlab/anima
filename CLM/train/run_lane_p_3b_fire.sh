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
# 2) build the scaled clean corpus (idempotent — skip if present + card matches)
if [ ! -s "$CORPUS" ]; then
  echo "[fire] building corpus → $CORPUS"
  python3 "$REPO_DIR/CLM/corpus/build_wiki_3b_corpus.py" "$CORPUS" "$BYTES_LANG" "$WORK/cbuild" "$LANGS" \
    2>&1 | tee "$WORK/corpus_build.log"
else
  echo "[fire] corpus exists ($(stat -c%s "$CORPUS") bytes) — reuse"
fi
sha256sum "$CORPUS" | tee "$WORK/corpus.sha256"

# 3) train the 3.07B rung (bf16, periodic ckpt every 2000 steps)
echo "[fire] training 3.07B (d4096 L30 E30) …"
CLM_NO_CUDNN="${CLM_NO_CUDNN:-1}" python3 -u "$REPO_DIR/CLM/train/train_lane_p_3b.py" \
  --d-model 4096 --n-trunk-layers 30 --n-experts 30 --kernel-size 3 \
  --steps "$STEPS" --seq-len "$SEQ" --batch-size "$BATCH" --grad-accum "$ACCUM" \
  --lr 2e-4 --warmup 500 --bf16 \
  --corpus "$CORPUS" \
  --ckpt-out "$WORK/clm_3b.pt" \
  --clm-out "$WORK/clm_3b.clm" \
  --json-out "$WORK/result_3b.json" \
  --log-every 100 --ckpt-every 2000 \
  2>&1 | tee "$WORK/train_3b.log"

echo "[fire] DONE $(date -u). artifacts in $WORK:"
ls -la "$WORK"/clm_3b.* "$WORK"/result_3b.json 2>/dev/null
