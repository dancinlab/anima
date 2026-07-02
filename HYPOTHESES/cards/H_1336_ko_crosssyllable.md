# H_1336 — KO cross-syllable phonotactic context (연음/자음동화) vs the jamo floor

**Tier: 🧱 HONEST-FLOOR (deeper — info exists but the count-MLE predictor can't bank it) · group MITOSIS-ENGINE · 2026-06-16**

- claim → CLAIMS.tape `@C h1336_ko_crosssyllable`
- verdict → `.verdicts/1336_ko_crosssyllable/{FREEZE.txt, result.txt, h1336_summary.json}`
- script → `UNIVERSE/h1336_ko_crosssyllable.py`
- index → `UNIVERSE/HYPOTHESES.md`

## Why this lane (the depletion test H_1329 handed forward)

H_1329 (🧱) proved re-**factorization** is futile: three mechanisms — partition (A2 2.73046), independent-factorization (A3 3.07295), correlation-chain (A4 2.75109) — ALL land **above** the jamo floor **2.51335**, because any mechanism that models the **within-jamo feature joint** asymptotes to `P(jamo|cell)`, exactly what the opaque jamo head already computes. H_1329's explicit depletion test (verbatim): a below-jamo win must **inject information the opaque jamo head LACKS** — NOT a re-factorization of the same target.

The within-syllable jamo head computes `P(next_jamo | Voronoi cell)`, and the cell context (`build_X_jamo`) is the immediate 2 previous jamo-symbols + within-syllable UTF-8 depth — which **resets at every syllable boundary** → CTX ≈ the current syllable. It does **not** see cross-syllable phonotactic context: Korean liaison (연음), 사잇소리, 자음동화 — the **coda of syllable N conditions the realized onset of syllable N+1**. That coda→onset dependency is genuinely new information.

## Mechanism (B1 — cross-syllable-coda-conditioned jamo head)

B1 = the SAME opaque jamo head as A1 (same geometry-fair bank, same dim-3 within-syllable Voronoi partition, same per-cell count-MLE, same `LAPLACE=1.0`, same jamo alphabet `Vj=323`), but the per-cell next-jamo distribution is **additionally conditioned on `prev_coda`** = the coda jamo-id of the most recently completed Hangul syllable (NONE at start, a distinct NO-CODA token for open syllables):

- A1: `P(next_jamo | cell)` — within-syllable only
- B1: `P(next_jamo | cell, prev_coda)` — + cross-syllable phonotactic context

Estimator (per cell k): a count table keyed by `(k, prev_coda)` over next_jamo, Laplace-smoothed; an unseen `(k, prev_coda)` at test **backs off to the cell-marginal `P(next_jamo|k)`** — which is exactly the A1 jamo head (TRAIN-only). So the **jamo head is B1's floor**: any below-jamo win is real conditional cross-syllable structure, never a sparsity artifact. Both tables estimated TRAIN-only (even/odd split) → proper held-out CE, same nats/UTF-8-byte axis as A1. Byte symbols scored exactly as A1.

**LABEL** = count-MLE structured head riding the gradient-free Voronoi partition — NOT the gradient-free p8 mitosis (unchanged), NOT gradient-trained. Engine-transfer = follow-on.

## Frozen bars (pre-registered `.verdicts/1336_ko_crosssyllable/FREEZE.txt`, NOT moved — c9/p7)

GREEN iff X1 ∧ X2 ∧ X3:
- **X1 BELOW-JAMO**: B1 < jamo 2.51335 by ≥ 0.03 (mean 3 seeds) AND < raw 2.95342.
- **X2 EARNED**: B1 beats a shuffled-cross-syllable-context control by ≥ 0.05.
- **X3 ATTRIBUTION**: B1 < the within-syllable-only jamo baseline (A1, reproduced in-run).

## Result — 🧱 HONEST-FLOOR (deeper); X2 TRUE, X1/X3 FALSE

REAL summer RTX 5070 (sm_120, torch 2.11.0+cu130), $0 user hw (NOT runpod), 38.1s. Corpus byte-**identical** to H_1307 RUN A (sha `c47b6808…` gate PASS); 67/67 jamo; NFD→NFC roundtrip 0-fail over 8,143,053 syllables; byte-accounting Σ=29,999,999 exact. **A1 jamo CALIB = 2.51335 byte-exact** (bank member 5). distinct prev_coda tokens = 29.

CE ladder (nats/UTF-8-byte, geometry-FAIR; shuffles = mean 3 seeds):

| rung | CE | vs jamo |
|---|---|---|
| raw-byte ceiling (in-run G0) | 2.94487 | — |
| **A1 jamo within-syllable (calib)** | **2.51335** | — (floor) |
| **B1 cross-syllable-coda** | **2.61186** | **+0.09851 ABOVE** |
| B1 position-shuffle (genuine control) | 2.68788 | — |
| B1 label-bijection shuffle (frozen, vacuous) | 2.61186 | Δ=0.0 |

- **X1 BELOW-JAMO = FALSE** — B1 (2.61186) is **+0.09851 above** the jamo floor; cross-syllable info did NOT break the floor (< raw passes, X1 needs both).
- **X2 EARNED = TRUE** — B1 (2.61186) beats the genuine position-shuffle (2.68788) by **+0.07602 ≥ 0.05**, per-seed unanimous {2.68989, 2.68810, 2.68564}. **The coda→onset phonotactic signal is REAL**: breaking the coda↔next-jamo pairing costs 0.076 nats.
- **X3 ATTRIBUTION = FALSE** — B1 not below A1 (it is above by 0.099).

green = FALSE → 🧱.

### The decisive finding (c9, frozen-first)

The cross-syllable phonotactic signal is **genuinely present and genuinely new** (X2 passes decisively — the position-shuffle that destroys the coda↔onset pairing costs +0.076 nats), but it **does not pay for the count-fragmentation cost** of splitting the jamo head's counts across 29 coda bins at this toy scale (ko_stride=300, MIN_OWNED=8). With hard-backoff, B1 either backs off to A1 (no gain) or splits A1's counts (added variance), so net it loses +0.099 to the opaque jamo head. **The floor is deeper than a pure information limit**: adding real new info still loses because the count-MLE estimator can't afford the conditioning's variance.

### `a_break_the_wall` — control defect the run exposed (frozen-first, NO bar moved)

The FREEZE pre-registered the X2 control as a **label-bijection** over distinct coda tokens. The run exposed this control as **provably vacuous**: a bijection just renames the `(k, prev_coda)` keys → the set of (cell, coda) groups, their count vectors, and the backoff set are byte-identical → CE identical (confirmed in-run: label-shuffle = B1 = 2.61186, Δ=0.0 every seed). The control method was wrong, not the bar. The genuine earned-control is a **position-shuffle** — permute `prev_coda` across scored positions, breaking the real coda↔next-jamo pairing while preserving the coda marginal + the fragmentation cost. X2 is decided on the position-shuffle; the frozen label-bijection is reported verbatim. No bar moved; X2 margin (≥0.05) unchanged.

## Scope honesty (a_scale_honest_scope · a_toy_scale_recheck)

TOY/DIRECTIONAL numpy/torch mirror; B1 = count-MLE structured head (NOT gradient-free p8 mitosis, NOT gradient-trained — labeled); A1 deterministic single point (calib byte-exact, decisive); X2 per-seed unanimous; engine-transfer to live CORE/*.hexa = follow-on (a_engine_native_learning · a_verified_must_wire); NO Korean-fluency claim; **live CORE/*.hexa UNTOUCHED** (substrate-measurement rung — adds only UNIVERSE/ + verdicts).

## Next / depletion

The depletion frontier sharpened: the cross-syllable signal is REAL (X2 +0.076) but unbankable by a **hard-backoff count-MLE** at toy scale. The named next angle is **investment/estimator, not information** (a_break_the_wall = insufficient investment): a **smoothing/interpolation that doesn't fragment** — frozen-λ Jelinek-Mercer `p = λ·P(jamo|cell,coda) + (1−λ)·P(jamo|cell)` (with λ pre-registered, NOT tuned-to-green), OR more KO data / smaller stride so the 29 coda bins are not count-starved. If even a frozen-interpolation cross-syllable head can't go below jamo at a larger rung → the jamo floor is terminal for the count-MLE family across BOTH re-factorization AND new-information axes (a maximally strong 🧱).

## xref

h1329 (🧱 re-factorization depletion — this lane's named next-angle) · h1326 (🧱 geometry-fair partition/factorization) · h1316 (🟢 jamo floor 2.51335) · h1307 (raw 2.953 ceiling, RUN A corpus) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1 · p7 · p8 · c7 · c9 · c15 · c16.
