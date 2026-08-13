# R4 low-LR turn-SFT — 2026-08-13

Status: **COMPLETE — FAIL-LOW-LR-TURN-SFT**.

The full-CE language phase passed broad heldout CE, but the `1e-3` turn phase changed it from
`2.25960` to `7.11936` while still scoring independent semantics `0/7`. This one-arm treatment
reuses the exact fixed language engine and changes only turn peak LR to the canonical one-tenth
transfer ratio `1e-4`. The 1,875-step endpoint, fresh optimizer, data, objective, alignment, seed,
decoder and gates remain unchanged.

Retention is fail-closed at the natural uniform CE ceiling, not a result-tuned tolerance. A pass
still requires the unchanged conversation panel and later manual review; no result directly
authorizes 303M, IIT-mouth coupling, participant mounting or production.

The one-tenth LR preserved broad language below the frozen uniform ceiling: fixed CE `3.09264`,
top-1 `0.26881`. It did not learn the turn task sufficiently. The training probe reached only
teacher top-1 `0.60305`, exact/target `0/8`, structural `5/8`, although prompt controls remained
`8/8`. Heldout dialogue assistant CE improved to `3.17190`, but independent semantics remained
`0/7`, structural `3/7`, with memory and correction failures.

This falsifies LR reduction alone: high LR adapts and forgets, while low LR retains and
under-adapts. The next separately preregistered single conceptual axis uses the existing native
two-cell round-robin with additive CE so broad full-CE replay and dialogue response supervision
coexist in every step. It does not add an engine or evaluator.
