#!/bin/bash
# emitted by tool/p9_lora_mode1_eval_h100_orchestrator.hexa — Mode 1 LoRA-vs-base lifecycle
# raw#9 sibling-pattern Mac-side bash. Regenerate via --emit. raw#37 H100 transient py.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/p9_lora_mode1_eval_2026_05_04'
RESULTS_DIR='/Users/ghost/core/anima/state/p9_lora_mode1_eval_2026_05_04/results'
POD_INFO='/Users/ghost/core/anima/state/p9_lora_mode1_eval_2026_05_04/pod_info.json'
VERDICT='/Users/ghost/core/anima/state/p9_lora_mode1_eval_2026_05_04/verdict.json'
RUN_LOG='/Users/ghost/core/anima/state/p9_lora_mode1_eval_2026_05_04/run.log'
HEARTBEAT='/Users/ghost/core/anima/state/p9_lora_mode1_eval_2026_05_04/heartbeat.txt'
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
RUNPODCTL='/opt/homebrew/bin/runpodctl'
MAX_WALL_MIN=45
BUDGET_HARD_CAP=2.5
OD_RATE=2.99
HF_LORA_REPO='need-singularity/p9-llama32-lora-stage1'
HF_LORA_REVISION='5a9b4584'
HF_BASE_REPO='meta-llama/Llama-3.2-3B'
START_EPOCH=$(date -u +%s)

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

# ── Stage 1: boot H100 pod (sed redact at boot, BEFORE tee — lesson L5) ──
POD_NAME='anima-p9-lora-mode1-eval-2026-05-04'
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
# Redact BEFORE writing to long-lived log. Then delete raw.
redact_hf < "$BOOT_RAW_OUT" > "$BOOT_OUT"
rm -f "$BOOT_RAW_OUT"
if [ $BOOT_RC -ne 0 ]; then
    log "FATAL: pod boot failed rc=$BOOT_RC"
    cat "$BOOT_OUT" | redact_hf | tee -a "$RUN_LOG"
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed" '{cycle:"p9_lora_mode1_eval_2026_05_04",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
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
log "setup: install lm-eval + peft + download Llama base + step-8k LoRA"
hb "stage3_setup_starting"
$SSH 'mkdir -p /workspace/p9_lora_eval/results'
$SCP "/Users/ghost/core/anima/state/p9_lora_mode1_eval_2026_05_04/run_h100.bash" "root@$SSH_HOST:/workspace/p9_lora_eval/run_h100.bash" 2>&1 | tail -1
$SSH 'chmod +x /workspace/p9_lora_eval/run_h100.bash'

# Launch detached. Source HF_TOKEN from /proc/1/environ (runpodctl --env injects to PID1 only).
log "launching benchmark suite on H100"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/p9_lora_eval/hf_token.env && cd /workspace/p9_lora_eval && set -a && . hf_token.env && set +a && nohup bash run_h100.bash > orchestrator.log 2>&1 & echo $! > run.pid; disown $! 2>/dev/null || true; sleep 2; cat run.pid'
hb "stage3_h100_launched"

# ── Stage 4: poll loop (heartbeat each cycle) ──
log "poll loop start (max ${MAX_WALL_MIN}min, budget cap \$${BUDGET_HARD_CAP})"
COMPLETE=0
POLL_INTERVAL=60  # 1-min poll for snappy auto-kill (lesson L3 sharpened)
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

    PROBE=$($SSH 'ls /workspace/p9_lora_eval/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ps -p $(cat /workspace/p9_lora_eval/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|')"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|' | head -c 200)"

    # incremental sync (small JSONs only)
    $SCP -r "root@$SSH_HOST:/workspace/p9_lora_eval/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/p9_lora_eval/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync FIRST then auto-kill (lesson: don't lose data)"
        COMPLETE=1
        # final sync — fetch results FIRST before kill (lesson 5)
        $SCP -r "root@$SSH_HOST:/workspace/p9_lora_eval/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        $SCP "root@$SSH_HOST:/workspace/p9_lora_eval/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>&1 | tail -1 || true
        break
    fi

    sleep $POLL_INTERVAL
done

# ── Stage 5: pod kill via trap (auto on exit) ──
# trap _kill_pod fires when this script exits.

# ── Stage 6: verdict (per-bench numeric extraction + c3/c4 gates) ──
log "computing verdict from per-bench JSONs"
FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")
hb "stage6_verdict_computing"

