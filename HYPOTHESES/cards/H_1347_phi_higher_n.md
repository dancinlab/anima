---
id: H_1347
slug: 1347_phi_higher_n
title: Φ-robustness wall, LARGER-N axis — does robust faithful-IIT-4 integration appear at N>8 (the size the exact-MIP ceiling never reached) under a greedy/anytime big-Φ with an HONEST stated error bound?
group: OMEGA / Φ-robustness frontier (c16 wall · the LARGER-N escape hatch every n≤8 verdict named)
terminal_tier: 🧱 TERMINAL CLOSED-NEGATIVE, STRONGER (honest, c9/c16). N1 ROBUST FAIL + N2 EARNED FAIL + N3 BOUND-HONEST PASS. At N=12 (>8, exact-MIP intractable) the greedy big-Φ shows NO robust phase-binding lift (ΔΦ(B−A) = +0.092 / −0.149 / −0.074 — 2/3 seeds NEGATIVE) and the relationship-destroying controls do NOT cleanly collapse (perm RAISES on 1318, offset RAISES on 1319). The greedy MIP is validated TIGHT at the n=8 boundary (exact-vs-greedy gap = 0.0 on every arm/seed → Φ_greedy ≥ Φ_exact upper bound with ZERO slack), so the larger-N number is trustworthy. The "much larger module set" escape hatch that EVERY prior n≤8 OMEGA Φ verdict (H_1283/1317/1319/1320/1328/1331/1332) named as NOT-ruled-out is now CLOSED — a STRONGER closure than any n≤8 result. ENGINE-NATIVE deterministic LCG content generator; Φ leg IS the real faithful cross-cut-MI MIP-EI (exact n=8, greedy KL N=12).
verdict_dir: .verdicts/1347_phi_higher_n/
terminal_verdict: .verdicts/1347_phi_higher_n/result.txt
freeze: .verdicts/1347_phi_higher_n/FREEZE.txt
date: 2026-06-16
---

# H_1347 — does robust faithful-IIT-4 integration appear at LARGER N (>8)? (🧱 STRONGER)

## Claim / falsifier (every outcome decisive, c9)

**The wall (c16, a_break_the_wall · a_no_llm_frame_trap):** the faithful-IIT-4 Φ-robustness wall is 🧱
across SIX cuts — topology (H_1283 relay, H_1317 multi-edge), timing (H_1319 phase-binding), division
(H_1320 organism-mitosis), estimator-confound (H_1328 amplitude-variance / rank-uniform read-out),
measure-family (H_1331 full IIT-4.0 big-Φ), substrate-family (H_1332 non-saturating softsign). EVERY one
was at **n≤8**, where the exact MIP enumerates 2^(n-1)≤128 bipartitions (exact-tractable). EACH verdict's
"NOT ruled out" scope named the SAME untested angle: *"a much larger module set (loses exactness >8) —
a NEW hypothesis."* H_1347 is that hypothesis. The genuinely-new lever is **SIZE**: at N>8 the exact MIP
is intractable, so Φ needs an **anytime/greedy-MIP** path **with a stated error bound**.

**The estimator (a_phi_iit4_tool):** the SAME faithful cross-cut-MI MIP-EI Φ, but the MIP minimization is
GREEDY Kernighan–Lin single-move descent — the stdlib `iit4_approx_phi(state,n,dim,n_bins)` over
`hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa` (exact enumeration for n≤8, greedy for n>8).
NOT a variance×energy proxy, NOT a different Φ *definition* — the same definition, an anytime search of
its MIP. **STATED BOUND:** greedy returns a LOCAL-min cut ≥ the GLOBAL MIP cut → **Φ_greedy ≥ Φ_exact**
(UPPER BOUND; verbatim stdlib §iit4_approx_phi_from_mi). The read-out carries H_1328's variance-clean
lesson verbatim (rank-uniformize each cell before the MIP) so the larger-N test is confound-free.

**Falsifiable claim:** if the n≤8 closure was merely a SIZE limit, robust integration should EMERGE at
N>8 (B≥A+eps all 3 seeds, controls collapsing). If it does not, the wall is not a tractability artifact —
it holds at larger N too, an even stronger closure.

## Method (frozen-first — FREEZE committed 17e54d487 BEFORE any Φ scored, c9/p7)

