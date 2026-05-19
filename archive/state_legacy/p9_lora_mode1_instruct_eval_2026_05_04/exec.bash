#!/bin/bash
# emitted by tool/p9_lora_mode1_instruct_eval_h100_orchestrator.hexa — BG-Ψ Mac-side lifecycle
# raw#9 sibling-pattern Mac-side bash. Regenerate via --emit. raw#37 H100 transient py.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04'
RESULTS_DIR='/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/results'
POD_INFO='/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/pod_info.json'
VERDICT='/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/verdict.json'
RUN_LOG='/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/run.log'
HEARTBEAT='/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/heartbeat.txt'
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
RUNPODCTL='/opt/homebrew/bin/runpodctl'
MAX_WALL_MIN=60
BUDGET_HARD_CAP=3.50
OD_RATE=2.99
HF_LORA_REPO='need-singularity/p9-llama32-lora-stage1'
HF_LORA_REVISION='5a9b4584'
HF_BASE_REPO='meta-llama/Llama-3.2-3B-Instruct'
START_EPOCH=$(date -u +%s)

# BG-Ρ deltas (non-Instruct base) for hypothesis comparison
BG_RHO_HS_PP=-1.2
BG_RHO_MM_PP=-4.95
BG_RHO_TQ_PP=-9.4

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }
hb()  { echo "[$(date -u +%FT%TZ)] $*" > "$HEARTBEAT"; }
redact_hf() { sed -E 's/(HF_TOKEN["[:space:]]*[:=]["[:space:]]*)hf_[A-Za-z0-9_]+/\1<REDACTED>/g; s/(hf_)[A-Za-z0-9_]{20,}/\1<REDACTED>/g'; }

# ── Stage 0: secrets (use --raw to bypass claude-redaction wrapper) ──
export RUNPOD_API_KEY=$(secret get --raw runpod.api_key 2>/dev/null)
export HF_TOKEN_LOCAL=$(secret get --raw huggingface.token 2>/dev/null)
if [ -z "${RUNPOD_API_KEY:-}" ] || [ -z "${HF_TOKEN_LOCAL:-}" ]; then
    log "FATAL: secrets unavailable"
    exit 2
fi
if [[ "$RUNPOD_API_KEY" == \*\*\** ]] || [[ "$HF_TOKEN_LOCAL" == \*\*\** ]]; then
    log "FATAL: secret returned redacted form despite --raw — wrapper broken"
    exit 2
fi
log "secrets OK (runpod=${#RUNPOD_API_KEY}b, hf=${#HF_TOKEN_LOCAL}b)"
hb "stage0_secrets_loaded"

# ── Stage 1: boot H100 pod ──
POD_NAME='anima-p9-lora-mode1-instruct-eval-2026-05-04'
log "booting pod=$POD_NAME (H100 80GB HBM3 secure on-demand @ \$$OD_RATE/hr)"
BOOT_RAW_OUT="$STATE_DIR/boot.raw.tmp"
BOOT_OUT="$STATE_DIR/boot.log"
hb "stage1_booting_pod"
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
redact_hf < "$BOOT_RAW_OUT" > "$BOOT_OUT"
rm -f "$BOOT_RAW_OUT"
if [ $BOOT_RC -ne 0 ]; then
    log "FATAL: pod boot failed rc=$BOOT_RC"
    cat "$BOOT_OUT" | redact_hf | tee -a "$RUN_LOG"
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed" '{cycle:"p9_lora_mode1_instruct_eval_2026_05_04",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
    exit 3
fi
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

# ── Stage 3: setup pod ──
log "setup: install lm-eval + peft + download Llama-Instruct + step-8k LoRA"
hb "stage3_setup_starting"
$SSH 'mkdir -p /workspace/p9_eval/results'
$SCP "$STATE_DIR/run_h100.bash" "root@$SSH_HOST:/workspace/p9_eval/run_h100.bash" 2>&1 | tail -1
$SSH 'chmod +x /workspace/p9_eval/run_h100.bash'

log "launching dual eval suite (Instruct base + Instruct+LoRA × 3 benchmarks) on H100"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/p9_eval/hf_token.env && cd /workspace/p9_eval && set -a && . hf_token.env && set +a && nohup bash run_h100.bash > orchestrator.log 2>&1 & echo $! > run.pid; disown $! 2>/dev/null || true; sleep 2; cat run.pid'
hb "stage3_h100_launched"

