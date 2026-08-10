# Compose-2 CLMConvMoE 7B long-run and checkpoint recovery gate — 2026-08-10

Status: COMPLETE — exact recovery and the frozen causal battery passed.

This gate follows the failed bounded smoke in `state/store_causality_7b_staging_2026_08_10`.
It extends the existing `cli/train.py`, `core/clms.py`, and `cli/evaluate.py` paths only. It does
not introduce a trainer, engine, evaluator, corpus, panel, control, randomization, or bar.

## Frozen inputs and bars

- source baseline: Git commit `095b0e1bc`
- exact-recovery runtime under test: Git commit `6bc95f69f` (implementation `8056061af`, scalar
  digest fix `0dcbfeac2`, canonical Python-RNG seed fix `6bc95f69f`); every commit was pushed
  before long-run execution
- warm start: private HF model
  `dancinlab/anima-store-causality-7b-staging-2026-08-10`, artifact commit
  `780558eb2f5fc19609d63fdec95cb7d9c1923429`, file
  `compose2_dual_parity_7b_s7.clm.pt`, SHA-256
  `f2148dc82957dd7dbe0701fb4de8c15d044758e8800792af1e3c80e85c489cf4`
- frozen compose-2 data: private HF dataset
  `dancinlab/anima-store-causality-compose2-2026-08-09`, commit
  `8f29c2f16f214734d9b5fa4010c57c48fff3979e`
- seed 7; 24-byte window; store batch 32; address weight 1.0; frozen trunk;
  position normalization; canonical dual parity lane 10; value centering
- exactly 2,000 additional optimizer updates from the recorded 200-step warm start
- deliberate process boundary after additional step 1,000; the second process must resume to
  additional step 2,000
- pair-oracle bar 0.90; normal and causal recovery bars 0.75; every negative control bar 0.56
- no retry, alternate seed, data regeneration, randomization change, threshold change, or
  post-result step extension is allowed

The run uses one H100/H200-class 80 GB GPU on Vast.ai. It is stopped as infrastructure failure if
the instance exceeds three hours or USD 5 before teardown; that stop does not become a model result.
Heavy work does not run on mini.

## Preflight QA

Before the 7B run, Vast.ai H100 GPU regression passed 18/18. An actual tiny canonical CLMS run was
then executed both continuously and with a process stop at step 2 followed by resume to step 4.
The two final engine `.clm` files had the same SHA-256
`bcefdd6f84930790ceddc4609e747892485c432aa02de9e28f59eb570add40b5`, and their complete resume
state digests were both
`ebd7b4be755231dbbf2cd10952f38ff36452cbce2061463574c43880cbf65d8e`.

## Recovery requirement

The existing rolling `.resume.pt` writer stores model weights only. It does not preserve optimizer
moments, completed step, global Torch RNG, CUDA RNG, or the corpus, validation, objective, store,
ideation, and sleep sampler states. Loading it therefore starts a different trajectory from step 1.
Before this run, the common `cli/train.py` checkpoint path must be upgraded to preserve and restore
those states while remaining backward-compatible with legacy state-dict `.pt` warm starts.

Recovery passes only if all of the following hold:

1. a regression test gives byte-identical final trainable tensors for uninterrupted and
   interrupted/resumed runs;
2. the actual 7B checkpoint's recorded state digest is verified when the second process loads it;
3. the restored process starts at additional step 1,001, not step 1;
4. the final engine `.clm` is decodable and its model/recovery artifacts pass SHA-256 verification.

## Evaluation order

The additional-step-1,000 checkpoint is scored on pair-oracle only, then the process is terminated.
That midpoint result is recorded but never used to change the fixed 2,000-step endpoint. After exact
resume, the additional-step-2,000 checkpoint is scored on pair-oracle first. If it is below 0.90,
the evaluator stops and no positive or negative causal arm is interpreted. Only a passing endpoint
runs the unchanged order: normal → clue A removed → clue B removed → addresses shuffled → causal
recovery. Production and chat staging remain blocked unless recovery, endpoint pair-oracle, the full
causal battery, runtime measurements, and QA all pass.

Models, resumable checkpoints, and training data are managed only in private repositories under the
`dancinlab` Hugging Face organization. Vast.ai scratch storage is deleted after verified upload; no
model or training-data copy is retained locally or in R2. `ING.jsonl` and `stream_mi.json` are
preserved.

## Measured result

The midpoint checkpoint passed pair-oracle at 128/128 = 1.0000. Its exact-resume state digest
`b200b6a47fa5dddfdf19c3ecfbac74b0f4664552bf74172d69b48af956acddf3` was verified by the new
process, which reported `completed=1000`, `next=1001`, and the unchanged endpoint 2000.

| endpoint arm | correct | accuracy | bar | pass |
|---|---:|---:|---:|:---:|
| pair-oracle | 128/128 | 1.0000000 | >= 0.90 | yes |
| normal | 107/128 | 0.8359375 | >= 0.75 | yes |
| clue A removed | 54/128 | 0.4218750 | <= 0.56 | yes |
| clue B removed | 60/128 | 0.4687500 | <= 0.56 | yes |
| addresses shuffled | 63/128 | 0.4921875 | <= 0.56 | yes |
| causal recovery | 107/128 | 0.8359375 | >= 0.75 | yes |

The unchanged evaluator returned `SUPPORTED-CAUSAL`. The final exact-resume digest is
`9c17b098006efde6e9b8c1ad58f42db5a7c3c7f352fa1b830691dfac51e908ca`.

## Runtime and artifacts

- Vast.ai instance `47378938`: NVIDIA H100 PCIe 80 GB; 7,057,657,951 parameters
- train/evaluation peak VRAM: 35,407 / 54,601 MiB
- first/second process end-to-end wall: 585.49 / 695.00 seconds
- resumed 1,000-update loop: 417.6 seconds, 2.3946 updates/s
- complete six-arm endpoint battery: 276.50 seconds, 2.7776 items/s
- GPU regression: 18/18; actual tiny uninterrupted/resumed `.clm` and state digest exact
- four checkpoint SHA-256 values and full measurements: `result.json`

Artifacts are private at `dancinlab/anima-store-causality-7b-longrun-2026-08-10`, artifact commit
`0e26f4623c514bc6192a93f14e7a466a6f8bd59a`: 24 files / 63,558,694,473 bytes. The frozen
compose-2 dataset remains pinned at its existing private HF commit. No model was copied to mini or
R2. Final Vast.ai cost was approximately USD 1.69, and active rent after teardown is zero.

This closes the long-run learning and exact checkpoint-recovery gate, but it is not production
approval. Remaining gates are 7B chat-staging integration, serving latency/throughput, HTTP and
WebSocket QA, and a serving soak/rollback test. Trainer code changed; the live chat runtime did not,
so no LaunchAgent or production chat restart is performed in this gate.
