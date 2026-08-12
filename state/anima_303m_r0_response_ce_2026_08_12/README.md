# Anima 303M R0 response-supervision recovery — 2026-08-12

Status: **COMPLETED — FAIL-MEANINGLESS-REPETITION**

The proportional seed-7 run improved held-out macro CE to `0.95471` but still produced phrase
loops, irrelevant answers, damaged bytes, and stale corrections. The fixed conversation gate
failed English semantic relevance `2/7`, Korean `0/7`, structural checks `0/14`, and manual review
`0/14`. R1 and production therefore remain locked.

## Shared-flow cause and change

The trainer samples random 512-byte windows and applies ordinary next-byte CE to every byte. A
streaming audit of the immutable parent corpus found that `59.48%` of sampled English dialogue
windows and `47.70%` of Korean dialogue windows contained assistant payload without its assistant
role marker. Only `39.11%` and `51.92%`, respectively, contained the marker needed to establish
the prompt-to-response boundary. The full run also exposed only `229,376,000` target bytes to a
`303,097,856`-parameter model. This does not prove either factor is sufficient, but it explains
why decreasing aggregate CE did not certify question-conditioned answers.

The treatment extends the trainer's existing `answer_ce` path rather than adding a new trainer or
evaluator. `--answer-ce-marker "assistant: " --answer-ce-all-spans` supervises each canonical
assistant response present in a window. The legacy arrow-corpus behavior remains the default.
The bf16 and fp32 branches share the marker and span logic, and exact-resume binds the response
objective into its recipe. Checkpoints and summaries retain the actual active steps, selected
positions, and response CE so a silent no-op cannot be mistaken for a treatment.

## Frozen comparison

`protocol.json` is the SSOT. Data repository and revision, seed 7, 14,000-step endpoint,
architecture, proportional sampler, optimizer, LR schedule, validation, checkpoint selection,
greedy decode, fixed panel SHA, and all conversation bars remain identical to the parent. The
only treatment is one normalized response CE term with fixed weight `1.0`; no weight sweep or
post-result extension is allowed.

The run order is Python regression and telemetry, fixed training, then the unchanged meaningful
conversation gate. A gate failure ends interpretation, preserves all raw responses privately on
HF `dancinlab`, and leaves R1 and production blocked. H100 is forbidden; the Vast.ai instance must
be removed after artifacts are verified.

## Local preregistration QA

- Chat span masks select every assistant payload while excluding user text and stop at newlines.
- The legacy answer mask still selects only the final arrow-line answer.
- Gradient support is restricted to exactly the selected response bytes.
- A canonical tiny `anima-py train` run wrote complete, nonzero response-objective telemetry.
- Focused trainer, validation, exact-resume, conversation scorer, and import regressions passed
  `28 tests + 3 subtests`.

## Vast.ai execution and result

The immutable comparison ran on one Vast.ai RTX 4090 24 GB. H100 was not used. Remote Python
regression passed `31 tests + 3 subtests`, including CUDA decode parity. All eight downloaded HF
train/validation files matched their registered SHA-256 values.

Training completed all 14,000 fixed steps in `6,005.1s` with peak observed VRAM `19,718MiB`.
The response objective was active on `13,475/14,000` steps, selected `11,025,460` target positions,
and recorded mean response CE `1.22175`; this proves the treatment was not a silent no-op. All four
held-out cells descended. Final macro validation CE was `1.16413`: English general `1.35949`,
Korean general `1.23561`, English dialogue `1.16245`, and Korean dialogue `0.89897`.

The unchanged conversation gate nevertheless failed decisively:

- English semantic `0/7`, Korean semantic `0/7`.
- English structural `0/7`, Korean structural `0/7`.
- All 14 continuations were incomplete; all seven English and four Korean responses failed the
  repetition check, while three Korean responses also ended with invalid UTF-8.
- Memory and correction failed in both languages. The corrected Korean drink remained coffee.
- Manual meaningful/relevant review failed `0/14`.

Representative raw outputs include `The sunlight is a sunlight in sunlight...`, `The process of
the process...`, `의식이란 의식이란...`, and `실용적인 방법은 실용적인 방법...`.
Response-only CE strengthened a real conditioning signal but did not solve the shared language
mouth's undertraining and long-form repetition under the fixed 229.38M-byte budget. Therefore
this result falsifies the registered treatment, not 303M capacity in general. No added seed,
loss-weight sweep, R1 workspace work, or production deployment was run.

The failed model, exact-resume state, intermediate checkpoints, training telemetry, and lossless
raw replies are retained in the private HF `dancinlab` model repository registered by
`protocol.json`. `result.json` records file hashes and the immutable revision.
