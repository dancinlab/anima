#!/bin/bash
# fire_arms.sh — MORPH-ATOM (H_9288) decisive arms: M (codec atomicity) vs C1 (raw utf-8 control).
# M  = MORPH-2B codec, NON-collapsed (codec.json): must recombine 안/않/못 knowledge to flip held-out 아니.
# C1 = raw utf-8 baseline: same drill, no codec atomicity. M ≫ C1 on F2 held-out = G1 recombination crack.
# MEASURED 2026-07-13: M F2=0.908 (margin 2.14) ≫ C1 F2=0.617 (margin 0.05) · Δ +0.291 · both drilled F1≈1.0
#   · C3 shared-⟨NEG⟩ leak-ceiling F2=0.917 = V1 liveness PASS → the harness detects a real held-out flip.
# PREREQ: the harness must be the FIXED one (cupy _asnp · real-context framing · first-divergence scoring —
#   convergence morphatom-gate-py-1). The pre-fix harness reports margins==0 / chance and FAKES a null.
set -e
NVLIB='/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_runtime/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_nvrtc/lib'
export LD_LIBRARY_PATH=$NVLIB:$LD_LIBRARY_PATH
export PATH=$PATH:$HOME/.local/bin PYTHONUTF8=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=8
cd "$(dirname "$0")"
TR="anima-py train --arch clm --canon --arm ctrl --objective ce_marginal --emax 4 --cell-label ko-general --batch-size 8 --bf16 --seed 4302"

echo "=== M arm: CPT 16k on cpt_M.bytes (non-collapsed codec) ==="
$TR --corpus ./cpt_M.bytes --steps 16000 --init ./base_reinit.pt \
  --out ./cpt_M16.clm --ckpt-out ./cpt_M16.pt 2>&1 | tail -3
echo "=== M arm: drill 2500 on drill_M.bytes ==="
$TR --corpus ./drill_M.bytes --steps 2500 --init ./cpt_M16.pt --out ./drill_M.clm 2>&1 | tail -3
echo "=== M arm: eval (codec.json non-collapsed · real-context framing) ==="
python3 morphatom_eval.py drill_M.clm --panel eval_f2.json --codec codec.json --ctx cpt_M.bytes --out vM_f2.json 2>&1 | grep -vE "gauge_lib"
python3 morphatom_eval.py drill_M.clm --panel eval_f1.json --codec codec.json --ctx cpt_M.bytes --out vM_f1.json 2>&1 | grep -vE "gauge_lib"

echo "=== C1 arm: CPT 16k on cpt_C1.bytes (raw utf-8 · from the UN-reinit base) ==="
$TR --corpus ./cpt_C1.bytes --steps 16000 --init ./base.pt \
  --out ./cpt_C1_16.clm --ckpt-out ./cpt_C1_16.pt 2>&1 | tail -3
echo "=== C1 arm: drill 2500 on drill_C1.bytes ==="
$TR --corpus ./drill_C1.bytes --steps 2500 --init ./cpt_C1_16.pt --out ./drill_C1.clm 2>&1 | tail -3
echo "=== C1 arm: eval (raw utf-8 · --codec none) ==="
python3 morphatom_eval.py drill_C1.clm --panel eval_f2.json --codec none --ctx cpt_C1.bytes --out vC1_f2.json 2>&1 | grep -vE "gauge_lib"
python3 morphatom_eval.py drill_C1.clm --panel eval_f1.json --codec none --ctx cpt_C1.bytes --out vC1_f1.json 2>&1 | grep -vE "gauge_lib"
echo ARMS_DONE
