# R4 aligned 64-document exposure match — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

Aligned 32 documents pass at 600 steps, while 64 documents retain teacher top-1 `0.9669` and
prompt control but fail exact rollout. This one-arm test uses 64 documents and 1,200 steps, exactly
matching the passing A32 arm's expected presentations per unique document. Model, sampler, data,
objective, optimizer, decoder and all gates remain fixed.

The first eight probes require teacher top-1 `>=0.95`, exact/target/structural `8/8`, and prompt
control `8/8`. This memorization test cannot authorize 303M, IIT coupling or production. Vast.ai
and user files remain untouched.
