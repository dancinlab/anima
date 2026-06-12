#!/usr/bin/env bash
# h1146_anchor_pod_run.sh — pod-side driver for H_1146 ANCHOR-CONDITIONED DECODE.
# SELF-TERMINATING: measure 3 arms -> HF-upload results -> self-terminate via the
# pod-resident RUNPOD_KEY (zero idle burn even if the orchestrator turn ends).
#
#   1) pull dancinlab/anima-clm-7b-h1141-g1pass-step6500 (the .pt) + verify sha256
#   2) build the deterministic en 300MB grounding corpus (== h1143 probe corpus,
#      sha 80ba6b48...) so the 40 openers + corpus-absence predicate are IDENTICAL
#   3) h1146_anchor_conditioned_decode.py --ckpt ... -> 3 arms (uncond/true/wrong)
#      -> g5_result_*.json + h1146_fabrate_*.json + h1146_anchor_result.json
#   4) HF-upload the result JSONs to a PRIVATE repo (WIP measurement artifacts)
#   5) print H1146_DONE sentinel, then SELF-TERMINATE (podTerminate) via RUNPOD_KEY.
# Tokens come from env (HF_TOKEN, RUNPOD_KEY, RUNPOD_POD_ID) — never argv.
set -uo pipefail
exec > >(tee -a /workspace/h1146.log) 2>&1
echo "[pod] start $(date -u)"
cd /workspace

self_terminate() {
  echo "[pod] self-terminate pod=${RUNPOD_POD_ID:-?} $(date -u)"
  if [ -n "${RUNPOD_KEY:-}" ] && [ -n "${RUNPOD_POD_ID:-}" ]; then
    curl -s -X POST https://api.runpod.io/graphql \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${RUNPOD_KEY}" \
      -d "{\"query\":\"mutation { podTerminate(input:{podId:\\\"${RUNPOD_POD_ID}\\\"}) }\"}" || true
  fi
  # belt-and-suspenders: also try runpodctl if present
  command -v runpodctl >/dev/null 2>&1 && runpodctl remove pod "${RUNPOD_POD_ID:-}" >/dev/null 2>&1 || true
}

export PIP_ROOT_USER_ACTION=ignore
pip install -q -U "huggingface_hub>=0.23" pyarrow 2>&1 | tail -2 || true
python3 -c "import torch; print('[torch]', torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"

REPO="dancinlab/anima-clm-7b-h1141-g1pass-step6500"
CKFILE="h1141_g1pass_step6500.pt"
EXPECT_SHA="4de903714112c26c826a983797e5dfea0c7b3c1f19f15a34dd35822f33e245d9"

# 1) pull ckpt + verify sha256
echo "[pod] downloading 7B ckpt from HF ..."
python3 - <<PY
import os
from huggingface_hub import hf_hub_download
p = hf_hub_download("$REPO", "$CKFILE", token=os.environ["HF_TOKEN"], local_dir="/workspace/ck")
print("CK", p)
PY
CK=/workspace/ck/$CKFILE
GOT=$(sha256sum "$CK" | cut -d' ' -f1)
echo "[pod] 7B sha256 got=$GOT expect=$EXPECT_SHA"
[ "$GOT" = "$EXPECT_SHA" ] || { echo "[pod] SHA MISMATCH -- abort"; touch /workspace/H1146_FAILED; self_terminate; exit 1; }

# 2) build the en 300MB grounding corpus (deterministic; == h1143/h1144/h1145 probe corpus)
echo "[pod] building 1200MB en corpus then slicing the 300MB head ..."
python3 /workspace/build_wiki5_bigcorpus_en.py /workspace/corpus_en_1200mb.txt 1258291200 /workspace/wk 2>&1 | tail -8
head -c 314572800 /workspace/corpus_en_1200mb.txt > /workspace/corpus_en_300mb.txt
PROBE_SHA=$(sha256sum /workspace/corpus_en_300mb.txt | cut -d' ' -f1)
echo "[pod] probe-corpus(300MB) sha256=$PROBE_SHA (expect 80ba6b48943e1943c4c3a0753c2bc594132acd7f30046733f4bf0102020c979d)"

# 3) run the 3-arm anchor-conditioned-decode measure
echo "[pod] running H_1146 3-arm anchor-conditioned-decode measure ..."
python3 /workspace/h1146_anchor_conditioned_decode.py \
    --ckpt "$CK" --corpus /workspace/corpus_en_300mb.txt \
    --en_mb 300 --n_sentences 40 --outdir /workspace
[ -f /workspace/h1146_anchor_result.json ] || { echo "[pod] result missing"; touch /workspace/H1146_FAILED; self_terminate; exit 1; }

echo "[pod] === H_1146 RESULT ==="
python3 -c "import json; d=json.load(open('/workspace/h1146_anchor_result.json')); print('fab=',d['fab_rate'],'F1=',d['F1_anchor_grounds'],'F2=',d['F2_information_not_length'],'tier=',d['tier'])"

# 4) HF-upload result JSONs (PRIVATE — WIP measurement artifacts; a_hf_autonomous)
echo "[pod] uploading result JSONs to HF (private) ..."
python3 - <<PY || echo "[pod] HF upload soft-fail (artifacts still on pod for scp)"
import os
from huggingface_hub import HfApi
api = HfApi(token=os.environ["HF_TOKEN"])
repo = "dancinlab/anima-h1146-anchor-conditioned-decode"
api.create_repo(repo, repo_type="dataset", private=True, exist_ok=True)
for f in ["h1146_anchor_result.json","h1146_fabrate_uncond.json","h1146_fabrate_true.json",
          "h1146_fabrate_wrong.json","g5_result_uncond.json","g5_result_true.json",
          "g5_result_wrong.json","h1146.log"]:
    p="/workspace/"+f
    if os.path.exists(p):
        api.upload_file(path_or_fileobj=p, path_in_repo=f, repo_id=repo, repo_type="dataset")
        print("uploaded", f)
print("HF_UPLOAD_DONE", repo)
PY

echo "H1146_DONE $(date -u)"
echo "[pod] end $(date -u)"
# 5) self-terminate (zero idle burn). Orchestrator will 404-verify independently.
self_terminate
