# R4 aligned 32/64-document boundary — 2026-08-13

Status: **COMPLETED — BOUNDARY-BETWEEN-32-AND-64**.

Aligned 16 documents pass at 600 steps while aligned 100 fail. This bounded test runs only the
deterministically derived 32- and 64-document views with the same tiny model, 600 steps, aligned
sampler, deterministic CPU execution, objective, optimizer and decoder. Each arm is scored on its
first eight fixed probes and must reach teacher top-1 `>=0.95`, exact/target/structural `8/8`, and
prompt control `8/8`.

This is a memorization boundary, not meaningful-conversation evidence. It cannot authorize 303M,
IIT coupling, participant mounting or production. Vast.ai and user files remain untouched.

## Result

A32 passed with teacher top-1 `1.0000`, exact/target/structural `8/8` and prompt control `8/8`.
A64 retained teacher top-1 `0.9669` and prompt control `8/8`, but scored target `6/8`, structural
`5/8` and exact `0/8`. The boundary is therefore between 32 and 64 documents at 600 steps.

Because A64 is already teacher-forced high and prompt-controlled, this looks like a near-threshold
exposure/rollout boundary rather than uniform capacity collapse. The next single arm uses 1,200
steps at 64 documents, exactly matching A32's expected presentations per unique document.
