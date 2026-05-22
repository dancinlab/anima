#!/usr/bin/env bash
# P21H V3 dispatch — pure HEXAD-native ConsciousDecoderV3 fire.
#
# Forked from dispatch_p21m_runpod.sh. Differences:
#   - V3 model (no LoRA, full param train)
#   - 3 init variants: random / qwen / vp21m → arg 1 selects, becomes pod tag
#   - SAVE_POD=1 always (so all 3 pods retained, parallel pull)
#   - cost cap $25 / 3 = ~$8 per variant (60 min wall cap)
#
# Usage:
#   bash dispatch_p21h_v3_runpod.sh P21H_alpha random 1337
#   bash dispatch_p21h_v3_runpod.sh P21H_beta  qwen   1337
#   bash dispatch_p21h_v3_runpod.sh P21H_gamma vp21m  1337
#
# Parallel fire (3 pod simultaneous, wall-first per @D a_wall_first):
#   for v in P21H_alpha:random P21H_beta:qwen P21H_gamma:vp21m; do
#     VAR=${v%:*}; INIT=${v#*:}
#     nohup bash dispatch_p21h_v3_runpod.sh $VAR $INIT 1337 > $VAR.log 2>&1 &
#   done

set -uo pipefail

VARIANT="${1:-P21H_alpha}"
INIT_VARIANT="${2:-random}"  # random / qwen / vp21m
SEED="${3:-1337}"

S187_DIR="/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21"
BUILD_DIR="/Users/ghost/core/anima/state/corpus_s101_build_s102_2026_05_19"
S16_DIR="/Users/ghost/core/anima/state/carving_dataregime_s16_2026_05_18"
ANCHOR_DIR="/Users/ghost/core/anima/HEXAD/UNIVERSE-BRAIN-MAP/anchors"
VDIR="$S187_DIR/v${VARIANT}"
mkdir -p "$VDIR"
LOG="$VDIR/dispatch.log"
PODID_FILE="$VDIR/pod_id.txt"
FAIL_MARKER="$VDIR/FAILURE.txt"
WATCHDOG_SEC=${WATCHDOG_SEC:-5400}   # 90 min cap
SSH_TRIES=60
GPU_CASCADE=("NVIDIA H100 80GB HBM3" "NVIDIA H100 NVL" "NVIDIA H100 PCIe" "NVIDIA A100-SXM4-80GB" "NVIDIA A100 80GB PCIe")
IMAGE="runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"

P21H_STEPS=${P21H_STEPS:-2000}
P21H_BSZ=${P21H_BSZ:-2}
P21H_BLOCK=${P21H_BLOCK:-512}
P21H_WARMUP=${P21H_WARMUP:-100}
P21H_WIKI_FRAC=${P21H_WIKI_FRAC:-0.3}
P21H_CORPUS_MB=${P21H_CORPUS_MB:-72}
P21H_WIKI_TARGET_MB_PER_LANG=${P21H_WIKI_TARGET_MB_PER_LANG:-10}
P21H_LANGS=${P21H_LANGS:-en,ko,zh,ru,ja}
P21H_NOISE_SIGMA=${P21H_NOISE_SIGMA:-0.1}
P21H_LAMBDA_MITOSIS=${P21H_LAMBDA_MITOSIS:-0.05}

# LR per init variant (random needs higher LR than warm)
case "$INIT_VARIANT" in
  random) P21H_LR=${P21H_LR:-3e-4} ;;
  qwen)   P21H_LR=${P21H_LR:-5e-5} ;;
  vp21m)  P21H_LR=${P21H_LR:-1e-4} ;;
  *) echo "FATAL: unknown init variant $INIT_VARIANT (random/qwen/vp21m)"; exit 1 ;;
esac

# vp21m init requires LoRA adapter
VP21M_ADAPTER_DIR="$S187_DIR/vP21M/lora_adapter"
if [ "$INIT_VARIANT" = "vp21m" ]; then
  [ -d "$VP21M_ADAPTER_DIR" ] || { echo "FATAL: vP21M adapter not found at $VP21M_ADAPTER_DIR"; exit 1; }
