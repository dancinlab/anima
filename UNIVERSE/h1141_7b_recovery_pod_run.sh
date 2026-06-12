#!/usr/bin/env bash
# h1141_7b_recovery_pod_run.sh — pod-side driver for the 7B G5-L2 recovery
# diagnosis. Builds the en corpus slice, pulls the ckpt, runs the 3-probe
# diagnostic, prints DIAG_DONE, leaves the result JSON on /workspace.
# Tokens come from env (HF_TOKEN) — never argv. Self-terminates via GraphQL at end.
set -uo pipefail
exec > >(tee -a /workspace/diag.log) 2>&1
echo "[pod] start $(date -u)"
cd /workspace

export PIP_ROOT_USER_ACTION=ignore
pip install -q -U "huggingface_hub>=0.23" pyarrow 2>&1 | tail -2 || true
python3 -c "import torch; print('[torch]', torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"

# 1) pull the ckpt from HF (PRIVATE) — verify sha256
echo "[pod] downloading ckpt from HF ..."
python3 - <<'PY'
import os
from huggingface_hub import hf_hub_download
p = hf_hub_download("dancinlab/anima-clm-7b-h1141-g1pass-step6500",
                    "h1141_g1pass_step6500.pt", token=os.environ["HF_TOKEN"],
                    local_dir="/workspace/ckpt")
print("CKPT", p)
PY
CKPT=/workspace/ckpt/h1141_g1pass_step6500.pt
EXPECT=4de903714112c26c826a983797e5dfea0c7b3c1f19f15a34dd35822f33e245d9
GOT=$(sha256sum "$CKPT" | cut -d' ' -f1)
echo "[pod] ckpt sha256 got=$GOT expect=$EXPECT"
[ "$GOT" = "$EXPECT" ] || { echo "[pod] SHA MISMATCH -- abort"; touch /workspace/DIAG_FAILED; exit 1; }

# 2) build the EN corpus slice (first lang in the deterministic concat = English).
# Only need 300MB en for the L2 probe; build_wiki5 streams en first.
echo "[pod] building en corpus slice (300MB) ..."
python3 /workspace/build_wiki5_bigcorpus_en.py /workspace/corpus_en.txt 314572800 /workspace/wk 2>&1 | tail -8

# 3) run the diagnostic (en_mb 300 = the en slice; corpus_en.txt IS the en portion)
echo "[pod] running recovery diagnostic ..."
python3 /workspace/h1141_7b_recovery_diag.py \
  --ckpt "$CKPT" --corpus /workspace/corpus_en.txt --en_mb 300 \
  --n_sentences 40 --out /workspace/h1141_recovery_diag.json
RC=$?
echo "[pod] diag rc=$RC"
[ $RC -eq 0 ] && echo "DIAG_DONE $(date -u)" || { echo "DIAG_FAILED rc=$RC"; touch /workspace/DIAG_FAILED; }
echo "[pod] end $(date -u)"
