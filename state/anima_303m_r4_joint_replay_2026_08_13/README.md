# R4 native joint broad replay + dialogue supervision — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

High-LR turn-only SFT memorized and erased broad language; one-tenth LR retained broad language and
underfit the same turns. This one-arm treatment uses only the existing trainer's canonical
multi-cell round-robin and additive answer CE. Each batch contains four broad rows receiving full
CE and four document-aligned dialogue rows receiving full CE plus assistant response CE.

The endpoint `3,750 = 1,875×8/4` preserves exactly 15,000 expected dialogue rows from the failed
high-LR arm while adding 15,000 broad replay rows. The language checkpoint, data views, model,
seed, peak LR, dialogue supervision, decoder and independent gates remain fixed. No new runtime
engine or evaluator is added. Any failure is final for this registered arm, and no result directly
authorizes 303M, IIT-mouth coupling, participant mounting or production.
