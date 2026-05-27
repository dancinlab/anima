#!/usr/bin/env bash
# DESIGN-1 orchestrator — boots H100, runs F-SHIM-V5-4 fresh-init differential eval, auto-kills.
# Modeled after state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05/orchestrate.bash.
# .own 4 / raw#9 carve-out: single-purpose bash orchestrator (transient).
# own 16 self-validation: register + heartbeat + trap pre-stop deregister + verdict schema.
set -uo pipefail

# ── constants ─────────────────────────────────────────────────────────────
ROOT="/Users/ghost/core/anima"
STATE_DIR="$ROOT/state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05"
RESULTS_DIR="$STATE_DIR/results"
LOGS_DIR="$STATE_DIR/logs"
RUN_LOG="$LOGS_DIR/orchestrator.log"
POD_INFO="$STATE_DIR/pod.json"
VERDICT="$STATE_DIR/verdict.json"
CYCLE_TAG="clm_v4_hf_format_shim_v5_4_design_1_2026_05_05"
BG_LANE="V5-4-DESIGN-1"
TARGET_USD="3.0"
BUDGET_HARD_CAP="3"
MAX_WALL_MIN=55  # 1h hard cap
OD_RATE="2.99"
POD_NAME="anima-shim-v5-4-design-1-fresh-init-2026-05-05"
SSH_KEY="$HOME/.ssh/id_ed25519"

WATCHDOG_REGISTER="$ROOT/tool/h100_register.bash"
WATCHDOG_HB_DIR="$ROOT/state/h100_watchdog/heartbeats"
WATCHDOG_HEXA="$ROOT/tool/h100_cost_watchdog.hexa"

EVAL_PY_SRC="$ROOT/tool/transient_py/clm_v4_shim_v5_4_design_1_eval.py"
RUN_H100_BASH="$STATE_DIR/run_h100.bash"
DECODER_V3_SRC="$ROOT/state/p9_base_validation_h100_2026_05_04/clm_v4_hf/decoder_v3.py"
CONSCIOUS_DECODER_SRC="$ROOT/state/p9_base_validation_h100_2026_05_04/clm_v4_hf/conscious_decoder.py"
TOKENIZER_SRC="$ROOT/state/p9_base_validation_h100_2026_05_04/clm_v4_hf/tokenizer_64k_multilingual.model"
FIXTURE_SRC="$ROOT/state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt"

mkdir -p "$RESULTS_DIR" "$LOGS_DIR"

# ── helpers ───────────────────────────────────────────────────────────────
RUNPODCTL="/opt/homebrew/bin/runpodctl"
START_EPOCH=$(date -u +%s)

log() {
    local ts="$(date -u +%FT%TZ)"
    echo "[$ts] $*" | tee -a "$RUN_LOG"
}
hb() {
    if [ -d "$WATCHDOG_HB_DIR" ]; then
        echo "$(date -u +%FT%TZ) $*" > "$WATCHDOG_HB_DIR/$BG_LANE.txt" 2>/dev/null || true
    fi
}
redact_hf() {
    sed -E 's/(hf_[A-Za-z0-9]{16,})/hf_***REDACTED***/g'
}

log "starting DESIGN-1 orchestrator: cycle=$CYCLE_TAG bg_lane=$BG_LANE target=\$$TARGET_USD"
hb "stage0_starting"

# ── Stage 0: secrets (CLI does NOT take --raw — plain `secret get`) ──────
log "loading secrets"
RUNPOD_API_KEY=$(/Users/ghost/core/secret/bin/secret get runpod.api_key 2>/dev/null)
HF_TOKEN_LOCAL=$(/Users/ghost/core/secret/bin/secret get huggingface.token 2>/dev/null)
if [ -z "${RUNPOD_API_KEY:-}" ] || [ -z "${HF_TOKEN_LOCAL:-}" ]; then
    log "FATAL: secrets unavailable (runpod=${#RUNPOD_API_KEY}b hf=${#HF_TOKEN_LOCAL}b)"
    exit 2
