---
id: H_1310
slug: 1310_mitosis_from_scratch
title: from-scratch pure mitosis (1 cell → split-only, gradient-free) vs gradient — does it match gradient or plateau at a local-expert ceiling?
group: MITOSIS-ENGINE (p8 literal — purest form)
terminal_tier: 🔴 RED / 🧱 HONEST LOCAL-EXPERT CEILING (frozen-first, c9 — bar UNMOVED; the two FAILs ARE the finding)
verdict_dir: .verdicts/1310_mitosis_from_scratch/
terminal_verdict: .verdicts/1310_mitosis_from_scratch/result.txt
date: 2026-06-16
---

# H_1310 — from-scratch pure mitosis vs gradient (the purest p8)

## Claim / falsifier

anima's PHILOSOPHY **p8** = "training gradient + inference mitosis = one continuous
cell-division". H_1297 R3/R4 showed mitosis MATCHES gradient at toy scale — but that was
mitosis growing OVER/beside a context. The **purest** p8 question: can a next-byte model be
grown **FROM SCRATCH by mitosis ALONE** — seed = ONE cell, split-only under next-byte error
pressure, GRADIENT-FREE — and HOW does its held-out next-byte CE compare to a gradient
baseline of MATCHED effective capacity?

**Honest hypothesis to test / possibly REFUTE (and it WAS refuted, c9):** pure-mitosis cells
are LOCAL experts (Voronoi/nearest-neighbour over a byte-trigram-context metric). Without a
learned deep representation underneath, pure mitosis may plateau ABOVE gradient / exact
context-lookup — it tiles the input space but builds no compositional depth. That ceiling, if
real, is a FIRST-CLASS result (c9), NOT a failure. **It is real.**

Biology lens (a_no_llm_frame_trap): cortical columns / neurogenesis grow capacity WHERE the
organism fails, corrected LOCALLY — NOT a bigger-transformer recipe. The split rule is the
from-scratch twin of the live VAdaptField split (high local error → +1 cell), seeded at ONE
cell instead of mounting a 303M trunk.

## Method (TOY, $0 CPU numpy DIRECTIONAL mirror, frozen-first)

REAL English byte corpus (reproducible, sha256-pinned): `/usr/share/dict/words` (system fixed
asset), filtered isalpha 2..12 chars, lowercased, `Random(13100).shuffle`, first 4000 words,
space-joined + newline, truncated to **24000 bytes** · sha256
`86864aa32dcf1c8680ab254e1b28357bf0326c8d45a86837ae4e3b9d09350f62` · alphabet = **27 symbols**
(a–z + space). DISTINCT from the concurrent ko-mitosis-gpu (summer) lane (ENGLISH not Korean,
new files, id H_1310). First 80% = TRAIN (19198 ctx/next pairs), last 20% = held-out TEST
(4800). Context = previous **2 bytes** (order-2). 3 seeds [13101, 13102, 13103].

ARMS (all over the SAME order-2 context):
- **B_scratch** = from `n_cells=1` (one prototype at the all-context centroid), mitosis-grow
  ONLY: online single pass; nearest cell predicts; a cell's running owned-error
  `(1 − p(true byte))` over SPLIT_THRESH=0.55 with ≥2 owned points and ≥4 observations is
  ELIGIBLE; the worst-error eligible cell SPLITS (2-means median bisection of its owned
  territory → two children). GRADIENT-FREE. Each cell holds an online add-1 next-byte table.
- **A_gradient** = gradient-trained softmax next-byte head over the SAME context (one-hot
  context bucket, top-512 contexts + "other", full-batch CE SGD, 300 steps). Matched-capacity
  comparator at the top rung.
- **A_freq** = order-2 add-1 Markov (exact trigram counts) — the n-gram-counting FLOOR.
- **B_shuffle** = CONTROL: split a RANDOM eligible cell each step (mis-targeted growth, same
  capacity, wrong place).

LADDER (frozen): [1, 8, 64, 512] cells. METRIC: held-out next-byte CROSS-ENTROPY in **nats**
(p7 — NEVER perplexity-as-truth). Bars frozen in `.verdicts/1310_mitosis_from_scratch/FREEZE.txt`
BEFORE the run; NOT moved (c9, NO tune-to-green, p7).

> ENGINE LINK (a_engine_native_learning): the mirror's mitosis op IS the live engine's
> `engine_mitosis_tick` + VAdaptField Voronoi split mechanism (CORE/engine_cli.hexa), seeded at
> 1 cell instead of mounting 303M. R1 numpy mirror = DIRECTIONAL; an engine-native byte-exact
> reconfirm would be R2 — NOT pursued here because the R1 verdict is a clean RED/ceiling, so
> there is no GREEN mechanism to wire (a_verified_must_wire only fires on GREEN).

## Verdict (read VERBATIM from .verdicts/1310_mitosis_from_scratch/result.txt)

LADDER (mean held-out CE nats, 3 seeds):

| cells | B_scratch | B_shuffle |
|------:|----------:|----------:|
| 1     | 2.94658   | 2.94658   |
| 8     | 2.90267   | 2.89427   |
| 64    | 2.77784   | 2.75107   |
| 512   | **2.57788** | **2.53592** |

