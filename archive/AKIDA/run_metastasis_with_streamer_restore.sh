#!/bin/bash
# H_861 METASTASIS domain-boundary transfer — single-chip discipline (#1717): stop spike-streamer, confirm
# akida.devices(), run the metastasis harness TWICE (real domain split vs shuffled control) ONE AT A TIME,
# RESTORE + verify streamer. substrate=HYBRID (on-chip AKD1000 enc ⊕ off-chip Elman head, numpy BPTT, NO torch).
# a_lane_akida_gpu_split · g63 NO sw fallback (device==[] -> abort) · thermal pause >=82C.
set -u
HOME_DIR=/home/ubuntu
ROOT=$HOME_DIR/clm_kosmos_akida
LOG=$ROOT/metastasis_wrap.log
PY=$HOME_DIR/.venv/anima-akida/bin/python
STREAMER_ARGV="--port 9512 --duration 86400 --regime R3"
HARNESS=$ROOT/onchip_xlm_metastasis_flores.py
temp_c() { vcgencmd measure_temp 2>/dev/null | sed 's/[^0-9.]//g' | cut -d. -f1; }
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }
restore_streamer() {
  sleep 2
  systemctl --user start spike-streamer 2>/dev/null && log "streamer service restarted" || \
    ( cd "$HOME_DIR/anima/SUB_ENGINES/AKIDA/scripts" && nohup $PY spike_streamer.py $STREAMER_ARGV > "$ROOT/streamer_restore.log" 2>&1 & log "streamer nohup restarted pid=$!" )
  sleep 3
  ACT=$(systemctl --user is-active spike-streamer 2>/dev/null)
  ARGV=$(systemctl --user show -p ExecStart spike-streamer 2>/dev/null | grep -o 'spike_streamer.py [^;]*' | head -1)
  log "RESTORE verify: is-active=$ACT  argv=[$ARGV]  throttled=$(vcgencmd get_throttled)"
  echo "$(date -u +%FT%TZ) WRAP done is-active=$ACT" >> "$LOG"
}
trap restore_streamer EXIT
echo "" > "$LOG"
log "WRAP start throttled=$(vcgencmd get_throttled) temp=$(vcgencmd measure_temp)"
systemctl --user stop spike-streamer 2>/dev/null && log "streamer service stopped" || true
pkill -f "spike_streamer.py" 2>/dev/null && log "streamer proc killed" || log "no streamer proc"
sleep 4
DEVN=$($PY -c "import akida; print(len(akida.devices()))" 2>>"$LOG")
log "akida.devices() count=$DEVN"
if [ "$DEVN" != "1" ]; then
  log "ABORT (g63): akida.devices() did not return exactly one device. NO sw fallback."
  exit 91
fi
run_with_thermal() {
  local name="$1"; local outlog="$2"; local corpus="$3"
  local T=$(temp_c)
  log "$name pre-fire temp=${T}C throttled=$(vcgencmd get_throttled)"
  while [ -n "$T" ] && [ "$T" -ge 82 ]; do
    log "$name THERMAL PAUSE temp=${T}C >=82C — waiting 30s"; sleep 30; T=$(temp_c)
  done
  log "$name FIRE (CORPUS_DIR=$corpus) -> $outlog"
  cd "$ROOT"
  CORPUS_DIR="$corpus" LANE_A_LADDER_NC="1012" N_TEST_FRAC="0.3162" $PY -u "$HARNESS" > "$outlog" 2>&1
  local rc=$?
  log "$name exit rc=$rc temp=$(vcgencmd measure_temp) throttled=$(vcgencmd get_throttled)"
  return $rc
}
# ---- RUN A: real domain split (TEST = wikivoyage, a distant source domain) ----
run_with_thermal "metastasis-DOMAIN" "$ROOT/metastasis_domain.log" "corpus_flores_domain"
RC_D=$?
sleep 8
# ---- RUN B: shuffled control (TEST = domain-mixed, within-distribution baseline at matched geometry) ----
run_with_thermal "metastasis-SHUFFLED" "$ROOT/metastasis_shuffled.log" "corpus_flores_shuffled"
RC_S=$?
log "metastasis done RC_domain=$RC_D RC_shuffled=$RC_S"
