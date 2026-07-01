#!/usr/bin/env bash
# remote_run.sh — on-pod one-shot: fetch R2 subset -> train CLMConvMoE -> .clm v0.2.
# Runs under nohup; all output to /workspace/mid_fire.log. POLL-INLINE from laptop.
set -uo pipefail
cd /workspace

echo "=== REMOTE FIRE START $(date -u +%FT%TZ) ==="
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader || true

# 0. deps
pip -q install boto3 >/dev/null 2>&1
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0))"

# 1. corpus fetch (balanced 5-lang incl ko)
export CORPUS_OUT=/workspace/mid_corpus_5lang.bytes
python3 /workspace/job/remote_fetch_corpus.py
ls -la "$CORPUS_OUT"

# 2. train CLMConvMoE -> serialize .clm v0.2 (imports clm_serialize_v2)
cd /workspace/job/repo
echo "=== TRAIN START $(date -u +%FT%TZ) ==="
python3 CLM/train/train_lane_p.py \
  --d-model 768 --steps 6000 --seq-len 256 --batch-size 64 --lr 3e-4 --bf16 \
  --corpus "$CORPUS_OUT" \
  --ckpt-out /workspace/mid_convmoe.pt \
  --clm-out  /workspace/mid_convmoe.clm \
  --json-out /workspace/mid_result.json
TRAIN_RC=$?
echo "=== TRAIN RC=$TRAIN_RC ==="

# 3. verify clm_decodable (pure-stdlib mirror of clm_decode.hexa)
echo "=== VERIFY CLM_V2 ==="
GOLDEN_CLM="" python3 CLM/model/verify_clm_v2.py 2>&1 | tail -6
python3 - <<'PY'
import sys; sys.path.insert(0,'CLM/model')
from verify_clm_v2 import clm_decodable, parse_clm
p="/workspace/mid_convmoe.clm"
dec=clm_decodable(p); g=parse_clm(p)
print("MID_CLM_DECODABLE", "TRUE" if dec else "FALSE",
      "nblk", g["nblk"], "clmx", g["clmx_found"], "n_ext", g["n_ext"],
      "block0", g["blocks"][0] if g["blocks"] else None)
PY

echo "=== REMOTE FIRE DONE $(date -u +%FT%TZ) RC=$TRAIN_RC ==="
echo "FIRE_COMPLETE_SENTINEL"
