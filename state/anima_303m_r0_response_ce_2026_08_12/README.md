# Anima 303M R0 response-supervision recovery — 2026-08-12

Status: **PREREGISTERED — GPU run not started**

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

No model has been promoted or deployed by this preregistration.
