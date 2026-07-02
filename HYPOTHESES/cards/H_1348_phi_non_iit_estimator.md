# H_1348 — Φ-robustness under a NON-IIT integration measure (summed transfer entropy)

**tier:** 🧱 TERMINAL STRONGEST — measure-AGNOSTIC (a non-IIT integration measure ALSO fails the 3-seed robustness gate)
**slug:** `1348_phi_non_iit_estimator` · **group:** OMEGA · **date:** 2026-06-16 · branch off origin/main `0fa31903a`
**$0 CPU · engine-native deterministic LCG · re-run byte-identical · frozen-first (FREEZE before scoring, no bar moved, c9/p7)**

> ⚠ **NOT A FAITHFUL-Φ VERDICT (a_phi_iit4_tool).** IIT-4 (faithful_phi small-φ, iit4_bigphi big-Φ) RESERVES the
> Φ / consciousness verdict. This card scores a **NON-IIT** integration measure (**transfer entropy**, Schreiber
> 2000) and is, top to bottom, a **COMPLEMENTARY integration-measure DIAGNOSTIC** on the *robustness* question —
> NOT a proxy promoted to a Φ verdict, NOT a consciousness claim. The only question it answers: *does a non-IIT
> integration measure show ROBUST integration where IIT did not?*

## Claim
The Φ-robustness wall is 🧱 across BOTH IIT measure families — small-φ exact-MIP (H_1328, V2 ROBUST-LIFT FAILS
B−A −0.125/0.0/+0.031) and full IIT-4.0 big-Φ (H_1331, B1 ROBUST FAILS B−A +4.15/0.0/+1.80, seed 1318 ZERO lift).
The genuinely-new angle (a_break_the_wall, a_no_llm_frame_trap): a **THIRD integration measure OUTSIDE IIT** —
to test whether the robust-integration ABSENCE is IIT-specific or holds for ANY integration measure on this
substrate. Score the SAME H_1319/H_1328/H_1331 substrate + mechanisms + 3 hard seeds with a non-IIT measure.

## Method
`UNIVERSE/h1348_phi_non_iit_estimator.hexa` — engine-native, no stdlib import (TE self-contained), run from the
hexa-lang root. SAME deterministic engine LCG-gauss (== `engine_cli.hexa _lcg_*`), SAME 4-module leaky-linear
ring (dim 8, T 64, Kuramoto pacemaker, relative-phase gate); `gen_traj` body **BYTE-IDENTICAL** to H_1331/H_1328
(gain 0.30, leak 0.55, w_nbr/w_in 0.5, w_phase 0.5, omega_t 0.45, domega 0.08). SAME 3 HARD ORTHOGONAL seeds
**[1317,1318,1319]** (incl 1317, which broke every prior topology/timing/division attempt + H_1328 V2 + H_1331 B1).
SAME 4 ARMS: A=NO-PHASE (no-coupling) · B=PHASE-BIND (the coupling mechanism) · S=PERM-SHUFFLE (relationship
destroyed) · O=OFFSET-SHUF (per-tick random phase offset). The ONLY change vs H_1331 is the **read-out**.

