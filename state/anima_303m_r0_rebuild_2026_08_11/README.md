# Anima 303M R0 native-mouth rebuild — 2026-08-11

Status: IN PROGRESS — seed 7 complete; seeds 11 and 13 remain.

The previous 303M run honestly failed at `rho-form 3/5`, but it did not reproduce the successful
native-byte lineage: it used one 60.05 MB general-English cell, constant LR, AdamW beta2 `0.999`,
zero weight decay, 6,000 updates, and one seed. R0 therefore tests the existing ByteGPT engine under
the broad-plus-dialogue bilingual training conditions that were missing. It does not add a model
architecture, evaluator, prompt, threshold, or post-result retry.

`protocol.json` is the execution SSOT. It pins five existing HF `dancinlab` corpus files by commit,
for 282,414,903 bytes total: the historical 154.85 MB 70/30 broad-dialogue register plus clean
English/Korean general and SNS cells. The trainer consumes these through immutable
`hf://datasets/<repo>@<commit>/<file>` references, proportional sampling, and `--require-cells 5`.
No training data or model artifact is kept outside HF custody after the run.

Each seed in `[7, 11, 13]` starts from random initialization at ByteGPT V256, d1024, 24 layers,
16 heads, block 512. The fixed endpoint is 14,000 updates, global batch 32, bf16, AdamW
`beta=(0.9,0.95)`, weight decay `0.1`, peak LR `3e-4`, 500-step linear warm-up, then cosine decay to
`0.1x` at step 14,000. Intermediate 2,000-step checkpoints are diagnostics only; the final
step-14,000 checkpoint is always the scored checkpoint, so validation or gate output cannot select
an easier endpoint.

R0 uses the existing canonical chain:

`cli/train.py --arch bytegpt` -> `core/model.py::ByteGPT` -> `core/serialize.py` ->
`core/decode.py` -> `cli/evaluate.py --rho-axon --rho-axes form --rho-out`.

The gate requires HILLOCK `LIVE`, aggregate `rho-form >= 0.70`, self-shuffle `<= 0.05`, and the
registered English/Korean cell breakout for every one of all three seeds. The JSON evidence must
retain every generated string, its known-word ratio, its shuffle score, and seed. A failed seed is
recorded as a failure; data, seed, endpoint, sampling, prompt, detector, and threshold do not change.

R1 remains locked until R0 passes 3/3. If unlocked, R1 will compare a parameter-matched stateless
ByteGPT control, a recurrent latent-workspace ByteGPT treatment, and a workspace-reset ablation on
the same data and compute. If R0 fails, no workspace result is run or interpreted.

Before GPU execution, Python compile, schedule boundaries, legacy constant-LR behavior, immutable
HF URI parsing, exact-resume, serializer/decode, and rho evidence regressions must pass. Execution
runs only on Vast.ai. Results, hashes, HF revisions, QA, and cost are recorded here and in a result
JSON, committed, and pushed. The H100 is deleted at completion even when the gate fails.

`ING.jsonl` and `stream_mi.json` are existing user files and remain untouched.

## Interim execution record

Vast.ai seed 7 reached the fixed 14,000-step endpoint with pooled held-out CE `0.99906`; all five
registered cells were below the uniform baseline. Its final engine SHA-256 is
`6b30cce18221fa541f310122833c4cdf7d1c2e9fd027d3fc4a2aca959767e0da`.

The frozen final-checkpoint panel returned HILLOCK `LIVE`, aggregate rho-form `0.40`, and
self-shuffle `0.00`, so seed 7 failed the aggregate `0.70` gate. The English general and SNS cells
both returned `0.40`/FAIL; Korean general returned `0.40`/PASS under its registered `0.20` bar and
Korean SNS returned `0.60`/PASS. Raw generation, KWR, shuffle KWR, and seeds are retained in the
machine result. R1 is therefore locked; the remaining preregistered R0 seeds still run so the
failure's reproducibility is measured without a result-dependent retry.

This run also exposed two shared runtime defects before the seed result could be preserved. The
ByteGPT loader and KV forward were NumPy-only even when the existing canonical CUDA dispatcher was
live, leaving a paid H100 idle. They now use one-time device residency and the same CUDA-backed
attention/KV path while preserving the CPU path. H100 tests verified CPU/CUDA logits within
`1e-10` and identical seeded token streams; the real 303M load took `2.038 s` and an 8-byte decode
`0.552 s`. The second defect was rho JSON serialization rejecting arbitrary byte-mouth
surrogateescape output. Raw bytes are now retained losslessly as standards-compliant escaped JSON.
