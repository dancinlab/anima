# Compose-2 canonical parity reproducibility — 2026-08-10

Status: COMPLETE — `REPRODUCED` / `SUPPORTED-CAUSAL` on seeds 7 and 11.

This follow-up preserves the frozen compose-2 corpus, panel, control manifests, randomness, and
bars in `state/store_causality_2026_08_09`. It reuses the canonical `anima-py train` and
`anima-py evaluate --store-causality` paths. No composed row was added to training and no failed
seed was retried with a different recipe.

## Root cause

The training manifest has 512 one-clue rows, zero `target_slot_b` fields, and
`mention_a == mention_b` on all 512 rows. Legacy lane 8 duplicated that one address and formed
`[vA+vB ; (vA-vB)^2]`. Its second block was therefore exactly zero for every training row, received
no gradient, and became active for the first time on held-out unequal pairs. The seed-7 pass and
seed-11 pair-oracle 0.2500 failure were different random extrapolations through this untrained
off-diagonal block, not a panel or evaluator difference.

The shared CLMS runtime now serializes new dual checkpoints as lane 10. It keeps both existing
mention-conditioned address reads, composes their soft binary values with the canonical parity
identity `p = a + b - 2ab`, and interpolates `p` onto the same learned `val[0]/val[1]` manifold as
one-clue training. A missing B uses the XOR identity zero. This removes the train-unreachable
fusion region without teaching a composed example. Existing lane-8 checkpoints remain decoded
with their original semantics.

## Frozen repetition

- warm start: `.fire-recover/h9672_rv_sweep/RV3c_13_CONFIRM_orc1.00_p1_0.99_flip0.99.clm`
- architecture: d3784 / L4 / E3, frozen trunk, position-normalized dual CLMS lane
- training: unchanged 24-byte window, store batch 32, 24,000 steps, direct address supervision
- seeds: the previously registered 7 and 11
- gate order: pair-oracle first; controls only after pair-oracle is at least 0.90
- unchanged bars: normal/recovery at least 0.75; each control at most 0.56

## Results

| Seed | Pair oracle | Normal | Drop A | Drop B | Shuffle | Recovery | Verdict |
|---:|---:|---:|---:|---:|---:|---:|---|
| 7 | 1.0000 | 1.0000 | 0.3984 | 0.4453 | 0.4766 | 1.0000 | SUPPORTED-CAUSAL |
| 11 | 1.0000 | 1.0000 | 0.3906 | 0.4609 | 0.4766 | 1.0000 | SUPPORTED-CAUSAL |

Both independent initializations pass the instrument and the full causal battery. This closes the
specific two-seed reproducibility failure recorded in `state/store_causality_repro_2026_08_10`;
it is not a claim about arbitrary seeds or more than two clues.

Recovered artifacts:

- seed 7 `.clm`: `0073bfb60d4686e96d1029b5c581231f51b2a17a122dd454f18365b4c88c5e89`
- seed 7 `.clm.pt`: `1dcea452f041af45999b6979e4785cf1afa17d2d02a275a7221b69d994d09682`
- seed 11 `.clm`: `d13cc3603ee3295b8d6fec3f3d7b256b8da6c063258097a6d9bc247a17b162cb`
- seed 11 `.clm.pt`: `14880777e2449e9b38ea9364d6f460b861b88e9a4af3b12478d1bd4ca180e8ad`
- local root: `.fire-recover/store_causality_canonical_2026_08_10/`

QA on Vast.ai RTX 3090: canonical pytest collection passed 17/17; Torch↔NumPy learned-address and
pair-oracle parity errors were `6.245e-17` and `5.898e-17`; the legacy lane-8 seed-7 checkpoint
reproduced its original six-arm result exactly. Training took 2,062.3s (seed 7) and 1,893.8s
(seed 11). Instance `47297500` and the failed incompatible-image instance were removed; active
Vast.ai instances are zero. Total estimated rental cost was about $0.26.

## Production outlook

As of 2026-08-10, an experimental 7B staging deployment is estimated at 1–2 weeks and a
production deployment at 4–8 weeks. These are conditional estimates: broader multi-seed
repetition, 7B staging training with measured memory and latency, and long-running stability
validation remain required gates. This canonical change was committed as `87b504489` and pushed
to `origin/main`. Chat runtime code was not changed, so neither the local LaunchAgent nor
`https://chat.dancinlab.org` was redeployed. The user-owned untracked files `ING.jsonl` and
`stream_mi.json` remain preserved.

## Registered next run

The next run keeps this compose-2 panel, recipe, randomness, and bars frozen. It first verifies the
baseline artifacts, then runs at least five new seeds on Vast.ai. A failed pair-oracle is recorded
and diagnosed in the shared training/runtime path; it is never repaired by selecting a new seed or
changing the panel. Only seeds reaching pair-oracle 0.90 proceed to the five-arm causal battery.

After multi-seed closure, the same canonical training path is scaled to a bounded 7B staging smoke:
VRAM, throughput, latency, wall time, and cost are measured, followed by checkpoint recovery and a
long-run stability gate. Chat staging HTTP/WebSocket QA is required only if the chat runtime path is
changed. Production remains blocked until every recorded gate passes. GPU-heavy work runs on
Vast.ai rather than mini.
