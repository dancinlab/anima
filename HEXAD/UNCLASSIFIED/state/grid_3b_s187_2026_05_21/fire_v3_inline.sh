#!/bin/bash
# Inline V3 fire — direct ssh, no tee, no process-substitution. bash 3.2 safe.
#
# Usage: bash fire_v3_inline.sh <VARIANT> <INIT> <POD_ID> <IP> <PORT> <LR>
set -uo pipefail

VARIANT="${1:?}"
INIT="${2:?}"
POD_ID="${3:?}"
IP="${4:?}"
PORT="${5:?}"
LR="${6:?}"
SEED="${7:-1337}"

S187_DIR="/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21"
BUILD_DIR="/Users/ghost/core/anima/state/corpus_s101_build_s102_2026_05_19"
S16_DIR="/Users/ghost/core/anima/state/carving_dataregime_s16_2026_05_18"
ANCHOR_DIR="/Users/ghost/core/anima/HEXAD/UNIVERSE-BRAIN-MAP/anchors"
VDIR="$S187_DIR/v${VARIANT}"
mkdir -p "$VDIR"
LOG="$VDIR/dispatch.log"
echo "$POD_ID" > "$VDIR/pod_id.txt"

SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8 -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -p $PORT root@$IP"
SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8 -P $PORT"

log() { echo "[$(date -u +%H:%M:%S) $VARIANT] $*" | tee -a "$LOG"; }

log "=== fire V3 inline (variant=$VARIANT init=$INIT pod=$POD_ID lr=$LR) ==="

# 1. SSH up?
$SSH 'echo SSH_UP' 2>&1 | grep -q SSH_UP || { log "SSH not ready"; exit 1; }
log "SSH OK $IP:$PORT"

# 2. Upload code
P21HR=/workspace/p21hr
BUILD_REL=state/corpus_s101_build_s102_2026_05_19
S16_REL=state/carving_dataregime_s16_2026_05_18
ANCHOR_REL=HEXAD/UNIVERSE-BRAIN-MAP/anchors
$SSH "mkdir -p $P21HR/$BUILD_REL $P21HR/$S16_REL $P21HR/$ANCHOR_REL $P21HR/out_main $P21HR/wiki_parts $P21HR/vp21m_adapter" 2>&1 | head -3
log "dirs created"

$SCP "$BUILD_DIR/build_corpus_s101.py" "root@$IP:$P21HR/$BUILD_REL/" >/dev/null 2>&1
$SCP "$S16_DIR/corpus_carving_s16_generator.py" "root@$IP:$P21HR/$S16_REL/" >/dev/null 2>&1
$SCP "$ANCHOR_DIR"/knuth_*.kosmos "root@$IP:$P21HR/$ANCHOR_REL/" >/dev/null 2>&1 || true
$SCP "$S187_DIR/build_multilingual_corpus_p21m.py" "root@$IP:$P21HR/" >/dev/null 2>&1
$SCP "$S187_DIR/train_p21m_multilingual.py"        "root@$IP:$P21HR/" >/dev/null 2>&1
$SCP "$S187_DIR/train_p21h_v3.py"                  "root@$IP:$P21HR/" >/dev/null 2>&1
$SCP "$S187_DIR/conscious_decoder_v3.py"           "root@$IP:$P21HR/" >/dev/null 2>&1
$SCP "$S187_DIR/kosmos_io.py"                      "root@$IP:$P21HR/" >/dev/null 2>&1
$SCP "$S187_DIR/mitosis_lib.py"                    "root@$IP:$P21HR/" >/dev/null 2>&1
$SCP "$S187_DIR/launch_trainer_p21.sh"             "root@$IP:$P21HR/launch_trainer_p21h.sh" >/dev/null 2>&1
$SSH "chmod +x $P21HR/launch_trainer_p21h.sh" >/dev/null 2>&1
log "code uploaded"

