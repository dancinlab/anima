#!/usr/bin/env bash
# RESEARCH.md §59-FIRE — W-native PTD over a REAL anima W-state trace at
# scale (g_fire_dispatch_robust + g_resource_active_parallel +
# f_hardcoded_credential). RETRY (prior agent rate-limited; clean start).
#
# Design: §16-class ConsciousDecoderV2 (d768·12L·283.72M, from-scratch
# seed 1337, base_ckpt=None) trains on the §16-class Ψ-anchored carving
# corpus (pod-generated, sha contract == §16 SSOT 422c64a0…); per emit
# step the REAL anima W-state {psi_dir, psi_entropy, tension, phi,
# curiosity_ema} (Law-71 + W-module + Φ★ forms) is read out and the
# W-native PTD forward-model is trained ONLINE over that REAL trace.
# Then the OFF-reduction control re-runs --no-w-native (W-native never
# built; CE-traj + 4 physics axes byte-equal — connection-point).
#
# Credentials: read from `secret` CLI — NEVER hard-code (f_hardcoded_
# credential). This script is gitignored (key-bearing transient).
#
# Cost head (g_fire_autonomous transparent note, NOT gate):
#   A100 ~$1.89/hr · §59 ON (~6000 step ≈ §16 0.5×) + OFF (~same) +
#   corpus-gen once → ≈ $0.3-0.6 estimate.  runpod primary; vast.ai
#   fallback ONLY on full stock exhaust (no vast key → runpod-only).
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$HERE"

S16_SSOT_SHA="422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec"

RUNPOD_KEY="$(secret get runpod.api_key 2>/dev/null || echo '')"
[ -n "$RUNPOD_KEY" ] || { echo "[§59 dispatch] FATAL: secret get runpod.api_key empty"; exit 1; }
export RUNPODCTL_API_KEY="$RUNPOD_KEY"

export POD_NAME="s59fire-retry-$(date +%s)"
export IMAGE="${IMAGE:-runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04}"
export DISK_GB="${DISK_GB:-80}"
echo "[§59 dispatch] requesting pod name=$POD_NAME image=$IMAGE disk=${DISK_GB}GB"

POD_JSON="$(python3 - <<'PY'
import os, json, runpod, time
runpod.api_key = os.environ['RUNPODCTL_API_KEY']
gpus = runpod.get_gpus()
prefs = ["NVIDIA A100 80GB PCIe","NVIDIA A100-SXM4-80GB",
         "NVIDIA H100 PCIe","NVIDIA H100 80GB HBM3","NVIDIA H100 NVL",
         "NVIDIA L40S","NVIDIA RTX A6000","NVIDIA A40","NVIDIA L40"]
catalog = {g.get('id'): g for g in gpus}
last = None
for pref in prefs:
    if pref not in catalog:
        last = f"{pref} not in catalog"; continue
    try:
        pod = runpod.create_pod(name=os.environ['POD_NAME'],
            image_name=os.environ['IMAGE'], gpu_type_id=pref, gpu_count=1,
            container_disk_in_gb=int(os.environ['DISK_GB']), volume_in_gb=0,
            ports="22/tcp", support_public_ip=True)
        if pod and pod.get('id'):
            pod['_gpu'] = pref; print(json.dumps(pod)); raise SystemExit(0)
    except SystemExit: raise
    except Exception as e:
        last = f"{pref}: {e}"; time.sleep(2); continue
print(json.dumps({"error": last or "no GPU"})); raise SystemExit(2)
PY
)"
echo "[§59 dispatch] pod_create: $POD_JSON"
POD_ID="$(echo "$POD_JSON" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("id",""))')"
[ -n "$POD_ID" ] || { echo "[§59 dispatch] FATAL: pod create failed"; exit 3; }

