# H_1540 🧘 SEROTONIN-AS-PATIENCE — REGIME-SHIFTING-HORIZON retry of H_1538

**tier:** 🟠 AMBER DIRECTIONAL (R1 numpy mirror; `wired:DIRECTIONAL-mirror` — engine R2 deferred ING)
**verdict source:** `state/verdicts/1540_nt_5ht_retry/` (`H_1540_FREEZE.txt` · `H_1540_R1.txt` · `H_1540_R1.json`)
**parent:** H_1538 🟠 (#2519) — retries its OWN identified gap (bar C: fixed γ captured ~51%, adaptive a minority lever)

## THE RETRY (the H_1538 lane's own gap, NOT tune-to-green)

H_1538 found the wait-for-better-emit PATIENCE faculty PRESENT + EARNED — only the strong mechanism-attribution **bar C** failed: a FIXED γ already captured ~51% of the patience value, so the substrate-ADAPTIVE 5-HT slope read was real but a MINORITY lever. The lane's own diagnosis of WHY: H_1538 used a SINGLE value-arrival timescale (rise_len ∈ [3,7]) → one constant discount horizon was near-optimal everywhere, leaving little for adaptation.

**The one change (pre-registered, bars unchanged):** a **REGIME-SHIFTING HORIZON** where the optimal patience genuinely SHIFTS across contexts, inferable from substrate state:
- **FAST regime** — peak EARLY (rise_len 1-2), decays HARD (0.14-0.22) → SHORT optimal wait, waiting punished; early slope STEEP.
- **SLOW regime** — peak LATE (rise_len 7-9), decays gently (0.04-0.08) → LONG optimal wait, waiting rewarded; early slope SHALLOW.

50/50 mix, regime HIDDEN (only the early-slope substrate signal leaks it). A single fixed γ is a compromise wrong in BOTH regimes; the substrate-state-gated adaptive γ (5-HT read) SHOULD now carry the MAJORITY → clear bar C. This is the Doya 2002 condition (5-HT sets the *context-adaptive* reward time-scale).

Two construction choices, frozen-first (a_break_the_wall type-a, bars UNCHANGED): (i) the wait rule uses a **γ-horizon multi-step look-ahead** (best γ^k-discounted grounded value reachable by waiting k ticks net of k wait-costs), NOT a myopic one-tick peek — a one-step peek cannot SEE a grounded peak several ticks away, degenerating the SLOW regime to 0 for ALL arms (a faulty control wiring, not a bar). γ IS the integration horizon, so the regime-gated γ is the lever a fixed γ cannot match. (ii) the adaptive γ is read ONCE per episode from the early-slope steepness (`γ_eff = clip01(0.55 + 1.2·(0.30 − early_slope))`), constants set from the generative regime structure, NOT fitted to the bar.

## ARMS

| arm | policy |
|---|---|
| **IMPULSIVE** | emit at tick 0 (γ→0, impatient baseline) |
| **PATIENT-5HT** | γ ADAPTED by substrate early-slope REGIME read (the 5-HT faculty) |
| **ABL-FIXED** | fixed γ=0.55, NO regime read (patience without the 5-HT adaptive horizon) |
| **NEVERWAIT** | always-wait floor (emit only at last tick) — must-not-just-always-wait control |
| **SHUFFLE** | PATIENT & IMPULSIVE on the SAME time-permuted envelope (rising→decaying destroyed) |

## FROZEN BARS (IDENTICAL to H_1538; GREEN iff A∧A2∧B∧B2∧C∧D — `H_1540_FREEZE.txt`)

| bar | def | result | pass |
|---|---|---|---|
| A PRESENCE | mean PATIENT − IMPULSIVE ≥ +0.10 | **+0.5057** | ✅ |
| A2 PER-SEED | lift ≥ +0.10 on ≥2/3 seeds | 3/3 (+0.5184/+0.4957/+0.5032) | ✅ |
| B NOT-ALWAYS-WAIT | mean PATIENT − NEVERWAIT ≥ +0.10 | **+0.3750** | ✅ |
| B2 WAIT-BETWEEN | wait-ticks IMPULSIVE < PATIENT < NEVERWAIT | 0.00 < 1.96 < 11.00 | ✅ |
| C EARNED ablate | (PAT−IMP) − (ABL−IMP) ≥ 0.5×lift | **+0.0328 vs bar +0.2529** | ❌ |
| D EARNED shuffle | (patient edge real − shuffled) ≥ 0.5×lift | +0.4416 (edge +0.506→+0.064) | ✅ |

## VERDICT — 🟠 AMBER (c9, frozen-first, NO bar moved)

The **wait-for-better-emit PATIENCE faculty is PRESENT and EARNED** under the regime-shifting horizon too: it out-earns impulsive (+0.5057), strictly beats the always-wait floor (+0.3750; waits 1.96 ticks, between IMPULSIVE 0 and NEVERWAIT 11 — *not* procrastination), and its edge **collapses** when the arrival-time envelope is shuffled (+0.506 → +0.064). A∧A2∧B∧B2∧D all PASS.

The single fail is **C** again — and *more decisively* than H_1538: under a regime that should MAXIMALLY reward adaptation, a **fixed γ STILL captures ~94%** of the patience value (margin +0.0328 vs bar +0.2529, stable across all 3 seeds); the substrate-adaptive 5-HT regime read carries only **~6%** (vs H_1538's ~49%). Per-regime diagnostic: the entire edge lives where the climb-then-decay envelope exists; the per-tick wait/emit comparison (which watches the running grounded value + local slope and stops the moment the climb plateaus) is **intrinsically regime-discriminating** regardless of the explicit γ — so a fixed γ + online slope-watching already does almost all the regime-discrimination work, leaving the explicit substrate-state γ-gate a thin top slice.

**Honest reading (c9):** serotonin-as-patience DOES add a real, envelope-earned wait-for-better-emit timing faculty to the emit gate — and that holds across regime-shifting horizons — **but the value is captured by *any* online finite-horizon discounter; the substrate-state-ADAPTIVE ("infer the regime from the early slope and set γ") read is real yet a *minority* lever, and the regime-shifting test makes that MORE clear, not less.** This is a genuine, seed-stable, falsified-prediction result (the retry's hypothesis — "shifting horizon flips adaptation to majority" — is REFUTED, ~6% not ≥50%), NOT a tune-to-green miss: the bar stays frozen. The deeper lesson: the patience/horizon value is a property of *discounting at all*, not of *context-adaptive* discounting — so 5-HT-as-faculty is best framed as a finite-horizon emit-timing controller (Doya/Miyazaki temporal-discounting), with the adaptive-time-scale claim a minority refinement. Two independent regimes (single-timescale H_1538, regime-shifting H_1540) now converge on the same minority-adaptation result (a_break_the_wall multi-lens).

## SCOPE / wiring (a_engine_native_learning · a_verified_must_wire)
DIRECTIONAL numpy mirror (`grep numpy` ⇒ auto-DIRECTIONAL) — **engine-transfer UNVERIFIED**. TOY 12-tick synthetic 2-regime value envelope / 400 ep / 3 seeds / deterministic policy (tests the patience-faculty STRUCTURE under regime-shift, not a learned discounter). Scale / real grounded-value stream off live immune recall margin / continuous γ / >2 regimes / learned regime-inference / engine-native R2 on `core/engine_cli.hexa` emit gate = follow-on **ING** (R2 deferred). Ψ-disjoint read (timing policy over a value stream, no pure_field/emit mutation). p7 (payoff nets wait-cost + requires grounding, no perplexity), frozen-first, c9.
