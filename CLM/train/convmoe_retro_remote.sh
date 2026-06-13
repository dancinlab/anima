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

# deps: torch is in the image; need numpy + a RECENT datasets (old script-based loaders
# were removed; modern HF datasets are parquet-native) + hf for upload.
pip install -q --no-input -U "numpy" "datasets>=2.19" "huggingface_hub" "pyarrow" 2>&1 | tail -2 || true
# english word dictionary for G0 known-word-ratio (kwr vs /usr/share/dict)
apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq wamerican >/dev/null 2>&1 || \
  pip install -q english-words 2>/dev/null || true
ls -la /usr/share/dict/ 2>/dev/null || echo "[remote] WARN: no /usr/share/dict (G0 uses concept-kw fallback)"

# ---- English-dominant ASCII corpus (equivalent to the aiden en_wiki_120mb) ----
CORPUS=/workspace/en_wiki_120mb.txt
if [ ! -s "$CORPUS" ]; then
  echo "[remote] building English wiki corpus via HF datasets (parquet-native; multi-source fallback)..."
  python3 - <<'PY'
import os
out="/workspace/en_wiki_120mb.txt"
TARGET=120*1024*1024
TOK=os.environ.get("HF_TOKEN") or None

def ascii_filt(s):
    # keep printable ASCII (English-dominant, byte-efficient like the aiden sweep)
    return "".join(c for c in s if 32 <= ord(c) < 127 or c=="\n")

# Each source is a (label, fn) where fn(write) streams English text. Modern HF datasets
# are PARQUET-native — the old script-based "wikitext"/"wikipedia" loaders were REMOVED,
# so we point at parquet repos (Salesforce/wikitext, wikimedia/wikipedia, fineweb sample).
def gen_wikitext(write):
    from datasets import load_dataset
    ds=load_dataset("Salesforce/wikitext","wikitext-103-raw-v1",split="train",
                    streaming=True,token=TOK)
    for ex in ds:
        t=ex.get("text","") or ""
        if t.strip().startswith("=") and len(t.strip())<80:  # skip section headers
            continue
        t=ascii_filt(t)
        if len(t)<40: continue
        if not write(t.strip()+"\n"): return

def gen_wikimedia(write):
    from datasets import load_dataset
    ds=load_dataset("wikimedia/wikipedia","20231101.en",split="train",
                    streaming=True,token=TOK)
    for ex in ds:
        t=ascii_filt(ex.get("text","") or "")
        if len(t)<200: continue
        if not write(t.strip()+"\n"): return

def gen_fineweb(write):
    from datasets import load_dataset
    ds=load_dataset("HuggingFaceFW/fineweb","sample-10BT",split="train",
                    streaming=True,token=TOK)
    for ex in ds:
        t=ascii_filt(ex.get("text","") or "")
        if len(t)<200: continue
        if not write(t.strip()+"\n"): return

SOURCES=[("Salesforce/wikitext-103",gen_wikitext),
         ("wikimedia/wikipedia.20231101.en",gen_wikimedia),
         ("HuggingFaceFW/fineweb.sample-10BT",gen_fineweb)]

for label,fn in SOURCES:
    try:
        written=[0]
        f=open(out,"w")
        def write(s, _f=f, _w=written):
            _f.write(s); _w[0]+=len(s)
            return _w[0]<TARGET
        fn(write); f.close()
        if written[0] >= TARGET*0.5:   # accept if we got at least 60MB
            print(f"[corpus] wrote {written[0]/1e6:.1f}MB from {label}")
            break
        else:
            print(f"[corpus] {label} yielded only {written[0]/1e6:.1f}MB; trying next source")
    except Exception as e:
        print(f"[corpus] {label} failed: {e!r}; trying next source")
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
