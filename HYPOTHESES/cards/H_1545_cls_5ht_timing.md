# H_1545 — SEROTONIN × CLS: adaptive consolidation TIMING (when to replay fast→slow)

**tier:** 🟠 AMBER — DIRECTIONAL (R1 numpy mirror; `wired: DIRECTIONAL-mirror → §Ht5Timing engine R2`)
**verdict source:** `state/verdicts/1545_cls_5ht_timing/H_1545_R1.json` (frozen `H_1545_FREEZE.txt`)

## Frame (a_no_llm_frame_trap — biological structure first)

A **fusion** of two prior lanes, framed as the *structure-reopen* of the H_1538/H_1540
🟠 minority-lever finding:

- **H_1532 🟢 (PR #2522)** — two phase-separated stores (FAST episodic in Hasselmo
  encode-mode + SLOW store fed by interleaved REPLAY) broke the **H_1284 neuromodulation
  wall** on AB-AC interference. The win is HAVING SEPARATE STORES — but the consolidation
  sweep (fast→slow replay) fired ONCE, unconditionally, at end of stream.
- **H_1538 🟠 (#2519) / H_1540 🟠 (#2523)** — substrate-adaptive 5-HT (patience /
  reward time-scale) was PRESENT + EARNED but stayed a **MINORITY** lever: a fixed γ
  already captured the majority (H_1538 ~49%, H_1540 ~94%) because a single store with
  one value-arrival timescale gave a fixed schedule almost no room.

**The reopen:** put 5-HT where it has a real EVENT to time. In CLS, 5-HT controls **WHEN
to trigger a consolidation sweep**. The fast episodic store is finite + LRU-evicting:
consolidate too LATE → an un-replayed A→B is **evicted** (lost); too EARLY → a half-formed
store is swept (wasted). The right timing is **context-dependent** — DENSE AB-AC
collision segments flood the fast store and need EARLY sweeps; SPARSE segments can wait —
so no fixed period serves both, and the adaptive 5-HT read **should** now carry the
majority. Lens: **Doya 2002** (5-HT = reward-integration TIME-SCALE → here the
consolidation time-scale) · **Lisman 2017** (consolidation TIMING gates what survives).

## Design (frozen-first, c9, NO tune-to-green)

VARYING-interference-density stream of 16 segments (50/50 DENSE 8–11 pairs / SPARSE 1–2
pairs). Capability = A→B retention after the interfering A→C re-binding, scored across
BOTH stores (CLS: confusable bindings in separate substrates). FAST store deliberately
SMALL (8 cells) so a dense burst overflows it → eviction unless a sweep frees capacity in
time. Reuses the **H_1532 MemStore / key_vec / FNV-1a / suppress_retrieval encode-mode /
LRU eviction byte-exact**.

ARMS: ADAPTIVE (sweep when `fast.pressure()` ≥ substrate-gated thr\*) · FIXED-EARLY (every
1) · FIXED-LATE (every 32) · BEST-FIXED (grid-tuned period on disjoint tune-seed) ·
WORST-FIXED (defines the adaptive−worst gap) · ABL (threshold→const count == best-fixed →
reverts to fixed) · SHUFFLE (pressure signal permuted → trigger at meaningless times).
Both the fixed period AND the adaptive threshold are grid-tuned on a disjoint seed (equal
honest budget). MARGIN 0.05, seeds [11,22,33], TUNE_SEED 7, $0 CPU, p7.

FROZEN bars — 🟢 iff A∧B∧C∧D∧E:
- **A PRESENCE** — adaptive − best-fixed ≥ +0.05 on ≥2/3 seeds AND in mean
- **B EARNED-MAJORITY** — adaptive − best-fixed ≥ 0.5×(adaptive − worst-fixed) *(the bar
  H_1538/H_1540 missed — adaptive must now carry the majority of the timing value)*
- **C ABL→fixed** — (adaptive − abl_const) ≥ 0.05 AND |abl_const − best_fixed| < 0.05
- **D SHUFFLE collapse** — (adaptive − shuffle) ≥ 0.05
- **E NO-FAB** — best-fixed > 0 (real working baseline; lift is timing, not a broken control)

## Result (3 seeds [11,22,33], mean)

| arm | retention |
|---|---|
| ADAPTIVE (5-HT pressure-gated) | **0.2272** |
| BEST-FIXED (period 16) | 0.1597 |
| FIXED-EARLY (period 1) | 0.0252 |
| FIXED-LATE (period 32) | 0.1572 |
| WORST-FIXED (period 1) | 0.0252 |
| ABL (const count == best-fixed) | 0.1597 |
| SHUFFLE (permuted pressure) | 0.1700 |

