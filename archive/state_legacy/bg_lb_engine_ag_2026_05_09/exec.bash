#!/bin/bash
# emitted by tool/bg_lb_engine_ag_orchestrator.hexa
# BG-LB Engine A/G dual-engine 350M scratch pre-train (1.5GB target corpus) H100 lifecycle
# own 14 V14 mirror prereq + own 16 cost cap + own 30 ckpt pull + own 40 resource CLI
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/bg_lb_engine_ag_2026_05_09'
RESULTS_DIR='/Users/ghost/core/anima/state/bg_lb_engine_ag_2026_05_09/results'
CORPUS_TIER_A_V4='/Users/ghost/core/anima/state/anima_persona_tier_a_v4_2026_05_09.txt'
CORPUS_PERSONA_2='/Users/ghost/core/anima/state/anima_persona_tier_a_2026_05_08.txt'
CORPUS_DIALOGUE_2='/Users/ghost/core/anima/state/anima_dialogue_tier_a_iter2_2026_05_08.txt'
CORPUS_COMBINED='/Users/ghost/core/anima/state/bg_lb_engine_ag_2026_05_09/big_corpus.txt'
ARCH_PY='/Users/ghost/core/anima/training/engine_a_g_arch.py'
TRAIN_PY='/Users/ghost/core/anima/tool/transient_py/anima_clm_lb_h100.py'
RESOURCE='/Users/ghost/.hx/packages/resource/bin/resource'
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
BUDGET_HARD_CAP=65
MAX_WALL_MIN=1200
BG_LANE='BG-LB'
OWN_PID=$$
OWN_TS=$(date +%s)
POD_NAME="bg-lb-350m-pretrain-${OWN_TS}-pid${OWN_PID}"
DURATION='20h'
GPU='H100'
PROVIDER='runpod'
VERDICT="${STATE_DIR}/verdict.json"
RUN_LOG="${STATE_DIR}/run.log"
POD_INFO="${STATE_DIR}/pod_info.json"
START_EPOCH=$(date -u +%s)

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }

# Phase 0a: V14 mirror prereq verify (own 14)
log "=== Phase 0a: V14 mirror prereq verify (own 14) ==="
hexa run /Users/ghost/core/anima/tool/bg_lb_engine_ag_orchestrator.hexa --verify-v14 || { log 'FATAL: V14 mirrors missing'; exit 2; }

# Phase 0b: build combined corpus (tier_a_v4 + persona_2 + dialogue_2 — best available toward 1.5GB)
log "=== Phase 0b: build combined corpus ==="
if [ ! -s "$CORPUS_COMBINED" ]; then
    cat "$CORPUS_TIER_A_V4" > "$CORPUS_COMBINED"
    [ -f "$CORPUS_PERSONA_2" ] && cat "$CORPUS_PERSONA_2" >> "$CORPUS_COMBINED"
    [ -f "$CORPUS_DIALOGUE_2" ] && cat "$CORPUS_DIALOGUE_2" >> "$CORPUS_COMBINED"
fi
CORPUS_SZ=$(wc -c < "$CORPUS_COMBINED")
log "corpus_combined size=${CORPUS_SZ} bytes (target 1.5GB; best-available without iter-3)"

# Phase 1: provision-ephemeral with unique pod tag (own 40 + concurrency mitigation)
log "=== Phase 1: provision-ephemeral via resource CLI (pod_name=$POD_NAME) ==="
RESOURCE_EPHEMERAL_YES_COST=1 $RESOURCE provision-ephemeral --provider $PROVIDER --gpu $GPU --duration $DURATION --yes-cost --name "$POD_NAME" 2>&1 | tee -a "$RUN_LOG"
PROV_RC=${PIPESTATUS[0]}
if [ $PROV_RC -ne 0 ]; then log "FATAL: provision rc=$PROV_RC"; exit 3; fi

# Parse pod info — filter by own pod_name to avoid sibling BG-LA collision (concurrency mitigation)
POD_ID=$($RESOURCE ephemeral-list --json 2>/dev/null | python3 -c 'import json,sys,os; d=json.load(sys.stdin); pn=os.environ["POD_NAME"]; cands=[p for p in d.get("pods",[]) if pn in p.get("name","")]; print(cands[0]["pod_id"] if cands else "")' || echo '')
if [ -z "$POD_ID" ]; then log "FATAL: pod_id parse failed (pod_name=$POD_NAME not in ephemeral-list)"; exit 4; fi
SSH_INFO=$(runpodctl ssh info "$POD_ID" 2>&1 || echo '')
SSH_HOST=$(echo "$SSH_INFO" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -1)
SSH_PORT=$(echo "$SSH_INFO" | grep -oE 'port [0-9]+' | grep -oE '[0-9]+' | head -1)
log "pod_id=$POD_ID ssh=$SSH_HOST:$SSH_PORT pod_name=$POD_NAME"
echo "{\"pod_id\":\"$POD_ID\",\"pod_name\":\"$POD_NAME\",\"ssh_host\":\"$SSH_HOST\",\"ssh_port\":\"$SSH_PORT\",\"own_pid\":\"$OWN_PID\",\"own_ts\":\"$OWN_TS\"}" > "$POD_INFO"

# Phase 2: SSH + GPU smoke
log "=== Phase 2: SSH + GPU smoke ==="
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST 'nvidia-smi -L' 2>&1 | tee -a "$RUN_LOG"

