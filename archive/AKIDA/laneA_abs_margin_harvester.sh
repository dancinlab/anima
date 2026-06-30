#!/bin/bash
# Lane A durable harvester (substrate=AKIDA · pi5-akida · a_lane_akida_gpu_split).
# Waits (indefinitely, ~20s poll) for pi5-akida to rejoin the LAN, then settles the
# pre-registered ABSOLUTE-margin decider (.verdicts/lane-a-absmargin/PREREGISTER.md):
#   - if a TERMINAL result (disposition present) exists -> harvest log + JSON, done.
#   - elif the decider is genuinely RUNNING on-chip -> wait for it to finish.
#   - else (host up, no terminal result, decider not running) -> RE-FIRE the decider
#     via the streamer-stop/restore wrapper (the chip is single-occupant; the R3 tonic
#     streamer holds the akida device lock and must be stopped, then restored).
# CPU-local poll, NO Monitor/waiter (a_cpu_local_no_waiter). pi5-akida is sacred host
# config (PI5-AKIDA.json) — never swapped, never converted to pool compute.
#
# FIX vs prior arm: prior `pgrep -f abs_margin_chip.py` over ssh matched the harvester's
# OWN remote command string -> false proc=RUNNING forever, never re-fired. This version
# greps `pgrep -fa` output and excludes the wrapper/pgrep shells, so RUNNING is real.
LOG=/tmp/laneA_harvest.log
HOST=ubuntu@192.168.50.155
RDIR=/home/ubuntu/clm_kosmos_akida
SSH="ssh -o ConnectTimeout=8 -o BatchMode=yes"
log(){ echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }

log "harvester (v2, false-RUNNING fix + chip-lock-aware re-fire) start; waiting for pi5-akida"
tries=0
while true; do
  tries=$((tries+1))
  if $SSH "$HOST" 'true' 2>/dev/null; then
    log "HOST UP (try $tries)"
    # Terminal result already on disk?
    HASDISP=$($SSH "$HOST" "grep -l '\"disposition\"' $RDIR/out/result_abs_margin.json 2>/dev/null")
    if [ -n "$HASDISP" ]; then
      log "RESULT TERMINAL (disposition present) — harvesting"
      $SSH "$HOST" "cat $RDIR/abs_margin.log"            > /tmp/abs_margin.log.harvested 2>>"$LOG"
      $SSH "$HOST" "cat $RDIR/out/result_abs_margin.json" > /tmp/result_abs_margin.json.harvested 2>>"$LOG"
      log "HARVEST_OK"; tail -50 /tmp/abs_margin.log.harvested >> "$LOG"; break
    fi
    # Decider genuinely running? (real proc, NOT this harvester's own ssh/pgrep shell)
    RUN=$($SSH "$HOST" "pgrep -fa abs_margin_chip.py | grep -v 'pgrep' | grep -v 'grep '" 2>/dev/null)
    if echo "$RUN" | grep -q 'bin/python'; then
      log "decider RUNNING on-chip ($RUN); waiting"
      sleep 20; continue
    fi
    # Host up, no terminal result, decider not running -> re-fire via streamer-restore wrapper.
    log "HOST UP, NO terminal result, decider NOT running — re-firing decider (streamer stop/restore)"
    $SSH "$HOST" "cd $RDIR && setsid nohup bash run_decider_with_streamer_restore.sh > wrap_nohup.log 2>&1 < /dev/null & echo fired pid=\$!" >> "$LOG" 2>&1
    log "decider re-fired on-chip; continue polling for terminal disposition"
    sleep 45; continue
  fi
  if [ $((tries % 30)) -eq 0 ]; then log "still dark after $tries tries"; fi
  sleep 20
done
log "harvester exit"
