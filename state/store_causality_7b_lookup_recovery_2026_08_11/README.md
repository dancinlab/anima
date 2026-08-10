# Compose-2 CLMConvMoE 7B lookup recovery gate — 2026-08-11

Status: REGISTERED — awaiting fixed-condition Vast.ai diagnosis and execution.

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
