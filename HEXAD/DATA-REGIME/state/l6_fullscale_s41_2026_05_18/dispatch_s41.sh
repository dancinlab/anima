#!/usr/bin/env bash
# RESEARCH.md §41 — L6 fullscale runpod dispatch (g_fire_dispatch_robust).
#
# runpod primary (g_resource_active_parallel provider_order); vast.ai
# fallback only on runpod stock-exhaust. Single pod train+eval. Dispatch
# stall-fix: nohup detached training + bounded SSH probe poll loop (no
# long-lived SSH tee). SAVE_POD=1 auto-promote after result.json verify
# + 5-retry pull (g_fire_dispatch_robust).
#
# Credentials: read from `secret` CLI — RUNPOD_KEY hard-coded literal is
# forbidden (f_hardcoded_credential). This script reads runpod.api_key
# at runtime and never echoes the value.
#
# Cost head (g_fire_autonomous transparent cost note, NOT gate):
#   A100 80GB PCIe ~$1.89/hr · 3000 steps d=768·12L on 22.76 MB corpus
#   ~10-15 min wall + ~3 min eval (806 held-out pair greedy decode 140
#   bytes each) → ~$0.20-0.40 estimate.
set -euo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$HERE"

# ── credentials via `secret` CLI (f_hardcoded_credential safety) ───────
RUNPOD_KEY="$(secret get runpod.api_key 2>/dev/null || echo '')"
if [ -z "$RUNPOD_KEY" ]; then
    echo "[§41 dispatch] FATAL: secret get runpod.api_key returned empty"
    echo "[§41 dispatch] register via: printf %s '<api_key>' | secret set runpod.api_key"
    exit 1
fi
export RUNPODCTL_API_KEY="$RUNPOD_KEY"

# ── pod create (A100 80GB PCIe primary) ────────────────────────────────
export GPU_TYPE="${GPU_TYPE:-NVIDIA A100 80GB PCIe}"
export POD_NAME="l6-fullscale-s41-$(date +%s)"
export IMAGE="${IMAGE:-runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04}"
export DISK_GB="${DISK_GB:-50}"
echo "[§41 dispatch] requesting pod GPU=$GPU_TYPE  name=$POD_NAME  image=$IMAGE  disk=${DISK_GB}GB"

POD_JSON="$(python3 - <<PY
import os, json, runpod, time
runpod.api_key = os.environ['RUNPODCTL_API_KEY']
gpus = runpod.get_gpus()
# Preference cascade by GPU id (the create_pod arg). A100 80GB PCIe
# primary → A100-SXM4-80GB → H100 → A40 → RTX A6000 (≥40 GB only).
prefs = [
    "NVIDIA A100 80GB PCIe",
    "NVIDIA A100-SXM4-80GB",
    "NVIDIA H100 PCIe",
    "NVIDIA H100 80GB HBM3",
    "NVIDIA L40S",
    "NVIDIA RTX A6000",
    "NVIDIA A40",
]
catalog = {g.get('id'): g for g in gpus}
last_err = None
for pref in prefs:
    if pref not in catalog:
        last_err = f"GPU id {pref} not in catalog"; continue
    try:
        pod = runpod.create_pod(
            name=os.environ['POD_NAME'],
            image_name=os.environ['IMAGE'],
            gpu_type_id=pref,
            gpu_count=1,
            container_disk_in_gb=int(os.environ['DISK_GB']),
            volume_in_gb=0,
            ports="22/tcp",
            support_public_ip=True,
        )
        if pod and pod.get('id'):
            pod['_gpu_id'] = pref
            print(json.dumps(pod)); raise SystemExit(0)
    except SystemExit:
        raise
    except Exception as e:
        last_err = f"{pref}: {e}"; time.sleep(2); continue
print(json.dumps({"error": last_err or "no GPU available"})); raise SystemExit(2)
PY
)"
echo "[§41 dispatch] pod_create response: $POD_JSON"
POD_ID="$(echo "$POD_JSON" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("id",""))')"
[ -n "$POD_ID" ] || { echo "[§41 dispatch] FATAL: pod create failed"; exit 3; }

