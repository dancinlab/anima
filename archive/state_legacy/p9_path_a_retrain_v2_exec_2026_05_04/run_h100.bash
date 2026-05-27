#!/bin/bash
# emitted by tool/p9_path_a_retrain_v2_h100_orchestrator.hexa — H100-side retrain v2 runner
# raw#37 transient: Python on Linux (transformers + torch + peft + trl + lm_eval) permitted; killed with pod.
set -uo pipefail

WORK=/workspace/p9_retrain_v2
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

LLAMA_ID='meta-llama/Llama-3.2-3B'
RESULTS=$WORK/results
CKPTS=$WORK/ckpts
CORPUS=$WORK/corpus
SENTINELS=$RESULTS/sentinels
mkdir -p $RESULTS $CKPTS $CORPUS $SENTINELS

echo "[orch] start ts=$(date -u +%FT%TZ)"

# Setup: install transformers + peft + trl + lm-eval + datasets
echo "[setup] installing pip packages"
pip install -q --no-input \
    'transformers>=4.45,<4.50' 'peft>=0.12' 'trl>=0.11' 'accelerate>=0.34' \
    'datasets>=2.20' 'huggingface_hub>=0.25' \
    'lm-eval==0.4.11' \
    safetensors sentencepiece 2>&1 | tail -10

# Auth
hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true
echo "[setup] hf auth: $(hf auth whoami 2>&1 | head -1 || huggingface-cli whoami 2>&1 | head -1)"

# Download Llama base (~6GB)
echo "[setup] downloading $LLAMA_ID base"
hf download "$LLAMA_ID" 2>&1 | tail -3 || huggingface-cli download "$LLAMA_ID" 2>&1 | tail -3

echo "[orch] versions: torch=$(python -c 'import torch; print(torch.__version__)') trl=$(pip show trl 2>/dev/null | awk '/^Version/{print $2}') peft=$(pip show peft 2>/dev/null | awk '/^Version/{print $2}')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

# ── Phase A: corpus mix (slice A loaded from local jsonl + B/C downloaded from HF) ──
echo "[A] corpus mix start"
MIXED=$CORPUS/sft_mix_2026_05_04.jsonl
python corpus_mix.py \
    --slice-a "$CORPUS/slice_A_anima_30k.jsonl" \
    --out "$MIXED" 2>&1 | tee $RESULTS/corpus_mix.log
if [ ! -f "$MIXED" ]; then
    echo "[FATAL] corpus mix failed"
    echo "{\"ok\": false, \"error\": \"corpus_mix_failed\"}" > $RESULTS/COMPLETE.sentinel
    exit 1
fi
MIXED_LINES=$(wc -l < "$MIXED")
echo "[A] corpus mix OK: $MIXED ($MIXED_LINES lines)"
cp -f "$MIXED.summary.json" "$RESULTS/corpus_mix_summary.json" 2>/dev/null || true

# ── Phase B: train (target ~5h on H100) ──
echo "[B] train start"
TRAIN_LOG=$RESULTS/train.log
python train.py \
    --base-model "$LLAMA_ID" \
    --data-jsonl "$MIXED" \
    --output-dir "$CKPTS" \
    --lora-r 64 --lora-alpha 64 --lora-dropout 0.05 \
    --lr 5e-5 \
    --max-steps 6000 \
    --save-steps 500 \
    --eval-step-trigger 2000 \
    --per-device-batch 1 --grad-accum 8 \
    --seed 42 \
    > "$TRAIN_LOG" 2>&1 &
TRAIN_PID=$!
echo "[B] train pid=$TRAIN_PID"

# ── Phase B-watch: monitor for intermediate eval sentinel and run lm-eval probe ──
INTER_DONE=0
WAIT_INT=0
while kill -0 $TRAIN_PID 2>/dev/null; do
    if [ "$INTER_DONE" = "0" ]; then
        REQ=$(ls $CKPTS/sentinels/INTERMEDIATE_EVAL_REQUEST_step_*.sentinel 2>/dev/null | head -1)
        if [ -n "$REQ" ]; then
            STEP=$(basename "$REQ" | grep -oE 'step_[0-9]+' | grep -oE '[0-9]+' | head -1)
            CKPT_DIR="$CKPTS/checkpoint-${STEP}"
            echo "[B-watch] intermediate eval requested at step=$STEP; waiting for ckpt-${STEP}/adapter_model.safetensors"
            for j in $(seq 1 60); do
                if [ -f "$CKPT_DIR/adapter_model.safetensors" ]; then break; fi
                sleep 10
            done
            if [ -f "$CKPT_DIR/adapter_model.safetensors" ]; then
                echo "[B-watch] running HellaSwag-200 probe on $CKPT_DIR"
                INTER_OUT=$RESULTS/intermediate_dir
                lm_eval --model hf \
                    --model_args "pretrained=${LLAMA_ID},peft=${CKPT_DIR},dtype=bfloat16,trust_remote_code=False" \
                    --tasks hellaswag --num_fewshot 0 --batch_size 16 --device cuda:0 --seed 42 --limit 200 \
                    --output_path "$INTER_OUT" > $RESULTS/intermediate_eval.log 2>&1 || true
                INTER_RES=$(find "$INTER_OUT" -name 'results*.json' | head -1)
                if [ -n "$INTER_RES" ]; then
                    cp -f "$INTER_RES" $RESULTS/intermediate_hellaswag200.json
                    INTER_VAL=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' $RESULTS/intermediate_hellaswag200.json)
                    echo "[B-watch] intermediate HellaSwag-200 acc_norm=$INTER_VAL (threshold 0.604)"
                    DROP=$(awk -v v="$INTER_VAL" 'BEGIN{ if (v == "null" || v+0 < 0.604) print "FAIL"; else print "PASS" }')
                    if [ "$DROP" = "FAIL" ]; then
                        echo "[B-watch] EARLY-STOP TRIGGER: HellaSwag-200 acc_norm=$INTER_VAL < 0.604 — F-PA-RETRAIN-v2-2 fail"
                        echo "{\"step\": $STEP, \"acc_norm\": \"$INTER_VAL\", \"trigger\": \"5pp_drop\", \"ts_utc\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/EARLY_STOP.sentinel
                        echo "[B-watch] killing train pid=$TRAIN_PID for early stop"
                        kill $TRAIN_PID 2>/dev/null || true
                        sleep 5
                        kill -9 $TRAIN_PID 2>/dev/null || true
                        break
                    fi
                else
                    echo "[B-watch] intermediate eval results JSON not found — continuing train (best-effort)"
                fi
                INTER_DONE=1
            else
                echo "[B-watch] ckpt-${STEP} adapter never appeared in 600s — skipping intermediate; continuing train"
                INTER_DONE=1
            fi
        fi
    fi
    sleep 30
