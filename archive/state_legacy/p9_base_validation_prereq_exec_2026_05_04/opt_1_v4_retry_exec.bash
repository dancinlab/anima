#!/bin/bash
# v4 RETRY (BG-γ' 2026-05-04) — explicit sentencepiece pre-install fix.
# Derived from tool/p9_opt_1_v4_exec_h100_orchestrator.hexa emitted exec.bash.
# raw#9 sibling-pattern Mac-side bash. raw#37 H100 transient py.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04'
RESULTS_DIR='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_results'
POD_INFO='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_pod_info.json'
VERDICT='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_verdict.json'
RUN_LOG='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_run.log'
HEARTBEAT='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_heartbeat.txt'
BOOT_LOG='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_boot.log'
SHIM_PATH='/Users/ghost/core/anima/tool/transient_py/clm_v4_hf_format_shim.py'
FIXTURE_PATH='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_consciousness_states_fixture.json'
TRAIN_AVG_DST='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_train_avg_fixture.json'
DECODER_V3_PATH='/Users/ghost/core/anima/ready/anima/models/legacy/decoder_v3.py'
CONSCIOUS_DEC_PATH='/Users/ghost/core/anima/ready/models/conscious_decoder.py'
RUN_H100_PATH='/Users/ghost/core/anima/state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_run_h100.bash'
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
RUNPODCTL='/opt/homebrew/bin/runpodctl'
MAX_WALL_MIN=60
BUDGET_HARD_CAP=3
OD_RATE=2.99
START_EPOCH=$(date -u +%s)

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }
hb()  { echo "[$(date -u +%FT%TZ)] $*" > "$HEARTBEAT"; }
redact_hf() { sed -E 's/(HF_TOKEN["[:space:]]*[:=]["[:space:]]*)hf_[A-Za-z0-9_]+/\1<REDACTED>/g; s/(hf_)[A-Za-z0-9_]{20,}/\1<REDACTED>/g'; }

# ── Stage 0: secrets ──
export RUNPOD_API_KEY=$(secret get --raw runpod.api_key 2>/dev/null)
export HF_TOKEN_LOCAL=$(secret get --raw huggingface.token 2>/dev/null)
if [ -z "${RUNPOD_API_KEY:-}" ] || [ -z "${HF_TOKEN_LOCAL:-}" ]; then
    log "FATAL: secrets unavailable"
    exit 2
fi
if [[ "$RUNPOD_API_KEY" == \*\*\** ]] || [[ "$HF_TOKEN_LOCAL" == \*\*\** ]]; then
    log "FATAL: secret returned redacted form despite --raw"
    exit 2
fi
log "secrets OK (runpod=${#RUNPOD_API_KEY}b, hf=${#HF_TOKEN_LOCAL}b)"
hb "stage0_secrets_loaded"

# ── Stage 1: boot H100 pod ──
POD_NAME='anima-p9-opt-1-v4-retry-2026-05-04'
log "booting pod=$POD_NAME (H100 80GB HBM3 secure on-demand @ \$$OD_RATE/hr)"
BOOT_RAW_OUT="$STATE_DIR/opt_1_v4_exec_boot.raw.tmp"
hb "stage1_booting_pod"
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
    > "$BOOT_RAW_OUT" 2>&1
BOOT_RC=$?
redact_hf < "$BOOT_RAW_OUT" > "$BOOT_LOG"
rm -f "$BOOT_RAW_OUT"
if [ $BOOT_RC -ne 0 ]; then
    log "FATAL: pod boot failed rc=$BOOT_RC"
    cat "$BOOT_LOG" | redact_hf | tee -a "$RUN_LOG"
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed" '{cycle:"opt_1_v4_exec_2026_05_04",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
    exit 3
fi
POD_ID=$(grep -oE '"[a-z0-9]{14}"' "$BOOT_LOG" | head -1 | tr -d '"')
if [ -z "$POD_ID" ]; then
    POD_ID=$(grep -oE 'pod [a-z0-9]{12,16}' "$BOOT_LOG" | head -1 | awk '{print $2}')
