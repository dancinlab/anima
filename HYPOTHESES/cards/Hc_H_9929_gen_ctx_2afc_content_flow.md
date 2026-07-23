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

## VERDICT — 🔴 NULL (THEATER) · 303M pool fire (2026-07-23 · summer · engine-native)

`h9720_fresh3_s11.clm` (179MB, 303M-class) · `ANIMA_TICKS=200` monologue · `anima-py evaluate
--gen-ctx-2afc`. **100 emit-ticks spanning two phase classes (SUSTAIN 76 · RESONANT 24) produced
ONE byte-identical utterance** — content-invariance census = 1 distinct hash across all 100 ticks
and both classes. The daemon collapses to a fixed attractor; the shipped 2-bit phase channel — and
the whole A⇄G tension state — has ZERO effect on emitted content. Matches the toy QA at scale.

**Honest scope (verdict-integrity — corrected from a first draft that quoted the toy's numbers):**
the SCORING-side arms are window-defeated on this trace and are NOT evidence. Content is 80 bytes,
seed (phase+anchor) is 52 bytes; with the T=64 right-aligned scoring window the whole seed falls
outside the scored positions, so anchor-ablation came back **0.5000 (100/100 ties)** — not the 1.0
the toy showed — and the phase-swap 2AFC is a formal 0.5 (also O(n²)≈10h at 303M, now short-
circuited under content-invariance). The NULL rests ENTIRELY on the **generation-side** content-
invariance census: the seed WAS in-window (52<64) while the daemon generated the first ~12 content
bytes, so phase COULD have shaped them — and the content is byte-identical across SUSTAIN and
RESONANT, so it did not.

Tool hardened after the real run: SCORING-WINDOW-BLIND guard (warns when seed_len ≥ T for most
ticks), phase-swap short-circuit under content-invariance, deterministic pair cap (1500).

## Next (optional refinements, not blocking the verdict)

- To certify the SCORING-side arms in general, score the phase-reachable content PREFIX (first
  ~T−seed_len bytes) instead of the window-truncated whole.
- A varying-anchor session (percept_source) or `--pc2-mouth on` is a SEPARATE measurement — the
  one live content-side write authority (H_9575 PC2) was off here.
