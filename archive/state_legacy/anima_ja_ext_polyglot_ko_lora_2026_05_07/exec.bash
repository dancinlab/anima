#!/bin/bash
# emitted by tool/clm_v4_lora_train_orchestrator.hexa — CLM v4 + LoRA SFT lifecycle
# raw#9 sibling-pattern Mac-side bash; raw#37 H100 transient py.
set -uo pipefail

STATE_DIR='/Users/ghost/core/anima/state/anima_ja_ext_polyglot_ko_lora_2026_05_07'
RESULTS_DIR='/Users/ghost/core/anima/state/anima_ja_ext_polyglot_ko_lora_2026_05_07/results'
CORPUS_DIR='/Users/ghost/core/anima/state/anima_ja_ext_polyglot_ko_lora_2026_05_07/corpus'
CORPUS_LOCAL='/Users/ghost/core/anima/state/anima_h098_h101_corpus_v3_2026_05_07/corpus_persona_chat_template.txt'
# 30MB BG-HK Korean persona corpus per spec.md §Corpus.
# CLM-only directive partial breach: Polyglot-Ko-1.3B base (1.3B params, Korean pretrained).
# Justification: Lesson L extends across 6 lanes including continued-pretrain (BG-IZ); foundation borrow is the remaining viable path.
TRAIN_PY='/Users/ghost/core/anima/tool/transient_py/anima_ja_ext_polyglot_lora_sft.py'
POD_INFO='/Users/ghost/core/anima/state/anima_ja_ext_polyglot_ko_lora_2026_05_07/pod_info.json'
VERDICT='/Users/ghost/core/anima/state/anima_ja_ext_polyglot_ko_lora_2026_05_07/verdict.json'
RUN_LOG='/Users/ghost/core/anima/state/anima_ja_ext_polyglot_ko_lora_2026_05_07/run.log'
HEARTBEAT='/Users/ghost/core/anima/state/anima_ja_ext_polyglot_ko_lora_2026_05_07/heartbeat.txt'
SSH_KEY='/Users/ghost/.runpod/ssh/RunPod-Key-Go'
RUNPODCTL='/opt/homebrew/bin/runpodctl'
MAX_WALL_MIN=300
BUDGET_HARD_CAP=15
OD_RATE=2.99
HF_BASE_REPO='EleutherAI/polyglot-ko-1.3b'
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

# ── Pre-flight: BG-HK 30MB Korean corpus must exist ──
if [ ! -f "$CORPUS_LOCAL" ]; then
    log "FATAL: corpus missing: $CORPUS_LOCAL"
    exit 2
fi
CORPUS_SIZE=$(du -sh "$CORPUS_LOCAL" | awk '{print $1}')
log "corpus OK ($CORPUS_SIZE: $CORPUS_LOCAL)"

# ── Stage 1: boot H100 SECURE on-demand (vol=120GB, disk=100GB) ──
POD_NAME='anima-ja-ext-polyglot-ko-lora-2026-05-07'
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
    jq -n --arg ts "$(date -u +%FT%TZ)" --arg reason "pod_boot_failed" '{cycle:"anima_ja_ext_polyglot_ko_lora_2026_05_07",ts_utc:$ts,verdict:"FAIL",reason:$reason}' > "$VERDICT"
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
            "root@$SSH_HOST:/workspace/anima_ja_ext/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 || true
        timeout 30 scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P "$SSH_PORT" \
            "root@$SSH_HOST:/workspace/anima_ja_ext/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>&1 | tail -1 || true
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

