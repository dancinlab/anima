# Compose-2 CLMConvMoE 7B staging smoke — 2026-08-10

Status: BLOCKED — pre-registered before the five new canonical multi-seed results were known.

This is a bounded compatibility and capacity smoke, not a production approval or a convergence
claim. It starts only if seeds 13, 17, 19, 23, and 29 complete the frozen compose-2 protocol in
`state/store_causality_multiseed_2026_08_10`. It reuses `cli/train.py`, `core/clms.py`, and
`cli/evaluate.py`; no new trainer, engine, evaluator, corpus, panel, control, randomization, or bar
is introduced.

## Pre-registered run

- code/source commit: `ed369736e` (documentation-only descendants do not change the runtime)
- base checkpoint: `dancinlab/clm-7b-undertrained-step2000/clm_7b.clm`
- base checkpoint SHA-256: `05b558e1fe2d4fc507f3826fcd44e9fe8b877b4a576df615b8bd48604b58fabe`
- base architecture: CLMConvMoE d6208 / L30 / E30, byte vocabulary 256
- honest base status: WIP / undertrained step 2000 of 3500; it is not a production artifact
- canonical lane: dual read, value centering, position-normalized parity lane 10
- fixed smoke seed: 7
- fixed smoke length: 200 steps
- unchanged store recipe: 24-byte window, store batch 32, direct address weight 1.0, frozen trunk
- hardware floor: one H100/H200-class 80 GB GPU and at least 96 GB host memory
- measurements: parameter scope, observed peak VRAM, utilization, throughput, wall time, and cost
- evaluation order: pair-oracle first; below 0.90 stops the remaining causal battery
- unchanged bars: normal/recovery at least 0.75; every control at most 0.56

The 200-step boundary is fixed from the already-recorded 303M canonical learning trace, where
store/address training accuracy reached 1.0 by step 200. It is deliberately only a scale smoke.
Failure is recorded without retrying or changing steps, seed, data, randomization, or thresholds.
Even a pass leaves checkpoint recovery, long-run stability, latency, and chat staging as later
production gates.

The root README previously described `dancinlab/clm-v1-ref-pytorch-cuda-7b` as CLMConvMoE. Its own
model card identifies a 7.25B ByteGPT/decoder-only Transformer, so it cannot warm-start the existing
CLMS path. The compatible existing artifact above is used instead; the root model table will be
corrected with the measured result.
