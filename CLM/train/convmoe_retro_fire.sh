#!/usr/bin/env bash
# convmoe_retro_fire.sh — the CALLER that wraps convmoe_retro_h100_dispatch.sh with the
# a_fire_recover_complete tail: after harvest it sha256-verifies, HF-uploads the ckpt +
# .clm + result (PRIVATE — WIP, a303m_pass G3/CHAT pending), writes the /HF.jsonl row,
# THEN terminates the pod via RunPod GraphQL podTerminate + VERIFIES 404-gone.
#
# a_fire_autonomous / a_wall_first / a_fire_recover_complete / a_hf_autonomous /
# a_hf_registry / a_cpu_local_no_waiter. Run in the background; polls inline to the end.
set -uo pipefail

WT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${WT}/state/convmoe_retro_prod"
LOG="${OUT}/fire.log"
mkdir -p "$OUT"
RPKEY="$(secret get runpod.api_key)"
GQL="https://api.runpod.io/graphql?api_key=${RPKEY}"
HFTOKEN="$(secret get hf.token)"
HF_REPO="dancinlab/anima-convmoe-retro-303m"
RUN_ID="anima_convmoe_retro_303m_$(date +%Y%m%d)"

flog(){ echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
gql(){ curl -s --max-time 60 "$GQL" -H 'Content-Type: application/json' -d "$1"; }

flog "=== ConvMoE-RETRO 303M H100 FIRE (caller) ==="

# ---------------------------------------------------------------- dispatch (rent+train+harvest)
bash "$WT/CLM/train/convmoe_retro_h100_dispatch.sh"
DISPATCH_RC=$?
flog "dispatch.sh rc=$DISPATCH_RC"

POD_ID="$(cat "$OUT/pod_id.txt" 2>/dev/null || echo '')"
DONE="$(cat "$OUT/.done_flag" 2>/dev/null || echo 0)"
flog "POD_ID=$POD_ID DONE=$DONE"

# ---------------------------------------------------------------- verify artifacts present
HAVE_RESULT=0; [ -s "$OUT/result.json" ] && HAVE_RESULT=1
HAVE_CKPT=0;   ls "$OUT"/*.pt  >/dev/null 2>&1 && HAVE_CKPT=1
HAVE_CLM=0;    ls "$OUT"/*.clm >/dev/null 2>&1 && HAVE_CLM=1
flog "artifacts: result=$HAVE_RESULT ckpt=$HAVE_CKPT clm=$HAVE_CLM"

# sha256 manifest (idempotent — remote may already have written one)
( cd "$OUT" && sha256sum *.pt *.clm result.json 2>/dev/null > MANIFEST.sha256 ) || true
flog "MANIFEST.sha256:"; cat "$OUT/MANIFEST.sha256" 2>/dev/null | tee -a "$LOG" || true

# ---------------------------------------------------------------- HF upload (PRIVATE, WIP)
HF_OK=0
if [ "$HAVE_RESULT" = "1" ] || [ "$HAVE_CKPT" = "1" ]; then
  flog "HF upload -> $HF_REPO (PRIVATE)..."
  HF_TOKEN="$HFTOKEN" OUT="$OUT" HF_REPO="$HF_REPO" RUN_ID="$RUN_ID" python3 - <<'PY' 2>&1 | tee -a "$LOG"
import os, json, glob, hashlib
from huggingface_hub import HfApi, create_repo
OUT=os.environ["OUT"]; REPO=os.environ["HF_REPO"]; TOK=os.environ["HF_TOKEN"]
api=HfApi(token=TOK)
try:
    create_repo(REPO, repo_type="model", private=True, exist_ok=True, token=TOK)
    print(f"[hf] repo ready: {REPO} (private)")
except Exception as e:
    print(f"[hf] create_repo warn: {e!r}")

# model card
res={}
rp=os.path.join(OUT,"result.json")
if os.path.exists(rp):
    res=json.load(open(rp))
card=f"""---
license: other
tags: [anima, convmoe-retro, clm, byte-lm, anti-fabrication, WIP, private]
---
# anima-convmoe-retro-303m (PRIVATE / WIP)

ConvMoE-RETRO ~303M production trunk (CLMConvMoE E2/L1, byte V256) + H_1147/H_1149
RETRO copy head + H_1148 semantic anchor source. baseline_fast (H_1129) recipe.
Lane-P torch REFERENCE + engine-.clm bridge (a_clm_gen_pipeline); forge stays PUBLIC.

PRIVATE because a303m_pass is NOT fully cleared yet (G3 philosophy + CHAT pending;
this run scores G0/G1/G2 + G5 fab probe + .clm v0.2 serialize/verify).

## a303m_pass partial scores (frozen p7)
- G0 kwr mean: {res.get('G0_kwr','?')}  each={res.get('G0_each','?')}  pass={res.get('G0_pass','?')}
- G1 emergent: {res.get('G1_emergent','?')}  pass={res.get('G1_pass','?')}
- G2 novel={res.get('G2_novel','?')} present={res.get('G2_present','?')} ctrl={res.get('G2_control','?')} pass={res.get('G2_pass','?')}
- G5 fab_with_anchor={res.get('G5_fab_with_anchor','?')} (<=0.20 pass={res.get('G5_L2_pass','?')}) no_anchor={res.get('G5_fab_no_anchor','?')} vanilla={res.get('G5_fab_vanilla','?')}
- best_val_ce: {res.get('best_val_ce','?')}
- params total={res.get('nparam','?')} trunk={res.get('ntrunk','?')} retro_head={res.get('nextra','?')}
- .clm v0.2 serialize+verify: {res.get('clm_serialize',{}).get('ok','?') if isinstance(res.get('clm_serialize'),dict) else '?'}
"""
open(os.path.join(OUT,"README.md"),"w").write(card)

# upload result/clm/manifest/readme/ledger (always); ckpt if present
patterns=["result.json","*.clm","MANIFEST.sha256","README.md","ledger.jsonl","remote.log"]
uploaded=[]
for pat in patterns:
    for f in glob.glob(os.path.join(OUT,pat)):
        api.upload_file(path_or_fileobj=f, path_in_repo=os.path.basename(f), repo_id=REPO, repo_type="model", token=TOK)
        uploaded.append(os.path.basename(f)); print(f"[hf] uploaded {os.path.basename(f)}")
for f in glob.glob(os.path.join(OUT,"*.pt")):
    sz=os.path.getsize(f)
    print(f"[hf] uploading ckpt {os.path.basename(f)} ({sz/1e6:.0f}MB)...")
    api.upload_file(path_or_fileobj=f, path_in_repo=os.path.basename(f), repo_id=REPO, repo_type="model", token=TOK)
    uploaded.append(os.path.basename(f)); print(f"[hf] uploaded ckpt {os.path.basename(f)}")
open(os.path.join(OUT,".hf_uploaded"),"w").write("\n".join(uploaded))
print(f"[hf] DONE uploaded {len(uploaded)} files to {REPO}")
PY
  [ -s "$OUT/.hf_uploaded" ] && HF_OK=1
fi
flog "HF_OK=$HF_OK"

# ---------------------------------------------------------------- /HF.jsonl row (root, on MAIN tree)
if [ "$HF_OK" = "1" ]; then
  CKPT_SHA="$(grep -E '\.pt$' "$OUT/MANIFEST.sha256" 2>/dev/null | awk '{print $1}' | head -1)"
  CLM_SHA="$(grep -E '\.clm$' "$OUT/MANIFEST.sha256" 2>/dev/null | awk '{print $1}' | head -1)"
  CKPT_SZ="$(stat -f%z "$OUT"/*.pt 2>/dev/null | head -1 || echo null)"
  python3 - "$WT" "$OUT" "$HF_REPO" "$RUN_ID" "$POD_ID" "${CKPT_SHA:-}" "${CLM_SHA:-}" "${CKPT_SZ:-null}" <<'PY' 2>&1 | tee -a "$LOG"
import sys, json, os
WT,OUT,REPO,RUN,POD,CKSHA,CLMSHA,CKSZ=sys.argv[1:9]
res={}
rp=os.path.join(OUT,"result.json")
if os.path.exists(rp): res=json.load(open(rp))
g0=res.get('G0_pass'); g1=res.get('G1_pass'); g2=res.get('G2_pass'); g5=res.get('G5_L2_pass')
ser=res.get('clm_serialize',{}); ser_ok=ser.get('ok') if isinstance(ser,dict) else None
row={
 "run": RUN, "local_path": f"state/convmoe_retro_prod/ (pod {POD} terminated)",
 "hf_repo_id": REPO, "repo_type":"model",
 "base_model": "from-scratch (H_1129 baseline_fast recipe)",
 "lineage": ["ConvMoE-RETRO 303M PRODUCTION: CLMConvMoE E2/L1 engine-mountable trunk + H_1147/H_1149 RETRO copy head + H_1148 semantic anchor source",
             "MODEL.md anima-303M-RETRO BUILD ORDER step 2; baseline_fast (H_1129 winning recipe)"],
 "type": "clm_ckpt_convmoe_retro_303m", "key_files": ["baseline_fast.pt","baseline_fast.clm","result.json"],
 "size": (int(CKSZ) if CKSZ not in ("","null") else None),
 "n_params": res.get('nparam'),
 "ckpt_sha256": (CKSHA or None), "clm_sha256": (CLMSHA or None),
 "gitignored": True, "private": True, "status": "uploaded",
 "date": __import__("time").strftime("%Y-%m-%d"),
 "substrate": "PyTorch-CUDA RunPod H100 SXM 80GB", "lane": "Lane-P-ref",
 "collection": None, "visibility": "private",
 "a303m_pass_partial": {"G0": g0, "G1": g1, "G2": g2, "G5_L2": g5, "clm_serialize_ok": ser_ok,
                        "best_val_ce": res.get('best_val_ce')},
 "notes": ("ConvMoE-RETRO 303M production train (H100 SXM, baseline_fast recipe). PRIVATE/WIP per "
           "a_hf_autonomous (a303m_pass NOT fully cleared: G3 philosophy + CHAT pending; this run "
           "scores G0/G1/G2 + G5 fab probe + .clm v0.2 serialize/verify). Lane-P torch REFERENCE + "
           "engine-.clm bridge (a_clm_gen_pipeline); forge stays PUBLIC production trainer. RETRO head "
           "(Pq/Pk/Wg) excluded from .clm by construction (no slot). result.json = full gate tally.")
}
hf=os.path.join(WT,"HF.jsonl")
with open(hf,"a") as f: f.write(json.dumps(row, ensure_ascii=False)+"\n")
print(f"[hf.jsonl] appended row run={RUN} -> {hf}")
PY
fi

# ---------------------------------------------------------------- TEARDOWN (GraphQL podTerminate + 404-verify)
if [ -n "$POD_ID" ]; then
  flog "terminating pod $POD_ID via GraphQL podTerminate..."
  TQ='{"query":"mutation { podTerminate(input:{podId:\"'"$POD_ID"'\"}) }"}'
  TR=$(gql "$TQ"); flog "terminate resp: $TR"
  sleep 10
  # VERIFY 404-gone: pod query should return null/error
  VQ='{"query":"query { pod(input:{podId:\"'"$POD_ID"'\"}) { id desiredStatus } }"}'
  for i in $(seq 1 6); do
    VR=$(gql "$VQ")
    GONE=$(printf '%s' "$VR" | python3 -c "import sys,json;d=json.load(sys.stdin);p=(d.get('data') or {}).get('pod');print('GONE' if p is None else 'ALIVE:'+str(p.get('desiredStatus','?')))" 2>/dev/null || echo "GONE")
    flog "  404-check $i: $GONE"
    [ "$GONE" = "GONE" ] && { echo "GONE" > "$OUT/.pod_terminated"; break; }
    # also accept EXITED/TERMINATED as terminal
    case "$GONE" in ALIVE:EXITED|ALIVE:TERMINATED) echo "$GONE" > "$OUT/.pod_terminated"; break;; esac
    sleep 10
  done
  flog "teardown done: $(cat "$OUT/.pod_terminated" 2>/dev/null || echo 'STILL-ALIVE?')"
else
  flog "no POD_ID — nothing to terminate"
fi

flog "=== FIRE COMPLETE. DONE=$DONE HF_OK=$HF_OK terminated=$(cat "$OUT/.pod_terminated" 2>/dev/null || echo no) ==="