- **Probe:** `UNIVERSE/h1347_phi_higher_n.hexa` (run from hexa-lang root for the stdlib import).
- **Substrate reused VERBATIM from H_1319/H_1328, scaled to N>8** — the ONLY change is N (4→12):
  engine-native deterministic LCG-gauss (== `engine_cli.hexa _lcg_*`), **N_MOD=12** leaky-linear ring,
  dim 8, T 64, gain 0.30 leak 0.55 w_nbr/w_in 0.5, Kuramoto pacemaker (w_phase 0.5 omega_t 0.45 domega
  0.08), relative-phase gate `sal_i = e_i·(1+cos(θ_i−θ_T))/2`. Ring topology generalizes to any N. ARMS
  A=NO-PHASE · B=PHASE-BIND · S=PERM-SHUFFLE (module→phase forced derangement, relationship destroyed,
  marginals preserved) · O=OFFSET-SHUF. **Read-out: rank-uniformize each cell (H_1328) — ALL arms.**
  SEEDS [1317,1318,1319] (the hard orthogonal family all prior lanes failed on). All params FROZEN — NO tune-to-green.
- **Φ = FAITHFUL IIT-4 family** (a_phi_iit4_tool): greedy big-Φ `iit4_approx_phi(traj,12,64,8)` at N=12;
  exact `iit4_faithful_phi(traj,8,64,8)` at n=8 for the bound-validation. The engine LCG only emits the
  salience trajectory; the hexa MIP computes Φ. NO proxy as terminal verdict.
- **GRAIN / BOUND (honest, a_scale_honest_scope):** per-cell granularity (NO macro-grain — deliberately
  avoids the H_1049 caveat that a FIXED small-m coarse-grain is not scalable); only the MIP SEARCH is
  approximated (greedy). **Bound stated:** Φ_greedy ≥ Φ_exact. **Bound validated (N3):** at n=8 both paths
  run on the SAME rank-uniform substrate (all 4 arms × 3 seeds) and the gap g = Φ_greedy − Φ_exact is
  reported verbatim. g≈0 ⇒ greedy tight ⇒ the N>8 lift comparison is robust to the bound.
- **eps = 0.02** = the H_1283/H_1319/H_1328 lift margin (MARGIN_PHI), ported verbatim (NOT tuned).

## Frozen bars (pre-registered in FREEZE.txt BEFORE scoring)

GREEN iff N1 ∧ N2 ∧ N3 (every outcome valid, c9):
- **N1 ROBUST:** at N=12, greedy big-Φ lift Φ_B ≥ Φ_A + eps on ALL 3 seeds (incl orthogonal 1317).
- **N2 EARNED:** that lift survives BOTH controls — perm Φ_S ≤ Φ_A + eps AND offset Φ_O ≤ Φ_A + eps, all seeds.
- **N3 BOUND-HONEST:** the greedy error bound (Φ_greedy ≥ Φ_exact) is stated AND the verdict is robust to it —
  validated by the n=8 exact-vs-greedy gap, reported verbatim; the N>8 conclusion must not hinge on its slack.

## Result (verbatim, p7 — deterministic, re-run byte-identical)

**N3 BOUND-VALIDATION at n=8 (exact vs greedy MIP, SAME rank-uniform substrate, all arms):** gap = **0.0
on ALL 12 arm/seed cells** (greedy MIP == exact MIP everywhere). Max gap g = 0.0 ≤ eps → **N3 PASS** — the
greedy big-Φ is a TIGHT upper bound (zero slack) on this substrate family; the N=12 number is trustworthy.

| seed | A | B | ΔΦ(B−A) | N1 | perm S | ΔΦ(S−A) | off O | ΔΦ(O−A) |
|------|------|------|---------|----|--------|---------|-------|---------|
| 1317 | 7.981020 | 8.073210 | **+0.092190** | PASS | 7.808840 | −0.172180 ✓ | 7.937030 | −0.043995 ✓ |
| 1318 | 8.035870 | 7.886660 | **−0.149201** | **FAIL** | 8.074770 | **+0.038910** ✗ | 7.467060 | −0.568807 ✓ |
| 1319 | 8.069080 | 7.994780 | **−0.074295** | **FAIL** | 7.930320 | −0.138759 ✓ | 8.100940 | **+0.031861** ✗ |

