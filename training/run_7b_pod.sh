#!/usr/bin/env bash
# run_7b_pod.sh — on-pod driver for the 7B chat+persona 2-stage fine-tune.
# Downloads base 7B ckpt + trainer + both corpora to /workspace, runs train+eval, then demo.
# Requires: HF_TOKEN env (public repos, but authed re-download for sha-verify). CUDA GPU.
set -euo pipefail
WS=/workspace
OUT=$WS/out
mkdir -p "$OUT"
cd "$WS"

echo "=== [pod] env setup ==="
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
pip install -q --upgrade pip
pip install -q "torch>=2.4" bitsandbytes huggingface_hub 2>&1 | tail -3 || true

echo "=== [pod] download base 7B ckpt + corpora ==="
python3 - <<'PY'
from huggingface_hub import hf_hub_download
import shutil, os
WS="/workspace"
# base 7B ckpt (14.5GB)
p = hf_hub_download("dancinlab/clm-v1-ref-pytorch-cuda-7b", "clm_ref_pytorch_cuda_7b.pt", repo_type="model")
shutil.copy(p, f"{WS}/clm_ref_pytorch_cuda_7b.pt")
# chat corpus
p = hf_hub_download("dancinlab/anima-chat-corpus-mix-70wiki-30dialogue", "chat_corpus_mix.txt", repo_type="dataset")
shutil.copy(p, f"{WS}/chat_corpus_mix.txt")
# persona corpus
p = hf_hub_download("dancinlab/anima-persona-sns-corpus", "persona_sns_corpus.txt", repo_type="dataset")
shutil.copy(p, f"{WS}/persona_sns_corpus.txt")
for f in ["clm_ref_pytorch_cuda_7b.pt","chat_corpus_mix.txt","persona_sns_corpus.txt"]:
    print(f, os.path.getsize(f"{WS}/{f}"), "bytes")
PY

echo "=== [pod] PHILOSOPHY GATE — grep corpora for role/persona/character tags (MUST be 0) ==="
for c in chat_corpus_mix.txt persona_sns_corpus.txt; do
  n=$(grep -cE '\[role:|\[persona:|\[character:' "$WS/$c" || true)
  echo "  $c : [role:/[persona:/[character: count = ${n:-0}"
done

echo "=== [pod] STAGE-A + STAGE-B fine-tune + p7 eval ==="
cd "$WS"
python3 chat_persona_7b_train_eval.py \
  --base-ckpt "$WS/clm_ref_pytorch_cuda_7b.pt" \
  --chat-corpus "$WS/chat_corpus_mix.txt" \
  --persona-corpus "$WS/persona_sns_corpus.txt" \
  --out-dir "$OUT" \
  --stage-a-steps "${STAGE_A_STEPS:-600}" --stage-b-steps "${STAGE_B_STEPS:-600}" \
  --batch "${BATCH:-8}" --block 512 --lr "${LR:-2e-5}" --warmup 40 --opt adamw8bit --seed 42 \
  2>&1 | tee "$OUT/train_eval.log"

echo "=== [pod] runnable demo transcript ==="
python3 chat_persona_7b_demo.py --ckpt "$OUT/chat_persona_7b_stageB.pt" 2>&1 | tee "$OUT/demo_transcript.txt"

echo "=== [pod] sha256 of output ckpts ==="
sha256sum "$OUT"/chat_7b_stageA.pt "$OUT"/chat_persona_7b_stageB.pt | tee "$OUT/ckpt_sha256.txt"
echo "=== [pod] DONE ==="
touch "$OUT/POD_DONE"
