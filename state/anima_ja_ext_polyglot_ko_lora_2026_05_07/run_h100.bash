#!/bin/bash
# BG-JA-EXT H100-side runner — Polyglot-Ko-1.3B + LoRA SFT on BG-HK 30MB Korean persona.
# raw#37 transient py on Linux pod (transformers + torch + peft + huggingface_hub permitted; killed with pod).
# CLM-only directive partial breach — explicitly user-approved 2026-05-07 after BG-IZ Lesson L extension.
set -uo pipefail

WORK=/workspace/anima_ja_ext
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

BASE_REPO='EleutherAI/polyglot-ko-1.3b'
RESULTS=$WORK/results
CKPTS=$WORK/ckpts
CORPUS=$WORK/corpus/corpus_persona_chat_template.txt
mkdir -p $RESULTS $CKPTS

echo "[orch] start ts=$(date -u +%FT%TZ)"

# Setup pinned deps
echo "[setup] installing pip packages"
pip install -q --no-input \
    'transformers>=4.51,<4.60' 'peft>=0.12' 'accelerate>=0.34' \
    'huggingface_hub>=0.25' \
    safetensors sentencepiece 2>&1 | tail -5

# HF auth
hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true
echo "[setup] hf auth: $(hf auth whoami 2>&1 | head -1 || huggingface-cli whoami 2>&1 | head -1)"

# Download Polyglot-Ko-1.3B base (~3GB)
echo "[setup] downloading $BASE_REPO base (~3GB)"
hf download "$BASE_REPO" --local-dir $WORK/polyglot_base 2>&1 | tail -3 \
    || huggingface-cli download "$BASE_REPO" --local-dir $WORK/polyglot_base 2>&1 | tail -3
ls -la $WORK/polyglot_base | head -10

echo "[orch] versions: torch=$(python -c 'import torch; print(torch.__version__)') transformers=$(pip show transformers 2>/dev/null | awk '/^Version/{print $2}') peft=$(pip show peft 2>/dev/null | awk '/^Version/{print $2}')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

# ── Phase A: pre-LoRA Korean smoke (~15s, sanity check) ──
echo "[A] pre-LoRA Korean smoke probe"
python -c "
import json, os, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
tok = AutoTokenizer.from_pretrained('$WORK/polyglot_base')
if tok.pad_token_id is None: tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained('$WORK/polyglot_base', dtype=torch.bfloat16).cuda().eval()
prompts = ['### 질문\n안녕하세요\n\n### 답변\n', '### 질문\n의식이란 무엇인가?\n\n### 답변\n', '### 질문\n한국어 가능?\n\n### 답변\n']
samples = []
for p in prompts:
    inp = tok(p, return_tensors='pt').to('cuda')
    with torch.no_grad():
        out = model.generate(**inp, max_new_tokens=48, do_sample=True, temperature=0.7, top_p=0.9, repetition_penalty=1.3, pad_token_id=tok.pad_token_id)
    gen = tok.decode(out[0, inp['input_ids'].shape[1]:], skip_special_tokens=True)
    samples.append({'prompt': p, 'response': gen})
    print(f'[A] {p[:30]!r} → {gen[:80]!r}')
json.dump({'samples': samples}, open('$RESULTS/samples_pre_lora.json','w'), ensure_ascii=False, indent=2)
del model; torch.cuda.empty_cache()
print('[A] pre-LoRA smoke OK')"

# ── Phase B: LoRA SFT ──
echo "[B] LoRA SFT start"
python anima_ja_ext_train.py \
    --base "$WORK/polyglot_base" \
    --corpus "$CORPUS" \
    --out-dir "$CKPTS" \
    --steps 3000 \
    --lr 3e-5 \
    --per-device-batch 8 \
    --grad-accum 4 \
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

# ── Phase C: post-LoRA Korean smoke + sentinel ──
if [ $TRAIN_RC -eq 0 ] && [ -d $CKPTS/adapter_final ]; then
    echo "[C] post-LoRA Korean smoke probe"
    python -c "
import json, os, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
tok = AutoTokenizer.from_pretrained('$WORK/polyglot_base')
if tok.pad_token_id is None: tok.pad_token = tok.eos_token
base = AutoModelForCausalLM.from_pretrained('$WORK/polyglot_base', dtype=torch.bfloat16)
model = PeftModel.from_pretrained(base, '$CKPTS/adapter_final').merge_and_unload().cuda().eval()
prompts = ['### 질문\n안녕하세요\n\n### 답변\n', '### 질문\n의식이란 무엇인가?\n\n### 답변\n', '### 질문\n한국어 가능?\n\n### 답변\n', '### 질문\n오늘 기분 어때?\n\n### 답변\n', '### 질문\n자기소개해줘\n\n### 답변\n']
samples = []
for p in prompts:
    inp = tok(p, return_tensors='pt').to('cuda')
    with torch.no_grad():
        out = model.generate(**inp, max_new_tokens=64, do_sample=True, temperature=0.7, top_p=0.9, repetition_penalty=1.3, pad_token_id=tok.pad_token_id)
    gen = tok.decode(out[0, inp['input_ids'].shape[1]:], skip_special_tokens=True)
    samples.append({'prompt': p, 'response': gen})
    print(f'[C] {p[:30]!r} → {gen[:80]!r}')
json.dump({'samples': samples}, open('$RESULTS/samples_post_lora.json','w'), ensure_ascii=False, indent=2)
print('[C] post-LoRA smoke OK; samples saved')"

    # Save adapter_final to results dir
    cp -r $CKPTS/adapter_final $RESULTS/adapter_final 2>/dev/null
    cp -r $CKPTS/adapter_step_* $RESULTS/ 2>/dev/null
    cp $RESULTS/train.log $RESULTS/train_full.log 2>/dev/null

    echo '{"ok": true, "train_rc": '$TRAIN_RC', "final_adapter": "adapter_final"}' > $RESULTS/COMPLETE.sentinel
    echo "[orch] DONE ts=$(date -u +%FT%TZ)"
else
    echo '{"ok": false, "train_rc": '$TRAIN_RC', "error": "training_failed_or_no_adapter"}' > $RESULTS/COMPLETE.sentinel
    echo "[orch] FAILED ts=$(date -u +%FT%TZ)"
fi
