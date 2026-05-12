#!/bin/bash
# emitted by tool/clm_v4_lora_train_orchestrator.hexa — H100-side runner
# raw#37 transient: Python on Linux (transformers + torch + peft + trl + lm_eval) permitted; killed with pod.
set -uo pipefail

WORK=/workspace/clm_v4_lora
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

BASE_REPO='need-singularity/clm-v4-mk2-v1'
RESULTS=$WORK/results
CKPTS=$WORK/ckpts
CORPUS=$WORK/corpus
SENTINELS=$RESULTS/sentinels
mkdir -p $RESULTS $CKPTS $CORPUS $SENTINELS

echo "[orch] start ts=$(date -u +%FT%TZ)"

# Setup: install pinned deps for SFT + lm-eval (transformers >=4.51 for dtype kwarg compat per L14)
echo "[setup] installing pip packages"
pip install -q --no-input \
    'transformers>=4.51,<4.60' 'peft>=0.12' 'trl>=0.11' 'accelerate>=0.34' \
    'datasets>=2.20' 'huggingface_hub>=0.25' \
    'lm-eval==0.4.11' \
    safetensors sentencepiece 2>&1 | tail -10

# Auth
hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true
echo "[setup] hf auth: $(hf auth whoami 2>&1 | head -1 || huggingface-cli whoami 2>&1 | head -1)"

# Download CLM v4 mk2-v1 base (~2.1GB safetensors + 5.4GB best.pt; we only need safetensors + custom code)
echo "[setup] downloading $BASE_REPO base (safetensors path; best.pt skipped)"
hf download "$BASE_REPO" --exclude 'best.pt' 2>&1 | tail -3 || huggingface-cli download "$BASE_REPO" --exclude best.pt 2>&1 | tail -3

echo "[orch] versions: torch=$(python -c 'import torch; print(torch.__version__)') trl=$(pip show trl 2>/dev/null | awk '/^Version/{print $2}') peft=$(pip show peft 2>/dev/null | awk '/^Version/{print $2}') transformers=$(pip show transformers 2>/dev/null | awk '/^Version/{print $2}')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

# ── Phase A: corpus mix ──
echo "[A] corpus mix start"
MIXED=$CORPUS/sft_mix_2026_05_05.jsonl
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

# ── Phase A2: pre-LoRA φ★ proxy + smoke (cheap, ~30s) ──
echo "[A2] pre-LoRA φ★ proxy + smoke"
python -c "
import json, os, torch, sys
sys.path.insert(0, '$WORK')
from transformers import AutoModelForCausalLM
from huggingface_hub import hf_hub_download
import sentencepiece as spm
spm_path = hf_hub_download(repo_id='$BASE_REPO', filename='tokenizer_64k_multilingual.model', token=os.environ['HF_TOKEN'])
sp = spm.SentencePieceProcessor(); sp.load(spm_path)
model = AutoModelForCausalLM.from_pretrained('$BASE_REPO', dtype=torch.bfloat16, trust_remote_code=True, token=os.environ['HF_TOKEN']).cuda().eval()
prompts = ['The quick brown fox jumps over the lazy dog.', 'Hello, how are you today?', '안녕하세요. 오늘 기분이 어떠세요?', 'def factorial(n): return 1 if n<=1 else n*factorial(n-1)', 'In quantum mechanics, observation collapses the wavefunction.']
stds = []
for p in prompts:
    ids = sp.encode(p, out_type=int)[:510]
    if not ids: continue
    inp = torch.tensor([ids], dtype=torch.long).cuda()
    with torch.no_grad():
        out = model(inp, return_dict=True)
    stds.append(float(out.logits.float().std().item()))
import numpy as np
arr = np.array(stds)
json.dump({'phi_star_proxy_raw_mean': float(arr.mean()), 'phi_star_proxy_raw_std': float(arr.std()), 'n_prompts': len(stds), 'note': 'in-pod logit-std proxy; canonical φ★ Mac-side'}, open('$RESULTS/phi_star_pre_lora.json','w'))
print('[A2] pre-LoRA φ★ proxy mean=', float(arr.mean()))
" 2>&1 | tee $RESULTS/phi_pre_log.txt

# ── Phase B: train (target ~2-2.5h on H100) ──
echo "[B] train start"
TRAIN_LOG=$RESULTS/train.log
python train.py \
    --base-model "$BASE_REPO" \
    --data-jsonl "$MIXED" \
    --output-dir "$CKPTS" \
    --lora-r 32 --lora-alpha 64 --lora-dropout 0.05 \
    --lr 3e-5 \
    --max-steps 6000 \
    --save-steps 1000 \
    --eval-step-triggers '2000,4000,6000' \
    --per-device-batch 8 --grad-accum 4 \
    --seq-len 512 --warmup-steps 300 \
    --seed 20260504 \
    > "$TRAIN_LOG" 2>&1 &
