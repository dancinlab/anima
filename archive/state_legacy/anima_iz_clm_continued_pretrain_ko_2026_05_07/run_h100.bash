#!/bin/bash
# BG-IZ H100-side runner — CLM mk2-v1 continued pre-training on Korean conversational mass.
# raw#37 transient py on Linux pod (transformers + torch + sentencepiece + huggingface_hub permitted; killed with pod).
# Lesson Q reconciliation: continued PRE-TRAINING (raw next-token CE), NOT instruction SFT.
set -uo pipefail

WORK=/workspace/anima_iz_pretrain
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

BASE_REPO='need-singularity/clm-v4-mk2-v1'
RESULTS=$WORK/results
CKPTS=$WORK/ckpts
CORPUS=$WORK/corpus/corpus_ko_chat_template.txt
mkdir -p $RESULTS $CKPTS

echo "[orch] start ts=$(date -u +%FT%TZ)"

# Setup pinned deps (transformers >=4.51 for dtype-kwarg compat per Lesson L14)
echo "[setup] installing pip packages"
pip install -q --no-input \
    'transformers>=4.51,<4.60' 'accelerate>=0.34' \
    'huggingface_hub>=0.25' \
    safetensors sentencepiece 2>&1 | tail -5

# HF auth
hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true
echo "[setup] hf auth: $(hf auth whoami 2>&1 | head -1 || huggingface-cli whoami 2>&1 | head -1)"

# Download CLM mk2-v1 base (safetensors + custom code; skip best.pt)
echo "[setup] downloading $BASE_REPO base"
hf download "$BASE_REPO" --exclude 'best.pt' --local-dir $WORK/clm_base 2>&1 | tail -3 \
    || huggingface-cli download "$BASE_REPO" --exclude best.pt --local-dir $WORK/clm_base 2>&1 | tail -3
ls -la $WORK/clm_base | head -10

echo "[orch] versions: torch=$(python -c 'import torch; print(torch.__version__)') transformers=$(pip show transformers 2>/dev/null | awk '/^Version/{print $2}')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

# ── Phase A: pre-pretrain phi-star proxy + smoke (~30s, sanity check) ──
echo "[A] pre-pretrain phi-star proxy"
python -c "
import json, os, torch, sys
from transformers import AutoModelForCausalLM
import sentencepiece as spm
sys.path.insert(0, '$WORK/clm_base')
sp = spm.SentencePieceProcessor(); sp.load('$WORK/clm_base/tokenizer_64k_multilingual.model')
model = AutoModelForCausalLM.from_pretrained('$WORK/clm_base', dtype=torch.bfloat16, trust_remote_code=True).cuda().eval()
prompts = ['안녕하세요. 오늘 기분이 어떠세요?', 'def factorial(n): return 1 if n<=1 else n*factorial(n-1)', '의식이란 무엇인가?']
stds = []
for p in prompts:
    ids = sp.encode(p, out_type=int)[:510]
    if not ids: continue
    inp = torch.tensor([ids], dtype=torch.long).cuda()
    with torch.no_grad(): out = model(inp, return_dict=True)
    stds.append(float(out.logits.float().std().item()))
import numpy as np
arr = np.array(stds) if stds else np.array([0.0])
json.dump({'phi_star_proxy_pre_pretrain': float(arr.mean()), 'phi_star_proxy_std': float(arr.std()), 'n_prompts': len(stds)}, open('$RESULTS/phi_star_pre_pretrain.json','w'))
del model; torch.cuda.empty_cache()
print('[A] pre-pretrain phi-star OK')"

# ── Phase B: continued pre-training ──
echo "[B] continued pre-training start"
python anima_iz_train.py \
    --base "$WORK/clm_base" \
    --corpus "$CORPUS" \
    --out-dir "$CKPTS" \
    --steps 6000 \
    --lr 1e-5 \
    --per-device-batch 4 \
    --grad-accum 8 \
    --ctx 512 \
    --warmup 300 \
    --weight-decay 0.01 \
    --save-every 1000 \
    --seed 42 \
    --dtype bf16 \
    2>&1 | tee $RESULTS/train.log

TRAIN_RC=${PIPESTATUS[0]}
echo "[B] train exit rc=$TRAIN_RC"

# ── Phase C: post-pretrain phi-star proxy + sentinel ──
if [ $TRAIN_RC -eq 0 ] && [ -f $CKPTS/ckpt_final.pt ]; then
    echo "[C] post-pretrain phi-star proxy"
    python -c "
import json, os, torch, sys
from transformers import AutoModelForCausalLM
import sentencepiece as spm
sys.path.insert(0, '$WORK/clm_base')
sp = spm.SentencePieceProcessor(); sp.load('$WORK/clm_base/tokenizer_64k_multilingual.model')
model = AutoModelForCausalLM.from_pretrained('$WORK/clm_base', dtype=torch.bfloat16, trust_remote_code=True)
state = torch.load('$CKPTS/ckpt_final.pt', map_location='cpu', weights_only=False)
model.load_state_dict(state['model'], strict=False)
model = model.cuda().eval()
prompts = ['안녕하세요. 오늘 기분이 어떠세요?', '의식이란 무엇인가?', '한국어 가능?']
stds, samples = [], []
for p in prompts:
    ids = [1] + sp.encode(p, out_type=int)[:128]
    inp = torch.tensor([ids], dtype=torch.long).cuda()
    with torch.no_grad():
        out = model(inp, return_dict=True)
        stds.append(float(out.logits.float().std().item()))
        gen = model.generate(inp, max_new_tokens=48, do_sample=True, temperature=0.7, top_p=0.9, repetition_penalty=1.3, pad_token_id=0, eos_token_id=2)
        samples.append({'prompt': p, 'response': sp.decode([i for i in gen[0,inp.shape[1]:].tolist() if i not in (0,1,2)])})
import numpy as np
arr = np.array(stds)
json.dump({'phi_star_proxy_post_pretrain': float(arr.mean()), 'phi_star_proxy_std': float(arr.std()), 'samples': samples}, open('$RESULTS/phi_star_post_pretrain.json','w'), ensure_ascii=False, indent=2)
print('[C] post-pretrain phi-star OK; samples saved')"

    # Save final ckpt to results dir for sync
    cp $CKPTS/ckpt_final.pt $RESULTS/ckpt_final.pt 2>/dev/null
    cp $CKPTS/ckpt_step_*.pt $RESULTS/ 2>/dev/null
    cp $RESULTS/train.log $RESULTS/train_full.log 2>/dev/null

    echo '{"ok": true, "train_rc": '$TRAIN_RC', "final_ckpt": "ckpt_final.pt"}' > $RESULTS/COMPLETE.sentinel
    echo "[orch] DONE ts=$(date -u +%FT%TZ)"
else
    echo '{"ok": false, "train_rc": '$TRAIN_RC', "error": "training_failed_or_no_ckpt"}' > $RESULTS/COMPLETE.sentinel
    echo "[orch] FAILED ts=$(date -u +%FT%TZ)"
fi
