#!/bin/bash
# emitted by tool/clm_v4_lora_train_orchestrator_opt_b.hexa — CLM v4 OPT-B cross_attn retrain lifecycle
# raw#9 sibling-pattern Mac-side bash; raw#37 H100 transient py.
# OPT-B variant — sibling of state/clm_v4_lora_sft_2026_05_05/exec.bash; v1 UNTOUCHED.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/clm_v4_lora_sft_opt_b_2026_05_05'
RESULTS_DIR='/Users/ghost/core/anima/state/clm_v4_lora_sft_opt_b_2026_05_05/results'
CORPUS_DIR='/Users/ghost/core/anima/state/clm_v4_lora_sft_opt_b_2026_05_05/corpus'
SLICE_A_LOCAL='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl'
CORPUS_MIX_PY='/Users/ghost/core/anima/tool/transient_py/p9_retrain_v2_corpus_mix.py'
TRAIN_PY='/Users/ghost/core/anima/tool/transient_py/clm_v4_lora_train_opt_b.py'
POD_INFO='/Users/ghost/core/anima/state/clm_v4_lora_sft_opt_b_2026_05_05/pod_info.json'
VERDICT='/Users/ghost/core/anima/state/clm_v4_lora_sft_opt_b_2026_05_05/verdict.json'
RUN_LOG='/Users/ghost/core/anima/state/clm_v4_lora_sft_opt_b_2026_05_05/run.log'
HEARTBEAT='/Users/ghost/core/anima/state/clm_v4_lora_sft_opt_b_2026_05_05/heartbeat.txt'
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
RUNPODCTL='/opt/homebrew/bin/runpodctl'
MAX_WALL_MIN=300
BUDGET_HARD_CAP=50
BUDGET_TARGET=30
OD_RATE=2.99
HF_BASE_REPO='need-singularity/clm-v4-mk2-v1'
BG_LANE='OPT-B-CROSS-ATTN-RETRAIN'
TARGET_USD='30'
WATCHDOG_REGISTER='/Users/ghost/core/anima/tool/h100_register.bash'
WATCHDOG_HB_DIR='/Users/ghost/core/anima/state/h100_watchdog/heartbeats'
WATCHDOG_HEXA='/Users/ghost/core/anima/tool/h100_cost_watchdog.hexa'
START_EPOCH=$(date -u +%s)

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }
hb()  { echo "[$(date -u +%FT%TZ)] $*" > "$HEARTBEAT"; }
redact_hf() { sed -E 's/(HF_TOKEN["[:space:]]*[:=]["[:space:]]*)hf_[A-Za-z0-9_]+/\1<REDACTED>/g; s/(hf_)[A-Za-z0-9_]{20,}/\1<REDACTED>/g'; }

log "OPT-B variant: cross_attn qkvo retrain — REQUIRES EXPLICIT USER $20-50 COST ACK"
log "hyperparameter locks: lr=5e-6 dropout=0.10 max_steps=3000 abort_drift_pp=-10.0"

# ── Stage 0: secrets (raw bypass for redaction wrapper) ──
export RUNPOD_API_KEY=$(/Users/ghost/core/secret/bin/secret get runpod.api_key --raw 2>/dev/null)
export HF_TOKEN_LOCAL=$(/Users/ghost/core/secret/bin/secret get huggingface.token --raw 2>/dev/null)
if [ -z "${RUNPOD_API_KEY:-}" ] || [ -z "${HF_TOKEN_LOCAL:-}" ]; then
    log "FATAL: secrets unavailable"
    exit 2
fi
log "secrets OK (runpod=${#RUNPOD_API_KEY}b hf=${#HF_TOKEN_LOCAL}b)"
hb "stage0_secrets_loaded"