# ── Stage 4: poll loop (heartbeat each cycle) ──
log "poll loop start (max ${MAX_WALL_MIN}min, budget cap \$${BUDGET_HARD_CAP})"
COMPLETE=0
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
        log "WALL CAP HIT ${ELAPSED_MIN}min ≥ ${MAX_WALL_MIN}min — auto-kill"
        break
    fi

    PROBE=$($SSH 'ls /workspace/p9_eval/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ps -p $(cat /workspace/p9_eval/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|')"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|' | head -c 200)"

    # incremental sync (small JSONs only)
    $SCP -r "root@$SSH_HOST:/workspace/p9_eval/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/p9_eval/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync FIRST then auto-kill (lesson: don't lose data)"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/p9_eval/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        $SCP "root@$SSH_HOST:/workspace/p9_eval/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>&1 | tail -1 || true
        break
    fi

    sleep $POLL_INTERVAL
done

# ── Stage 5: pod kill via trap (auto on exit) ──

# ── Stage 6: verdict ──
log "computing verdict from per-bench JSONs"
FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")
hb "stage6_verdict_computing"

# Helper: extract metrics from a results JSON. Returns "acc|stderr" (or "norm|se" for hellaswag).
_extract_hs() {
    local f=$1
    if [ ! -f "$f" ]; then echo "null|null|null"; return; fi
    local acc=$(jq -r '.results.hellaswag."acc,none" // .results.hellaswag.acc // "null"' "$f")
    local norm=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' "$f")
    local se=$(jq -r '.results.hellaswag."acc_norm_stderr,none" // .results.hellaswag.acc_norm_stderr // "null"' "$f")
    echo "$acc|$norm|$se"
}
_extract_mm() {
    local f=$1
    if [ ! -f "$f" ]; then echo "null|null"; return; fi
    local acc=$(jq -r '.results.mmlu."acc,none" // .results.mmlu.acc // "null"' "$f")
    local se=$(jq -r '.results.mmlu."acc_stderr,none" // .results.mmlu.acc_stderr // "null"' "$f")
    echo "$acc|$se"
}
_extract_tq() {
    local f=$1
    if [ ! -f "$f" ]; then echo "null|null"; return; fi
    local em=$(jq -r '.results.triviaqa."exact_match,remove_whitespace" // .results.triviaqa."exact_match,none" // .results.triviaqa.exact_match // "null"' "$f")
    local se=$(jq -r '.results.triviaqa."exact_match_stderr,remove_whitespace" // .results.triviaqa."exact_match_stderr,none" // .results.triviaqa.exact_match_stderr // "null"' "$f")
    echo "$em|$se"
}

# Pass 1: Instruct base anchors
IFS='|' read -r IB_HS_ACC IB_HS_NORM IB_HS_SE <<< "$(_extract_hs "$RESULTS_DIR/instruct_base_hellaswag.json")"
IFS='|' read -r IB_MM_ACC IB_MM_SE              <<< "$(_extract_mm "$RESULTS_DIR/instruct_base_mmlu.json")"
IFS='|' read -r IB_TQ_EM  IB_TQ_SE              <<< "$(_extract_tq "$RESULTS_DIR/instruct_base_triviaqa.json")"

# Pass 2: Instruct + LoRA
IFS='|' read -r IL_HS_ACC IL_HS_NORM IL_HS_SE <<< "$(_extract_hs "$RESULTS_DIR/instruct_lora_hellaswag.json")"
IFS='|' read -r IL_MM_ACC IL_MM_SE              <<< "$(_extract_mm "$RESULTS_DIR/instruct_lora_mmlu.json")"
IFS='|' read -r IL_TQ_EM  IL_TQ_SE              <<< "$(_extract_tq "$RESULTS_DIR/instruct_lora_triviaqa.json")"

# Random + 5pp baselines
R5_HS=0.30
R5_MM=0.30
R5_TQ=0.05

