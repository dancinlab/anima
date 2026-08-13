# R4 deterministic CPU baseline gate — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

Apple MPS correctly failed closed because its indexed accumulated backward operation lacks a
deterministic implementation. This protocol reuses the same shared trainer and exact duplicate
gate on CPU with two threads; it does not weaken the native deterministic contract or use
warn-only execution.

Two fresh processes train the same four documents with `d=128/L=4/600 steps`. Engine SHA-256,
checkpoint state digest, every model tensor, teacher trace and canonical behavior must match
exactly. The result does not authorize 303M, IIT-mouth coupling, participant mounting or
production. No Vast.ai instance is allowed and `ING.jsonl` plus `stream_mi.json` remain untouched.
