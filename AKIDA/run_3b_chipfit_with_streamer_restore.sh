#!/bin/bash
# Lane A 3B chip-fit/paging capacity ladder — single-chip occupancy. Stop the R3 spike-streamer (it holds the
# AKD1000 file lock), run the 3B chip-fit ladder to terminal, RESTORE R3 on exit (trap).
# substrate=HYBRID(on-chip encoder ⊕ off-chip host-CPU decode) · a_lane_akida_gpu_split. NO sw fallback (g63).
set -u
LOG=/home/ubuntu/clm_kosmos_akida/chipfit_wrap.log
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
echo "$(date -u +%FT%TZ) chipfit fire throttled=$(vcgencmd get_throttled)" >> $LOG
$PY -u onchip_xlm_3b_chipfit_ladder.py > chipfit.log 2>&1
RC=$?
echo "$(date -u +%FT%TZ) chipfit exit rc=$RC throttled=$(vcgencmd get_throttled)" >> $LOG
exit $RC
