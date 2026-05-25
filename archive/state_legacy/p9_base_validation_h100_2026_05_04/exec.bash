#!/bin/bash
# emitted by tool/p9_base_validation_h100_orchestrator.hexa — P9 F1_v3 base-validation H100 lifecycle
# raw#9 Mac-side bash grandfathered (sibling pattern: tool/h100_pods_sync.bash, tool/h100_corpus_shard_prestage.bash etc.)
# DO NOT edit by hand; regenerate via `hexa run tool/p9_base_validation_h100_orchestrator.hexa --emit`.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/p9_base_validation_h100_2026_05_04'
RESULTS_DIR="$STATE_DIR/results"
POD_INFO="$STATE_DIR/pod_info.json"
VERDICT="$STATE_DIR/verdict.json"
RUN_LOG="$STATE_DIR/run.log"
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
RUNPODCTL='/opt/homebrew/bin/runpodctl'
MAX_WALL_MIN=180
BUDGET_HARD_CAP=10
SPOT_RATE=2.54
OD_RATE=2.99
START_EPOCH=$(date -u +%s)

mkdir -p "$STATE_DIR" "$RESULTS_DIR"
log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }

# ── Stage 0: secrets ──────────────────────────────────────────────────────
export RUNPOD_API_KEY=$(secret get runpod.api_key 2>/dev/null)
export HF_TOKEN_LOCAL=$(secret get huggingface.token 2>/dev/null)
if [ -z "${RUNPOD_API_KEY:-}" ] || [ -z "${HF_TOKEN_LOCAL:-}" ]; then
    log "FATAL: secrets unavailable"
    exit 2
fi
log "secrets OK (runpod=${#RUNPOD_API_KEY}b, hf=${#HF_TOKEN_LOCAL}b)"

# ── Stage 1: boot H100 spot pod ───────────────────────────────────────────
POD_NAME='anima-p9-base-val-h100-2026-05-04'
log "booting pod=$POD_NAME (H100 80GB HBM3 secure on-demand @ \$$OD_RATE/hr; 1.5-2h job → ~\$5)"
BOOT_OUT="$STATE_DIR/boot.log"
$RUNPODCTL pod create \
    --name "$POD_NAME" \
    --gpu-id 'NVIDIA H100 80GB HBM3' \
    --gpu-count 1 \
    --image 'runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04' \
    --container-disk-in-gb 80 \
    --volume-in-gb 50 \
    --volume-mount-path /workspace \
    --ports '22/tcp,8888/http' \
    --cloud-type SECURE \
    --ssh \
    --env "{\"HF_TOKEN\":\"$HF_TOKEN_LOCAL\"}" \
    > "$BOOT_OUT" 2>&1
BOOT_RC=$?
log "boot rc=$BOOT_RC"
cat "$BOOT_OUT" | tee -a "$RUN_LOG"

if [ $BOOT_RC -ne 0 ]; then
    log "FATAL: pod boot failed"
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed_rc_$BOOT_RC" '{cycle:"p9_base_validation_h100_2026_05_04",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
    exit 3
fi

# Extract pod_id (new runpodctl pod create returns JSON like {"id":"...","name":"..."}; legacy prints `pod "abc..." created ...`)
POD_ID=$(jq -r '.id // empty' "$BOOT_OUT" 2>/dev/null)
if [ -z "$POD_ID" ] || [ "$POD_ID" = "null" ]; then
    POD_ID=$(grep -oE '"id"\s*:\s*"[a-z0-9]+"' "$BOOT_OUT" | head -1 | grep -oE '"[a-z0-9]{12,18}"' | tail -1 | tr -d '"')
fi
if [ -z "$POD_ID" ]; then
    POD_ID=$(grep -oE '"[a-z0-9]{12,18}"' "$BOOT_OUT" | head -1 | tr -d '"')
fi
if [ -z "$POD_ID" ]; then
    log "FATAL: cannot extract pod_id from boot output"
    exit 4
fi
log "pod_id=$POD_ID"
echo "{\"pod_id\":\"$POD_ID\",\"booted_ts\":\"$(date -u +%FT%TZ)\"}" > "$POD_INFO"

