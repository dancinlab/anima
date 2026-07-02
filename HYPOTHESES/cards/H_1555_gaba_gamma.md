---
id: H_1555
slug: 1555_gaba_gamma
title: GABA × CLS — GAMMA-OSCILLATION temporal-binding (adaptive bin-width) — the LAST orthogonal GABA mechanism-family; closes the GABA census
group: brain-structure-ladder (GABA mechanism-family census · gamma temporal-segmentation · c15 missing-structure)
terminal_tier: 🟠 KNOB — DIRECTIONAL (numpy mirror; engine-native §GabaGamma R2 deferred ING)
verdict_dir: state/verdicts/1555_gaba_gamma/
terminal_verdict: state/verdicts/1555_gaba_gamma/H_1555_R1.json
date: 2026-06-21
wired: DIRECTIONAL-mirror (numpy; engine §GabaGamma R2 deferred ING h1555-r2-engine-native)
---

# H_1555 — GABA × CLS: GAMMA-OSCILLATION temporal-binding (🟠 KNOB, DIRECTIONAL)

## The lens (a_no_llm_frame_trap · a_break_the_wall MULTI-LENS) — LAST orthogonal GABA family

Census H_1553 RANK 2 — the **LAST untested orthogonal GABA mechanism-family**. After this
the GABA frontier has a full mechanism-family census:
- **sparse-coding** — H_1546 separation INERT · H_1551 capacity STATIC · H_1552 non-stationary
  STATIC (all 🧱).
- **disinhibition-routing** — H_1554 🟠 KNOB (best-fixed-gate absorbed it).
- **gamma temporal-segmentation** — THIS lens (R2). Census R3 divisive-norm (🧱 argmax-invariant)
  and R4 E/I-setpoint (🧱 single-target monotone) are SKIP per their priors.

**Biology.** PV-basket-cell GABAergic feedback generates a ~40 Hz gamma rhythm that chops
continuous input into discrete TIME-BINS: features arriving in the SAME gamma cycle bind into
ONE memory item, features in SUCCESSIVE cycles stay SEPARATE (Lisman & Jensen 2013 *Neuron*
77:1002 "The Theta-Gamma Neural Code"; Buzsáki & Wang 2012 *Annu Rev Neurosci* 35:203). This is
a TEMPORAL-SEGMENTATION lever — it decides *which features count as simultaneous* (one item) vs
*span two items* — orthogonal to representational density (sparse), write-port routing
(disinhibition), score rescale (divnorm), and E/I setpoint. **Adaptive bin-WIDTH** (gamma
frequency tracking input rate) has a regime-shifting optimum: fast input → narrow bins; slow →
wide bins. A FIXED width over-merges the fast regime OR over-fragments the slow regime.

## Capability / falsifier (boundary-free co-occurrence grouping — NE-deconfound load-bearing)

A boundary-free continuous STREAM of feature EVENTS with inter-arrival GAPs. Ground-truth ITEMS
are groups of features whose within-item gaps are SMALL (co-occur); successive items separated by
a LARGER gap (1:4 within:between, SAME separability both regimes). **NO abrupt context boundaries**
— the whole stream is one continuous context; the only cue is co-occurrence TIMING. METRIC =
item-binding F1 (a recovered group matches a truth item iff their feature-SETS are identical).

**RATE SWEEP** (the regime-shift test): FAST regime (within_gap=1.0, compressed) vs SLOW
(within_gap=8.0, stretched) × seeds [11,22,33]. The 1:4 ratio is identical → only the ABSOLUTE
scale shifts, so a fixed bin tuned to one regime should fail the other; the adaptive bin should
track both. Frozen ADAPT_K=0.5 (width = ADAPT_K × running median-gap EMA), EMA_ALPHA=0.30,
MARGIN=0.10. LR*=0.20, TH*=0.30 (engine VAdaptField constants), ABSTAIN=0.45.

**ARMS** (identical fixture per (regime,seed); gap timestamps are the cue):
- **GAMMA-ADAPTIVE** — bin-width tracks the running inter-arrival gap (ADAPT_K × median-gap EMA);
  a new bin opens when the next gap exceeds the current adaptive width.
- **NO-BINNING** — H_1532 default: each feature a singleton (no grouping) = wall baseline.
- **BEST-FIXED-BINWIDTH** — a single CONSTANT bin-width, grid-tuned over the WHOLE rate sweep on
  DISJOINT tune seed 7 (the honest strong baseline; if one width wins BOTH regimes, gamma INERT).
- **ABL (const-bin)** — adaptive signal frozen to a constant → MUST revert to fixed-bin.
- **SHUFFLE** — inter-arrival GAP cue permuted → MUST collapse (true timing, not bin count).
- **NE-FROZEN-DECONFOUND** — NE-flush (H_1544 🟢) held ON. **CRITICAL, census-flagged:** NE-flush
  is a FIXED boundary detector (no tempo tracking); on a boundary-free GROUPING stream it cannot
  adaptively track the rate. Gamma's lift MUST survive (gamma − ne_frozen ≥ MARGIN) → proves
  boundary-free GROUPING ≠ NE segmentation. If it ties NE → gamma is NE re-skinned → 🧱-redundant.

