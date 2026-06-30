#!/usr/bin/env bash
# tooluse_argcopy_fire.sh — Lane G (GPU) argcopy residual-closer fire driver.
# Runs on the pool host `summer` (RTX 5070). Self-contained: pulls base ckpt + base
# chat corpus from HF (PUBLIC), generates the argcopy agent-lane corpus, builds the
# two EQUAL-BYTE training corpora (with-argcopy ⊃ base chat ; no-grammar = base chat
# + equal-byte base filler), then runs the A/B falsifier harness.
set -euo pipefail
WORK="${1:-$HOME/anima_argcopy}"
SRC="${2:-$WORK/src}"   # checked-out repo path containing serving/ + training/
mkdir -p "$WORK"
cd "$WORK"

echo "[fire] work=$WORK src=$SRC"
python3 -c "import torch;assert torch.cuda.is_available();print('[gpu]',torch.cuda.get_device_name(0),'cuda',torch.version.cuda)"

# ── 1. base ckpt (PUBLIC HF model) ──
if [ ! -f "$WORK/chat_rung0_18m.pt" ]; then
  echo "[fire] downloading base ckpt from HF…"
  python3 - <<'PY'
from huggingface_hub import hf_hub_download
import shutil, os
p = hf_hub_download("dancinlab/anima-clm-chat-rung0-byte-18m", "chat_rung0_18m.pt")
shutil.copy(p, os.path.expanduser(os.environ.get("WORK","~/anima_argcopy")+"/chat_rung0_18m.pt"))
print("[base] copied", p)
PY
fi
BASE_SHA=$(sha256sum "$WORK/chat_rung0_18m.pt" | awk '{print $1}')
echo "[fire] base ckpt sha256=$BASE_SHA (expect 9d5e1394c020378e19bd700fc95144bdd67c65ca3382adc558828ccd99c743b7)"

# ── 2. base chat corpus (PUBLIC HF dataset) ──
if [ ! -f "$WORK/chat_corpus_mix.txt" ]; then
  echo "[fire] downloading base chat corpus from HF…"
  python3 - <<'PY'
from huggingface_hub import hf_hub_download
import shutil, os
p = hf_hub_download("dancinlab/anima-chat-corpus-mix-70wiki-30dialogue", "chat_corpus_mix.txt", repo_type="dataset")
shutil.copy(p, os.path.expanduser(os.environ.get("WORK","~/anima_argcopy")+"/chat_corpus_mix.txt"))
print("[chat] copied", p)
PY
fi

# ── 3. generate the argcopy agent-lane corpus ──
echo "[fire] generating argcopy agent-lane corpus…"
python3 "$SRC/serving/agent_lane_argcopy_gen.py" \
  --out "$WORK/agent_lane_argcopy.full.txt" \
  --meta "$WORK/agent_lane_argcopy.meta.jsonl"
ARGCOPY_SHA=$(sha256sum "$WORK/agent_lane_argcopy.full.txt" | awk '{print $1}')
echo "[fire] argcopy corpus sha256=$ARGCOPY_SHA"

# ── 4. build the two EQUAL-BYTE training corpora ──
#   with_argcopy = base_chat ++ argcopy_lane
#   no_grammar   = base_chat ++ (equal-byte slice of base_chat as filler, NO tool demos)
python3 - <<PY
import os
W=os.path.expanduser("$WORK")
base=open(os.path.join(W,"chat_corpus_mix.txt"),"rb").read()
lane=open(os.path.join(W,"agent_lane_argcopy.full.txt"),"rb").read()
wa = base + b"\n" + lane
# filler = repeat base to match exactly len(lane)+1 extra bytes
need = len(wa) - len(base)
filler = (base * ((need//len(base))+1))[:need]
ng = base + filler
assert len(wa)==len(ng), (len(wa),len(ng))
open(os.path.join(W,"train_with_argcopy.txt"),"wb").write(wa)
open(os.path.join(W,"train_no_grammar.txt"),"wb").write(ng)
print(f"[corpora] with_argcopy={len(wa)} no_grammar={len(ng)} (byte-eq={len(wa)==len(ng)})")
PY

# ── 5. fire the A/B falsifier harness ──
echo "[fire] running A/B harness…"
WORK="$WORK" python3 "$SRC/training/tooluse_argcopy_ab.py" \
  --base-ckpt "$WORK/chat_rung0_18m.pt" \
  --corpus-with-argcopy "$WORK/train_with_argcopy.txt" \
  --corpus-no-grammar "$WORK/train_no_grammar.txt" \
  --out-dir "$WORK/out" \
  --steps 2500 --batch 32 --block 256 --lr 5e-5 --warmup 100 --seed 42 \
  2>&1 | tee "$WORK/fire.log"
echo "[fire] DONE — artifacts in $WORK/out"
