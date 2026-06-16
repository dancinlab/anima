#!/usr/bin/env bash
# h1144_grounding_pod_run.sh — pod-side driver for the H_1144 grounding continue-train.
# PROBE-FIRST: pull base ckpt -> build corpus -> LEG1 probe (2000 steps) ->
# regenerate 40 factual continuations -> re-measure fab-rate (h1143 harness VERBATIM)
# -> FROZEN slope rule -> conditionally converge -> full a7b_pass battery.
# Self-uploads result ckpt to HF (PRIVATE) BEFORE printing the DONE sentinel.
# Tokens come from env (HF_TOKEN) — never argv. NO teardown here (orchestrator owns it).
set -uo pipefail
exec > >(tee -a /workspace/h1144.log) 2>&1
echo "[pod] start $(date -u)"
cd /workspace

export PIP_ROOT_USER_ACTION=ignore
pip install -q -U "huggingface_hub>=0.23" pyarrow 2>&1 | tail -2 || true
python3 -c "import torch; print('[torch]', torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"

BASE_REPO="dancinlab/anima-clm-7b-h1141-g1pass-step6500"
BASE_FILE="h1141_g1pass_step6500.pt"
EXPECT_SHA="4de903714112c26c826a983797e5dfea0c7b3c1f19f15a34dd35822f33e245d9"

# 1) pull base ckpt + verify sha256
echo "[pod] downloading base ckpt from HF ..."
python3 - <<PY
import os
from huggingface_hub import hf_hub_download
p = hf_hub_download("$BASE_REPO", "$BASE_FILE", token=os.environ["HF_TOKEN"], local_dir="/workspace/base")
print("BASE", p)
PY
BASE=/workspace/base/$BASE_FILE
GOT=$(sha256sum "$BASE" | cut -d' ' -f1)
echo "[pod] base sha256 got=$GOT expect=$EXPECT_SHA"
[ "$GOT" = "$EXPECT_SHA" ] || { echo "[pod] SHA MISMATCH -- abort"; touch /workspace/H1144_FAILED; exit 1; }

# 2) build the 1200MB en grounding corpus (deterministic; first 300MB == probe corpus)
echo "[pod] building 1200MB en grounding corpus ..."
python3 /workspace/build_wiki5_bigcorpus_en.py /workspace/corpus_en_1200mb.txt 1258291200 /workspace/wk 2>&1 | tail -10
ls -la /workspace/corpus_en_1200mb.txt
# 300MB probe corpus = first 314572800 bytes (byte-identical to h1143 corpus sha 80ba6b48..)
head -c 314572800 /workspace/corpus_en_1200mb.txt > /workspace/corpus_en_300mb.txt
PROBE_SHA=$(sha256sum /workspace/corpus_en_300mb.txt | cut -d' ' -f1)
echo "[pod] probe-corpus(300MB) sha256=$PROBE_SHA (expect 80ba6b48943e1943c4c3a0753c2bc594132acd7f30046733f4bf0102020c979d)"

measure_ckpt () {
  # $1 = ckpt path, $2 = tag (probe|converge)
  local CK="$1" TAG="$2"
  echo "[pod] [$TAG] regenerating 40 factual continuations (h1141_7b_g5_eval gate_g5_l2) ..."
  python3 /workspace/h1141_7b_g5_eval.py --ckpt "$CK" --corpus /workspace/corpus_en_300mb.txt \
      --en_mb 300 --n_sentences 40 --out /workspace/g5_result_${TAG}.json
  echo "[pod] [$TAG] re-measuring fabricated-entity-rate (h1143 harness VERBATIM) ..."
  python3 /workspace/h1143_g5l2_nonfab_measure.py /workspace/g5_result_${TAG}.json \
      /workspace/corpus_en_300mb.txt /workspace/h1144_fabrate_${TAG}.json
}

# 3) LEG 1 — PROBE (2000 steps, LR 2e-5, best-ckpt-by-val, real held-out val tail)
echo "[pod] === LEG 1 PROBE (2000 steps) ==="
python3 /workspace/h1144_grounding_train.py --base "$BASE" --corpus /workspace/corpus_en_1200mb.txt \
    --cap_mb 1200 --steps 2000 --lr 2e-5 --leg probe \
    --ckpt /workspace/ckpt/h1144_probe_best.pt --out /workspace/h1144_curve_probe.json