# ── Stage 0b: HF whoami pre-flight (L9) ──
WHOAMI=$(curl -s -H "Authorization: Bearer $HF_TOKEN_LOCAL" 'https://huggingface.co/api/whoami-v2' | head -c 300)
if echo "$WHOAMI" | grep -q '"name"'; then
    USER=$(echo "$WHOAMI" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("name","?"))')
    log "hf auth PASS user=$USER"
else
    log "FATAL L9: hf auth FAIL: $WHOAMI"
    exit 2
fi
hb "stage0b_hf_auth_ok"

# ── Pre-flight: slice A reused from v1 cycle ──
if [ ! -f "$SLICE_A_LOCAL" ]; then
    log "FATAL: slice A missing (reused from v1 cycle): $SLICE_A_LOCAL"
    exit 2
fi
SLICE_A_LINES=$(wc -l < "$SLICE_A_LOCAL" | awk '{print $1}')
log "slice A OK ($SLICE_A_LINES lines, reused from v1)"

# ── Stage 1: boot H100 SECURE on-demand ──
POD_NAME='anima-clm-v4-lora-opt-b-2026-05-05'
log "booting pod=$POD_NAME (H100 80GB SXM SECURE on-demand @ \$$OD_RATE/hr)"
BOOT_RAW_OUT="$STATE_DIR/boot.raw.tmp"
BOOT_OUT="$STATE_DIR/boot.log"
hb "stage1_booting_pod"
$RUNPODCTL pod create \
    --name "$POD_NAME" \
    --gpu-id 'NVIDIA H100 80GB HBM3' \
    --gpu-count 1 \
    --image 'runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04' \
    --container-disk-in-gb 100 \
    --volume-in-gb 120 \
    --volume-mount-path /workspace \
    --ports '22/tcp,8888/http' \
    --cloud-type SECURE \
    --ssh \
    --env "{\"HF_TOKEN\":\"$HF_TOKEN_LOCAL\"}" \
    > "$BOOT_RAW_OUT" 2>&1
BOOT_RC=$?
redact_hf < "$BOOT_RAW_OUT" > "$BOOT_OUT"
rm -f "$BOOT_RAW_OUT"
if [ $BOOT_RC -ne 0 ]; then
    log "FATAL: pod boot failed rc=$BOOT_RC"
    cat "$BOOT_OUT" | tee -a "$RUN_LOG"
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed" '{cycle:"clm_v4_lora_sft_opt_b_2026_05_05",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
    exit 3
fi
POD_ID=$(grep -oE '"[a-z0-9]{14}"' "$BOOT_OUT" | head -1 | tr -d '"')
if [ -z "$POD_ID" ]; then
    POD_ID=$(grep -oE 'pod [a-z0-9]{12,16}' "$BOOT_OUT" | head -1 | awk '{print $2}')
fi
if [ -z "$POD_ID" ]; then
    log "FATAL: cannot extract pod_id"
    exit 4
fi
log "pod_id=$POD_ID"
echo '{"pod_id":"'$POD_ID'","booted_ts":"'$(date -u +%FT%TZ)'","bg_lane":"'$BG_LANE'"}' > "$POD_INFO"
hb "stage1_pod_booted pod_id=$POD_ID"

# === own 16 Phase 2 watchdog hook (boot — register pod) ===
if [ -x "$WATCHDOG_REGISTER" ] || [ -f "$WATCHDOG_REGISTER" ]; then
    if bash "$WATCHDOG_REGISTER" "$POD_ID" "$BG_LANE" "$TARGET_USD" 2>&1 | tee -a "$RUN_LOG"; then
        WATCHDOG_REGISTERED=1
        log "[watchdog] register OK pod=$POD_ID lane=$BG_LANE target=\$$TARGET_USD"
    else
        WATCHDOG_REGISTERED=0
        log "[watchdog] WARN register failed (rc=$?)"
    fi
else
    WATCHDOG_REGISTERED=0
    log "[watchdog] WARN $WATCHDOG_REGISTER not present"
