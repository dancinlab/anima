# R4 deterministic four-document treatments — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

The native two-thread CPU gate produced exact duplicate trajectories. This protocol reruns the
previously uninterpretable four-document treatments under that execution contract. The baseline is
frozen at teacher top-1 `0.7240293809024134`, target-prefix `2/4` and structural `1/4`, with zero
tolerance on the teacher score.

`B0` reproduces `d=128/L=4/600 steps`. `O1` changes only the horizon to 2,400 steps. `C1` changes
only canonical width/head capacity to `d=256/L=4`; `C2` changes only depth to `d=128/L=8`, both at
600 steps. A treatment passes only with teacher top-1 `>=0.95`, exact/target/structural `4/4` and
causal prompt control `4/4`. Exact conditions and the result-independent decision table are in
`protocol.json`.

This local memorization/conditioning result cannot itself authorize 303M, IIT-mouth coupling,
participant mounting or production. Vast.ai is forbidden and `ING.jsonl` plus `stream_mi.json`
remain untouched.