fi
case "$RUNPOD_API_KEY" in
    \*\*\**) log "FATAL: runpod secret returned redacted form"; exit 2;;
esac
case "$HF_TOKEN_LOCAL" in
    \*\*\**) log "FATAL: hf secret returned redacted form"; exit 2;;
esac
log "secrets OK (runpod=${#RUNPOD_API_KEY}b hf=${#HF_TOKEN_LOCAL}b)"
hb "stage0_secrets_loaded"

export RUNPOD_API_KEY

# ── pre-flight: source files ─────────────────────────────────────────────
for f in "$EVAL_PY_SRC" "$RUN_H100_BASH" "$DECODER_V3_SRC" "$CONSCIOUS_DECODER_SRC" "$TOKENIZER_SRC" "$FIXTURE_SRC"; do
    if [ ! -f "$f" ]; then
        log "FATAL: missing source file: $f"
        exit 2
    fi
done
log "all source files present"

# ── Stage 1: boot pod (H100 80GB SECURE @ $2.99/hr) ───────────────────────
log "booting pod: $POD_NAME (H100 80GB SECURE @ \$$OD_RATE/hr, vol=80GB, disk=60GB)"
hb "stage1_booting_pod"
BOOT_RAW="$LOGS_DIR/boot.raw.tmp"
BOOT_OUT="$LOGS_DIR/boot.log"
$RUNPODCTL create pod \
    --name "$POD_NAME" \
    --gpuType "NVIDIA H100 80GB HBM3" \
    --gpuCount 1 \
    --imageName "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04" \
    --containerDiskSize 60 \
    --volumeSize 80 \
    --volumePath /workspace \
    --ports "22/tcp,8888/http" \
    --secureCloud \
    --startSSH \
    --env "HF_TOKEN=$HF_TOKEN_LOCAL" \
    --cost 3.20 \
    > "$BOOT_RAW" 2>&1
BOOT_RC=$?
redact_hf < "$BOOT_RAW" > "$BOOT_OUT"
rm -f "$BOOT_RAW"
if [ $BOOT_RC -ne 0 ]; then
    log "FATAL: pod boot failed rc=$BOOT_RC"
    cat "$BOOT_OUT" | tee -a "$RUN_LOG"
    cat > "$VERDICT" <<EOF
{
    "schema": "anima/clm_v4_shim_v5_4_design_1/verdict/1",
    "ts_utc": "$(date -u +%FT%TZ)",
    "cycle": "$CYCLE_TAG",
    "bg_lane": "$BG_LANE",
    "verdict": "FAIL",
    "reason": "pod_boot_failed",
    "boot_rc": $BOOT_RC,
    "cost_target_usd": $TARGET_USD,
    "cost_actual_usd": 0.0
}
EOF
    exit 3
fi
log "boot output:"
sed 's/^/  /' "$BOOT_OUT" | tee -a "$RUN_LOG"

POD_ID=$(grep -oE '"[a-z0-9]{14}"' "$BOOT_OUT" | head -1 | tr -d '"')
if [ -z "$POD_ID" ]; then
    POD_ID=$(grep -oE 'pod [a-z0-9]{12,16}' "$BOOT_OUT" | head -1 | awk '{print $2}')
fi
if [ -z "$POD_ID" ]; then
    POD_ID=$(grep -oE '[a-z0-9]{14}' "$BOOT_OUT" | head -1)
fi
if [ -z "$POD_ID" ]; then
    log "FATAL: cannot extract pod_id from boot output"
    cat "$BOOT_OUT" | tee -a "$RUN_LOG"
    exit 4
fi
log "pod_id=$POD_ID"
echo "{\"pod_id\":\"$POD_ID\",\"booted_ts\":\"$(date -u +%FT%TZ)\"}" > "$POD_INFO"
hb "stage1_pod_booted pod_id=$POD_ID"