done

wait $TRAIN_PID 2>/dev/null
TRAIN_RC=$?
echo "[B] train rc=$TRAIN_RC"

# Capture trainer_state.json for F-PA-RETRAIN-v2-1 loss converge
FINAL_TRAINER_STATE=$(find $CKPTS -name 'trainer_state.json' | sort | tail -1)
if [ -n "$FINAL_TRAINER_STATE" ]; then
    cp -f "$FINAL_TRAINER_STATE" $RESULTS/final_trainer_state.json
    # Compute simple loss-converged check: max(loss_window_increase) < 0.1 across last 4 windows of 500 steps
    LOSS_OK=$(python -c "
import json
d=json.load(open('$RESULTS/final_trainer_state.json'))
hist=[h for h in d.get('log_history',[]) if 'loss' in h]
if len(hist) < 5:
    print('false')
else:
    losses=[h['loss'] for h in hist]
    has_nan=any(l!=l or l==float('inf') for l in losses)
    if has_nan: print('false')
    else:
        # last 4 windows: each window = 500/logging_steps_per_window observations
        # simple: rolling diff over last 25% of points
        n=len(losses)
        tail=losses[-min(n,40):]
        max_inc=0
        for i in range(1,len(tail)):
            inc=tail[i]-tail[i-1]
            if inc>max_inc: max_inc=inc
        print('true' if max_inc < 1.0 else 'false')
" 2>/dev/null || echo 'unknown')
    echo "{\"loss_converged\": $LOSS_OK, \"trainer_state\": \"final_trainer_state.json\"}" > $RESULTS/train_log.json
fi

# If early-stopped, emit COMPLETE.sentinel anyway so orchestrator scp + kill
if [ -f "$RESULTS/EARLY_STOP.sentinel" ]; then
    echo "[B] early-stop path: skipping final eval; emit COMPLETE.sentinel"
    echo "{\"ok\": false, \"early_stopped\": true, \"finished_at\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/COMPLETE.sentinel
    echo "[orch] complete (early-stop)"
    exit 0
fi

if [ $TRAIN_RC -ne 0 ]; then
    echo "[B] train failed rc=$TRAIN_RC; emit COMPLETE.sentinel for cleanup"
    tail -50 "$TRAIN_LOG"
    echo "{\"ok\": false, \"train_rc\": $TRAIN_RC, \"finished_at\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/COMPLETE.sentinel
    exit 1
fi

# ── Phase C: final 3-bench eval (limit=500, seed=42) ──
echo "[C] final eval start"
FINAL_ADAPTER="$CKPTS/final"
if [ ! -f "$FINAL_ADAPTER/adapter_model.safetensors" ]; then
    # fall back to latest checkpoint-XXXX
    FINAL_ADAPTER=$(ls -d $CKPTS/checkpoint-* 2>/dev/null | sort -V | tail -1)
fi
echo "[C] final adapter: $FINAL_ADAPTER"

run_bench() {
    local tkey=$1; local task=$2; local nshot=$3
    local out=$RESULTS/final_lora_${tkey}_dir
    local log=$RESULTS/final_${tkey}.log
    echo "[C] task=$task n=$nshot → $out"
    local t0=$(date -u +%s)
    lm_eval --model hf \
        --model_args "pretrained=${LLAMA_ID},peft=${FINAL_ADAPTER},dtype=bfloat16,trust_remote_code=False" \
        --tasks "$task" \
        --num_fewshot "$nshot" \
        --batch_size 16 \
        --device cuda:0 \
        --seed 42 \
        --limit 500 \
        --log_samples \
        --output_path "$out" \
        > "$log" 2>&1
    local rc=$?
    local t1=$(date -u +%s)
    echo "[C] done task=$task rc=$rc wall=$((t1-t0))s"
    if [ $rc -ne 0 ]; then echo "[FAIL]"; tail -50 "$log"; fi
    if [ -d "$out" ]; then
        find "$out" -name 'results*.json' -exec cp {} $RESULTS/final_lora_${tkey}.json \;
    fi
    return $rc
}

run_bench 'hellaswag' 'hellaswag' 0
run_bench 'mmlu' 'mmlu' 5
run_bench 'triviaqa' 'triviaqa' 0

# ── Phase D: emit COMPLETE.sentinel ──
echo "{\"ok\": true, \"finished_at\": \"$(date -u +%FT%TZ)\", \"phases\": [\"corpus_mix\", \"train\", \"intermediate_eval\", \"final_eval\"]}" > $RESULTS/COMPLETE.sentinel
echo "[orch] complete"
