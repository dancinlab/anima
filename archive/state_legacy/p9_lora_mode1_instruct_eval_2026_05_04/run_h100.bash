#!/bin/bash
# emitted by tool/p9_lora_mode1_instruct_eval_h100_orchestrator.hexa — BG-Ψ H100-side runner
# raw#37 transient: Python on Linux (lm_eval + peft) permitted; killed with pod.
#
# Performs DUAL eval suite:
#   Pass 1: Llama-3.2-3B-Instruct base alone × {hellaswag (0-shot), mmlu (5-shot), triviaqa (0-shot)}
#   Pass 2: Llama-3.2-3B-Instruct + step-8k LoRA × same 3 benchmarks
# Total = 6 lm-eval runs, limit=500, seed=42, bf16.
set -uo pipefail

WORK=/workspace/p9_eval
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

INSTRUCT_ID='meta-llama/Llama-3.2-3B-Instruct'
LORA_ID='need-singularity/p9-llama32-lora-stage1'
LORA_REV='5a9b4584'
RESULTS=$WORK/results
mkdir -p $RESULTS

echo "[orch] start ts=$(date -u +%FT%TZ)"

# Setup
echo "[setup] installing lm-eval + peft + huggingface_hub"
pip install -q --no-input huggingface_hub 'lm-eval==0.4.11' 'transformers>=4.45' 'peft>=0.12' accelerate datasets 2>&1 | tail -10

# Auth
hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true
echo "[setup] hf auth: $(hf auth whoami 2>&1 | head -1 || huggingface-cli whoami 2>&1 | head -1)"

# Download Instruct base (~6GB)
echo "[setup] downloading $INSTRUCT_ID"
hf download "$INSTRUCT_ID" 2>&1 | tail -5 || \
    huggingface-cli download "$INSTRUCT_ID" 2>&1 | tail -5

# Download step-8k LoRA at pinned revision to LOCAL DIR
LORA_LOCAL_DIR="$WORK/lora_step8k"
echo "[setup] downloading $LORA_ID@$LORA_REV → $LORA_LOCAL_DIR"
mkdir -p "$LORA_LOCAL_DIR"
hf download "$LORA_ID" --revision "$LORA_REV" --local-dir "$LORA_LOCAL_DIR" 2>&1 | tail -5 || \
    huggingface-cli download "$LORA_ID" --revision "$LORA_REV" --local-dir "$LORA_LOCAL_DIR" 2>&1 | tail -5
if [ ! -f "$LORA_LOCAL_DIR/adapter_model.safetensors" ] || [ ! -f "$LORA_LOCAL_DIR/adapter_config.json" ]; then
    echo "[FATAL] LoRA adapter files missing in $LORA_LOCAL_DIR"
    ls -la "$LORA_LOCAL_DIR" 2>&1
    echo "{\"ok\": false, \"error\": \"lora_download_failed\", \"finished_at\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/COMPLETE.sentinel
    exit 1
fi
echo "[setup] LoRA adapter present: $(du -sh $LORA_LOCAL_DIR/adapter_model.safetensors | awk '{print $1}')"

# Verify adapter declared base = Instruct (now matches eval base — no template mismatch)
ADAPTER_BASE=$(python3 -c "import json; print(json.load(open('$LORA_LOCAL_DIR/adapter_config.json')).get('base_model_name_or_path',''))" 2>/dev/null)
echo "[setup] adapter declared base = $ADAPTER_BASE (eval base = $INSTRUCT_ID)"
if [ "$ADAPTER_BASE" != "$INSTRUCT_ID" ]; then
    echo "[WARN] adapter base mismatch — adapter declares $ADAPTER_BASE but eval uses $INSTRUCT_ID"
fi

echo "[orch] lm_eval=$(pip show lm-eval 2>/dev/null | grep Version | awk '{print $2}')"
echo "[orch] peft=$(pip show peft 2>/dev/null | grep Version | awk '{print $2}')"
echo "[orch] torch=$(python -c 'import torch; print(torch.__version__)')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

