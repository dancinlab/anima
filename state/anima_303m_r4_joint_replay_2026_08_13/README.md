# R4 native joint broad replay + dialogue supervision — 2026-08-13

Status: **COMPLETE — FAIL-JOINT-MEANINGFUL-CONVERSATION**.

High-LR turn-only SFT memorized and erased broad language; one-tenth LR retained broad language and
underfit the same turns. This one-arm treatment uses only the existing trainer's canonical
multi-cell round-robin and additive answer CE. Each batch contains four broad rows receiving full
CE and four document-aligned dialogue rows receiving full CE plus assistant response CE.

The endpoint `3,750 = 1,875×8/4` preserves exactly 15,000 expected dialogue rows from the failed
high-LR arm while adding 15,000 broad replay rows. The language checkpoint, data views, model,
seed, peak LR, dialogue supervision, decoder and independent gates remain fixed. No new runtime
engine or evaluator is added. Any failure is final for this registered arm, and no result directly
authorizes 303M, IIT-mouth coupling, participant mounting or production.

The joint arm passed both mechanical sides: fixed broad CE `2.06204`, top-1 `0.40096`, and the
dialogue training probe reached teacher top-1 `1.0000`, exact/target/structural/prompt controls
`8/8`. Independent output became structurally complete (`7/7`) but remained semantically wrong
(`0/7`); heldout dialogue assistant CE was `5.00458`, and memory/correction both failed. The
verdict is therefore `FAIL-JOINT-MEANINGFUL-CONVERSATION`.

The measured command passed `--cell-label` twice even though argparse defines one `nargs=*`
argument. Raw telemetry consequently calls the 1 MiB broad cell `dialogue` and the 18.3 KiB
dialogue cell `cell1`. File order, hashes, 15,000/15,000 windows, chat-frame detection and loss are
unaffected, so the scientific verdict remains valid; the harness now uses the canonical single
`--cell-label broad dialogue` call and its regression asserts that exact argv shape.

Joint replay closes the bounded optimizer/sampler explanation but does not create generalization
from 100 dialogues in a 0.89M model. The next result-bearing axis must be a separately
preregistered dialogue-support scale test; changing model capacity at the same time is forbidden.
