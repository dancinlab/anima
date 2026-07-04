#!/usr/bin/env bash
# Rent-until-good: rent a plain vast pod, verify it BOOTS (port maps + ssh), keep the
# first that works, tear down duds. Launches the bootstrap sweep on the first good host.
SP=/private/tmp/claude-501/-Users-mini-dancinlab-anima/a1a1adf6-9373-4338-9ac2-15fadbeffce4/scratchpad
cd /Users/mini/dancinlab/anima
GPUS="RTX_3090 RTX_3090 RTX_A5000 RTX_4090"
n=0
for GPU in $GPUS; do
  n=$((n+1))
  TAG="r8_$n"
  echo "[loop] === attempt $n gpu=$GPU ==="
  timeout 360 hexa cloud rent vast --gpu $GPU --image pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime --disk 45 --desc "g1-derivtrace-robust-H9124-$TAG" --project @anima --max-wait-sec 300 > $SP/rent_$TAG.log 2>&1
  PID=$(hexa cloud list --json 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);print(next((p.get('id') for p in d if '$TAG' in str(p.get('purpose',''))), ''))" 2>/dev/null)
  echo "[loop] pod=$PID"
  [ -z "$PID" ] && { echo "[loop] no pod id (rent failed); next"; continue; }
  # verify boot: ssh works (proxy or direct) within ~4min AND port maps
  RH=""; RP=""
  for t in $(seq 1 12); do
    A=$(hexa cloud alive $PID --provider vast 2>&1 | tail -1)
    echo "$A" | grep -q GONE && { echo "[loop] pod GONE at t$t"; break; }
    EP=$(hexa cloud ssh-port $PID --provider vast 2>/dev/null | grep -o 'ssh[0-9]*.vast.ai:[0-9]*')
    PH=${EP%:*}; PP=${EP#*:}
    read DIP DPP < <(hexa cloud api vast GET "instances" 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);[print(i.get('public_ipaddr'),(i.get('ports') or {}).get('22/tcp',[{}])[0].get('HostPort')) for i in d.get('instances',[]) if str(i.get('id'))=='$PID']" 2>/dev/null)
    for cand in "$PH $PP" "$DIP $DPP"; do
      set -- $cand; [ -z "$1" ] || [ "$2" = "None" ] && continue
      R=$(timeout 22 hexa cloud exec $1 --port $2 --insecure -- "echo GOODHOST" 2>&1)
      echo "$R" | grep -q GOODHOST && { RH=$1; RP=$2; break 2; }
    done
    sleep 20
  done
  if [ -n "$RH" ]; then
    echo "[loop] GOOD HOST pod=$PID $RH:$RP — launching bootstrap"
    nohup bash $SP/bootstrap.sh $PID $RH $RP > $SP/bootstrap.out 2>&1 &
    echo "GOOD_POD=$PID EP=$RH:$RP" > $SP/good_pod.env
    echo "[loop] LAUNCHED_SWEEP pod=$PID ep=$RH:$RP"
    exit 0
  fi
  echo "[loop] DUD pod=$PID — tearing down"
  hexa cloud down $PID --provider vast --yes > /dev/null 2>&1
done
echo "[loop] ALL_ATTEMPTS_FAILED"
exit 1
