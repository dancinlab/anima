# R4 deterministic baseline gate — 2026-08-13

Status: **COMPLETED — FAIL-DETERMINISTIC-UNSUPPORTED**.

The preceding four-document experiment stopped because a same-seed/same-recipe MPS baseline did
not reproduce the preserved trajectory. The current scorer exactly reproduced the old checkpoint,
while all 53 newly trained tensors diverged after step 100. This protocol tests the shared
trainer's new native `--deterministic` contract before any treatment is rerun.

Two fresh processes train the same four documents with the same `d=128/L=4/600-step` recipe and
the same input paths. The gate requires exact engine SHA-256, checkpoint state digest, every model
tensor, teacher trace and canonical behavioral score. Unsupported deterministic operations fail
closed. No approximate metric tolerance can pass this gate. Exact conditions are in
`protocol.json`.

This gate does not authorize 303M, IIT-mouth coupling, participant mounting or production. It uses
no Vast.ai instance and leaves `ING.jsonl` and `stream_mi.json` untouched.

## Result

The gate failed closed on the first backward pass. PyTorch reported that
`index_put_with_accumulate_mps` has no deterministic implementation while native deterministic
algorithms are enabled. No model checkpoint was emitted, no second run was needed, and warn-only
or per-operator bypass was not used. This validates the trainer guard but falsifies Apple MPS as
an exact-trajectory execution backend for this recipe. The raw error is preserved in `result.json`.

The next admissible step is a separately preregistered two-thread CPU duplicate gate. The invalid
four-document treatments remain uninterpreted, and all larger/model/runtime gates remain blocked.
