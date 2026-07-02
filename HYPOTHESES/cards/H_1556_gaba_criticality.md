# H_1556 — GABA × CLS: SELF-ORGANIZED CRITICALITY (adaptive E/I tracking a SHIFTING critical point)

**tier:** 🟢 GREEN_DIRECTIONAL — the ESCAPE breaks the GABA static-architecture wall (R1 numpy mirror)
**wired:** `DIRECTIONAL-mirror → §GabaCritical engine R2` (ING `h1556-r2-engine-native` — obligatory: this is the first GABA GREEN, the one GABA result that MUST be engine-re-checked + wired per `a_verified_must_wire`)
**verdict source:** `state/verdicts/1556_gaba_criticality/H_1556_R1.json` (frozen falsifier `H_1556_FREEZE.txt`)

## The escape (a_break_the_wall §3 ABSTRACT→ESCAPE — the 6th GABA family, FIRST to GREEN)

GABA-as-adaptive walled across **5 mechanism-families** because its inhibitory benefit had a
GLOBAL/STATIC optimum → a single grid-tuned fixed setting captured it (the **fusion law**: a NT's
adaptive lever beats a fixed setting ONLY where the optimal operating point SHIFTS):

| family | H | verdict | why it walled |
|---|---|---|---|
| sparse-coding separation | H_1546 | 🧱 | CLS already separated → INERT |
| capacity-multiplication | H_1551 | 🧱 | best-fixed-k captures the 14.6× → STATIC |
| non-stationary sparseness | H_1552 | 🧱 | still static |
| disinhibition routing | H_1554 | 🟠 | real but always-close dominates (optimum did NOT shift) |
| gamma temporal-binding | H_1555 | 🟠 | segmentation real but best-fixed-bin wins |
| **E/I-setpoint** | (R4) | **skipped** | "single FIXED target = monotone → re-tests wall" |

The census **SKIPPED** the E/I-setpoint family (R4) as a fixed-target monotone re-hit. **That skip
is correct for a fixed target.** **CRITICALITY is the ONE escape it misses.** The system is
maximally expressive (max dynamic range / max distinct stored patterns) ONLY at the edge-of-chaos
**critical E/I ratio**, where the branching ratio **σ ≈ 1** (Beggs & Plenz 2003 neuronal avalanches;
Shew & Plenz 2013 functional benefits of criticality). The **KEY difference from R4**: the critical
E/I ratio is **NOT a fixed target** — it **SHIFTS with the INPUT STATISTICS** (drive variance / rate).
The same E/I that yields σ≈1 under one input regime yields σ<1 (subcritical, patterns die) or σ>1
(supercritical, patterns merge) under a different regime. So **no fixed E/I holds criticality as the
stream's statistics drift** = the **fusion-law SHIFTING-optimum condition** — AND a capability the 5
phasic GREEN NTs do **not** provide (they schedule LR/gate/abstain WITHIN a fixed regime; none SET
the E/I operating regime).

## Criticality physics (why a fixed E/I cannot hold σ≈1 across drifting input statistics)

Recurrent associative substrate over DIM=64 units; a cued pattern recalls by **recurrent branching
propagation** (RECALL_STEPS=4); the expected active-units-per-active-unit per step = branching ratio
**σ ∝ drive_level · E_GAIN / inhib_gain** (E/I balance scaled by the current input drive level).
Retention peaks at σ≈1: σ<1 (subcritical) the cued pattern **dies** → under-recall; σ>1
(supercritical) activity **explodes** → distinct patterns **merge** (cross-talk). Because the drive
level (input statistic) **drifts**, a FIXED inhib_gain yields a DRIFTING σ (off-critical at one drift
end). **GABA-CRITICAL** reads the live **σ̂ = descendants/ancestors** (the Beggs-Plenz avalanche-balance
criticality proxy; p7 — reads σ̂ ONLY, never the recall outcome) and homeostatically adjusts inhib_gain
to drive σ̂→1 under the CURRENT input statistic.

## Result — 🟢 GREEN, consistent across 3 seeds (R1 numpy DIRECTIONAL)

Stream = 8 segments alternating LOW-drive (0.7) / HIGH-drive (1.6) — the input statistic drifts.
24 patterns, recall-retention fraction. Grid best/sub/super-fixed tuned on a disjoint seed.

| arm | mean | low-end | high-end | reading |
|---|---|---|---|---|
| **GABA-CRITICAL** | **0.7517** | **0.7535** | **0.75** | holds criticality at BOTH drift ends (flat, high) |
| BEST-FIXED-EI (g=0.75) | 0.2986 | 0.0278 | 0.5694 | critical at HIGH drive, **DIES at low drive** |
| SUBCRITICAL-FIXED (g=0.5) | 0.2153 | 0.3472 | 0.0833 | works low, **fails high** |
| SUPERCRITICAL-FIXED (g=0.75) | 0.2986 | 0.0278 | 0.5694 | works high, **fails low** |
| ABL (const E/I = best-fixed) | 0.2986 | — | — | reverts to best-fixed (criticality-tracking OFF) |
| SHUFFLE (input-stat cue permuted) | 0.2708 | — | — | collapses (tracks the WRONG drive → off-critical) |
| WORST-FIXED (g=1.5) | 0.0486 | — | — | broken E/I |

