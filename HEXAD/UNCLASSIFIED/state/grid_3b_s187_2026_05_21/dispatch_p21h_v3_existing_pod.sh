#!/usr/bin/env bash
# P21H V3 dispatch — REUSE existing pod (skip pod creation). For when
# pod creation is rate-limited but pods are already alive (saga 2026-05-22).
#
# Usage:
#   bash dispatch_p21h_v3_existing_pod.sh VARIANT INIT POD_ID SEED
#   bash dispatch_p21h_v3_existing_pod.sh P21H_alpha random m7bezjoahsbh26 1337

set -uo pipefail

VARIANT="${1:?need VARIANT (P21H_alpha/beta/gamma)}"
INIT_VARIANT="${2:?need INIT (random/qwen/vp21m)}"
POD_ID="${3:?need POD_ID}"
SEED="${4:-1337}"

S187_DIR="/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21"
BUILD_DIR="/Users/ghost/core/anima/state/corpus_s101_build_s102_2026_05_19"
S16_DIR="/Users/ghost/core/anima/state/carving_dataregime_s16_2026_05_18"
ANCHOR_DIR="/Users/ghost/core/anima/HEXAD/UNIVERSE-BRAIN-MAP/anchors"
VDIR="$S187_DIR/v${VARIANT}"
mkdir -p "$VDIR"
LOG="$VDIR/dispatch.log"
PODID_FILE="$VDIR/pod_id.txt"
FAIL_MARKER="$VDIR/FAILURE.txt"
WATCHDOG_SEC=${WATCHDOG_SEC:-5400}

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

case "$INIT_VARIANT" in
  random) P21H_LR=${P21H_LR:-3e-4} ;;
  qwen)   P21H_LR=${P21H_LR:-5e-5} ;;
  vp21m)  P21H_LR=${P21H_LR:-1e-4} ;;
  *) echo "FATAL: bad init $INIT_VARIANT"; exit 1 ;;
esac

VP21M_ADAPTER_DIR="$S187_DIR/vP21M/lora_adapter"
if [ "$INIT_VARIANT" = "vp21m" ]; then
  [ -d "$VP21M_ADAPTER_DIR" ] || { echo "FATAL: vP21M adapter missing"; exit 1; }
fi

echo "$POD_ID" > "$PODID_FILE"

exec > >(tee -a "$LOG") 2>&1
echo "=== P21H V3 dispatch (REUSE pod) $(date -u +%FT%TZ) ==="
echo "    variant=$VARIANT init=$INIT_VARIANT pod=$POD_ID seed=$SEED lr=$P21H_LR"

RK="$(secret get runpod.api_key 2>/dev/null)"
read_creds() {
  local f="$1"; [ -f "$f" ] || return 1
  awk '/^\[runpod\]/{f=1;next} /^\[/{f=0} f && /^api_key/{
    sub(/^[^=]*=[[:space:]]*"?/,"",$0); sub(/"?[[:space:]]*$/,"",$0); print; exit
  }' "$f"
}
[ -z "$RK" ] && RK="$(read_creds "$HOME/.local/credentials")"
[ -z "$RK" ] && RK="$(read_creds "$HOME/etc/secret/credentials")"
[ -z "$RK" ] && { echo "FATAL no runpod key"; exit 1; }
GQL="https://api.runpod.io/graphql?api_key=${RK}"
gql() { curl -s -X POST "$GQL" -H "Content-Type: application/json" -d "$1"; }

# SAVE_POD=1 always (do NOT auto-terminate)
SAVE_POD=1
teardown() {
  local rc=$?
  echo "[teardown] SAVE_POD=1 - pod $POD_ID RETAINED"
  echo "=== P21H V3 (reuse) end $(date -u +%FT%TZ) rc=$rc ==="
}
trap teardown EXIT

# Watchdog
( sleep "$WATCHDOG_SEC"
  if [ ! -s "$VDIR/result.json" ]; then
    echo "WATCHDOG FIRED $(date -u +%FT%TZ): no result.json after ${WATCHDOG_SEC}s" > "$FAIL_MARKER"
    pkill -P $$ 2>/dev/null
  fi ) &
WATCHDOG_PID=$!

# Resolve SSH
IP=""; PORT=""; SSH=""; SCP=""
for i in $(seq 1 60); do
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
      echo "[ssh-ready] iter $i: $IP:$PORT"
      break
    fi
    [ $((i % 6)) -eq 0 ] && echo "[ssh-wait] iter $i: $IP:$PORT mapped, sshd booting"
  fi
  SSH=""; sleep 10
