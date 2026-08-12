# 303M V1 context-length micro experiment — 2026-08-12

Status: **COMPLETED — FAIL-V1-CONTEXT-MICRO**.

R3 proves that the IIT daemon's final state can select one of two exact bounded utterances. It is
not a learned mouth. R4 therefore remains blocked on an independently trained model that can hold
meaningful English conversation before any IIT state is allowed to affect free generation.

The immediately preceding V0/V2 micro run found that the existing trainer, serializer and
canonical generator can exactly learn one complete exchange, but both matched tiny arms collapse
on 100 exchanges. It also measured that 15,114 of 24,239 valid OpenAssistant targets cannot fit
their final complete prompt/response pair in 513 bytes. A further 303M run at the same block length
is prohibited.

V1 changes only causal context length. The fixed source, eligibility, official split, canonical
chat format, greedy decode, optimizer family, seed and total target-byte budget are unchanged.
The source census is performed at 513, 1025 and 2049 serialized bytes. Exact documents are
deduplicated, SHA-ordered, panel-decontaminated and checked for split overlap before training.

The matched short-view comparison trains the same existing ByteGPT configuration on the same 100
documents at block 512 and block 2048. Batch sizes 8 and 2 keep 4,096 target bytes per step. A third
2048 arm uses 100 preregistered long documents that cannot enter the 512 arm. No new trainer,
decoder or evaluator is introduced; training runs through `cli/train.py`, generation through
`core.generator`, and structural scoring through the existing conversation evaluator.

Promotion is fail-closed. The 2048 census must preserve at least 90% of valid targets. The short
2048 arm must outperform the 512 control and recover at least six of eight registered response
prefixes; the long arm must meet the same 6/8 recovery bar. Every arm must descend on held-out CE,
and both 2048 arms must emit at least six distinct, non-empty, structurally valid replies. Failure
forbids a 303M run, IIT-mouth coupling and production deployment. Exact hashes, bars and stop rules
are frozen in `protocol.json`; results will be appended without changing them.

## Result

The context census and every data-integrity gate passed. Complete final prompt/response coverage
was `9,125/24,239` at 513 bytes, `15,421/24,239` at 1025 and `22,139/24,239` (`91.34%`) at
2049. The SHA-ordered private views are fixed at HF dataset revision
`dancinlab/anima-303m-v1-context-micro-2026-08-12@5d82d887b58f4d13c4f0e32f5ee9d15a2b46987b`.

All three matched arms completed 1,200 steps on a Vast.ai RTX 3090 without H100. Held-out CE
descended in every arm, but the registered generation gates failed:

- `V0_short_512`: final held-out CE `4.55867`, non-empty/distinct `8/8`, structural `4/8`,
  target-prefix recovery `3/8`.
- `V1_short_2048`: final held-out CE `2.91105`, non-empty/distinct `8/8`, structural `0/8`,
  target-prefix recovery `0/8`.
- `V1_long_2048`: final held-out CE `2.55302`, non-empty/distinct `8/8`, structural `0/8`,
  target-prefix recovery `0/8`.

The 2048 arms reduced held-out CE and admitted far more human dialogue, yet collapsed into loops
such as `an an an...`, `the the the...` and `ic ic ic...`. Context length is therefore a real
support-set bottleneck but not the sole cause of meaningless generation. The registered verdict is
`FAIL-V1-CONTEXT-MICRO`; 303M training, IIT state coupling, participant mounting and production
remain blocked.

Python QA passed locally at `93 passed` with the expected unavailable CUDA/CuPy case skipped. Vast
QA passed `92` tests before CuPy installation and `7/7` CUDA-focused tests after installation. That
last check exposed a shared runtime defect: `core.cuda_paths` found split pip CUDA directories but
preloaded only the first, leaving `libnvrtc` unresolved and silently forcing CPU decode. The shared
loader now searches every canonical candidate directory and has a split-wheel regression. This QA
fix does not change the failed model verdict.

The three checkpoints, summaries, logs and lossless raw replies are preserved in private HF model
revision `dancinlab/anima-303m-v1-context-micro-2026-08-12@c2b8939a4baba95ce99ecafa83197a22fa2c242a`
(16 files, 251,477,746 bytes). No model is deployed. The next allowed work is a separately
preregistered single-axis mouth/data-objective micro diagnosis; increasing context or training a
303M model again is not authorized by this result.
