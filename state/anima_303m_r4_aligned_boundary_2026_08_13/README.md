# R4 aligned 32/64-document boundary — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

Aligned 16 documents pass at 600 steps while aligned 100 fail. This bounded test runs only the
deterministically derived 32- and 64-document views with the same tiny model, 600 steps, aligned
sampler, deterministic CPU execution, objective, optimizer and decoder. Each arm is scored on its
first eight fixed probes and must reach teacher top-1 `>=0.95`, exact/target/structural `8/8`, and
prompt control `8/8`.

This is a memorization boundary, not meaningful-conversation evidence. It cannot authorize 303M,
IIT coupling, participant mounting or production. Vast.ai and user files remain untouched.