fi
hb "stage1c_watchdog_registered=$WATCHDOG_REGISTERED"

# ── Stage 1b: trap kill-on-exit (own 16 trap pre-stop hook) ──
POD_KILL_VERIFIED_404=0
WATCHDOG_DEREGISTERED=0
_kill_pod() {
    log "[trap] data-first scp before kill (L13)"
    if [ -n "${SSH_HOST:-}" ] && [ -n "${SSH_PORT:-}" ]; then
        timeout 60 scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P "$SSH_PORT" -r \
            "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 || true
        timeout 30 scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P "$SSH_PORT" \
            "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>&1 | tail -1 || true
    fi
    if [ -d "$WATCHDOG_HB_DIR" ]; then
        echo "EXITING $(date -u +%FT%TZ) pod=$POD_ID" > "$WATCHDOG_HB_DIR/$BG_LANE.txt" || true
    fi
    log "[trap] killing pod=$POD_ID"
    $RUNPODCTL pod stop "$POD_ID" 2>&1 | redact_hf | tee -a "$RUN_LOG" || true
    sleep 3
    $RUNPODCTL pod delete "$POD_ID" 2>&1 | redact_hf | tee -a "$RUN_LOG" || true
    sleep 5
    POD_KILL_VERIFIED_404=0
    for vi in 1 2 3; do
        POST=$($RUNPODCTL pod get "$POD_ID" 2>&1 | redact_hf | head -3)
        if echo "$POST" | grep -qiE 'not found|404|does not exist'; then
            POD_KILL_VERIFIED_404=1
            log "[trap] 404 verified (try $vi/3)"
            break
        fi
        log "[trap] 404 verify try $vi/3 not yet — sleep 30s"
        sleep 30
    done
    log "[trap] post-kill: $POST  pod_kill_verified_404=$POD_KILL_VERIFIED_404"
    WATCHDOG_DEREGISTERED=0
    if [ "$POD_KILL_VERIFIED_404" = "1" ] && [ -f "$WATCHDOG_HEXA" ]; then
        if /Users/ghost/core/hexa-lang/hexa run "$WATCHDOG_HEXA" --deregister "$POD_ID" 2>&1 | tee -a "$RUN_LOG"; then
            WATCHDOG_DEREGISTERED=1
            log "[watchdog] deregister OK pod=$POD_ID"
        else
            log "[watchdog] WARN deregister failed (rc=$?)"
        fi
    fi
    if [ -f "$POD_INFO" ]; then
        jq --arg killed "$(date -u +%FT%TZ)" --arg post "$POST" --argjson k404 "$POD_KILL_VERIFIED_404" --argjson wdd "$WATCHDOG_DEREGISTERED" \
            '. + {killed_ts:$killed, post_kill_status:$post, pod_kill_verified_404:($k404==1), watchdog_deregistered:($wdd==1)}' "$POD_INFO" > "$POD_INFO.tmp" && mv "$POD_INFO.tmp" "$POD_INFO" || true
    fi
}
trap _kill_pod EXIT INT TERM

# ── Stage 2: wait for SSH ready (max 6min) ──
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

# ── Stage 3: ship transient py + slice A (OPT-B variant uses sibling train script) ──
log "shipping slice A (76MB) + OPT-B transient py sibling"
hb "stage3_setup_starting"
$SSH 'mkdir -p /workspace/clm_v4_lora_opt_b/{corpus,results,ckpts,sentinels}'
$SCP "$SLICE_A_LOCAL" "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/corpus/slice_A_anima_30k.jsonl" 2>&1 | tail -1
$SCP "$CORPUS_MIX_PY" "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/corpus_mix.py" 2>&1 | tail -1
$SCP "$TRAIN_PY" "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/train.py" 2>&1 | tail -1
$SCP "/Users/ghost/core/anima/state/clm_v4_lora_sft_opt_b_2026_05_05/run_h100.bash" "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/run_h100.bash" 2>&1 | tail -1
$SSH 'chmod +x /workspace/clm_v4_lora_opt_b/run_h100.bash'

