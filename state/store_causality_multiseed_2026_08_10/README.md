# Compose-2 canonical multi-seed and 7B staging gate — 2026-08-10

Status: RUNNING — protocol and seeds registered before GPU rental.

This run extends the seed-7/11 result in `state/store_causality_canonical_2026_08_10`. The source
compose-2 corpus, panel, three controls, randomization, training recipe, and accuracy bars remain
unchanged. Nothing is regenerated. GPU-heavy work runs on Vast.ai, not mini.

## Pre-registered multi-seed protocol

- source commit: `2bd7fa198`
- warm start: `.fire-recover/h9672_rv_sweep/RV3c_13_CONFIRM_orc1.00_p1_0.99_flip0.99.clm`
- architecture: d3784 / L4 / E3, frozen trunk, position-normalized canonical lane 10
- training: 24-byte window, store batch 32, 24,000 steps, direct address supervision
- existing seeds retained: 7 and 11
- new seeds fixed before execution: 13, 17, 19, 23, 29
- gate order: pair-oracle first; controls run only when pair-oracle is at least 0.90
- unchanged bars: normal/recovery at least 0.75; each control at most 0.56

Every seed is trained exactly once with the frozen recipe. A failure is recorded as a failure and
diagnosed in the shared `cli/train.py` → `core/clms.py` → `cli/evaluate.py` path; it is not retried
with a different seed, panel, randomization, step count, or threshold.

## 7B staging gate

The 7B smoke begins only after the five new seed results are recorded. It must reuse the canonical
training/runtime path and first measure checkpoint configuration, trainable/frozen parameter scope,
estimated and observed VRAM, throughput, latency, wall time, and cost. Pair-oracle below 0.90 stops
the causal battery. Checkpoint recovery and long-run stability remain later gates; production is
not approved by a smoke result alone.