TRAIN_PID=$!
echo "[B] train pid=$TRAIN_PID"

# ── Phase B-watch: monitor sentinels for intermediate eval ──
DONE_STEPS=''
while kill -0 $TRAIN_PID 2>/dev/null; do
    for STEP in 2000 4000 6000; do
        case " $DONE_STEPS " in *" $STEP "*) continue ;; esac
        REQ=$(ls $CKPTS/sentinels/INTERMEDIATE_EVAL_REQUEST_step_${STEP}*.sentinel 2>/dev/null | head -1)
        if [ -z "$REQ" ]; then continue; fi
        CKPT_DIR="$CKPTS/checkpoint-${STEP}"
        echo "[B-watch] intermediate eval requested at step=$STEP"
        for j in $(seq 1 60); do
            if [ -f "$CKPT_DIR/adapter_model.safetensors" ]; then break; fi
            sleep 10
        done
        if [ ! -f "$CKPT_DIR/adapter_model.safetensors" ]; then
            echo "[B-watch] ckpt-${STEP} adapter never appeared in 600s — skipping"
            DONE_STEPS="$DONE_STEPS $STEP"
            continue
        fi
        INTER_OUT=$RESULTS/intermediate_dir_step${STEP}
        echo "[B-watch] running HellaSwag-200 + φ★ probe at step $STEP"
        # Run hellaswag eval via lm-eval with PEFT adapter loaded onto base mk2-v1
        lm_eval --model hf \
            --model_args "pretrained=${BASE_REPO},peft=${CKPT_DIR},dtype=bfloat16,trust_remote_code=True" \
            --tasks hellaswag --num_fewshot 5 --batch_size 16 --device cuda:0 --seed 42 --limit 200 \
            --output_path "$INTER_OUT" > $RESULTS/intermediate_eval_step${STEP}.log 2>&1 || \
            echo "[B-watch] WARN intermediate eval at step $STEP returned non-zero rc"
        INTER_RES=$(find "$INTER_OUT" -name 'results*.json' 2>/dev/null | head -1)
        if [ -n "$INTER_RES" ]; then
            cp -f "$INTER_RES" $RESULTS/intermediate_hs_step${STEP}.json
            INTER_VAL=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' $RESULTS/intermediate_hs_step${STEP}.json)
            echo "[B-watch] step=$STEP HS-200 acc_norm=$INTER_VAL"
            # F-CLM-LORA-1: drop > 5pp from baseline 0.255 → 0.205 ABORT trigger
            DROP=$(awk -v v="$INTER_VAL" 'BEGIN{ if (v == "null") print "NULL"; else if (v+0 < 0.205) print "FAIL"; else print "PASS" }')
            if [ "$DROP" = "FAIL" ]; then
                echo "[B-watch] EARLY-STOP TRIGGER F-CLM-LORA-1: HS-200=$INTER_VAL < 0.205"
                echo "{\"step\": $STEP, \"acc_norm\": \"$INTER_VAL\", \"trigger\": \"hs_5pp_drop_from_clm_v4_baseline\", \"ts_utc\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/EARLY_STOP.sentinel
                kill $TRAIN_PID 2>/dev/null || true
                sleep 5
                kill -9 $TRAIN_PID 2>/dev/null || true
                break
            fi
        fi
        DONE_STEPS="$DONE_STEPS $STEP"
    done
    sleep 30
done

wait $TRAIN_PID 2>/dev/null
TRAIN_RC=$?
echo "[B] train rc=$TRAIN_RC"

# Capture trainer_state.json
FINAL_TRAINER_STATE=$(find $CKPTS -name 'trainer_state.json' | sort | tail -1)
if [ -n "$FINAL_TRAINER_STATE" ]; then
    cp -f "$FINAL_TRAINER_STATE" $RESULTS/final_trainer_state.json
fi

# If early-stopped or train failed, emit COMPLETE.sentinel for cleanup
if [ -f "$RESULTS/EARLY_STOP.sentinel" ]; then
    echo "[B] early-stop path"
    cp -rf "$CKPTS/final" "$CKPTS/final_aborted" 2>/dev/null || true
    echo "{\"ok\": false, \"early_stopped\": true, \"finished_at\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/COMPLETE.sentinel
    exit 0
fi
if [ $TRAIN_RC -ne 0 ]; then
    echo "[B] train failed rc=$TRAIN_RC"
    tail -50 "$TRAIN_LOG"
    echo "{\"ok\": false, \"train_rc\": $TRAIN_RC, \"finished_at\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/COMPLETE.sentinel
    exit 1
fi

