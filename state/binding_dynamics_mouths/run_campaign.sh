#!/usr/bin/env bash
# DYNAMICS/ALGEBRAIC binding-mouth campaign driver (pod-side).
# train (3 arms x 4 mouths) -> serialize .clm -> held-out DESCENT -> engine-native G0-G6.
# Sequential (heavy-on-pool guard: eval sequential beats oversubscribe).
set -u
REPO="${REPO:-$HOME/anima}"
BDM="$REPO/state/binding_dynamics_mouths"
CORP="$REPO/state/clm303_clean_corpus"
OUT="${OUT:-$BDM/_run}"
SEED="${SEED:-7}"
STEPS="${STEPS:-2000}"
ARMS="${ARMS:-ctrl bind ablate}"
MOUTHS="${MOUTHS:-H1620_energy_settle H1630_tropical H1631_sheaf H1632_galois}"
mkdir -p "$OUT"

CELLS=(--corpus "$CORP/gen_ko.txt" "$CORP/gen_en.txt" "$CORP/sns_ko.txt" "$CORP/sns_en.txt"
       --cell-label ko-general en-general ko-sns en-sns)
EVAL_CORP=(--corpus "$CORP/gen_ko.txt" "$CORP/gen_en.txt" "$CORP/sns_ko.txt" "$CORP/sns_en.txt")
HELD="$CORP/gen_en.txt"   # held-out descent reference corpus

export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
export PYTHONPATH="$REPO/core:$REPO/cli:$REPO/train/clm/model"

echo "=== campaign: mouths=[$MOUTHS] arms=[$ARMS] seed=$SEED steps=$STEPS ==="
for M in $MOUTHS; do
  for ARM in $ARMS; do
    tag="${M}_${ARM}_s${SEED}"
    clm="$OUT/${tag}.clm"
    pt="$OUT/${tag}.pt"
    sm="$OUT/${tag}.summary.json"
    log="$OUT/${tag}.train.log"
    echo "--- TRAIN $tag ---"
    python3 "$BDM/$M/trainer.py" --arm "$ARM" --seed "$SEED" --canon --steps "$STEPS" \
        "${CELLS[@]}" --sample proportional --val-frac 0.05 --val-every 400 \
        --bf16 --out "$clm" --ckpt-out "$pt" --summary-out "$sm" \
        > "$log" 2>&1
    echo "  train rc=$? -> $log (tail:)"; tail -6 "$log"
    if [ -f "$clm" ]; then
      echo "--- DESCENT $tag ---"
      python3 "$REPO/train/clm/model/verify_clm_v2.py" descent "$clm" "$HELD" 32 \
          > "$OUT/${tag}.descent.log" 2>&1
      echo "  descent rc=$?"; grep -iE "DESCENT|overfit|model_ce|uniform|shuffle" "$OUT/${tag}.descent.log" | head -8
      echo "--- ENGINE-NATIVE G0-G6 $tag ---"
      python3 "$REPO/cli/evaluate.py" "$clm" "${EVAL_CORP[@]}" --gen 80 \
          > "$OUT/${tag}.g0g6.log" 2>&1
      echo "  eval rc=$?"; tail -25 "$OUT/${tag}.g0g6.log"
    else
      echo "  NO .clm produced for $tag (IMPL-BLOCKED or serialize fail)"
    fi
  done
done
echo "=== campaign done -> $OUT ==="
ls -la "$OUT"
