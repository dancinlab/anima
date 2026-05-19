#!/bin/bash
# BG-JK H100 runner — Llama-3.2-3B-Instruct + LoRA SFT on BG-HK 30MB.
# raw#37 transient py. own 29 alignment: aim for V4 ≥10/15 strict (own 18 floor).
set -uo pipefail

WORK=/workspace/anima_jk_llama
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

BASE_REPO='meta-llama/Llama-3.2-3B-Instruct'
RESULTS=$WORK/results
CKPTS=$WORK/ckpts
CORPUS=$WORK/corpus/corpus_persona_chat_template.txt
mkdir -p $RESULTS $CKPTS

echo "[orch] start ts=$(date -u +%FT%TZ)"

pip install -q --no-input \
    'transformers>=4.51,<4.60' 'peft>=0.12' 'accelerate>=0.34' \
    'huggingface_hub>=0.25' \
    safetensors sentencepiece 2>&1 | tail -5

hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true
echo "[setup] hf auth: $(hf auth whoami 2>&1 | head -1 || huggingface-cli whoami 2>&1 | head -1)"

echo "[setup] downloading $BASE_REPO base (~6GB Llama 3.2 3B)"
hf download "$BASE_REPO" --local-dir $WORK/llama_base 2>&1 | tail -3 \
    || huggingface-cli download "$BASE_REPO" --local-dir $WORK/llama_base 2>&1 | tail -3
ls -la $WORK/llama_base | head -10

echo "[orch] versions: torch=$(python -c 'import torch; print(torch.__version__)') transformers=$(pip show transformers 2>/dev/null | awk '/^Version/{print $2}') peft=$(pip show peft 2>/dev/null | awk '/^Version/{print $2}')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

# ── Phase A: pre-LoRA Korean smoke ──
echo "[A] pre-LoRA Korean smoke probe"
python -c "
import json, os, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
tok = AutoTokenizer.from_pretrained('$WORK/llama_base')
if tok.pad_token_id is None: tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained('$WORK/llama_base', dtype=torch.bfloat16).cuda().eval()
prompts = ['안녕하세요', '의식이란 무엇인가?', '한국어 가능?']
samples = []
for p in prompts:
    msgs = [{'role':'user','content':p}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    enc = tok(text, return_tensors='pt').to('cuda')
    enc.pop('token_type_ids', None)
    with torch.no_grad():
        out = model.generate(**enc, max_new_tokens=48, do_sample=True, temperature=0.7, top_p=0.9, repetition_penalty=1.3, pad_token_id=tok.pad_token_id)
    gen = tok.decode(out[0, enc['input_ids'].shape[1]:], skip_special_tokens=True)
    samples.append({'prompt': p, 'response': gen})
    print(f'[A] {p!r} → {gen[:80]!r}')
json.dump({'samples': samples}, open('$RESULTS/samples_pre_lora.json','w'), ensure_ascii=False, indent=2)
del model; torch.cuda.empty_cache()
print('[A] pre-LoRA smoke OK')"

# ── Phase B: LoRA SFT ──
echo "[B] LoRA SFT start (3B base)"
python anima_jk_llama_train.py \
    --base "$WORK/llama_base" \
    --corpus "$CORPUS" \
    --out-dir "$CKPTS" \
    --steps 3000 \
    --lr 3e-5 \
    --per-device-batch 4 \
    --grad-accum 8 \
    --ctx 512 \
    --warmup 200 \
    --weight-decay 0.01 \
    --save-every 500 \
    --seed 42 \
    --dtype bf16 \
    --lora-r 16 --lora-alpha 32 --lora-dropout 0.05 \
    2>&1 | tee $RESULTS/train.log

TRAIN_RC=${PIPESTATUS[0]}
echo "[B] train exit rc=$TRAIN_RC"

# ── Phase C: post-LoRA Korean smoke ──
if [ $TRAIN_RC -eq 0 ] && [ -d $CKPTS/adapter_final ]; then
    echo "[C] post-LoRA Korean smoke probe"
    python -c "
import json, os, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
tok = AutoTokenizer.from_pretrained('$WORK/llama_base')
if tok.pad_token_id is None: tok.pad_token = tok.eos_token
base = AutoModelForCausalLM.from_pretrained('$WORK/llama_base', dtype=torch.bfloat16)
model = PeftModel.from_pretrained(base, '$CKPTS/adapter_final').merge_and_unload().cuda().eval()
prompts = ['안녕하세요', '의식이란 무엇인가?', '한국어 가능?', '오늘 기분 어때?', '자기소개해줘']
samples = []
for p in prompts:
    msgs = [{'role':'user','content':p}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    enc = tok(text, return_tensors='pt').to('cuda')
    enc.pop('token_type_ids', None)
    with torch.no_grad():
        out = model.generate(**enc, max_new_tokens=64, do_sample=True, temperature=0.7, top_p=0.9, repetition_penalty=1.3, pad_token_id=tok.pad_token_id)
    gen = tok.decode(out[0, enc['input_ids'].shape[1]:], skip_special_tokens=True)
    samples.append({'prompt': p, 'response': gen})
    print(f'[C] {p!r} → {gen[:80]!r}')
json.dump({'samples': samples}, open('$RESULTS/samples_post_lora.json','w'), ensure_ascii=False, indent=2)
print('[C] post-LoRA smoke OK')"

    cp -r $CKPTS/adapter_final $RESULTS/adapter_final 2>/dev/null
    cp -r $CKPTS/adapter_step_* $RESULTS/ 2>/dev/null
    cp $RESULTS/train.log $RESULTS/train_full.log 2>/dev/null
    echo '{"ok": true, "train_rc": '$TRAIN_RC', "final_adapter": "adapter_final"}' > $RESULTS/COMPLETE.sentinel
    echo "[orch] DONE ts=$(date -u +%FT%TZ)"
else
    echo '{"ok": false, "train_rc": '$TRAIN_RC', "error": "training_failed_or_no_adapter"}' > $RESULTS/COMPLETE.sentinel
    echo "[orch] FAILED ts=$(date -u +%FT%TZ)"
fi