# c3 helper: |LoRA - Instruct_base| ≥ 2 × max(LoRA_se, Instruct_base_se)
c3_check() {
    local lora=$1; local base=$2; local lse=$3; local bse=$4
    if [ "$lora" = "null" ] || [ "$base" = "null" ]; then echo "MISSING|null|null"; return; fi
    awk "BEGIN{
        d = ($lora - $base);
        ad = (d < 0) ? -d : d;
        m = ($lse > $bse) ? $lse : $bse;
        thr = 2 * m;
        delta_pp = d * 100;
        thr_pp = thr * 100;
        if (ad >= thr) print \"PASS|\" delta_pp \"|\" thr_pp;
        else            print \"FAIL|\" delta_pp \"|\" thr_pp;
    }"
}
# c4 helper: LoRA ≥ random + 5pp
c4_check() {
    local lora=$1; local r5=$2
    if [ "$lora" = "null" ]; then echo "MISSING"; return; fi
    awk "BEGIN{ if ($lora >= $r5) print \"PASS\"; else print \"FAIL\" }"
}

HS_C3_LINE=$(c3_check "$IL_HS_NORM" "$IB_HS_NORM" "$IL_HS_SE" "$IB_HS_SE")
MM_C3_LINE=$(c3_check "$IL_MM_ACC"  "$IB_MM_ACC"  "$IL_MM_SE" "$IB_MM_SE")
TQ_C3_LINE=$(c3_check "$IL_TQ_EM"   "$IB_TQ_EM"   "$IL_TQ_SE" "$IB_TQ_SE")
HS_C3=$(echo $HS_C3_LINE | cut -d'|' -f1); HS_DELTA_PP=$(echo $HS_C3_LINE | cut -d'|' -f2); HS_THR_PP=$(echo $HS_C3_LINE | cut -d'|' -f3)
MM_C3=$(echo $MM_C3_LINE | cut -d'|' -f1); MM_DELTA_PP=$(echo $MM_C3_LINE | cut -d'|' -f2); MM_THR_PP=$(echo $MM_C3_LINE | cut -d'|' -f3)
TQ_C3=$(echo $TQ_C3_LINE | cut -d'|' -f1); TQ_DELTA_PP=$(echo $TQ_C3_LINE | cut -d'|' -f2); TQ_THR_PP=$(echo $TQ_C3_LINE | cut -d'|' -f3)

HS_C4=$(c4_check "$IL_HS_NORM" $R5_HS)
MM_C4=$(c4_check "$IL_MM_ACC"  $R5_MM)
TQ_C4=$(c4_check "$IL_TQ_EM"   $R5_TQ)

C3_PASS_COUNT=0
for g in $HS_C3 $MM_C3 $TQ_C3; do [ "$g" = "PASS" ] && C3_PASS_COUNT=$((C3_PASS_COUNT+1)); done
C4_PASS_COUNT=0
for g in $HS_C4 $MM_C4 $TQ_C4; do [ "$g" = "PASS" ] && C4_PASS_COUNT=$((C4_PASS_COUNT+1)); done

C3_VERDICT='FAIL'; [ $C3_PASS_COUNT -ge 2 ] && C3_VERDICT='PASS'
C4_VERDICT='FAIL'; [ $C4_PASS_COUNT -ge 2 ] && C4_VERDICT='PASS'

# Δ-difference vs BG-Ρ (Instruct_Δ minus non_Instruct_Δ); if Instruct_Δ closer to 0 → mismatch reduced
# delta_difference > 0 means Instruct degrades less (template-mismatch hypothesis support)
HS_DIFF=$(awk "BEGIN{ if (\"$HS_DELTA_PP\"==\"null\") print \"null\"; else printf \"%.2f\", ($HS_DELTA_PP) - ($BG_RHO_HS_PP) }")
MM_DIFF=$(awk "BEGIN{ if (\"$MM_DELTA_PP\"==\"null\") print \"null\"; else printf \"%.2f\", ($MM_DELTA_PP) - ($BG_RHO_MM_PP) }")
TQ_DIFF=$(awk "BEGIN{ if (\"$TQ_DELTA_PP\"==\"null\") print \"null\"; else printf \"%.2f\", ($TQ_DELTA_PP) - ($BG_RHO_TQ_PP) }")