BENCH_COUNT=$(ls $RESULTS_DIR/lora_*.json 2>/dev/null | wc -l | awk '{print $1}')

# Llama base anchors (BG-Ο 93bef8c8)
LB_HS_NORM=0.654
LB_HS_SE=0.02129
LB_MM_ACC=0.5796
LB_MM_SE=0.00428
LB_TQ_EM=0.396
LB_TQ_SE=0.02189

# Random + 5pp baselines
R5_HS=0.30   # random 0.25 + 0.05
R5_MM=0.30   # random 0.25 + 0.05
R5_TQ=0.05   # random ~0 + 0.05

# Extract LoRA metrics
LR_HS_ACC="null"; LR_HS_NORM="null"; LR_HS_SE="null"
if [ -f "$RESULTS_DIR/lora_hellaswag.json" ]; then
    LR_HS_ACC=$(jq -r '.results.hellaswag."acc,none" // .results.hellaswag.acc // "null"' "$RESULTS_DIR/lora_hellaswag.json")
    LR_HS_NORM=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' "$RESULTS_DIR/lora_hellaswag.json")
    LR_HS_SE=$(jq -r '.results.hellaswag."acc_norm_stderr,none" // .results.hellaswag.acc_norm_stderr // "null"' "$RESULTS_DIR/lora_hellaswag.json")
fi
LR_MM_ACC="null"; LR_MM_SE="null"
if [ -f "$RESULTS_DIR/lora_mmlu.json" ]; then
    LR_MM_ACC=$(jq -r '.results.mmlu."acc,none" // .results.mmlu.acc // "null"' "$RESULTS_DIR/lora_mmlu.json")
    LR_MM_SE=$(jq -r '.results.mmlu."acc_stderr,none" // .results.mmlu.acc_stderr // "null"' "$RESULTS_DIR/lora_mmlu.json")
fi
LR_TQ_EM="null"; LR_TQ_SE="null"
if [ -f "$RESULTS_DIR/lora_triviaqa.json" ]; then
    LR_TQ_EM=$(jq -r '.results.triviaqa."exact_match,remove_whitespace" // .results.triviaqa."exact_match,none" // .results.triviaqa.exact_match // "null"' "$RESULTS_DIR/lora_triviaqa.json")
    LR_TQ_SE=$(jq -r '.results.triviaqa."exact_match_stderr,remove_whitespace" // .results.triviaqa."exact_match_stderr,none" // .results.triviaqa.exact_match_stderr // "null"' "$RESULTS_DIR/lora_triviaqa.json")
fi

# c3 helper: |LoRA - Llama_base| ≥ 2 × max(LoRA_se, Llama_se)
c3_check() {
    local lora=$1; local base=$2; local lse=$3; local bse=$4
    if [ "$lora" = "null" ]; then echo "MISSING|null|null"; return; fi
    awk "BEGIN{
        d = ($lora - $base);
        ad = (d < 0) ? -d : d;
        m = ($lse > $bse) ? $lse : $bse;
        thr = 2 * m;
        delta_pp = d * 100;
        thr_pp = thr * 100;
        if (ad >= thr) print "PASS|" delta_pp "|" thr_pp;
        else            print "FAIL|" delta_pp "|" thr_pp;
    }"
}
# c4 helper: LoRA ≥ random + 5pp
c4_check() {
    local lora=$1; local r5=$2
    if [ "$lora" = "null" ]; then echo "MISSING"; return; fi
    awk "BEGIN{ if ($lora >= $r5) print \"PASS\"; else print \"FAIL\" }"
}

HS_C3_LINE=$(c3_check "$LR_HS_NORM" $LB_HS_NORM "$LR_HS_SE" $LB_HS_SE)
MM_C3_LINE=$(c3_check "$LR_MM_ACC"  $LB_MM_ACC  "$LR_MM_SE" $LB_MM_SE)
TQ_C3_LINE=$(c3_check "$LR_TQ_EM"   $LB_TQ_EM   "$LR_TQ_SE" $LB_TQ_SE)
HS_C3=$(echo $HS_C3_LINE | cut -d'|' -f1); HS_DELTA_PP=$(echo $HS_C3_LINE | cut -d'|' -f2); HS_C3_THR_PP=$(echo $HS_C3_LINE | cut -d'|' -f3)
MM_C3=$(echo $MM_C3_LINE | cut -d'|' -f1); MM_DELTA_PP=$(echo $MM_C3_LINE | cut -d'|' -f2); MM_C3_THR_PP=$(echo $MM_C3_LINE | cut -d'|' -f3)
TQ_C3=$(echo $TQ_C3_LINE | cut -d'|' -f1); TQ_DELTA_PP=$(echo $TQ_C3_LINE | cut -d'|' -f2); TQ_C3_THR_PP=$(echo $TQ_C3_LINE | cut -d'|' -f3)

