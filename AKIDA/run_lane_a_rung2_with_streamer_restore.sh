#!/bin/bash
# Lane A rung+1 sequential fire — single-chip EXCLUSIVE (#1717). Stop R3 spike-streamer, CONFIRM device, run
# A-single (AKIDA, synth-capacity gen ladder anchors 500/1000/2000) THEN A-multi (HYBRID, NC=100 synth, K=5 deep),
# ONE AT A TIME, RESTORE R3 on ANY exit (trap). g63 no-sw-fallback. Thermal: log temp at every stage.
set -u
WD=/home/ubuntu/clm_kosmos_akida
PY=/home/ubuntu/.venv/anima-akida/bin/python
STREAMER_ARGS="--port 9512 --duration 86400 --regime R3"
STREAMER_PY=/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py
LOG=$WD/lane_a_rung2_wrap.log
echo "$(date -u +%FT%TZ) WRAP start temp=$(vcgencmd measure_temp) throttled=$(vcgencmd get_throttled)" > $LOG
restore_streamer() {
  sleep 2
  systemctl --user start spike-streamer 2>/dev/null && echo "$(date -u +%FT%TZ) streamer service restarted" >> $LOG || \
    ( cd $WD && nohup $PY $STREAMER_PY $STREAMER_ARGS > $WD/streamer_restore.log 2>&1 & echo "$(date -u +%FT%TZ) streamer nohup pid=$!" >> $LOG )
  echo "$(date -u +%FT%TZ) WRAP done temp=$(vcgencmd measure_temp) throttled=$(vcgencmd get_throttled)" >> $LOG
}
trap restore_streamer EXIT
systemctl --user stop spike-streamer 2>/dev/null && echo "$(date -u +%FT%TZ) streamer service stopped" >> $LOG || true
pkill -f "spike_streamer.py" 2>/dev/null && echo "$(date -u +%FT%TZ) streamer proc killed" >> $LOG || echo "$(date -u +%FT%TZ) no streamer proc" >> $LOG
sleep 4
cd $WD
# device-confirm (g63): akida.devices() must return a device or ABORT (no sw fallback)
$PY -c "import akida,sys; d=akida.devices(); print('DEVICE_CONFIRM', d[0].version if d else 'NONE'); sys.exit(0 if d else 9)" >> $LOG 2>&1
if [ $? -ne 0 ]; then echo "$(date -u +%FT%TZ) DEVICE-CONFIRM FAILED — ABORT (g63 no sw fallback)" >> $LOG; exit 9; fi
# ---- A-single rung+1 (substrate=AKIDA) — synth-capacity gen ladder: n_concepts {100,200,400} -> anchors {500,1000,2000} ----
echo "$(date -u +%FT%TZ) A-single fire temp=$(vcgencmd measure_temp)" >> $LOG
LANE_A_CORPUS=corpus_synth LANE_A_GEN_NCONCEPTS="100,200,400" $PY -u onchip_xlm_gen_scale.py > $WD/lane_a_single_rung2.log 2>&1
echo "$(date -u +%FT%TZ) A-single exit rc=$? temp=$(vcgencmd measure_temp) throttled=$(vcgencmd get_throttled)" >> $LOG
# ---- A-multi rung+1 (substrate=HYBRID) — NC=100 synth, DEEPER K=5 (hop-4/5), wider B=5 branching, NC ladder {50,75,100} ----
echo "$(date -u +%FT%TZ) A-multi fire temp=$(vcgencmd measure_temp)" >> $LOG
LANE_A_CORPUS=corpus_synth LANE_A_K_ROLL=5 LANE_A_DELTAS="1,7,13,19,29" LANE_A_LADDER_NC="50,75,100" $PY -u onchip_xlm_branching.py > $WD/lane_a_multi_rung2.log 2>&1
echo "$(date -u +%FT%TZ) A-multi exit rc=$? temp=$(vcgencmd measure_temp) throttled=$(vcgencmd get_throttled)" >> $LOG
echo "$(date -u +%FT%TZ) BOTH RUNGS COMPLETE temp=$(vcgencmd measure_temp)" >> $LOG