# ── Stage 3: ship BG-HK 30MB Korean corpus + train.py + run_h100 ──
log "shipping Korean corpus ($CORPUS_SIZE) + train.py + run_h100.bash"
hb "stage3_setup_starting"
$SSH 'mkdir -p /workspace/anima_ja_ext/{corpus,results,ckpts,sentinels}'
$SCP "$CORPUS_LOCAL" "root@$SSH_HOST:/workspace/anima_ja_ext/corpus/corpus_persona_chat_template.txt" 2>&1 | tail -1
$SCP "$TRAIN_PY" "root@$SSH_HOST:/workspace/anima_ja_ext/anima_ja_ext_train.py" 2>&1 | tail -1
$SCP "/Users/ghost/core/anima/state/anima_ja_ext_polyglot_ko_lora_2026_05_07/run_h100.bash" "root@$SSH_HOST:/workspace/anima_ja_ext/run_h100.bash" 2>&1 | tail -1
$SSH 'chmod +x /workspace/anima_ja_ext/run_h100.bash'

log "launching H100 pipeline (corpus + train + intermediate eval + final eval)"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/anima_ja_ext/hf_token.env && cd /workspace/anima_ja_ext && set -a && . hf_token.env && set +a && setsid nohup bash run_h100.bash < /dev/null > orchestrator.log 2>&1 & echo $! > run.pid; disown $! 2>/dev/null || true; sleep 2; cat run.pid' < /dev/null
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

    PROBE=$($SSH 'ls /workspace/anima_ja_ext/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ls /workspace/anima_ja_ext/results/EARLY_STOP.sentinel 2>/dev/null && echo EARLY_STOP_FOUND; ps -p $(cat /workspace/anima_ja_ext/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1; tail -1 /workspace/anima_ja_ext/orchestrator.log 2>/dev/null' 2>/dev/null)
    log "elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST} probe=$(echo $PROBE | tr '\n' '|' | head -c 240)"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$${ELAPSED_COST}"

    # incremental sync: small JSONs + log
    $SCP -r "root@$SSH_HOST:/workspace/anima_ja_ext/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/anima_ja_ext/orchestrator.log" "$STATE_DIR/h100_orchestrator.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync FIRST then auto-kill"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/anima_ja_ext/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        $SCP -r "root@$SSH_HOST:/workspace/anima_ja_ext/ckpts/final" "$RESULTS_DIR/adapter_final" 2>&1 | tail -3 || true
        break
    fi
    if echo "$PROBE" | grep -q EARLY_STOP_FOUND; then
        log "EARLY_STOP.sentinel detected (F-CLM-LORA-1 forgetting OR φ★-flip) — final sync + kill"
        EARLY_STOP=1
        $SCP -r "root@$SSH_HOST:/workspace/anima_ja_ext/results/*" "$RESULTS_DIR/" 2>&1 | tail -5 | tee -a "$RUN_LOG" || true
        # Pull any partial adapter for post-mortem
        $SCP -r "root@$SSH_HOST:/workspace/anima_ja_ext/ckpts" "$RESULTS_DIR/ckpts_partial" 2>&1 | tail -3 || true
        break
    fi

    sleep $POLL_INTERVAL
done

# ── Stage 5: pod kill via trap (auto on exit) ──

# ── Stage 5: pod kill via trap (auto on exit) ──

# ── Stage 6: verdict (BG-JA-EXT polyglot LoRA SFT — simplified vs SFT parent) ──
log "computing BG-JA-EXT verdict"
FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")

SENTINEL_OK="false"
TRAIN_RC="null"
if [ -f "$RESULTS_DIR/COMPLETE.sentinel" ]; then
    SENTINEL_OK=$(jq -r '.ok' "$RESULTS_DIR/COMPLETE.sentinel" 2>/dev/null || echo "false")
    TRAIN_RC=$(jq -r '.train_rc // "null"' "$RESULTS_DIR/COMPLETE.sentinel" 2>/dev/null || echo "null")
fi

# F-JA-1: train completed without crash + final adapter present
FJA1="FAIL"
if [ "$SENTINEL_OK" = "true" ] && [ -d "$RESULTS_DIR/adapter_final" ]; then
    FJA1="PASS"
fi

