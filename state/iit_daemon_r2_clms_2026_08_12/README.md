# IIT daemon R2 — CLMS two-address latch (2026-08-12)

Status: PREREGISTERED — implementation and result generation have not started.

This Python-only protocol is registered after R1 returned
`SUPPORTED-DELAYED-STATE-CAUSALITY` and before R2 implementation or result generation. It reuses
the frozen compose-2 material and canonical seed-7 lane-10 checkpoint, the existing
`core.clms.store_apply`/`cli.evaluate.store_run` read, and `core.iit_daemon.IITDaemonCore`. It does
not regenerate data, train a model, add a language engine, move a bar, choose a seed, or introduce
an alternate store evaluator.

## Question and claim boundary

R2 asks whether the already validated CLMS two-address result can be latched as a bounded
intervention into the persistent IIT core so that the later categorical action depends on the
CLMS result. The core must receive only one of two registered one-node cues from the CLMS
prediction. It must not receive the store, entity addresses, prompt, target slots, or gold label.

Passing R2 may support only a fixed two-address-read to bounded-state/action causal chain. It does
not show that Phi measures consciousness, that this three-node candidate is a maximal complex, or
that the system understands language. The compose-2 strings are a synthetic instrument, not a
meaningful mouth. R2 cannot authorize participant or production deployment.

## Frozen sources

- Checkpoint: canonical lane-10 seed 7, SHA-256
  `0073bfb60d4686e96d1029b5c581231f51b2a17a122dd454f18365b4c88c5e89`.
- HF source: private `dancinlab/anima-store-causality-multiseed-2026-08-10` revision
  `16731bacb8bf449e22563917aefe0d5ebe87c85d`, artifact
  `seed7/compose2_dual_parity_s7.clm`.
- Normal compose-2 panel: the existing 128 rows at SHA-256 `f2e5bd17...11939`.
- Clue-A removal: the existing 128 rows at SHA-256 `79e03d33...0aa0`.
- Clue-B removal: the existing 128 rows at SHA-256 `9536ace9...bb0`.
- Existing store settings: 24-byte window and address-control seed `9423`.
- Existing ordering: pair oracle first; no normal or negative-control arm may run when it is below
  `0.90`.

Every path, full digest, task value and gate is the single source of truth in `protocol.json`. The
evaluator must verify the checkpoint, panel and R1 result bytes before execution and fail closed on
any mismatch.

## Frozen latch and arm order

The fixed class-to-cue map is `good -> 1`, `bad -> 2`. Both are distinct one-node interventions.
For each CLMS prediction an independent state-zero core executes that intervention, advances one
autonomous no-event turn, and decodes the final state through the codebook derived from the frozen
transition. Gold is retained only for scoring after the action has been produced.

The registered order is:

1. CLMS pair oracle and latch integrity;
2. normal lookup;
3. clue A removal;
4. clue B removal;
5. CLMS entity-address shuffle;
6. normal snapshot recovery.

Recovery saves the post-latch state, disturbs a separate live copy, reloads the exact atomic
snapshot, advances the same one silent turn, and requires final state and action equality with the
normal trial. The address shuffle is the existing deterministic CLMS Sattolo arm; it is not an IIT
node permutation and must move every unique entity.

## Frozen gates

R2 returns `SUPPORTED-CLMS-LATCH-CAUSALITY` only when all checks hold:

1. R1 artifact and R0 mechanics fingerprints are unchanged.
2. The compose-2 panel remains balanced with measured chance `0.50`.
3. Pair-oracle CLMS accuracy and pair-oracle latched-action accuracy are each at least `0.90`.
4. Every readable CLMS prediction maps to exactly one registered bounded cue, and every latched
   action equals that prediction.
5. Normal latched-action accuracy is at least `0.75`.
6. Clue-A removal, clue-B removal and address shuffle are each at most measured chance plus `0.06`,
   namely `0.56`.
7. Shuffle integrity has zero fixed entities under the existing store evaluator.
8. Recovery is at least `0.75`, exactly matches normal accuracy, and reproduces every normal final
   state and action.
9. Python unit/regression, actual checkpoint, CLI replay, JSON, package/wheel and Git checks pass.

Failure is recorded without changing data, randomness, mapping, delay, thresholds or readout. A
pair-oracle failure returns `INVALID-INSTRUMENT` and forbids interpretation of later arms. Any other
gate failure returns `FALSIFIED` and blocks R3. Passing R2 opens only R3 mouth-content causality;
meaningful conversation and production remain blocked as `BLOCKED-R2-NOT-A-MOUTH`.
