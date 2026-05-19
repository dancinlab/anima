#!/usr/bin/env bash
# RESEARCH.md §46 — SGD-trajectory variance multi-seed §16 refire dispatch
# (g_fire_dispatch_robust + g_resource_active_parallel + f_hardcoded_credential).
#
# Tests §42's prediction: tier≥77 17-vs-29 routing-success split is NOT
# separable by anchor property (top acc 0.6739, nc-lift 0.241) — §42 hypothesis:
#   "within-band routing-success looks like SGD-trajectory lottery within
#    an already-necessary band; re-firing §16 with a different seed would
#    re-shuffle which 17 anchors of the 46 land in the success set".
#
# Design: §16 trainer + §16 corpus byte-identical (single corpus generation
# at seed=1337 — corpus is the §16 SSOT, sha256 422c64a0…); ONLY the trainer
# `--seed` varies. SEEDS = {2026, 7777} (2-fire sequential on single pod —
# cost <2× single fire, complete trajectory isolation, simpler than parallel).
# Original §16 used seed 1337 → its routing-correct set is the third datapoint
# already on file (eval_result_s16.json, 21 anchors).
#
# Credentials: read from `secret` CLI — RUNPOD_KEY hard-coded literal is
# forbidden (f_hardcoded_credential). This script reads runpod.api_key at
# runtime; literal API-key strings would trip `git diff --cached | grep` pre-commit.
#
# Cost head (g_fire_autonomous transparent cost note, NOT gate):
#   A100 80GB PCIe ~$1.89/hr · §16 train wall 1810s + eval ~3min → ~$1.10/seed
#   × 2 seeds + corpus-gen ~3min once → ≈ $2.30-3.00 estimate.
#   (Reusable corpus = a fixed cost paid once; runpod primary, vast.ai fallback
#    only on stock exhaust per g_resource_active_parallel.)
set -euo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$HERE"

# Seed list — both fires share corpus, vary only trainer seed (§16 used 1337
# already, on file as the third datapoint — we add 2 new seeds for triangulation).
SEEDS=(2026 7777)

# ── credentials via `secret` CLI (f_hardcoded_credential safety) ───────
RUNPOD_KEY="$(secret get runpod.api_key 2>/dev/null || echo '')"
if [ -z "$RUNPOD_KEY" ]; then
    echo "[§46 dispatch] FATAL: secret get runpod.api_key returned empty"
    echo "[§46 dispatch] register via: printf %s '<api_key>' | secret set runpod.api_key"
    exit 1
fi
export RUNPODCTL_API_KEY="$RUNPOD_KEY"

# ── pod create (A100 80GB PCIe primary, GPU cascade fallback) ─────────
export GPU_TYPE="${GPU_TYPE:-NVIDIA A100 80GB PCIe}"
export POD_NAME="s46-seed-variance-$(date +%s)"
export IMAGE="${IMAGE:-runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04}"
export DISK_GB="${DISK_GB:-80}"
echo "[§46 dispatch] requesting pod GPU=$GPU_TYPE  name=$POD_NAME  image=$IMAGE  disk=${DISK_GB}GB"

POD_JSON="$(python3 - <<'PY'
import os, json, runpod, time
runpod.api_key = os.environ['RUNPODCTL_API_KEY']
gpus = runpod.get_gpus()
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
echo "[§46 dispatch] pod_create response: $POD_JSON"
POD_ID="$(echo "$POD_JSON" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("id",""))')"
[ -n "$POD_ID" ] || { echo "[§46 dispatch] FATAL: pod create failed"; exit 3; }