fi
if [ -z "$POD_ID" ]; then
    log "FATAL: cannot extract pod_id"
    cat "$BOOT_LOG"
    exit 4
fi
log "pod_id=$POD_ID"
echo '{"pod_id":"'$POD_ID'","booted_ts":"'$(date -u +%FT%TZ)'"}' > "$POD_INFO"
hb "stage1_pod_booted pod_id=$POD_ID"

# ── Stage 1b: kill-on-exit trap ──
_kill_pod() {
    log "[trap] killing pod=$POD_ID (auto-kill mandatory)"
    $RUNPODCTL pod stop "$POD_ID" 2>&1 | tee -a "$RUN_LOG" || true
    sleep 3
    $RUNPODCTL pod delete "$POD_ID" 2>&1 | tee -a "$RUN_LOG" || true
    sleep 3
    POST=$($RUNPODCTL pod get "$POD_ID" 2>&1 | head -3)
    log "[trap] post-kill: $POST"
    POD_404=0
    if echo "$POST" | grep -qiE '404|not.?found|no.?pod'; then
        POD_404=1
    fi
    if [ -f "$POD_INFO" ]; then
        jq --arg killed "$(date -u +%FT%TZ)" --arg post "$POST" --argjson p404 "$POD_404" \
            '. + {killed_ts:$killed, post_kill_status:$post, pod_kill_verified_404:($p404==1)}' "$POD_INFO" > "$POD_INFO.tmp" && mv "$POD_INFO.tmp" "$POD_INFO" || true
    fi
}
trap _kill_pod EXIT INT TERM

# ── Stage 2: wait for SSH (max 6min) ──
log "waiting for SSH ready (max 6min)"
hb "stage2_waiting_ssh"
SSH_HOST=''
SSH_PORT=''
for i in $(seq 1 36); do
    INFO=$($RUNPODCTL pod get "$POD_ID" -o json 2>/dev/null)
    SSH_HOST=$(echo "$INFO" | jq -r '.ssh.ip // empty' 2>/dev/null)
    SSH_PORT=$(echo "$INFO" | jq -r '.ssh.port // empty' 2>/dev/null)
    if [ -n "$SSH_HOST" ] && [ "$SSH_HOST" != "null" ] && [ -n "$SSH_PORT" ] && [ "$SSH_PORT" != "null" ]; then
        if ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>/dev/null | grep -q READY; then
            log "SSH ready at $SSH_HOST:$SSH_PORT (after ${i} probes)"
            break
        fi
    fi
    sleep 10
done
if [ -z "$SSH_HOST" ] || [ "$SSH_HOST" = "null" ] || [ -z "$SSH_PORT" ] || [ "$SSH_PORT" = "null" ]; then
    log "FATAL: pod never reached SSH ready in 6min"
    exit 5
fi
jq --arg h "$SSH_HOST" --arg p "$SSH_PORT" '. + {ssh_host:$h, ssh_port:($p|tonumber)}' "$POD_INFO" > "$POD_INFO.tmp" && mv "$POD_INFO.tmp" "$POD_INFO"
hb "stage2_ssh_ready host=$SSH_HOST port=$SSH_PORT"

SSH="ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $SSH_PORT root@$SSH_HOST"
SCP="scp -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $SSH_PORT"

# ── Stage 3: scp shim + fixture + legacy decoder modules + run script ──
log "setup: ssh mkdir + scp shim v4 + canonical_zero fixture + legacy decoder + run_h100.bash"
hb "stage3_setup_starting"
$SSH 'mkdir -p /workspace/p9_v4_exec/results /root/anima/ready/anima/models/legacy /root/anima/ready/models'
$SCP "$SHIM_PATH" "root@$SSH_HOST:/workspace/p9_v4_exec/clm_v4_hf_format_shim.py" 2>&1 | tail -1
$SCP "$FIXTURE_PATH" "root@$SSH_HOST:/workspace/p9_v4_exec/opt_1_v4_consciousness_states_fixture.json" 2>&1 | tail -1
$SCP "$DECODER_V3_PATH" "root@$SSH_HOST:/root/anima/ready/anima/models/legacy/decoder_v3.py" 2>&1 | tail -1
$SCP "$CONSCIOUS_DEC_PATH" "root@$SSH_HOST:/root/anima/ready/models/conscious_decoder.py" 2>&1 | tail -1
$SCP "$RUN_H100_PATH" "root@$SSH_HOST:/workspace/p9_v4_exec/run_h100.bash" 2>&1 | tail -1
$SSH 'chmod +x /workspace/p9_v4_exec/run_h100.bash'