## Result (R1 numpy DIRECTIONAL, mean 3 seeds [11,22,33], $0 CPU, p7, deterministic ×2)

`state/1555_gaba_gamma/h1555_gaba_gamma.py` · `H_1555_R1.json`. Grid-tuned fixed_bin* = 2.479.

| arm | item-F1 (mean) | fast | slow |
|---|---|---|---|
| BEST-FIXED-BINWIDTH | **0.5821** | 1.0000 | 0.1641 |
| **GAMMA-ADAPTIVE** | 0.4705 | 0.4705 | 0.4705 |
| NE-FROZEN-DECONFOUND | 0.2952 | — | — |
| NO-BINNING | 0.1641 | 0.1538 | 0.1641 |
| SHUFFLE (permuted gap) | 0.1506 | — | — |
| ABL (const-bin) | 0.5821 | 1.0000 | 0.1641 |

Key deltas: adaptive − fixed = **−0.1116** (best-fixed BEATS adaptive on the rate-mean) ·
adaptive − no_binning = **+0.3064** · adaptive − shuffle = **+0.3199** · adaptive − ne_frozen =
**+0.1753** · ½(adaptive − worst_fixed) = 0.1532.

**FROZEN BARS (MARGIN=0.10, `H_1555_FREEZE.txt` pre-registered — NOT moved, c9):**
- **(A PRESENCE+SHIFT)** earned-shift `(adp−fix) ≥ ½(adp−worst_fixed)` → **−0.1116 ≥ 0.1532 FAIL**
  (best-fixed beats adaptive) → PRESENCE **FAIL**.
- **(B DISTINCT)** no_binning 0.1641 < adp−0.10 AND best-fixed loses ≥0.10 in the SLOW regime
  (fixed_slow 0.1641 < adp_slow 0.4705 − 0.10) → **PASS** (gamma IS distinct from no-binning, and a
  fixed bin genuinely cannot win both regimes).
