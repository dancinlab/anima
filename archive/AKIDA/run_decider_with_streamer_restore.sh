#!/bin/bash
# Lane A: single-chip occupancy — stop R3 streamer, run abs-margin decider to terminal, restart streamer.
# Runs ON pi5-akida (~/clm_kosmos_akida/). The R3 tonic spike_streamer holds the AKD1000 device lock
# (akida.devices() -> ERROR file lock 11 while it runs), so the decider — which maps a Model to the
# device — needs exclusive access: stop streamer -> fire decider -> restore the R3 tonic heartbeat.
# This mirrors the COFFESHOP single-chip procedure (service stop -> chip job -> service restart).
set -u
LOG=/home/ubuntu/clm_kosmos_akida/decider_wrap.log
PY=/home/ubuntu/.venv/anima-akida/bin/python
STREAMER="/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py --port 9512 --duration 86400 --regime R3"
echo "$(date -u +%FT%TZ) WRAP start" > $LOG
# 1) free the chip: stop the R3 streamer (it holds the akida device lock)
pkill -f "spike_streamer.py" 2>/dev/null && echo "$(date -u +%FT%TZ) streamer stopped" >> $LOG || echo "$(date -u +%FT%TZ) no streamer to stop" >> $LOG
sleep 4
# 2) run decider to terminal (commit-early JSON inside script)
cd /home/ubuntu/clm_kosmos_akida
echo "$(date -u +%FT%TZ) decider fire" >> $LOG
$PY -u abs_margin_chip.py > abs_margin.log 2>&1
RC=$?
echo "$(date -u +%FT%TZ) decider exit rc=$RC" >> $LOG
# 3) restore the R3 tonic streamer (ultradian hardware heartbeat)
cd /home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts
sleep 3
nohup $PY $STREAMER > /home/ubuntu/clm_kosmos_akida/streamer_restore.log 2>&1 &
echo "$(date -u +%FT%TZ) streamer restarted pid=$!" >> $LOG
echo "$(date -u +%FT%TZ) WRAP done" >> $LOG
