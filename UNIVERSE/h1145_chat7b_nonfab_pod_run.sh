#!/usr/bin/env bash
# h1145_chat7b_nonfab_pod_run.sh — pod-side driver for H_1145.
# PIGGYBACK MEASURE of the chat-7b's G5-L2 fabricated-entity-rate using the SAME
# frozen h1143 harness + the SAME 40 factual openers + the SAME 0.20 frozen bar
# as H_1143/H_1144. FREEZE nothing new. Honest either way.
#
#   1) pull dancinlab/anima-clm-chat-7b (anima_clm_chat_7b.pt) + verify sha256
#   2) build the deterministic 300MB en grounding corpus (== h1143 probe corpus,
#      sha 80ba6b48...) so the 40 openers + corpus-absence predicate are IDENTICAL
#   3) h1141_7b_g5_eval.py --ckpt chat-7b  (VERBATIM gate_g5_l2: same extract_sentences
#      over the 300MB head, same 40 openers, temp 0.7, seed 7) -> g5_result_chat7b.json
#   4) h1143_g5l2_nonfab_measure.py g5_result_chat7b.json corpus_en_300mb.txt out.json
#      (VERBATIM frozen 0.20 bar, regex NER + corpus-absence predicate)
#   5) print H1145_DONE sentinel. NO teardown here (orchestrator owns it).
# Tokens come from env (HF_TOKEN) — never argv.
set -uo pipefail
exec > >(tee -a /workspace/h1145.log) 2>&1
echo "[pod] start $(date -u)"
cd /workspace

export PIP_ROOT_USER_ACTION=ignore
pip install -q -U "huggingface_hub>=0.23" pyarrow 2>&1 | tail -2 || true
python3 -c "import torch; print('[torch]', torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"

CHAT_REPO="dancinlab/anima-clm-chat-7b"
CHAT_FILE="anima_clm_chat_7b.pt"
EXPECT_SHA="4b8957c7bee01e3d36b154b2cffc88490dec68f56776fde9c8070ad1bd4cb56a"

# 1) pull chat-7b ckpt + verify sha256
echo "[pod] downloading chat-7b ckpt from HF ..."
python3 - <<PY
import os
from huggingface_hub import hf_hub_download
p = hf_hub_download("$CHAT_REPO", "$CHAT_FILE", token=os.environ["HF_TOKEN"], local_dir="/workspace/chat")
print("CHAT", p)
PY
CK=/workspace/chat/$CHAT_FILE
GOT=$(sha256sum "$CK" | cut -d' ' -f1)
echo "[pod] chat-7b sha256 got=$GOT expect=$EXPECT_SHA"
[ "$GOT" = "$EXPECT_SHA" ] || { echo "[pod] SHA MISMATCH -- abort"; touch /workspace/H1145_FAILED; exit 1; }

# 2) build the 300MB en grounding corpus (deterministic; == h1143/h1144 probe corpus)
echo "[pod] building 1200MB en corpus then slicing the 300MB head ..."
python3 /workspace/build_wiki5_bigcorpus_en.py /workspace/corpus_en_1200mb.txt 1258291200 /workspace/wk 2>&1 | tail -8
head -c 314572800 /workspace/corpus_en_1200mb.txt > /workspace/corpus_en_300mb.txt
PROBE_SHA=$(sha256sum /workspace/corpus_en_300mb.txt | cut -d' ' -f1)
echo "[pod] probe-corpus(300MB) sha256=$PROBE_SHA (expect 80ba6b48943e1943c4c3a0753c2bc594132acd7f30046733f4bf0102020c979d)"

# 3) regenerate the 40 factual continuations (h1141_7b_g5_eval gate_g5_l2 VERBATIM)
echo "[pod] regenerating 40 factual continuations on chat-7b (gate_g5_l2 VERBATIM) ..."
python3 /workspace/h1141_7b_g5_eval.py --ckpt "$CK" --corpus /workspace/corpus_en_300mb.txt \
    --en_mb 300 --n_sentences 40 --out /workspace/g5_result_chat7b.json
[ -f /workspace/g5_result_chat7b.json ] || { echo "[pod] g5_result missing"; touch /workspace/H1145_FAILED; exit 1; }

# 4) re-measure fabricated-entity-rate (h1143 harness VERBATIM, frozen 0.20 bar)
echo "[pod] re-measuring fabricated-entity-rate (h1143 harness VERBATIM) ..."
python3 /workspace/h1143_g5l2_nonfab_measure.py /workspace/g5_result_chat7b.json \
    /workspace/corpus_en_300mb.txt /workspace/h1145_fabrate_chat7b.json
echo "[pod] === H_1145 RESULT ==="
python3 -c "import json; d=json.load(open('/workspace/h1145_fabrate_chat7b.json')); print('fab_rate=',d['fabricated_entity_rate'],'new_L2_pass=',d['new_L2_pass'],'n_fab=',d['n_fabricated'],'n_total=',d['n_entities_total'])"

echo "H1145_DONE $(date -u)"
echo "[pod] end $(date -u)"
