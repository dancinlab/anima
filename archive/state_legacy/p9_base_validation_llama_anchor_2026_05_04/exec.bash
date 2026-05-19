#!/bin/bash
# emitted by tool/p9_llama_anchor_h100_orchestrator.hexa — Llama anchor lifecycle
# raw#9 sibling-pattern Mac-side bash. Regenerate via --emit. raw#37 H100 transient py.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/p9_base_validation_llama_anchor_2026_05_04'
RESULTS_DIR='/Users/ghost/core/anima/state/p9_base_validation_llama_anchor_2026_05_04/results'
POD_INFO='/Users/ghost/core/anima/state/p9_base_validation_llama_anchor_2026_05_04/pod_info.json'
VERDICT='/Users/ghost/core/anima/state/p9_base_validation_llama_anchor_2026_05_04/verdict.json'
RUN_LOG='/Users/ghost/core/anima/state/p9_base_validation_llama_anchor_2026_05_04/run.log'
HEARTBEAT='/Users/ghost/core/anima/state/p9_base_validation_llama_anchor_2026_05_04/heartbeat.txt'
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
RUNPODCTL='/opt/homebrew/bin/runpodctl'
MAX_WALL_MIN=45
BUDGET_HARD_CAP=2.5
OD_RATE=2.99
START_EPOCH=$(date -u +%s)

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }
hb()  { echo "[$(date -u +%FT%TZ)] $*" > "$HEARTBEAT"; }
redact_hf() { sed -E 's/(HF_TOKEN["[:space:]]*[:=]["[:space:]]*)hf_[A-Za-z0-9_]+/\1<REDACTED>/g; s/(hf_)[A-Za-z0-9_]{20,}/\1<REDACTED>/g'; }

# ── Stage 0: secrets (use --raw to bypass new claude-redaction wrapper) ──
export RUNPOD_API_KEY=$(secret get --raw runpod.api_key 2>/dev/null)
export HF_TOKEN_LOCAL=$(secret get --raw huggingface.token 2>/dev/null)
if [ -z "${RUNPOD_API_KEY:-}" ] || [ -z "${HF_TOKEN_LOCAL:-}" ]; then
    log "FATAL: secrets unavailable"
    exit 2
fi
# Sanity: redacted form starts with '***' — refuse to proceed if we got that
if [[ "$RUNPOD_API_KEY" == \*\*\** ]] || [[ "$HF_TOKEN_LOCAL" == \*\*\** ]]; then
    log "FATAL: secret returned redacted form despite --raw — wrapper broken"
    exit 2
fi
log "secrets OK (runpod=${#RUNPOD_API_KEY}b, hf=${#HF_TOKEN_LOCAL}b)"
hb "stage0_secrets_loaded"

# ── Stage 1: boot H100 pod (sed redact at boot, BEFORE tee — lesson L5) ──
POD_NAME='anima-p9-llama-anchor-2026-05-04'
log "booting pod=$POD_NAME (H100 80GB HBM3 secure on-demand @ \$$OD_RATE/hr)"
BOOT_RAW_OUT="$STATE_DIR/boot.raw.tmp"
BOOT_OUT="$STATE_DIR/boot.log"
hb "stage1_booting_pod"
# Capture stdout+stderr to temp, redact, tee to boot.log, delete raw temp.
$RUNPODCTL pod create \
    --name "$POD_NAME" \
    --gpu-id 'NVIDIA H100 80GB HBM3' \
    --gpu-count 1 \
    --image 'runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04' \
    --container-disk-in-gb 60 \
    --volume-in-gb 30 \
    --volume-mount-path /workspace \
    --ports '22/tcp,8888/http' \
    --cloud-type SECURE \
    --ssh \
    --env "{\"HF_TOKEN\":\"$HF_TOKEN_LOCAL\"}" \
    > "$BOOT_RAW_OUT" 2>&1
