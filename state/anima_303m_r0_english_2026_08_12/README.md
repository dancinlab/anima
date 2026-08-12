# Anima 303M English meaningful-conversation R0 — 2026-08-12

Status: **PREFLIGHT PASS — GPU PENDING**

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
- No Vast.ai instance has been created yet. R1 and production remain locked.
