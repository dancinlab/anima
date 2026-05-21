#!/usr/bin/env bash
# Manual artifact-puller for S187-G dispatches that lost their dispatch
# wrapper (env-verify SSH timeout, monitor session terminated, etc.).
#
# Usage:
#   bash pull_s187g_artifacts.sh <pod_id> <variant> <mit_mode> [seed]
# Example:
#   bash pull_s187g_artifacts.sh kg46v7uniyupt4 A ctrl 1337
set -euo pipefail
POD_ID="$1"
VARIANT="$2"
MIT_MODE="$3"
SEED="${4:-1337}"
SEED_TAG=""
case "$SEED" in
  1337) SEED_TAG="" ;;
  42)   SEED_TAG="_s42" ;;
  *)    SEED_TAG="_s${SEED}" ;;
esac

SDIR="/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21"
VDIR="$SDIR/g_${VARIANT}_${MIT_MODE}${SEED_TAG}"
mkdir -p "$VDIR"

RK="$(secret get runpod.api_key)"
GQL="https://api.runpod.io/graphql?api_key=${RK}"

echo "[pull] resolving SSH for $POD_ID"
PR=$(curl -s -X POST "$GQL" -H "Content-Type: application/json" \
    -d "{\"query\":\"query { pod(input:{podId:\\\"$POD_ID\\\"}) { runtime { ports { ip publicPort privatePort isIpPublic } } } }\"}")
read -r IP PORT < <(echo "$PR" | python3 -c "
import sys,json
d=json.load(sys.stdin)
rt=((d.get('data',{}).get('pod') or {}).get('runtime') or {}) or {}
for p in (rt.get('ports') or []):
    if p.get('privatePort')==22 and p.get('isIpPublic') and p.get('ip') and p.get('publicPort'):
        print(p['ip'], p['publicPort']); break
")
[ -z "$IP" ] && { echo "FATAL: no SSH for pod $POD_ID"; exit 1; }
echo "[pull] SSH $IP:$PORT"
SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=15 -p $PORT root@$IP"
SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=15 -P $PORT"

# Wait for ckpt to appear (poll every 60s, 30 min cap)
S187R=/workspace/s187r
CKPT_POD="$S187R/out_main/ckpt_s184_combined.pt"
RESULT_POD="$S187R/out_main/result.json"

for i in $(seq 1 30); do
  if $SSH "test -s $CKPT_POD && test -s $RESULT_POD && echo OK" 2>/dev/null | grep -q OK; then
    echo "[pull] artifacts ready (iter $i)"
    break
  fi
  ALIVE=$($SSH 'pgrep -f train_s187_3b.py >/dev/null && echo ALIVE || echo DEAD' 2>/dev/null || echo "UNREACHABLE")
  echo "[pull] iter $i: $ALIVE - sleeping 60"
  $SSH "tail -2 $S187R/train.log 2>/dev/null" 2>/dev/null | sed 's/^/  /'
  if [ "$ALIVE" = "DEAD" ]; then
    echo "[pull] trainer died — checking for ckpt anyway"
    $SSH "ls -la $S187R/out_main 2>/dev/null"
  fi
  sleep 60
done

# Pull
for k in 1 2 3 4 5; do
  $SCP "root@$IP:$RESULT_POD"      "$VDIR/result.json" && \
  $SCP "root@$IP:$CKPT_POD"        "$VDIR/ckpt_s187g_${VARIANT}_${MIT_MODE}${SEED_TAG}.pt" && \
  $SCP "root@$IP:$S187R/train.log" "$VDIR/train.log" && \
  { echo "[pull] success try $k"; break; }
  echo "[pull] retry $k failed"; sleep 60
done

if [ -s "$VDIR/result.json" ]; then
  echo "[pull] DONE; terminating pod $POD_ID"
  curl -s -X POST "$GQL" -H "Content-Type: application/json" \
    -d "{\"query\":\"mutation { podTerminate(input:{podId:\\\"$POD_ID\\\"}) }\"}" >/dev/null
  sha256sum "$VDIR/ckpt_s187g_${VARIANT}_${MIT_MODE}${SEED_TAG}.pt"
  python3 -c "
import json
d=json.load(open('$VDIR/result.json'))
fl=d.get('final_log') or {}
ms=d.get('mitosis_summary') or {}
print('=== g_${VARIANT}_${MIT_MODE} ===')
print('  n_params=',d.get('n_params'),'wall_s=',round(d.get('train_wall_s',0),1),'final_CE=',fl.get('L_ce'))
print('  mitosis_active=',d.get('mitosis_active'),'lambda_mitosis=',d.get('lambda_mitosis'))
print('  final_L_mitosis=',fl.get('L_mitosis'))
print('  TRAIN-pool: splits=',ms.get('splits'),'merges=',ms.get('merges'),'final_cells=',ms.get('final_cells'),'phi_final=',round(ms.get('phi_final',0.0),4))
"
else
  echo "[pull] FAILED — pod $POD_ID retained for manual recovery"
fi
