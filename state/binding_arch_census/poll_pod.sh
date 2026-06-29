#!/usr/bin/env bash
# poll_pod.sh — check pod progress for H_1640/1641 trainings + H_1602 eval.
H=ssh5.vast.ai; P=13584
S="ssh -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=25 -p $P root@$H"
$S 'cd ~/anima
echo "=== GPU ==="; nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader
echo "=== H1640 progress ==="
ls state/binding_arch_census/h1640_hamiltonian/ckpt/*.clm 2>/dev/null | wc -l | xargs echo "clms_done(of 9):"
grep -c "EVAL G0-G6" h1640.log 2>/dev/null | xargs echo "evals_done:"
tail -3 h1640.log 2>/dev/null
echo "=== H1641 progress ==="
ls state/binding_arch_census/h1641_laminar/ckpt/*.clm 2>/dev/null | wc -l | xargs echo "clms_done(of 9):"
tail -2 h1641.log 2>/dev/null
echo "=== H1602 eval progress ==="
ls state/binding_arch_census/h1602_eval/*.g0g6.txt 2>/dev/null | wc -l | xargs echo "evals_done(of 9):"
echo "=== procs ==="; ps aux | grep -E "trainer.py|evaluate.py|pod_run" | grep -v grep | wc -l | xargs echo "live_procs:"
' 2>&1 | grep -vE "Warning|Welcome|Have fun"
