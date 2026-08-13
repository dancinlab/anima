# R4 fixed-data capacity ladder — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

The fixed 3,500-document exposure experiment reproduced its control and remained semantic `0/7`
after `120,000` dialogue rows. This protocol changes only the existing ByteGPT shape. It freezes
the broad and dialogue data revisions and byte views, seed, batch, two-phase objective, optimizer,
row exposure, canonical generator and fail-closed conversation panel.

The frozen `0.89M` endpoint is not rerun. New `3M`, `10M` and `30M` labels denote exact registered
models of `2,817,024`, `10,110,080` and `29,316,224` parameters. Their shapes are respectively
`d192/L6/H3`, `d320/L8/H5` and `d448/L12/H7`, preserving the native 64-dimensional attention head.
Each arm is created from scratch by the same existing Python trainer: a 2,000-step full-CE broad
language phase followed by the same 30,000-step joint broad-replay plus additive assistant-response
phase. A smaller checkpoint cannot be warm-started into a larger shape, so rebuilding the language
phase per shape is part of the capacity treatment rather than a new engine.

All three arms run regardless of intermediate results. `30M` is the fixed primary endpoint, so a
lower arm cannot be selected after seeing the outputs. Every arm records exact parameter identity,
language and retained broad CE, held-out assistant CE/top-1, training probes, raw canonical
responses, semantic/structural bars, repetition, memory and correction. An automatic panel pass
still requires manual blind review before any larger action.

This is a bounded capacity-at-fixed-exposure test. A failure does not prove a universal model-size
limit because a larger model can be more undertrained under the same row budget. A pass is evidence
for a usable language mouth, not evidence of consciousness. The interpretation remains constrained
by [`dancinlab/anima-research@03d55ef`](https://github.com/dancinlab/anima-research/commit/03d55ef9848df304a435a88a2b90a74722bc5b73).

Local work is limited to protocol, command parity and tiny smoke checks. The result-bearing ladder
may use one non-H100 Vast.ai GPU because the registered `30M` trajectory would impose unnecessary
load on the mini. All model/data artifacts must be kept only in the private HF `dancinlab`
repository, independently SHA-verified, and local copies removed afterward. The rented instance
must be destroyed after completion. `ING.jsonl` and `stream_mi.json` remain untouched.