if [ "$INIT" = "vp21m" ]; then
  log "uploading vP21M LoRA adapter (147 MB)..."
  $SCP -r "$S187_DIR/vP21M/lora_adapter"/* "root@$IP:$P21HR/vp21m_adapter/" >/dev/null 2>&1
  log "adapter uploaded"
fi

# 3. Build corpus
log "building anima corpus (~30s)..."
$SSH "python3 $P21HR/$BUILD_REL/build_corpus_s101.py --out-dir $P21HR/$BUILD_REL --s1-n 777000 --seed 1337 > /tmp/build_anima.log 2>&1; tail -5 /tmp/build_anima.log" 2>&1 | tail -3
ANIMA_SIZE=$($SSH "stat -c %s $P21HR/$BUILD_REL/corpus_s101.jsonl 2>/dev/null || echo 0")
log "anima corpus size=$ANIMA_SIZE"
[ "$ANIMA_SIZE" -lt 1048576 ] && { log "ANIMA_CORPUS_FAIL"; echo "anima fail" > "$VDIR/FAILURE.txt"; exit 1; }

log "installing datasets package + building 5-lang wiki (~60s)..."
$SSH "pip install -q -U datasets huggingface_hub 2>&1 | tail -3" 2>&1 | tail -3
$SSH "python3 $P21HR/build_multilingual_corpus_p21m.py --out $P21HR/multi_wiki_corpus.jsonl --target-mb-per-lang 10 --langs en,ko,zh,ru,ja --per-lang-dir $P21HR/wiki_parts > /tmp/build_wiki.log 2>&1; tail -5 /tmp/build_wiki.log" 2>&1 | tail -3
WIKI_SIZE=$($SSH "stat -c %s $P21HR/multi_wiki_corpus.jsonl 2>/dev/null || echo 0")
log "wiki size=$WIKI_SIZE"
[ "$WIKI_SIZE" -lt 5242880 ] && { log "WIKI_FAIL"; echo "wiki fail" > "$VDIR/FAILURE.txt"; exit 1; }

$SSH 'nvidia-smi --query-gpu=name,memory.total --format=csv,noheader' 2>&1 | head -2

# 4. Launch trainer
LORA_ARG=""
[ "$INIT" = "vp21m" ] && LORA_ARG="--lora-adapter-dir $P21HR/vp21m_adapter"

log "launching trainer (init=$INIT lr=$LR steps=2000)..."
$SSH "cd $P21HR && nohup bash launch_trainer_p21h.sh train_p21h_v3.py \
  --wiki-corpus $P21HR/multi_wiki_corpus.jsonl \
  --anima-corpus $P21HR/$BUILD_REL/corpus_s101.jsonl \
  --mixed-corpus $P21HR/mixed_corpus_v3.jsonl \
  --out-dir $P21HR/out_main \
  --base-model Qwen/Qwen2.5-1.5B \
  --init-variant $INIT $LORA_ARG \
  --steps 2000 --bsz 2 --block 512 --lr $LR \
  --warmup-steps 100 --seed $SEED \
  --wiki-frac 0.3 --target-corpus-mb 72 \
  --noise-sigma 0.1 --lambda-mitosis 0.05 \
  > $P21HR/train.log 2>&1 & echo TRAIN_PID \$!" 2>&1 | head -3
log "trainer launched. polling for completion..."

# 5. Poll
RESULT_POD="$P21HR/out_main/result.json"
for i in $(seq 1 90); do
  sleep 60
  DONE=$($SSH "test -f $RESULT_POD && echo YES || echo NO" 2>/dev/null)
  if [ "$DONE" = "YES" ]; then
    log "TRAIN DONE (iter $i = $((i)) min)"
    break
  fi
  ALIVE=$($SSH "pgrep -f train_p21h_v3.py >/dev/null && echo ALIVE || echo DEAD" 2>/dev/null)
  if [ "$ALIVE" = "DEAD" ]; then
    log "TRAINER DIED at iter $i"
    $SSH "tail -50 $P21HR/train.log" 2>&1 | tee -a "$LOG" | tail -20
    echo "trainer died" > "$VDIR/FAILURE.txt"
    exit 1
  fi
  if [ $((i % 3)) -eq 0 ]; then
    TAIL=$($SSH "tail -1 $P21HR/train.log 2>/dev/null" 2>/dev/null)
    log "iter $i: $TAIL"
  fi
done

# 6. Pull
$SCP "root@$IP:$RESULT_POD" "$VDIR/result.json" >/dev/null 2>&1
$SCP "root@$IP:$P21HR/out_main/heldout_vp21h_v3.json" "$VDIR/heldout_vp21h_v3.json" >/dev/null 2>&1
$SCP "root@$IP:$P21HR/out_main/vp21h_v3_eval1.json" "$VDIR/vp21h_v3_eval1.json" >/dev/null 2>&1
$SCP "root@$IP:$P21HR/out_main/mix_info.json" "$VDIR/mix_info.json" >/dev/null 2>&1
$SCP "root@$IP:$P21HR/train.log" "$VDIR/train.log" >/dev/null 2>&1
$SCP -r "root@$IP:$P21HR/out_main/kosmos_anchors" "$VDIR/" >/dev/null 2>&1 || true

if [ -s "$VDIR/result.json" ]; then
  log "result.json pulled"
  python3 -c "
import json
d=json.load(open('$VDIR/result.json'))
fl=d.get('final_log') or {}
print('VERDICT=', d.get('verdict'))
print('  init=', d.get('init_variant'))
print('  n_strong=', d.get('n_strong'), 'n_partial=', d.get('n_partial'),
      'n_weak=', d.get('n_weak'))
print('  final_CE=', fl.get('L_ce'))
print('  n_kosmos_anchors=', d.get('n_kosmos_anchors'))
for v in d.get('per_lang_verdicts', []):
    print(f\"  {v['lang']}: {v['verdict']} score={v['n_score']}/20\")
" 2>&1 | tee -a "$LOG"
  log "pipeline complete"
else
  log "PULL_FAILED"
  echo "pull failed" > "$VDIR/FAILURE.txt"
fi
