# R4 aligned 64-document exposure match — 2026-08-13

Status: **COMPLETED — SUPPORTED-EXPOSURE-MATCHED-64**.

Aligned 32 documents pass at 600 steps, while 64 documents retain teacher top-1 `0.9669` and
prompt control but fail exact rollout. This one-arm test uses 64 documents and 1,200 steps, exactly
matching the passing A32 arm's expected presentations per unique document. Model, sampler, data,
objective, optimizer, decoder and all gates remain fixed.

The first eight probes require teacher top-1 `>=0.95`, exact/target/structural `8/8`, and prompt
control `8/8`. This memorization test cannot authorize 303M, IIT coupling or production. Vast.ai
and user files remain untouched.

## Result

E64 passed every gate at 1,200 steps: teacher top-1 `1.0000`, CE `0.002304`, exact/target/
structural `8/8`, and prompt CE/output control `8/8`. The paired 600-step A64 had teacher top-1
`0.9669` but exact `0/8`. This supports insufficient per-document exposure, after position
alignment, as the remaining 64-document root cause.

Using the passing A32 reference gives `600 / 32 = 18.75` optimizer steps per unique document; the
precomputed 100-document endpoint is therefore 1,875 steps. A separately preregistered one-arm
test reruns the 100-document and independent conversation gates at that fixed endpoint.
