# R4 aligned 100-document and independent conversation test — 2026-08-13

Status: **COMPLETED — FAIL-ALIGNED-100-MEANINGFUL-CONVERSATION**.

The runtime-compatible four-document arm passed exact conditional learning. This protocol tests
whether that repaired shared position map scales to 100 documents and independent conversation
prompts at the unchanged tiny `d=128/L=4/600-step` budget.

The training view is derived before training by scanning the immutable source in order and taking
the first 100 complete single user-assistant documents whose responses fit the canonical 192-byte
generation budget. Its SHA-256 is frozen in `protocol.json`. The existing document-aligned sampler,
deterministic two-thread CPU execution, objective, optimizer and decoder remain fixed.

The first eight training documents require teacher top-1 `>=0.80`, exact/target/structural `8/8`
and prompt causal control at least `6/8`. All 32 heldout documents are reported without checkpoint
selection. The unchanged independent conversation panel must pass its existing automatic bars;
even then manual review remains required. This run cannot authorize 303M, IIT coupling, participant
mounting or production. Vast.ai is forbidden and the user files remain untouched.

## Result

The 100-document treatment failed both the in-view and independent gates. The first eight training
probes reached teacher top-1 `0.6641`, CE `1.26965`, target/exact `0/8`, structural `3/8`, and prompt
CE control `4/8`. All 32 fixed heldout documents scored assistant-turn CE `4.13494` and top-1
`0.15734`.

The unchanged meaningful-conversation evaluator passed all scorer controls but the checkpoint
scored semantic `0/7`, structural `5/7`, and failed both multiturn finals. Outputs included
`"The an's."` and long fragmented repetitions. The verdict is
`FAIL-ALIGNED-100-MEANINGFUL-CONVERSATION`; the mouth is not meaningful and no manual promotion,
303M, IIT coupling, participant or production action is allowed.

Alignment therefore fixes the four-document position mapping but is not sufficient at 100
documents under the fixed 600-step exposure. The next separately preregistered two-arm experiment
uses 16 documents to compare 600 steps against 2,400 steps, which matches the successful
four-document arm's presentations per unique document without changing model capacity.