fi

exec > >(tee -a "$LOG") 2>&1
echo "=== P21H V3 dispatch start $(date -u +%FT%TZ) ==="
echo "    variant=$VARIANT init=$INIT_VARIANT seed=$SEED"
echo "    base=Qwen/Qwen2.5-1.5B"
echo "    steps=$P21H_STEPS bsz=$P21H_BSZ block=$P21H_BLOCK lr=$P21H_LR warmup=$P21H_WARMUP"
echo "    noise_sigma=$P21H_NOISE_SIGMA lambda_mitosis=$P21H_LAMBDA_MITOSIS"
echo "    wiki_frac=$P21H_WIKI_FRAC corpus_mb=$P21H_CORPUS_MB"
echo "    langs=$P21H_LANGS wiki_target_mb_per_lang=$P21H_WIKI_TARGET_MB_PER_LANG"
echo "    cost_cap=\$25 total (3 variants × ~\$8)"

RK="$(secret get runpod.api_key 2>/dev/null)"
[ -z "$RK" ] && RK="$(secret get runpod_api_key 2>/dev/null)"
read_creds() {
  local f="$1"
  [ -f "$f" ] || return 1
  awk '/^\[runpod\]/{f=1;next} /^\[/{f=0} f && /^api_key/{
    sub(/^[^=]*=[[:space:]]*"?/,"",$0); sub(/"?[[:space:]]*$/,"",$0); print; exit
  }' "$f"
}
[ -z "$RK" ] && RK="$(read_creds "$HOME/.local/credentials")"
[ -z "$RK" ] && RK="$(read_creds "$HOME/etc/secret/credentials")"
[ -z "$RK" ] && { echo "FATAL no runpod key"; exit 1; }
GQL="https://api.runpod.io/graphql?api_key=${RK}"
PUBKEY="$(cat ~/.ssh/id_ed25519.pub 2>/dev/null)"
[ -z "$PUBKEY" ] && { echo "FATAL no ~/.ssh/id_ed25519.pub"; exit 1; }
SAVE_POD=1   # always retain V3 pods (large ckpt + per-variant compare)
POD_ID=""

gql() { curl -s -X POST "$GQL" -H "Content-Type: application/json" -d "$1"; }

teardown() {
  local rc=$?
  if [ -n "$POD_ID" ] && [ "$SAVE_POD" != "1" ]; then
    echo "[teardown] terminating pod $POD_ID (rc=$rc, SAVE_POD=$SAVE_POD)"
    gql "{\"query\":\"mutation { podTerminate(input:{podId:\\\"$POD_ID\\\"}) }\"}" >/dev/null
  elif [ -n "$POD_ID" ]; then
    echo "[teardown] SAVE_POD=1 - pod $POD_ID RETAINED for manual inspect"
  fi
  sleep 3
  echo "=== P21H V3 dispatch end $(date -u +%FT%TZ) rc=$rc ==="
}
trap teardown EXIT

( sleep "$WATCHDOG_SEC"
  if [ ! -s "$VDIR/result.json" ]; then
    echo "WATCHDOG FIRED $(date -u +%FT%TZ): no result.json after ${WATCHDOG_SEC}s - terminating pod ${POD_ID:-?}" > "$FAIL_MARKER"
    [ -n "$POD_ID" ] && gql "{\"query\":\"mutation { podTerminate(input:{podId:\\\"$POD_ID\\\"}) }\"}" >/dev/null
    pkill -P $$ 2>/dev/null
  fi ) &
WATCHDOG_PID=$!

