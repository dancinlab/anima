#!/usr/bin/env bash
# H_1816 pod runner: 3 arms (ce_marginal/pc_bind/pc_free_energy) seed7, 303M canon.
# train(torch) -> .clm(additive) -> held-out DESCENT gate -> py g_gates G0-G6 (DIRECTIONAL).
# Hexa-native TERMINAL eval is run separately via cli/eval_pod.sh (g_gates.hexa).
set -u
REPO="${REPO:?set REPO to anima repo root on the host}"
cd "$REPO"
export ANIMA_CORPUS_CACHE="$REPO/.corpus_cache"
OUT="$REPO/state/1641_predcoding_binding/ckpt"; mkdir -p "$OUT"
KO_GEN="$ANIMA_CORPUS_CACHE/anima-corpus-ko-general.txt"
EN_GEN="$ANIMA_CORPUS_CACHE/anima-corpus-en-general.txt"
KO_SNS="$ANIMA_CORPUS_CACHE/anima-corpus-ko-sns.txt"
EN_SNS="$ANIMA_CORPUS_CACHE/anima-corpus-en-sns.txt"
for f in "$KO_GEN" "$EN_GEN" "$KO_SNS" "$EN_SNS"; do
  [ -s "$f" ] || { echo "FATAL corpus missing: $f"; exit 3; }
done
SEED="${SEED:-7}"
STEPS="${STEPS:-2000}"

echo "############ H_1816 TRAIN seed=$SEED steps=$STEPS $(date -u +%FT%TZ) ############"
for OBJ in ce_marginal pc_bind pc_free_energy; do
  echo "=== TRAIN obj=$OBJ seed=$SEED $(date -u +%FT%TZ) ==="
  python3 -u state/1641_predcoding_binding/trainer.py --objective "$OBJ" --seed "$SEED" --canon \
    --corpus "$KO_GEN" "$EN_GEN" "$KO_SNS" "$EN_SNS" \
    --cell-label ko-general en-general ko-sns en-sns \
    --sample proportional --steps "$STEPS" --val-every 200 --bf16 \
    --out "$OUT/${OBJ}_seed${SEED}.clm" \
    --ckpt-out "$OUT/${OBJ}_seed${SEED}.pt" \
    --gauges-out "$OUT/${OBJ}_seed${SEED}.json" 2>&1 | tee "$OUT/${OBJ}_seed${SEED}.log"
done

echo "############ HELD-OUT DESCENT GATE (math.log mirror, per register) ############"
# trainer.py already logs FINAL held-out val-CE per register (the DESCENT gate). Here we
# additionally run the standalone verify_clm_v2 descent (heldout-only) on each of the 4
# register corpora so each arm has an explicit per-cell DESCENT verdict.
for OBJ in ce_marginal pc_bind pc_free_energy; do
  CLM="$OUT/${OBJ}_seed${SEED}.clm"
  : > "$OUT/${OBJ}_seed${SEED}.descent.txt"
  for CELL in "$KO_GEN" "$EN_GEN" "$KO_SNS" "$EN_SNS"; do
    echo "=== DESCENT $OBJ cell=$(basename $CELL) ===" | tee -a "$OUT/${OBJ}_seed${SEED}.descent.txt"
    python3 train/clm/model/verify_clm_v2.py descent "$CLM" "$CELL" 2>&1 | tail -12 \
      | tee -a "$OUT/${OBJ}_seed${SEED}.descent.txt"
  done
done

echo "############ py g_gates G0-G6 (DIRECTIONAL cross-check) ############"
for OBJ in ce_marginal pc_bind pc_free_energy; do
  CLM="$OUT/${OBJ}_seed${SEED}.clm"
  echo "=== G0-G6 $OBJ ==="
  PYTHONPATH="$REPO/core:$REPO/train/clm/model:$PYTHONPATH" \
    python3 core/g_gates.py "$CLM" "$KO_GEN" "$EN_GEN" --gen 80 2>&1 | tee "$OUT/${OBJ}_seed${SEED}.g0g6_py.txt"
done
echo "############ H_1816 POD RUN DONE $(date -u +%FT%TZ) ############"
