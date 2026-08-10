# Compose-2 CLMConvMoE 7B staging smoke — 2026-08-10

Status: COMPLETE — bounded smoke ran once and failed pair-oracle at 0.5000.

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

The 200-step boundary was fixed from the already-recorded 303M canonical learning trace, where
store/address training accuracy reached 1.0 by step 200. It is deliberately only a scale smoke.
Failure is recorded without retrying or changing steps, seed, data, randomization, or thresholds.
Even a pass leaves checkpoint recovery, long-run stability, latency, and chat staging as later
production gates.

The root README previously described `dancinlab/clm-v1-ref-pytorch-cuda-7b` as CLMConvMoE. Its own
model card identifies a 7.25B ByteGPT/decoder-only Transformer, so it cannot warm-start the existing
CLMS path. The compatible existing artifact above is used instead; the root model table will be
corrected with the measured result.

## Measured result

- instance: Vast.ai `47362407`, NVIDIA H100 PCIe 80 GB, 226 GB host RAM
- actual model: 7,057,657,951 parameters
- warm start: 189/197 keys, `.clm` round-trip byte-identical, fresh CLMS lane
- 200-step compute: 85.5 seconds; full init/train/serialize wall: 880.01 seconds
- last training batch: address accuracy 0.8125, store accuracy 0.59375
- peak train VRAM: 35,769 MiB; peak evaluation VRAM: 54,789 MiB
- train monitor: peak utilization 100%, active-sample mean 64.31%
- evaluation wall: 284.04 seconds
- pair-oracle: **0.5000 (64/128)** → `INVALID-INSTRUMENT`
- normal, drop A, drop B, shuffle, recovery: not executed or interpreted

The scale smoke proves that the canonical 7B CLMConvMoE and CLMS paths fit on one 80 GB H100, but
it does not prove causal learning at 7B. The pre-registered 200 steps that were enough for 303M were
not enough for the fresh 7B CLMS lane. No step extension or second seed was attempted. Production
and chat staging remain blocked; the next scientific gate must pre-register a longer 7B learning
run and a checkpoint-recovery test without changing the frozen data, randomness, or bars.

Artifacts are private in `dancinlab/anima-store-causality-7b-staging-2026-08-10` on Hugging Face.
Its immutable artifact commit contains 13 files / 31,772,494,874 bytes, including the engine `.clm`
and resumable `.clm.pt`. Small local records are under
`.fire-recover/store_causality_7b_staging_2026_08_10/`. Models and training data
are managed only in the `dancinlab` Hugging Face organization; the unchanged compose-2 fixture is
pinned in private dataset `dancinlab/anima-store-causality-compose2-2026-08-09` at commit
`8f29c2f16f214734d9b5fa4010c57c48fff3979e`. No R2 or local model copy remains.
The final Vast.ai invoice capture was $1.034 for the H100 smoke and $1.606 including the preceding
multi-seed run and discarded setup instances. Active Vast.ai rent is zero.
