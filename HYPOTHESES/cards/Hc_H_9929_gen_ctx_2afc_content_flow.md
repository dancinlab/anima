# H_9929 · gen-ctx-2AFC — does the A⇄G phase VALUE causally shape content, or is it theater?

**group** engine-clm-flow · **date** 2026-07-23 · **tier** instrument · **status** MEASURING · **verdict** PENDING

## Question

H_9392 (re-censused 2026-07-23, #4453/#4454) narrowed the shipped engine→CLM channel to **one
string, `phase` ∈ {DORMANT,FLICKER,SUSTAIN,RESONANT} = 2 bits/tick**, prepended to the decode
seed. Write-back is 0 (sha256), and Φ never enters a forward pass. That leaves ONE open question:
are those 2 bits **causal** (the phase value shapes the emitted content = FLOW) or **theater**
(any string of that shape would do; the anchor alone determines content = NULL)?

## Instrument (engine-native · $0 · a_eval_py_canonical)

```
anima-py evaluate <clm> --gen-ctx-2afc <trace.jsonl> [--out f.json] [--win 64]
```

Reads a live `ANIMA_DECISION_TRACE` (from `anima-py chat` — no chat change; the trace already
records, per emit tick, `seed_b64 = "<PHASE> <anchor>"` and `gtext_b64` = the emitted bytes).
The whole discriminator is a **re-scoring on the frozen trunk** with the engine's own CE
(`_gen_ctx_cont_nll`, a surrogate-safe twin of `_xbind_cont_nll`) — no new forward-pass semantics.

**Why PAIR-2AFC, not byte-divergence** (Fable design, reconciled): a byte-LM changes its
continuation whenever the prefix changes, so Δ(live↔clamp)>0 is guaranteed and uninformative.
"Flow" must mean the substrate treats the phase VALUE as information about *this* tick's content.
content_i was argmax-generated under (phase_i + anchor_i); so if phase carries information,
`CE(content_i | phase_i + anchor_i)` should beat `CE(content_i | phase_j + anchor_i)` for a
different phase_j (anchor held fixed). Fraction of ticks the true phase wins = the 2AFC score;
under an inert phase the two CEs are equal (tie ⇒ 0.5), so chance is **derived from the realized
tie rate**, never assumed.

- **PRIMARY** phase-swap 2AFC — the value test.
- **POSITIVE CONTROL** anchor-swap 2AFC — the anchor is the known-causal seed half (content is
  grounded in / often copies it); blind here ⇒ INSTRUMENT-DEAD, no phase read.
- **SECONDARY** carrier (phase vs length-matched neutral token) — robustness, reported not gating.
- **PEDESTAL G-P0** deterministic re-score must be byte-identical (drift ⇒ INVALID).
- Provenance: trace's `ckpt_sha256` must match the passed ckpt (else INVALID-PROVENANCE).

**Prereg decision table** (margin m = one-sided binomial bound at N; covers below-chance):

| gate | read | verdict |
|---|---|---|
| G-P0 | true-rescore not byte-identical | INVALID |
| G-P1 | anchor 2AFC ≤ chance+m | INSTRUMENT-DEAD |
| deg | < 2 phase classes in the trace | UNDECIDABLE |
| G-F1 | phase 2AFC > chance+m | **FLOW** |
| G-F3 | phase 2AFC within ±m of chance | **NULL** (theater) |
| G-F4 | phase 2AFC < chance−m | BELOW-CHANCE (INVALID, audit) |

Sol dissent (recorded, not taken): score by Δ(quality-panel) with ±0.02 prereg + bootstrap CI.
Rejected — no predeclared quality panel exists for free monologue; the engine's own CE is the
more native, tie-honest DV.

## QA (toy.clm · venv install · this session)

- **bug found+fixed**: daemon content carries raw model bytes (utf-8 surrogateescape); the shared
  `_xbind_cont_nll` uses strict `cont.encode()` and crashed. Fixed with a local surrogate-safe CE
  helper (shared primitive untouched · clean-ASCII scores byte-identical, so G-P0 preserved).
- degenerate toy (1 phase, 1 anchor) → **UNDECIDABLE** (guard).
- contrast trace (2 phases × 2 anchors, content = anchor fact) → G-P0 PASS · positive-control
  anchor-swap 2AFC = **1.0000** (proves the >chance+m FLOW branch fires) · phase-swap 2AFC =
  **0.5000 NULL** (toy phase inert given the anchor = honest) · per-class split · JSON out.
- content unrelated to both seed halves → **INSTRUMENT-DEAD** (correctly refuses to read).
- provenance mismatch → **INVALID-PROVENANCE**.
- Every prereg gate exercised; instrument certified (store-mix bar: no-op byte-identical + guard
  proven able to fail + live control arm).

## Next

Pool (summer) · a real 303M `.clm` + a long chat session with `ANIMA_DECISION_TRACE` (so phase
actually varies) → `--gen-ctx-2afc`. If the real session's phase is near-constant, the honest
outcome is UNDECIDABLE (the 2-bit channel is <2 bits in practice) — itself a finding.
