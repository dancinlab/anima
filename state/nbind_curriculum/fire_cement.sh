#!/bin/bash
# fire_cement.sh — H_9288 MORPH-ATOM cement: the missing C2 control + a replication seed.
#
# Measured so far (seed 4302): M(codec) held-out 아니 F2=0.908 ≫ C1(raw utf-8) 0.617 · Δ+0.291
#   → atomicity CAUSES held-out recombination (H_9288 🟢 DIRECTIONAL, 1 seed, C2 arm never fired).
#
# This fire closes the two honest gaps:
#   [C2] codec, held-out stem ABLATED from the CPT corpus (gen_morphatom_s1 cpt_C2.bytes = every natural
#        line containing 아니 removed). The drill still teaches the flip on 안/않/못. Question: does the
#        model need a PRETRAINED representation of the held-out atom for the drilled rule to transfer?
#        C2 ≈ chance while M=0.908 ⟹ yes — the drill cannot conjure the atom's meaning from nothing;
#        atomicity works by giving the flip-rule a pretrained address to land on.
#        C2 ≈ M ⟹ no — the atomic slot alone suffices, pretraining exposure is irrelevant.
#   [seed 7] M + C1 replicated at a 2nd seed — is Δ+0.291 a seed fluke? (N2's worst install swing 0.225)
#
# Harness = the FIXED one (cupy _asnp · real-context framing · first-divergence scoring — the pre-fix
# harness reports margins==0 / chance and fakes a null · convergence morphatom-gate-py-1).
set -e
NVLIB='/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_runtime/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_nvrtc/lib'
export LD_LIBRARY_PATH=$NVLIB:$LD_LIBRARY_PATH
export PATH=$PATH:$HOME/.local/bin PYTHONUTF8=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=8
cd "$(dirname "$0")"
TR="anima-py train --arch clm --canon --arm ctrl --objective ce_marginal --emax 4 --cell-label ko-general --batch-size 8 --bf16"

echo "=== [0] corpus + codec + arms (deterministic regen) ==="
python3 gen_morph_corpus.py --out morph_corpus.txt 2>&1 | tail -1
python3 gen_morphatom_s1.py --corpus morph_corpus.txt --k 2048 --held ani --cpt-lines 120000 --out-dir . 2>&1 | tail -2
python3 morphatom_reinit.py ./base.pt ./base_reinit.pt 2>&1 | tail -1

# ---------- [C2] held-out atom ABLATED from CPT (seed 4302 = the original) ----------
echo "=== [C2] CPT 16k on cpt_C2.bytes (codec · 아니-ablated corpus) ==="
$TR --seed 4302 --corpus ./cpt_C2.bytes --steps 16000 --init ./base_reinit.pt \
  --out ./cpt_C2_16.clm --ckpt-out ./cpt_C2_16.pt 2>&1 | tail -2
echo "=== [C2] drill 2500 + eval ==="
$TR --seed 4302 --corpus ./drill_C2.bytes --steps 2500 --init ./cpt_C2_16.pt --out ./drill_C2.clm 2>&1 | tail -2
python3 morphatom_eval.py drill_C2.clm --panel eval_f2.json --codec codec.json --ctx cpt_C2.bytes --out vC2_f2.json 2>&1 | grep -vE "gauge_lib"
python3 morphatom_eval.py drill_C2.clm --panel eval_f1.json --codec codec.json --ctx cpt_C2.bytes --out vC2_f1.json 2>&1 | grep -vE "gauge_lib"

# ---------- [seed 7] M + C1 replication ----------
echo "=== [M·s7] CPT 16k + drill + eval (codec · non-collapsed) ==="
$TR --seed 7 --corpus ./cpt_M.bytes --steps 16000 --init ./base_reinit.pt --out ./cpt_M_s7.clm --ckpt-out ./cpt_M_s7.pt 2>&1 | tail -2
$TR --seed 7 --corpus ./drill_M.bytes --steps 2500 --init ./cpt_M_s7.pt --out ./drill_M_s7.clm 2>&1 | tail -2
python3 morphatom_eval.py drill_M_s7.clm --panel eval_f2.json --codec codec.json --ctx cpt_M.bytes --out vM_s7_f2.json 2>&1 | grep -vE "gauge_lib"
python3 morphatom_eval.py drill_M_s7.clm --panel eval_f1.json --codec codec.json --ctx cpt_M.bytes --out vM_s7_f1.json 2>&1 | grep -vE "gauge_lib"

echo "=== [C1·s7] CPT 16k + drill + eval (raw utf-8 · from un-reinit base) ==="
$TR --seed 7 --corpus ./cpt_C1.bytes --steps 16000 --init ./base.pt --out ./cpt_C1_s7.clm --ckpt-out ./cpt_C1_s7.pt 2>&1 | tail -2
$TR --seed 7 --corpus ./drill_C1.bytes --steps 2500 --init ./cpt_C1_s7.pt --out ./drill_C1_s7.clm 2>&1 | tail -2
python3 morphatom_eval.py drill_C1_s7.clm --panel eval_f2.json --codec none --ctx cpt_C1.bytes --out vC1_s7_f2.json 2>&1 | grep -vE "gauge_lib"
python3 morphatom_eval.py drill_C1_s7.clm --panel eval_f1.json --codec none --ctx cpt_C1.bytes --out vC1_s7_f1.json 2>&1 | grep -vE "gauge_lib"

echo "=== SUMMARY ==="
for f in vC2_f2 vC2_f1 vM_s7_f2 vM_s7_f1 vC1_s7_f2 vC1_s7_f1; do
  [ -f $f.json ] && echo -n "$f: " && python3 -c "import json;d=json.load(open('$f.json'));print('d_acc=',d['d_acc'],'margin=',d['mean_margin'])"
done
echo CEMENT_DONE