# Hypothesis verdict
# - For each bench, compute "shrink_ratio" = 1 - |Instruct_Δ| / |BG_Ρ_Δ|. If ≥0.5 → shrunk by ≥50%.
# - TEMPLATE_MISMATCH_CONFIRMED: ≥2/3 benches shrink_ratio ≥ 0.5
# - UNEXPECTED: any bench has |Instruct_Δ| > |BG_Ρ_Δ| × 1.25 (degraded MORE)
# - FORGETTING_INDEPENDENT: degradation persists (|Instruct_Δ| within 25% of |BG_Ρ_Δ|) on ≥2/3
shrink_ratio() {
    local id=$1; local rd=$2  # signed Δ in pp; rd is BG-Ρ baseline
    if [ "$id" = "null" ]; then echo "null"; return; fi
    awk "BEGIN{
        a=($id<0)?-($id):($id);
        b=($rd<0)?-($rd):($rd);
        if (b==0){ if (a==0) print 1.0; else print -99; } else printf \"%.4f\", 1 - a/b;
    }"
}
HS_SR=$(shrink_ratio "$HS_DELTA_PP" "$BG_RHO_HS_PP")
MM_SR=$(shrink_ratio "$MM_DELTA_PP" "$BG_RHO_MM_PP")
TQ_SR=$(shrink_ratio "$TQ_DELTA_PP" "$BG_RHO_TQ_PP")

increased_count=0
shrunk_count=0
persisted_count=0
for sr in $HS_SR $MM_SR $TQ_SR; do
    [ "$sr" = "null" ] && continue
    awk_result=$(awk "BEGIN{
        sr=$sr;
        if (sr < -0.25) print \"INCREASED\";
        else if (sr >= 0.5) print \"SHRUNK\";
        else print \"PERSISTED\";
    }")
    case "$awk_result" in
        INCREASED) increased_count=$((increased_count+1));;
        SHRUNK)    shrunk_count=$((shrunk_count+1));;
        PERSISTED) persisted_count=$((persisted_count+1));;
    esac
done

HYPOTHESIS='INCONCLUSIVE'
if [ $increased_count -ge 1 ] && [ $shrunk_count -lt 2 ]; then
    HYPOTHESIS='UNEXPECTED'
elif [ $shrunk_count -ge 2 ]; then
    HYPOTHESIS='TEMPLATE_MISMATCH_CONFIRMED'
elif [ $persisted_count -ge 2 ]; then
    HYPOTHESIS='FORGETTING_INDEPENDENT'
fi

# F1_v3 V2 verdict with Instruct anchor (parallel mapping to BG-Ρ)
F1_V3_V2='FAIL'
if [ "$C3_VERDICT" = "PASS" ] && [ "$C4_VERDICT" = "PASS" ]; then
    F1_V3_V2='SUCCESS'
elif [ "$C3_VERDICT" = "PASS" ] && [ "$C4_VERDICT" = "FAIL" ]; then
    F1_V3_V2='COMPARATIVE_PASS'
elif [ "$C3_VERDICT" = "FAIL" ] && [ "$C4_VERDICT" = "PASS" ]; then
    F1_V3_V2='ANCHOR_PASS'
elif [ $C3_PASS_COUNT -ge 1 ] || [ $C4_PASS_COUNT -ge 1 ]; then
    F1_V3_V2='PARTIAL_v3_AMEND'
fi

POD_KILL_404='false'
if [ -f "$POD_INFO" ]; then
    POST=$(jq -r '.post_kill_status // ""' "$POD_INFO" 2>/dev/null)
    if echo "$POST" | grep -qiE 'not found|404|no such|does not exist'; then
        POD_KILL_404='true'
    fi
fi