# ── Phase C: post-LoRA φ★ proxy + smoke (F-CLM-LORA-4) + shim compat (F-CLM-LORA-5) ──
echo "[C] post-LoRA probes"
FINAL_ADAPTER="$CKPTS/final"
if [ ! -f "$FINAL_ADAPTER/adapter_model.safetensors" ]; then
    FINAL_ADAPTER=$(ls -d $CKPTS/checkpoint-* 2>/dev/null | sort -V | tail -1)
fi
echo "[C] final adapter dir: $FINAL_ADAPTER"
python -c "
import json, os, torch, sys
sys.path.insert(0, '$WORK')
from transformers import AutoModelForCausalLM
from peft import PeftModel
from huggingface_hub import hf_hub_download
import sentencepiece as spm
spm_path = hf_hub_download(repo_id='$BASE_REPO', filename='tokenizer_64k_multilingual.model', token=os.environ['HF_TOKEN'])
sp = spm.SentencePieceProcessor(); sp.load(spm_path)
base = AutoModelForCausalLM.from_pretrained('$BASE_REPO', dtype=torch.bfloat16, trust_remote_code=True, token=os.environ['HF_TOKEN']).cuda().eval()
model = PeftModel.from_pretrained(base, '$FINAL_ADAPTER').cuda().eval()
prompts = ['The quick brown fox jumps over the lazy dog.', 'Hello, how are you today?', '안녕하세요. 오늘 기분이 어떠세요?', 'def factorial(n): return 1 if n<=1 else n*factorial(n-1)', 'In quantum mechanics, observation collapses the wavefunction.']
stds = []; finite_all = True
for p in prompts:
    ids = sp.encode(p, out_type=int)[:510]
    if not ids: continue
    inp = torch.tensor([ids], dtype=torch.long).cuda()
    with torch.no_grad():
        out = model(inp, return_dict=True)
    finite_all = finite_all and bool(torch.isfinite(out.logits).all().item())
    stds.append(float(out.logits.float().std().item()))
import numpy as np
arr = np.array(stds)
json.dump({'phi_star_proxy_raw_mean': float(arr.mean()), 'phi_star_proxy_raw_std': float(arr.std()), 'n_prompts': len(stds), 'finite': finite_all}, open('$RESULTS/phi_star_post_lora.json','w'))
json.dump({'smoke_pass': 'PASS' if finite_all and len(stds) >= 3 else 'FAIL', 'n_prompts_tested': len(stds), 'logits_finite_all': finite_all, 'logits_std_mean': float(arr.mean()) if len(stds) else None}, open('$RESULTS/post_lora_smoke.json','w'))
# F-CLM-LORA-5: shim compat — model already loaded via from_pretrained(trust_remote_code=True), so this is the gate itself
json.dump({'shim_compat': 'PASS' if finite_all else 'FAIL', 'note': 'load via AutoModelForCausalLM(trust_remote_code=True) + PeftModel.from_pretrained — both succeeded; logits finite'}, open('$RESULTS/post_lora_shim_compat.json','w'))
print('[C] post-LoRA: phi_proxy=', float(arr.mean()), 'finite=', finite_all)
" 2>&1 | tee $RESULTS/post_lora_probe.log

# ── Phase D: final 3-bench eval (limit=200, seed=42 — match retry-3 eval-rerun stderr) ──
echo "[D] final eval start"

run_bench() {
    local tkey=$1; local task=$2; local nshot=$3
    local out=$RESULTS/final_lora_${tkey}_dir
    local log=$RESULTS/final_${tkey}.log
    echo "[D] task=$task n=$nshot → $out"
    local t0=$(date -u +%s)
    lm_eval --model hf \
        --model_args "pretrained=${BASE_REPO},peft=${FINAL_ADAPTER},dtype=bfloat16,trust_remote_code=True" \
        --tasks "$task" \
        --num_fewshot "$nshot" \
        --batch_size 16 \
        --device cuda:0 \
        --seed 42 \
        --limit 200 \
        --output_path "$out" \
        > "$log" 2>&1
    local rc=$?
    local t1=$(date -u +%s)
    echo "[D] done task=$task rc=$rc wall=$((t1-t0))s"
    if [ $rc -ne 0 ]; then echo "[FAIL]"; tail -50 "$log"; fi
    if [ -d "$out" ]; then
        find "$out" -name 'results*.json' -exec cp {} $RESULTS/final_lora_${tkey}.json \;
    fi
    return $rc
}

run_bench 'hellaswag' 'hellaswag' 5
run_bench 'mmlu' 'mmlu' 0
run_bench 'triviaqa' 'triviaqa' 5

# ── Phase E: emit COMPLETE.sentinel ──
echo "{\"ok\": true, \"finished_at\": \"$(date -u +%FT%TZ)\", \"phases\": [\"corpus_mix\", \"phi_pre\", \"train\", \"intermediate_eval\", \"phi_post\", \"final_eval\"]}" > $RESULTS/COMPLETE.sentinel
echo "[orch] complete"