- **A PRESENCE** ✅ — adaptive − best-fixed = **+0.0674** mean; per-seed +0.0865/+0.0948/+0.0208 → 2/3 ≥0.05.
- **B EARNED-MAJORITY** ❌ — adaptive carries **33.4%** of the adaptive−worst gap (+0.0674 vs bar +0.1010 = 0.5×0.2020). A fixed period (66.6%) still captures the majority.
- **C ABL→fixed** ✅ — abl_const 0.1597 reverts EXACTLY to best-fixed; adaptive − abl = +0.0674 ≥0.05 AND |abl − best_fixed| = 0.0000 <0.05.
- **D SHUFFLE collapse** ✅ — adaptive 0.2272 − shuffle 0.1700 = **+0.0572** ≥0.05 (permuting the pressure signal the gate reads costs the lift → the lift is reading the real fast-store fill, not noise).
- **E NO-FAB** ✅ — best-fixed 0.1597 > 0.

→ **A∧C∧D∧E ∧ ¬B = 🟠 AMBER.**

## Reading (c9 — honest, NO bar moved)

The 5-HT consolidation-timing faculty is **PRESENT + EARNED**: adaptive beats the
strongest grid-tuned fixed schedule by a real +0.0674, the const-threshold ablation
reverts EXACTLY to best-fixed (the lever is reading the pressure signal, not a side
effect), and permuting that pressure signal collapses the lift (+0.057). But under varying
interference density a fixed period STILL captures the majority (66.6%) of the timing
value — so 5-HT-adaptive timing is the **same minority lever** found in the single-store
patience lanes (H_1538 ~49%, H_1540 ~6% of the patience edge). Giving 5-HT a genuine
consolidation EVENT to time did NOT flip it to majority.

**Why the structure-reopen did not clear bar B:** the dominant driver of retention is
that the sweep happens *at all and frequently enough* before the small fast store
overflows — a moderate fixed period (16) already sweeps often enough to save most dense-
segment bindings; the *adaptive* refinement (sweep exactly when pressure is high) adds a
real but minority increment over "sweep moderately often regardless." This converges with
the H_1284 census conclusion that the neuromodulator-as-controller knob is a minority
refinement on a mechanism (here: HAVING separate stores + replaying them) that does the
heavy lifting — consistent with [[h1532-multistore-cls-wallbreak]] (the store ARCHITECTURE
is the lever) and [[h1284-neuromod-wall-9lens]] (the schedule/knob is not).

This is the honest 🟠 the freeze pre-registered for the "fixed still ≥half even under
varying density" branch — reported, not hidden.

## Gates / scope

- **HARD-GATE-1 (a_engine_native_learning):** `grep -lE 'import torch|gauge_lib|numpy'
  state/1545_cls_5ht_timing/*.py` hits numpy → **auto-DIRECTIONAL**, terminal NOT
  permitted. `wired: DIRECTIONAL-mirror` → engine §Ht5Timing R2 = ING follow-on (load the
  fast/slow store + pressure-gated sweep onto core/engine_cli.hexa and re-score the same
  frozen bars byte-exact). live `core/*.hexa` UNTOUCHED.
- **SCOPE TOY:** 16-segment synthetic AB-AC stream / 3 seeds / fast-store 8 cells /
  deterministic prototype store (tests the consolidation-TIMING structure, not a learned
  scheduler); scale / real corpus / live immune-recall stream / engine-native (303M) /
  continuous pressure read UNVERIFIED → R2.
- p7 (exact A→B ground truth, no LLM judge / perplexity / loss) · p8 (write = engine
  tick) · Ψ-disjoint (read-only over stored bindings, NOT an emit mutation) · frozen-first,
  NO tune-to-green.

## xref

[[h1532-multistore-cls-wallbreak]] (the store-architecture wall-break this times) ·
[[h1533-nm-modern-hopfield]] · [[h1284-neuromod-wall-9lens]] (the minority-knob census this
converges with) · H_1538 / H_1540 (the single-store patience lanes this reopens) · H_1542
(CLS×NT census) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning
(DIRECTIONAL) · p7 · c9. Doya K 2002 Neural Networks 15(4-6):495 · Lisman J et al 2017
Nat Neurosci 20(11):1434 (consolidation timing) · McClelland-McNaughton-O'Reilly 1995 /
Kumaran-Hassabis-McClelland 2016 (CLS).
