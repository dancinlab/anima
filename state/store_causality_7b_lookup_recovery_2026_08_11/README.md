# Compose-2 CLMConvMoE 7B lookup recovery gate — 2026-08-11

Status: SUPPORTED-CAUSAL — lookup recovered; production remains blocked by serving throughput.

This gate follows the honest `FALSIFIED` result in
`state/store_causality_7b_rho_form_recovery_2026_08_11`. It keeps the compatible step-3,500 trunk,
frozen compose-2 data, seed, 2,200 updates, randomization, evaluator, arm order, and bars unchanged.
It reuses `cli/train.py --store-bridge`, the canonical lane-10 implementation in `core/clms.py`, and
`cli/evaluate.py --store-causality`. It adds no engine, trainer, evaluator, corpus row, prompt,
threshold, seed, retry, or result-dependent extension.

## Observed boundary and diagnostic order

The previous checkpoint passed rho-form at `1.00` and pair-oracle at `1.0000`, proving that the
completed trunk and the serialized parity/value/readout path work. Actual lookup reached only
`0.6094`. The frozen 512-row training manifest contains unary examples only: `mention_a` and
`mention_b` identify the same first-entity row and no row has `target_slot_b`. The held-out
compose-2 panel reads A at the first mention and B after `and`, from a different causal context.
Existing training telemetry measures only supervised live reads, while the NumPy address audit
records the answer-row attention computed before the dual-read replacement. Neither therefore
reports the two attentions that determine the actual lane-10 result.

The fixed Vast.ai diagnostic runs in this order:

1. load the exact failed checkpoint from its private `dancinlab` HF repository and reproduce
   rho-form, pair-oracle, and normal `0.6094` without changing inputs;
2. expose monitor-only A/B attention telemetry from the existing Torch and NumPy lane-10 paths,
   including target top-1, target mass, and entropy; prove Torch/NumPy parity on the same tensors;
3. stratify the fixed panel by A/B address correctness and verify the existing window, mention,
   operator, key, polarity, and answer-row coordinates against `StoreBindCell`;
4. identify the common learning/runtime cause. If the failure is not localized, record it and stop;
5. if localized, make the smallest shared-path correction without adding data or changing the
   target function, then run Python regression and actual tiny Torch-to-NumPy serialization parity;
6. train exactly 2,200 updates from the same step-3,500 source and seed 7;
7. require rho-form `>=0.70`, then pair-oracle `>=0.90`; only a pair-oracle pass unlocks normal →
   clue-A removal → clue-B removal → address shuffle → exact recovery;
8. require normal/recovery `>=0.75` and every control `<=0.56`. Only a complete pass unlocks the
   already-fixed serving, HTTP/WebSocket, performance, soak, and rollback battery.

## Frozen inputs, bars, and custody

- source code baseline: Git commit `137dd0ec3`;
- source trunk: private `dancinlab/clm-7b-undertrained-step3500` commit
  `c3c6d127545ccde6737fb96f99b51a2ac581d9e9`, `.clm` SHA-256
  `5e0db1371bc4ed7246ef5adcebe245c3991c053acd5fbde8107873add7853de5`;
- failed checkpoint: private
  `dancinlab/anima-store-causality-7b-rho-form-recovery-2026-08-11`, `.clm` SHA-256
  `d6de508b7a1dd440812dc5304bb5c702d03b5c8ccdc8bfdff798668807308db2`;
- frozen data: private `dancinlab/anima-store-causality-compose2-2026-08-09` commit
  `8f29c2f16f214734d9b5fa4010c57c48fff3979e`;
- seed 7; 24-byte window; batch 32; address weight 1.0; frozen source-preserving global trunk;
  value centering; canonical parity lane 10; exactly 2,200 updates;
- rho-form `>=0.70`, self-shuffle `<=0.05`, pair-oracle `>=0.90`, positive/recovery `>=0.75`,
  controls `<=0.56`.