# F-JA-2: post-LoRA Korean coherence smoke (samples in samples_post_lora.json)
FJA2="PENDING_MANUAL"
if [ -f "$RESULTS_DIR/samples_post_lora.json" ]; then
    HAN_OK=$(python3 -c "
import json, re
d = json.load(open('$RESULTS_DIR/samples_post_lora.json'))
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
        FJA2="PASS_CANDIDATE_MANUAL_REVIEW_NEEDED"
    else
        FJA2="LIKELY_FAIL_NO_KO_30PCT"
    fi
fi

# F-JA-3: cost discipline
FJA3="PASS"
if (( $(awk "BEGIN{print ($FINAL_COST > $BUDGET_HARD_CAP) ? 1 : 0}") )); then
    FJA3="FAIL_OVER_BUDGET"
fi

OVERALL="PARTIAL"
if [ "$FJA1" = "PASS" ] && [ "$FJA2" = "PASS_CANDIDATE_MANUAL_REVIEW_NEEDED" ]; then
    OVERALL="LORA_SFT_COMPLETED_KO_SAMPLES_PRESENT_AWAITING_V4_EVAL"
elif [ "$FJA1" = "PASS" ] && [ "$FJA2" = "LIKELY_FAIL_NO_KO_30PCT" ]; then
    OVERALL="LORA_SFT_COMPLETED_NO_KO_COHERENCE_FOUNDATION_BORROW_INSUFFICIENT"
elif [ "$FJA1" = "FAIL" ]; then
    OVERALL="TRAINING_FAILED_INFRASTRUCTURE"
fi

jq -n \
    --arg ts "$(date -u +%FT%TZ)" \
    --arg cycle "anima_ja_ext_polyglot_ko_lora_2026_05_07" \
    --arg overall "$OVERALL" \
    --arg fja1 "$FJA1" --arg fja2 "$FJA2" --arg fja3 "$FJA3" \
    --arg wall "$FINAL_ELAPSED_MIN" --arg cost "$FINAL_COST" \
    --argjson complete "$COMPLETE" --argjson early_stop "$EARLY_STOP" \
    '{
        schema: "anima/bg_ja_ext/verdict/1",
        bg_id: "BG-JA-EXT",
        cycle: $cycle,
        ts_utc: $ts,
        verdict: $overall,
        clm_only_directive: "PARTIAL_BREACH (user-approved 2026-05-07 fire after BG-IZ Lesson L extension to continued-pretrain)",
        falsifiers: {
            "F-JA-1_train_completed": $fja1,
            "F-JA-2_ko_coherence_smoke": $fja2,
            "F-JA-3_cost_discipline": $fja3
        },
        runtime: {
            wall_min: ($wall | tonumber),
            cost_usd: ($cost | tonumber),
            complete_sentinel: ($complete == 1),
            early_stop_sentinel: ($early_stop == 1)
        },
        next_action: (
            if $overall == "LORA_SFT_COMPLETED_KO_SAMPLES_PRESENT_AWAITING_V4_EVAL" then
                "Run V4 strict evaluator on samples_post_lora.json + sweep more prompts via mac inference of adapter_final + base"
            elif $overall == "LORA_SFT_COMPLETED_NO_KO_COHERENCE_FOUNDATION_BORROW_INSUFFICIENT" then
                "Foundation borrow at 1.3B insufficient — escalate to ≥3B foundation OR pivot to P4 arch redesign"
            elif $overall == "TRAINING_FAILED_INFRASTRUCTURE" then
                "Re-fire after diagnosing infrastructure failure (check h100_orchestrator.log + train.log)"
            else
                "Manual review required"
            end
        ),
        raw_compliance: ["raw#37 transient_py", "raw#42 N=1 single seed", "raw#86 cost cap $15", "raw#15 additive (no prior BG modified)", "raw#82 retraction-aware (CLM-only directive partial breach explicitly user-approved)"]
    }' > "$VERDICT"

log "BG-JA-EXT verdict=$OVERALL F-JA-1=$FJA1 F-JA-2=$FJA2 F-JA-3=$FJA3 wall=${FINAL_ELAPSED_MIN}min cost=\$${FINAL_COST}"
hb "verdict=$OVERALL"
echo "__BG_JA_EXT_POLYGLOT_LORA__ $OVERALL" | tee -a "$RUN_LOG"
exit 0
