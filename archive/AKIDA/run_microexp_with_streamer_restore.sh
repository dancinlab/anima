#!/bin/bash
# Lane A micro-exp runner: stop R3 streamer (record argv), run ONE on-chip micro-exp to terminal, restore R3.
# substrate=AKIDA · a_lane_akida_gpu_split. NO sw fallback (g63). restore-on-exit via trap.
# usage: run_microexp_with_streamer_restore.sh <script.py> <slug>
set -u
SCRIPT="$1"; SLUG="$2"
DIR=/home/ubuntu/clm_kosmos_akida
LOG=$DIR/microexp_${SLUG}_wrap.log
PY=/home/ubuntu/.venv/anima-akida/bin/python
STREAMER="/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py --port 9512 --duration 86400 --regime R3"
echo "$(date -u +%FT%TZ) WRAP start slug=$SLUG throttled=$(vcgencmd get_throttled) temp=$(vcgencmd measure_temp)" > $LOG
restore_streamer() {
  sleep 2
  systemctl --user start spike-streamer 2>/dev/null && echo "$(date -u +%FT%TZ) streamer service restarted" >> $LOG || \
    ( cd /home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts && nohup $PY $STREAMER > /home/ubuntu/clm_kosmos_akida/streamer_restore.log 2>&1 & echo "$(date -u +%FT%TZ) streamer nohup restarted pid=$!" >> $LOG )
  echo "$(date -u +%FT%TZ) WRAP done slug=$SLUG throttled=$(vcgencmd get_throttled) temp=$(vcgencmd measure_temp)" >> $LOG
}
trap restore_streamer EXIT
systemctl --user stop spike-streamer 2>/dev/null && echo "$(date -u +%FT%TZ) streamer service stopped" >> $LOG || true
pkill -f "spike_streamer.py" 2>/dev/null && echo "$(date -u +%FT%TZ) streamer proc killed" >> $LOG || echo "$(date -u +%FT%TZ) no streamer proc" >> $LOG
sleep 4
cd $DIR
echo "$(date -u +%FT%TZ) ${SLUG} fire throttled=$(vcgencmd get_throttled) temp=$(vcgencmd measure_temp)" >> $LOG
$PY -u $SCRIPT > microexp_${SLUG}.log 2>&1
RC=$?
echo "$(date -u +%FT%TZ) ${SLUG} exit rc=$RC throttled=$(vcgencmd get_throttled) temp=$(vcgencmd measure_temp)" >> $LOG
exit $RC
