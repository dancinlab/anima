#!/bin/bash
# Lane A P3' ENCODER-LADDER: stop R3 streamer, run encoder-ladder on chip to terminal, restart streamer.
set -u
LOG=/home/ubuntu/clm_kosmos_akida/encoder_ladder_wrap.log
PY=/home/ubuntu/.venv/anima-akida/bin/python
STREAMER="/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py --port 9512 --duration 86400 --regime R3"
echo "$(date -u +%FT%TZ) WRAP start" > $LOG
echo "$(date -u +%FT%TZ) throttled(pre)=$(vcgencmd get_throttled)" >> $LOG
# 1) free the chip
pkill -f "spike_streamer.py" 2>/dev/null && echo "$(date -u +%FT%TZ) streamer stopped" >> $LOG || echo "$(date -u +%FT%TZ) no streamer" >> $LOG
sleep 4
# 2) run ladder to terminal (commit-early JSON inside)
cd /home/ubuntu/clm_kosmos_akida
echo "$(date -u +%FT%TZ) ladder fire" >> $LOG
$PY -u encoder_ladder_chip.py > encoder_ladder.log 2>&1
RC=$?
echo "$(date -u +%FT%TZ) ladder exit rc=$RC throttled(post)=$(vcgencmd get_throttled)" >> $LOG
# 3) restore R3 streamer
cd /home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts
sleep 3
nohup $PY $STREAMER > /home/ubuntu/clm_kosmos_akida/streamer_restore.log 2>&1 &
echo "$(date -u +%FT%TZ) streamer restarted pid=$!" >> $LOG
echo "$(date -u +%FT%TZ) WRAP done rc=$RC" >> $LOG