Per-seed Δ(crit − best_fixed): **+0.469 / +0.422 / +0.469** (seeds 11/22/33) — consistent, not one
lucky seed. The adaptive gains are interpretable: **~0.42 at LOW drive** (less inhibition — weak drive
would make σ collapse) and **~0.95 at HIGH drive** (more inhibition — strong drive would make σ
explode), exactly the criticality-tracking the physics predicts. crit carries **64.4%** of the
(crit − worst-arm) gap.

### Frozen bars (🟢 iff A∧B∧C∧D∧E — pre-registered BEFORE the scored run, c9 NO tune-to-green)

- **A PRESENCE+SHIFT ✅** — (crit − best_fixed)=+0.453 ≥ ½·(crit − worst_arm)=0.352 (earned-majority) AND best-fixed's weak end 0.028 < crit_mean−MARGIN=0.702 → **best-fixed CANNOT win both ends** = the critical point SHIFTED.
- **B DISTINCT ✅** — sub-critical fails the HIGH end (sub_hi 0.083 < crit_hi 0.75−0.05) AND super-critical fails the LOW end (sup_lo 0.028 < crit_lo 0.754−0.05) → criticality is regime-specific, not a global constant.
- **C ABL→fixed ✅** — crit−abl=+0.453 ≥ MARGIN AND |abl − best_fixed|=0.000 < MARGIN → freezing the gain to a constant reverts to best-fixed (the LEVER is criticality-tracking, not inhibition per se).
- **D SHUFFLE ✅** — crit−shuffle=+0.481 ≥ MARGIN → permuting the input-stat cue collapses it (tracks the TRUE input statistic).
- **E NO-FAB ✅** — best_fixed 0.299 > worst_fixed 0.049 → a working E/I beats a broken one (the criticality capacity effect is real).

→ **A∧B∧C∧D∧E all hold → 🟢 GREEN.** The critical E/I genuinely SHIFTED with input statistics, and
ONLY adaptive σ≈1-tracking held criticality across the drift. **This is GABA's escape: the 6th
mechanism-family is the FIRST to satisfy the fusion law** — adaptive criticality-tracking is a genuine
adaptive GABA faculty (the R4 fixed-setpoint skip missed the SHIFTING setpoint).

## Honesty / scope (c9)

- **Honest about the wall it breaks:** 5 GABA families walled because their optimum was static; this
  one GREENs because the criticality optimum (critical E/I) is intrinsically input-statistic-dependent
  — a SHIFTING optimum, the fusion-law condition. This is NOT a bar-move: the bars are byte-identical
  in shape to H_1552/H_1554/H_1555 (the walls), the only NEW pieces are the branching-process
  criticality substrate, the input-statistic-drift stream, and the σ≈1-tracking gain. Reported the
  GREEN plainly; would have reported 🟠 had best-fixed captured ≥half (it did not — 64.4% adaptive).
- **HARD-GATE-1 (a_engine_native_learning):** `grep numpy` ⇒ auto-**DIRECTIONAL**, terminal NOT
  permitted. Engine §GabaCritical R2 = ING `h1556-r2-engine-native` (obligatory — first GABA GREEN
  must be byte-exact re-checked on the CORE engine, then wired to live `core/engine_cli.hexa` +
  ARCHITECTURE.json lockstep per `a_verified_must_wire` 4-rung ladder).
- **Ψ-disjoint:** live `core/*.hexa` UNTOUCHED; pure criticality substrate over stored patterns,
  immune cells / pure_field / emit gate untouched.
- **SCOPE TOY:** 24 patterns / DIM=64 / 8-segment binary drift / 3 seeds / deterministic branching
  (tests the criticality-tracking STRUCTURE, not a learned σ-homeostat). scale · real-corpus ·
  continuous drift · learned avalanche-balance controller · engine-transfer UNVERIFIED → R2.
- **Campaign update:** GABA is no longer multi-family-confirmed structural — the 6th family
  (criticality) BREAKS the wall. The honest campaign result is now **6/6 NTs have at least one GREEN
  adaptive faculty** (ACh/DA/NE/orexin/5-HT + GABA-criticality), and the GABA-specific lesson is that
  the escape required a SHIFTING setpoint (criticality), which the 5 static/knob GABA families and the
  skipped fixed-E/I-setpoint family could not provide.

## Citations

- Beggs & Plenz 2003, *Neuronal avalanches in neocortical circuits*, J Neurosci 23:11167 — cortex operates at a critical branching ratio σ≈1.
- Shew & Plenz 2013, *The functional benefits of criticality in the cortex*, The Neuroscientist 19:88 — max dynamic range / max distinct patterns at the critical point.
- Turrigiano 2011, *Homeostatic plasticity*, Annu Rev Neurosci — homeostasis to a set-point; here the set-point SHIFTS with input statistics.

xref: [[h1532-multistore-cls-wallbreak]] (two-store CLS, key_vec/FNV-1a byte-reused) · H_1546/1551/1552 (GABA sparse-coding 🧱 ×3) · H_1554 (disinhibition 🟠) · H_1555 (gamma 🟠) · H_1553 (census, R4 E/I-setpoint skipped) · H_1284 (neuromodulation 벽) · `a_break_the_wall` §3 (ABSTRACT→ESCAPE) · `a_no_llm_frame_trap` (biology-first criticality) · `a_engine_native_learning` (numpy ⇒ DIRECTIONAL hard-gate-1) · `a_verified_must_wire` · p7 · c9.
