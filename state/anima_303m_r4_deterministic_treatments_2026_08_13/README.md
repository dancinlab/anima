# R4 deterministic four-document treatments — 2026-08-13

Status: **COMPLETED — FALSIFIED-BOUNDED-HORIZON-AND-CAPACITY-TREATMENTS**.

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

## Result

The deterministic baseline reproduced exactly. None of the registered treatments passed:

| Arm | Teacher top-1 | Target | Structural | Exact | Prompt CE control |
| --- | ---: | ---: | ---: | ---: | ---: |
| B0 `d128/L4/600` | `0.7240` | `2/4` | `1/4` | `1/4` | `3/4` |
| O1 `d128/L4/2400` | `0.7933` | `3/4` | `1/4` | `1/4` | `3/4` |
| C1 `d256/L4/600` | `0.7849` | `3/4` | `1/4` | `1/4` | `3/4` |
| C2 `d128/L8/600` | `0.7639` | `2/4` | `1/4` | `1/4` | `3/4` |

O1 and C1 learned the first three responses at teacher top-1 `1.0`, but the fourth response failed
from byte zero with CE `7.704` and `6.310`. The fourth document is at corpus EOF: legacy stream
framing can only place its user role around byte position 222, while evaluator/runtime starts an
isolated user role at position zero. This reveals a training-to-runtime position-map gap rather
than uniform capacity shortage. The next separately preregistered single-axis treatment aligns the
selected complete document to runtime position zero while preserving the legacy stream mode as a
control. All larger and production gates remain blocked.
