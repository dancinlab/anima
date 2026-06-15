#!/usr/bin/env bash
# CLM/train/dispatch_rung.sh — anima-side rung-fire dispatch wrapper.
#
# THE SECOND PIPELINE SURFACE (dojo recipe → THIS cloud dispatch → gauge monitor).
#
# WHY a wrapper (not a reimplementation): pod lifecycle (rent/run/teardown) is owned
# by the hexa cloud `/pod` plugin (`hexa cloud fire|dispatch`). Per the repo boundary
# (a_runpod_inbox · do not lock pod logic in anima), this script does NOT reimplement
# pod management — it WRAPS `hexa cloud fire` and ENCODES the two governance hooks the
# bare plugin call leaves to the caller:
#
#   • a_fire_recover_complete — pull ckpt + result + log + engine .clm + gauges.jsonl
#     + anchors, VERIFY, then HF upload, BEFORE any pod teardown.
#   • a_cpu_local_no_waiter   — poll the remote job INLINE (sleep loop), never await a
#     Monitor/waiter (which only advances in the main loop → stall). Commit-early.
#
# The actual trainer is CLM/train/train_lane_p_3b.py (Lane-P · a_clm_gen_pipeline),
# NOT the legacy train_clm.py. The fire command + recovery checklist are the
# machine-readable contract in CLM/train/fire_3b_rung_qat.hexa (run it to print them:
# `hexa run CLM/train/fire_3b_rung_qat.hexa`). The inline gauges are MONITOR-ONLY
# (a_train_inline_gauge); the FROZEN verdict mounts the emitted .clm on the CORE
# engine post-train (a_engine_measured_verdict) — gauges NEVER gate.
#
# USAGE:
#   bash CLM/train/dispatch_rung.sh <rung> <pod-host> <corpus> [arm] [n_gpu]
#   bash CLM/train/dispatch_rung.sh --print 3b            # dry-print the contract, no fire
#
#   <rung>     3b (d3584/L32/E48) — the rung knobs come from fire_3b_rung_qat.hexa
#   <pod-host> the runpod ssh host already provisioned by `hexa cloud` (this wrapper
#              does NOT rent the pod — provision via the /pod plugin first)
#   <corpus>   remote corpus path for the Lane-P trainer --corpus
#   [arm]      A|B|AB  (seed sweep arm; default A)  [n_gpu] DDP procs (default 2)
#
# COST (a_fire_autonomous — state then dispatch, no user gate):
#   ~$40~120 / ~12~24h wall on H100 80GB ×2~4 (DDP · a_wall_first).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"

RUNG="${1:-3b}"
if [ "$RUNG" = "--print" ]; then
  RUNG="${2:-3b}"
  echo "── rung $RUNG fire contract (from CLM/train/fire_${RUNG}_rung_qat.hexa) ──"
  if command -v hexa >/dev/null 2>&1; then
    hexa run "$REPO/CLM/train/fire_${RUNG}_rung_qat.hexa" || true
  else
    echo "(hexa not on PATH — read CLM/train/fire_${RUNG}_rung_qat.hexa for the dispatch + recover contract)"
  fi
  exit 0
fi

POD_HOST="${2:?need <pod-host> (provision via the /pod plugin first; this wrapper does not rent pods)}"
CORPUS="${3:?need <corpus> remote path for train_lane_p_3b.py --corpus}"
ARM="${4:-A}"
N_GPU="${5:-2}"

# rung knobs (mirror CLM/train/fire_3b_rung_qat.hexa — keep in sync there, the .hexa is SSOT).
case "$RUNG" in
  3b) D_MODEL=3584; N_LAYERS=32; N_EXPERTS=48; STEPS=2000; BASE_SEED=42; GAUGE_EVERY=400 ;;
  *)  echo "unknown rung: $RUNG (only 3b wired here; add knobs from fire_${RUNG}_rung_qat.hexa)"; exit 2 ;;
esac
case "$ARM" in A) SEED=$BASE_SEED ;; B) SEED=$((BASE_SEED+1)) ;; AB) SEED=$((BASE_SEED+2)) ;; *) echo "arm must be A|B|AB"; exit 2 ;; esac

TAG="${RUNG}_${ARM}_s${SEED}"
REMOTE_OUT="out"
HF_REPO="dancinlab/anima-clm-${RUNG}"
LOCAL_PULL="$REPO/state/lane_p_${RUNG}_fire"
mkdir -p "$LOCAL_PULL"