HS_C4=$(c4_check "$LR_HS_NORM" $R5_HS)
MM_C4=$(c4_check "$LR_MM_ACC"  $R5_MM)
TQ_C4=$(c4_check "$LR_TQ_EM"   $R5_TQ)

# c3 / c4 ≥2/3 PASS rule
C3_PASS_COUNT=0
for g in $HS_C3 $MM_C3 $TQ_C3; do [ "$g" = "PASS" ] && C3_PASS_COUNT=$((C3_PASS_COUNT+1)); done
C4_PASS_COUNT=0
for g in $HS_C4 $MM_C4 $TQ_C4; do [ "$g" = "PASS" ] && C4_PASS_COUNT=$((C4_PASS_COUNT+1)); done

C3_VERDICT='FAIL'; [ $C3_PASS_COUNT -ge 2 ] && C3_VERDICT='PASS'
C4_VERDICT='FAIL'; [ $C4_PASS_COUNT -ge 2 ] && C4_VERDICT='PASS'

# Overall Mode 1 verdict
VERDICT_LABEL='FAIL'
if [ "$C3_VERDICT" = "PASS" ] && [ "$C4_VERDICT" = "PASS" ]; then
    VERDICT_LABEL='PASS'
elif [ "$C3_VERDICT" = "PASS" ] || [ "$C4_VERDICT" = "PASS" ]; then
    VERDICT_LABEL='PARTIAL'
fi