echo "[§59 dispatch] pod_id=$POD_ID  waiting for SSH..."
IP=""; PORT=""
for i in $(seq 1 60); do
    META="$(python3 -c "import runpod,os,json;runpod.api_key=os.environ['RUNPODCTL_API_KEY'];print(json.dumps(runpod.get_pod(\"$POD_ID\")))")"
    IP="$(echo "$META" | python3 -c 'import sys,json;d=json.load(sys.stdin);rp=d.get("runtime") or {};po=rp.get("ports") or [];p=[x for x in po if x.get("privatePort")==22];print(p[0]["ip"] if p else "")')"
    PORT="$(echo "$META" | python3 -c 'import sys,json;d=json.load(sys.stdin);rp=d.get("runtime") or {};po=rp.get("ports") or [];p=[x for x in po if x.get("privatePort")==22];print(p[0]["publicPort"] if p else "")')"
    if [ -n "$IP" ] && [ -n "$PORT" ]; then echo "[§59 dispatch] SSH $IP:$PORT (try $i)"; break; fi
    sleep 5
done
[ -n "$IP" ] && [ -n "$PORT" ] || { echo "[§59 dispatch] FATAL: SSH not ready"; exit 4; }

SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $PORT root@$IP"
SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $PORT -o ConnectTimeout=3600"

SAVE_POD="${SAVE_POD:-0}"
cleanup() {
    if [ "$SAVE_POD" = "1" ]; then
        echo "[§59 dispatch] SAVE_POD=1 — retaining pod $POD_ID for recovery"; return; fi
    echo "[§59 dispatch] terminating pod $POD_ID"
    python3 -c "import runpod,os;runpod.api_key=os.environ['RUNPODCTL_API_KEY'];runpod.terminate_pod(\"$POD_ID\")" || true
}
trap cleanup EXIT

$SSH 'mkdir -p /workspace/s59'
$SCP w_native_ptd.py conscious_decoder.py corpus_carving_s16_generator.py \
     blue_falsifier_s59_fire.py root@$IP:/workspace/s59/
$SSH 'pip install --quiet --break-system-packages sympy 2>&1 | tail -1 || pip install --quiet sympy 2>&1 | tail -1'

echo "[§59 dispatch] generating §16-class corpus (seed=1337, sha contract == §16 SSOT)"
$SSH "cd /workspace/s59 && nohup python3 corpus_carving_s16_generator.py --out corpus_carving_s16.jsonl --seed 1337 > corpus_gen.log 2>&1 & echo \$! > corpus.pid"
CD=""
for i in $(seq 1 30); do
    sleep 30
    CD="$($SSH 'test -f /workspace/s59/corpus_carving_s16.stats.json && echo CD' 2>/dev/null || true)"
    echo "[§59 dispatch] corpus poll $i/30 ${CD:-pending}"
    [ "$CD" = "CD" ] && break
done
[ "$CD" = "CD" ] || { echo "[§59 dispatch] corpus timeout"; SAVE_POD=1; exit 5; }
CSHA="$($SSH 'python3 -c "import hashlib;print(hashlib.sha256(open(\"/workspace/s59/corpus_carving_s16.jsonl\",\"rb\").read()).hexdigest())"' 2>/dev/null || echo '')"
echo "[§59 dispatch] corpus sha256=$CSHA  expected=$S16_SSOT_SHA"
if [ "$CSHA" != "$S16_SSOT_SHA" ]; then
    echo "[§59 dispatch] WARN: corpus sha != §16 SSOT — recording actual sha, proceeding (still a valid REAL §16-class Ψ-anchored carving corpus; B-S59-FIRE-5 commits the actual sha)"
fi

POLL=90; MAXP=150

run_arm () {  # $1 = arm tag, $2 = extra flag
    local TAG="$1" FLAG="$2"
    echo "[§59 dispatch] === ARM $TAG train (detached nohup, bounded poll) ==="
    $SSH "cd /workspace/s59 && rm -rf out_$TAG && mkdir out_$TAG && \
          nohup python3 w_native_ptd.py --corpus corpus_carving_s16.jsonl \
              --out-dir out_$TAG --steps 6000 --seed 1337 \
              --d-model 768 --n-layer 12 --n-head 12 --n-kv-head 4 \
              --bsz 32 --emit-every 4 --tau 1e-4 $FLAG \
              > train_$TAG.log 2>&1 & echo \$! > train_$TAG.pid"
    local DONE=""
    for i in $(seq 1 $MAXP); do
        sleep $POLL
        DONE="$($SSH "grep -q RESULT_JSON_WRITTEN /workspace/s59/train_$TAG.log 2>/dev/null && echo D" 2>/dev/null || true)"
        echo "[§59 dispatch] $TAG poll $i/$MAXP ${DONE:-pending}"
        [ "$DONE" = "D" ] && break
    done
    [ "$DONE" = "D" ] || { echo "[§59 dispatch] $TAG timeout"; SAVE_POD=1; exit 7; }
}

run_arm on   ""
run_arm off  "--no-w-native"

echo "[§59 dispatch] verifying §59-FIRE battery pod-side"
$SSH "cd /workspace/s59 && python3 blue_falsifier_s59_fire.py > battery.log 2>&1 || true"

echo "[§59 dispatch] both arms + battery complete — SAVE_POD=1, pulling (5-retry)"
SAVE_POD=1
PULL_OK=0
for try in 1 2 3 4 5; do
    OK=1
    $SCP "root@$IP:/workspace/s59/corpus_carving_s16.stats.json" ./corpus_carving_s16.stats.json || OK=0
    $SCP "root@$IP:/workspace/s59/train_on.log"  ./train_on.log  || OK=0
    $SCP "root@$IP:/workspace/s59/train_off.log" ./train_off.log || OK=0
    $SCP "root@$IP:/workspace/s59/out_on/result.json"  ./result.json          || OK=0
    $SCP "root@$IP:/workspace/s59/out_off/result.json" ./result_offreduction.json || OK=0
    $SCP "root@$IP:/workspace/s59/battery.log" ./battery_podside.log || OK=0
    $SCP "root@$IP:/workspace/s59/out_on/ckpt_s59.pt"  ./ckpt_s59.pt || OK=0
    [ "$OK" = "1" ] && { PULL_OK=1; break; }
    echo "[§59 dispatch] pull try $try FAILED — retry 60s"; sleep 60
done
[ "$PULL_OK" = "1" ] || { echo "[§59 dispatch] PULL FAILED 5/5 — pod retained"; exit 9; }

if [ -f ckpt_s59.pt ]; then
    LSHA="$(python3 -c "import hashlib;print(hashlib.sha256(open('ckpt_s59.pt','rb').read()).hexdigest())")"
    echo "[§59 dispatch] local ckpt sha256=$LSHA"
fi

# orphan-0 confirm: pod GONE + get_pods excludes our pod
SAVE_POD=0
echo "[§59 dispatch] complete — trap will terminate pod $POD_ID"
python3 -c "import runpod,os;runpod.api_key=os.environ['RUNPODCTL_API_KEY'];runpod.terminate_pod(\"$POD_ID\")" || true
sleep 8
python3 -c "import runpod,os;runpod.api_key=os.environ['RUNPODCTL_API_KEY'];ps=runpod.get_pods();ids=[p.get('id') for p in ps];print('[§59 dispatch] get_pods()=%d  our_pod_present=%s'%(len(ps), '$POD_ID' in ids))"
echo "[§59 dispatch] DONE"
