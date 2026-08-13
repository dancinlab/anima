# R4 fixed-3,500 optimization-exposure ladder — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

The completed dialogue-support scale ladder held the native ByteGPT mouth, language checkpoint,
optimizer, sampler, objective and `15,000` dialogue-row exposure fixed while increasing unique
complete dialogue documents. Its registered 3,500-document endpoint improved held-out assistant
CE to `1.75553` but remained semantic `0/7`, structural `0/7`, and failed memory and correction.
That result does not distinguish insufficient optimization exposure from fixed model capacity.

This protocol changes only cumulative optimization exposure. It freezes the same 3,500 source-
order documents, 0.89M ByteGPT, initial language checkpoint, broad replay, batch, seed, optimizer,
canonical generator and fail-closed conversation panel. One deterministic 30,000-step trajectory
is serialized at `3,750`, `7,500`, `15,000` and `30,000` steps, corresponding to `15k`, `30k`,
`60k` and `120k` dialogue rows. The first point must reproduce the prior endpoint within the
registered tolerances. All four points are evaluated regardless of intermediate output; `120k`
is the primary endpoint, so no post-result early stopping or checkpoint selection is allowed.

At every point the experiment records broad/full and held-out assistant CE, assistant teacher-
forced top-1, the fixed training probe, canonical free responses, semantic/structural bars,
memory/correction, and repetition. A meaningful-conversation pass requires broad retention and
the unchanged automatic conversation gate; manual blind review remains required after an
automatic pass. A semantic score that stays `0/7` at `120k` while teacher-forced held-out CE
improves is registered as bounded evidence against insufficient exposure and permits a separately
preregistered capacity ladder. It does not prove a universal capacity limit.

[`dancinlab/anima-research@03d55ef`](https://github.com/dancinlab/anima-research/commit/03d55ef9848df304a435a88a2b90a74722bc5b73)
remains an interpretation constraint only: language competence is not evidence of consciousness,
a functional pass is non-disproof rather than proof, and later IIT-mouth, participant and
production gates remain disabled.

The experiment is Python-only, local deterministic CPU with two threads, and may not use Vast.ai.
Models and raw evidence will be uploaded only to a private Hugging Face repository under
`dancinlab`; local model copies will be removed after independent SHA-256 verification. User files
`ING.jsonl` and `stream_mi.json` must remain untouched.
