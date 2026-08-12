# IIT daemon R1 — delayed state causality (2026-08-12)

This Python-only protocol is registered after R0 returned `SUPPORTED-CAUSAL-CORE` and before R1
implementation or result generation. It reuses `core.iit_daemon.IITDaemonCore`, its frozen
three-node XOR-ring TPM, intervention permutation, atomic snapshot, and the existing
`cli/evaluate.py` entry point. It does not add a model, trainer, alternate IIT instrument, mouth,
participant path, or adjustable evaluation panel.

## Question and claim boundary

R1 asks whether the same persistent core can carry a bounded causal cue across silent turns so
that a later categorical action depends on that state. The positive result must disappear when
state is reset or cue addresses are permuted, then return exactly after the registered snapshot is
restored.

Passing R1 may support only delayed state-to-action causality in this fixed four-class task. The
readout is a prescribed inverse of the frozen transition, not a learned semantic decoder. R1 does
not claim phenomenal consciousness, maximal-complex exclusion, learning, open-ended memory,
meaningful conversation, or production readiness. Phi remains neither a loss nor an action gate.

## Frozen task

- Initial intrinsic state: `0` for every independent trial.
- Balanced cue interventions: `0`, `1`, `2`, `4`; these are no cue and each one-node cue once.
- Delays: `1`, `2`, `4` autonomous no-event turns after cue encoding.
- Panel: the Cartesian product of four cues and three delays, exactly 12 trials.
- Action: invert the four stable states reached by the frozen XOR-ring from initial state `0`.
  Any state outside this complete registered codebook is an incorrect/unknown action.
- Chance: largest class frequency in the fixed panel, `3/12 = 0.25`.
- Address shuffle: the frozen cyclic node permutation `(1,2,0)`, which moves every one-node cue.
- Reset control: replace intrinsic state with `0` before every delayed no-event transition.
- Recovery: save the post-cue normal state atomically, execute the disruptive controls separately,
  reload that exact snapshot, and run the same delay and action readout.

The evaluator must preserve every trial's cue, delay, encoded state, final state, action, gold,
correctness, tick and audit head. It must reject invalid cue/delay/panel/codebook construction
rather than silently score it.

## Frozen gates

R1 returns `SUPPORTED-DELAYED-STATE-CAUSALITY` only when all checks hold:

1. The four cues are balanced and map bijectively to four distinct stable intrinsic states.
2. Normal accuracy is at least `0.75`.
3. Reset-every-turn accuracy is at most measured chance plus `0.06` (`0.31`).
4. Cyclic cue-address-shuffle accuracy is at most `0.31`.
5. Snapshot recovery accuracy is at least `0.75` and exactly equals normal accuracy.
6. Every recovered trial reproduces the normal final state and action for the same cue/delay.
7. R0's canonical TPM, checksum, all-state Phi vector and causal edge set remain unchanged.
8. Python unit/regression, CLI result replay, JSON, package/wheel and Git checks pass.

Pair-oracle and compose-2 evidence are not part of R1 and remain unchanged. No result-dependent
cue, delay, permutation, seed, threshold or readout adjustment is allowed. Failure is recorded as
`FALSIFIED` and blocks R2. Passing R1 opens only R2 CLMS two-address latching; R3 mouth-content
causality and meaningful conversation remain separately blocked.

## Execution state

Preregistered; implementation and results pending.
