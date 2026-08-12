# Anima 303M English meaningful-conversation R0 — 2026-08-12

Status: **COMPLETED — FAIL-MEANINGLESS-IRRELEVANT**

The user accepted English-only capability for the next screen. This removes the unavailable
Korean provenance requirement from the claimed scope; it does not reinterpret the earlier
bilingual failures or lower a passing bar.

`protocol.json` freezes a Python-only, from-scratch 303M ByteGPT run before GPU execution. It
reuses the existing private immutable HF English general and human-reviewed OpenAssistant cells,
the existing proportional sampler, response CE, canonical complete-document chat sampling, and
the shared generator/evaluator path. The source revision, seed 7, 14,000-step endpoint, optimizer,
greedy decode, and `6/7` per-language semantic bar remain fixed.

The new panel is exactly the prior seven English responses, with the same structure, memory,
correction, duplicate, and manual-review requirements. Additional preregistered scorer controls
reject contradiction, keyword salad, stale correction, meaningless repetition, and accept known
good memory/correction replies. Its SHA-256 is
`cf1a6d6837a69031929168b2b02aaf771406e0d8429bb8912b65f0be2ccbad4a`.

Before renting a GPU, local Python regression, panel controls, HF privacy/revision/file hashes,
and a tiny end-to-end root-flow run must pass. Any failure blocks the rental. A trained model that
fails automatic or seven-response manual meaning review is uploaded as failed evidence, receives
no extra seed or tuning, and does not unlock R1 or production. The Vast.ai instance must be
deleted after verified HF custody.

## Preflight result

- Focused Python engine, trainer, evaluator, exact-load, and participant QA passed `54 tests + 3
  subtests` with two CPU threads.
- The canonical tiny train/serialize/evaluate route and all seven scorer controls passed.
- The private HF revision and all four selected English train/validation files matched the pinned
  revision, sizes, and SHA-256 values (`64,861,642` bytes total).
- Vast.ai RTX 4090 QA passed `56 tests + 3 subtests` with one registered environment skip; the
  installed CUDA decode path then passed `3/3`.

## Fixed run result

The fixed seed-7 run completed all 14,000 steps in `5,699.2s`. Peak VRAM was `19,723MiB`; sampled
GPU power implies about `0.656kWh`. Train CE fell `5.66173 → 1.20952`, and both held-out cells
descended, but terminal validation remained much worse for dialogue (`2.00281`) than general text
(`1.26341`). The framed sampler fired for all `31,259` selected dialogue windows, and response CE
was active on `12,560/14,000` steps over `7,691,001` response positions, so the treatment was not
a silent no-op.

All seven preregistered scorer controls passed before the checkpoint was read. The real checkpoint
then failed automatic English conversation: semantic relevance `0/7`, structural `3/7`, and both
multi-turn finals failed. Manual review also failed `0/7`. The consciousness reply was a damaged
generic offer, the exam reply was an unrelated real-time-information disclaimer, and neither the
red-key memory nor purple correction was recovered. Raw lossless replies are in
`conversation_result.json`; item-level review is in `manual_review.json`.

No extra seed, step extension, decode/bar change, R1 work, or runtime deployment was performed.
The failed model, exact-resume state, intermediate recovery checkpoints, telemetry, and evaluation
evidence are retained privately at HF
`dancinlab/anima-303m-r0-english-seed7-2026-08-12@efdaf53c92e9e16cff6b0eb00cc94d0b88a97d33`.
All 27 files (`15,778,608,955` bytes) are present; HF reports SHA-256 metadata for all nine LFS
objects, and the final model plus both exact-resume artifacts were directly matched to their source
hashes before teardown. Vast.ai instance `47529789` was deleted, leaving zero active rentals at an
estimated `$0.7114`. R1 and production remain locked.
