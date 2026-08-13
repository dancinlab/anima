# R4 aligned 100-document exposure match — 2026-08-13

Status: **COMPLETE — FAIL-ALIGNED-100-MEANINGFUL-CONVERSATION**.

Aligned 64 documents fail at 600 steps and pass at 1,200, establishing an exposure boundary. This
one-arm test derives its 100-document endpoint from the passing 32-document reference:
`600 / 32 × 100 = 1,875` steps. The derivation is frozen before training.

The same immutable 100-document view, aligned sampler, tiny model, objective, optimizer,
deterministic CPU path, canonical decoder, 32 heldout documents and independent meaningful-
conversation panel are retained. Automatic conversation pass still requires manual review and no
result directly authorizes 303M, IIT coupling, participant mounting or production.

The fixed 1,875-step run fully learned the registered 100-document training support: the first
eight probe documents reached teacher-forced top-1 `1.0000`, CE `0.001315`, and exact/target/
structural/prompt-control `8/8`. This closes document alignment and per-document exposure as the
remaining explanation for in-view failure.

It did not generalize. The fixed heldout view scored assistant-byte top-1 `0.1370` and CE
`8.0896`, worse than the 600-step run, while the unchanged conversation panel remained semantic
`0/7` with structural `6/7`; memory and correction both failed. Outputs were grammatical-looking
byte fragments rather than relevant answers. The result therefore separates successful
memorization from failed language generalization and supports response-only overfit on the tiny
100-document support. It does not authorize post-hoc endpoint selection, 303M training, IIT-mouth
coupling, participant mounting, or production. The next single-axis test must start from a
separately preregistered broad full-CE language phase and retain the aligned turn-SFT phase and
independent panel unchanged.
