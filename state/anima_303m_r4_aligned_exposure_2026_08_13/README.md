# R4 aligned 16-document exposure test — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

Alignment fixes four-document conditional learning, while aligned 100 documents fail at 600
steps. This two-arm local Python experiment tests whether the remaining boundary is expected
presentations per unique document rather than model capacity.

Both arms use the first 16 source-order complete exchanges whose responses fit the canonical
192-byte budget, document alignment, `d=128/L=4`, seed 7 and the same optimizer/objective/decoder.
`S16` retains 600 steps. `E16` uses 2,400 steps, matching the successful four-document arm's
expected presentations per unique document at batch 8. The first eight probes require teacher
top-1 `>=0.95`, exact/target/structural `8/8`, and prompt causal control `8/8`.

No result authorizes 303M, IIT coupling, participant mounting or production. Vast.ai is forbidden
and the user files remain untouched.
