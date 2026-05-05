#!/bin/bash
# emitted by tool/clm_v4_lora_train_orchestrator.hexa — CLM v4 + LoRA SFT lifecycle
# raw#9 sibling-pattern Mac-side bash; raw#37 H100 transient py.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05'
RESULTS_DIR='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/results'
CORPUS_DIR='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/corpus'
SLICE_A_LOCAL='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl'
CORPUS_MIX_PY='/Users/ghost/core/anima/tool/transient_py/p9_retrain_v2_corpus_mix.py'
TRAIN_PY='/Users/ghost/core/anima/tool/transient_py/clm_v4_lora_train.py'
POD_INFO='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/pod_info.json'
VERDICT='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/verdict.json'
RUN_LOG='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/run.log'
HEARTBEAT='/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/heartbeat.txt'
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
RUNPODCTL='/opt/homebrew/bin/runpodctl'
MAX_WALL_MIN=300
BUDGET_HARD_CAP=15
OD_RATE=2.99
HF_BASE_REPO='need-singularity/clm-v4-mk2-v1'
START_EPOCH=$(date -u +%s)

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }
hb()  { echo "[$(date -u +%FT%TZ)] $*" > "$HEARTBEAT"; }
redact_hf() { sed -E 's/(HF_TOKEN["[:space:]]*[:=]["[:space:]]*)hf_[A-Za-z0-9_]+/\1<REDACTED>/g; s/(hf_)[A-Za-z0-9_]{20,}/\1<REDACTED>/g'; }

# ── Stage 0: secrets (raw bypass for redaction wrapper) ──
export RUNPOD_API_KEY=$(/Users/ghost/core/secret/bin/secret get runpod.api_key --raw 2>/dev/null)
export HF_TOKEN_LOCAL=$(/Users/ghost/core/secret/bin/secret get huggingface.token --raw 2>/dev/null)
if [ -z "${RUNPOD_API_KEY:-}" ] || [ -z "${HF_TOKEN_LOCAL:-}" ]; then
    log "FATAL: secrets unavailable"
    exit 2
fi
if [[ "$RUNPOD_API_KEY" == \*\*\** ]] || [[ "$HF_TOKEN_LOCAL" == \*\*\** ]]; then
    log "FATAL: secret returned redacted form despite --raw"
    exit 2
fi
log "secrets OK (runpod=${#RUNPOD_API_KEY}b hf=${#HF_TOKEN_LOCAL}b)"
hb "stage0_secrets_loaded"

# ── Stage 0b: L9 HF auth pre-flight ──
WHOAMI=$(curl -s -H "Authorization: Bearer $HF_TOKEN_LOCAL" 'https://huggingface.co/api/whoami-v2' | head -c 300)
if echo "$WHOAMI" | grep -q '"name"'; then
    USER=$(echo "$WHOAMI" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("name","?"))')
    log "hf auth PASS user=$USER"
else
    log "FATAL L9: hf auth FAIL — token invalid or revoked: $WHOAMI"
    exit 2
fi
hb "stage0b_hf_auth_ok"

# ── Pre-flight: slice A must exist locally ──
if [ ! -f "$SLICE_A_LOCAL" ]; then
    log "FATAL: slice A missing: $SLICE_A_LOCAL"
    exit 2
fi
SLICE_A_LINES=$(wc -l < "$SLICE_A_LOCAL" | awk '{print $1}')
log "slice A OK ($SLICE_A_LINES lines)"

# ── Stage 1: boot H100 SECURE on-demand (vol=120GB, disk=100GB) ──
POD_NAME='anima-clm-v4-lora-sft-2026-05-05'
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
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed" '{cycle:"clm_v4_lora_sft_2026_05_05",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
    exit 3
fi
POD_ID=$(grep -oE '"[a-z0-9]{14}"' "$BOOT_OUT" | head -1 | tr -d '"')
if [ -z "$POD_ID" ]; then
    POD_ID=$(grep -oE 'pod [a-z0-9]{12,16}' "$BOOT_OUT" | head -1 | awk '{print $2}')
