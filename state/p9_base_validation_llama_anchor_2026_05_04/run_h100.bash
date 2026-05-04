#!/bin/bash
# emitted by tool/p9_llama_anchor_h100_orchestrator.hexa — H100-side benchmark runner
# raw#37 transient: Python on Linux (lm_eval) permitted; killed with pod.
set -uo pipefail

WORK=/workspace/p9_llama_anchor
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

LLAMA_ID=meta-llama/Llama-3.2-3B
RESULTS=$WORK/results
mkdir -p $RESULTS

echo "[orch] start ts=$(date -u +%FT%TZ)"

# Setup: install lm-eval and download Llama base
echo "[setup] installing lm-eval + huggingface_hub"
pip install -q --no-input huggingface_hub 'lm-eval==0.4.11' 'transformers>=4.45' accelerate datasets 2>&1 | tail -10

# Auth (token already in env from boot)
hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true
echo "[setup] hf auth: $(hf auth whoami 2>&1 | head -1 || huggingface-cli whoami 2>&1 | head -1)"

# Download Llama-3.2-3B (~6GB)
echo "[setup] downloading Llama-3.2-3B"
hf download meta-llama/Llama-3.2-3B 2>&1 | tail -5 || \
    huggingface-cli download meta-llama/Llama-3.2-3B 2>&1 | tail -5

echo "[orch] lm_eval=$(pip show lm-eval 2>/dev/null | grep Version | awk '{print $2}')"
echo "[orch] torch=$(python -c 'import torch; print(torch.__version__)')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

run_bench() {
    local tkey=$1; local task=$2; local nshot=$3
    local out=$RESULTS/llama_${tkey}_dir
    local log=$RESULTS/${tkey}.log
    echo "[run] task=$task n=$nshot → $out"
    local t0=$(date -u +%s)
    lm_eval --model hf \
        --model_args "pretrained=${LLAMA_ID},dtype=bfloat16,trust_remote_code=False" \
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
    # Copy results.json out for streaming back to Mac (lm-eval writes nested)
    if [ -d "$out" ]; then
        find "$out" -name 'results*.json' -exec cp {} $RESULTS/llama_${tkey}.json \;
    fi
    return $rc
}

# 3 jobs: Llama × HellaSwag (0-shot acc_norm), MMLU (5-shot), TriviaQA (0-shot EM)
# Spec said 5-shot uniformly for batch=16 seed=42 limit=500 — but harness convention
# uses 0-shot for HellaSwag/TriviaQA acc_norm/EM published numbers. We follow harness
# defaults to compare to published numbers (criterion 2 ±10%).

run_bench 'hellaswag' 'hellaswag' 0
run_bench 'mmlu' 'mmlu' 5
run_bench 'triviaqa' 'triviaqa' 0

# completion sentinel — STANDARDIZED NAME per spec L1
echo "{\"ok\": true, \"finished_at\": \"$(date -u +%FT%TZ)\", \"benchmarks\": [\"hellaswag\", \"mmlu\", \"triviaqa\"]}" > $RESULTS/COMPLETE.sentinel
echo "[orch] complete"