Models, checkpoints, and training data remain only in private Hugging Face repositories under
`dancinlab`. Heavy work runs only on Vast.ai; scratch is deleted after verified HF upload. A failed
result is recorded without serving or production deployment. `ING.jsonl` and `stream_mi.json`
remain untouched.

## Fixed diagnostic amendment

The exact failed checkpoint reproduced pair-oracle `1.0000`, normal/recovery `0.6094`, clue-A
removal `0.5469`, clue-B removal `0.4609`, and shuffle `0.4688`. The new monitor-only audit exposed
the attentions actually consumed by lane 10: on the held-out panel read A had top-1 `0.7031` and
target mass `0.5498`; read B had top-1 `0.5703` and target mass `0.4830`. The oracle handed both
addresses and measured `1.0000`/`1.0000`, confirming that value/parity/readout remain intact.

The existing-name `compose2_seen` diagnostic scored `0.8125`, with both read-A and read-B top-1 at
`0.7500`. Thus second-position context alone does not explain the held-out collapse. The common
address path instead projects one final-byte trunk state into a key that is defined as the mean of
all bytes in the entity. At 7B this mismatched query/key unit retains seen-name identity but does
not reliably generalize unseen spellings.

The registered correction therefore keeps the same lane, tensors, data rows, loss, seed, update
count, and evaluator, but makes both training and NumPy runtime pool the complete entity mention
before applying the shared `W_q`. Mention ends already exist in the frozen manifests; starts are
derived canonically from each entity's byte length. No target slot, polarity, gold answer, new row,
or evaluator value enters the pooling operator. The store key and mention query now share the same
whole-entity unit.

## Fixed-condition result

The exact seed-7, 2,200-update recovery run completed on one full H100 PCIe. The serialized model
kept the source's global normalization and passed the unchanged canonical form gate at `1.00`
(self-shuffle `0.00`). Pair-oracle then passed at `1.0000`, unlocking the complete battery:

- normal `0.7734` -> clue A removed `0.4688` -> clue B removed `0.4453` -> address shuffled
  `0.5234` -> exact recovery `0.7734`;
- normal/recovery exceed the frozen `0.75` bar; all controls remain below `0.56`; shuffle integrity
  and exact recovery passed; the engine verdict is `SUPPORTED-CAUSAL`;
- live normal read-A/read-B top-1 improved to `0.6875`/`0.6484`; the pair oracle remained
  `1.0000`/`1.0000`, while shuffle reduced target top-1 to `0.0625`/`0.0391`.

The unlocked staging battery passed cold readiness (`11.03 s`), HTTP 100/100 (p95 `0.635 ms`),
three-recipient WebSocket fan-out 100/100 (p95 `0.541 ms`), serving VRAM (`54,733 MiB`), a
30-minute soak (360 probes, zero failures, RSS/GPU growth `0.116%`/`0%`), and CLM-to-AKIDA
rollback (`1.401 s` plus two-user broadcast). Generation latency passed at p95 `18.140 s`, but the
minimum fixed 32-byte throughput was `1.763 bytes/s`, below the unchanged `2.0 bytes/s` production
bar on this H100 PCIe. No faster-GPU retry or bar adjustment was made. The causal result is closed,
but production deployment remains blocked by serving throughput; the live broker and LaunchAgent
were not changed.

The checkpoint and exact-resume state are retained only in the private HF model repository
`dancinlab/anima-store-causality-7b-lookup-recovery-2026-08-11`. H100 regression passed `17/17`;
the local CPU-capable subset passed `8/8` with two Torch/GPU paths skipped. Full machine-readable
evidence is in `result.json`. Both Vast.ai instances were deleted after verified upload (active
rentals `0`, final billed total `$5.133`, including the excluded fractional offer). The unchanged
live broker LaunchAgent remained running; read-only production verification returned HTTP 200 and
a WebSocket `hello`. Its pre-existing participant state remains `anima_alive=false`.
