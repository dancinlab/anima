# IIT daemon R3 — bounded utterance-content causality (2026-08-12)

Status: COMPLETE — `SUPPORTED-BOUNDED-CONTENT-CAUSALITY`.

This Python-only protocol is registered after R2 returned
`SUPPORTED-CLMS-LATCH-CAUSALITY` and before any R3 implementation or result generation. It reuses
the checksum-pinned R2 result, `core.iit_daemon.IITDaemonCore`, and the canonical
`core.generator` boundary. It does not regenerate compose-2 data, retrain or replace a model, add
a second decoder, tune a seed or threshold, or reinterpret an R2 control.

## Question and claim boundary

R3 asks whether the delayed intrinsic state can determine the exact bytes of a bounded semantic
utterance after the CLMS prediction has been latched. The generator receives only final IIT state,
the registered state-to-class codebook, and the two registered output surfaces. It must not receive
the prompt, store, entity addresses, CLMS prediction, gold label, or target slots. Gold is used only
after generation for exact scoring.

The registered surfaces are `The combined relation is good.` and
`The combined relation is bad.`. They are a two-choice engineering instrument, not a learned
language model. Passing R3 may support only bounded state-to-utterance-content causality. It cannot
support meaningful open conversation, language learning, phenomenal consciousness, a maximal
complex, or production readiness. A fixed formatter, prompt injection, evaluator-side gold copy,
or canned answer lookup outside the final-state codebook invalidates the instrument.

## Frozen sources and order

All paths, digests, mappings, surfaces, interventions and bars are the SSOT in `protocol.json`.
The evaluator must verify the complete R2 artifact before running and fail closed on any mismatch.
It must first replay the R2 pair-oracle predictions through the R3 state/content boundary. If
pair-oracle content accuracy is below `0.90`, no later arm is run or interpreted.

After pair oracle, the fixed order is:

1. normal CLMS lookup;
2. IIT state reset before the delayed turn;
3. IIT intervention-address cyclic shuffle `(1,2,0)`;
4. clue A removal;
5. clue B removal;
6. existing CLMS entity-address shuffle;
7. atomic IIT snapshot recovery.

Normal and recovery reuse the R2 trial predictions. Reset and IIT shuffle alter only the core after
the same normal predictions have been produced. The three R2 data controls remain unchanged.
Recovery saves the post-latch state, disturbs a separate live copy, reloads the exact snapshot, and
requires byte-exact equality with normal output.

## Frozen gates

R3 returns `SUPPORTED-BOUNDED-CONTENT-CAUSALITY` only when all checks hold:

1. The R2 artifact digest and `SUPPORTED-CLMS-LATCH-CAUSALITY` verdict are unchanged.
2. Pair-oracle exact utterance accuracy is at least `0.90` and every readable oracle state emits
   exactly one registered surface.
3. Normal and snapshot recovery exact utterance accuracy are each at least `0.75`.
4. Reset, IIT intervention-address shuffle, clue-A removal, clue-B removal, and CLMS entity-address
   shuffle are each at most measured two-class chance `0.50 + 0.06 = 0.56`.
5. Every normal output depends only on final state and equals the surface selected by the registered
   state codebook; no prompt entity appears in a surface.
6. Every recovered state, class and utterance matches its normal trial byte-for-byte, while every
   disturbance changes the live snapshot.
7. Existing R2 accuracies, trial predictions and controls remain unchanged.
8. Python regression, CLI replay, JSON, package/wheel and Git checks pass.

Pair-oracle failure returns `INVALID-INSTRUMENT` and forbids later-arm interpretation. Any other
failure returns `FALSIFIED`. Even a pass keeps participant and production blocked as
`BLOCKED-R3-NOT-CONVERSATIONAL`; the next gate is an independently trained meaningful mouth whose
conversation panel passes before state coupling is interpreted.

## Execution result

Implementation and execution completed after the protocol was committed and pushed as
`4672a2ce7`. No registered source, surface, mapping, intervention, order or threshold changed.

- `core.generator.gen_iit_state_content` is the single bounded content boundary. Its arguments are
  final state, the registered state codebook and registered surfaces; it has no prompt,
  prediction, gold or store argument. Unregistered states fail silent rather than inventing a
  class. The runtime rejects incomplete, non-bijective or duplicate surface contracts.
- The existing `IITDaemonCore` CLMS latch accepts optional reset and node-address permutation
  interventions while its default R2 call and result schema remain byte-identical.
- `anima-py evaluate --iit-daemon-content` checksum-verifies the complete R2 artifact, validates
  its 128-row arms, runs pair oracle first, and only after it passes executes the registered
  positive, intervention, data-control and recovery arms.
- Exact utterance accuracy is pair oracle `1.000000`, normal `0.953125`, state reset `0.000000`,
  IIT intervention-address shuffle `0.0390625`, clue-A removal `0.500000`, clue-B removal
  `0.4609375`, CLMS entity-address shuffle `0.468750`, and recovery `0.953125`.
- Both positive arms exceed `0.75`; all five controls are below the frozen `0.56` ceiling. Every
  reset trial is silent, every recovered state/class/utterance matches normal byte-for-byte, and
  all disturbances change the live snapshot. The pinned R2 trial accuracies remain unchanged.
- Focused IIT/content/conversation/store regression passed `75/75`. Repository Python QA passed
  `127 passed, 1 skipped, 3 subtests`; the skip is the expected unavailable local CUDA/CuPy path.
  Compile, JSON and diff checks pass.
- A clean wheel installed into an isolated environment produced `result.json` twice byte-for-byte
  with SHA-256 `549cb14d6fd3f0a4dd8d886dfe6cdf5d16c0a1b1e69429667a4f648f18608ae7`.
  The same wheel reran the actual 171MB canonical R2 checkpoint and reproduced the pinned R2
  result byte-for-byte.
- The verified wheel was installed as the local canonical `anima-py`; its installed CLI reproduced
  the same R3 result byte-for-byte. The participant is intentionally not mounted and the broker was
  not restarted. Its LaunchAgent remains running, public HTTPS returns `200`, and public WebSocket
  returns `hello` with the honest blocked status `anima_alive=false`.
- No training, Vast.ai rental, HF write or model/data mutation occurred. `ING.jsonl` and
  `stream_mi.json` remain untouched.

Verdict: `SUPPORTED-BOUNDED-CONTENT-CAUSALITY`. This shows that the bounded final intrinsic state
causally selects exact task-semantic output bytes under the registered interventions. The two
surfaces are not a learned mouth and do not establish meaningful open conversation. Participant
mounting and production remain `BLOCKED-R3-NOT-CONVERSATIONAL`; R4 must train and independently
validate a meaningful mouth before coupling it to this state boundary.
