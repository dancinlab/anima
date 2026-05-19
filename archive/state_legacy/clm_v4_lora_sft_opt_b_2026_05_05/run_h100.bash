#!/bin/bash
# emitted by tool/clm_v4_lora_train_orchestrator_opt_b.hexa — H100-side OPT-B runner
# raw#37 transient: Python on Linux (transformers + torch + peft + trl + lm_eval) permitted.
set -uo pipefail

WORK=/workspace/clm_v4_lora_opt_b
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
BASE_REPO='need-singularity/clm-v4-mk2-v1'
RESULTS=$WORK/results
CKPTS=$WORK/ckpts
MIXED=$WORK/corpus/mixed_50k.jsonl

echo "[orch-opt-b] start $(date -u +%FT%TZ)"

# ── deps install ──
pip install -q --no-cache-dir 'transformers>=4.45,<4.50' 'peft>=0.13' 'trl>=0.11' 'datasets>=3.0' 'lm-eval==0.4.11' 'sentencepiece' 'huggingface_hub'

# ── Phase A: corpus mix (60/30/10 — same as v1) ──
echo "[A] corpus mix (60/30/10 — reused recipe)"
python corpus_mix.py --slice-a $WORK/corpus/slice_A_anima_30k.jsonl --output $MIXED --seed 20260504

# ── Phase B: train OPT-B variant (cross_attn qkvo) ──
echo "[B] OPT-B train start: lr=5e-6 dropout=0.10 max_steps=3000 (cross_attn=qkvo)"
TRAIN_LOG=$RESULTS/train.log
python train.py \
    --base-model "$BASE_REPO" \
    --data-jsonl "$MIXED" \
    --output-dir "$CKPTS" \
    --lora-r 32 --lora-alpha 64 --lora-dropout 0.10 \
    --lr 5e-6 \
    --max-steps 3000 \
    --save-steps 500 \
    --eval-step-triggers '500,1000,1500,2000,2500,3000' \
    --phi-probe-interval 500 \
    --abort-phi-drift-pp -10.0 \
    --phi-baseline-in-pipeline 35.81 \
    --target-modules-include-cross-attn qkvo \
    --per-device-batch 8 --grad-accum 4 \
    --seq-len 512 --warmup-steps 300 \
    --seed 20260504 \
    > "$TRAIN_LOG" 2>&1 &
TRAIN_PID=$!
echo "[B] OPT-B train pid=$TRAIN_PID"

# ── Phase B-watch: monitor train + emit COMPLETE/PHI_ABORT/EARLY_STOP sentinels ──
while kill -0 $TRAIN_PID 2>/dev/null; do
    sleep 30
    # Forward train stdout sample to orchestrator log
    tail -3 "$TRAIN_LOG" 2>/dev/null || true
done
wait $TRAIN_PID
TRAIN_RC=$?
echo "[B] train done rc=$TRAIN_RC"

# Copy adapter final into results for SCP retrieval
if [ -d "$CKPTS/final" ]; then
    cp -r "$CKPTS/final" "$RESULTS/adapter_final"
fi
# Copy std/grad/audit JSONs to results (top-level for SCP)
for f in target_modules_audit gradient_flow_probe cross_attn_o_proj_std_pre_train cross_attn_o_proj_std_post_train TRAIN_DONE config; do
    [ -f "$CKPTS/${f}.json" ] && cp "$CKPTS/${f}.json" "$RESULTS/${f}.json"
done

if [ $TRAIN_RC -ne 0 ]; then
    echo "{\"reason\": \"train_rc=$TRAIN_RC\", \"finished_at\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/EARLY_STOP.sentinel
    exit $TRAIN_RC
fi

# ── Phase C: emit COMPLETE.sentinel (Phase 4 eval is separate dispatch) ──
echo "{\"ok\": true, \"finished_at\": \"$(date -u +%FT%TZ)\", \"phases\": [\"corpus_mix\", \"train_opt_b_cross_attn_qkvo\"], \"phase_4_eval\": \"separate_dispatch\"}" > $RESULTS/COMPLETE.sentinel
echo "[orch-opt-b] complete"