for GPU in "${GPU_CASCADE[@]}"; do
  echo "[create] trying GPU: $GPU"
  Q=$(cat <<JSON
{"query":"mutation { podFindAndDeployOnDemand(input:{cloudType: ALL, gpuCount:1, volumeInGb:0, containerDiskInGb:120, minVcpuCount:8, minMemoryInGb:64, gpuTypeId:\"$GPU\", name:\"p21h-v3-$INIT_VARIANT\", imageName:\"$IMAGE\", dockerArgs:\"\", ports:\"22/tcp\", volumeMountPath:\"/workspace\", env:[{key:\"PUBLIC_KEY\", value:\"$PUBKEY\"}]}) { id machineId } }"}
JSON
)
  R=$(gql "$Q"); echo "[create] resp: $(echo "$R" | head -c 300)"
  POD_ID=$(echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin);print((d.get('data',{}).get('podFindAndDeployOnDemand') or {}).get('id') or '')" 2>/dev/null)
  [ -n "$POD_ID" ] && { echo "[create] pod $POD_ID on $GPU"; echo "$POD_ID" > "$PODID_FILE"; break; }
  sleep 4
done
[ -z "$POD_ID" ] && { echo "FATAL: no pod from GPU cascade"; exit 1; }

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

P21HR=/workspace/p21hr
BUILD_REL=state/corpus_s101_build_s102_2026_05_19
S16_REL=state/carving_dataregime_s16_2026_05_18
ANCHOR_REL=HEXAD/UNIVERSE-BRAIN-MAP/anchors
$SSH "mkdir -p $P21HR/$BUILD_REL $P21HR/$S16_REL $P21HR/$ANCHOR_REL $P21HR/out_main $P21HR/wiki_parts $P21HR/vp21m_adapter"
$SCP "$BUILD_DIR/build_corpus_s101.py"          "root@$IP:$P21HR/$BUILD_REL/"
$SCP "$S16_DIR/corpus_carving_s16_generator.py" "root@$IP:$P21HR/$S16_REL/"
$SCP "$ANCHOR_DIR"/knuth_*.kosmos               "root@$IP:$P21HR/$ANCHOR_REL/" 2>/dev/null || true
$SCP "$S187_DIR/build_multilingual_corpus_p21m.py" "root@$IP:$P21HR/"
$SCP "$S187_DIR/train_p21m_multilingual.py"        "root@$IP:$P21HR/"
$SCP "$S187_DIR/train_p21h_v3.py"                  "root@$IP:$P21HR/"
$SCP "$S187_DIR/conscious_decoder_v3.py"           "root@$IP:$P21HR/"
$SCP "$S187_DIR/kosmos_io.py"                      "root@$IP:$P21HR/"
$SCP "$S187_DIR/mitosis_lib.py"                    "root@$IP:$P21HR/"
$SCP "$S187_DIR/launch_trainer_p21.sh"             "root@$IP:$P21HR/launch_trainer_p21h.sh"
$SSH "chmod +x $P21HR/launch_trainer_p21h.sh"