echo "═══ anima rung-fire dispatch (a_fire_autonomous · ~\$40~120 / ~12~24h H100×${N_GPU} DDP) ═══"
echo "  rung=$RUNG arm=$ARM seed=$SEED  d=$D_MODEL L=$N_LAYERS E=$N_EXPERTS steps=$STEPS gauge_every=$GAUGE_EVERY"
echo "  trainer=CLM/train/train_lane_p_3b.py (Lane-P · NOT legacy train_clm.py)"
echo "  pod=$POD_HOST corpus=$CORPUS  HF=$HF_REPO"

# The REAL trainer CLI (matches fire_3b_rung_qat.hexa::fire_cmd).
FIRE_ARGV="torchrun --nproc_per_node=${N_GPU} CLM/train/train_lane_p_3b.py \
  --corpus ${CORPUS} --d-model ${D_MODEL} --n-trunk-layers ${N_LAYERS} \
  --n-experts ${N_EXPERTS} --steps ${STEPS} --seed ${SEED} --bf16 --grad-checkpoint \
  --gauge-every ${GAUGE_EVERY} --gauges-out ${REMOTE_OUT}/gauges_${TAG}.jsonl \
  --ckpt-out ${REMOTE_OUT}/clm_${TAG}.pt --clm-out ${REMOTE_OUT}/clm_${TAG}.clm \
  --json-out ${REMOTE_OUT}/clm_${TAG}.json"

REMOTE_LOG="${REMOTE_OUT}/fire_${TAG}.log"

echo "── (1/4) fire (hexa cloud fire · atomic nohup + auto-log) ──"
# a_cpu_local_no_waiter: --register lets us inline-poll; we do NOT await a Monitor.
hexa cloud fire "$POD_HOST" --log "$REMOTE_LOG" --register -- $FIRE_ARGV

echo "── (2/4) INLINE poll (a_cpu_local_no_waiter — sleep loop, never await a Monitor) ──"
# Poll the remote result JSON inline; commit-early on landing. Live CPU/step output
# is progress, NOT a stall (a_dont_kill_live_compute) — let it run to RESULT.
until hexa cloud copy-from "$POD_HOST" "${REMOTE_OUT}/clm_${TAG}.json" "$LOCAL_PULL/clm_${TAG}.json" 2>/dev/null; do
  echo "  [poll $(date +%H:%M:%S)] result not landed yet — sleeping 30s (live train = progress, not stall)"
  sleep 30
done
echo "  result landed: $LOCAL_PULL/clm_${TAG}.json"

echo "── (3/4) a_fire_recover_complete: pull ALL artifacts → verify → HF, BEFORE teardown ──"
for f in "clm_${TAG}.clm" "clm_${TAG}.pt" "gauges_${TAG}.jsonl" "fire_${TAG}.log"; do
  hexa cloud copy-from "$POD_HOST" "${REMOTE_OUT}/${f}" "$LOCAL_PULL/${f}" \
    || echo "  WARN pull failed for ${f} (PULL_FAILED != pod dead — retry before teardown)"
done
# verify the engine-loadable .clm (a_clm_gen_pipeline) — gauges are MONITOR-ONLY, the
# frozen verdict mounts THIS .clm on the CORE engine (a_engine_measured_verdict).
python3 "$REPO/CLM/model/verify_clm_v2.py" "$LOCAL_PULL/clm_${TAG}.clm" \
  && echo "  verify_clm_v2 OK (engine-loadable)" || echo "  WARN verify_clm_v2 flagged — inspect before HF"
# render the gauge dashboard from the pulled gauges.jsonl (monitor surface, $0 local).
python3 "$REPO/UNIVERSE/gauge_monitor.py" --once "$LOCAL_PULL/gauges_${TAG}.jsonl" \
  --log "$LOCAL_PULL/fire_${TAG}.log" || true
# HF upload (a_hf_autonomous — autonomous, no user gate; tier by post-train verdict).
if command -v hf >/dev/null 2>&1; then
  echo "  HF upload (a_hf_autonomous · a_hf_complete) → $HF_REPO (ALL: .clm + ckpt + gauges + json)"
  hf upload "$HF_REPO" "$LOCAL_PULL" "." --repo-type model \
    || echo "  WARN HF upload flagged — retry; do NOT teardown until uploaded (a_hf_registry)"
else
  echo "  (hf CLI absent — register the pull in HF.jsonl status=pending_upload; do NOT teardown)"
fi

echo "── (4/4) THEN teardown (only after pull+verify+HF; PULL_FAILED != pod dead) ──"
echo "  to teardown: hexa cloud dispatch rm <pod-id>   (verify all artifacts landed first)"
echo "═══ dispatch complete — monitor live next time with:"
echo "    python3 UNIVERSE/gauge_monitor.py --follow $LOCAL_PULL/gauges_${TAG}.jsonl --log $LOCAL_PULL/fire_${TAG}.log"