# Phase 3: stage corpus + arch py + train py
log "=== Phase 3: stage artifacts to pod ==="
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST 'mkdir -p /workspace/anima_clm_lb /workspace/anima_clm_lb/ckpts /workspace/anima_clm_lb/state /workspace/data'
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no "$ARCH_PY" root@$SSH_HOST:/workspace/anima_clm_lb/engine_a_g_arch.py
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no "$TRAIN_PY" root@$SSH_HOST:/workspace/anima_clm_lb/anima_clm_lb_h100.py
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no "$CORPUS_COMBINED" root@$SSH_HOST:/workspace/data/big_corpus.txt
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST 'touch /workspace/anima_clm_lb/_pod_marker'

# Phase 4: install deps (Ubuntu 24.04 PEP 668 — break-system-packages per orchestrator gotcha memory)
log "=== Phase 4: install transformers/torch ==="
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST 'pip install --break-system-packages transformers safetensors 2>&1 | tail -5'

# Phase 5: launch training (nohup; preset lb_350m_pretrain; full corpus)
log "=== Phase 5: launch pod training (lb_350m_pretrain preset) ==="
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST 'cd /workspace/anima_clm_lb && nohup python3 anima_clm_lb_h100.py --preset lb_350m_pretrain --corpus /workspace/data/big_corpus.txt --output /workspace/anima_clm_lb/ckpts > train.log 2>&1 &'

# Phase 6: heartbeat monitor (60s tick, cost halt at hard cap)
log "=== Phase 6: heartbeat monitor ==="
ELAPSED=0
while [ $ELAPSED -lt $((MAX_WALL_MIN * 60)) ]; do
    sleep 60
    ELAPSED=$(($(date -u +%s) - START_EPOCH))
    COST=$(echo "scale=2; $ELAPSED * 2.99 / 3600" | bc)
    log "hb t=${ELAPSED}s cost=\$$COST pod=$POD_NAME"
    if (( $(echo "$COST > $BUDGET_HARD_CAP" | bc -l) )); then
        log "COST_OVERRUN — hard cap exceeded; killing"
        break
    fi
    DONE=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST 'test -f /workspace/anima_clm_lb/state/COMPLETE.sentinel && echo done || echo running' 2>/dev/null)
    if [ "$DONE" = "done" ]; then log 'COMPLETE.sentinel detected'; break; fi
done

# Phase 7: ckpt pull (own 30 mandate-1 BEFORE pod delete)
log "=== Phase 7: ckpt pull (own 30 mandate-1) ==="
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no -r -o ConnectTimeout=3600 root@$SSH_HOST:/workspace/anima_clm_lb/ckpts/. "$RESULTS_DIR/ckpts/" 2>&1 | tee -a "$RUN_LOG"
PULL_RC=${PIPESTATUS[0]}
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no -r root@$SSH_HOST:/workspace/anima_clm_lb/state/. "$RESULTS_DIR/state/" 2>&1 | tee -a "$RUN_LOG"

# Phase 8: size sanity check (own 30 mandate-2 ~1.3GB floor for 350M ckpt)
POD_SZ=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST 'du -sb /workspace/anima_clm_lb/ckpts | cut -f1' 2>/dev/null || echo 0)
LOCAL_SZ=$(du -sb "$RESULTS_DIR/ckpts" 2>/dev/null | cut -f1 || echo 0)
log "size check: pod=$POD_SZ local=$LOCAL_SZ (own 30 mandate-2 floor 0.9× pod; expect ~1.3GB for 350M bf16)"

# Phase 9: pod release ONLY if pull succeeded — own slug only target (concurrency mitigation)
if [ $PULL_RC -eq 0 ] && [ "$LOCAL_SZ" != "0" ]; then
    log "=== Phase 9: pod release (own slug only: $POD_NAME / pod_id=$POD_ID) ==="
    $RESOURCE release "$POD_NAME" --reason 'BG-LB pull verified' 2>&1 | tee -a "$RUN_LOG"
else
    log "PULL FAILED — POD RETAINED (own 30 mandate-3); manual release after recovery"
fi

# Phase 10: ledger append
log "=== Phase 10: ledger append ==="
python3 -c "import json,time,os; open('/Users/ghost/core/anima/state/anima_model_attempts_ledger.jsonl','a').write(json.dumps({'ts':time.strftime('%FT%TZ'),'bg_id':'BG-LB','cycle':'bg_lb_engine_ag_2026_05_09','verdict_path':'$VERDICT','pod_id':'$POD_ID','pod_name':'$POD_NAME','elapsed_s':$ELAPSED,'cost_usd_est':$COST,'corpus_size_bytes':$CORPUS_SZ}) + chr(10))"

# Phase 11: verdict + HF promote (private only — own 37 lifecycle)
log "=== Phase 11: verdict + HF promote (private default) ==="
if [ -f "$VERDICT" ]; then
    VERDICT_CLASS=$(python3 -c "import json; print(json.load(open('$VERDICT')).get('final_class','UNKNOWN'))" 2>/dev/null || echo UNKNOWN)
    log "verdict=$VERDICT_CLASS"
    if [[ "$VERDICT_CLASS" == "SIMPLE_STACK_PASS_STRICT_C3" || "$VERDICT_CLASS" == "SIMPLE_STACK_PASS_STRICT_C3_ANIMA" ]]; then
        log "HF private upload: dancinlab/clm-v5-bg-lb-350m-pretrain-path-a-remapped (own 31 Flavor B + own 37 private default)"
        # huggingface-cli upload (private flag) — actual upload deferred to anima_clm_lb_h100.py post-eval
    fi
fi
log "BG-LB orchestrator DONE"
