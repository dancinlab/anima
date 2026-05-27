#!/usr/bin/env bash
# P21G dispatch — vP21 LoRA continue-train on diverse wiki+anima mix.
#
# Forked from dispatch_p21_llama_mitosis_runpod.sh. Differences:
#   - Upload existing vP21/lora_adapter from local to pod
#   - Build BOTH wikitext + corpus_s101 on pod
#   - Continue-train (lower LR 5e-5, no mitosis) on 70/30 mix
#   - On-pod OOD held-out eval + anima-register Eval1 (both small JSON pulls)
#   - SAVE_POD=1 only if pull fails; else terminate
#
# Cost cap: $15. H100 80GB SXM ~$0.32/min ≈ 47 min cap. Expected wall:
#   - corpus build wiki=10-15 min download + build
#   - train 1000 step LoRA continue ≈ 4-6 min
#   - eval 60 generations ≈ 2-3 min
#   - total ≈ 20-25 min ≈ $7-8 actual.
set -uo pipefail

VARIANT="${1:-P21G}"
SEED="${2:-1337}"

S187_DIR="/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21"
BUILD_DIR="/Users/ghost/core/anima/state/corpus_s101_build_s102_2026_05_19"
S16_DIR="/Users/ghost/core/anima/state/carving_dataregime_s16_2026_05_18"
ANCHOR_DIR="/Users/ghost/core/anima/HEXAD/UNIVERSE-BRAIN-MAP/anchors"
VDIR="$S187_DIR/v${VARIANT}"
mkdir -p "$VDIR"
LOG="$VDIR/dispatch.log"
PODID_FILE="$VDIR/pod_id.txt"
FAIL_MARKER="$VDIR/FAILURE.txt"
WATCHDOG_SEC=${WATCHDOG_SEC:-3600}   # 1h cap (continue-train + small corpus + eval)
SSH_TRIES=60
GPU_CASCADE=("NVIDIA H100 80GB HBM3" "NVIDIA H100 NVL" "NVIDIA H100 PCIe" "NVIDIA A100-SXM4-80GB" "NVIDIA A100 80GB PCIe")
IMAGE="runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"

# P21G hyperparams
P21G_STEPS=${P21G_STEPS:-1000}
P21G_BSZ=${P21G_BSZ:-2}
P21G_BLOCK=${P21G_BLOCK:-512}
P21G_LR=${P21G_LR:-5e-5}
P21G_WARMUP=${P21G_WARMUP:-50}
P21G_WIKI_FRAC=${P21G_WIKI_FRAC:-0.7}
P21G_CORPUS_MB=${P21G_CORPUS_MB:-80}

VP21_ADAPTER_DIR="$S187_DIR/vP21/lora_adapter"
[ -d "$VP21_ADAPTER_DIR" ] || { echo "FATAL: vP21 adapter not found at $VP21_ADAPTER_DIR"; exit 1; }

exec > >(tee -a "$LOG") 2>&1
echo "=== P21G generalization-unlock dispatch start $(date -u +%FT%TZ) ==="
echo "    base=Qwen/Qwen2.5-1.5B vp21_adapter=$VP21_ADAPTER_DIR"
echo "    steps=$P21G_STEPS bsz=$P21G_BSZ block=$P21G_BLOCK lr=$P21G_LR warmup=$P21G_WARMUP"
echo "    wiki_frac=$P21G_WIKI_FRAC corpus_mb=$P21G_CORPUS_MB"

RK="$(secret get runpod.api_key 2>/dev/null)"
if [ -z "$RK" ] && [ -f "$HOME/.runpod/config.toml" ]; then
  RK="$(grep -E '^apikey' "$HOME/.runpod/config.toml" | head -1 | sed -E "s/.*=[[:space:]]*'([^']+)'.*/\1/")"
fi
[ -z "$RK" ] && { echo "FATAL no runpod key"; exit 1; }
GQL="https://api.runpod.io/graphql?api_key=${RK}"
PUBKEY="$(cat ~/.ssh/id_ed25519.pub 2>/dev/null)"
[ -z "$PUBKEY" ] && { echo "FATAL no ~/.ssh/id_ed25519.pub"; exit 1; }
SAVE_POD=0
POD_ID=""

gql() { curl -s -X POST "$GQL" -H "Content-Type: application/json" -d "$1"; }

