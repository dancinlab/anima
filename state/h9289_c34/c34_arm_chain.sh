#!/bin/bash
# c34_arm_chain.sh <TAG> <PORT> <POD_ID> — one C34 arm, end to end.
#   wait C34_<TAG>_DONE -> verify artifacts (anti fake-DONE) -> PULL ckpt+evals
#   -> run GATE-0 hidden dump on that pod's now-idle GPU (transfer 0) -> PULL reps_<TAG>.npz
#   -> teardown the pod.
# Direct endpoint only (the vast ssh proxy is flaky). Handoff: 2026-07-14.

set -u
TAG="$1"; PORT="$2"; POD="$3"
HOST="192.234.50.153"
KEEP="$HOME/anima-weights/c34"
R() { timeout "${2:-120}" hexa cloud run "$HOST" --port "$PORT" -- "$1" 2>/dev/null | grep -v '^\[cloud\]'; }
log() { echo "[$(date '+%H:%M:%S')][$TAG] $*"; }

mkdir -p "$KEEP"

# ---- 1. wait for a REAL completion -----------------------------------------
while :; do
  st=$(R "grep -c C34_${TAG}_DONE /workspace/c34/run_${TAG}.log 2>/dev/null || echo 0" 90)
  if [ "${st:-0}" -ge 1 ] 2>/dev/null; then
    # anti fake-DONE (set -e defeated by pipe → wrapper can write a DONE with no artifacts)
    ok=$(R "s=\$(stat -c%s /workspace/c34/natem_c34_${TAG}.clm 2>/dev/null || echo 0); \
            e1=\$(stat -c%s /workspace/c34/eval_c34_${TAG}.json 2>/dev/null || echo 0); \
            e2=\$(stat -c%s /workspace/c34/eval_seen_c34_${TAG}.json 2>/dev/null || echo 0); \
            [ \$s -gt 100000000 ] && [ \$e1 -gt 1000 ] && [ \$e2 -gt 1000 ] && echo REAL || echo FAKE:\$s:\$e1:\$e2" 90)
    if echo "$ok" | grep -q REAL; then log "DONE + 산출물 검증 OK"; break; fi
    log "⚠️ DONE 마커는 있으나 산출물 미완 ($ok) — 가짜 DONE 의심, 60s 후 재확인"
    sleep 60
    continue
  fi
  log "학습중"
  sleep 240
done

# ---- 2. PULL (a_fire_recover_complete: before ANY teardown) ----------------
for f in eval_c34_${TAG}.json eval_seen_c34_${TAG}.json run_${TAG}.log natem_c34_${TAG}.clm; do
  timeout 3600 hexa cloud copy-from "$HOST" "/workspace/c34/$f" "$KEEP/$f" --port "$PORT" >/dev/null 2>&1 \
    && log "PULL ✅ $f ($(wc -c < "$KEEP/$f" 2>/dev/null) B)" \
    || { log "PULL ✗ $f — 중단(pod 유지·teardown 금지)"; exit 1; }
done

# ---- 3. GATE-0 hidden dump on the pod's idle GPU (no 450MB transfer) -------
for f in gt_step0_gprobe.py gt_prompts.json gt_atoms.json reduce_reps.py; do
  timeout 300 hexa cloud copy-to "$HOST" "$KEEP/$f" "/workspace/c34/$f" --port "$PORT" >/dev/null 2>&1 \
    && log "push → $f" || log "push ✗ $f"
done
R "cd /workspace/c34 && nohup bash -c 'anima-py evaluate natem_c34_${TAG}.clm --dump-hidden gt_prompts.json --out gt_hidden_${TAG}.npz --win 24 > dump_${TAG}.log 2>&1; python3 reduce_reps.py ${TAG} >> dump_${TAG}.log 2>&1; echo GATE0_${TAG}_DONE >> dump_${TAG}.log' > /dev/null 2>&1 < /dev/null & echo FIRED" 90
log "GATE-0 덤프 발사"

while :; do
  g=$(R "grep -c GATE0_${TAG}_DONE /workspace/c34/dump_${TAG}.log 2>/dev/null || echo 0" 90)
  [ "${g:-0}" -ge 1 ] 2>/dev/null && { log "GATE-0 덤프 완료"; break; }
  log "GATE-0 덤프 중… $(R 'tail -1 /workspace/c34/dump_'"${TAG}"'.log 2>/dev/null' 60 | cut -c1-60)"
  sleep 120
done

timeout 900 hexa cloud copy-from "$HOST" "/workspace/c34/reps_${TAG}.npz" "$KEEP/reps_${TAG}.npz" --port "$PORT" >/dev/null 2>&1 \
  && log "PULL ✅ reps_${TAG}.npz ($(wc -c < "$KEEP/reps_${TAG}.npz" 2>/dev/null) B)" \
  || { log "PULL ✗ reps — pod 유지(teardown 금지)"; exit 1; }

# ---- 4. teardown (only after everything is on permanent storage) -----------
timeout 120 hexa cloud rm "$POD" --provider vast --force >/dev/null 2>&1 \
  || timeout 120 hexa cloud api vast DELETE "instances/$POD" --allow-mutate >/dev/null 2>&1
log "teardown 요청 완료 (pod $POD)"
log "ARM COMPLETE"
