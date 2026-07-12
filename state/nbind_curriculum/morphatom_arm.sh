#!/bin/bash
# morphatom_arm.sh <HOST> <PORT> <ARM> [--smoke] — one MORPH-ATOM arm on a dedicated pod (VALIDATED pattern).
# Uses the smoke-proven chain: script-file fire (no nested quotes) + detached install + detached fire + poll.
# ARM ∈ {M,C1,C2,C3}. Assumes scripts already uploadable from $SP; uploads base.pt + corpus.
set -uo pipefail
HOST="$1"; PORT="$2"; ARM="$3"; SMOKE="${4:-}"
SP=/private/tmp/claude-501/-Users-mini-dancinlab-anima/f5b1994e-2cff-42cb-9e82-494c5e7d490b/scratchpad
CK=~/anima-weights/morphatom
BASE=~/anima-weights/clm303_clean/clm303_clean.pt
NVLIB='/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_runtime/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_nvrtc/lib'
S="scp -P $PORT -o StrictHostKeyChecking=no -o ConnectTimeout=30"
SSH="ssh -p $PORT -o StrictHostKeyChecking=no -o ConnectTimeout=25 -o ServerAliveInterval=20 root@$HOST"
mkdir -p "$CK"
if [ "$SMOKE" = "--smoke" ]; then CPT_STEPS=300; DR_STEPS=150; CPT_LINES=8000; else CPT_STEPS=8000; DR_STEPS=2500; CPT_LINES=120000; fi
CODEC=codec.json; [ "$ARM" = C3 ] && CODEC=codec_c3.json; [ "$ARM" = C1 ] && CODEC=none

# per-arm fire script (script-file → no nested-quote hell)
cat > "$SP/fire_$ARM.sh" <<EOF
#!/bin/bash
set -e
export LD_LIBRARY_PATH=$NVLIB:\$LD_LIBRARY_PATH
export PATH=\$PATH:\$HOME/.local/bin PYTHONUTF8=1 PYTHONUNBUFFERED=1
cd /workspace/ma
echo "=== build ($ARM held=ani K=2048 cpt=$CPT_LINES) ==="
python3 gen_morphatom_s1.py --corpus morph_corpus.txt --k 2048 --held ani --cpt-lines $CPT_LINES --out-dir /workspace/ma 2>&1 | tail -3
echo "=== CPT warm-start $CPT_STEPS ==="
anima-py train --arch clm --canon --arm ctrl --objective ce_marginal --emax 4 --corpus /workspace/ma/cpt_$ARM.bytes --cell-label ko-general --steps $CPT_STEPS --batch-size 8 --bf16 --seed 4302 --init /workspace/ma/base.pt --out /workspace/ma/cpt_$ARM.clm --ckpt-out /workspace/ma/cpt_$ARM.pt 2>&1 | tail -5
echo "=== drill FT $DR_STEPS ==="
anima-py train --arch clm --canon --arm ctrl --objective ce_marginal --emax 4 --corpus /workspace/ma/drill_$ARM.bytes --cell-label ko-general --steps $DR_STEPS --batch-size 8 --bf16 --seed 4302 --init /workspace/ma/cpt_$ARM.pt --out /workspace/ma/drill_$ARM.clm 2>&1 | tail -5
echo "=== F2/F1 eval (codec=$CODEC) ==="
python3 morphatom_eval.py /workspace/ma/drill_$ARM.clm --panel eval_f2.json --codec $CODEC --out /workspace/ma/f2_$ARM.json
python3 morphatom_eval.py /workspace/ma/drill_$ARM.clm --panel eval_f1.json --codec $CODEC --out /workspace/ma/f1_$ARM.json
echo MORPHATOM_${ARM}_DONE
EOF

echo "$(date +%H:%M:%S) [$ARM] upload scripts + base.pt + corpus → $HOST:$PORT"
$SSH 'mkdir -p /workspace/ma' 2>&1 | grep -vE "Welcome|Have fun|Permanently" || true
for f in morph2b.py gen_nbind.py gen_morphatom_s1.py morphatom_eval.py morph_corpus.txt install_ma.sh fire_$ARM.sh; do $S "$SP/$f" "root@$HOST:/workspace/ma/$f" 2>&1 | tail -1; done
if [ "$($SSH 'stat -c%s /workspace/ma/base.pt 2>/dev/null||echo 0' 2>/dev/null|tr -dc 0-9)" -gt 1000000000 ] 2>/dev/null; then echo "base.pt already present, skip"; else $S "$BASE" "root@$HOST:/workspace/ma/base.pt" 2>&1 | tail -1; fi

echo "$(date +%H:%M:%S) [$ARM] detached install"
$SSH 'cd /workspace/ma; rm -f INSTALL_DONE; nohup setsid bash /workspace/ma/install_ma.sh >/dev/null 2>&1 & disown; echo launched' 2>&1 | grep -vE "Welcome|Have fun|Permanently" | tail -1
for i in $(seq 1 30); do
  R=$(timeout 50 $SSH 'D=$(cat /workspace/ma/INSTALL_DONE 2>/dev/null); [ -n "$D" ] && echo "INSTALL:$D $(command -v anima-py||echo NOPY)" || echo installing' 2>&1 | grep -vE "Welcome|Have fun|Permanently")
  echo "$(date +%H:%M:%S) [$ARM] inst#$i: $R"
  echo "$R" | grep -q "INSTALL:0" && echo "$R" | grep -q anima-py && break
  echo "$R" | grep -qE "INSTALL:[1-9]" && { echo "[$ARM] INSTALL FAILED"; exit 1; }
  sleep 40
done

echo "$(date +%H:%M:%S) [$ARM] detached fire (~95min full)"
$SSH "cd /workspace/ma; rm -f MORPHATOM_${ARM}_DONE run_$ARM.log; nohup setsid bash /workspace/ma/fire_$ARM.sh >/workspace/ma/run_$ARM.log 2>&1 & disown; echo fired-$ARM" 2>&1 | grep -vE "Welcome|Have fun|Permanently" | tail -1
echo "$(date +%H:%M:%S) [$ARM] LAUNCHED on $HOST:$PORT — poll run_$ARM.log for MORPHATOM_${ARM}_DONE"