# ── Stage 1b: kill-on-exit trap MANDATORY ─────────────────────────────────
_kill_pod() {
    log "[trap] killing pod=$POD_ID (auto-kill mandatory)"
    # pod delete terminates directly. pod stop first (defensive in case delete needs stopped state).
    $RUNPODCTL pod stop "$POD_ID" 2>&1 | tee -a "$RUN_LOG" || true
    sleep 3
    $RUNPODCTL pod delete "$POD_ID" 2>&1 | tee -a "$RUN_LOG" || true
    sleep 3
    # verify gone — should return "pod not found" 404
    STATUS=$($RUNPODCTL pod get "$POD_ID" 2>&1 | head -3 | tr '\n' '|')
    log "[trap] post-kill status_head=$STATUS"
    if echo "$STATUS" | grep -qi "not found\|404"; then
        log "[trap] pod kill CONFIRMED (404)"
    else
        log "[trap] WARN: pod may not be fully gone — manual check required"
    fi
    if [ -f "$POD_INFO" ]; then
        jq --arg killed "$(date -u +%FT%TZ)" --arg post "$STATUS" \
            '. + {killed_ts:$killed, post_kill_status:$post}' "$POD_INFO" > "$POD_INFO.tmp" && mv "$POD_INFO.tmp" "$POD_INFO" || true
    fi
}
trap _kill_pod EXIT INT TERM

# ── Stage 2: wait for SSH ready ───────────────────────────────────────────
log "waiting for SSH ready (max 6min)"
SSH_HOST=''
SSH_PORT=''
for i in $(seq 1 36); do
    INFO=$($RUNPODCTL pod get "$POD_ID" -o json 2>/dev/null)
    SSH_HOST=$(echo "$INFO" | jq -r '.ssh.ip // empty' 2>/dev/null)
    SSH_PORT=$(echo "$INFO" | jq -r '.ssh.port // empty' 2>/dev/null)
    if [ -n "$SSH_HOST" ] && [ "$SSH_HOST" != "null" ] && [ -n "$SSH_PORT" ] && [ "$SSH_PORT" != "null" ]; then
        if ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=8 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>/dev/null | grep -q READY; then
            log "SSH ready at $SSH_HOST:$SSH_PORT (after ${i} probes)"
            break
        fi
    fi
    sleep 10
done
if [ -z "$SSH_HOST" ] || [ "$SSH_HOST" = "null" ] || [ -z "$SSH_PORT" ] || [ "$SSH_PORT" = "null" ]; then
    log "FATAL: pod never reached SSH ready"
    exit 5
fi
jq --arg h "$SSH_HOST" --arg p "$SSH_PORT" '. + {ssh_host:$h, ssh_port:($p|tonumber)}' "$POD_INFO" > "$POD_INFO.tmp" && mv "$POD_INFO.tmp" "$POD_INFO"

SSH="ssh -i $SSH_KEY -o StrictHostKeyChecking=no -p $SSH_PORT root@$SSH_HOST"
SCP="scp -i $SSH_KEY -o StrictHostKeyChecking=no -P $SSH_PORT"

# ── Stage 3: prime cache (ubu1 → Mac → H100) ─────────────────────────────
log "priming HF cache"
CLM_LOCAL_DIR="$STATE_DIR/clm_v4_hf"
if [ ! -f "$CLM_LOCAL_DIR/model.safetensors" ]; then
    mkdir -p "$CLM_LOCAL_DIR"
    log "rsync CLM v4 HF dir from ubu1 → Mac"
    rsync -a ubu1:p9_clm_v4_hf_format_2026_05_04/output/ "$CLM_LOCAL_DIR/" 2>&1 | tail -3 | tee -a "$RUN_LOG"
fi
if [ ! -f "$CLM_LOCAL_DIR/model.safetensors" ]; then
    log "FATAL: CLM v4 HF dir not present after rsync"
    exit 6
