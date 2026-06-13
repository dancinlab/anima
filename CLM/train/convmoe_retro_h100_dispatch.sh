#!/usr/bin/env bash
# convmoe_retro_h100_dispatch.sh — rent 1x H100 SXM 80GB, train ConvMoE-RETRO 303M
# (baseline_fast recipe), harvest ckpt/.clm/result/log, HF-upload PRIVATE, terminate.
#
# Lifecycle = RunPod GraphQL (podFindAndDeployOnDemand + podTerminate) — NOT runpodctl
# (the prior 7B fire's runpodctl teardown FAILED on a version mismatch). Transport = ssh/scp.
# a_fire_autonomous / a_wall_first / a_fire_recover_complete / a_cpu_local_no_waiter.
set -uo pipefail

RPKEY="$(secret get runpod.api_key)"
GQL="https://api.runpod.io/graphql?api_key=${RPKEY}"
GPU="NVIDIA H100 80GB HBM3"
IMAGE="runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"
PUBKEY="$(cat ~/.ssh/id_ed25519.pub)"
WT="$(cd "$(dirname "$0")/../.." && pwd)"            # worktree root
OUT="${WT}/state/convmoe_retro_prod"
LOG="${OUT}/dispatch.log"
mkdir -p "$OUT"

log(){ echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
gql(){ curl -s --max-time 60 "$GQL" -H 'Content-Type: application/json' -d "$1"; }

# ---------------------------------------------------------------- rent
log "renting 1x H100 SXM 80GB on-demand..."
ENV_PUB=$(printf '%s' "$PUBKEY" | sed 's/"/\\"/g')
PODNAME="anima-convmoe-retro-303m-$(date +%H%M%S)"     # unique suffix => distinguishable from any stale dup
CREATE_Q=$(cat <<JSON
{"query":"mutation { podFindAndDeployOnDemand(input:{cloudType:ALL, gpuCount:1, volumeInGb:80, containerDiskInGb:80, minVcpuCount:8, minMemoryInGb:64, gpuTypeId:\"${GPU}\", name:\"${PODNAME}\", imageName:\"${IMAGE}\", dockerArgs:\"\", ports:\"22/tcp\", volumeMountPath:\"/workspace\", env:[{key:\"PUBLIC_KEY\",value:\"${ENV_PUB}\"}]}) { id imageName machineId } }"}
JSON
)
RESP=$(gql "$CREATE_Q"); log "create resp: $RESP"
POD_ID=$(printf '%s' "$RESP" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('data',{}).get('podFindAndDeployOnDemand',{}).get('id','') or '')" 2>/dev/null)
if [ -z "$POD_ID" ]; then log "FATAL: rent failed (no pod id)"; exit 2; fi
log "POD_ID=$POD_ID"
echo "$POD_ID" > "$OUT/pod_id.txt"

# ---------------------------------------------------------------- wait for SSH
log "waiting for pod RUNNING + ssh port..."
HOST=""; PORT=""
for i in $(seq 1 60); do
  Q='{"query":"query { pod(input:{podId:\"'"$POD_ID"'\"}) { desiredStatus runtime { ports { ip isIpPublic privatePort publicPort type } } } }"}'
  R=$(gql "$Q")
  read HOST PORT < <(printf '%s' "$R" | python3 -c "
import sys,json
d=json.load(sys.stdin)
rt=(d.get('data',{}).get('pod') or {}).get('runtime') or {}
for p in (rt.get('ports') or []):
    if p.get('privatePort')==22 and p.get('isIpPublic'):
        print(p['ip'], p['publicPort']); break
" 2>/dev/null)
  if [ -n "${HOST:-}" ] && [ -n "${PORT:-}" ]; then log "ssh ready: $HOST:$PORT"; break; fi
  sleep 15
done
if [ -z "${HOST:-}" ]; then log "FATAL: no ssh endpoint after wait"; exit 3; fi
echo "$HOST $PORT" > "$OUT/ssh_endpoint.txt"
# ServerAliveInterval + ConnectTimeout + a per-cmd timeout so the inline poll can NEVER
# block indefinitely on a stalled SSH (the prod fire's poll hung 1h+ with 0 CPU on a
# blocked poll SSH — these options make every poll cmd return within ~30s, win or fail).
SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=20 -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -p $PORT root@$HOST"
SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=20 -o ServerAliveInterval=15 -P $PORT"

# wait until sshd answers
for i in $(seq 1 40); do $SSH "echo ok" 2>/dev/null | grep -q ok && break; sleep 10; done

# ---------------------------------------------------------------- upload code
log "uploading code..."
$SSH "mkdir -p /workspace/anima/CLM/model /workspace/anima/CLM/train /workspace/anima/UNIVERSE"
$SCP "$WT/CLM/model/model.py"               root@$HOST:/workspace/anima/CLM/model/ >/dev/null
$SCP "$WT/CLM/model/clm_serialize_v2.py"    root@$HOST:/workspace/anima/CLM/model/ >/dev/null
$SCP "$WT/CLM/model/verify_clm_v2.py"       root@$HOST:/workspace/anima/CLM/model/ >/dev/null
$SCP "$WT/CLM/model/retro303m_en.py"        root@$HOST:/workspace/anima/CLM/model/ >/dev/null
$SCP "$WT/UNIVERSE/h1129_midcap_broad_converged_recombination.py" root@$HOST:/workspace/anima/UNIVERSE/ >/dev/null
$SCP "$WT/CLM/train/train_convmoe_retro_prod.py" root@$HOST:/workspace/anima/CLM/train/ >/dev/null
$SCP "$WT/CLM/train/convmoe_retro_remote.sh" root@$HOST:/workspace/anima/ >/dev/null

# ---------------------------------------------------------------- launch (nohup remote)
log "launching remote train+eval+serialize (nohup)..."
HFTOK="$(secret get hf.token 2>/dev/null || echo '')"
$SSH "cd /workspace/anima && HF_TOKEN='${HFTOK}' nohup bash convmoe_retro_remote.sh > /workspace/train.log 2>&1 & echo LAUNCHED \$!"

# ---------------------------------------------------------------- inline poll (a_cpu_local_no_waiter)
# Each poll cmd is hard-wrapped in `timeout 40` so a stalled SSH can NEVER hang the loop
# (the prod fire hung 1h on a blocked poll SSH). One combined remote probe per iteration.
log "polling remote until DONE marker..."
DONE=0
SD=/workspace/anima/state/convmoe_retro_prod
for i in $(seq 1 240); do          # up to ~2h (30s * 240)
  PROBE=$(timeout 40 $SSH "if [ -f $SD/DONE ]; then echo DONE; elif [ -f $SD/FAILED ]; then echo FAILED; else echo RUN; fi; tail -2 /workspace/train.log 2>/dev/null" 2>/dev/null)
  STAT=$(printf '%s' "$PROBE" | head -1)
  TAIL=$(printf '%s' "$PROBE" | tail -n +2 | tr '\n' ' ')
  log "  poll $i [$STAT]: $TAIL"
  if [ "$STAT" = "DONE" ]; then DONE=1; log "remote DONE"; break; fi
  if [ "$STAT" = "FAILED" ]; then log "remote FAILED"; break; fi
  sleep 30
done

# ---------------------------------------------------------------- harvest (BEFORE teardown)
log "harvesting artifacts..."
$SCP -r root@$HOST:/workspace/anima/state/convmoe_retro_prod/. "$OUT/" >/dev/null 2>&1 || log "WARN: state harvest partial"
$SCP root@$HOST:/workspace/train.log "$OUT/train.log" >/dev/null 2>&1 || true
ls -la "$OUT" | tee -a "$LOG"

echo "$DONE" > "$OUT/.done_flag"
log "harvest complete. DONE=$DONE. (HF upload + teardown handled by caller)"
