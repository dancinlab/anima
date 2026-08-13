# R4 deterministic CPU baseline gate — 2026-08-13

Status: **COMPLETED — SUPPORTED-DETERMINISTIC-TRAJECTORY**.

Apple MPS correctly failed closed because its indexed accumulated backward operation lacks a
deterministic implementation. This protocol reuses the same shared trainer and exact duplicate
gate on CPU with two threads; it does not weaken the native deterministic contract or use
warn-only execution.

Two fresh processes train the same four documents with `d=128/L=4/600 steps`. Engine SHA-256,
checkpoint state digest, every model tensor, teacher trace and canonical behavior must match
exactly. The result does not authorize 303M, IIT-mouth coupling, participant mounting or
production. No Vast.ai instance is allowed and `ING.jsonl` plus `stream_mi.json` remain untouched.

## Result

The two fresh CPU processes produced the same engine SHA-256
`2afc3c75…d8086cb6`, checkpoint state digest `ab386012…92d0321f`, every one of 53 model tensors,
teacher trace and canonical behavioral result. Maximum tensor error was exactly `0.0`. Both runs
scored teacher top-1 `0.724029`, target-prefix `2/4`, structural `1/4`, exact `1/4`, and prompt
control `3/4`; this remains a failing behavioral baseline but is now a valid exact execution
reference.

The verdict is `SUPPORTED-DETERMINISTIC-TRAJECTORY`. A separately preregistered treatment
comparison may use this exact CPU execution contract. The result does not itself authorize 303M,
IIT-mouth coupling, participant mounting or production.
