#!/bin/bash
# emitted by tool/p9_lora_mode1_eval_h100_orchestrator.hexa — H100-side LoRA eval runner
# raw#37 transient: Python on Linux (lm_eval + peft) permitted; killed with pod.
set -uo pipefail

WORK=/workspace/p9_lora_eval
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

LLAMA_ID='meta-llama/Llama-3.2-3B'
LORA_ID='need-singularity/p9-llama32-lora-stage1'
LORA_REV='5a9b4584'
RESULTS=$WORK/results
mkdir -p $RESULTS

echo "[orch] start ts=$(date -u +%FT%TZ)"

# Setup: install lm-eval + peft + transformers + datasets
echo "[setup] installing lm-eval + peft + huggingface_hub"
pip install -q --no-input huggingface_hub 'lm-eval==0.4.11' 'transformers>=4.45' 'peft>=0.12' accelerate datasets 2>&1 | tail -10

# Auth
hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true
echo "[setup] hf auth: $(hf auth whoami 2>&1 | head -1 || huggingface-cli whoami 2>&1 | head -1)"

# Download Llama base (~6GB)
echo "[setup] downloading $LLAMA_ID"
hf download "$LLAMA_ID" 2>&1 | tail -5 || \
    huggingface-cli download "$LLAMA_ID" 2>&1 | tail -5

# Download step-8k LoRA adapter (~389MB) at pinned revision to LOCAL DIR.
# CRITICAL: lm-eval `revision=` flag applies to the BASE pretrained model, NOT to the peft
# adapter (which has its own `peft=` arg). Passing revision=<lora_sha> caused 404 against the
# Llama base. Fix: pre-download LoRA at pinned revision, then pass peft=<local_dir>.
LORA_LOCAL_DIR="$WORK/lora_step8k"
echo "[setup] downloading $LORA_ID@$LORA_REV → $LORA_LOCAL_DIR (step-8k LoRA)"
mkdir -p "$LORA_LOCAL_DIR"
hf download "$LORA_ID" --revision "$LORA_REV" --local-dir "$LORA_LOCAL_DIR" 2>&1 | tail -5 || \
    huggingface-cli download "$LORA_ID" --revision "$LORA_REV" --local-dir "$LORA_LOCAL_DIR" 2>&1 | tail -5
# Verify adapter files present
if [ ! -f "$LORA_LOCAL_DIR/adapter_model.safetensors" ] || [ ! -f "$LORA_LOCAL_DIR/adapter_config.json" ]; then
    echo "[FATAL] LoRA adapter files missing in $LORA_LOCAL_DIR"
    ls -la "$LORA_LOCAL_DIR" 2>&1
    # still emit sentinel so orchestrator auto-kills cleanly
    echo "{\"ok\": false, \"error\": \"lora_download_failed\", \"finished_at\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/COMPLETE.sentinel
    exit 1
fi
echo "[setup] LoRA adapter present: $(du -sh $LORA_LOCAL_DIR/adapter_model.safetensors | awk '{print $1}')"

echo "[orch] lm_eval=$(pip show lm-eval 2>/dev/null | grep Version | awk '{print $2}')"
echo "[orch] peft=$(pip show peft 2>/dev/null | grep Version | awk '{print $2}')"
echo "[orch] torch=$(python -c 'import torch; print(torch.__version__)')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

# Verify peft= flag is supported in this lm-eval version (0.4.11 supports peft= in model_args).
# Reference: lm-eval-harness/lm_eval/models/huggingface.py — HFLM accepts `peft` kwarg, attaches
# PeftModel.from_pretrained(model, peft) after base load.

run_bench() {
    local tkey=$1; local task=$2; local nshot=$3
    local out=$RESULTS/lora_${tkey}_dir
    local log=$RESULTS/${tkey}.log
    echo "[run] task=$task n=$nshot → $out"
    local t0=$(date -u +%s)
    # peft= argument: standard lm-eval composition. NOTE: revision= is intentionally OMITTED
    # because it applies to the BASE pretrained model, not the peft adapter. The adapter is
    # already pinned via $LORA_LOCAL_DIR (downloaded at $LORA_REV in setup).
    # The base 'pretrained' uses the non-Instruct Llama-3.2-3B (matches BG-Ο anchor).
    lm_eval --model hf \
        --model_args "pretrained=${LLAMA_ID},peft=${LORA_LOCAL_DIR},dtype=bfloat16,trust_remote_code=False" \
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
    local wall=$((t1 - t0))
    echo "[done] task=$task rc=$rc wall=${wall}s"
    if [ $rc -ne 0 ]; then
        echo "[FAIL] tail of $log:"; tail -50 "$log"
    fi
    if [ -d "$out" ]; then
        find "$out" -name 'results*.json' -exec cp {} $RESULTS/lora_${tkey}.json \;
    fi
    return $rc
}

# 3 jobs: LoRA × HellaSwag (0-shot acc_norm), MMLU (5-shot), TriviaQA (0-shot EM)
# Same fewshot pattern as BG-Ο Llama base anchors for direct Δ computation.

run_bench 'hellaswag' 'hellaswag' 0
run_bench 'mmlu' 'mmlu' 5
run_bench 'triviaqa' 'triviaqa' 0

# completion sentinel — STANDARDIZED NAME per lesson L1
echo "{\"ok\": true, \"finished_at\": \"$(date -u +%FT%TZ)\", \"benchmarks\": [\"hellaswag\", \"mmlu\", \"triviaqa\"]}" > $RESULTS/COMPLETE.sentinel
echo "[orch] complete"
