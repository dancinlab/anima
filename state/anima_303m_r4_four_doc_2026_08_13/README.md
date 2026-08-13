# R4 four-document optimization/capacity test — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

D0–D6 passed decoder bisimulation and located the first failure between one and four unique
dialogue documents. The frozen four-document baseline reached teacher-forced top-1 `0.6978`,
target-prefix recovery `2/4` and structural generation `1/4`. This protocol tests that boundary
without changing the four documents, assistant-turn objective, complete-document sampler, seed,
optimizer, peak learning rate, canonical decoder or behavioral bars after results are visible.

Four local Python arms are allowed. `B0` reproduces `d=128/L=4/600 steps`. `O1` changes only the
registered optimization horizon to 2,400 steps. `C1` changes only canonical width/head capacity to
`d=256/L=4`, and `C2` changes only depth to `d=128/L=8`; both remain at 600 steps. Each treatment
must reach teacher top-1 `>=0.95`, exact response and target-prefix recovery `4/4`, structural
generation `4/4`, and causal prompt control `4/4`. A baseline mismatch invalidates treatment
interpretation. Exact conditions and the result-independent decision table are in `protocol.json`.

This is a memorization/conditioning diagnosis, not evidence of held-out meaningful conversation.
No outcome directly authorizes 303M training, IIT-mouth coupling, participant mounting or
production. Model and data custody remains private HF `dancinlab`; Vast.ai is forbidden for this
local run. `ING.jsonl` and `stream_mi.json` remain untouched.
