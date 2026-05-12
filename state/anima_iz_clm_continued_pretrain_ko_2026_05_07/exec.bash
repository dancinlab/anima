#!/bin/bash
# emitted by tool/clm_v4_lora_train_orchestrator.hexa — CLM v4 + LoRA SFT lifecycle
# raw#9 sibling-pattern Mac-side bash; raw#37 H100 transient py.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/anima_iz_clm_continued_pretrain_ko_2026_05_07'
RESULTS_DIR='/Users/ghost/core/anima/state/anima_iz_clm_continued_pretrain_ko_2026_05_07/results'
CORPUS_DIR='/Users/ghost/core/anima/state/anima_iz_clm_continued_pretrain_ko_2026_05_07/corpus'
CORPUS_LOCAL='/Users/ghost/core/anima/state/anima_ko_chat_corpus_2026_05_06/corpus_ko_chat_template.txt'
# 261MB Korean conversational mass — chosen for continued-pretrain mass per spec.md §Corpus.
# Lesson Q reconciliation: this is NOT SFT; corpus is ingested as raw next-token CE.
# raw#82 retraction-aware: Korean 30M corpus already exhaustively tested in BG-JZ-FT (full SFT FAIL); BG-IZ uses LARGER 261MB AND different objective (continued-pretrain not SFT).
TRAIN_PY='/Users/ghost/core/anima/tool/transient_py/anima_iz_clm_continued_pretrain.py'
POD_INFO='/Users/ghost/core/anima/state/anima_iz_clm_continued_pretrain_ko_2026_05_07/pod_info.json'
VERDICT='/Users/ghost/core/anima/state/anima_iz_clm_continued_pretrain_ko_2026_05_07/verdict.json'
RUN_LOG='/Users/ghost/core/anima/state/anima_iz_clm_continued_pretrain_ko_2026_05_07/run.log'
HEARTBEAT='/Users/ghost/core/anima/state/anima_iz_clm_continued_pretrain_ko_2026_05_07/heartbeat.txt'
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

# ── Pre-flight: Korean corpus must exist locally ──
if [ ! -f "$CORPUS_LOCAL" ]; then
    log "FATAL: corpus missing: $CORPUS_LOCAL"
    exit 2
fi
CORPUS_SIZE=$(du -sh "$CORPUS_LOCAL" | awk '{print $1}')
log "corpus OK ($CORPUS_SIZE: $CORPUS_LOCAL)"

# ── Stage 1: boot H100 SECURE on-demand (vol=120GB, disk=100GB) ──
POD_NAME='anima-iz-clm-continued-pretrain-2026-05-07'
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
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed" '{cycle:"anima_iz_clm_continued_pretrain_ko_2026_05_07",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
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
            "root@$SSH_HOST:/workspace/anima_iz_pretrain/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 || true
        timeout 30 scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P "$SSH_PORT" \
            "root@$SSH_HOST:/workspace/anima_iz_pretrain/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>&1 | tail -1 || true
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

# ── Stage 3: ship Korean corpus 261MB + transient py + run_h100 ──
log "shipping Korean corpus ($CORPUS_SIZE) + train.py + run_h100.bash"
hb "stage3_setup_starting"
$SSH 'mkdir -p /workspace/anima_iz_pretrain/{corpus,results,ckpts,sentinels}'
$SCP "$CORPUS_LOCAL" "root@$SSH_HOST:/workspace/anima_iz_pretrain/corpus/corpus_ko_chat_template.txt" 2>&1 | tail -1
$SCP "$TRAIN_PY" "root@$SSH_HOST:/workspace/anima_iz_pretrain/anima_iz_train.py" 2>&1 | tail -1
$SCP "/Users/ghost/core/anima/state/anima_iz_clm_continued_pretrain_ko_2026_05_07/run_h100.bash" "root@$SSH_HOST:/workspace/anima_iz_pretrain/run_h100.bash" 2>&1 | tail -1
$SSH 'chmod +x /workspace/anima_iz_pretrain/run_h100.bash'

