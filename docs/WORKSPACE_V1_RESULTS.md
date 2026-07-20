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

## Realizer and resource finding

The existing 303M mouth preserved every required structured field in 0/10 attempted natural-language
realizations. The seam therefore failed closed to the structured renderer in all ten cases; no meaning-
dropping model output was accepted. This is a measured limitation, not reported as a model win.

On this CPU host, the full canonical 303M ρ-AXON run was terminated by memory pressure after 2–3
decodes. The same runner completed five decodes with the tiny smoke checkpoint (its reach scores were
expectedly INVALID). The default-off chat path performs no workspace import or substitution, and the
workspace is restricted to the spoken-text seam when explicitly enabled.