# ── own 16 watchdog: register ─────────────────────────────────────────────
WATCHDOG_REGISTERED=0
if [ -f "$WATCHDOG_REGISTER" ]; then
    if bash "$WATCHDOG_REGISTER" "$POD_ID" "$BG_LANE" "$TARGET_USD" 2>&1 | tee -a "$RUN_LOG"; then
        WATCHDOG_REGISTERED=1
        log "[watchdog] register OK pod=$POD_ID lane=$BG_LANE target=\$$TARGET_USD"
    else
        log "[watchdog] WARN register failed — proceeding without watchdog"
    fi
fi

# ── kill-on-exit trap ─────────────────────────────────────────────────────
POD_KILL_VERIFIED_404=0
WATCHDOG_DEREGISTERED=0
COST_OVERRUN_2X_ALERTED=0
COMPLETE=0
ELAPSED_MIN=0
ELAPSED_COST="0.00"

_emit_verdict() {
    local FINAL_ELAPSED_MIN=$(( ($(date -u +%s) - START_EPOCH) / 60 ))
    local FINAL_COST=$(awk "BEGIN{printf \"%.2f\", $FINAL_ELAPSED_MIN/60 * $OD_RATE}")
    local OVERRUN_RATIO=$(awk "BEGIN{printf \"%.3f\", $FINAL_COST / $TARGET_USD}")
    if (( $(awk "BEGIN{print ($FINAL_COST > 2.0 * $TARGET_USD) ? 1 : 0}") )); then
        COST_OVERRUN_2X_ALERTED=1
    fi

    local F_VERDICT="INDETERMINATE"
    local LIFT_PP_V5="null"
    local LIFT_PP_V4="null"
    local DELTA_NF="null"
    local DELTA_RF="null"
    local A_V4_NF="null"
    local A_V4_RF="null"
    local A_V5_NF="null"
    local A_V5_RF="null"
    local SUB_DIFF="null"
    local V5_O_PROJ_STD="null"
    local V4_O_PROJ_STD="null"
    local RATIO="null"
    local RATIONALE='[]'
    if [ -f "$RESULTS_DIR/eval_summary.json" ]; then
        F_VERDICT=$(jq -r '.F_SHIM_V5_4_verdict // "INDETERMINATE"' "$RESULTS_DIR/eval_summary.json")
        LIFT_PP_V5=$(jq -r '.lift_pp_v5_via_real_fixture // "null"' "$RESULTS_DIR/eval_summary.json")
        LIFT_PP_V4=$(jq -r '.lift_pp_v4_via_real_fixture // "null"' "$RESULTS_DIR/eval_summary.json")
        DELTA_NF=$(jq -r '.delta_v5_v4_NF_pp // "null"' "$RESULTS_DIR/eval_summary.json")
        DELTA_RF=$(jq -r '.delta_v5_v4_RF_pp // "null"' "$RESULTS_DIR/eval_summary.json")
        A_V4_NF=$(jq -r '.v4_fresh_init_acc_norm // "null"' "$RESULTS_DIR/eval_summary.json")
        A_V4_RF=$(jq -r '.v4_fresh_init_with_real_fixture_acc_norm // "null"' "$RESULTS_DIR/eval_summary.json")
        A_V5_NF=$(jq -r '.v5_fresh_init_acc_norm // "null"' "$RESULTS_DIR/eval_summary.json")
        A_V5_RF=$(jq -r '.v5_fresh_init_with_real_fixture_acc_norm // "null"' "$RESULTS_DIR/eval_summary.json")
        SUB_DIFF=$(jq -r '.substrate_differential_measurable // false' "$RESULTS_DIR/eval_summary.json")
        V5_O_PROJ_STD=$(jq -r '.shim_v5_o_proj_std_observed_mean // "null"' "$RESULTS_DIR/eval_summary.json")
        V4_O_PROJ_STD=$(jq -r '.shim_v4_o_proj_std_observed_mean // "null"' "$RESULTS_DIR/eval_summary.json")
        RATIO=$(jq -r '.ratio_v5_over_v4_o_proj_std // "null"' "$RESULTS_DIR/eval_summary.json")
        RATIONALE=$(jq -c '.F_SHIM_V5_4_rationale // []' "$RESULTS_DIR/eval_summary.json")
    fi

    local CLOSES_PATH_B="false"
    local OWN_15_G3_UPGRADE="false"
    if [ "$F_VERDICT" = "PASS" ]; then
        CLOSES_PATH_B="true"
        OWN_15_G3_UPGRADE="true"
    fi

    cat > "$VERDICT" <<EOF
{
    "schema": "anima/clm_v4_shim_v5_4_design_1/verdict/1",
    "ts_utc": "$(date -u +%FT%TZ)",
    "cycle": "$CYCLE_TAG",
    "bg_lane": "$BG_LANE",
    "spec_anchor": "docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md",
    "phase2_opt_a_carry": "state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json",
    "design": "DESIGN-1: fresh-init forward (no best.pt load), pure architectural differential",
    "pod_id": "$POD_ID",
    "pod_name": "$POD_NAME",
    "pod_kill_verified_404": $( [ "$POD_KILL_VERIFIED_404" = "1" ] && echo true || echo false ),
    "watchdog_registered": $( [ "$WATCHDOG_REGISTERED" = "1" ] && echo true || echo false ),
    "watchdog_deregistered": $( [ "$WATCHDOG_DEREGISTERED" = "1" ] && echo true || echo false ),
    "cost_target_usd": $TARGET_USD,
    "cost_actual_usd": $FINAL_COST,
    "cost_overrun_ratio": $OVERRUN_RATIO,
    "cost_overrun_2x_alerted": $( [ "$COST_OVERRUN_2X_ALERTED" = "1" ] && echo true || echo false ),
    "wall_time_min": $FINAL_ELAPSED_MIN,
    "max_wall_min_cap": $MAX_WALL_MIN,
    "budget_hard_cap_usd": $BUDGET_HARD_CAP,
    "shim_v5_o_proj_std_observed": $V5_O_PROJ_STD,
    "shim_v4_o_proj_std_observed": $V4_O_PROJ_STD,
    "ratio_v5_over_v4_o_proj_std": $RATIO,
    "v4_fresh_init_acc_norm": $A_V4_NF,
    "v5_fresh_init_acc_norm": $A_V5_NF,
    "delta_v5_v4_NF_pp": $DELTA_NF,
    "v4_fresh_init_with_real_fixture_acc_norm": $A_V4_RF,
    "v5_fresh_init_with_real_fixture_acc_norm": $A_V5_RF,
    "delta_v5_v4_RF_pp": $DELTA_RF,
    "lift_pp_v5_via_real_fixture": $LIFT_PP_V5,
    "lift_pp_v4_via_real_fixture": $LIFT_PP_V4,
    "lift_pp_threshold": 5.0,
    "F_SHIM_V5_4_verdict": "$F_VERDICT",
    "F_SHIM_V5_4_rationale": $RATIONALE,
    "substrate_differential_measurable": $SUB_DIFF,
    "closes_path_b_shim_v5_alternative_decisive": $CLOSES_PATH_B,
    "own_15_g3_promote_gate_upgrade_eligible": $OWN_15_G3_UPGRADE,
    "confirmation_falsification_complete": $([ "$COMPLETE" = "1" ] && echo true || echo false),
    "honest_c3": [
        "C1 — Fresh-init untrained: both shim variants are random-weight on hellaswag-200 (5-shot, seed=42). Absolute acc_norm should hover near random-floor (~0.25). The DIFFERENTIAL between v5 and v4 (delta_v5_v4_NF=$DELTA_NF pp, delta_v5_v4_RF=$DELTA_RF pp) is what's being measured — not lift over a trained baseline. PASS verdict requires lift_pp_v5 >= +5pp AND substrate differential measurable above combined stderr.",
        "C2 — Substrate differential measured at random-floor may NOT transfer to trained-weights regime: best.pt's trained o_proj at ~0.0199 OVERWRITES the OPT-A re-init at inference (Phase 2 OPT-A verdict §differential_evidence). DESIGN-1 only proves that std=0.10 produces an architecturally-distinct forward at fresh-init. Trained-weight transfer is unconfirmed and would require OPT-B (retrain at v5 init) or Path B (cross-attn-active SFT).",
        "C3 — Real fixture lift_pp via cross_attn architectural: shim v5 OPT-A o_proj std=0.10 gives 5x-larger cross-attn output magnitude vs v4 std=0.02. With train_avg_real.pt fixture (L2~2.20), the v5 substrate sees 5x more conscious_signal mixed into residual. lift_pp_v5=$LIFT_PP_V5 pp tests whether this scale matters for hellaswag at random-init. lift_pp_v4=$LIFT_PP_V4 pp is the v4-substrate baseline.",
        "C4 — Stderr at limit=200: bootstrap stderr typically ~3pp on acc_norm; combined stderr for differential is sqrt(2)*3pp ≈ 4.2pp. Threshold 5pp is at the noise edge. |lift_pp_v5 - se_pp| comparison is decisive only if magnitude is clear. Verdict path: PASS = lift>=5pp+sigdiff; PARTIAL = sigdiff but lift<5pp; FAIL = no sigdiff or |lift|<se.",
        "C5 — own 15 G3 upgrade eligibility: own_15_g3_promote_gate_upgrade_eligible=$OWN_15_G3_UPGRADE. PASS verdict alone may be INSUFFICIENT for full G3 upgrade — fresh-init evidence does not prove production-trained-weights substrate viability. A complete G3 case requires DESIGN-1 PASS PLUS OPT-B retrain corroboration OR Path B SFT lift, neither of which fall within this BG's scope.",
        "C6 — Cost discipline: target=\$$TARGET_USD, actual=\$$FINAL_COST, ratio=$OVERRUN_RATIO. own 16 watchdog: registered=$WATCHDOG_REGISTERED deregistered=$WATCHDOG_DEREGISTERED pod_kill_verified_404=$POD_KILL_VERIFIED_404 cost_overrun_2x_alerted=$COST_OVERRUN_2X_ALERTED. Auto-kill mandatory at \$$BUDGET_HARD_CAP cap or ${MAX_WALL_MIN}min wall.",
        "C7 — Recipe replicability: hellaswag limit=200, num_fewshot=5, seed=42, init_seed=1234, lm-eval-harness 0.4.11. fp32 path. Both v4 + v5 share the same init_seed (1234) so all weights except the cross_attn.o_proj re-init are bit-identical. This isolates the differential to the o_proj std lever (and downstream deterministic forward consequences thereof)."
    ],
    "raw_compliance": {
        "raw_9": "transient_py used (clm_v4_shim_v5_4_design_1_eval.py + run_h100.bash) — opt-out path",
        "raw_10": "7 honest C3 entries (>=5 required)",
        "raw_15": "additive only — no shim v4/v5 source mutation; Mac shim_v5.py LOCKED at OPT-A std=0.10, eval re-implements OPT-A re-init logic verbatim from the Mac source",
        "raw_71": "F-SHIM-V5-4 +5pp threshold carried verbatim from spec; verdict gate adds substrate_differential_measurable conjunction per spec §3 V5-4",
        "no_git_commit": "OK per BG spec",
        "no_hf_push": "OK — eval-only run, no model upload",
        "no_shim_v4_mutation": "OK — shim v4 source untouched",
        "secret_cli_used": "OK — secret get runpod.api_key + huggingface.token (CLI does not support --raw flag)"
    },
    "next_phase_options": {
        "if_PASS": "DESIGN-1 closes path-B shim v5 alternative at fresh-init. Forward step: OPT-B (retrain CLM v4 with cross_attn.o_proj std=0.10 init scale) to test trained-weights transfer.",
        "if_PARTIAL": "Substrate differential exists but real-fixture lift below 5pp threshold. Forward step: investigate fixture quality (per-prompt harvest vs single fixture broadcast) OR OPT-B retrain.",
        "if_FAIL": "Architecturally no fresh-init differential survives forward path. Forward step: re-examine cross-attn integration (gate_strength=0.001 may be the binding constraint, not o_proj std)."
    }
}
EOF
    log "verdict written: $VERDICT"
}

