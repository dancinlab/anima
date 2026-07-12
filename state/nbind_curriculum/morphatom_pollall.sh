#!/bin/bash
# poll all 4 arms → pull f2/f1 → combined verdict (bash 3.2 compatible, no assoc arrays).
CK=~/anima-weights/morphatom; mkdir -p "$CK"
O="-o StrictHostKeyChecking=no -o ConnectTimeout=25 -o ServerAliveInterval=20"
hp() { case "$1" in M) echo "ssh8.vast.ai 13988";; C1) echo "ssh1.vast.ai 13988";; C2) echo "ssh4.vast.ai 13986";; C3) echo "ssh5.vast.ai 13986";; esac; }
DONE_M=0; DONE_C1=0; DONE_C2=0; DONE_C3=0
for round in $(seq 1 70); do
  alldone=1
  for arm in M C1 C2 C3; do
    eval "d=\$DONE_$arm"; [ "$d" = 1 ] && continue
    set -- $(hp $arm); h=$1; p=$2
    R=$(timeout 45 ssh -p $p $O root@$h "cd /workspace/ma 2>/dev/null; if grep -q MORPHATOM_${arm}_DONE run_$arm.log 2>/dev/null; then echo DONE; cat f2_$arm.json 2>/dev/null; echo; cat f1_$arm.json 2>/dev/null; elif grep -iE 'Traceback|shape mismatch|command not found|No module named .(slw|numpy|torch|anima)' run_$arm.log | grep -qv gauge_lib 2>/dev/null; then echo XERR; tail -5 run_$arm.log; else echo RUN:\$(tail -1 run_$arm.log 2>/dev/null|cut -c1-50); fi" 2>&1 | grep -vE "Welcome|Have fun|Permanently")
    if echo "$R" | grep -q "^DONE"; then
      echo "$(date +%H:%M) [$arm] DONE $(echo "$R"|grep -o 'd_acc[^,}]*'|head -2|tr '\n' ' ')"; eval "DONE_$arm=1"
      scp -P $p $O root@$h:/workspace/ma/f2_$arm.json "$CK/f2_$arm.json" 2>/dev/null
      scp -P $p $O root@$h:/workspace/ma/f1_$arm.json "$CK/f1_$arm.json" 2>/dev/null
    elif echo "$R" | grep -q "^XERR"; then echo "$(date +%H:%M) [$arm] ERR $(echo "$R"|tail -1)"; eval "DONE_$arm=1"
    else echo "$(date +%H:%M) [$arm] $R"; alldone=0; fi
  done
  [ "$alldone" = 1 ] && { echo ALL_ARMS_DONE; break; }
  sleep 90
done
echo "=== COMBINED VERDICT ==="
python3 - "$CK" <<'PYEOF'
import json,sys
CK=sys.argv[1]; r={}
for a in ["M","C1","C2","C3"]:
    try: r[a]={"f2":json.load(open(f"{CK}/f2_{a}.json"))["d_acc"],"f1":json.load(open(f"{CK}/f1_{a}.json"))["d_acc"]}
    except Exception as e: r[a]=None
print(json.dumps(r,indent=1))
M,C1,C2,C3=(r.get(x) for x in["M","C1","C2","C3"])
if M and C1:
    d=round(M["f2"]-C1["f2"],3)
    ok=M["f2"]>=0.70 and d>=0.15 and (C3 and C3["f2"]>=0.90) and (C2 and C2["f2"]<=0.55) and M["f1"]>=0.75
    print(("PASS" if ok else "NOT-PASS")+f" | F2(M)={M['f2']} d(M-C1)={d} C3={C3['f2'] if C3 else '?'}(V1) C2={C2['f2'] if C2 else '?'}(abl) F1(M)={M['f1']}")
PYEOF
echo MORPHATOM_POLLALL_COMPLETE