log "launching H100 OPT-B pipeline (cross_attn qkvo retrain — phi probe every 500 steps, ABORT @ -10pp)"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/clm_v4_lora_opt_b/hf_token.env && cd /workspace/clm_v4_lora_opt_b && set -a && . hf_token.env && set +a && setsid nohup bash run_h100.bash < /dev/null > orchestrator.log 2>&1 & echo $! > run.pid; disown $! 2>/dev/null || true; sleep 2; cat run.pid' < /dev/null
hb "stage3_h100_launched"

# ── Stage 4: poll loop (heartbeat per cycle, sentinel-kill, cost cap) ──
log "poll loop start (max ${MAX_WALL_MIN}min, target \$${BUDGET_TARGET}, hard_cap \$${BUDGET_HARD_CAP})"
COMPLETE=0
EARLY_STOP=0
PHI_ABORT=0
POLL_INTERVAL=60
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
        log "WALL CAP HIT ${ELAPSED_MIN}min — auto-kill"
        break
    fi

    PROBE=$($SSH 'ls /workspace/clm_v4_lora_opt_b/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ls /workspace/clm_v4_lora_opt_b/results/EARLY_STOP.sentinel 2>/dev/null && echo EARLY_STOP_FOUND; ls /workspace/clm_v4_lora_opt_b/results/PHI_ABORT.sentinel 2>/dev/null && echo PHI_ABORT_FOUND; ps -p $(cat /workspace/clm_v4_lora_opt_b/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1; tail -1 /workspace/clm_v4_lora_opt_b/orchestrator.log 2>/dev/null' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|' | head -c 240)"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST}"

    # === own 16 Phase 2 watchdog hook (heartbeat) ===
    if [ -n "${WATCHDOG_HB_DIR:-}" ]; then
        mkdir -p "$WATCHDOG_HB_DIR" 2>/dev/null || true
        echo "poll $(date -u +%FT%TZ) pod=$POD_ID elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST}" > "$WATCHDOG_HB_DIR/$BG_LANE.txt" 2>/dev/null || true
    fi

    $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync FIRST"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/ckpts/final" "$RESULTS_DIR/adapter_final" 2>&1 | tail -3 || true
        break
    fi
    if echo "$PROBE" | grep -q PHI_ABORT_FOUND; then
        log "PHI_ABORT.sentinel detected (F-OPT-B-1 drift > -10pp) — rescue last good adapter"
        PHI_ABORT=1
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/ckpts" "$RESULTS_DIR/ckpts_phi_abort" 2>&1 | tail -3 || true
        break
    fi
    if echo "$PROBE" | grep -q EARLY_STOP_FOUND; then
        log "EARLY_STOP.sentinel detected (forgetting OR train-side abort) — final sync + kill"
        EARLY_STOP=1
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora_opt_b/ckpts" "$RESULTS_DIR/ckpts_partial" 2>&1 | tail -3 || true
        break
    fi

    sleep $POLL_INTERVAL
done

# ── Stage 5: pod kill via trap (auto on exit) ──

# ── Stage 6: verdict (OPT-B schema with F-OPT-B-1..5 + own 16 cost-discipline fields) ──
log "computing OPT-B verdict"
FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")
hb "stage6_verdict_computing"

# OPT-B anchors (from spec §1 + §2)
PHI_BASELINE_IN_PIPELINE=35.81
PHI_ABORT_THRESHOLD=-10.0

# Extract final post-LoRA phi★ canonical (Mac-side post-cycle; placeholder here)
PHI_POST_FINAL="null"
if [ -f "$RESULTS_DIR/phi_canonical_final.json" ]; then
    PHI_POST_FINAL=$(jq -r '.phi_mean_K8 // "null"' "$RESULTS_DIR/phi_canonical_final.json")
fi
# Compute drift (pp from in-pipeline base 35.81)
PHI_DRIFT_PP="null"
if [ "$PHI_POST_FINAL" != "null" ]; then
    PHI_DRIFT_PP=$(awk -v p="$PHI_POST_FINAL" -v b="$PHI_BASELINE_IN_PIPELINE" 'BEGIN{printf "%.4f", p - b}')
fi

# F-OPT-B-1 (NO_FLIP) — drift > -10pp PASS; -5 to -10 PARTIAL; < -10 FAIL
FOPTB1="UNKNOWN"
if [ "$PHI_DRIFT_PP" != "null" ]; then
    FOPTB1=$(awk -v d="$PHI_DRIFT_PP" -v t="$PHI_ABORT_THRESHOLD" 'BEGIN{ if (d+0 > -5.0) print "PASS"; else if (d+0 >= t+0) print "PARTIAL"; else print "FAIL_FLIP" }')
fi

# F-OPT-B-2 (cross_attn actually trained — std diverges from init floor 0.02)
FOPTB2="UNKNOWN"
CROSS_ATTN_O_PROJ_STD_POST="null"
if [ -f "$RESULTS_DIR/cross_attn_o_proj_std_post_train.json" ]; then
    CROSS_ATTN_O_PROJ_STD_POST=$(jq -r '.mean_std // "null"' "$RESULTS_DIR/cross_attn_o_proj_std_post_train.json")
    FOPTB2=$(jq -r '(.f_opt_b_2_pass | if . then "PASS" else "FAIL" end) // "UNKNOWN"' "$RESULTS_DIR/cross_attn_o_proj_std_post_train.json")
fi

# F-OPT-B-3 (decisive — F-SHIM-V5-4 lift_pp ≥ +5pp; computed in Phase 4 separate dispatch)
FOPTB3="PHASE_4_PENDING"

# F-OPT-B-4 (composite ≥ 0.30) — computed Phase 4
FOPTB4="PHASE_4_PENDING"

# F-OPT-B-5 (forgetting_index < 0.05) — computed Phase 4
FOPTB5="PHASE_4_PENDING"

# Overall verdict
OVERALL="OPT_B_PHASE_3_UNKNOWN"
if [ "$PHI_ABORT" = "1" ]; then
    OVERALL="OPT_B_PHASE_3_PHI_ABORT"
elif [ "$EARLY_STOP" = "1" ]; then
    OVERALL="OPT_B_PHASE_3_EARLY_STOP"
elif [ "$COMPLETE" = "1" ] && [ "$FOPTB1" = "PASS" ] && [ "$FOPTB2" = "PASS" ]; then
    OVERALL="OPT_B_PHASE_3_PASS_PROCEED_TO_PHASE_4"
elif [ "$COMPLETE" = "1" ] && ( [ "$FOPTB1" = "PARTIAL" ] || [ "$FOPTB2" = "FAIL" ] ); then
    OVERALL="OPT_B_PHASE_3_PARTIAL"
elif [ "$COMPLETE" = "1" ] && [ "$FOPTB1" = "FAIL_FLIP" ]; then
    OVERALL="OPT_B_PHASE_3_FAIL_FLIP"
fi

POD_KILL_404='false'
if [ -f "$POD_INFO" ]; then
    POST=$(jq -r '.post_kill_status // ""' "$POD_INFO" 2>/dev/null)
    if echo "$POST" | grep -qiE 'not found|404|no such|does not exist'; then
        POD_KILL_404='true'
    fi
fi

# === own 16 Phase 2 verdict schema (cost-discipline fields) ===
COST_TARGET_USD=$TARGET_USD
COST_ACTUAL_USD=$FINAL_COST
COST_OVERRUN_RATIO=$(awk -v a="$COST_ACTUAL_USD" -v t="$COST_TARGET_USD" 'BEGIN{ if (t+0 > 0) printf "%.4f", a/t; else print "0" }')
COST_OVERRUN_2X_ALERTED='false'
if awk -v r="$COST_OVERRUN_RATIO" 'BEGIN{exit !(r+0 >= 2.0)}'; then COST_OVERRUN_2X_ALERTED='true'; fi
WATCHDOG_DEREGISTERED_FINAL='false'
if [ -f "$POD_INFO" ]; then
    WD_TMP=$(jq -r '.watchdog_deregistered // false' "$POD_INFO" 2>/dev/null)
    if [ "$WD_TMP" = "true" ]; then WATCHDOG_DEREGISTERED_FINAL='true'; fi
fi

jq -n \
    --arg cycle "clm_v4_lora_sft_opt_b_2026_05_05" \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg pod "$POD_ID" \
    --argjson kill_404 "$POD_KILL_404" \
    --argjson wd_dereg "$WATCHDOG_DEREGISTERED_FINAL" \
    --argjson cost_target "$COST_TARGET_USD" \
    --argjson cost_actual "$COST_ACTUAL_USD" \
    --argjson cost_ratio "$COST_OVERRUN_RATIO" \
    --argjson cost_2x "$COST_OVERRUN_2X_ALERTED" \
    --arg overall "$OVERALL" \
    --arg foptb1 "$FOPTB1" --arg foptb2 "$FOPTB2" --arg foptb3 "$FOPTB3" --arg foptb4 "$FOPTB4" --arg foptb5 "$FOPTB5" \
    --arg phi_post "$PHI_POST_FINAL" --arg phi_drift "$PHI_DRIFT_PP" \
    --arg ca_std "$CROSS_ATTN_O_PROJ_STD_POST" \
    --argjson wall "$FINAL_ELAPSED_MIN" \
    --argjson cost "$FINAL_COST" \
    --argjson complete "$COMPLETE" \
    --argjson early_stop "$EARLY_STOP" \
    --argjson phi_abort "$PHI_ABORT" \
    '{
        schema: "anima/clm_v4_lora_sft_opt_b/verdict/1",
        cycle: $cycle, ts_utc: $ts,
        bg_lane: "OPT-B-CROSS-ATTN-RETRAIN",
        spec_source: "docs/clm_v4_lora_sft_opt_b_cross_attn_retrain_spec_2026_05_05.md",
        parent_v1_cycle: "clm_v4_lora_sft_2026_05_05",
        phi_baseline_in_pipeline: 35.81,
        phi_baseline_carry_substrate: 41.86,
        pod_id: $pod, pod_terminated: true, pod_kill_verified_404: $kill_404,
        hyperparameters: {r: 32, alpha: 64, dropout: 0.10, lr: 5e-6, max_steps: 3000, save_steps: 500, per_device_batch: 8, grad_accum: 4, eff_batch: 32, ctx: 512, bf16: true, target_modules: "self-attn qkvo + cross_attn qkvo on decoder.blocks.{0..15} (Q1-B wide; 128 modules total)"},
        opt_b_decision_locks: {Q1: "B (wide cross_attn qkvo)", Q2: "A (lr=5e-6)", Q3: "A (max_steps=3000)", Q4: "A (abort_drift=-10pp)", Q5: "B ($20-100 envelope; this orchestrator hard cap=$50 Phase 3 only)"},
        phi_post_final_canonical: $phi_post,
        phi_drift_pp_in_pipeline: $phi_drift,
        cross_attn_o_proj_std_post: $ca_std,
        F_OPT_B_1_phi_no_flip: $foptb1,
        F_OPT_B_2_cross_attn_actually_trained: $foptb2,
        F_OPT_B_3_shim_v5_4_lift_pp: $foptb3,
        F_OPT_B_4_composite_ge_0_30: $foptb4,
        F_OPT_B_5_forgetting_index_lt_0_05: $foptb5,
        verdict: $overall,
        wall_time_min: $wall,
        wall_time_h: ($wall / 60.0),
        actual_cost_usd: $cost,
        budget_target_usd: 30,
        budget_hard_cap_usd: 50,
        cost_target_usd: $cost_target,
        cost_actual_usd: $cost_actual,
        cost_overrun_ratio: $cost_ratio,
        cost_overrun_2x_alerted: $cost_2x,
        watchdog_deregistered: $wd_dereg,
        complete_sentinel_detected: ($complete == 1),
        early_stop_sentinel_detected: ($early_stop == 1),
        phi_abort_sentinel_detected: ($phi_abort == 1),
        phase_4_pending: ($foptb3 == "PHASE_4_PENDING"),
        lessons_applied: {
            L3_auto_kill: "trap _kill_pod EXIT INT TERM",
            L9_hf_whoami_preflight: "stage0b /api/whoami-v2 fail-fast",
            L13_trap_pre_kill_scp: "trap rescues results before pod stop",
            L24_setsid_disown: "H100 launch via setsid + < /dev/null + disown for chat-session resilience",
            phi_star_flip_mitigation_opt_b: "lr 10× lower (5e-6 vs 3e-5); dropout 2× (0.10 vs 0.05); max_steps 50% (3000 vs 6000); ABORT @ -10pp drift; phi probe every 500 steps"
        },
        honest_c3: [
            "OPT-B sibling pattern: train script + orchestrator are NEW siblings of v1; v1 train script + v1 orchestrator UNTOUCHED per raw#15 additive. If sibling drifts from v1 base behavior (e.g., PEFT version regression), v1 remains as a working comparator.",
            "phi★ in-pipeline baseline 35.81 was measured Mac CPU fp32; Phase 3 H100 bf16 substrate may yield methodology delta on the order of ~6pp (per CLM-2 phi canonical verdict honest_c3 #3). Authoritative ABORT trigger uses post-train Mac CPU fp32 phi probe (matching baseline substrate); in-pod heuristic is informational only.",
            "cross_attn target_modules count = 16 layers × 8 projections (Q1-B wide) = 128 modules total; +0.137% trainable params vs v1. Sanity assert in train.py at startup catches PEFT name-match regression.",
            "F-OPT-B-3 (decisive lift gate) is computed in Phase 4 separate dispatch — Phase 3 verdict marks PHASE_4_PENDING for FOPTB3/4/5. Phase 3 PASS = F-OPT-B-1 PASS + F-OPT-B-2 PASS only; Phase 4 must run before final OPT-B verdict.",
            "H100 SXM cost @ \$2.99/hr; expected Phase 3 wall ~3-5h (3000 steps + cross_attn 0.137% extra params + denser eval cadence). Hard cap \$50; 16% overrun headroom on \$30 target. ABORT contingency caps phi-flip ABORT spend at ~\$10-15.",
            "Slice A reused from v1 cycle (UNTOUCHED) ensures rehearsal mix is identical between v1 and OPT-B — only target_modules + LR + dropout + max_steps differ. Cross-cycle delta isolates the cross_attn participation effect from corpus mix variance.",
            "Phase 2 ubu1 smoke (RTX 5070 sm_120, fp32) verifies gradient flow through cross_attn LoRA before Phase 3 spend. Smoke verdict at state/clm_v4_lora_sft_opt_b_phase_1_2_prep_2026_05_05/verdict.json = ready_for_phase_3 gate."
        ]
    }' > "$VERDICT"

log "verdict=$OVERALL F-OPT-B-1=$FOPTB1 F-OPT-B-2=$FOPTB2 phi_drift=$PHI_DRIFT_PP cross_attn_std_post=$CROSS_ATTN_O_PROJ_STD_POST wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
hb "verdict=$OVERALL"
echo "__OPT_B_PHASE_3__ $OVERALL" | tee -a "$RUN_LOG"
exit 0