_kill_pod() {
    if [ -d "$WATCHDOG_HB_DIR" ]; then
        echo "EXITING $(date -u +%FT%TZ) pod=$POD_ID" > "$WATCHDOG_HB_DIR/$BG_LANE.txt" || true
    fi
    log "[trap] killing pod=$POD_ID (auto-kill mandatory)"
    $RUNPODCTL pod stop "$POD_ID" 2>&1 | tee -a "$RUN_LOG" || true
    sleep 3
    $RUNPODCTL pod delete "$POD_ID" 2>&1 | tee -a "$RUN_LOG" || true
    sleep 3
    POST=""
    for vi in 1 2 3; do
        # New CLI: `runpodctl pod get <id>` returns 404 when pod doesn't exist;
        # `runpodctl pod list -o json` is also reliable — pod absent from list = 404.
        POST=$($RUNPODCTL pod get "$POD_ID" -o json 2>&1)
        POST_RC=$?
        # Either: pod get errors out, OR pod absent from list
        IN_LIST=$($RUNPODCTL pod list -o json 2>/dev/null | jq -r --arg id "$POD_ID" '.[] | select(.id == $id) | .id' 2>/dev/null | head -1)
        if [ "$POST_RC" != "0" ] || echo "$POST" | grep -qiE 'not found|404|does not exist|no pod'; then
            POD_KILL_VERIFIED_404=1
            log "[trap] 404 verified via pod-get (try $vi/3)"
            break
        fi
        if [ -z "$IN_LIST" ]; then
            POD_KILL_VERIFIED_404=1
            log "[trap] 404 verified via pod-list absence (try $vi/3)"
            break
        fi
        log "[trap] 404 verify try $vi/3 not yet (in_list='$IN_LIST') — sleep 30s"
        sleep 30
    done
    log "[trap] post-kill: pod_kill_verified_404=$POD_KILL_VERIFIED_404"
    if [ "$POD_KILL_VERIFIED_404" = "1" ] && [ -f "$WATCHDOG_HEXA" ]; then
        if /Users/ghost/core/hexa-lang/hexa run "$WATCHDOG_HEXA" --deregister "$POD_ID" 2>&1 | tee -a "$RUN_LOG"; then
            WATCHDOG_DEREGISTERED=1
            log "[watchdog] deregister OK pod=$POD_ID"
        fi
    fi
    _emit_verdict
}
trap _kill_pod EXIT INT TERM

