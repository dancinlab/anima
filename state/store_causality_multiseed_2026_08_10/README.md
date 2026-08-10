# Compose-2 canonical multi-seed and 7B staging gate — 2026-08-10

Status: COMPLETE — all five pre-registered seeds are `SUPPORTED-CAUSAL`.

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

## Results

| Seed | Pair oracle | Normal | Drop A | Drop B | Shuffle | Recovery | Verdict |
|---:|---:|---:|---:|---:|---:|---:|---|
| 13 | 1.0000 | 1.0000 | 0.4141 | 0.4453 | 0.4766 | 1.0000 | SUPPORTED-CAUSAL |
| 17 | 1.0000 | 1.0000 | 0.3984 | 0.4453 | 0.4766 | 1.0000 | SUPPORTED-CAUSAL |
| 19 | 1.0000 | 1.0000 | 0.3984 | 0.4531 | 0.4766 | 1.0000 | SUPPORTED-CAUSAL |
| 23 | 1.0000 | 1.0000 | 0.3906 | 0.4453 | 0.4766 | 1.0000 | SUPPORTED-CAUSAL |
| 29 | 1.0000 | 1.0000 | 0.3906 | 0.4297 | 0.4766 | 1.0000 | SUPPORTED-CAUSAL |

The frozen seed-7 checkpoint was re-evaluated on the same pod and exactly reproduced pair-oracle,
normal, and recovery 1.0000; drop A 0.3984; drop B 0.4453; and shuffle 0.4766. The canonical Python
collection passed 17/17 on the RTX 3090 and again on the H100. No training or evaluation code was
changed, so no shared-flow repair was required.

The five `.clm`, five resumable `.clm.pt`, logs, summaries, and results are preserved in the private
`dancinlab/anima-store-causality-multiseed-2026-08-10` Hugging Face repository. Its immutable
artifact commit contains 35 files / 7,818,835,789 bytes. Small records are also under
`.fire-recover/store_causality_multiseed_2026_08_10/`. Models and training data are managed
only in the `dancinlab` Hugging Face organization; no R2 or local model copy remains. The unchanged
compose-2 training fixture is pinned in the private dataset
`dancinlab/anima-store-causality-compose2-2026-08-09` at commit
`8f29c2f16f214734d9b5fa4010c57c48fff3979e`.

Vast.ai invoice capture after teardown was $0.572 for the multi-seed run plus discarded setup
instances and $1.034 for the H100 smoke, $1.606 total. All instances were destroyed; active rent is
zero.

## 7B staging gate

The 7B smoke begins only after the five new seed results are recorded. It must reuse the canonical
training/runtime path and first measure checkpoint configuration, trainable/frozen parameter scope,
estimated and observed VRAM, throughput, latency, wall time, and cost. Pair-oracle below 0.90 stops
the causal battery. Checkpoint recovery and long-run stability remain later gates; production is
not approved by a smoke result alone. The exact bounded protocol was registered before these seed
results were known in `state/store_causality_7b_staging_2026_08_10`. The smoke ran after this gate
closed but stopped at pair-oracle 0.5000; its negative arms were not read.
