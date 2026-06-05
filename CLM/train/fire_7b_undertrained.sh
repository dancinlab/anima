#!/usr/bin/env bash
# fire_7b_undertrained.sh — M13 7B-undertrained ENGINE rung (Lane P, GPU-torch).
#  d6208/L30/E30 CLMConvMoE (~7.057B) on the R2 webscale ODC-BY corpus.
#  Fetches ~15-25 GB balanced 5-lang (eng,fra,deu,spa,kor incl ko) byte-direct
#  from R2 bucket phanes prefix anima-7b/web/<LANG3>/shardNNNN.bytes, concats to
#  ONE bytes file = --corpus (byte V=256). Serializes v0.3 .clm. Undertrained
#  (tok/param << Chinchilla 20) is the HONEST rung — exact tok/param reported.
#  a_fire_recover_complete: periodic ckpt+clm dump. a_lane_akida_gpu_split: Lane P.
set -uo pipefail

REPO_DIR="${REPO_DIR:-$HOME/anima}"
WORK="${WORK:-$HOME/lanep_7b}"
SHARDS_PER_LANG="${SHARDS_PER_LANG:-5}"   # 5 shards/lang
STEPS="${STEPS:-4000}"                     # bounded undertrained
SEQ="${SEQ:-512}"
BATCH="${BATCH:-4}"
ACCUM="${ACCUM:-8}"                         # eff batch 32 x 512 = 16384 tok/step
WARMUP="${WARMUP:-300}"
LOG_EVERY="${LOG_EVERY:-50}"
CKPT_EVERY="${CKPT_EVERY:-1000}"
D_MODEL="${D_MODEL:-6208}"
N_TRUNK="${N_TRUNK:-30}"
N_EXPERTS="${N_EXPERTS:-30}"

mkdir -p "$WORK"
echo "[fire7b] $(date -u) WORK=$WORK shards/lang=$SHARDS_PER_LANG steps=$STEPS d=$D_MODEL"

# 0) env
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())" || pip install -q torch
python3 -c "import boto3" 2>/dev/null || pip install -q boto3
python3 -c "import bitsandbytes" 2>/dev/null || pip install -q bitsandbytes
nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv,noheader || true

# 1) repo @ this branch (dilation cap + serialize_v3 landed)
if [ -d "$REPO_DIR/.git" ]; then
  git -C "$REPO_DIR" fetch origin -q && git -C "$REPO_DIR" checkout -q "$FIRE_BRANCH" 2>/dev/null || true
else
  git clone -q --branch "$FIRE_BRANCH" https://github.com/dancinlab/anima "$REPO_DIR"
fi
echo "[fire7b] repo HEAD=$(git -C "$REPO_DIR" rev-parse --short HEAD)"

CORPUS="$WORK/web_7b.bytes"
GB_PER_LANG="${GB_PER_LANG:-3.0}"   # balanced byte budget/lang (disk=60GB; 5x3=15GB + .pt28GB + pip fits)
# 2) fetch R2 byte-direct via Range-GET to a per-lang byte budget (shard sizes
#    differ 3GB vs 11GB so a shard-COUNT is unbalanced — use a byte budget).
if [ -s "$CORPUS" ] && [ -s "$WORK/corpus.done" ]; then
  echo "[fire7b] corpus exists ($(stat -c%s "$CORPUS") bytes) — reuse"
else
  rm -f "$CORPUS"
  python3 -u - "$CORPUS" "$GB_PER_LANG" <<'PYEOF' 2>&1 | tee "$WORK/corpus_fetch.log"
import os, sys, boto3
from botocore.config import Config
out_path = sys.argv[1]; budget = int(float(sys.argv[2]) * 1e9)
acct = os.environ["R2_ACCOUNT_ID"]; bucket = os.environ["R2_BUCKET"]
s3 = boto3.client("s3", endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
                  aws_access_key_id=os.environ["R2_KEY"],
                  aws_secret_access_key=os.environ["R2_SECRET"],
                  region_name="auto", config=Config(signature_version="s3v4"))
langs = ["eng","fra","deu","spa","kor"]
total = 0
with open(out_path, "wb") as fout:
    for lang in langs:
        pfx = f"anima-7b/web/{lang}/"
        keys = []; tok = None
        while True:
            kw = dict(Bucket=bucket, Prefix=pfx, MaxKeys=1000)
            if tok: kw["ContinuationToken"] = tok
            r = s3.list_objects_v2(**kw)
            for o in r.get("Contents", []):
                if o["Key"].endswith(".bytes"): keys.append((o["Key"], o["Size"]))
            if r.get("IsTruncated"): tok = r["NextContinuationToken"]
            else: break
        keys.sort()
        print(f"[r2] {lang}: {len(keys)} shards, budget={budget/1e9:.1f}GB", flush=True)
        lang_bytes = 0
        ki = 0
        while lang_bytes < budget and ki < len(keys):
            k, ksize = keys[ki]; ki += 1
            need = budget - lang_bytes
            end = min(need, ksize) - 1
            rng = f"bytes=0-{end}"
            obj = s3.get_object(Bucket=bucket, Key=k, Range=rng); body = obj["Body"]
            while True:
                chunk = body.read(64*1024*1024)
                if not chunk: break
                fout.write(chunk); lang_bytes += len(chunk); total += len(chunk)
            print(f"[r2]   {k} [{rng}] lang_total={lang_bytes/1e9:.2f}GB overall={total/1e9:.2f}GB", flush=True)
        print(f"[r2] {lang} DONE lang_total={lang_bytes/1e9:.2f}GB", flush=True)
print(f"[r2] CORPUS WRITTEN {out_path} total={total} bytes ({total/1e9:.2f}GB)", flush=True)
PYEOF
  if [ -s "$CORPUS" ]; then touch "$WORK/corpus.done"; else echo "[fire7b] FATAL corpus fetch empty"; exit 4; fi
fi
echo "[fire7b] corpus $(stat -c%s "$CORPUS") bytes"

# 3) train the ~7.06B rung (bf16 + grad-ckpt; 80GB fit)
echo "[fire7b] training d$D_MODEL L$N_TRUNK E$N_EXPERTS ~7B …"
PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}" \
CLM_NO_CUDNN="${CLM_NO_CUDNN:-1}" python3 -u "$REPO_DIR/CLM/train/train_lane_p_3b.py" \
  --d-model "$D_MODEL" --n-trunk-layers "$N_TRUNK" --n-experts "$N_EXPERTS" --kernel-size 3 \
  --steps "$STEPS" --seq-len "$SEQ" --batch-size "$BATCH" --grad-accum "$ACCUM" \
  --lr 2e-4 --warmup "$WARMUP" --bf16 --grad-checkpoint --optim8bit \
  --corpus "$CORPUS" \
  --ckpt-out "$WORK/clm_7b.pt" \
  --clm-out "$WORK/clm_7b.clm" \
  --json-out "$WORK/result_7b.json" \
  --log-every "$LOG_EVERY" --ckpt-every "$CKPT_EVERY" \
  2>&1 | tee "$WORK/train_7b.log"

echo "[fire7b] DONE $(date -u). artifacts in $WORK:"
ls -la "$WORK"/clm_7b.* "$WORK"/result_7b.json 2>/dev/null
echo "FIRE7B_COMPLETE"
