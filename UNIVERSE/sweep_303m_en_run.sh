#!/usr/bin/env bash
# sweep_303m_en_run.sh — the 303M-EN recipe sweep ORCHESTRATOR (runs detached on aiden).
#
# Trains the 4-config sweep matrix SEQUENTIALLY on aiden's RTX 5070 (one 303M fits 12GB;
# serial keeps VRAM sane), appending a303m_pass G0/G1/G2 rows to the on-disk ledger after
# each. Designed to be launched via `nohup ... &` so it SURVIVES an SSH drop.
#
# Matrix (2 axes around the H_1129 base d1024/L24/H16/block512, byte vocab256):
#   AXIS-1 anti-overfit (dropout/weight_decay) : baseline(0.0/0.1) vs reg(0.1/0.2)
#   AXIS-2 LR/warmup                            : fast(3e-4/300) vs gentle(2e-4/600)
#   cfg A = baseline_fast    (= H_1129 reference recipe)
#   cfg B = reg_fast         (anti-overfit: dropout+wd, H_1141 overfit-past-7000 mitigation)
#   cfg C = baseline_gentle  (slower LR / longer warmup)
#   cfg D = reg_gentle       (both anti-overfit levers)
# Dialogue-ratio axis is PARKED: no clean English dialogue corpus on hand (the 5-lang blend's
# dialogue is non-English, ASCII-filtered out) — note in ledger; next axis once EN dialogue lands.
set -u
ROOT=/home/aiden/core/anima_sweep303
LEDGER=$ROOT/state/sweep_303m_en/ledger.jsonl
CKDIR=$ROOT/state/sweep_303m_en/ckpt
LOGDIR=/tmp/sweep_303m
CORPUS=/tmp/sweep_303m/en_wiki_120mb.txt
SRC=/home/aiden/core/anima/data/corpus_mix_70wiki_30dialogue.txt
STEPS=${STEPS:-12000}
mkdir -p "$(dirname "$LEDGER")" "$CKDIR" "$LOGDIR"

cd "$ROOT/UNIVERSE" || exit 3
echo "[sweep] $(date) host=aiden root=$ROOT steps=$STEPS" >> "$LOGDIR/orch.log"

# 1) prep English-dominant corpus (deterministic ASCII-filter; idempotent)
if [ ! -s "$CORPUS" ]; then
  echo "[sweep] prepping corpus -> $CORPUS" >> "$LOGDIR/orch.log"
  python3 -u sweep_303m_en_prep_corpus.py "$SRC" "$CORPUS" --max_mb 120 >> "$LOGDIR/prep.log" 2>&1
fi

run_cfg () {
  local cfg="$1" dropout="$2" wd="$3" lr="$4" warmup="$5"
  echo "[sweep] $(date) START $cfg dropout=$dropout wd=$wd lr=$lr warmup=$warmup" >> "$LOGDIR/orch.log"
  python3 -u sweep_303m_en_train.py \
    --corpus "$CORPUS" --cfg "$cfg" --host aiden \
    --ledger "$LEDGER" --ckpt "$CKDIR/${cfg}.pt" \
    --d 1024 --n_layer 24 --n_head 16 --block 512 \
    --bs 8 --accum 4 --steps "$STEPS" \
    --dropout "$dropout" --weight_decay "$wd" --lr "$lr" --warmup "$warmup" \
    --grad_ckpt --eval_every 500 \
    > "$LOGDIR/${cfg}.log" 2>&1
  echo "[sweep] $(date) END   $cfg rc=$?" >> "$LOGDIR/orch.log"
}

run_cfg baseline_fast   0.0 0.1 3e-4 300
run_cfg reg_fast        0.1 0.2 3e-4 300
run_cfg baseline_gentle 0.0 0.1 2e-4 600
run_cfg reg_gentle      0.1 0.2 2e-4 600

echo "[sweep] $(date) ALL DONE" >> "$LOGDIR/orch.log"
