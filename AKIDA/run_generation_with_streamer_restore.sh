#!/bin/bash
# Lane A: single-chip occupancy — stop R3 streamer, run on-chip open-vocab GENERATION probe to terminal,
# restore R3. substrate=AKIDA · a_lane_akida_gpu_split. NO sw fallback (g63).
set -u
LOG=/home/ubuntu/clm_kosmos_akida/generation_wrap.log
PY=/home/ubuntu/.venv/anima-akida/bin/python
STREAMER="/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py --port 9512 --duration 86400 --regime R3"
echo "$(date -u +%FT%TZ) WRAP start throttled=$(vcgencmd get_throttled)" > $LOG
systemctl --user stop spike-streamer 2>/dev/null && echo "$(date -u +%FT%TZ) streamer service stopped" >> $LOG || true
pkill -f "spike_streamer.py" 2>/dev/null && echo "$(date -u +%FT%TZ) streamer proc killed" >> $LOG || echo "$(date -u +%FT%TZ) no streamer proc" >> $LOG
sleep 4
cd /home/ubuntu/clm_kosmos_akida
echo "$(date -u +%FT%TZ) generation fire throttled=$(vcgencmd get_throttled)" >> $LOG
$PY -u onchip_xlm_generation.py > generation.log 2>&1
RC=$?
echo "$(date -u +%FT%TZ) generation exit rc=$RC throttled=$(vcgencmd get_throttled)" >> $LOG
sleep 3
systemctl --user start spike-streamer 2>/dev/null && echo "$(date -u +%FT%TZ) streamer service restarted" >> $LOG || \
  ( cd /home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts && nohup $PY $STREAMER > /home/ubuntu/clm_kosmos_akida/streamer_restore.log 2>&1 & echo "$(date -u +%FT%TZ) streamer nohup restarted pid=$!" >> $LOG )
echo "$(date -u +%FT%TZ) WRAP done throttled=$(vcgencmd get_throttled)" >> $LOG