# ── Stage 2: wait for SSH ────────────────────────────────────────────────
# Use NEW CLI form: `runpodctl pod get <id> -o json --include-machine`
# (deprecated `runpodctl get pod` returns tabular even with -o json on this version).
log "waiting for SSH ready (max 9min)"
hb "stage2_waiting_ssh"
SSH_HOST=""
SSH_PORT=""
INFO=""
SSH_READY=0
for i in $(seq 1 54); do
    INFO=$($RUNPODCTL pod get "$POD_ID" -o json --include-machine 2>/dev/null)
    # Try multiple JSON shapes — runpodctl schema varies across versions.
    SSH_HOST=$(echo "$INFO" | jq -r '
        .ssh.ip
        // .ssh.host
        // .machine.publicIp
        // .machine.podHostId
        // .ip
        // .publicIp
        // empty' 2>/dev/null)
    SSH_PORT=$(echo "$INFO" | jq -r '
        .ssh.port
        // .machine.podPort
        // (.runtime.ports // [] | map(select(.privatePort==22)) | .[0].publicPort)
        // (.ports // [] | map(select(.privatePort==22)) | .[0].publicPort)
        // empty' 2>/dev/null)
    # Fallback: parse from pod list JSON
    if [ -z "$SSH_HOST" ] || [ "$SSH_HOST" = "null" ] || [ -z "$SSH_PORT" ] || [ "$SSH_PORT" = "null" ]; then
        LIST=$($RUNPODCTL pod list -o json 2>/dev/null)
        SSH_HOST=$(echo "$LIST" | jq -r --arg id "$POD_ID" '
            .[] | select(.id == $id) | (
                .ssh.ip
                // .machine.publicIp
                // .publicIp
                // .ip
                // empty
            )' 2>/dev/null | head -1)
        SSH_PORT=$(echo "$LIST" | jq -r --arg id "$POD_ID" '
            .[] | select(.id == $id) | (
                .ssh.port
                // (.runtime.ports // [] | map(select(.privatePort==22)) | .[0].publicPort)
                // (.ports // [] | map(select(.privatePort==22)) | .[0].publicPort)
                // empty
            )' 2>/dev/null | head -1)
    fi
    if [ -n "$SSH_HOST" ] && [ "$SSH_HOST" != "null" ] && [ -n "$SSH_PORT" ] && [ "$SSH_PORT" != "null" ]; then
        if ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
            -o ConnectTimeout=8 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>/dev/null | grep -q READY; then
            log "SSH ready at $SSH_HOST:$SSH_PORT (after ${i} probes)"
            SSH_READY=1
            break
        fi
    fi
    log "  ssh probe $i/54: host=$SSH_HOST port=$SSH_PORT"
    hb "stage2_ssh_probe $i/54"
    sleep 10
done
if [ "$SSH_READY" != "1" ]; then
    log "FATAL: pod never reached SSH ready in 9min"
    log "last INFO json (truncated):"
    echo "$INFO" | head -20 | tee -a "$RUN_LOG"
    log "last LIST json (truncated):"
    $RUNPODCTL pod list -o json 2>/dev/null | head -50 | tee -a "$RUN_LOG"
    exit 5
fi
jq --arg h "$SSH_HOST" --arg p "$SSH_PORT" '. + {ssh_host:$h, ssh_port:($p|tonumber)}' "$POD_INFO" > "$POD_INFO.tmp" && mv "$POD_INFO.tmp" "$POD_INFO"
hb "stage2_ssh_ready host=$SSH_HOST port=$SSH_PORT"

SSH="ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $SSH_PORT root@$SSH_HOST"
SCP="scp -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $SSH_PORT"

# ── Stage 3: scp inputs + eval_py + run_h100.bash ────────────────────────
log "stage 3: setup pod (scp inputs)"
hb "stage3_scp_inputs"
$SSH 'mkdir -p /workspace/clm_v4_shim_v5_4_design_1'
$SCP "$EVAL_PY_SRC"           "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/clm_v4_shim_v5_4_design_1_eval.py" 2>&1 | tail -1
$SCP "$RUN_H100_BASH"          "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/run_h100.bash" 2>&1 | tail -1
$SCP "$DECODER_V3_SRC"         "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/decoder_v3.py" 2>&1 | tail -1
$SCP "$CONSCIOUS_DECODER_SRC"  "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/conscious_decoder.py" 2>&1 | tail -1
$SCP "$TOKENIZER_SRC"          "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/tokenizer_64k_multilingual.model" 2>&1 | tail -1
$SCP "$FIXTURE_SRC"            "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/train_avg_real.pt" 2>&1 | tail -1
$SSH 'chmod +x /workspace/clm_v4_shim_v5_4_design_1/run_h100.bash'
$SSH 'ls -la /workspace/clm_v4_shim_v5_4_design_1/' 2>&1 | tee -a "$RUN_LOG"

log "stage 3b: launching run on H100 (detached via nohup + setsid)"
hb "stage3_launch"
$SSH 'cat /proc/1/environ | tr "\0" "\n" | grep ^HF_TOKEN= > /workspace/clm_v4_shim_v5_4_design_1/hf_token.env && cd /workspace/clm_v4_shim_v5_4_design_1 && set -a && . hf_token.env && set +a && nohup setsid bash run_h100.bash > orchestrator.log 2>&1 < /dev/null & echo $! > run.pid; sleep 2; cat run.pid'

# ── Stage 4: poll loop ───────────────────────────────────────────────────
log "poll loop start (max ${MAX_WALL_MIN}min, budget cap \$$BUDGET_HARD_CAP)"
POLL_INTERVAL=120
while true; do
    NOW=$(date -u +%s)
    ELAPSED_MIN=$(( (NOW - START_EPOCH) / 60 ))
    ELAPSED_HR_DEC=$(awk "BEGIN{printf \"%.4f\", ($NOW - $START_EPOCH) / 3600}")
    ELAPSED_COST=$(awk "BEGIN{printf \"%.2f\", $ELAPSED_HR_DEC * $OD_RATE}")

    if (( $(awk "BEGIN{print ($ELAPSED_COST > $BUDGET_HARD_CAP) ? 1 : 0}") )); then
        log "COST CAP HIT \$$ELAPSED_COST > \$$BUDGET_HARD_CAP — auto-kill"
        break
    fi
    if [ "$ELAPSED_MIN" -ge "$MAX_WALL_MIN" ]; then
        log "WALL CAP HIT ${ELAPSED_MIN}min >= ${MAX_WALL_MIN}min — auto-kill"
        break
    fi

    PROBE=$($SSH 'ls /workspace/clm_v4_shim_v5_4_design_1/results/COMPLETE.sentinel 2>/dev/null && echo SENTINEL_FOUND; ps -p $(cat /workspace/clm_v4_shim_v5_4_design_1/run.pid 2>/dev/null) -o pid,etime,comm 2>/dev/null | tail -1' 2>/dev/null)
    PROBE_LINE=$(echo "$PROBE" | tr '\n' '|')
    log "elapsed=${ELAPSED_MIN}min cost=\$$ELAPSED_COST probe=$PROBE_LINE"
    hb "poll elapsed=${ELAPSED_MIN}min cost=\$$ELAPSED_COST probe=$(echo $PROBE_LINE | head -c 200)"

    $SCP -r "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/results/*.json" "$RESULTS_DIR/" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/orchestrator.log" "$LOGS_DIR/h100_run.log" 2>/dev/null || true
    $SCP "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/run.log" "$LOGS_DIR/h100_run_inner.log" 2>/dev/null || true

    if echo "$PROBE" | grep -q SENTINEL_FOUND; then
        log "COMPLETE.sentinel detected — final sync + auto-kill imminent"
        COMPLETE=1
        $SCP -r "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/results/*" "$RESULTS_DIR/" 2>&1 | tail -3 | tee -a "$RUN_LOG" || true
        $SCP "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/orchestrator.log" "$LOGS_DIR/h100_run.log" 2>&1 | tail -1 || true
        $SCP "root@$SSH_HOST:/workspace/clm_v4_shim_v5_4_design_1/run.log" "$LOGS_DIR/h100_run_inner.log" 2>&1 | tail -1 || true
        break
    fi

    sleep $POLL_INTERVAL
done

log "stage 5: pod kill via trap (auto on exit)"
exit 0
