#!/usr/bin/env bash
# Phase E main protocol orchestrator — Mac-side
# raw#9 transient bash (orchestrates hexa + transient_py per session memory)
# raw#10 honest C3:
#   - This script does NOT replace impedance_validate; it CALLS it.
#   - LSL marker stream + EEG capture run as parallel processes; clock-drift
#     within each process is bounded by macOS monotonic clock — but cross-
#     process latency is verified post-hoc by F-PHASE-E-2 in the analysis pipe.
#   - 5-min eyes-closed + 5-min eyes-open baselines are SKIPPED here because
#     berger_ec_60s.npy + berger_eo_60s.npy are already captured 2026-05-05.
#     If user wants fresh baselines, set RECAPTURE_BASELINES=1 in env.
#   - Sound notification "say" depends on macOS TTS; harmless if absent.
#
# USAGE
#   bash state/anima_phase_e_eeg_live_2026_05_05/main_protocol_run.bash
#   RECAPTURE_BASELINES=1 bash state/.../main_protocol_run.bash    # fresh EC+EO

set -uo pipefail

CYCLE_DIR="/Users/ghost/core/anima/state/anima_phase_e_eeg_live_2026_05_05"
PROMPTS="$CYCLE_DIR/main_protocol_prompts.jsonl"
STIM_LOG="$CYCLE_DIR/main_protocol_stimulus_log.jsonl"
EEG_OUT="$CYCLE_DIR/phase_e_main_15min.npy"
EEG_DURATION_S=900   # 15 min
LSL_STREAM="anima_phase_e_markers"
PORT="${EEG_PORT:-/dev/cu.usbserial-DP04WGIQ}"
ANIMA_ROOT="/Users/ghost/core/anima"

cd "$ANIMA_ROOT"

echo "── Phase E main protocol launcher ──"
echo "cycle_dir:      $CYCLE_DIR"
echo "prompts:        $PROMPTS  (n=300 axis-conditioned)"
echo "eeg_out:        $EEG_OUT  ($EEG_DURATION_S s)"
echo "stim_log:       $STIM_LOG"
echo "lsl_stream:     $LSL_STREAM"
echo "eeg_port:       $PORT"
echo "recapture_baselines: ${RECAPTURE_BASELINES:-0}"
echo

# ── Step 0: Pre-flight gate — prompts file exists ─────────────────────────
if [[ ! -f "$PROMPTS" ]]; then
    echo "[abort] main_protocol_prompts.jsonl missing at $PROMPTS"
    exit 2
fi
N_PROMPTS=$(wc -l < "$PROMPTS" | tr -d ' ')
echo "[step0] prompts file present, n=$N_PROMPTS"
if [[ "$N_PROMPTS" -lt 300 ]]; then
    echo "[warn] prompts < 300; spec target N=300 reading-task epochs"
fi

# ── Step 1: Pre-flight — impedance recheck (mandatory per §4) ─────────────
echo
echo "[step1] impedance recheck — 16 ch GREEN goal, T7/T8/P7/P8 mandatory"
echo "        running: hexa-brain eeg impedance-validate --measure --port $PORT"
IMPEDANCE_LOG="$CYCLE_DIR/impedance_main_protocol.log"
hexa-brain eeg impedance-validate --measure --port "$PORT" 2>&1 | tee "$IMPEDANCE_LOG" | tail -20
IMP_RC=${PIPESTATUS[0]}
if [[ "$IMP_RC" -ne 0 ]] || ! grep -q "VERIFIED\|GREEN\|OK" "$IMPEDANCE_LOG"; then
    if command -v say >/dev/null 2>&1; then
        say -v Yuna -r 180 "임피던스 검증 실패. 헬멧 재조절 필요" || true
    fi
    echo "[abort] impedance verification failed; reseat electrodes per B-track v7 runbook"
    echo "        anima-eeg/docs/electrode_reseat_b_track_runbook_2026_05_03.md"
    exit 3
fi
echo "[step1] impedance VERIFIED"