log "launching H100 pipeline (corpus + train + intermediate eval + final eval)"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/anima_iz_pretrain/hf_token.env && cd /workspace/anima_iz_pretrain && set -a && . hf_token.env && set +a && setsid nohup bash run_h100.bash < /dev/null > orchestrator.log 2>&1 & echo $! > run.pid; disown $! 2>/dev/null || true; sleep 2; cat run.pid' < /dev/null
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

    PROBE=$($SSH 'ls /workspace/anima_iz_pretrain/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ls /workspace/anima_iz_pretrain/results/EARLY_STOP.sentinel 2>/dev/null && echo EARLY_STOP_FOUND; ps -p $(cat /workspace/anima_iz_pretrain/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1; tail -1 /workspace/anima_iz_pretrain/orchestrator.log 2>/dev/null' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|' | head -c 240)"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST}"

    # incremental sync: small JSONs + log
    $SCP -r "root@$SSH_HOST:/workspace/anima_iz_pretrain/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/anima_iz_pretrain/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync FIRST then auto-kill"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/anima_iz_pretrain/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        $SCP -r "root@$SSH_HOST:/workspace/anima_iz_pretrain/ckpts/final" "$RESULTS_DIR/adapter_final" 2>&1 | tail -3 || true
        break
    fi
    if echo "$PROBE" | grep -q EARLY_STOP_FOUND; then
        log "EARLY_STOP.sentinel detected (F-CLM-LORA-1 forgetting OR φ★-flip) — final sync + kill"
        EARLY_STOP=1
        $SCP -r "root@$SSH_HOST:/workspace/anima_iz_pretrain/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        # Pull any partial adapter for post-mortem
        $SCP -r "root@$SSH_HOST:/workspace/anima_iz_pretrain/ckpts" "$RESULTS_DIR/ckpts_partial" 2>&1 | tail -3 || true
        break
    fi

    sleep $POLL_INTERVAL
done

# ── Stage 5: pod kill via trap (auto on exit) ──


# ── Stage 6: verdict (BG-IZ continued-pretrain — simplified vs SFT parent) ──
log "computing BG-IZ verdict"
FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")

# Read sentinel to determine train outcome
SENTINEL_OK="false"
TRAIN_RC="null"
if [ -f "$RESULTS_DIR/COMPLETE.sentinel" ]; then
    SENTINEL_OK=$(jq -r '.ok' "$RESULTS_DIR/COMPLETE.sentinel" 2>/dev/null || echo "false")
    TRAIN_RC=$(jq -r '.train_rc // "null"' "$RESULTS_DIR/COMPLETE.sentinel" 2>/dev/null || echo "null")
fi

# Read pre/post phi-star proxies if available
PHI_PRE="null"
PHI_POST="null"
PHI_DRIFT="null"
if [ -f "$RESULTS_DIR/phi_star_pre_pretrain.json" ]; then
    PHI_PRE=$(jq -r '.phi_star_proxy_pre_pretrain // "null"' "$RESULTS_DIR/phi_star_pre_pretrain.json")
fi
if [ -f "$RESULTS_DIR/phi_star_post_pretrain.json" ]; then
    PHI_POST=$(jq -r '.phi_star_proxy_post_pretrain // "null"' "$RESULTS_DIR/phi_star_post_pretrain.json")
fi
if [ "$PHI_PRE" != "null" ] && [ "$PHI_POST" != "null" ]; then
    PHI_DRIFT=$(awk -v a="$PHI_PRE" -v b="$PHI_POST" 'BEGIN{printf "%.4f", b - a}')
fi

# F-IZ-1: train completed without crash + final ckpt present
FIZ1="FAIL"
if [ "$SENTINEL_OK" = "true" ] && [ -f "$RESULTS_DIR/ckpt_final.pt" ]; then
    FIZ1="PASS"
fi

# F-IZ-2: post-pretrain Korean coherence smoke (samples in phi_star_post_pretrain.json)
# Heuristic: if any sample has han_ratio >= 0.30, mark PASS-CANDIDATE (manual eval needed)
FIZ2="PENDING_MANUAL"
if [ -f "$RESULTS_DIR/phi_star_post_pretrain.json" ]; then
    HAN_OK=$(python3 -c "
import json, re
d = json.load(open('$RESULTS_DIR/phi_star_post_pretrain.json'))
samples = d.get('samples', [])
ok = False
for s in samples:
    r = s.get('response','')
    if r:
        han = len(re.findall(r'[가-힯]', r)) / max(1, len(r))
        if han >= 0.30:
            ok = True
            break
print('YES' if ok else 'NO')
" 2>/dev/null || echo "NO")
    if [ "$HAN_OK" = "YES" ]; then
        FIZ2="PASS_CANDIDATE_MANUAL_REVIEW_NEEDED"
    else
        FIZ2="LIKELY_FAIL_NO_KO_30PCT"
    fi
fi

# F-IZ-3: cost discipline
FIZ3="PASS"
if (( $(awk "BEGIN{print ($FINAL_COST > $BUDGET_HARD_CAP) ? 1 : 0}") )); then
    FIZ3="FAIL_OVER_BUDGET"
fi

OVERALL="PARTIAL"
if [ "$FIZ1" = "PASS" ] && [ "$FIZ2" = "PASS_CANDIDATE_MANUAL_REVIEW_NEEDED" ]; then
    OVERALL="TRAINING_COMPLETED_KO_SAMPLES_PRESENT_AWAITING_V4_EVAL"
elif [ "$FIZ1" = "PASS" ] && [ "$FIZ2" = "LIKELY_FAIL_NO_KO_30PCT" ]; then
    OVERALL="TRAINING_COMPLETED_NO_KO_COHERENCE_LESSON_L_EXTENDED"
elif [ "$FIZ1" = "FAIL" ]; then
    OVERALL="TRAINING_FAILED_INFRASTRUCTURE"
fi

jq -n \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg cycle "anima_iz_clm_continued_pretrain_ko_2026_05_07" \
    --arg overall "$OVERALL" \
    --arg fiz1 "$FIZ1" --arg fiz2 "$FIZ2" --arg fiz3 "$FIZ3" \
    --arg phi_pre "$PHI_PRE" --arg phi_post "$PHI_POST" --arg phi_drift "$PHI_DRIFT" \
    --arg wall "$FINAL_ELAPSED_MIN" --arg cost "$FINAL_COST" \
    --argjson complete "$COMPLETE" --argjson early_stop "$EARLY_STOP" \
    '{
        schema: "anima/bg_iz/verdict/1",
        bg_id: "BG-IZ",
        cycle: $cycle,
        ts_utc: $ts,
        verdict: $overall,
        falsifiers: {
            "F-IZ-1_train_completed": $fiz1,
            "F-IZ-2_ko_coherence_smoke": $fiz2,
            "F-IZ-3_cost_discipline": $fiz3
        },
        phi_star_proxy: {
            pre_pretrain: ($phi_pre | tonumber? // null),
            post_pretrain: ($phi_post | tonumber? // null),
            drift: ($phi_drift | tonumber? // null)
        },
        runtime: {
            wall_min: ($wall | tonumber),
            cost_usd: ($cost | tonumber),
            complete_sentinel: ($complete == 1),
            early_stop_sentinel: ($early_stop == 1)
        },
        next_action: (
            if $overall == "TRAINING_COMPLETED_KO_SAMPLES_PRESENT_AWAITING_V4_EVAL" then
                "Run V4 strict evaluator on phi_star_post_pretrain.json samples + sweep more prompts via mac inference of ckpt_final.pt"
            elif $overall == "TRAINING_COMPLETED_NO_KO_COHERENCE_LESSON_L_EXTENDED" then
                "Lesson L extends to continued-pretrain regime — pivot to P2 BG-JA-EXT (foundation borrow) or P4 arch redesign"
            elif $overall == "TRAINING_FAILED_INFRASTRUCTURE" then
                "Re-fire after diagnosing infrastructure failure (check h100_orchestrator.log + train.log)"
            else
                "Manual review required"
            end
        ),
        raw_compliance: ["raw#37 transient_py", "raw#42 N=1 single seed", "raw#86 cost cap $15", "raw#15 additive (no prior BG modified)", "raw#82 retraction-aware (Lesson Q reconciliation explicit in spec)"]
    }' > "$VERDICT"

log "BG-IZ verdict=$OVERALL F-IZ-1=$FIZ1 F-IZ-2=$FIZ2 F-IZ-3=$FIZ3 wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
log "phi_star: pre=$PHI_PRE post=$PHI_POST drift=$PHI_DRIFT"
hb "verdict=$OVERALL"
echo "__BG_IZ_CONTINUED_PRETRAIN__ $OVERALL" | tee -a "$RUN_LOG"
exit 0