- **(C ABL→fixed)** abl 0.5821 ≤ fixed 0.5821 + 0.10 → **PASS** (adaptive-OFF reverts to fixed).
- **(D SHUFFLE→collapse)** adp − shuffle = +0.3199 ≥ 0.10 → **PASS** (true co-occurrence timing).
- **(E NE-DECONFOUND)** adp − ne_frozen = +0.1753 ≥ 0.10 → **PASS** → **gamma is DISTINCT from NE**
  (boundary-free grouping survives NE-flush-frozen; NE's fixed boundary detector cannot track tempo).

→ B ∧ C ∧ D ∧ E hold, but **A (earned-shift) FAILS** → **🟠 KNOB**.

## Verdict: 🟠 KNOB — gamma is a REAL, NE-DISTINCT segmentation lever, but a fixed bin captures more

Gamma temporal-binding is **NOT inert** (it beats no-binning by +0.31, shuffle collapses it, ABL
reverts it) and it is **genuinely DISTINCT from NE-flush** (+0.1753 over NE-frozen — the
census-flagged near-overlap is REFUTED: boundary-free co-occurrence grouping is a capability NE's
fixed boundary detector does not have). **But the frozen adaptive tracker does not earn its keep
over a grid-tuned fixed bin** — best-fixed-binwidth (tuned to the FAST regime) scores 1.0 on FAST
and 0.16 on SLOW for a rate-mean of 0.58, BEATING the adaptive arm's flat 0.47 by 0.11. The
adaptive width is correctly SCALE-INVARIANT (identical 0.4705 in both regimes — the adaptivity
*works* in the sense that it does not collapse when the tempo shifts) but its absolute accuracy
is mediocre because the frozen ADAPT_K=0.5 mis-scales the bin relative to within-item gaps
(width pulled toward a middling value by the EMA averaging within+between gaps), so it
mis-segments in BOTH regimes rather than tracking the within-item tempo cleanly.

**This is the honest census-predicted outcome (prior 🟠).** Re-scaling ADAPT_K post-hoc to make
adaptive win would be **tune-to-green (c9) — NOT done**; the bar was frozen before the run. The
honest read: on this fixture, the regime-shift is real (a fixed bin provably cannot win both
regimes, bar B) but the SPECIFIC frozen adaptive rule does not exploit it better than a single
fixed operating point → KNOB, like H_1554 disinhibition and the 5-HT/H_1534 budget. A cleaner
adaptive rule (e.g. tracking the within-item gap mode, not the all-gap median) might earn GREEN,
but that is a NEW frozen-first round, not a retune of this one.

## GABA CENSUS CLOSED — multi-family verdict (honest endpoint)

With gamma measured, the GABA mechanism-family census is COMPLETE and the multi-family verdict
is honest (per `a_break_the_wall` §3 MULTI-LENS + fleet-full §6):

| GABA family | lever | tier | why |
|---|---|---|---|
| sparse-coding (separation) | code geometry k-of-N | 🧱 H_1546 INERT | density monotone, fixed-k captures |
| sparse-coding (capacity) | #cells | 🧱 H_1551 STATIC | capacity monotone, fixed-k=0.364 captures 14.6× |
| sparse-coding (non-stationary) | load-varying sparseness | 🧱 H_1552 STATIC | best-fixed captures |
| disinhibition-routing | write-port context gate | 🟠 H_1554 KNOB | best-fixed-gate absorbs |
| gamma temporal-segmentation | adaptive bin-width | 🟠 H_1555 KNOB | best-fixed-binwidth beats adaptive |
| divisive-norm | score rescale | 🧱 SKIP (R3) | argmax-invariant on WTA |
| E/I-setpoint | homeostatic target | 🧱 SKIP (R4) | single-target = monotone |

**GABA is now MULTI-FAMILY-CONFIRMED as a STRUCTURAL/KNOB substrate lever, NOT an adaptive
faculty** the way the 5 GREEN NTs (ACh mode-switch, DA replay-priority, NE boundary-flush,
orexin true-timing, 5-HT noise-rejection) are. Every GABA family either RE-tests the static-
architecture wall (sparse ×3, divnorm, E/I) or lands KNOB (disinhibition, gamma): the inhibitory
benefit is captured by a single fixed operating point, never by an adaptive *schedule*. The
fusion law (a modulator turns 🟢 iff its adaptive signal is load-bearing = optimal operating
point SHIFTS so no fixed setting captures it) is NOT satisfied by any GABA family — GABA's
benefits are real but STATIC/KNOB, distinguishing inhibition from the dynamic neuromodulators.
This is the honest endpoint either way.

## GUARDS / SCOPE
- **a_engine_native_learning HARD-GATE-1:** `grep -lE 'import torch|gauge_lib|numpy'
  state/1555_gaba_gamma/*.py` is **NON-EMPTY** (numpy mirror) → verdict is **DIRECTIONAL**, NOT
  terminal. Engine-native §GabaGamma R2 = obligatory follow-on ING `h1555-r2-engine-native`: live
  `core/engine_cli.hexa` §MultiStore (H_1532 lane) + a gamma bin-segmentation op, byte-exact
  re-measure of the 6 arms / 5 frozen bars.
- **a_verified_must_wire:** 🟠 KNOB-DIRECTIONAL → no GREEN to wire (KNOB, not a new capability lane).
  live core/*.hexa UNTOUCHED. (If a cleaner adaptive rule earns GREEN in a future frozen-first
  round, THAT round inherits the 4-rung wire ladder.)
- **c9 / p7:** FALSIFIED earned-shift reported as FALSIFIED (bar NOT moved — tune-to-green refused).
  exact ground truth (item grouping known), NO LLM judge / perplexity / loss — every decision is a
  no-grad read of substrate state (segmentation F1). **p8:** write = the engine's own tick.
- **p1/p2/p3/p6:** segmentation reads ONLY the gap timestamps + bound feature-sets, NO injected
  answer label / RLHF / persona / ethics. NOT an emit gate (memory-grouping read,
  `a_autonomy_over_hardcode`); Ψ-disjoint (pure temporal segmentation over stored items).
- **SCOPE TOY:** DIRECTIONAL numpy · 20 items / 2-4 feats / 8 distractors / 3 seeds / 2 rate
  regimes / deterministic readout (tests the gamma-segmentation STRUCTURE, not a learned bin
  controller). Discriminators decisive (no-binning 0.1641, shuffle 0.1506, ne_frozen 0.2952). The
  adaptive rule here = ADAPT_K × all-gap median EMA; a within-item-mode tracker is a follow-on.
  scale / real-corpus / learned bin-width / engine-transfer UNVERIFIED (`a_scale_honest_scope` ·
  `a_toy_scale_recheck`).

## artifacts
- `state/1555_gaba_gamma/h1555_gaba_gamma.py` (R1 numpy mirror, DIRECTIONAL — reuses H_1532/H_1544
  MemStore/key_vec/FNV-1a byte-for-byte; the ONLY new variable is the temporal bin segmentation)
- `state/verdicts/1555_gaba_gamma/H_1555_FREEZE.txt` (pre-registered frozen falsifier)
- `state/verdicts/1555_gaba_gamma/H_1555_R1.json` (R1 result, verbatim)

xref [[h1532-multistore-cls-wallbreak]] (CLS, the store this segments) · H_1544 (NE-flush 🟢, the
DECONFOUND target — gamma proven DISTINCT, +0.1753) · H_1554 (GABA disinhibition 🟠 KNOB, sibling
family) · H_1546/H_1551/H_1552 (GABA sparse-coding 🧱 ×3) · H_1553 (GABA census, RANK 2 gamma) ·
H_1284 (neuromodulation wall) · H_1534 (5-HT budget 🟠 KNOB precedent) · a_no_llm_frame_trap ·
a_break_the_wall (MULTI-LENS, census closed) · a_engine_native_learning (DIRECTIONAL) ·
a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9.
