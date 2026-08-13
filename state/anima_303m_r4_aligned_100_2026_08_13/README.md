# R4 aligned 100-document and independent conversation test — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

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