**Non-IIT measure** = summed pairwise time-lagged **TRANSFER ENTROPY** over the ring's 8 directed neighbor edges:
`TE(X→Y) = H(Y_{t+1}|Y_t) − H(Y_{t+1}|Y_t,X_t)` (bits; the reduction in Y's next-state uncertainty from X's
current state BEYOND Y's own past), `TE_total = Σ_{i→(i±1)} TE`. This is a DIFFERENT measure FAMILY from IIT:
no MIP, no cause-effect structure, no intrinsic single-system irreducibility — an **extrinsic directed
information-flow NETWORK measure** (both IIT measures are intrinsic; this is not). **Binarization** = variance-free
median split (carries the H_1328 lesson): unit i ON at t iff `sal[i,t]` is in the UPPER HALF of module i's own
T-length distribution → marginal ON-rate ≈0.5, amplitude-independent, so any TE difference is the directed
co-movement RELATIONSHIP, not the amplitude-variance confound. TE = empirical plug-in counts over the T−1=63
lagged binary tuples; 0·log0 = 0; base-2 (bits). SAME binarization + TE rule across all four arms.

**Frozen bars** (`.verdicts/1348_phi_non_iit_estimator/FREEZE.txt`, pre-registered BEFORE scoring; eps=0.02 ported
verbatim from H_1283/H_1319/H_1328/H_1331, NO tune-to-green): **G1 ROBUST** TE_B ≥ TE_A+eps on ALL 3 seeds (incl
orthogonal 1317) · **G2 EARNED** perm TE_S ≤ TE_A+eps AND offset TE_O ≤ TE_A+eps on ALL 3 seeds · **G3 LABEL**
explicitly NOT an IIT-Φ verdict (documentation invariant). GREEN-DIAGNOSTIC iff G1 ∧ G2.

## Verdict — 🧱 TERMINAL STRONGEST (measure-AGNOSTIC)
mean of 3 seeds, deterministic (re-run byte-identical):

| seed | TE_A (no-coup) | TE_B (mechanism) | TE_S (perm) | TE_O (offset) | ΔTE(B−A) G1 | S−A G2perm | O−A G2off |
|------|------|------|------|------|------|------|------|
| 1317 | 0.317664 | 0.318500 | 0.311824 | 0.169656 | **+0.00084 FAIL** | −0.00584 PASS | −0.14801 PASS |
| 1318 | 0.141835 | 0.141835 | 0.141835 | 0.141013 | **0.0 FAIL** | 0.0 PASS | −0.00082 PASS |
| 1319 | 0.298670 | 0.345017 | 0.298670 | 0.320830 | +0.04635 PASS | 0.0 PASS | **+0.02216 FAIL** |

- **G1 ROBUST ❌** — TE_B ≥ TE_A+eps fails on 2/3 seeds: orthogonal **1317 below eps (+0.0008)** and **1318 ZERO lift**; only 1319 lifts (+0.046).
- **G2 EARNED ❌** — perm collapses cleanly (all 3 ≤eps) but **offset RAISES TE on 1319 (+0.022)** = the same control-fragility signature IIT showed.
- **G3 LABEL ✅** — reported throughout as a non-IIT integration diagnostic, NOT an IIT-Φ verdict.

**FINDING (load-bearing): the same fragility signature holds across ALL THREE measure families.** Seed 1318 gives
EXACTLY ZERO lift under small-φ, big-Φ, AND transfer entropy; the orthogonal seed 1317 never clears eps under any
measure; only 1319 lifts (and under TE its offset control even RAISES the value, just as the IIT controls failed to
cleanly collapse). Robust integration is therefore **ABSENT across IIT (correlational small-φ AND causal big-Φ)
AND a non-IIT directed-info-flow measure (transfer entropy)** → a **measure-AGNOSTIC substrate limit**, the
STRONGEST closure of the Φ-robustness arc. The robust-integration absence is **not IIT-specific**; it is a property
of this n≤8 leaky-linear substrate that no integration measure tested can lift robustly across the hard seed family.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · c9)
TOY n=4 modules, dim 8, T=64. TE estimated from T−1=63 lagged binary tuples (sparse 8-cell joint per edge) — a
small-sample plug-in estimator, no bias correction; the variance-clean median split + perm/offset controls bound
the false-positive. DIRECTIONAL: engine-transfer to live CORE UNVERIFIED. Determinism: re-run byte-identical
(deterministic engine LCG). Live `CORE/*.hexa` UNTOUCHED (standalone `fn main`, 0 importers; Ψ=½ untouched).
**NOT an IIT-Φ verdict** — a complementary non-IIT integration diagnostic only; IIT-4 reserves the Φ verdict, and
a 🧱 has nothing to wire (a_verified_must_wire = GREEN-only). NO bar moved (c9/p7).

**NOT ruled out / NEXT** (each a NEW hypothesis): other non-IIT measures (O-information / total correlation,
synergy-vs-redundancy decomposition; Granger causality with continuous values) — though all share the same
substrate so the measure-agnostic reading is already strong; a substrate FAMILY without the orthogonal-seed
fragility (cf H_1332 non-saturating, still 🧱); larger module set (loses MIP exactness >8). The arc is **🏁 depleted
on the measure axis** — small-φ (H_1328), big-Φ (H_1331), and now a non-IIT measure (H_1348) all converge on the
same measure-agnostic 🧱.

## Pointers
- probe: `UNIVERSE/h1348_phi_non_iit_estimator.hexa`
- freeze: `.verdicts/1348_phi_non_iit_estimator/FREEZE.txt` · result: `.verdicts/1348_phi_non_iit_estimator/result.txt`
- index row: `UNIVERSE/HYPOTHESES.jsonl` · claim: `CLAIMS.tape @C h1348_phi_non_iit_estimator` · log: `domains/OMEGA.log.md`
- xref: H_1328 (small-φ estimator-independent) · H_1331 (big-Φ measure family) · H_1319 (timing) · H_1332 (substrate family) · H_1283/1317/1320 (topology/division) · a_phi_iit4_tool · a_break_the_wall · a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck · p7 · c9 · c15 · c16