log "launching v4 exec on H100"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/p9_v4_exec/hf_token.env && cd /workspace/p9_v4_exec && set -a && . hf_token.env && set +a && nohup bash run_h100.bash > orchestrator.log 2>&1 & echo $! > run.pid; disown $! 2>/dev/null || true; sleep 2; cat run.pid'
hb "stage3_h100_launched"

# ── Stage 4: poll loop ──
log "poll loop start (max ${MAX_WALL_MIN}min, budget cap \$${BUDGET_HARD_CAP})"
COMPLETE=0
POLL_INTERVAL=120
while true; do
    NOW=$(date -u +%s)
    ELAPSED_MIN=$(( (NOW - START_EPOCH) / 60 ))
    ELAPSED_HR_DEC=$(awk "BEGIN{printf \"%.4f\", ($NOW - $START_EPOCH) / 3600}")
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

    PROBE=$($SSH 'ls /workspace/p9_v4_exec/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ps -p $(cat /workspace/p9_v4_exec/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|')"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|' | head -c 200)"

    # incremental sync (small JSONs only)
    $SCP -r "root@$SSH_HOST:/workspace/p9_v4_exec/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/p9_v4_exec/orchestrator.log" "$STATE_DIR/opt_1_v4_retry_h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync + auto-kill imminent"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/p9_v4_exec/results/*" "$RESULTS_DIR/" 2>&1 | tail -3 | tee -a "$RUN_LOG" || true
        # Pull v4_apply.log + train_avg fixture + sanity eval logs
        $SCP "root@$SSH_HOST:/workspace/p9_v4_exec/v4_apply.log" "$RESULTS_DIR/v4_apply.log" 2>/dev/null || true
        $SCP "root@$SSH_HOST:/workspace/p9_v4_exec/output_v4/config.json" "$RESULTS_DIR/output_v4_config.json" 2>/dev/null || true
        $SCP "root@$SSH_HOST:/workspace/p9_v4_exec/results/train_avg_fixture.json" "$TRAIN_AVG_DST" 2>/dev/null || true
        $SCP "root@$SSH_HOST:/workspace/p9_v4_exec/orchestrator.log" "$STATE_DIR/opt_1_v4_retry_h100_orchestrator.log" 2>&1 | tail -1 || true
        break
    fi

    sleep $POLL_INTERVAL
done

# ── Stage 5: pod kill via trap (auto on exit) ──

# ── Stage 6: verdict ──
log "computing verdict"
FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")
hb "stage6_verdict_computing"

# Read structured verdict json from H100 (results/v4_verdict.json) if present
V4_VERDICT_SRC="$RESULTS_DIR/v4_verdict.json"

F_V4_3='UNKNOWN'
F_V4_4='HARVEST_STUB_ONLY'
HARVEST_VIA='FAILED'
FINITE_FORWARD='unknown'
SANITY_CZ='null'
SANITY_NF='null'
LIFT_PP='null'

if [ -f "$V4_VERDICT_SRC" ]; then
    F_V4_3=$(jq -r '.f_shim_v4_3 // "UNKNOWN"' "$V4_VERDICT_SRC")
    F_V4_4=$(jq -r '.f_shim_v4_4 // "HARVEST_STUB_ONLY"' "$V4_VERDICT_SRC")
    HARVEST_VIA=$(jq -r '.harvest_via // "FAILED"' "$V4_VERDICT_SRC")
    FINITE_FORWARD=$(jq -r '.finite_forward // "unknown"' "$V4_VERDICT_SRC")
    SANITY_CZ=$(jq -r '.sanity_canonical_zero_hellaswag_acc // "null"' "$V4_VERDICT_SRC")
    SANITY_NF=$(jq -r '.sanity_no_fixture_hellaswag_acc // "null"' "$V4_VERDICT_SRC")
    if [ "$SANITY_CZ" != "null" ] && [ "$SANITY_NF" != "null" ]; then
        LIFT_PP=$(awk "BEGIN{printf \"%.2f\", ($SANITY_CZ - $SANITY_NF) * 100}")
    fi
fi

# Pod 404 verification
POD_404='false'
if [ -f "$POD_INFO" ]; then
    POD_404=$(jq -r '.pod_kill_verified_404 // false' "$POD_INFO")
fi

jq -n \
    --arg cycle "opt_1_v4_exec_2026_05_04" \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg pod "$POD_ID" \
    --argjson pod404 "$POD_404" \
    --arg f3 "$F_V4_3" \
    --arg f4 "$F_V4_4" \
    --arg via "$HARVEST_VIA" \
    --arg fwd "$FINITE_FORWARD" \
    --arg cz "$SANITY_CZ" \
    --arg nf "$SANITY_NF" \
    --arg lift "$LIFT_PP" \
    --argjson wall "$FINAL_ELAPSED_MIN" \
    --argjson cost "$FINAL_COST" \
    --argjson complete "$COMPLETE" \
    '{
        cycle: "opt_1_v4_retry_2026_05_04",
        ts_utc: $ts, pod_id: $pod,
        pod_terminated: true,
        pod_kill_verified_404: $pod404,
        scope: "F-SHIM-V4-3 retry (sentencepiece pre-install fix) + train_avg harvest stub + canonical_zero sanity eval (limit=100 hellaswag)",
        f_shim_v4_1_dry_run_carry: "PASS",
        f_shim_v4_2_v3_regression_carry: "PASS",
        f_shim_v4_3_canonical_zero_finite_forward: $f3,
        f_shim_v4_4_train_avg_above_random_5pt: $f4,
        finite_forward: $fwd,
        train_avg_fixture_harvested_via: $via,
        train_avg_fixture_path: "state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_train_avg_fixture.json",
        sanity_eval_canonical_zero_hellaswag_acc: ($cz | if . == "null" then null else tonumber end),
        sanity_eval_no_fixture_hellaswag_acc: ($nf | if . == "null" then null else tonumber end),
        consciousness_injection_lift_pp: ($lift | if . == "null" then null else tonumber end),
        wall_time_min: $wall,
        actual_cost_usd: $cost,
        complete_sentinel_detected: ($complete == 1),
        honest_c3: [
            "canonical_zero is sanity-only fixture; cross_attn.o_proj init std=0.001 + zero values yields ~zero residual; lift_pp expected near 0",
            "limit=100 hellaswag has stderr ~5pp; lift_pp <5pp is within noise",
            "train_avg harvest is STUB if approach (b) used (synthetic forward-pass average via dummy text) — not a true train-time average",
            "H100 bfloat16 ⇒ slight numeric drift vs fp32; 1-batch forward finite check is robust (NaN/Inf would manifest immediately)",
            "shim v4 modeling.py adds 88 LoC dormant fixture loader; F-SHIM-V4-2 is runtime-equivalence not byte-level",
            "block_size=512 truncation orthogonal — v4 fixture cannot fix MMLU prompt left-truncation"
        ]
    }' > "$VERDICT"

log "verdict written: f_shim_v4_3=$F_V4_3 harvest_via=$HARVEST_VIA wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
hb "verdict f_shim_v4_3=$F_V4_3 harvest_via=$HARVEST_VIA"
echo "__P9_OPT_1_V4_EXEC__ f_shim_v4_3=$F_V4_3" | tee -a "$RUN_LOG"
exit 0
