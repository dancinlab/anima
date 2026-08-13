# R4 four-document optimization/capacity test — 2026-08-13

Status: **COMPLETED — INVALID-BASELINE-MISMATCH**.

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

## Result

The fail-closed baseline gate fired. The new run preserved target-prefix `2/4`, structural `1/4`
and exact `1/4`, but teacher top-1 was `0.728227` rather than the frozen `0.697796` and exceeded
the registered `0.002` tolerance. The verdict is therefore `INVALID-BASELINE-MISMATCH`; the O1/C1/C2
outputs exist but are not interpreted as treatment evidence.

The current scorer replayed the preserved HF baseline at exactly `0.697796`, ruling out evaluator
drift. Old and new recipes match except temporary paths, source and four-document bytes match, and
steps 1 and 100 logged identically. The trajectories first differed at step 200; all 53 final model
tensors differed, with maximum absolute difference `0.0208993`. This is seeded but nondeterministic
MPS training, not changed data or decode. `baseline_forensics.json` preserves the hashes and raw
comparison.

The shared trainer now exposes an explicit native `--deterministic` contract. It calls PyTorch's
fail-closed deterministic algorithms and records the setting in checkpoint recipes and summaries;
a seed alone is no longer treated as proof of an exact device trajectory. A separately
preregistered duplicate-baseline gate must prove byte-identical deterministic execution before the
same treatments can be interpreted. 303M, IIT-mouth coupling, participant mounting and production
remain blocked.