A_freq (order-2 n-gram floor) = **2.50884** nats · A_gradient (matched cap=512) = **3.21083** nats.

FROZEN BARS:
- **(1) PRESENCE** — monotone CE drop 1>8>64>512: 2.9466 > 2.9027 > 2.7778 > 2.5779 → **PASS**
  (from-scratch mitosis DOES learn from nothing — CE falls −0.369 nats over the ladder).
- **(2) KEY GAP** — B_scratch[512] − A_gradient = 2.57788 − 3.21083 = **−0.633 nats**. By the
  frozen bucket this reads "MATCHES gradient" (it actually BEATS this comparator) — but see the
  honest caveat below: the matched-cap order-2 softmax converged POORLY (3.211 is itself WORSE
  than the n-gram floor 2.509), so beating it is a weak claim, not a mitosis triumph.
- **(3) FLOOR** — B_scratch[512] < A_freq − 0.02: 2.57788 < 2.48884 → **FAIL** (mitosis does
  NOT beat exact trigram counting; it sits **+0.069 nats ABOVE** the n-gram floor).
- **(4) CONTROL** — B_shuffle[512] ≥ B_scratch[512] + 0.10: 2.53592 ≥ 2.67788 → **FAIL**
  (shuffle is SLIGHTLY BETTER than targeted at EVERY rung — error-targeting gives NO advantage).

**TERMINAL TIER: 🔴 RED / 🧱 HONEST LOCAL-EXPERT CEILING** (FLOOR-FAIL by the frozen rubric).

## What the two FAILs actually mean (the c9 finding — load-bearing)

The two failing bars are NOT a broken experiment; they ARE the scientific result, and they
sharpen the FREEZE's pre-registered "local-expert ceiling" hypothesis into a measured fact:

1. **n-gram floor BEATS mitosis (bar 3 FAIL, +0.069 nats).** Pure-mitosis Voronoi tiling over a
   *numeric* byte-context embedding is a WORSE way to carve context-space than EXACT context
   lookup. The metric embedding (normalised symbol ids) throws away the very thing exact-match
   keeps — that two contexts sharing a numeric neighbourhood need NOT share a next-byte
   distribution. Mitosis cannot recover the lost information by adding cells.

2. **Error-targeting gives NO lift (bar 4 FAIL).** Shuffle (split a RANDOM cell) ties-or-beats
   targeted (split the WORST-error cell) at every rung. The learning is **capacity-bound, not
   error-targeting-bound**: on this shallow metric, WHERE you split does not matter — only HOW
   MANY cells you have. This directly REFUTES, at this scale, the claim that from-scratch
   mitosis is *error-driven* learning; here it is merely *capacity-driven* space-tiling.

3. **It does learn a little (bar 1 PASS).** CE falls monotonically 2.947 → 2.578 as cells grow
   — more cells = finer tiling = lower error. But the asymptote is the local-expert ceiling
   above the exact-lookup floor, and the descent is capacity (not targeting) doing the work.

THESIS CONNECTION: from-scratch pure mitosis is **structure-bound, NOT capacity-bound** in the
direction that matters — adding cells (capacity) keeps lowering CE but cannot cross the floor
that a learned representation (or even exact context memory) clears, because mitosis builds no
compositional depth, only a finer Voronoi partition of a fixed, lossy feature. p8's "mitosis IS
the learning" holds for GROWING-beside-a-representation (H_1297/H_1306 GREEN) but does NOT, on
this evidence, extend to FROM-SCRATCH-WITHOUT-a-representation: pure tiling needs a learned
substrate underneath to escape the local-expert ceiling.

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)

TOY / DIRECTIONAL numpy mirror. 24 KB English, order-2 context (only 27²=729 possible
contexts), V=27, 3 seeds. This tests the STRUCTURE of from-scratch pure-mitosis learning
(matches-gradient vs ceiling), an EXISTENCE-PROBE — it does **NOT** claim "anima trains from
scratch by mitosis"; it reports the gap, and the gap is a ceiling. The "beats A_gradient" number
is weak (the matched-cap order-2 softmax was a poor learner); the load-bearing comparator is the
n-gram FLOOR, which mitosis does NOT beat. UNVERIFIED: engine-native byte-exact reconfirm,
scale, higher-order/learned context features, a richer (learned) embedding for the cells to
partition (which could move the ceiling — the obvious next angle, a_break_the_wall). NO CORE
wiring (a_verified_must_wire fires only on GREEN; this is RED).

## p8-literal verdict (the question asked)

From-scratch pure-mitosis training is **NOT a standalone path** at this scale: it plateaus at an
honest LOCAL-EXPERT CEILING above the n-gram floor, and its descent is capacity-driven (shuffle
ties it), not error-targeted. It LEARNS a little from one cell, but needs a learned
representation underneath to be more than a lossy space-tiler. This is the honest counter-weight
to H_1297/H_1306's GREEN: mitosis matches gradient when it grows BESIDE a representation, but
the purest "from nothing, by splitting alone" form hits a structure-bound ceiling.