BOOT_RC=$?
# Redact BEFORE writing to long-lived log. Then delete raw.
redact_hf < "$BOOT_RAW_OUT" > "$BOOT_OUT"
rm -f "$BOOT_RAW_OUT"
if [ $BOOT_RC -ne 0 ]; then
    log "FATAL: pod boot failed rc=$BOOT_RC"
    cat "$BOOT_OUT" | redact_hf | tee -a "$RUN_LOG"
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed" '{cycle:"p9_base_validation_llama_anchor_2026_05_04",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
    exit 3
fi
# Extract pod_id (runpodctl create pod prints e.g. 'pod "abc1234567890" created for ...')
POD_ID=$(grep -oE '"[a-z0-9]{14}"' "$BOOT_OUT" | head -1 | tr -d '"')
if [ -z "$POD_ID" ]; then
    POD_ID=$(grep -oE 'pod [a-z0-9]{12,16}' "$BOOT_OUT" | head -1 | awk '{print $2}')
fi
if [ -z "$POD_ID" ]; then
    log "FATAL: cannot extract pod_id"
    cat "$BOOT_OUT"
    exit 4
fi
log "pod_id=$POD_ID"
echo '{"pod_id":"'$POD_ID'","booted_ts":"'$(date -u +%FT%TZ)'"}' > "$POD_INFO"
hb "stage1_pod_booted pod_id=$POD_ID"

# ── Stage 1b: kill-on-exit trap MANDATORY ──
_kill_pod() {
    log "[trap] killing pod=$POD_ID (auto-kill mandatory)"
    $RUNPODCTL pod stop "$POD_ID" 2>&1 | tee -a "$RUN_LOG" || true
    sleep 3
    $RUNPODCTL pod delete "$POD_ID" 2>&1 | tee -a "$RUN_LOG" || true
    sleep 3
    POST=$($RUNPODCTL pod get "$POD_ID" 2>&1 | head -3)
    log "[trap] post-kill: $POST"
    if [ -f "$POD_INFO" ]; then
        jq --arg killed "$(date -u +%FT%TZ)" --arg post "$POST" \
            '. + {killed_ts:$killed, post_kill_status:$post}' "$POD_INFO" > "$POD_INFO.tmp" && mv "$POD_INFO.tmp" "$POD_INFO" || true
    fi
}
trap _kill_pod EXIT INT TERM

# ── Stage 2: wait for SSH (max 6min) — uses `runpodctl pod get -o json` ──
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

# ── Stage 3: setup pod (skip CLM, only Llama) — lesson L2 ──
log "setup: install lm-eval + download Llama-3.2-3B (~3-5min on H100 datacenter network)"
hb "stage3_setup_starting"
$SSH 'mkdir -p /workspace/p9_llama_anchor/results'
$SCP "/Users/ghost/core/anima/state/p9_base_validation_llama_anchor_2026_05_04/run_h100.bash" "root@$SSH_HOST:/workspace/p9_llama_anchor/run_h100.bash" 2>&1 | tail -1
$SSH 'chmod +x /workspace/p9_llama_anchor/run_h100.bash'

# Launch detached. Source HF_TOKEN from /proc/1/environ (runpodctl --env injects to PID1 only,
# not into ssh shell sessions). raw#9 — setting envvars on remote pod is not Mac-side .py.
log "launching benchmark suite on H100"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/p9_llama_anchor/hf_token.env && cd /workspace/p9_llama_anchor && set -a && . hf_token.env && set +a && nohup bash run_h100.bash > orchestrator.log 2>&1 & echo $! > run.pid; disown $! 2>/dev/null || true; sleep 2; cat run.pid'
hb "stage3_h100_launched"