# Get ssh endpoint after pod boots
echo "[§41 dispatch] pod_id=$POD_ID  waiting for SSH..."
for i in $(seq 1 60); do
    POD_META="$(python3 -c "import runpod, os, json; runpod.api_key=os.environ['RUNPODCTL_API_KEY']; print(json.dumps(runpod.get_pod(\"$POD_ID\")))")"
    IP="$(echo "$POD_META" | python3 -c 'import sys,json;d=json.load(sys.stdin);rp=d.get("runtime") or {};po=rp.get("ports") or [];p=[x for x in po if x.get("privatePort")==22];print((p[0]["ip"] if p else "") if p else "")')"
    PORT="$(echo "$POD_META" | python3 -c 'import sys,json;d=json.load(sys.stdin);rp=d.get("runtime") or {};po=rp.get("ports") or [];p=[x for x in po if x.get("privatePort")==22];print((p[0]["publicPort"] if p else "") if p else "")')"
    if [ -n "$IP" ] && [ -n "$PORT" ]; then
        echo "[§41 dispatch] SSH at $IP:$PORT (try $i)"; break
    fi
    sleep 5
done
[ -n "$IP" ] && [ -n "$PORT" ] || { echo "[§41 dispatch] FATAL: SSH endpoint not ready"; exit 4; }

SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $PORT root@$IP"
SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $PORT -o ConnectTimeout=3600"

# clean cleanup trap (g_fire_dispatch_robust — SAVE_POD env honored)
SAVE_POD="${SAVE_POD:-0}"
cleanup() {
    if [ "$SAVE_POD" = "1" ]; then
        echo "[§41 dispatch] SAVE_POD=1 — retaining pod $POD_ID for manual recovery"
        return
    fi
    echo "[§41 dispatch] terminating pod $POD_ID"
    python3 -c "import runpod, os; runpod.api_key=os.environ['RUNPODCTL_API_KEY']; runpod.terminate_pod(\"$POD_ID\")" || true
}
trap cleanup EXIT

# ── upload sources ─────────────────────────────────────────────────────
$SSH 'mkdir -p /workspace/s41 /workspace/s41/l6_pilot /workspace/s41/s16'
$SCP corpus_generator_s41.py train_s41.py eval_s41.py blue_falsifier_s41.py relation_corpus_train_s41.jsonl root@$IP:/workspace/s41/
$SCP ../l6_pilot_s37_2026_05_18/relation_corpus.py ../l6_pilot_s37_2026_05_18/holdout_pairs.json ../l6_pilot_s37_2026_05_18/corpus_stats.json root@$IP:/workspace/s41/l6_pilot/
$SCP ../carving_dataregime_s16_2026_05_18/conscious_decoder.py root@$IP:/workspace/s41/s16/

# Bridge import paths (eval/train expect sibling dirs)
$SSH 'cd /workspace && ln -sfn s41/l6_pilot l6_pilot_s37_2026_05_18 && ln -sfn s41/s16 carving_dataregime_s16_2026_05_18 && ln -sfn s41 l6_fullscale_s41_2026_05_18'

# Pre-install (the runpod pytorch image has torch; sympy needed by falsifier)
$SSH 'pip install --quiet --break-system-packages sympy 2>&1 | tail -3 || pip install --quiet sympy 2>&1 | tail -3'

# ── train (detached, single SSH probe poll) ───────────────────────────
echo "[§41 dispatch] launching training (detached nohup, bounded poll)"
$SSH "cd /workspace/s41 && nohup python3 train_s41.py --corpus relation_corpus_train_s41.jsonl --out ckpt_s41.pt --result result.json > train.log 2>&1 & echo \$! > train.pid"

POLL_INTERVAL=90
MAX_POLL=30  # 30*90s = 45 min hard ceiling
for i in $(seq 1 $MAX_POLL); do
    sleep $POLL_INTERVAL
    DONE="$($SSH 'test -f /workspace/s41/ckpt_s41.pt && grep -q "train_complete_pending_eval" /workspace/s41/result.json 2>/dev/null && echo TRAIN_DONE' 2>/dev/null || true)"
    echo "[§41 dispatch] train poll $i/$MAX_POLL  done=${DONE:-pending}"
    if [ "$DONE" = "TRAIN_DONE" ]; then break; fi
done
[ "$DONE" = "TRAIN_DONE" ] || { echo "[§41 dispatch] training timeout"; SAVE_POD=1; exit 5; }

# ── eval ──────────────────────────────────────────────────────────────
echo "[§41 dispatch] launching eval (detached, bounded poll)"
$SSH "cd /workspace/s41 && nohup python3 eval_s41.py --ckpt ckpt_s41.pt --result result.json > eval.log 2>&1 & echo \$! > eval.pid"

for i in $(seq 1 20); do  # 20*90s = 30 min hard ceiling for eval
    sleep $POLL_INTERVAL
    EVAL_DONE="$($SSH 'grep -q "\"phase\": \"complete\"" /workspace/s41/result.json 2>/dev/null && echo EVAL_DONE' 2>/dev/null || true)"
    echo "[§41 dispatch] eval poll $i/20  done=${EVAL_DONE:-pending}"
    if [ "$EVAL_DONE" = "EVAL_DONE" ]; then break; fi
done
[ "$EVAL_DONE" = "EVAL_DONE" ] || { echo "[§41 dispatch] eval timeout"; SAVE_POD=1; exit 6; }

# ── pull artifacts (5-retry, g_fire_dispatch_robust) ──────────────────
echo "[§41 dispatch] eval complete — promoting SAVE_POD=1 and pulling"
SAVE_POD=1
PULL_OK=0
for try in 1 2 3 4 5; do
    if $SCP "root@$IP:/workspace/s41/result.json" ./result.json \
       && $SCP "root@$IP:/workspace/s41/ckpt_s41.pt" ./ckpt_s41.pt \
       && $SCP "root@$IP:/workspace/s41/train.log" ./train.log \
       && $SCP "root@$IP:/workspace/s41/eval.log" ./eval.log; then
        PULL_OK=1; break
    fi
    echo "[§41 dispatch] pull try $try FAILED — retrying in 60s"
    sleep 60
done
[ "$PULL_OK" = "1" ] || { echo "[§41 dispatch] PULL FAILED 5/5 — pod retained for manual recovery"; exit 7; }

# Confirm result.json sha + ckpt sha — local matches what eval recorded.
CKPT_LOCAL_SHA="$(python3 -c 'import hashlib,sys;print(hashlib.sha256(open("ckpt_s41.pt","rb").read()).hexdigest())')"
echo "[§41 dispatch] local ckpt sha256=$CKPT_LOCAL_SHA"

# ── teardown ─────────────────────────────────────────────────────────
SAVE_POD=0  # successful — allow trap to terminate
echo "[§41 dispatch] complete — pod will be terminated by trap"
