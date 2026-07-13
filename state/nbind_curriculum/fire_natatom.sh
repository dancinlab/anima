#!/bin/bash
# fire_natatom.sh — NAT-ATOM (H_9290) decisive fire, single pod. Question: does codec morpheme atomicity
# rescue held-out predicate polarity grounding that raw bytes provably fail (N2 G-PROBE 0.55 = INFO-ABSENT)?
# reinit-embed → CPT 16k on NATURAL codec corpus (NO drill) → codec dump-hidden gt_prompts → H_9289 G-PROBE.
# MEASURED 2026-07-13: heldout_probe_acc 0.3448 < raw 0.5517 < bar 0.65 · RESCUE=false → NO-RESCUE (DATA-🧱).
# Inputs on the pod: base.pt · morph_corpus.txt · gt_prompts.json · gt_atoms.json · gt_step0_gprobe.py
#                    + morph2b.py · gen_codec_natural.py · morphatom_reinit.py · morphatom_dumphidden.py
#                    + morphatom_gprobe_run.py   (this dir is the SSOT for all of them)
set -e
NVLIB='/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_runtime/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_nvrtc/lib'
export LD_LIBRARY_PATH=$NVLIB:$LD_LIBRARY_PATH
export PATH=$PATH:$HOME/.local/bin PYTHONUTF8=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=8
cd "$(dirname "$0")"

echo "=== [1] gen codec-natural corpus (no drill) ==="
python3 gen_codec_natural.py --corpus morph_corpus.txt --k 2048 --cpt-lines 120000 --out-dir . 2>&1 | tail -2
echo "=== [2] reinit-embed base ==="
python3 morphatom_reinit.py ./base.pt ./base_reinit.pt 2>&1 | tail -2
echo "=== [3] CPT 16k on natural codec (M-nat · no drill) ==="
anima-py train --arch clm --canon --arm ctrl --objective ce_marginal --emax 4 \
  --corpus ./cpt_M.bytes --cell-label ko-general --steps 16000 --batch-size 8 --bf16 --seed 4302 \
  --init ./base_reinit.pt --out ./cpt_Mnat.clm --ckpt-out ./cpt_Mnat.pt 2>&1 | tail -3
echo "=== [4] codec dump-hidden gt_prompts (frozen H_9289 assets) ==="
python3 morphatom_dumphidden.py ./cpt_Mnat.clm gt_prompts.json ./gt_hidden_codec.npz \
  --codec codec.json --ctx cpt_M.bytes 2>&1 | grep -vE "gauge_lib" | tail -4
echo "=== [5] G-PROBE (held-out predicate polarity · vs raw 0.55) ==="
python3 morphatom_gprobe_run.py ./gt_hidden_codec.npz codec_Mnat 2>&1 | grep -vE "gauge_lib" | tail -3
echo NATATOM_DONE
