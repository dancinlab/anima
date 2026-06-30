#!/bin/bash
# Lane A HYBRID: single-chip occupancy — stop R3 streamer, run the HYBRID (on-chip encoder ⊕ off-chip decode head)
# autoregressive rung to terminal, restore R3. substrate=HYBRID(on-chip⊕off-chip) · a_lane_akida_gpu_split.
# The CHIP encoder part has NO sw fallback (g63); the decode head is explicitly host-CPU. restore-on-exit via trap.
set -u
LOG=/home/ubuntu/clm_kosmos_akida/hybrid_wrap.log
PY=/home/ubuntu/.venv/anima-akida/bin/python
STREAMER="/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py --port 9512 --duration 86400 --regime R3"
echo "$(date -u +%FT%TZ) WRAP start throttled=$(vcgencmd get_throttled)" > $LOG
restore_streamer() {
  sleep 2
  systemctl --user start spike-streamer 2>/dev/null && echo "$(date -u +%FT%TZ) streamer service restarted" >> $LOG || \
    ( cd /home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts && nohup $PY $STREAMER > /home/ubuntu/clm_kosmos_akida/streamer_restore.log 2>&1 & echo "$(date -u +%FT%TZ) streamer nohup restarted pid=$!" >> $LOG )
  echo "$(date -u +%FT%TZ) WRAP done throttled=$(vcgencmd get_throttled)" >> $LOG
}
trap restore_streamer EXIT
systemctl --user stop spike-streamer 2>/dev/null && echo "$(date -u +%FT%TZ) streamer service stopped" >> $LOG || true
pkill -f "spike_streamer.py" 2>/dev/null && echo "$(date -u +%FT%TZ) streamer proc killed" >> $LOG || echo "$(date -u +%FT%TZ) no streamer proc" >> $LOG
sleep 4
cd /home/ubuntu/clm_kosmos_akida
echo "$(date -u +%FT%TZ) hybrid fire throttled=$(vcgencmd get_throttled)" >> $LOG
$PY -u onchip_xlm_hybrid_decode.py > hybrid_decode.log 2>&1
RC=$?
echo "$(date -u +%FT%TZ) hybrid exit rc=$RC throttled=$(vcgencmd get_throttled)" >> $LOG
exit $RC