# Get ssh endpoint after pod boots
echo "[§46 dispatch] pod_id=$POD_ID  waiting for SSH..."
IP=""; PORT=""
for i in $(seq 1 60); do
    POD_META="$(python3 -c "import runpod, os, json; runpod.api_key=os.environ['RUNPODCTL_API_KEY']; print(json.dumps(runpod.get_pod(\"$POD_ID\")))")"
    IP="$(echo "$POD_META" | python3 -c 'import sys,json;d=json.load(sys.stdin);rp=d.get("runtime") or {};po=rp.get("ports") or [];p=[x for x in po if x.get("privatePort")==22];print((p[0]["ip"] if p else "") if p else "")')"
    PORT="$(echo "$POD_META" | python3 -c 'import sys,json;d=json.load(sys.stdin);rp=d.get("runtime") or {};po=rp.get("ports") or [];p=[x for x in po if x.get("privatePort")==22];print((p[0]["publicPort"] if p else "") if p else "")')"
    if [ -n "$IP" ] && [ -n "$PORT" ]; then
        echo "[§46 dispatch] SSH at $IP:$PORT (try $i)"; break
    fi
    sleep 5
done
[ -n "$IP" ] && [ -n "$PORT" ] || { echo "[§46 dispatch] FATAL: SSH endpoint not ready"; exit 4; }

SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $PORT root@$IP"
SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $PORT -o ConnectTimeout=3600"

# clean cleanup trap (g_fire_dispatch_robust — SAVE_POD env honored)
SAVE_POD="${SAVE_POD:-0}"
cleanup() {
    if [ "$SAVE_POD" = "1" ]; then
        echo "[§46 dispatch] SAVE_POD=1 — retaining pod $POD_ID for manual recovery"
        return
    fi
    echo "[§46 dispatch] terminating pod $POD_ID"
    python3 -c "import runpod, os; runpod.api_key=os.environ['RUNPODCTL_API_KEY']; runpod.terminate_pod(\"$POD_ID\")" || true
}
trap cleanup EXIT

# ── upload sources (§16 trainer + decoder + generator + eval, byte-identical) ─
$SSH 'mkdir -p /workspace/s46'
$SCP ../carving_dataregime_s16_2026_05_18/train_carving_s16.py \
     ../carving_dataregime_s16_2026_05_18/conscious_decoder.py \
     ../carving_dataregime_s16_2026_05_18/corpus_carving_s16_generator.py \
     ../carving_dataregime_s16_2026_05_18/eval_carving_s16.py \
     root@$IP:/workspace/s46/

# Pre-install (the runpod pytorch image has torch; sympy needed by aux).
$SSH 'pip install --quiet --break-system-packages sympy 2>&1 | tail -3 || pip install --quiet sympy 2>&1 | tail -3'

# ── corpus generation (once, seed=1337 → byte-identical to §16) ────────
echo "[§46 dispatch] generating §16 corpus (seed=1337, byte-identical to §16)"
$SSH "cd /workspace/s46 && nohup python3 corpus_carving_s16_generator.py --out corpus_carving_s16.jsonl --seed 1337 > corpus_gen.log 2>&1 & echo \$! > corpus.pid"

# Poll for corpus completion (small file → ~3 min)
CORPUS_DONE=""
for i in $(seq 1 20); do
    sleep 30
    CORPUS_DONE="$($SSH 'test -f /workspace/s46/corpus_carving_s16.stats.json && echo CORPUS_DONE' 2>/dev/null || true)"
    echo "[§46 dispatch] corpus poll $i/20  done=${CORPUS_DONE:-pending}"
    if [ "$CORPUS_DONE" = "CORPUS_DONE" ]; then break; fi
done
[ "$CORPUS_DONE" = "CORPUS_DONE" ] || { echo "[§46 dispatch] corpus generation timeout"; SAVE_POD=1; exit 5; }

# Verify corpus sha == §16 SSOT (byte-identical contract)
CORPUS_SHA="$($SSH 'python3 -c "import hashlib;print(hashlib.sha256(open(\"/workspace/s46/corpus_carving_s16.jsonl\",\"rb\").read()).hexdigest())"' 2>/dev/null || echo '')"
EXPECTED_SHA="422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec"
echo "[§46 dispatch] corpus sha256: $CORPUS_SHA"
echo "[§46 dispatch] expected sha:  $EXPECTED_SHA"
if [ "$CORPUS_SHA" != "$EXPECTED_SHA" ]; then
    echo "[§46 dispatch] FATAL: corpus sha mismatch — §16-byte-identity broken"
    SAVE_POD=1; exit 6
fi
echo "[§46 dispatch] corpus matches §16 SSOT — proceeding to seed loop"

# ── per-seed train + eval loop (sequential on one pod) ────────────────
POLL_INTERVAL=90
MAX_POLL=40  # 40 * 90s = 60 min per seed (train wall §16 = ~30min)
EVAL_MAX_POLL=20

for SEED in "${SEEDS[@]}"; do
    echo "[§46 dispatch] === SEED $SEED training (detached nohup, bounded poll) ==="
    $SSH "cd /workspace/s46 && rm -rf out_seed_$SEED && mkdir out_seed_$SEED && \
          nohup python3 train_carving_s16.py \
              --corpus corpus_carving_s16.jsonl \
              --out-dir out_seed_$SEED \
              --steps 12000 \
              --seed $SEED \
              > train_seed_$SEED.log 2>&1 & echo \$! > train_$SEED.pid"

    DONE=""
    for i in $(seq 1 $MAX_POLL); do
        sleep $POLL_INTERVAL
        DONE="$($SSH "grep -q RESULT_JSON_WRITTEN /workspace/s46/train_seed_$SEED.log 2>/dev/null && echo TRAIN_DONE" 2>/dev/null || true)"
        echo "[§46 dispatch] seed=$SEED train poll $i/$MAX_POLL  done=${DONE:-pending}"
        if [ "$DONE" = "TRAIN_DONE" ]; then break; fi
    done
    [ "$DONE" = "TRAIN_DONE" ] || { echo "[§46 dispatch] training timeout seed=$SEED"; SAVE_POD=1; exit 7; }

    echo "[§46 dispatch] === SEED $SEED eval (detached, bounded poll) ==="
    $SSH "cd /workspace/s46 && nohup python3 eval_carving_s16.py \
              --ckpt out_seed_$SEED/ckpt_carving_s16.pt \
              --output eval_result_seed_$SEED.json \
              --device cuda \
              > eval_seed_$SEED.log 2>&1 & echo \$! > eval_$SEED.pid"

    EVAL_DONE=""
    for i in $(seq 1 $EVAL_MAX_POLL); do
        sleep $POLL_INTERVAL
        EVAL_DONE="$($SSH "test -f /workspace/s46/eval_result_seed_$SEED.json && python3 -c 'import json;d=json.load(open(\"/workspace/s46/eval_result_seed_$SEED.json\"));print(\"OK\" if \"axis1_knowledge_access\" in d else \"NO\")' 2>/dev/null | grep -q OK && echo EVAL_DONE" 2>/dev/null || true)"
        echo "[§46 dispatch] seed=$SEED eval poll $i/$EVAL_MAX_POLL  done=${EVAL_DONE:-pending}"
        if [ "$EVAL_DONE" = "EVAL_DONE" ]; then break; fi
    done
    [ "$EVAL_DONE" = "EVAL_DONE" ] || { echo "[§46 dispatch] eval timeout seed=$SEED"; SAVE_POD=1; exit 8; }
done

# ── pull all artifacts (5-retry, g_fire_dispatch_robust) ──────────────
echo "[§46 dispatch] both seeds complete — promoting SAVE_POD=1 and pulling"
SAVE_POD=1

# Pull corpus stats + each seed's train log + result.json + eval_result + ckpt.
PULL_OK=0
for try in 1 2 3 4 5; do
    OK=1
    $SCP "root@$IP:/workspace/s46/corpus_carving_s16.stats.json" ./corpus_carving_s16.stats.json || OK=0
    for SEED in "${SEEDS[@]}"; do
        $SCP "root@$IP:/workspace/s46/train_seed_$SEED.log" ./train_seed_$SEED.log || OK=0
        $SCP "root@$IP:/workspace/s46/eval_seed_$SEED.log" ./eval_seed_$SEED.log || OK=0
        $SCP "root@$IP:/workspace/s46/eval_result_seed_$SEED.json" ./eval_result_seed_$SEED.json || OK=0
        $SCP "root@$IP:/workspace/s46/out_seed_$SEED/result.json" ./result_seed_$SEED.json || OK=0
        # ckpt is large (~1.1 GB) — pull but keep in gitignore (only sha matters for §46)
        $SCP "root@$IP:/workspace/s46/out_seed_$SEED/ckpt_carving_s16.pt" ./ckpt_seed_$SEED.pt || OK=0
    done
    if [ "$OK" = "1" ]; then PULL_OK=1; break; fi
    echo "[§46 dispatch] pull try $try FAILED — retrying in 60s"
    sleep 60
done
[ "$PULL_OK" = "1" ] || { echo "[§46 dispatch] PULL FAILED 5/5 — pod retained for manual recovery"; exit 9; }

# Confirm each ckpt local sha
for SEED in "${SEEDS[@]}"; do
    SHA="$(python3 -c "import hashlib;print(hashlib.sha256(open('ckpt_seed_$SEED.pt','rb').read()).hexdigest())")"
    echo "[§46 dispatch] seed=$SEED  local ckpt sha256=$SHA"
done

# ── teardown ─────────────────────────────────────────────────────────
SAVE_POD=0  # successful — allow trap to terminate
echo "[§46 dispatch] complete — pod will be terminated by trap"