teardown() {
  local rc=$?
  if [ -n "$POD_ID" ] && [ "$SAVE_POD" != "1" ]; then
    echo "[teardown] terminating pod $POD_ID (rc=$rc, SAVE_POD=$SAVE_POD)"
    gql "{\"query\":\"mutation { podTerminate(input:{podId:\\\"$POD_ID\\\"}) }\"}" >/dev/null
  elif [ -n "$POD_ID" ]; then
    echo "[teardown] SAVE_POD=1 - pod $POD_ID RETAINED"
  fi
  sleep 3
  local left; left="$(gql '{"query":"query { myself { pods { id } } }"}')"
  echo "[teardown] myself.pods = $left"
  echo "=== P21G dispatch end $(date -u +%FT%TZ) rc=$rc ==="
}
trap teardown EXIT

( sleep "$WATCHDOG_SEC"
  if [ ! -s "$VDIR/result.json" ]; then
    echo "WATCHDOG FIRED $(date -u +%FT%TZ): no result.json after ${WATCHDOG_SEC}s - terminating pod ${POD_ID:-?}" > "$FAIL_MARKER"
    [ -n "$POD_ID" ] && gql "{\"query\":\"mutation { podTerminate(input:{podId:\\\"$POD_ID\\\"}) }\"}" >/dev/null
    pkill -P $$ 2>/dev/null
  fi ) &
WATCHDOG_PID=$!

# pod create cascade
for GPU in "${GPU_CASCADE[@]}"; do
  echo "[create] trying GPU: $GPU"
  Q=$(cat <<JSON
{"query":"mutation { podFindAndDeployOnDemand(input:{cloudType: ALL, gpuCount:1, volumeInGb:0, containerDiskInGb:120, minVcpuCount:8, minMemoryInGb:64, gpuTypeId:\"$GPU\", name:\"p21g-generalize\", imageName:\"$IMAGE\", dockerArgs:\"\", ports:\"22/tcp\", volumeMountPath:\"/workspace\", env:[{key:\"PUBLIC_KEY\", value:\"$PUBKEY\"}]}) { id machineId } }"}
JSON
)
  R=$(gql "$Q"); echo "[create] resp: $(echo "$R" | head -c 300)"
  POD_ID=$(echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin);print((d.get('data',{}).get('podFindAndDeployOnDemand') or {}).get('id') or '')" 2>/dev/null)
  [ -n "$POD_ID" ] && { echo "[create] pod $POD_ID on $GPU"; echo "$POD_ID" > "$PODID_FILE"; break; }
  sleep 4
done
[ -z "$POD_ID" ] && { echo "FATAL: no pod from GPU cascade"; exit 1; }

