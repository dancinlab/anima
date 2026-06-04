#!/bin/bash
# dl7b_pod_run.sh — on-pod runner for the default-lane 7B fire (single leak-safe H100).
# All artifacts under /workspace (persistent volume). Corpus build -> 7B train -> STRICT p7 eval.
set -euo pipefail
WS=/workspace/dl7b
mkdir -p "$WS"
cd "$WS"

echo "[pod] python + torch + cuda check"
python3 -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),torch.cuda.get_device_name(0))"
pip -q install datasets bitsandbytes 2>&1 | tail -2 || echo "[pod] pip warn (continuing)"

echo "[pod] === STAGE 1: GB-scale default-lane corpus (en/fr/de/es/ko wiki + v2 chat blend) ==="
# fetch the v2 default-lane chat surfaces (small) to blend the chat register
python3 - <<'PY'
import os
try:
    from huggingface_hub import hf_hub_download, snapshot_download
    p = snapshot_download(repo_id="dancinlab/anima-corpus-5lang-unified-v2", repo_type="dataset")
    # flatten all text files into one v2_default.txt
    import glob
    parts=[]
    for fp in sorted(glob.glob(os.path.join(p,"**","*"), recursive=True)):
        if fp.lower().endswith((".txt",)):
            parts.append(open(fp,"rb").read())
    blob=b"\n\n".join(parts)
    open("/workspace/dl7b/v2_default.txt","wb").write(blob)
    print("[pod] v2 chat blend bytes:",len(blob))
except Exception as e:
    print("[pod] v2 blend WARN (wiki-only fallback):",repr(e))
    open("/workspace/dl7b/v2_default.txt","wb").write(b"")
PY

python3 build_default_lane_7b_corpus.py --out /workspace/dl7b/corpus.txt \
    --mb-per-lang 80 --date 20231101 --chat-blend /workspace/dl7b/v2_default.txt

echo "[pod] === STAGE 2: 7B dual-engine train (d4096/L21 ~7.05B, bf16+grad-ckpt+AdamW8bit) ==="
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
python3 default_lane_7b_train_eval.py \
    --corpus /workspace/dl7b/corpus.txt \
    --out-dir /workspace/dl7b/out \
    --steps 6000 --batch 8 --grad-accum 4 --block 512 \
    --d-model 4096 --n-layer 21 --n-head 32 \
    --lr 1.6e-4 --warmup 200 --ckpt-every 250 --eval-every 2000 --seed 42

echo "[pod] === DONE — artifacts in /workspace/dl7b/out ==="
ls -la /workspace/dl7b/out
sha256sum /workspace/dl7b/out/default_lane_7b.pt || true