# F1_v3 V2 cumulative (post-this-cycle):
#   c1 anchors_run PASS (BG-Ο)
#   c2 llama±10% PASS (BG-Ο, 2/3)
#   c3 lora-base 2σ → from this cycle
#   c4 lora≥random+5pt → from this cycle
# Mapping:
#   all 4 PASS → SUCCESS
#   c1+c2+c3 PASS, c4 FAIL → COMPARATIVE_PASS
#   c1+c2 PASS, c3 FAIL but c4 PASS → ANCHOR_PASS (anchors valid; LoRA above random but not statistically separated from base)
#   c1+c2 PASS, c3 FAIL, c4 FAIL → FAIL (catastrophic forgetting hypothesis)
#   any of c3/c4 partial (1 of 3 benchmarks) → PARTIAL_v3_AMEND
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
    --arg cycle "p9_lora_mode1_eval_2026_05_04" \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg model "$HF_BASE_REPO + $HF_LORA_REPO@$HF_LORA_REVISION (step-8k LoRA)" \
    --arg pod "$POD_ID" \
    --argjson kill_404 "$POD_KILL_404" \
    --arg verdict "$VERDICT_LABEL" \
    --arg c3v "$C3_VERDICT" --arg c4v "$C4_VERDICT" \
    --arg f1v3v2 "$F1_V3_V2" \
    --arg hs_acc "$LR_HS_ACC" --arg hs_norm "$LR_HS_NORM" --arg hs_se "$LR_HS_SE" \
    --arg hs_c3 "$HS_C3" --arg hs_c4 "$HS_C4" --arg hs_d "$HS_DELTA_PP" --arg hs_thr "$HS_C3_THR_PP" \
    --arg mm_acc "$LR_MM_ACC" --arg mm_se "$LR_MM_SE" \
    --arg mm_c3 "$MM_C3" --arg mm_c4 "$MM_C4" --arg mm_d "$MM_DELTA_PP" --arg mm_thr "$MM_C3_THR_PP" \
    --arg tq_em "$LR_TQ_EM" --arg tq_se "$LR_TQ_SE" \
    --arg tq_c3 "$TQ_C3" --arg tq_c4 "$TQ_C4" --arg tq_d "$TQ_DELTA_PP" --arg tq_thr "$TQ_C3_THR_PP" \
    --argjson wall "$FINAL_ELAPSED_MIN" \
    --argjson cost "$FINAL_COST" \
    --argjson n "$BENCH_COUNT" \
    --argjson complete "$COMPLETE" \
    '{
        cycle: $cycle, ts_utc: $ts,
        model: $model,
        scope: "Mode 1 — LoRA(step-8k)-vs-Llama-base internal Δ on 3 benchmarks (limit=500, seeds=42, bfloat16)",
        pod_id: $pod, pod_terminated: true, pod_kill_verified_404: $kill_404,
        verdict: $verdict,
        results_per_benchmark: {
            hellaswag: {acc: $hs_acc, acc_norm: $hs_norm, stderr: $hs_se,
                        llama_base_acc_norm: 0.654, llama_base_stderr: 0.02129,
                        delta_vs_llama_base_pp: $hs_d, c3_2_sigma_threshold_pp: $hs_thr,
                        c3_pass: ($hs_c3=="PASS"), c4_above_random5pt: ($hs_c4=="PASS")},
            mmlu:      {acc: $mm_acc, stderr: $mm_se,
                        llama_base_acc: 0.5796, llama_base_stderr: 0.00428,
                        delta_vs_llama_base_pp: $mm_d, c3_2_sigma_threshold_pp: $mm_thr,
                        c3_pass: ($mm_c3=="PASS"), c4_above_random5pt: ($mm_c4=="PASS"), fewshot: 5},
            triviaqa:  {exact_match: $tq_em, stderr: $tq_se,
                        llama_base_em: 0.396, llama_base_stderr: 0.02189,
                        delta_vs_llama_base_pp: $tq_d, c3_2_sigma_threshold_pp: $tq_thr,
                        c3_pass: ($tq_c3=="PASS"), c4_above_random5pt: ($tq_c4=="PASS"),
                        filter: "remove_whitespace"}
        },
        f1_v3_amended_criterion_3_lora_base_2_sigma: $c3v,
        f1_v3_amended_criterion_4_lora_above_random_5pt: $c4v,
        f1_v3_v2_full_verdict_with_bg_xi_amendment: $f1v3v2,
        bench_count_completed: $n,
        complete_sentinel_detected: ($complete == 1),
        wall_time_min: $wall,
        actual_cost_usd: $cost,
        budget_target_usd: 1.50,
        budget_hard_cap_usd: 2.50,
        lessons_applied: {
            L1_sentinel_name: "results/COMPLETE.sentinel",
            L2_skip_unneeded_setup: "Llama-only download (no CLM)",
            L3_sentinel_kill_lag_s: "poll interval 60s ⇒ ≤90s detection→kill",
            L4_single_process_heartbeat: "heartbeat.txt from main exec.bash",
            L5_redact_at_boot: "sed redact pre-tee for boot.log",
            L6_data_first_then_kill: "final scp before trap fires"
        },
        honest_c3: [
            "Anchor is step-8000 LoRA NOT preregistered step-10000 (per BG-ξ verify_report; 2000 steps lost during HF push race) — Δ vs base may be ~5-10% underestimated relative to fully-trained adapter",
            "limit=500 ⇒ stderr ~2pp on hellaswag/triviaqa; on tight 2σ thresholds (~4pp) borderline c3 calls are noise-sensitive",
            "adapter base mismatch caveat: HF adapter_config declares base = Llama-3.2-3B-Instruct; we compose onto Llama-3.2-3B (non-Instruct, BG-Ο anchor). Numerical drift expected from BOS/template behavior; verify lm-eval logs for chat-template warnings",
            "Single seed (42); per-prompt variance not characterized — full c3 confidence interval would require multi-seed (≥3) with paired bootstrap",
            "H100 bf16 + lm-eval 0.4.11 vendor-default decode params; LoRA inference_mode=true (no merge); slight numeric drift vs eval-time merge"
        ]
    }' > "$VERDICT"

log "verdict=$VERDICT_LABEL c3=$C3_VERDICT($C3_PASS_COUNT/3) c4=$C4_VERDICT($C4_PASS_COUNT/3) f1v3v2=$F1_V3_V2 wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
log "hs: norm=$LR_HS_NORM Δ=${HS_DELTA_PP}pp c3=$HS_C3 c4=$HS_C4   mmlu: acc=$LR_MM_ACC Δ=${MM_DELTA_PP}pp c3=$MM_C3 c4=$MM_C4   tq: em=$LR_TQ_EM Δ=${TQ_DELTA_PP}pp c3=$TQ_C3 c4=$TQ_C4"
hb "verdict=$VERDICT_LABEL c3=$C3_VERDICT c4=$C4_VERDICT f1v3v2=$F1_V3_V2"
echo "__P9_LORA_MODE1_EVAL__ $VERDICT_LABEL F1V3V2=$F1_V3_V2" | tee -a "$RUN_LOG"
exit 0