# ─── pass 1: Instruct base alone ───
run_base() {
    local tkey=$1; local task=$2; local nshot=$3
    local out=$RESULTS/instruct_base_${tkey}_dir
    local log=$RESULTS/instruct_base_${tkey}.log
    echo "[run-base] task=$task n=$nshot → $out"
    local t0=$(date -u +%s)
    lm_eval --model hf \
        --model_args "pretrained=${INSTRUCT_ID},dtype=bfloat16,trust_remote_code=False" \
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
    echo "[done-base] task=$task rc=$rc wall=${wall}s"
    if [ $rc -ne 0 ]; then
        echo "[FAIL-base] tail of $log:"; tail -50 "$log"
    fi
    if [ -d "$out" ]; then
        find "$out" -name 'results*.json' -exec cp {} $RESULTS/instruct_base_${tkey}.json \;
    fi
    return $rc
}

# ─── pass 2: Instruct + LoRA ───
run_lora() {
    local tkey=$1; local task=$2; local nshot=$3
    local out=$RESULTS/instruct_lora_${tkey}_dir
    local log=$RESULTS/instruct_lora_${tkey}.log
    echo "[run-lora] task=$task n=$nshot → $out"
    local t0=$(date -u +%s)
    lm_eval --model hf \
        --model_args "pretrained=${INSTRUCT_ID},peft=${LORA_LOCAL_DIR},dtype=bfloat16,trust_remote_code=False" \
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
    echo "[done-lora] task=$task rc=$rc wall=${wall}s"
    if [ $rc -ne 0 ]; then
        echo "[FAIL-lora] tail of $log:"; tail -50 "$log"
    fi
    if [ -d "$out" ]; then
        find "$out" -name 'results*.json' -exec cp {} $RESULTS/instruct_lora_${tkey}.json \;
    fi
    return $rc
}

# Pass 1: base anchors
run_base 'hellaswag' 'hellaswag' 0
run_base 'mmlu'      'mmlu'      5
run_base 'triviaqa'  'triviaqa'  0

# Pass 2: LoRA on Instruct
run_lora 'hellaswag' 'hellaswag' 0
run_lora 'mmlu'      'mmlu'      5
run_lora 'triviaqa'  'triviaqa'  0

# Aggregate compact JSON for downstream verdict computation
python3 -c "
import json, glob, os
results = {'instruct_base': {}, 'instruct_lora': {}}
for f in sorted(glob.glob('$RESULTS/instruct_base_*.json')):
    name = os.path.basename(f).replace('instruct_base_', '').replace('.json', '')
    if name.endswith('_dir'): continue
    try:
        with open(f) as fh:
            results['instruct_base'][name] = json.load(fh).get('results', {})
    except Exception as e:
        results['instruct_base'][name] = {'_error': str(e)}
for f in sorted(glob.glob('$RESULTS/instruct_lora_*.json')):
    name = os.path.basename(f).replace('instruct_lora_', '').replace('.json', '')
    if name.endswith('_dir'): continue
    try:
        with open(f) as fh:
            results['instruct_lora'][name] = json.load(fh).get('results', {})
    except Exception as e:
        results['instruct_lora'][name] = {'_error': str(e)}
with open('$RESULTS/eval_results.json', 'w') as fh:
    json.dump(results, fh, indent=2)
print('[agg] eval_results.json written')
"

# completion sentinel — STANDARDIZED NAME per lesson L1
echo "{\"ok\": true, \"finished_at\": \"$(date -u +%FT%TZ)\", \"benchmarks\": [\"hellaswag\", \"mmlu\", \"triviaqa\"], \"passes\": [\"instruct_base\", \"instruct_lora\"]}" > $RESULTS/COMPLETE.sentinel
echo "[orch] complete"