# SSH-readiness loop
IP=""; PORT=""; SSH=""; SCP=""
for i in $(seq 1 $SSH_TRIES); do
  PR=$(gql "{\"query\":\"query { pod(input:{podId:\\\"$POD_ID\\\"}) { runtime { ports { ip publicPort privatePort isIpPublic } } } }\"}")
  read -r IP PORT < <(echo "$PR" | python3 -c "
import sys,json
d=json.load(sys.stdin)
rt=((d.get('data',{}).get('pod') or {}).get('runtime') or {}) or {}
for p in (rt.get('ports') or []):
    if p.get('privatePort')==22 and p.get('isIpPublic') and p.get('ip') and p.get('publicPort'):
        print(p['ip'], p['publicPort']); break
" 2>/dev/null)
  if [ -n "$IP" ] && [ -n "$PORT" ]; then
    SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8 -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -p $PORT root@$IP"
    if $SSH 'echo SSH_UP' 2>/dev/null | grep -q SSH_UP; then
      SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8 -P $PORT"
      echo "[ssh-ready] iter $i: $IP:$PORT - port mapped AND handshake OK"
      break
    fi
    [ $((i % 6)) -eq 0 ] && echo "[ssh-wait] iter $i: $IP:$PORT mapped, sshd not accepting yet"
  fi
  SSH=""; sleep 10
done
[ -z "$SSH" ] && { echo "FATAL: SSH never ready"; echo "SSH_NEVER_READY pod=$POD_ID" > "$FAIL_MARKER"; exit 1; }

# stage repo layout
P21GR=/workspace/p21gr
BUILD_REL=state/corpus_s101_build_s102_2026_05_19
S16_REL=state/carving_dataregime_s16_2026_05_18
ANCHOR_REL=HEXAD/UNIVERSE-BRAIN-MAP/anchors
$SSH "mkdir -p $P21GR/$BUILD_REL $P21GR/$S16_REL $P21GR/$ANCHOR_REL $P21GR/out_main $P21GR/vp21_adapter"
$SCP "$BUILD_DIR/build_corpus_s101.py"          "root@$IP:$P21GR/$BUILD_REL/"
$SCP "$S16_DIR/corpus_carving_s16_generator.py" "root@$IP:$P21GR/$S16_REL/"
$SCP "$ANCHOR_DIR"/knuth_*.kosmos               "root@$IP:$P21GR/$ANCHOR_REL/"
$SCP "$S187_DIR/build_diverse_corpus_p21g.py"    "root@$IP:$P21GR/"
$SCP "$S187_DIR/train_p21g_diverse.py"           "root@$IP:$P21GR/"
$SCP "$S187_DIR/launch_trainer_p21.sh"           "root@$IP:$P21GR/launch_trainer_p21g.sh"
$SSH "chmod +x $P21GR/launch_trainer_p21g.sh"

# Upload vP21 adapter
echo "[upload] vP21 LoRA adapter → pod"
$SCP -r "$VP21_ADAPTER_DIR"/* "root@$IP:$P21GR/vp21_adapter/"
ADAPTER_FILES=$($SSH "ls $P21GR/vp21_adapter/ | wc -l")
echo "[upload] adapter files on pod: $ADAPTER_FILES"

# Build anima corpus (corpus_s101)
echo "[corpus-anima] building corpus_s101 (seed 1337 n=777000)"
$SSH "python3 $P21GR/$BUILD_REL/build_corpus_s101.py --out-dir $P21GR/$BUILD_REL --s1-n 777000 --seed 1337 2>&1 | tail -8"
ANIMA_POD="$P21GR/$BUILD_REL/corpus_s101.jsonl"
ANIMA_SHA=$($SSH "sha256sum $ANIMA_POD 2>/dev/null | cut -d' ' -f1")
ANIMA_SIZE=$($SSH "stat -c %s $ANIMA_POD 2>/dev/null || echo 0")
echo "[corpus-anima] sha=$ANIMA_SHA size=$ANIMA_SIZE bytes"
if [ -z "$ANIMA_SHA" ] || [ "$ANIMA_SIZE" -lt 1048576 ]; then
  echo "FATAL: corpus_s101 too small or missing (size=$ANIMA_SIZE)"
  echo "ANIMA_CORPUS_BUILD_FAILED" > "$FAIL_MARKER"
  exit 1
fi

# Build wikitext corpus (~60 MB target so 70/30 mix can pull ~56 wiki + 24 anima → 80 MB)
# Use diverse-corpus builder with multi-source fallback for HfUriError robustness.
echo "[corpus-wiki] building diverse-EN corpus (target ~60 MB)"
WIKI_POD="$P21GR/diverse_corpus.jsonl"
$SSH "pip install -q -U datasets huggingface_hub 2>&1 | tail -3"
$SSH "python3 $P21GR/build_diverse_corpus_p21g.py --out $WIKI_POD --target-mb 60 2>&1 | tail -10"
WIKI_SHA=$($SSH "sha256sum $WIKI_POD 2>/dev/null | cut -d' ' -f1")
WIKI_SIZE=$($SSH "stat -c %s $WIKI_POD 2>/dev/null || echo 0")
echo "[corpus-wiki] sha=$WIKI_SHA size=$WIKI_SIZE bytes"
if [ -z "$WIKI_SHA" ] || [ "$WIKI_SIZE" -lt 1048576 ]; then
  echo "FATAL: diverse corpus too small or missing (size=$WIKI_SIZE)"
  echo "DIVERSE_CORPUS_BUILD_FAILED" > "$FAIL_MARKER"
  exit 1
fi

$SSH 'nvidia-smi --query-gpu=name,memory.total --format=csv,noheader' 2>&1 | head -3

# launch trainer
MIXED_POD="$P21GR/mixed_corpus.jsonl"
CMD="bash $P21GR/launch_trainer_p21g.sh $P21GR/train_p21g_diverse.py \
  --wiki-corpus $WIKI_POD --anima-corpus $ANIMA_POD --mixed-corpus $MIXED_POD \
  --vp21-adapter-dir $P21GR/vp21_adapter \
  --out-dir $P21GR/out_main \
  --base-model Qwen/Qwen2.5-1.5B \
  --steps $P21G_STEPS --bsz $P21G_BSZ --block $P21G_BLOCK --lr $P21G_LR \
  --warmup-steps $P21G_WARMUP --seed $SEED \
  --wiki-frac $P21G_WIKI_FRAC --target-corpus-mb $P21G_CORPUS_MB"

echo "[train] P21G launch"
$SSH "cd $P21GR && nohup $CMD > $P21GR/train.log 2>&1 & echo TRAIN_PID \$!"

sleep 20
ENV_CHECK=$($SSH "grep -m1 -E '^\\[launch\\] PYTORCH_CUDA_ALLOC_CONF=' $P21GR/train.log 2>/dev/null || echo NO_STAMP")
echo "[env-verify] $ENV_CHECK"
if ! echo "$ENV_CHECK" | grep -q "PYTORCH_CUDA_ALLOC_CONF"; then
  echo "[env-verify] FAIL — dumping log:"
  $SSH "head -80 $P21GR/train.log 2>/dev/null"
  echo "ENV_PASSTHROUGH_FAILED" > "$FAIL_MARKER"
  exit 1
fi

# poll train completion
RESULT_POD="$P21GR/out_main/result.json"
TRAIN_PROC_FRAGMENT="train_p21g_diverse.py"
MAX_ITERS=$((WATCHDOG_SEC / 60 - 2))
for i in $(seq 1 $MAX_ITERS); do
  $SSH "test -f $RESULT_POD && echo TRAIN_DONE" 2>/dev/null | grep -q TRAIN_DONE && { echo "[train] done iter $i"; break; }
  ALIVE=$($SSH "pgrep -f $TRAIN_PROC_FRAGMENT >/dev/null 2>&1 && echo ALIVE || echo DEAD" 2>/dev/null)
  if [ "$ALIVE" = "DEAD" ]; then
    echo "FATAL: trainer process died before result (iter $i)"
    $SSH "tail -100 $P21GR/train.log" 2>/dev/null
    echo "TRAIN_CRASHED" > "$FAIL_MARKER"; exit 1
  fi
  if [ $((i % 2)) -eq 0 ]; then
    $SSH "tail -2 $P21GR/train.log" 2>/dev/null | sed "s/^/[train-P21G] /"
  fi
  sleep 60
done

$SSH "test -s $RESULT_POD && echo RESULT_DONE" 2>/dev/null | grep -q RESULT_DONE || {
  echo "FATAL: result.json never produced"; $SSH "tail -80 $P21GR/train.log" 2>/dev/null
  echo "TRAIN_NO_RESULT" > "$FAIL_MARKER"; exit 1; }

# SAVE_POD auto-promote + pull
SAVE_POD=1
for k in 1 2 3 4 5; do
  $SCP "root@$IP:$RESULT_POD"                        "$VDIR/result.json" && \
  $SCP "root@$IP:$P21GR/out_main/heldout_vp21g.json" "$VDIR/heldout_vp21g.json" && \
  $SCP "root@$IP:$P21GR/out_main/vp21g_eval1.json"   "$VDIR/vp21g_eval1.json" && \
  $SCP "root@$IP:$P21GR/out_main/mix_info.json"      "$VDIR/mix_info.json" && \
  $SCP "root@$IP:$P21GR/train.log"                   "$VDIR/train.log" && \
  $SCP -r "root@$IP:$P21GR/out_main/lora_adapter"    "$VDIR/" && \
  { echo "[pull] success try $k"; break; }
  echo "[pull] retry $k failed; sleep 30"; sleep 30
done
if [ -s "$VDIR/result.json" ]; then
  SAVE_POD=0
  echo "[pull] result.json present - SAVE_POD=0, pod will terminate"
  python3 -c "
import json
d=json.load(open('$VDIR/result.json'))
fl=d.get('final_log') or {}
print('VERDICT=', d.get('verdict'))
print('  OOD generalize=', d.get('n_ood_generalize_total'), '/20  memorize=', d.get('n_ood_memorize_total'), '/20')
print('  anima_register_hits=', d.get('n_anima_register_hits_total'), '/20')
print('  register_regress=', d.get('register_regress'))
print('  init_CE=', d.get('init_log',{}).get('L_ce'), 'final_CE=', fl.get('L_ce'))
print('  train_wall_s=', round(d.get('train_wall_s',0),1))
" 2>/dev/null || true
else
  SAVE_POD=1
  echo "[pull] FAILED 5x - SAVE_POD=1 retain pod $POD_ID"
  echo "PULL_FAILED pod=$POD_ID ssh=$IP:$PORT" > "$FAIL_MARKER"
fi
kill "$WATCHDOG_PID" 2>/dev/null
echo "=== P21G pipeline complete $(date -u +%FT%TZ) ==="
