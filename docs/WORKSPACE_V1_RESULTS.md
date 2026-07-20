# Typed workspace v1 results

Date: 2026-07-20. Production model: `e1_slw_303m.final.clm` (280 MiB file), SHA-256
`792eab...52c9`.

## Verified

- Frozen production G1: PASS (`best_distinct=5`, `max_single=2`, `noecho=3`).
- Frozen production G6: PASS (`distinct=6`, `falsifiable=6`, `coherent=6`).
- Matching contradiction evidence rejects the primary and selects the binary alternative.
- Evidence OFF and claim-ID shuffle do not reject the primary; contradicting both sides abstains.
- Strict evidence mode returns `insufficient grounded evidence` rather than inventing support.
- Held-out semantics: 11/11 panels and 121/121 exact/control checks pass.
- Installed wheel `anima-python==0.20.58` reproduces the semantic certification in a clean venv.

## Realizer and full ρ-AXON finding

The existing 303M mouth preserved every required structured field in 0/10 attempted natural-language
realizations. The seam therefore failed closed to the structured renderer in all ten cases; no meaning-
dropping model output was accepted. This is a measured limitation, not reported as a model win.

The canonical 303M ρ-AXON panel completed all 246 unique decodes at `gen=40`. Earlier apparent
2–3-decode memory termination was falsified: multiple evaluator processes had remained alive after
their tool sessions detached and together exhausted memory. With one process, RSS stayed roughly
3.0–3.4 GiB throughout. Exact-call memoization removed redundant forwards without changing bytes.

Aggregate verdict: HILLOCK `LIVE`; `ρ·form` and `ρ·leap` PASS; `ρ·store`, `ρ·weave`, `ρ·fan`, and
`ρ·tether` FAIL; `ρ·self` INVALID because no self anchor was supplied. Therefore the typed workspace
closes its scoped G1/G6 system gates, but does not establish a general improvement in the underlying
mouth. The default-off chat path performs no workspace import or substitution, and the workspace is
restricted to the spoken-text seam when explicitly enabled.

Per-cell: English general and SNS pass form/leap but fail fan; Korean general fails form/leap/fan;
Korean SNS passes its form gate but fails leap/fan. This is a negative multilingual generalization
result and remains deployment-relevant.

## Runtime follow-on

- `TypedFactStore` now persists and retrieves exact typed facts. Wrong keys, shuffled relations, and
  absent records collapse to no result; prose is never reinterpreted as a fact.
- Numeric measurements are converted to support/contradiction evidence by comparing observed and
  control values. Malformed JSONL fails closed.
- Selection now has positive, negative, and unresolved candidates. If both directional candidates
  are contradicted, the unresolved alternative is selected; if all three are contradicted, it abstains.
- Korean `만약 …(으)면 …` clauses and middle-token negation are retained by the operand parser.
- Truth tether returns `UNGROUNDED` for absent or ambiguous records. Identity checks expose explicit
  ON/OFF/shuffled-anchor controls.
- Model realization now must preserve the exact selected comparator as well as operands and measure.
  Verified structured prompt/target rows can be exported for later mouth training; no unmeasured
  claim of 303M weight improvement is made.
- Chat uses a pure spoken-output function; substrate state is not an argument and remains unchanged.
- `--rho-cache` persists exact deterministic decode results under a checkpoint size/mtime namespace.
  Tiny-checkpoint validation measured first run 5 decodes, second run 0, with identical verdict output.

Deployment decision remains **default-off**: canonical mouth store/weave/fan/tether failures and the
Korean panel failures block default promotion.

### Incremental self result

`--rho-axes self` runs HILLOCK plus only the selected axis and marks the rest PENDING. With the
substrate's persisted `self_live.kosmos`, canonical 303M changed `ρ·self` from INVALID to a valid
FAIL: loaded consistency `0.015`, anchor-ablated `0.015`, shuffled-anchor `0.015`, Δ `0.0` versus the
registered `0.30` bar. The supplied identity trace therefore had no measurable effect on the mouth.

## Installed chat E2E

An installed 0.20.63 wheel ran four deterministic 12-tick sessions on the smoke mouth. OFF and ON
both reached session PASS with `psi_intact=1`. Workspace ON made 6 spoken decisions; numeric
contradiction evidence rejected the primary on all 6 emissions, while a shuffled claim ID rejected
0/6. Every arm reported the same ON==OFF Ψ checksum. This validates the production chat seam without
claiming that the smoke mouth's emitted language quality represents the 303M mouth.