# ── Step 2: Optional baseline re-capture ──────────────────────────────────
if [[ "${RECAPTURE_BASELINES:-0}" == "1" ]]; then
    echo
    echo "[step2] re-capturing baselines (EC + EO 5min each)"
    if command -v say >/dev/null 2>&1; then
        say -v Yuna -r 180 "5분 눈 감기 시작" || true
    fi
    hexa run anima-eeg/collect.hexa \
        --collect --duration 300 --tag phase_e_ec_5min \
        --output "$CYCLE_DIR/phase_e_ec_5min.npy" \
        --port "$PORT" --board cyton_daisy 2>&1 | tail -5
    if command -v say >/dev/null 2>&1; then
        say -v Yuna -r 180 "5분 눈 감기 종료. 5분 눈 뜨기 시작" || true
    fi
    hexa run anima-eeg/collect.hexa \
        --collect --duration 300 --tag phase_e_eo_5min \
        --output "$CYCLE_DIR/phase_e_eo_5min.npy" \
        --port "$PORT" --board cyton_daisy 2>&1 | tail -5
    echo "[step2] baselines re-captured"
else
    echo
    echo "[step2] baselines skipped (already at berger_ec_60s.npy + berger_eo_60s.npy)"
fi

# ── Step 3: Stimulus presenter + EEG capture in parallel (LSL marker sync) ─
echo
echo "[step3] launching stimulus presenter + EEG capture (15min, LSL marker sync)"
if command -v say >/dev/null 2>&1; then
    say -v Yuna -r 180 "Phase E 본 protocol 측정 시작. 15분 독서 과제" || true
fi

# Launch presenter in BG
.venv-eeg/bin/python tool/transient_py/anima_phase_e_stimulus_presenter.py \
    --prompts "$PROMPTS" \
    --output  "$STIM_LOG" \
    > "$CYCLE_DIR/main_protocol_stimulus_presenter.log" 2>&1 &
STIM_PID=$!
echo "[step3] presenter pid=$STIM_PID"

# Tiny settle so LSL outlet is live before EEG capture starts (best-effort sync)
sleep 0.5

# EEG capture (foreground — blocks until duration elapses)
# NOTE: collect.hexa here captures direct via BrainFlow (not LSL inlet); the
# LSL marker stream is emitted by the presenter for the *analysis-side* sync
# (post-hoc F-PHASE-E-2 verification). Direct BrainFlow capture is preferred
# because it avoids LSL inlet jitter on the EEG side.
hexa run anima-eeg/collect.hexa \
    --collect --duration "$EEG_DURATION_S" --tag phase_e_main_15min \
    --output "$EEG_OUT" \
    --port "$PORT" --board cyton_daisy 2>&1 | tail -10
EEG_RC=${PIPESTATUS[0]}

# Wait for presenter to drain remaining sentences (or timeout)
echo "[step3] waiting for presenter to finish..."
wait "$STIM_PID"
STIM_RC=$?

if [[ "$EEG_RC" -ne 0 ]]; then
    echo "[warn] EEG capture exited rc=$EEG_RC"
fi
if [[ "$STIM_RC" -ne 0 ]]; then
    echo "[warn] stimulus presenter exited rc=$STIM_RC (130=user_abort)"
fi

# ── Step 4: Optional 5-min post-task rest ─────────────────────────────────
if [[ "${SKIP_POST_REST:-0}" != "1" ]]; then
    echo
    echo "[step4] 5-min post-task rest"
    if command -v say >/dev/null 2>&1; then
        say -v Yuna -r 180 "5분 휴식 시작. 눈 감으세요" || true
    fi
    hexa run anima-eeg/collect.hexa \
        --collect --duration 300 --tag phase_e_post_rest_5min \
        --output "$CYCLE_DIR/phase_e_post_rest_5min.npy" \
        --port "$PORT" --board cyton_daisy 2>&1 | tail -5
fi

# ── Step 5: Wrap ──────────────────────────────────────────────────────────
echo
echo "[done] Phase E main protocol capture complete"
echo "  eeg:           $EEG_OUT"
echo "  stim_log:      $STIM_LOG"
echo "  presenter_log: $CYCLE_DIR/main_protocol_stimulus_presenter.log"
if command -v say >/dev/null 2>&1; then
    say -v Yuna -r 180 "Phase E 본 protocol 측정 종료" || true
fi

# Honest C3 — analysis pipeline NOT executed by this script.
# Run §7 pipeline manually (P0 validate → P5 verdict) per spec, hexa-on-Mac
# where possible + ubu1 helper for ICA/coherence per session memory.
echo
echo "next: run analysis pipeline per docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md §7"
echo "      (P0 validate → P1 preprocess → P2 epoch → P3 coherence → P4 F-PHASE-E-1 → P5 F-PHASE-E-2 → P6 verdict)"

exit 0
