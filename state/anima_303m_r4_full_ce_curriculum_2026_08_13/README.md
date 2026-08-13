# R4 full-CE → aligned turn-SFT curriculum — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

The aligned 100-document response-only model now memorizes its registered training probe exactly
but scores semantic `0/7` on the unchanged independent panel. This one-arm local Python experiment
changes only the missing language-formation phase: the existing tiny ByteGPT first receives full
next-byte CE on a fixed 1 MiB view of the immutable private English-general HF corpus, then the
unchanged 100-dialogue document-aligned turn-only phase warm-starts from that fixed engine.

Both source revisions, byte ranges, derived SHA-256 values, optimizer schedules, endpoints, seed,
model, decoder, heldout dialogue view, panel and decision table are frozen in `protocol.json`.
The response-only 1,875-step result is the preserved control; there is no fresh control arm and no
post-hoc checkpoint choice. Failure at any gate remains a recorded failure. An automatic panel
pass still requires manual review and cannot directly authorize 303M, IIT coupling, participant
mounting, or production.