fi
log "scp CLM v4 HF dir → H100"
$SSH 'mkdir -p /workspace/p9_base_val/clm_v4_hf /workspace/p9_base_val/results'
$SCP -r "$CLM_LOCAL_DIR"/* "root@$SSH_HOST:/workspace/p9_base_val/clm_v4_hf/" 2>&1 | tail -3 | tee -a "$RUN_LOG"

log "H100: install lm-eval + download Llama-3.2-3B base"
cat > "$STATE_DIR/setup.sh" <<'SETUPEOF'
#!/bin/bash
set -uo pipefail
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
pip install -q --no-input huggingface_hub 'lm-eval==0.4.11' 'transformers>=4.45' accelerate datasets 2>&1 | tail -10
huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -3 || true
huggingface-cli download meta-llama/Llama-3.2-3B 2>&1 | tail -5
echo "[setup] complete $(date -u +%FT%TZ)"
SETUPEOF
$SCP "$STATE_DIR/setup.sh" "root@$SSH_HOST:/workspace/p9_base_val/setup.sh" 2>&1 | tail -1
$SSH 'chmod +x /workspace/p9_base_val/setup.sh && bash /workspace/p9_base_val/setup.sh' 2>&1 | tail -25 | tee -a "$RUN_LOG"

# ── Stage 4: upload run_h100.sh + launch detached ─────────────────────────
log "uploading run_h100.sh + launching benchmark suite"
$SCP "$STATE_DIR/run_h100.sh" "root@$SSH_HOST:/workspace/p9_base_val/run_h100.sh" 2>&1 | tail -1
$SSH 'chmod +x /workspace/p9_base_val/run_h100.sh && cd /workspace/p9_base_val && nohup bash run_h100.sh > orchestrator.log 2>&1 & PID=$!; echo $PID > run.pid; disown $PID 2>/dev/null || true; sleep 2; cat run.pid'

# ── Stage 5: poll loop with hard caps ─────────────────────────────────────
log "poll loop start (max ${MAX_WALL_MIN}min, budget cap \$${BUDGET_HARD_CAP})"
COMPLETE=0
while true; do
    NOW=$(date -u +%s)
    ELAPSED_MIN=$(( (NOW - START_EPOCH) / 60 ))
    ELAPSED_HR_DEC=$(awk "BEGIN{printf \"%.3f\", ($NOW - $START_EPOCH) / 3600}")
    ELAPSED_COST=$(awk "BEGIN{printf \"%.2f\", $ELAPSED_HR_DEC * $OD_RATE}")

    COST_OVER=$(awk "BEGIN{print ($ELAPSED_COST > $BUDGET_HARD_CAP) ? 1 : 0}")
    if [ "$COST_OVER" = "1" ]; then
        log "COST CAP HIT \$$ELAPSED_COST > \$$BUDGET_HARD_CAP — auto-kill"
        break
    fi
    if [ $ELAPSED_MIN -ge $MAX_WALL_MIN ]; then
        log "WALL CAP HIT ${ELAPSED_MIN}min ≥ ${MAX_WALL_MIN}min — auto-kill"
        break
    fi

    PROBE=$($SSH 'ls /workspace/p9_base_val/results/COMPLETE.sentinel 2>/dev/null; ps -p $(cat /workspace/p9_base_val/run.pid 2>/dev/null) -o pid,etime,cmd 2>/dev/null | tail -1' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$PROBE"

    $SCP -r "root@$SSH_HOST:/workspace/p9_base_val/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/p9_base_val/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q COMPLETE.sentinel; then
        log "COMPLETE.sentinel detected"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/p9_base_val/results/*.json" "$RESULTS_DIR/" 2>&1 | tail -3 | tee -a "$RUN_LOG"
        $SCP -r "root@$SSH_HOST:/workspace/p9_base_val/results/*.log" "$RESULTS_DIR/" 2>/dev/null
        $SCP "root@$SSH_HOST:/workspace/p9_base_val/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>&1 | tail -1
        break
    fi

    sleep 600
done

# ── Stage 6: pod kill via trap (set above) ────────────────────────────────
# trap fires on exit — pod stop + remove

# ── Stage 7: verdict skeleton ─────────────────────────────────────────────
log "computing verdict skeleton"
FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")
BENCH_COUNT_LLAMA=$(ls $RESULTS_DIR/llama_*.json 2>/dev/null | wc -l | awk '{print $1}')
BENCH_COUNT_CLM=$(ls $RESULTS_DIR/clm_v4_*.json 2>/dev/null | wc -l | awk '{print $1}')

VERDICT_LABEL='FAIL'
if [ "$COMPLETE" = "1" ] && [ "$BENCH_COUNT_LLAMA" -ge 3 ] && [ "$BENCH_COUNT_CLM" -ge 3 ]; then
    VERDICT_LABEL='PASS_PENDING_NUMERIC_GATE'
elif [ "$BENCH_COUNT_LLAMA" -ge 2 ] || [ "$BENCH_COUNT_CLM" -ge 2 ]; then
    VERDICT_LABEL='PARTIAL'
fi

jq -n \
    --arg cycle "p9_base_validation_h100_2026_05_04" \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg pod "$POD_ID" \
    --arg verdict "$VERDICT_LABEL" \
    --arg sentinel "__P9_BENCH_A_PRIME_BASE_VAL__ $VERDICT_LABEL" \
    --argjson wall "$FINAL_ELAPSED_MIN" \
    --argjson cost "$FINAL_COST" \
    --argjson llama_n "$BENCH_COUNT_LLAMA" \
    --argjson clm_n "$BENCH_COUNT_CLM" \
    --argjson complete "$COMPLETE" \
    '{
        cycle: $cycle, ts_utc: $ts, pod_id: $pod, verdict: $verdict,
        f1_v3_base_validation_status_emit: $sentinel,
        wall_time_minutes: $wall, actual_cost_usd: $cost,
        complete_sentinel_detected: ($complete == 1),
        bench_count: {llama_3_2_3b: $llama_n, clm_v4_base: $clm_n, total_required: 6},
        next: "run consolidator (paired bootstrap + McNemar + C1-C4 gate per spec section 3.2)"
    }' > "$VERDICT"

log "verdict=$VERDICT_LABEL wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
echo "__P9_BENCH_A_PRIME_BASE_VAL__ $VERDICT_LABEL" | tee -a "$RUN_LOG"
exit 0