[ -f /workspace/ckpt/h1144_probe_best.pt ] || { echo "[pod] PROBE ckpt missing"; touch /workspace/H1144_FAILED; exit 1; }
measure_ckpt /workspace/ckpt/h1144_probe_best.pt probe

# 4) FROZEN slope decision
echo "[pod] === SLOPE DECISION (frozen rule) ==="
python3 /workspace/h1144_slope_decide.py /workspace/h1144_fabrate_probe.json
SLOPE_RC=$?
echo "[pod] slope rc=$SLOPE_RC (0=GREENLIGHT 1=STOP)"

FINAL_CKPT=/workspace/ckpt/h1144_probe_best.pt
FINAL_TAG=probe
if [ $SLOPE_RC -eq 0 ]; then
  echo "[pod] === GREENLIGHT -> LEG 2 CONVERGE (up to 12000 steps, resume from probe best) ==="
  python3 /workspace/h1144_grounding_train.py --base "$BASE" --resume /workspace/ckpt/h1144_probe_best.pt \
      --corpus /workspace/corpus_en_1200mb.txt --cap_mb 1200 --steps 12000 --lr 2e-5 --leg converge \
      --ckpt /workspace/ckpt/h1144_converge_best.pt --out /workspace/h1144_curve_converge.json
  if [ -f /workspace/ckpt/h1144_converge_best.pt ]; then
    measure_ckpt /workspace/ckpt/h1144_converge_best.pt converge
    FINAL_CKPT=/workspace/ckpt/h1144_converge_best.pt
    FINAL_TAG=converge
  fi
else
  echo "[pod] === STOP (flat slope) — no convergence burn. Reporting probe closed-neg. ==="
fi

# 5) FULL a7b_pass battery on the FINAL ckpt (G0 G1 G2 G3; G5-L1 via g5_eval already; G5-L2 = re-measured)
echo "[pod] === FULL GATE BATTERY (G0 G1 G2 G3) on FINAL ckpt ($FINAL_TAG) ==="
python3 /workspace/h1141_7b_pass_attempt.py --base "$BASE" --gate_only --ckpt "$FINAL_CKPT" \
    --corpus /workspace/corpus_en_300mb.txt 2>&1 | tail -60 || true
# the pass_attempt writes /workspace/h1141_result.json — rename to h1144
[ -f /workspace/h1141_result.json ] && mv /workspace/h1141_result.json /workspace/h1144_battery_${FINAL_TAG}.json

# 6) sha256 the final ckpt + upload to HF PRIVATE (a_fire_recover_complete; visibility flipped later on PASS)
FINAL_SHA=$(sha256sum "$FINAL_CKPT" | cut -d' ' -f1)
FINAL_SIZE=$(stat -c%s "$FINAL_CKPT")
echo "[pod] FINAL ckpt $FINAL_CKPT sha256=$FINAL_SHA size=$FINAL_SIZE"
echo "{\"final_ckpt\":\"$FINAL_CKPT\",\"final_tag\":\"$FINAL_TAG\",\"sha256\":\"$FINAL_SHA\",\"size\":$FINAL_SIZE,\"slope_rc\":$SLOPE_RC}" > /workspace/h1144_final_manifest.json

echo "[pod] uploading FINAL ckpt to HF (PRIVATE) ..."
python3 - <<PY
import os
from huggingface_hub import HfApi
api = HfApi(token=os.environ["HF_TOKEN"])
repo = "dancinlab/anima-clm-7b-h1144-grounding-${FINAL_TAG}"
api.create_repo(repo, repo_type="model", private=True, exist_ok=True)
api.upload_file(path_or_fileobj="$FINAL_CKPT", path_in_repo="h1144_${FINAL_TAG}_best.pt",
                repo_id=repo, repo_type="model")
# upload the result jsons too (complete artifact set)
for f in ["h1144_fabrate_${FINAL_TAG}.json","h1144_battery_${FINAL_TAG}.json",
          "h1144_curve_probe.json","g5_result_${FINAL_TAG}.json","h1144_final_manifest.json"]:
    p="/workspace/"+f
    if os.path.exists(p):
        api.upload_file(path_or_fileobj=p, path_in_repo=f, repo_id=repo, repo_type="model")
print("HF_UPLOAD_OK", repo)
PY

echo "H1144_DONE $(date -u)"
echo "[pod] end $(date -u)"
