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
