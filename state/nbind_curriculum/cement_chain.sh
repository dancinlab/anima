#!/bin/bash
# cement_chain.sh — H_9288 CEMENT fire on pod 44701951 (/workspace/cem).
#   phase 1: wait INSTALL_DONE (torch+cupy ~2h; per convergence install-ma-sh-1 a flat log size is
#            NOT evidence of a stall — the package name on the last line changing IS progress)
#   phase 2: fire_cement.sh chains automatically -> wait CEMENT_DONE in run_cem.log (~5h)
#   phase 3: PULL the 3 verdict JSONs + logs (a_fire_recover_complete). Teardown stays MANUAL
#            (read the verdict first, then decide on the ckpt).
set -u
POD=44701951; HOST=ssh8.vast.ai; PORT=21950
KEEP="$HOME/anima-weights/cem"; mkdir -p "$KEEP"
R() { timeout "${2:-120}" hexa cloud run "$HOST" --port "$PORT" -- "$1" 2>/dev/null | grep -v '^\[cloud\]'; }
log() { echo "[$(date '+%H:%M:%S')][cem] $*"; }

log "phase1 — install 대기"
while :; do
  d=$(R "cat /workspace/cem/INSTALL_DONE 2>/dev/null || echo NO" 90)
  echo "$d" | grep -qv NO && [ -n "$d" ] && { log "INSTALL_DONE ✅"; break; }
  log "설치중 :: $(R 'tail -1 /workspace/cem/install.log 2>/dev/null' 60 | cut -c1-70)"
  sleep 300
done

log "phase2 — cement 체인 대기 (fire_cement.sh 자동 실행)"
while :; do
  c=$(R "grep -c CEMENT_DONE /workspace/cem/run_cem.log 2>/dev/null || echo 0" 90)
  [ "${c:-0}" -ge 1 ] 2>/dev/null && { log "CEMENT_DONE ✅"; break; }
  log "cement 진행 :: $(R 'tail -1 /workspace/cem/run_cem.log 2>/dev/null' 60 | cut -c1-70) · GPU $(R 'nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader' 60)"
  sleep 300
done

log "phase3 — 결과 회수"
for f in vC2_f2.json vM_s7_f2.json vC1_s7_f2.json run_cem.log install.log; do
  timeout 600 hexa cloud copy-from "$HOST" "/workspace/cem/$f" "$KEEP/$f" --port "$PORT" >/dev/null 2>&1 \
    && log "PULL ✅ $f ($(wc -c < "$KEEP/$f" 2>/dev/null) B)" || log "PULL ✗ $f"
done
log "CEMENT COMPLETE — 판독 대기 (teardown 은 판독 후 수동)"