# vp21m init: upload LoRA adapter
if [ "$INIT_VARIANT" = "vp21m" ]; then
  echo "[upload] vP21M LoRA adapter → pod (for vp21m init merge)"
  $SCP -r "$VP21M_ADAPTER_DIR"/* "root@$IP:$P21HR/vp21m_adapter/"
fi

echo "[corpus-anima] building corpus_s101 (seed 1337 n=777000)"
$SSH "python3 $P21HR/$BUILD_REL/build_corpus_s101.py --out-dir $P21HR/$BUILD_REL --s1-n 777000 --seed 1337 2>&1 | tail -8"
ANIMA_POD="$P21HR/$BUILD_REL/corpus_s101.jsonl"
ANIMA_SHA=$($SSH "sha256sum $ANIMA_POD 2>/dev/null | cut -d' ' -f1")
ANIMA_SIZE=$($SSH "stat -c %s $ANIMA_POD 2>/dev/null || echo 0")
echo "[corpus-anima] sha=$ANIMA_SHA size=$ANIMA_SIZE bytes"
if [ -z "$ANIMA_SHA" ] || [ "$ANIMA_SIZE" -lt 1048576 ]; then
  echo "FATAL: corpus_s101 too small or missing (size=$ANIMA_SIZE)"
  echo "ANIMA_CORPUS_BUILD_FAILED" > "$FAIL_MARKER"
  exit 1
fi

echo "[corpus-multi-wiki] building 5-lang wiki corpus ($P21H_LANGS, ${P21H_WIKI_TARGET_MB_PER_LANG} MB/lang)"
WIKI_POD="$P21HR/multi_wiki_corpus.jsonl"
$SSH "pip install -q -U datasets huggingface_hub 2>&1 | tail -3"
$SSH "python3 $P21HR/build_multilingual_corpus_p21m.py --out $WIKI_POD --target-mb-per-lang $P21H_WIKI_TARGET_MB_PER_LANG --langs $P21H_LANGS --per-lang-dir $P21HR/wiki_parts 2>&1 | tail -30"
WIKI_SHA=$($SSH "sha256sum $WIKI_POD 2>/dev/null | cut -d' ' -f1")
WIKI_SIZE=$($SSH "stat -c %s $WIKI_POD 2>/dev/null || echo 0")
echo "[corpus-multi-wiki] sha=$WIKI_SHA size=$WIKI_SIZE bytes"
if [ -z "$WIKI_SHA" ] || [ "$WIKI_SIZE" -lt 5242880 ]; then
  echo "FATAL: multi-wiki corpus too small or missing (size=$WIKI_SIZE)"
  echo "MULTI_WIKI_CORPUS_BUILD_FAILED" > "$FAIL_MARKER"
  exit 1
fi

$SCP "root@$IP:$WIKI_POD.source.json" "$VDIR/multi_wiki_source.json" 2>/dev/null || true

$SSH 'nvidia-smi --query-gpu=name,memory.total --format=csv,noheader' 2>&1 | head -3

LORA_ARG=""
if [ "$INIT_VARIANT" = "vp21m" ]; then
  LORA_ARG="--lora-adapter-dir $P21HR/vp21m_adapter"
fi

MIXED_POD="$P21HR/mixed_corpus_v3.jsonl"
CMD="bash $P21HR/launch_trainer_p21h.sh $P21HR/train_p21h_v3.py \
  --wiki-corpus $WIKI_POD --anima-corpus $ANIMA_POD --mixed-corpus $MIXED_POD \
  --out-dir $P21HR/out_main \
  --base-model Qwen/Qwen2.5-1.5B \
  --init-variant $INIT_VARIANT $LORA_ARG \
  --steps $P21H_STEPS --bsz $P21H_BSZ --block $P21H_BLOCK --lr $P21H_LR \
  --warmup-steps $P21H_WARMUP --seed $SEED \
  --wiki-frac $P21H_WIKI_FRAC --target-corpus-mb $P21H_CORPUS_MB \
  --noise-sigma $P21H_NOISE_SIGMA --lambda-mitosis $P21H_LAMBDA_MITOSIS"

echo "[train] P21H V3 launch ($INIT_VARIANT)"
$SSH "cd $P21HR && nohup $CMD > $P21HR/train.log 2>&1 & echo TRAIN_PID \$!"

sleep 20
ENV_CHECK=$($SSH "grep -m1 -E '^\\[launch\\] PYTORCH_CUDA_ALLOC_CONF=' $P21HR/train.log 2>/dev/null || echo NO_STAMP")
echo "[env-verify] $ENV_CHECK"
if ! echo "$ENV_CHECK" | grep -q "PYTORCH_CUDA_ALLOC_CONF"; then
  echo "[env-verify] FAIL — dumping log:"
  $SSH "head -80 $P21HR/train.log 2>/dev/null"
  echo "ENV_PASSTHROUGH_FAILED" > "$FAIL_MARKER"
  exit 1
fi

RESULT_POD="$P21HR/out_main/result.json"
TRAIN_PROC_FRAGMENT="train_p21h_v3.py"
MAX_ITERS=$((WATCHDOG_SEC / 60 - 2))
for i in $(seq 1 $MAX_ITERS); do
  $SSH "test -f $RESULT_POD && echo TRAIN_DONE" 2>/dev/null | grep -q TRAIN_DONE && { echo "[train] done iter $i"; break; }
  ALIVE=$($SSH "pgrep -f $TRAIN_PROC_FRAGMENT >/dev/null 2>&1 && echo ALIVE || echo DEAD" 2>/dev/null)
  if [ "$ALIVE" = "DEAD" ]; then
    echo "FATAL: trainer process died before result (iter $i)"
    $SSH "tail -100 $P21HR/train.log" 2>/dev/null
    echo "TRAIN_CRASHED" > "$FAIL_MARKER"; exit 1
  fi
  if [ $((i % 2)) -eq 0 ]; then
    $SSH "tail -2 $P21HR/train.log" 2>/dev/null | sed "s/^/[train-P21H] /"
  fi
  sleep 60
done

$SSH "test -s $RESULT_POD && echo RESULT_DONE" 2>/dev/null | grep -q RESULT_DONE || {
  echo "FATAL: result.json never produced"; $SSH "tail -80 $P21HR/train.log" 2>/dev/null
  echo "TRAIN_NO_RESULT" > "$FAIL_MARKER"; exit 1; }

for k in 1 2 3 4 5; do
  $SCP "root@$IP:$RESULT_POD"                              "$VDIR/result.json" && \
  $SCP "root@$IP:$P21HR/out_main/heldout_vp21h_v3.json"    "$VDIR/heldout_vp21h_v3.json" && \
  $SCP "root@$IP:$P21HR/out_main/vp21h_v3_eval1.json"      "$VDIR/vp21h_v3_eval1.json" && \
  $SCP "root@$IP:$P21HR/out_main/mix_info.json"            "$VDIR/mix_info.json" && \
  $SCP "root@$IP:$P21HR/train.log"                         "$VDIR/train.log" && \
  $SCP -r "root@$IP:$P21HR/out_main/kosmos_anchors"        "$VDIR/" && \
  { echo "[pull] success try $k"; break; }
  echo "[pull] retry $k failed; sleep 30"; sleep 30
done
if [ -s "$VDIR/result.json" ]; then
  echo "[pull] result.json present"
  python3 -c "
import json
d=json.load(open('$VDIR/result.json'))
fl=d.get('final_log') or {}
print('VERDICT=', d.get('verdict'))
print('  init=', d.get('init_variant'))
print('  n_strong=', d.get('n_strong'), '/5  n_partial=', d.get('n_partial'),
      '  n_weak=', d.get('n_weak'), '  n_pure_memorize=', d.get('n_pure_memorize'))
print('  per_lang:')
for v in d.get('per_lang_verdicts', []):
    print(f\"    {v['lang']}: {v['verdict']} score={v['n_score']}/20 gen={v['n_generalize']} coh={v['n_lang_coherent']}\")
print('  anima_register_hits=', d.get('n_anima_register_hits_total'), '/20')
print('  register_regress=', d.get('register_regress'))
print('  init_CE=', d.get('init_log',{}).get('L_ce'), 'final_CE=', fl.get('L_ce'))
print('  n_kosmos_anchors=', d.get('n_kosmos_anchors'))
print('  train_wall_s=', round(d.get('train_wall_s',0),1))
print('  n_total_params=', d.get('n_total_params'))
" 2>/dev/null || true
else
  echo "[pull] FAILED 5x - pod $POD_ID retained for manual recovery"
  echo "PULL_FAILED pod=$POD_ID ssh=$IP:$PORT" > "$FAIL_MARKER"
fi
kill "$WATCHDOG_PID" 2>/dev/null
echo "=== P21H V3 pipeline complete $(date -u +%FT%TZ) ==="