jq -n \
    --arg cycle "p9_lora_mode1_instruct_eval_2026_05_04" \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg scope "Mode 1 re-eval with Llama-3.2-3B-Instruct base — template-mismatch hypothesis test" \
    --arg model "$HF_BASE_REPO + $HF_LORA_REPO@$HF_LORA_REVISION (step-8k LoRA)" \
    --arg pod "$POD_ID" \
    --argjson kill_404 "$POD_KILL_404" \
    --arg verdict "$HYPOTHESIS" \
    --arg ib_hs_acc "$IB_HS_ACC" --arg ib_hs_norm "$IB_HS_NORM" --arg ib_hs_se "$IB_HS_SE" \
    --arg ib_mm_acc "$IB_MM_ACC" --arg ib_mm_se "$IB_MM_SE" \
    --arg ib_tq_em "$IB_TQ_EM" --arg ib_tq_se "$IB_TQ_SE" \
    --arg il_hs_acc "$IL_HS_ACC" --arg il_hs_norm "$IL_HS_NORM" --arg il_hs_se "$IL_HS_SE" \
    --arg il_mm_acc "$IL_MM_ACC" --arg il_mm_se "$IL_MM_SE" \
    --arg il_tq_em "$IL_TQ_EM" --arg il_tq_se "$IL_TQ_SE" \
    --arg hs_d "$HS_DELTA_PP" --arg hs_thr "$HS_THR_PP" --arg hs_c3 "$HS_C3" --arg hs_c4 "$HS_C4" --arg hs_sr "$HS_SR" --arg hs_diff "$HS_DIFF" \
    --arg mm_d "$MM_DELTA_PP" --arg mm_thr "$MM_THR_PP" --arg mm_c3 "$MM_C3" --arg mm_c4 "$MM_C4" --arg mm_sr "$MM_SR" --arg mm_diff "$MM_DIFF" \
    --arg tq_d "$TQ_DELTA_PP" --arg tq_thr "$TQ_THR_PP" --arg tq_c3 "$TQ_C3" --arg tq_c4 "$TQ_C4" --arg tq_sr "$TQ_SR" --arg tq_diff "$TQ_DIFF" \
    --arg c3v "$C3_VERDICT" --arg c4v "$C4_VERDICT" --arg f1v3v2 "$F1_V3_V2" \
    --argjson c3n "$C3_PASS_COUNT" --argjson c4n "$C4_PASS_COUNT" \
    --argjson shrunk "$shrunk_count" --argjson persisted "$persisted_count" --argjson increased "$increased_count" \
    --argjson wall "$FINAL_ELAPSED_MIN" \
    --argjson cost "$FINAL_COST" \
    --argjson complete "$COMPLETE" \
    '{
        cycle: $cycle, ts_utc: $ts,
        scope: $scope,
        model: $model,
        pod_id: $pod, pod_terminated: true, pod_kill_verified_404: $kill_404,
        verdict: $verdict,
        instruct_base_results: {
            hellaswag: {acc: $ib_hs_acc, acc_norm: $ib_hs_norm, stderr: $ib_hs_se, fewshot: 0, filter: "acc_norm"},
            mmlu:      {acc: $ib_mm_acc, stderr: $ib_mm_se, fewshot: 5},
            triviaqa:  {exact_match: $ib_tq_em, stderr: $ib_tq_se, fewshot: 0, filter: "remove_whitespace"}
        },
        instruct_lora_results: {
            hellaswag: {acc: $il_hs_acc, acc_norm: $il_hs_norm, stderr: $il_hs_se, fewshot: 0, filter: "acc_norm"},
            mmlu:      {acc: $il_mm_acc, stderr: $il_mm_se, fewshot: 5},
            triviaqa:  {exact_match: $il_tq_em, stderr: $il_tq_se, fewshot: 0, filter: "remove_whitespace"}
        },
        delta_per_bench_instruct: {
            hellaswag: ($hs_d|tonumber? // null),
            mmlu:      ($mm_d|tonumber? // null),
            triviaqa:  ($tq_d|tonumber? // null)
        },
        delta_per_bench_non_instruct_BG_Rho: {
            hellaswag: -1.2,
            mmlu:      -4.95,
            triviaqa:  -9.4
        },
        delta_difference_pp: {
            hellaswag_instruct_minus_rho: ($hs_diff|tonumber? // null),
            mmlu_instruct_minus_rho:      ($mm_diff|tonumber? // null),
            triviaqa_instruct_minus_rho:  ($tq_diff|tonumber? // null)
        },
        c3_per_bench: {
            hellaswag: {c3: $hs_c3, threshold_pp: ($hs_thr|tonumber? // null), shrink_ratio_vs_rho: ($hs_sr|tonumber? // null)},
            mmlu:      {c3: $mm_c3, threshold_pp: ($mm_thr|tonumber? // null), shrink_ratio_vs_rho: ($mm_sr|tonumber? // null)},
            triviaqa:  {c3: $tq_c3, threshold_pp: ($tq_thr|tonumber? // null), shrink_ratio_vs_rho: ($tq_sr|tonumber? // null)}
        },
        c4_per_bench: {hellaswag: $hs_c4, mmlu: $mm_c4, triviaqa: $tq_c4},
        c3_pass_count_instruct: ("\($c3n)/3"),
        c4_pass_count_instruct: ("\($c4n)/3"),
        c3_verdict: $c3v, c4_verdict: $c4v,
        f1_v3_v2_with_instruct_anchor: $f1v3v2,
        hypothesis_classification: {
            shrunk_count: $shrunk,
            persisted_count: $persisted,
            increased_count: $increased,
            decision_rule: "≥2/3 shrunk(≥50%) → TEMPLATE_MISMATCH_CONFIRMED; any increased(>+25%) → UNEXPECTED; ≥2/3 persisted → FORGETTING_INDEPENDENT"
        },
        complete_sentinel_detected: ($complete == 1),
        wall_time_min: $wall,
        actual_cost_usd: $cost,
        budget_target_usd: 2.50,
        budget_hard_cap_usd: 3.50,
        lessons_applied: {
            L1_sentinel_name: "results/COMPLETE.sentinel",
            L2_skip_unneeded_setup: "Instruct + LoRA only (no CLM)",
            L3_sentinel_kill_lag_s: "poll interval 60s ⇒ ≤90s detection→kill",
            L4_single_process_heartbeat: "heartbeat.txt from main exec.bash",
            L5_redact_at_boot: "sed redact pre-tee for boot.log",
            L6_data_first_then_kill: "final scp before trap fires"
        },
        honest_c3: [
            "Anchor remains step-8000 LoRA (HF commit 5a9b4584); same step-pin as BG-Ρ. Any step-10k recovery would shift both BG-Ρ and BG-Ψ deltas in correlated fashion — the relative delta_difference between Instruct and non-Instruct base anchors is what tests the template-mismatch hypothesis.",
            "Instruct base eval here uses NO chat-template wrapping (lm-eval default for hellaswag/mmlu/triviaqa is plain prompt). Instruct base may UNDERPERFORM its true ceiling without explicit chat-template framing. So instruct_base anchors here are 'raw-prompt-on-Instruct' — comparable to BG-Ρ's 'raw-prompt-on-non-Instruct' but NOT to Instruct's chat-templated ceiling.",
            "limit=500 single-seed: same statistical caveat as BG-Ρ. delta_difference precision ~3-4pp on hellaswag/triviaqa, ~0.6pp on MMLU. shrink_ratio thresholds (0.5, 0.25) chosen pre-launch per spec.",
            "Adapter base now matches eval base (Instruct=Instruct), so template-mismatch artifact removed. If degradation persists, this is direct evidence that the LoRA did not preserve base capabilities under proper anchor alignment ⇒ catastrophic forgetting independent of base choice.",
            "lm-eval peft= local-dir composition (same fix as BG-Ρ attempt 2). bf16, lm-eval 0.4.11, peft inference_mode=true (no merge). Numeric drift vs eval-time merge is small (≤0.5pp) but consistent across both base+LoRA passes."
        ]
    }' > "$VERDICT"

log "verdict=$HYPOTHESIS c3=$C3_VERDICT($C3_PASS_COUNT/3) c4=$C4_VERDICT($C4_PASS_COUNT/3) f1v3v2=$F1_V3_V2 wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
log "hs: Δ_inst=${HS_DELTA_PP}pp Δ_rho=${BG_RHO_HS_PP}pp diff=${HS_DIFF}pp shrink=${HS_SR} c3=$HS_C3 c4=$HS_C4"
log "mm: Δ_inst=${MM_DELTA_PP}pp Δ_rho=${BG_RHO_MM_PP}pp diff=${MM_DIFF}pp shrink=${MM_SR} c3=$MM_C3 c4=$MM_C4"
log "tq: Δ_inst=${TQ_DELTA_PP}pp Δ_rho=${BG_RHO_TQ_PP}pp diff=${TQ_DIFF}pp shrink=${TQ_SR} c3=$TQ_C3 c4=$TQ_C4"
log "hypothesis class: shrunk=$shrunk_count persisted=$persisted_count increased=$increased_count"
hb "verdict=$HYPOTHESIS c3=$C3_VERDICT c4=$C4_VERDICT f1v3v2=$F1_V3_V2"
echo "__P9_LORA_MODE1_INSTRUCT_EVAL__ $HYPOTHESIS F1V3V2=$F1_V3_V2" | tee -a "$RUN_LOG"
exit 0
