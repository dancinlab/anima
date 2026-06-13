#!/usr/bin/env bash
# convmoe_303m_en_run.sh — the 303M-EN ConvMoE (Lane-P) arch-axis ORCHESTRATOR.
#
# Mirrors sweep_303m_en_run.sh (the ByteGPT sweep) config-for-config so the two
# arches are compared on IDENTICAL axes + corpus + a303m_pass gates. Trains the
# 4-config matrix SEQUENTIALLY on aiden's RTX 5070 (one ~303M ConvMoE fits 12GB),
# appending G0/G1/G2 rows to state/convmoe_303m_en/ledger.jsonl. nohup-safe.
#
# Matrix (SAME 2 axes as the ByteGPT sweep, around d=5008 / E2 / L1 / K3, V256):
#   cfg A = baseline_fast    (dropout 0.0 / wd 0.1 / lr 3e-4 / warmup 300)
#   cfg B = reg_fast         (dropout 0.1 / wd 0.2 / lr 3e-4 / warmup 300)
#   cfg C = baseline_gentle  (dropout 0.0 / wd 0.1 / lr 2e-4 / warmup 600)
#   cfg D = reg_gentle       (dropout 0.1 / wd 0.2 / lr 2e-4 / warmup 600)
set -u
ROOT="${CONVMOE_ROOT:-/home/aiden/core/anima_convmoe303}"
LEDGER="$ROOT/state/convmoe_303m_en/ledger.jsonl"
CKDIR="$ROOT/state/convmoe_303m_en/ckpt"
CLMDIR="$ROOT/state/convmoe_303m_en/clm"
LOGDIR="${CONVMOE_LOGDIR:-/tmp/convmoe_303m}"
CORPUS="${CONVMOE_CORPUS:-/tmp/sweep_303m/en_wiki_120mb.txt}"   # SAME corpus as ByteGPT sweep
STEPS="${STEPS:-12000}"
DMODEL="${DMODEL:-5008}"
TRAIN="$ROOT/CLM/train/train_convmoe_303m_en.py"
mkdir -p "$(dirname "$LEDGER")" "$CKDIR" "$CLMDIR" "$LOGDIR"

cd "$ROOT/CLM/train" || exit 3
echo "[convmoe] $(date) host=aiden root=$ROOT steps=$STEPS d=$DMODEL corpus=$CORPUS" >> "$LOGDIR/orch.log"

if [ ! -s "$CORPUS" ]; then
  echo "[convmoe] FATAL corpus missing: $CORPUS" >> "$LOGDIR/orch.log"
  exit 4
fi

run_cfg () {
  local cfg="$1" dropout="$2" wd="$3" lr="$4" warmup="$5"
  echo "[convmoe] $(date) START $cfg dropout=$dropout wd=$wd lr=$lr warmup=$warmup" >> "$LOGDIR/orch.log"
  python3 -u "$TRAIN" \
    --corpus "$CORPUS" --cfg "$cfg" --host aiden \
    --ledger "$LEDGER" --ckpt "$CKDIR/${cfg}.pt" --clm-out "$CLMDIR/${cfg}.clm" \
    --d-model "$DMODEL" --seq-len 512 --bs 8 --accum 4 --steps "$STEPS" \
    --dropout "$dropout" --weight_decay "$wd" --lr "$lr" --warmup "$warmup" \
    --bf16 --eval_every 500 \
    > "$LOGDIR/${cfg}.log" 2>&1
  echo "[convmoe] $(date) END   $cfg rc=$?" >> "$LOGDIR/orch.log"
}

run_cfg baseline_fast   0.0 0.1 3e-4 300
run_cfg reg_fast        0.1 0.2 3e-4 300
run_cfg baseline_gentle 0.0 0.1 2e-4 600
run_cfg reg_gentle      0.1 0.2 2e-4 600

echo "[convmoe] $(date) ALL DONE" >> "$LOGDIR/orch.log"