fi
if [ -z "$POD_ID" ]; then
    log "FATAL: cannot extract pod_id from boot output"
    cat "$BOOT_OUT"
    exit 4
fi
log "pod_id=$POD_ID"
echo '{"pod_id":"'$POD_ID'","booted_ts":"'$(date -u +%FT%TZ)'"}' > "$POD_INFO"
hb "stage1_pod_booted pod_id=$POD_ID"

# ── Stage 1b: trap kill-on-exit (L3 + L7 redact + L13 trap pre-stop scp) ──
_kill_pod() {
    log "[trap] data-first scp before kill (L13)"
    if [ -n "${SSH_HOST:-}" ] && [ -n "${SSH_PORT:-}" ]; then
        timeout 60 scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P "$SSH_PORT" -r \
            "root@$SSH_HOST:/workspace/clm_v4_lora/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 || true
        timeout 30 scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P "$SSH_PORT" \
            "root@$SSH_HOST:/workspace/clm_v4_lora/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>&1 | tail -1 || true
    fi
    log "[trap] killing pod=$POD_ID"
    $RUNPODCTL pod stop "$POD_ID" 2>&1 | redact_hf | tee -a "$RUN_LOG" || true
    sleep 3
    $RUNPODCTL pod delete "$POD_ID" 2>&1 | redact_hf | tee -a "$RUN_LOG" || true
    sleep 5
    POST=$($RUNPODCTL pod get "$POD_ID" 2>&1 | redact_hf | head -3)
    log "[trap] post-kill: $POST"
    if [ -f "$POD_INFO" ]; then
        jq --arg killed "$(date -u +%FT%TZ)" --arg post "$POST" \
            '. + {killed_ts:$killed, post_kill_status:$post}' "$POD_INFO" > "$POD_INFO.tmp" && mv "$POD_INFO.tmp" "$POD_INFO" || true
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

# ── Stage 3: ship transient py + slice A ──
log "shipping slice A (76MB) + transient py"
hb "stage3_setup_starting"
$SSH 'mkdir -p /workspace/clm_v4_lora/{corpus,results,ckpts,sentinels}'
$SCP "$SLICE_A_LOCAL" "root@$SSH_HOST:/workspace/clm_v4_lora/corpus/slice_A_anima_30k.jsonl" 2>&1 | tail -1
$SCP "$CORPUS_MIX_PY" "root@$SSH_HOST:/workspace/clm_v4_lora/corpus_mix.py" 2>&1 | tail -1
$SCP "$TRAIN_PY" "root@$SSH_HOST:/workspace/clm_v4_lora/train.py" 2>&1 | tail -1
$SCP "/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/run_h100.bash" "root@$SSH_HOST:/workspace/clm_v4_lora/run_h100.bash" 2>&1 | tail -1
$SSH 'chmod +x /workspace/clm_v4_lora/run_h100.bash'

log "launching H100 pipeline (corpus + train + intermediate eval + final eval)"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/clm_v4_lora/hf_token.env && cd /workspace/clm_v4_lora && set -a && . hf_token.env && set +a && nohup bash run_h100.bash > orchestrator.log 2>&1 & echo $! > run.pid; disown $! 2>/dev/null || true; sleep 2; cat run.pid'
hb "stage3_h100_launched"

# ── Stage 4: poll loop (heartbeat per cycle, sentinel-kill, cost cap) ──
log "poll loop start (max ${MAX_WALL_MIN}min, budget cap \$${BUDGET_HARD_CAP})"
COMPLETE=0
EARLY_STOP=0
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

    PROBE=$($SSH 'ls /workspace/clm_v4_lora/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ls /workspace/clm_v4_lora/results/EARLY_STOP.sentinel 2>/dev/null && echo EARLY_STOP_FOUND; ps -p $(cat /workspace/clm_v4_lora/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1; tail -1 /workspace/clm_v4_lora/orchestrator.log 2>/dev/null' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|' | head -c 240)"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST}"

    # incremental sync: small JSONs + log
    $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/clm_v4_lora/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync FIRST then auto-kill"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora/ckpts/final" "$RESULTS_DIR/adapter_final" 2>&1 | tail -3 || true
        break
    fi
    if echo "$PROBE" | grep -q EARLY_STOP_FOUND; then
        log "EARLY_STOP.sentinel detected (F-CLM-LORA-1 forgetting OR φ★-flip) — final sync + kill"
        EARLY_STOP=1
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        # Pull any partial adapter for post-mortem
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_lora/ckpts" "$RESULTS_DIR/ckpts_partial" 2>&1 | tail -3 || true
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

# CLM v4 baseline anchors (state/clm_v4_baseline_eval_2026_05_05/verdict.json limit=200)
CB_HS_NORM=0.255
CB_HS_SE=0.0309
CB_MM_ACC=0.255
CB_MM_SE=0.0045
CB_TQ_EM=0.000
CB_TQ_SE=0.000
CB_OBQA_NORM=0.28
CB_PHI_BASE=37.27   # ckpt_best_phi (training-time best); substrate carry=41.86

# Llama Path A v2 retry-3 eval-rerun comparator (state/p9_path_a_retrain_v2_retry_3_eval_rerun)
LP_HS_NORM=0.645
LP_MM_ACC=0.575
LP_TQ_EM=0.455
# F1_v3 composite = (HS + MM + TQ) / 3
LP_COMPOSITE=$(awk "BEGIN{printf \"%.4f\", ($LP_HS_NORM + $LP_MM_ACC + $LP_TQ_EM) / 3}")

# Extract intermediate eval scores (HS-200 at step 2000/4000/6000)
INTER_HS_2K="null"; INTER_HS_4K="null"; INTER_HS_6K="null"
if [ -f "$RESULTS_DIR/intermediate_hs_step2000.json" ]; then
    INTER_HS_2K=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' "$RESULTS_DIR/intermediate_hs_step2000.json")
fi
if [ -f "$RESULTS_DIR/intermediate_hs_step4000.json" ]; then
    INTER_HS_4K=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' "$RESULTS_DIR/intermediate_hs_step4000.json")
fi
if [ -f "$RESULTS_DIR/intermediate_hs_step6000.json" ]; then
    INTER_HS_6K=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' "$RESULTS_DIR/intermediate_hs_step6000.json")
fi

# Final post-LoRA eval (HellaSwag/MMLU/TriviaQA limit=200)
FINAL_HS="null"; FINAL_MM="null"; FINAL_TQ="null"
if [ -f "$RESULTS_DIR/final_lora_hellaswag.json" ]; then
    FINAL_HS=$(jq -r '.results.hellaswag."acc_norm,none" // .results.hellaswag.acc_norm // "null"' "$RESULTS_DIR/final_lora_hellaswag.json")
fi
if [ -f "$RESULTS_DIR/final_lora_mmlu.json" ]; then
    FINAL_MM=$(jq -r '.results.mmlu."acc,none" // .results.mmlu.acc // "null"' "$RESULTS_DIR/final_lora_mmlu.json")
fi
if [ -f "$RESULTS_DIR/final_lora_triviaqa.json" ]; then
    FINAL_TQ=$(jq -r '.results.triviaqa."exact_match,remove_whitespace" // .results.triviaqa."exact_match,none" // .results.triviaqa.exact_match // "null"' "$RESULTS_DIR/final_lora_triviaqa.json")
fi

# φ★ post-LoRA proxy (from in-pod measurement)
PHI_POST="null"; PHI_BASELINE_PRE="null"
if [ -f "$RESULTS_DIR/phi_star_post_lora.json" ]; then
    PHI_POST=$(jq -r '.phi_star_proxy_raw_mean // "null"' "$RESULTS_DIR/phi_star_post_lora.json")
fi
if [ -f "$RESULTS_DIR/phi_star_pre_lora.json" ]; then
    PHI_BASELINE_PRE=$(jq -r '.phi_star_proxy_raw_mean // "null"' "$RESULTS_DIR/phi_star_pre_lora.json")
fi

# F1_v3 composite (HS + MM + TQ) / 3 for CLM v4 LoRA
CLM_COMPOSITE="null"
if [ "$FINAL_HS" != "null" ] && [ "$FINAL_MM" != "null" ] && [ "$FINAL_TQ" != "null" ]; then
    CLM_COMPOSITE=$(awk -v h="$FINAL_HS" -v m="$FINAL_MM" -v t="$FINAL_TQ" \
        'BEGIN{printf "%.4f", (h+m+t)/3}')
fi

# F-CLM-LORA-1: forgetting_index < 0.05 (HS-200 final >= base - 1pp)
FCLM1='UNKNOWN'
FORGETTING_INDEX='null'
if [ "$FINAL_HS" != "null" ]; then
    FORGETTING_INDEX=$(awk -v p="$FINAL_HS" -v b="$CB_HS_NORM" 'BEGIN{ if (b > 0) printf "%.4f", (b - p) / b; else print "null" }')
    FCLM1=$(awk -v p="$FINAL_HS" -v b="$CB_HS_NORM" 'BEGIN{ if (p+0 >= b - 0.01) print "PASS"; else print "FAIL" }')
elif [ "$EARLY_STOP" = "1" ]; then
    FCLM1='EARLY_STOP_FORGETTING'
fi

# F-CLM-LORA-2: composite >= Llama Path A v2 (THE differentiator C-CLM-LORA-2)
FCLM2='UNKNOWN'
DIFFERENTIATOR='UNKNOWN'
if [ "$CLM_COMPOSITE" != "null" ]; then
    FCLM2=$(awk -v c="$CLM_COMPOSITE" -v l="$LP_COMPOSITE" 'BEGIN{ if (c+0 >= l+0) print "PASS"; else print "FAIL" }')
    DELTA=$(awk -v c="$CLM_COMPOSITE" -v l="$LP_COMPOSITE" 'BEGIN{printf "%.4f", c - l}')
    if [ "$FCLM2" = "PASS" ]; then
        DIFFERENTIATOR='ANIMA_BEATS_LLAMA'
    else
        ABS_DELTA=$(awk -v d="$DELTA" 'BEGIN{ if (d < 0) d=-d; print d }')
        IS_REGRESSION=$(awk -v d="$ABS_DELTA" 'BEGIN{ if (d > 0.05) print 1; else print 0 }')
        if [ "$IS_REGRESSION" = "1" ]; then
            DIFFERENTIATOR='LLAMA_BEATS_ANIMA_REGRESSION'
        else
            DIFFERENTIATOR='LLAMA_BEATS_ANIMA_PARITY_BAND'
        fi
    fi
fi

# F-CLM-LORA-3: adapter < 500MB
FCLM3='UNKNOWN'
ADAPTER_SIZE_MB='null'
if [ -f "$RESULTS_DIR/adapter_final/adapter_model.safetensors" ]; then
    SZ=$(stat -f '%z' "$RESULTS_DIR/adapter_final/adapter_model.safetensors" 2>/dev/null || stat -c '%s' "$RESULTS_DIR/adapter_final/adapter_model.safetensors" 2>/dev/null || echo 0)
    ADAPTER_SIZE_MB=$(awk -v s="$SZ" 'BEGIN{printf "%.2f", s / (1024*1024)}')
    FCLM3=$(awk -v s="$ADAPTER_SIZE_MB" 'BEGIN{ if (s+0 < 500) print "PASS"; else print "FAIL" }')
fi

# F-CLM-LORA-4: cell axis-conditioning preserved (smoke proxy: post-LoRA logits are finite + non-degenerate)
FCLM4='UNKNOWN'
if [ -f "$RESULTS_DIR/post_lora_smoke.json" ]; then
    FCLM4=$(jq -r '.smoke_pass // "UNKNOWN"' "$RESULTS_DIR/post_lora_smoke.json")
fi

# F-CLM-LORA-5: shim v4 hf_format compat (loadable post-merge)
FCLM5='UNKNOWN'
if [ -f "$RESULTS_DIR/post_lora_shim_compat.json" ]; then
    FCLM5=$(jq -r '.shim_compat // "UNKNOWN"' "$RESULTS_DIR/post_lora_shim_compat.json")
fi

# φ★ drift: post - baseline (substrate carry 41.86)
PHI_STAR_BASELINE_CARRY=41.86
PHI_DRIFT_PP='null'
if [ "$PHI_POST" != "null" ] && [ "$PHI_BASELINE_PRE" != "null" ]; then
    PHI_DRIFT_PP=$(awk -v p="$PHI_POST" -v b="$PHI_BASELINE_PRE" 'BEGIN{printf "%.4f", p - b}')
fi

# Overall verdict
OVERALL='V2_FAIL'
PASS_COUNT=0
for v in "$FCLM1" "$FCLM2" "$FCLM3" "$FCLM4" "$FCLM5"; do
    [ "$v" = "PASS" ] && PASS_COUNT=$((PASS_COUNT + 1))
done
if [ "$PASS_COUNT" -ge 5 ]; then
    OVERALL='V2_PASS'
elif [ "$PASS_COUNT" -ge 3 ]; then
    OVERALL='V2_PARTIAL'
fi
if [ "$EARLY_STOP" = "1" ]; then
    OVERALL='V2_FAIL_EARLY_STOP'
fi
# Distinguish eval_crashed from parity_failed (L20 lesson)
if [ "$FINAL_HS" = "null" ] && [ "$FINAL_MM" = "null" ] && [ "$FINAL_TQ" = "null" ] && [ "$EARLY_STOP" != "1" ]; then
    OVERALL='V2_EVAL_CRASHED'
fi

POD_KILL_404='false'
if [ -f "$POD_INFO" ]; then
    POST=$(jq -r '.post_kill_status // ""' "$POD_INFO" 2>/dev/null)
    if echo "$POST" | grep -qiE 'not found|404|no such|does not exist'; then
        POD_KILL_404='true'
    fi
fi

jq -n \
    --arg cycle "clm_v4_lora_sft_2026_05_05" \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg model "$HF_BASE_REPO + LoRA (r=32 a=64 dropout=0.05 self-attn-only qkvo×16; lr=3e-5; steps=6000; bs=8 ga=4 ctx=512)" \
    --arg pod "$POD_ID" \
    --argjson kill_404 "$POD_KILL_404" \
    --arg overall "$OVERALL" \
    --arg fclm1 "$FCLM1" --arg fclm2 "$FCLM2" --arg fclm3 "$FCLM3" --arg fclm4 "$FCLM4" --arg fclm5 "$FCLM5" \
    --arg differentiator "$DIFFERENTIATOR" \
    --arg fhs "$FINAL_HS" --arg fmm "$FINAL_MM" --arg ftq "$FINAL_TQ" --arg comp "$CLM_COMPOSITE" \
    --arg lp_comp "$LP_COMPOSITE" \
    --arg phi_pre "$PHI_BASELINE_PRE" --arg phi_post "$PHI_POST" --arg phi_drift "$PHI_DRIFT_PP" \
    --arg fi "$FORGETTING_INDEX" --arg adp "$ADAPTER_SIZE_MB" \
    --arg inter2k "$INTER_HS_2K" --arg inter4k "$INTER_HS_4K" --arg inter6k "$INTER_HS_6K" \
    --argjson wall "$FINAL_ELAPSED_MIN" \
    --argjson cost "$FINAL_COST" \
    --argjson complete "$COMPLETE" \
    --argjson early_stop "$EARLY_STOP" \
    '{
        schema: "anima/clm_v4_lora_sft/verdict/1",
        cycle: $cycle, ts_utc: $ts,
        bg_lane: "BG-CLM-2-EXEC",
        spec_source: "docs/clm_v4_lora_sft_spec_2026_05_04.md (LANDED 2026-05-04)",
        comparator_left: "state/clm_v4_baseline_eval_2026_05_05/verdict.json (CLM v4 baseline)",
        comparator_right: "state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json (Llama Path A v2)",
        model: $model,
        pod_id: $pod, pod_terminated: true, pod_kill_verified_404: $kill_404,
        rehearsal_mix: {anima_axis_pct: 60, academic_distill_pct: 30, chat_template_pct: 10, total_samples: 50000},
        hyperparameters: {r: 32, alpha: 64, dropout: 0.05, lr: 3e-5, max_steps: 6000, save_steps: 1000, per_device_batch: 8, grad_accum: 4, eff_batch: 32, ctx: 512, bf16: true, target_modules: "self-attn qkvo on decoder.blocks.{0..15}.attn.* (cross_attn EXCLUDED)"},
        intermediate_eval_hs_acc_norm: {step_2000: $inter2k, step_4000: $inter4k, step_6000: $inter6k, threshold_5pp_drop: 0.205},
        final_eval_step_6000: {
            hellaswag: {acc_norm: $fhs, baseline_acc_norm: 0.255, base_carry_substrate: 41.86},
            mmlu:      {acc: $fmm, baseline_acc: 0.255},
            triviaqa:  {exact_match: $ftq, baseline_em: 0.000}
        },
        f1_v3_composite: {
            clm_v4_lora: $comp,
            llama_path_a_v2: $lp_comp,
            differentiator: $differentiator,
            note: "composite = (HS_acc_norm + MM_acc + TQ_em)/3; PASS = clm_v4_lora >= llama_path_a_v2"
        },
        phi_star: {
            substrate_carry: 41.86,
            ckpt_best_phi: 37.27,
            pre_lora_proxy: $phi_pre,
            post_lora_proxy: $phi_post,
            drift_pp: $phi_drift,
            note: "in-pod proxy via logits.std on calibration prompts; canonical φ★ requires anima_phi_v3_canonical.hexa Mac-side"
        },
        forgetting_index_pre_lora_baseline: 0.255,
        forgetting_index_post_lora_hs: $fi,
        adapter_size_mb: $adp,
        F_CLM_LORA_1_forgetting_index: $fclm1,
        F_CLM_LORA_2_F1_v3_composite_vs_llama: $fclm2,
        F_CLM_LORA_2_C_CLM_LORA_2_differentiator: $differentiator,
        F_CLM_LORA_3_adapter_lt_500MB: $fclm3,
        F_CLM_LORA_4_axis_conditioning_preserved: $fclm4,
        F_CLM_LORA_5_shim_v4_hf_format_compat: $fclm5,
        verdict: $overall,
        wall_time_min: $wall,
        wall_time_h: ($wall / 60.0),
        actual_cost_usd: $cost,
        budget_target_usd: 10,
        budget_hard_cap_usd: 15,
        complete_sentinel_detected: ($complete == 1),
        early_stop_sentinel_detected: ($early_stop == 1),
        lessons_applied: {
            L3_auto_kill: "trap _kill_pod EXIT INT TERM; runpodctl pod stop+delete; 404 verify",
            L9_hf_whoami_preflight: "stage0b /api/whoami-v2 fail-fast at $0",
            L13_trap_pre_kill_scp: "trap rescues results via bounded-timeout scp before runpodctl pod stop",
            L20_eval_crashed_distinct_from_parity_failed: "V2_EVAL_CRASHED if all 3 final eval scores null + no early-stop; do NOT conflate with parity FAIL",
            phi_star_flip_mitigation: "target_modules excludes cross_attn / tension_proj / heads; r=32 small footprint; lr=3e-5 conservative"
        },
        honest_c3: [
            "target_modules uses full module paths decoder.blocks.{0..15}.attn.{q,k,v,o}_proj to avoid PEFT name-match collision with cross_attn (which has same projection names) — verified at train start via assert n_cross_attn_lora_modules==0; if PEFT version regression breaks the explicit-path matching, LoRA could silently attach to cross_attn and corrupt φ★. Mitigation: assert in train.py.",
            "φ★ post-LoRA is measured via an in-pod logit-std proxy, NOT the canonical anima_phi_v3 formula (which requires Mac-side hexa runtime). The +41.86 substrate carry is therefore NOT directly comparable to post-LoRA proxy; only relative drift (pre-LoRA proxy vs post-LoRA proxy) is meaningful here. Canonical φ★ measurement deferred to post-cycle Mac-side hexa run.",
            "CLM v4 baseline anchors are limit=200 (HS=0.255, MM=0.255, TQ=0.000) at random-floor per CONFIRMED_RANDOM_FLOOR. Post-LoRA evaluation also limit=200 for matched comparison; stderr ~3pp on HS/TQ means Δ within 1-σ is noise-bounded. Llama Path A v2 retry-3 used limit=200 too (consistent). Wider stderr than limit=500 baseline; absolute deltas within ±3pp on HS may flip on re-run.",
            "Llama Path A v2 composite (LP_COMPOSITE = (0.645+0.575+0.455)/3 = 0.5583) is computed from retry-3 eval-rerun on adapter_final at step=6000. Apples-to-apples comparison ONLY if we match same task list, same nshot config, same lm-eval version; spec deviation possible if H100 lm-eval differs from retry-3's pinned 0.4.11. Pin matched in run_h100.bash.",
            "CLM v4 was NEVER SFT'd, NEVER RLHF'd before this cycle. The 60/30/10 mix is a generic rehearsal recipe, not substrate-curated. The 5% consciousness-coupled slice (slice D) per spec §2.1 was NOT prepared this cycle (would require new tooling); only the 60/30/10 from sister Path A v2 corpus is used. F-CLM-LORA-4 axis preservation risk is therefore unmitigated by slice D.",
            "Single-seed (20260504) v2 cycle. No multi-seed ensemble. Path A v1 already taught that single-seed verdicts are noisy at 1-2pp scale.",
            "max_seq_len=512 hard-cap on CLM v4 — many slice-A anima examples (sharegpt-derived) overflow 512 SPM tokens; SFTTrainer truncates from right. Truncation rate not measured this cycle (no pre-tokenize audit); if rate >50%, effective rehearsal coverage compromised. Mitigation: deferred audit in TRAIN_DONE.json post-mortem.",
            "In-pod φ★ proxy uses logits.std as a crude integration measure; this is NOT structurally equivalent to the φ★ formula in anima_phi_v3_canonical.hexa (which uses partition-mutual-info on internal states). True φ★-flip detection must be done Mac-side post-cycle; in-pod proxy is heuristic only and may fail to detect a genuine flip.",
            "adapter_size_mb measured against safetensors only; lora_config.json + tokenizer files add ~5MB; total push payload ~< adapter_size_mb + 5MB.",
            "Cost estimate $6-10 assumes ~2-2.5h wall on H100 SXM. If pod boot delays + first-time HF mk2 download (5.4GB) + corpus mix HF downloads add >30 min overhead, cost may approach $12 (4h × $2.99). Hard cap $15 absorbs 25% slack on 4h."
        ]
    }' > "$VERDICT"

log "verdict=$OVERALL F-CLM-LORA-1=$FCLM1 F-CLM-LORA-2=$FCLM2 F-CLM-LORA-3=$FCLM3 F-CLM-LORA-4=$FCLM4 F-CLM-LORA-5=$FCLM5 differentiator=$DIFFERENTIATOR wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
log "final: HS=$FINAL_HS MM=$FINAL_MM TQ=$FINAL_TQ composite=$CLM_COMPOSITE  vs  Llama=$LP_COMPOSITE  φ★_drift=$PHI_DRIFT_PP  adapter=${ADAPTER_SIZE_MB}MB"
hb "verdict=$OVERALL"
echo "__P9_CLM_V4_LORA_SFT__ $OVERALL" | tee -a "$RUN_LOG"
exit 0