# ── Stage 4: poll loop (heartbeat each cycle, lesson L4) ──
log "poll loop start (max ${MAX_WALL_MIN}min, budget cap \$${BUDGET_HARD_CAP})"
COMPLETE=0
POLL_INTERVAL=120  # 2-min poll for snappy auto-kill (lesson L3)
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

    PROBE=$($SSH 'ls /workspace/p9_llama_anchor/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ps -p $(cat /workspace/p9_llama_anchor/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|')"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|' | head -c 200)"

    # incremental sync (small JSONs only)
    $SCP -r "root@$SSH_HOST:/workspace/p9_llama_anchor/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/p9_llama_anchor/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync + auto-kill imminent"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/p9_llama_anchor/results/*" "$RESULTS_DIR/" 2>&1 | tail -3 | tee -a "$RUN_LOG" || true
        $SCP "root@$SSH_HOST:/workspace/p9_llama_anchor/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>&1 | tail -1 || true
        break
    fi

    sleep $POLL_INTERVAL
done

# ── Stage 5: pod kill via trap (auto on exit) ──
# Note: trap _kill_pod will fire when this script exits. Lesson L3: within 30s.

# ── Stage 6: verdict (per-bench numeric extraction + ±10% gate) ──
log "computing verdict from per-bench JSONs"
FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")
hb "stage6_verdict_computing"

BENCH_COUNT=$(ls $RESULTS_DIR/llama_*.json 2>/dev/null | wc -l | awk '{print $1}')

# Build verdict.json via inline python (raw#37 transient on Mac is BANNED — use jq)
# We use jq + awk only.

# Extract metrics (best-effort; lm-eval-harness JSON shape: .results.<task>.<metric>)
HS_ACC="null"; HS_NORM="null"; HS_STDERR="null"
if [ -f "$RESULTS_DIR/llama_hellaswag.json" ]; then
    HS_ACC=$(jq -r '.results.hellaswag."acc,none" // .results.hellaswag.acc // "null"' "$RESULTS_DIR/llama_hellaswag.json")
    HS_NORM=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' "$RESULTS_DIR/llama_hellaswag.json")
    HS_STDERR=$(jq -r '.results.hellaswag."acc_norm_stderr,none" // .results.hellaswag.acc_norm_stderr // "null"' "$RESULTS_DIR/llama_hellaswag.json")
fi
MM_ACC="null"; MM_STDERR="null"
if [ -f "$RESULTS_DIR/llama_mmlu.json" ]; then
    MM_ACC=$(jq -r '.results.mmlu."acc,none" // .results.mmlu.acc // "null"' "$RESULTS_DIR/llama_mmlu.json")
    MM_STDERR=$(jq -r '.results.mmlu."acc_stderr,none" // .results.mmlu.acc_stderr // "null"' "$RESULTS_DIR/llama_mmlu.json")
fi
TQ_EM="null"; TQ_STDERR="null"
if [ -f "$RESULTS_DIR/llama_triviaqa.json" ]; then
    TQ_EM=$(jq -r '.results.triviaqa."exact_match,remove_whitespace" // .results.triviaqa."exact_match,none" // .results.triviaqa.exact_match // "null"' "$RESULTS_DIR/llama_triviaqa.json")
    TQ_STDERR=$(jq -r '.results.triviaqa."exact_match_stderr,remove_whitespace" // .results.triviaqa."exact_match_stderr,none" // .results.triviaqa.exact_match_stderr // "null"' "$RESULTS_DIR/llama_triviaqa.json")
fi

# ±10% bands vs published mid-range
# HellaSwag mid 0.704 → [0.634, 0.774]; MMLU 5-shot mid 0.555 → [0.500, 0.611]; TriviaQA mid 0.275 → [0.248, 0.303]
check_band() {
    local val=$1; local lo=$2; local hi=$3
    if [ "$val" = "null" ]; then echo "MISSING"; return; fi
    awk "BEGIN{ if ($val >= $lo && $val <= $hi) print \"PASS\"; else print \"FAIL\" }"
}
HS_GATE=$(check_band "$HS_NORM" 0.634 0.774)
MM_GATE=$(check_band "$MM_ACC" 0.500 0.611)
TQ_GATE=$(check_band "$TQ_EM" 0.248 0.303)

# Overall verdict
PASS_COUNT=0
for g in $HS_GATE $MM_GATE $TQ_GATE; do
    [ "$g" = "PASS" ] && PASS_COUNT=$((PASS_COUNT+1))
done

VERDICT_LABEL='FAIL'
C1='FAIL'
C2='FAIL'
if [ "$BENCH_COUNT" -ge 3 ] && [ "$COMPLETE" = "1" ]; then
    C1='PASS'
fi
if [ "$PASS_COUNT" -ge 2 ]; then
    C2='PASS'
fi
if [ "$C1" = "PASS" ] && [ "$C2" = "PASS" ]; then
    VERDICT_LABEL='PASS'
elif [ "$C1" = "PASS" ]; then
    VERDICT_LABEL='PARTIAL'
fi

jq -n \
    --arg cycle "p9_base_validation_llama_anchor_2026_05_04" \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg pod "$POD_ID" \
    --arg verdict "$VERDICT_LABEL" \
    --arg c1 "$C1" \
    --arg c2 "$C2" \
    --arg hs_norm "$HS_NORM" --arg hs_acc "$HS_ACC" --arg hs_se "$HS_STDERR" --arg hs_gate "$HS_GATE" \
    --arg mm_acc "$MM_ACC" --arg mm_se "$MM_STDERR" --arg mm_gate "$MM_GATE" \
    --arg tq_em "$TQ_EM" --arg tq_se "$TQ_STDERR" --arg tq_gate "$TQ_GATE" \
    --argjson wall "$FINAL_ELAPSED_MIN" \
    --argjson cost "$FINAL_COST" \
    --argjson n "$BENCH_COUNT" \
    --argjson complete "$COMPLETE" \
    '{
        cycle: $cycle, ts_utc: $ts, pod_id: $pod,
        model: "meta-llama/Llama-3.2-3B",
        scope: "Mode 2 anchor — stock lm-eval-harness, no shim, limit=500, batch_size=16, seed=42, num_fewshot=5 (mmlu only; hellaswag/triviaqa 0-shot per spec convention)",
        verdict: $verdict,
        f1_v3_amended_criterion_1_anchors_run: $c1,
        f1_v3_amended_criterion_2_llama_within_pm10pct: $c2,
        results_per_benchmark: {
            hellaswag: {acc: $hs_acc, acc_norm: $hs_norm, stderr: $hs_se, vs_published_band: "[0.634, 0.774]", gate: $hs_gate},
            mmlu:      {acc: $mm_acc, stderr: $mm_se, vs_published_band: "[0.500, 0.611]", gate: $mm_gate, fewshot: 5},
            triviaqa:  {exact_match: $tq_em, stderr: $tq_se, vs_published_band: "[0.248, 0.303]", gate: $tq_gate}
        },
        bench_count_completed: $n,
        complete_sentinel_detected: ($complete == 1),
        wall_time_min: $wall,
        actual_cost_usd: $cost,
        honest_c3: [
            "limit=500 ⇒ stderr ~2pp; published bands ±10% may need widening if at edge",
            "MMLU 5-shot only; HellaSwag/TriviaQA reported 0-shot per harness convention (spec text said 5-shot for all but harness convention overrides)",
            "H100 bfloat16 ⇒ slight numeric drift vs fp32 published numbers (typically <0.5pp)",
            "Llama-3.2-3B base; instruct variants will differ",
            "Single seed (42); per-prompt variance not characterized"
        ]
    }' > "$VERDICT"

log "verdict=$VERDICT_LABEL c1=$C1 c2=$C2 wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
log "hellaswag_acc_norm=$HS_NORM (gate=$HS_GATE)  mmlu_acc=$MM_ACC (gate=$MM_GATE)  triviaqa_em=$TQ_EM (gate=$TQ_GATE)"
hb "verdict=$VERDICT_LABEL c1=$C1 c2=$C2"
echo "__P9_LLAMA_ANCHOR_BASE_VAL__ $VERDICT_LABEL" | tee -a "$RUN_LOG"
exit 0