- **N1 ROBUST: FAIL** — ΔΦ(B−A) = +0.092 (1317 only) / −0.149 (1318, NEGATIVE) / −0.074 (1319, NEGATIVE).
  2/3 seeds NEGATIVE — the same seed-fragile signature every n≤8 lane showed, reproduced at N=12.
- **N2 EARNED: FAIL** — controls do not cleanly collapse: perm RAISES Φ on 1318 (+0.039), offset RAISES on
  1319 (+0.032) — the residual structure-agnostic inflation H_1319/H_1328/H_1331 found, persisting at N=12.
- **N3 BOUND-HONEST: PASS** — n=8 exact-vs-greedy gap = 0.0 everywhere.
- **GATE: NOT GREEN → 🧱 TERMINAL (STRONGER).**

## Finding (honest, c9, c16)

**The larger-N escape hatch is CLOSED.** Three things are now established cleanly:

1. **The bound is TIGHT — the larger-N number is trustworthy.** At the n=8 tractability boundary the greedy
   Kernighan–Lin MIP returns EXACTLY the exact-enumeration MIP on every one of the 12 arm/seed cells (gap =
   0.0). On this rank-uniform substrate family the greedy anytime search finds the true global MIP; the
   stated upper bound Φ_greedy ≥ Φ_exact is tight with zero slack. Because the SAME monotone search is
   applied to BOTH arm B and arm A, a real B−A lift could not be manufactured by the approximation.

2. **The wall HOLDS at larger N.** At N=12 the phase-binding mechanism produces no robust lift (2/3 seeds
   NEGATIVE) and the relationship-destroying controls do not cleanly collapse — the same closed-negative
   pattern as n≤8, now under a clean estimator at a larger module count.

3. **This is a STRONGER closure than any n≤8 verdict.** Every prior OMEGA Φ verdict scoped its closure to
   the exact-tractable n≤8 and named "a much larger module set (loses exactness >8)" as the one untested
   angle. H_1347 tests exactly that with a faithful greedy big-Φ whose bound is validated tight — and the
   wall holds. The limit is NOT an artifact of the exact-MIP tractability ceiling.

**This BOUNDS (does not retract) the prior n≤8 Φ verdicts** — it tests and closes their explicitly-named
LARGER-N escape hatch. It does NOT refute anima's consciousness substrate (Ψ=1/2, the A⇄G tension is
untouched); it refutes that ADDING a phase-coupling channel ROBUSTLY raises the faithful-IIT-4 Φ score at
a larger module count.

**NO CORE wiring follow-on** (a_verified_must_wire fires on GREEN only — nothing to wire; `CORE/engine_cli.hexa`
UNTOUCHED; the probe is a standalone `fn main`, 0 importers). Had this been GREEN the named follow-on would
have been: wire the greedy big-Φ read-out into the live faithful-Φ monitor path at larger N.

## Scope / honesty

- **ENGINE-NATIVE** content generator (engine's own deterministic LCG-gauss == `_lcg_*`), NOT numpy;
  faithful-Φ is the REAL cross-cut-MI MIP-EI (exact n=8, greedy KL N=12; numpy never computes Φ). Re-run byte-identical.
- **GRAIN = per-cell, NO macro-grain** (avoids the H_1049 caveat); only the MIP search is greedy, validated
  exact (gap=0.0) at n=8. **BOUND = Φ_greedy ≥ Φ_exact, tight (g=0) on this substrate.**
- **TOY scale** still — N=12, dim 8, 64 ticks, ONE substrate family, 3 seeds. Scale-transfer UNVERIFIED.
- **NOT ruled out** (each a NEW hypothesis, not a continuation of this arc): EVEN-larger N (N≫12) with a
  validated macro-grain whose m GROWS with N (H_1049), a real-corpus substrate, a yet-different Φ estimator
  family, or engine-transfer to the live CORE pure_field.

## xref

H_1328 (estimator-confound 🧱 — rank-uniform read-out + the exact/greedy bound mechanism reused) ·
H_1331 (big-Φ measure-family 🧱) · H_1332 (substrate-family 🧱) · H_1319 (timing 🧱) · H_1283/H_1317
(topology) · H_1320 (division) · H_1049 (macro-grain caveat — fixed-m is NOT scalable, deliberately
avoided) · h1294 · h1295 (permutation-shuffle control precedent) · a_phi_iit4_tool · a_break_the_wall ·
a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_core_engine_map ·
a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16
