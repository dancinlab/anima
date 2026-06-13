#!/usr/bin/env bash
# convmoe_retro_remote.sh — runs ON the H100 pod. Fetch English corpus, train
# ConvMoE-RETRO 303M (baseline_fast), eval a303m_pass G0/G1/G2 + G5, serialize .clm.
set -uo pipefail
cd /workspace/anima
OUT=/workspace/anima/state/convmoe_retro_prod
mkdir -p "$OUT"
exec > >(tee -a "$OUT/remote.log") 2>&1
echo "[remote] $(date) start. nvidia-smi:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true

# deps: torch is in the image; need numpy + datasets for corpus + hf for upload
pip install -q --no-input numpy datasets huggingface_hub 2>&1 | tail -2 || true
# english word dictionary for G0 known-word-ratio (kwr vs /usr/share/dict)
apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq wamerican >/dev/null 2>&1 || \
  pip install -q english-words 2>/dev/null || true
ls -la /usr/share/dict/ 2>/dev/null || echo "[remote] WARN: no /usr/share/dict (G0 uses concept-kw fallback)"

# ---- English-dominant ASCII corpus (equivalent to the aiden en_wiki_120mb) ----
CORPUS=/workspace/en_wiki_120mb.txt
if [ ! -s "$CORPUS" ]; then
  echo "[remote] building English wiki corpus via HF datasets..."
  python3 - <<'PY'
import re
out="/workspace/en_wiki_120mb.txt"
TARGET=120*1024*1024
written=0
def ascii_filt(s):
    # keep printable ASCII (English-dominant, byte-efficient like the aiden sweep)
    return "".join(c for c in s if 32 <= ord(c) < 127 or c=="\n")
try:
    from datasets import load_dataset
    ds=load_dataset("wikitext","wikitext-103-raw-v1",split="train",streaming=True)
    with open(out,"w") as f:
        for ex in ds:
            t=ex.get("text","")
            if not t or t.strip().startswith("="):
                if len(t.strip())<4: continue
            t=ascii_filt(t)
            if len(t)<40: continue
            f.write(t.strip()+"\n")
            written+=len(t)
            if written>=TARGET: break
    print(f"[corpus] wrote {written/1e6:.1f}MB from wikitext-103")
except Exception as e:
    print(f"[corpus] wikitext-103 failed: {e!r}; trying wikipedia 20220301.en")
    written=0
    from datasets import load_dataset
    ds=load_dataset("wikipedia","20220301.en",split="train",streaming=True)
    with open(out,"w") as f:
        for ex in ds:
            t=ascii_filt(ex.get("text",""))
            if len(t)<200: continue
            f.write(t.strip()+"\n")
            written+=len(t)
            if written>=TARGET: break
    print(f"[corpus] wrote {written/1e6:.1f}MB from wikipedia.en")
PY
fi
if [ ! -s "$CORPUS" ]; then echo "[remote] FATAL: corpus build failed"; touch "$OUT/FAILED"; exit 4; fi
echo "[remote] corpus: $(ls -la $CORPUS)"

# ---- train ConvMoE-RETRO 303M baseline_fast (grad-ckpt OFF, big batch, bf16) ----
STEPS="${STEPS:-12000}"
echo "[remote] training ConvMoE-RETRO d=5008 (~303M) steps=$STEPS bs=24 accum=2 bf16..."
python3 -u CLM/train/train_convmoe_retro_prod.py \
  --corpus "$CORPUS" --cfg baseline_fast --host runpod-h100 \
  --out-dir "$OUT" --d-model 5008 --seq-len 512 \
  --bs 24 --accum 2 --steps "$STEPS" --La 128 --gap 64 --retro-frac 0.5 \
  --dropout 0.0 --weight_decay 0.1 --lr 3e-4 --warmup 300 --eval_every 500 --bf16
RC=$?
echo "[remote] trainer rc=$RC"
if [ $RC -eq 0 ] && [ -s "$OUT/result.json" ]; then
  # sha256 manifest for a_hf_registry / a_fire_recover_complete
  ( cd "$OUT" && sha256sum *.pt *.clm result.json 2>/dev/null > MANIFEST.sha256 )
  echo "[remote] $(date) DONE"; touch "$OUT/DONE"
else
  echo "[remote] $(date) trainer did not complete cleanly"; touch "$OUT/FAILED"
fi
