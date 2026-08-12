# 303M V0/V2 micro experiment — 2026-08-12

Status: **PREREGISTERED; no result yet**.

The preceding English R0 did not fail because response supervision was silent: it failed after
the complete-document sampler and response CE were both active. The narrower shared cause is that
only 226 of 2,308 selected dialogue documents fit the 512-byte causal window; 2,082 documents were
dropped before sampling. Repeating 303M training on that support set is prohibited.

This experiment changes one data-construction axis first. It keeps the pinned human-reviewed
OpenAssistant source, eligibility, official splits, ByteGPT architecture, 512-byte block and
canonical chat format. The control is the previous one-best-path-per-root corpus. The treatment
uses every eligible human assistant turn and serializes the longest complete alternating ancestry
suffix that fits 513 bytes. It never slices a UTF-8 sequence, role prefix, prompt or response.

Only after the data gates pass, matched tiny ByteGPT arms compare V0 base CE with V2 base CE plus
the existing `answer_ce` term. The test reuses `cli/train.py`, `core/generator.py` and the existing
conversation structural checks. It does not create another trainer, decoder or evaluator.

Promotion is fail-closed. Invalid role alternation, partial turns, train/validation overlap, panel
contamination, less than 95% coverage of otherwise eligible fitting assistant turns, or any
serialized document over 513 bytes stops before GPU work. Tiny failure stops before 303M. A tiny
pass permits only a separately recorded single-seed 303M screen; it does not unlock R1 or
production. Exact conditions and stop rules are frozen in `protocol.json`.

Progress and raw results will be appended here without changing the registered thresholds.
