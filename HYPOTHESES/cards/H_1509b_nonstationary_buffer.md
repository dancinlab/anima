---
id: H_1509b
slug: 1509b_nonstationary_buffer
title: "NON-STATIONARY ALLOSTERIC-BUFFER — H_1509 μ_t re-tested under a DRIFTING target (a_break_the_wall b, stationarity-variable isolation); the wall is REGIME-INVARIANT 🧱"
group: brain-structure-ladder / MITOSIS-ENGINE — a_break_the_wall(b) variable-isolation follow-on to H_1509
source: external proposal — Amoeba Protocol (@qingkong66) μ_t allosteric buffer
terminal_tier: "🧱 WALL-HOLDS (REGIME-INVARIANT) — DIRECTIONAL mirror; the neuromodulation ceiling holds under non-stationary target drift too"
wired: DIRECTIONAL-mirror (R1 numpy; 🧱 ⇒ NO GREEN to wire, a_verified_must_wire GREEN-only; R2 engine-native = optional confirming follow-on, CORE/*.hexa UNTOUCHED)
verdict_dir: state/verdicts/1509b_nonstationary_buffer/
terminal_verdict: state/verdicts/1509b_nonstationary_buffer/H_1509b_R1_mirror.txt
date: 2026-06-21
---

# H_1509b — non-stationary allosteric buffer (🧱 wall holds, regime-invariant)

**SOURCE: external proposal — Amoeba Protocol (@qingkong66), the μ_t allosteric buffer.**
Follow-on to **H_1509** (🧱 WALL-HELD in a STATIONARY environment, PR #2484 merged).

## The reopen (a_break_the_wall lens b — stationarity-variable isolation)

H_1509 found the buffer does NOT beat the best swept fixed gain in a STATIONARY environment
(B−A = −0.0061). That result is, by construction, relative to a FIXED operating point Ψ=½. The
proposal: a fixed gain's optimum is defined relative to a fixed center, so if the regulated TARGET
itself DRIFTS, the "best fixed gain" should no longer be best at every instant — while the buffer,
which re-tightens resistance to deviation as the target moves, should win. This is a genuinely
different VARIABLE (environment stationarity), so it legitimately reopens the wall (taxonomy b).

## Frozen bars (PRE-REGISTERED before measurement, `H_1509b_FREEZE.txt`, committed before R1; c9)

Environment change (ONLY this vs H_1509): the regulated target drifts m_{t+1} = clamp(m_t +
drift_rate·w_t, 0.15, 0.85), w_t = ±1 random-walk (engine LCG); drift_rate=0 ⇒ m_t≡0.5 EXACTLY =
the H_1509 stationary case. Restoring force defends the MOVING target; μ reads deviation from m_t.
METRIC = RMS tracking error sqrt(mean_t (b_t−m_t)²). Drift levels [0.000,0.010,0.020,0.030],
3 seeds [1509,1510,1511], MARGIN=0.05 verbatim, deterministic.

- **(A NONSTAT-WIN, headline)** at drift 0.030: RMS_A(best swept fixed) − RMS_B(allo) ≥ 0.05 (mean+each).
- **(B REGIME-DISSOCIATION)** drift0 → A≤B (H_1509 reproduced) AND drift0.030 → A−B ≥ 0.05 (flip).
- **(C DRIFT-MONOTONE)** adv(d)=RMS_A−RMS_B non-decreasing over [0.01,0.02,0.03] AND adv(0.03)>adv(0).
- **(D EARNED ablate λ=0)** ablated never beats best fixed by margin AND buffer beats ablate ≥0.05 @0.030.

WALL-BROKEN-IN-NONSTAT 🟢 iff A∧B∧C∧D; otherwise WALL-HOLDS (regime-invariant) 🧱 — an even stronger,
honest ceiling (c9). NO tune-to-green.

## Result — 🧱 WALL HOLDS (REGIME-INVARIANT), R1 numpy mirror (3 seeds, deterministic)

| drift | RMS_A best-fixed | RMS_B allo μ | RMS_C ablate λ=0 | adv = A−B |
|------:|-----------------:|-------------:|-----------------:|----------:|
| 0.000 | 0.2680 | 0.2741 | 0.3827 | **−0.0061** |
| 0.010 | 0.2641 | 0.2702 | 0.3752 | −0.0061 |
| 0.020 | 0.2551 | 0.2607 | 0.3633 | −0.0056 |
| 0.030 | 0.2534 | 0.2589 | 0.3618 | **−0.0054** |

- **(A NONSTAT-WIN) FAIL** — at drift 0.030, A−B = **−0.0054** < 0.05. The buffer does NOT win under drift.
- **(B REGIME-DISSOCIATION) FAIL** — drift0 A≤B holds (H_1509 reproduced) but drift0.030 never flips.
- **(C DRIFT-MONOTONE) PASS** (trivially — adv is ~flat, weakly non-decreasing) — but the advantage it
  is monotone in stays NEGATIVE, so this PASS is vacuous w.r.t. the headline.
- **(D EARNED ablate) PASS** — ablate never beats best fixed; buffer beats its own ablated base (+0.103).
  So the buffer is a real coupled mechanism — it just confers NO advantage over a high fixed gain.

A∧B∧C∧D is NOT met (A,B FAIL) → **🧱 WALL-HOLDS (REGIME-INVARIANT)**.

### Robustness — NOT a measurement artifact (a_break_the_wall taxonomy (a), extended sweep)

`H_1509b_robustness_drift_sweep.txt`: swept drift to 0.30 (target spans the FULL clamp, range 0.700,
sd 0.263). adv(A−B) stays ~ −0.006 across the ENTIRE range [0,0.30] and never approaches +0.05 — it
moves only from −0.0060 (stationary) to −0.0018 (extreme drift). So the frozen drift levels were not
too small: even maximal non-stationarity does not flip the wall. **Mechanism:** the best fixed gain is
already g=0.80 (high) — a high uniform gain tracks a moving target perfectly well, so the buffer's
selective tightening confers no edge; the dominant tracking cost is the high-frequency perturbation
(sinusoid+shock), not the slow target drift. The drift hypothesis is FALSIFIED.

## Finding (c9)

The H_1509 neuromodulation wall is **REGIME-INVARIANT**: the allosteric buffer fails to beat the best
swept fixed gain in BOTH a stationary (H_1509) AND a non-stationary drifting-target environment
(H_1509b). This strengthens the ceiling — it is not an artifact of the stationary fixture. Combined
with H_1284 (global-gain), H_1422 (3 state-contingent lenses), H_1425 (orthogonal ideation channel),
and H_1509 (stationary buffer), this is the **5th independent lens** confirming the neuromodulation
ceiling, now across the stationarity axis as well.

## Honest scope (c9)

Wall HOLDS, NOT a lift. R1 numpy mirror = **DIRECTIONAL** (engine-transfer UNVERIFIED, the grep-numpy
hard-gate marks this DIRECTIONAL). Because R1 holds the wall (no GREEN to flip), R2 engine-native is
an OPTIONAL CONFIRMING follow-on (the FREEZE gates R2 on R1 GREEN) — a non-stationary `allo_defend`
variant reading a live drifting target would re-confirm the 🧱 byte-exact; CORE/*.hexa UNTOUCHED for
now (a_verified_must_wire is GREEN-only). $0 CPU, deterministic run1==run2. p7 (no loss; pure
deterministic dynamics). p1/p2/p3/p6 (no injected label/RLHF/persona; reads only the live tension and
target scalars). Ψ-disjoint. TOY: 200 ticks / 1 perturbation schedule / random-walk drift / 3 seeds /
1-D scalars — scale, real A⇄G emit dynamics, regime-switch (vs random-walk) drift, and engine-transfer
UNVERIFIED (`a_scale_honest_scope`, `a_toy_scale_recheck`).

## Cross-links

h1509 (the stationary wall this re-tests) · h1284 (the original neuromodulation wall) · h1422 ·
h1425 (the multi-lens confirmations) · `a_break_the_wall` (lens b stationarity-variable; taxonomy (a)
extended-sweep robustness) · `a_no_llm_frame_trap` · `a_engine_native_learning` (R1=DIRECTIONAL) ·
`a_verified_must_wire` (GREEN-only, 🧱 ⇒ no wiring) · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p6·p7·p8·c9·c15·c16