done
[ -z "$SSH" ] && { echo "FATAL: SSH never ready"; echo "SSH_NEVER_READY" > "$FAIL_MARKER"; exit 1; }

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

if [ "$INIT_VARIANT" = "vp21m" ]; then
  echo "[upload] vP21M LoRA adapter"
  $SCP -r "$VP21M_ADAPTER_DIR"/* "root@$IP:$P21HR/vp21m_adapter/"
fi

echo "[corpus-anima] building"
$SSH "python3 $P21HR/$BUILD_REL/build_corpus_s101.py --out-dir $P21HR/$BUILD_REL --s1-n 777000 --seed 1337 2>&1 | tail -8"
ANIMA_POD="$P21HR/$BUILD_REL/corpus_s101.jsonl"
ANIMA_SIZE=$($SSH "stat -c %s $ANIMA_POD 2>/dev/null || echo 0")
[ "$ANIMA_SIZE" -lt 1048576 ] && { echo "FATAL: corpus_s101 fail size=$ANIMA_SIZE"; echo "ANIMA_CORPUS_FAIL" > "$FAIL_MARKER"; exit 1; }
echo "[corpus-anima] size=$ANIMA_SIZE"

echo "[corpus-multi-wiki] building"
WIKI_POD="$P21HR/multi_wiki_corpus.jsonl"
$SSH "pip install -q -U datasets huggingface_hub 2>&1 | tail -3"
$SSH "python3 $P21HR/build_multilingual_corpus_p21m.py --out $WIKI_POD --target-mb-per-lang $P21H_WIKI_TARGET_MB_PER_LANG --langs $P21H_LANGS --per-lang-dir $P21HR/wiki_parts 2>&1 | tail -20"
WIKI_SIZE=$($SSH "stat -c %s $WIKI_POD 2>/dev/null || echo 0")
[ "$WIKI_SIZE" -lt 5242880 ] && { echo "FATAL: wiki size=$WIKI_SIZE"; echo "WIKI_FAIL" > "$FAIL_MARKER"; exit 1; }
echo "[corpus-multi-wiki] size=$WIKI_SIZE"
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

echo "[train] launch ($INIT_VARIANT)"
$SSH "cd $P21HR && nohup $CMD > $P21HR/train.log 2>&1 & echo TRAIN_PID \$!"

sleep 20
ENV_CHECK=$($SSH "grep -m1 'PYTORCH_CUDA_ALLOC_CONF' $P21HR/train.log 2>/dev/null || echo NO_STAMP")
echo "[env-verify] $ENV_CHECK"
echo "$ENV_CHECK" | grep -q PYTORCH_CUDA_ALLOC_CONF || {
  $SSH "head -80 $P21HR/train.log 2>/dev/null"
  echo "ENV_FAIL" > "$FAIL_MARKER"; exit 1
}

RESULT_POD="$P21HR/out_main/result.json"
MAX_ITERS=$((WATCHDOG_SEC / 60 - 2))
for i in $(seq 1 $MAX_ITERS); do
  $SSH "test -f $RESULT_POD && echo TRAIN_DONE" 2>/dev/null | grep -q TRAIN_DONE && { echo "[train] done iter $i"; break; }
  ALIVE=$($SSH "pgrep -f train_p21h_v3.py >/dev/null 2>&1 && echo ALIVE || echo DEAD" 2>/dev/null)
  if [ "$ALIVE" = "DEAD" ]; then
    echo "FATAL: trainer died (iter $i)"
    $SSH "tail -100 $P21HR/train.log" 2>/dev/null
    echo "TRAIN_CRASHED" > "$FAIL_MARKER"; exit 1
  fi
  if [ $((i % 2)) -eq 0 ]; then
    $SSH "tail -2 $P21HR/train.log" 2>/dev/null | sed "s/^/[train-$INIT_VARIANT] /"
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
  python3 -c "
import json
d=json.load(open('$VDIR/result.json'))
fl=d.get('final_log') or {}
print('VERDICT=', d.get('verdict'))
print('  init=', d.get('init_variant'))
print('  n_strong=', d.get('n_strong'), 'n_partial=', d.get('n_partial'))
print('  init_CE=', d.get('init_log',{}).get('L_ce'), 'final_CE=', fl.get('L_ce'))
" 2>/dev/null || true
else
  echo "PULL_FAILED pod=$POD_ID ssh=$IP:$PORT" > "$FAIL_MARKER"
fi
kill "$WATCHDOG_PID" 2>/dev/null
echo "=== P21H V3 (reuse) pipeline complete $(date -u +%FT%TZ) ==="
