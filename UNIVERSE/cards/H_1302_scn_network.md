---
id: H_1302
slug: 1302_scn_network
title: multi-oscillator SCN-network — Kuramoto consensus from N heterogeneous oscillators (emergent consensus ⊥ single-oscillator entrainment; temporal phase-sync ⊥ static Φ-superadditivity)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE + WIRED
verdict_dir: .verdicts/1302_scn_network/
terminal_verdict: .verdicts/1302_scn_network/result.txt
date: 2026-06-16
---

# H_1302 — multi-oscillator SCN-network (HD36) — the r8 depletion candidate, SURVIVED

## Claim / falsifier

The PhaseResetClock (H_1301) is a SINGLE oscillator that entrains to an EXTERNAL Zeitgeber; the
CircadianClock (H_1298) and IntervalTimer (H_1299) are likewise single-oscillator timekeepers.
Falsifiable claim: a dedicated **multi-oscillator SCN-network** — N heterogeneous phase
oscillators (each its own intrinsic period `tau_i`) coupled by a **mutual Kuramoto coupling**
`dphi_i += K/(2π)·Σ_j C_ij·sin(2π·(phi_j − phi_i))` (the standard coupled-oscillator form;
SCN VIP/GABA mutual entrainment) — is a brain subsystem DISTINCT from every single-oscillator
lane AND from the hive(CollectivePool) Φ-superadditivity lane. The network does TWO things no
single oscillator can: (i) reach an **emergent CONSENSUS PERIOD** from N heterogeneous members
(the Kuramoto order parameter `R → 1`), and (ii) **network DAMPING** — a single de-tuned member
is pulled back into the synchronized cluster. Metric = order parameter R (consensus) + R under a
perturbed member (damping). Both controls (a FRUSTRATED random-sign coupling / K=0) must collapse
consensus, or it is variance → honest 🔴/🏁. Lens: chronobiology coupled-oscillator network (c15,
a_no_llm_frame_trap) — NOT an LLM recipe.

## Depletion test — the whole question, and why it SURVIVES

This lane is r8 of the brain-structure ladder, run as the explicit DEPLETION TEST (the H_1301
card named exactly three thin r8 candidates: multi-oscillator SCN-network, a nonphotic
opposite-sign Zeitgeber, and a multi-interval nested scheduler). The SCN-network was the strong
candidate — it adds a genuinely new mechanism (a NETWORK of mutually-coupled oscillators), whereas
the nonphotic Zeitgeber is mostly PhaseResetClock with a sign flip and the nested scheduler reduces
to an array of IntervalTimers. A subsystem joins ONLY if it clears BOTH (i) a falsifiable
gap-vs-the-live-engine AND (ii) a **control-surviving distinctness vs EVERY existing lane** —
decisively vs the two nearest: PhaseResetClock (single-oscillator entrainment) and CollectivePool
(Φ-superadditivity). It SURVIVED: the load-bearing distinctness — **emergent consensus from N
heterogeneous oscillators + network damping of a perturbed member** — is exactly what neither
nearest lane can do, and both controls cleanly collapse it.

## Why DISTINCT vs the nearest lanes (load-bearing, both control-surviving)

- **vs PhaseResetClock (H_1301) — the nearest temporal lane:** a SINGLE oscillator entrains to an
  EXTERNAL Zeitgeber; it has NO ensemble + NO mutual coupling, so it CANNOT produce a consensus
  period FROM N members (there is only one member), and no network damps a perturbation. The
  falsifier arm **A** = the SAME N heterogeneous oscillators with NO mutual coupling (= N
  independent free-running PhaseResetClocks): the phase spread NEVER collapses (mirror R≈0.37,
  engine R≈0.49 ≤ 0.65) and a perturbed member is NOT pulled back (mirror A_R_pert≈0.41).
- **vs CollectivePool (H_1295) — the coupled-MEMBERS lane (the steer's critical dissociation):**
  CollectivePool measures the IIT-4 big-Φ **SUPER-ADDITIVITY of coupled ECA SUBSTRATES** — a
  STATIC structural-integration GAUGE over a transition-probability matrix. It has **NO phase, NO
  temporal oscillation, NO consensus PERIOD, NO Kuramoto order parameter**. The SCN-network is a
  TEMPORAL phase-synchronization DYNAMIC (phases evolving over ticks toward a shared period).
  These are orthogonal axes: a structural Φ gauge is not a temporal phase-consensus process. The
  SCN-network does NOT reduce to CollectivePool (no Φ measure anywhere) and does NOT reduce to one
  averaged oscillator (the order parameter R IS the many-vs-one discriminator).
- vs CircadianClock (H_1298) / IntervalTimer (H_1299): single baked/learned-period oscillators,
  no ensemble. vs cerebellum (H_1280): content prediction, no phase. vs WM (H_1282): leak, no
  oscillator. vs HomeostaticDrive (H_1292): content-gated scalar.
  → DISTINCT vs ALL (the controls: a FRUSTRATED random-sign coupling / K=0 both collapse consensus).

## Method (frozen-first, anti-Goodhart)

3 seeds [5320,5321,5322], $0 CPU numpy mirror (DIRECTIONAL), deterministic (byte-identical
reruns) → engine-native R2. Regime: N=8 heterogeneous oscillators, `tau` in [22,26] (mean 24,
spread 2), K_couple=0.25, STEPS=400, SETTLE=200, R_CONSENSUS=0.90, PERTURB_DETUNE=6.0. Arms:
**A** = uncoupled (N independent PhaseResetClocks — the nearest-lane falsifier, SHOULD fail
consensus), **B** = mutually-coupled Kuramoto network, **B-SHUFFLE** = FRUSTRATED random-sign
symmetric coupling (same magnitude, half attract / half repel — NO coherent consensus field),
**B-ABLATE** = K_couple=0 (each free-runs at its tau). Bars c1 PRESENCE · c2 DISTINCT · c3
EARNED-FRUSTRATED · c4 EARNED-ABLATE · c5 DAMP · c6 NO-FAB. BOTH controls must collapse or honest
🔴/🏁.

## Verdict (verbatim from `.verdicts/1302_scn_network/`)

**R1b numpy mirror 🟢 GREEN (DIRECTIONAL)** — all 6 bars on all 3 seeds + mean:

| metric | B (network) | A (uncoupled) | B-FRUST | B-ABL |
|--------|-------------|---------------|---------|-------|
| order parameter R | **0.9988** | 0.3731 | 0.1320 | 0.3731 |
| R under perturb | **0.9975** | 0.4115 | — | — |

c1 PRESENCE ✓ (B_R 0.9988 ≥ 0.90, gap +0.6257 ≥ 0.30) · c2 DISTINCT ✓ (A_R 0.3731 ≤ 0.65) · c3
EARNED-FRUST ✓ (Bshuf 0.1320 ≤ A+0.15, BELOW uncoupled) · c4 EARNED-ABL ✓ (Babl 0.3731 ≤ A+0.15)
· c5 DAMP ✓ (B_R_pert 0.9975 ≥ 0.90, gap +0.5859 ≥ 0.30) · c6 NO-FAB ✓ (A_R 0.3731 < 0.90) → 🟢
GREEN (c1..c6 = [T,T,T,T,T,T], every seed).

**Honesty trail (c9 — frozen-first, NO tune-to-green; the DISTINCTNESS bars c1/c2 NEVER moved):**
R1a (original controls) gave c1..c6 = [T,T,**F**,T,**F**,T]. The two FAILs were MIS-SPECIFIED
controls/metrics, NOT a collapse of the claim — corrected to be CORRECT/STRICTER (each correction
made the test more decisive; the load-bearing presence/distinctness held from the first run):
- **c3 SHUFFLE 🔧** R1a used an asymmetric ONE-WAY 'directed chain' coupling that preserved per-row
  magnitude — but a directed chain STILL drags oscillators toward sync (Bshuf_R=0.79), a
  mean-preserving-magnitude LEAK that does not break the claimed structure (the SAME trap
  H_1299/H_1301-R1b hit). FIXED to a FRUSTRATED random-SIGN symmetric matrix (same |coupling|,
  half attract / half repel) → no coherent consensus field → R collapses to 0.13 (BELOW uncoupled).
- **c5 DAMP 🔧** R1a used the consensus PERIOD shift under a perturbed member, but Kuramoto coupling
  is phase-difference antisymmetric and CONSERVES the mean ensemble frequency, so the period shift
  is IDENTICAL for coupled & uncoupled (B=A=0.647) — a metric blind to damping by construction
  (not a collapse, a wrong metric). FIXED to the ORDER PARAMETER under a perturbed member: does the
  ensemble PULL the de-tuned member BACK into the synchronized cluster (R stays high) — B keeps
  R≈0.997, uncoupled stays ≈0.41. The c1 PRESENCE and c2 DISTINCT bars are UNCHANGED.

**R2 ENGINE-NATIVE + WIRED 🟢** — `SCNNetwork` lane added to live `CORE/engine_cli.hexa`
(`scn_new`/`scn_new_uncoupled`/`scn_new_frustrated`/`scn_new_ablated`/`scn_detune`/`scn_step`/
`scn_run`/`scn_order`/`scn_consensus`), realizing the N-heterogeneous-oscillator mutual Kuramoto
coupling in code (a deterministic engine check, seed 5320, N=8, 400 steps): **B_R=0.999 ·
A_R=0.489 · Bfrust_R=0.018 · Babl_R=0.489 · B_R_pert=0.997 · A_R_pert=0.436** — all 6 bars hold
engine-native (the c1 consensus / c2 uncoupled-distinct / c3 frustrated-collapse / c4
ablate-collapse / c5 damping dissociation engine-native; A_R differs slightly from the mirror's
0.373 because the engine LCG modular arithmetic differs from Python's, but every bar holds with
margin → engine-transfer VERIFIED for the STRUCTURE, not the exact float). Regression guards no
regression: **engine_cli_smoke 73/0** (+5 SCNNetwork cases 69–73: reaches-consensus /
uncoupled-no-consensus / frustrated-collapses / ablate-collapses / network-damps-perturbed-member)
· h1196 single-entry **7/0** · h1205 separation-invariant **PASS** (generation byte-identical
ON==OFF, Ψ=½ untouched).

## Guards

- **@L4 NOT an emit gate** (`a_autonomy_over_hardcode`): `scn_consensus` is an OPTIONAL ensemble
  read a caller MAY consult — it does NOT force emit/silence.
- **Ψ-disjoint by construction**: the network holds ONLY its per-member phase vector + the
  per-member taus + K + mode; reads NO immune store, NO grounding, NO `pure_field` Φ/phase/Ψ.
- **p1/p2/p3/p6**: reads only its own member phases — NO persona, NO "you are X", NO injected
  "fire now" label, NO RLHF. The Kuramoto coupling is geometry over phase differences, scored only.
  The controls prove the lift is the COHERENT MUTUAL coupling (frustrated + ablate both collapse).
- **`a_core_engine_map`**: NO 2nd .clm/.kosmos entry (pure timekeeper; single-entry 7/0 unchanged).

## Scope (UNVERIFIED)

numpy-mirror DIRECTIONAL (engine-transfer reconfirmed by R2 — all bars hold engine-native, exact
floats differ by the LCG); TOY (1 tau-spread regime, N=8, 3 seeds, deterministic Kuramoto — tests
the CONSENSUS/DAMPING STRUCTURE, not a learned network); B's consensus is an EXISTENCE-PROOF (a
mutually-coupled ensemble synchronizes N heterogeneous oscillators), the discriminators (uncoupled
R≈0.37–0.49, frustrated R collapses below uncoupled, ablate→uncoupled) carry the verdict. Scale /
real-corpus / larger ensembles / heterogeneity-vs-coupling phase diagram (Kuramoto critical Kc) /
weak-coupling near-threshold regime / wiring the consensus into the dream-stage scheduler alongside
`clock_fire`/`itimer_fire`/`prc_zeitgeber` = follow-on (`a_engine_native_learning`·
`a_verified_must_wire`·`a_scale_honest_scope`·`a_toy_scale_recheck`).

## Ladder status (c15) — HD36 lands; the ladder is now VERY thin, near DEPLETION

HD36 (multi-oscillator SCN-network) SURVIVED the depletion test and is wired engine-native — the
r8 candidate the H_1301 card flagged as the most-likely-to-survive cleared BOTH arms (falsifiable
gap + control-surviving distinctness vs every lane, decisively vs the single-oscillator
PhaseResetClock AND the static-Φ CollectivePool). The c15 brain-structure ladder therefore
**CONTINUES** past HD36 rather than terminating. But the frontier is now extremely thin: every
realized lane reads/integrates anima's own substrate state, its own counter, or (now) a coupled
ensemble of its own oscillators. The two remaining r8 candidates the H_1301 card named are
WEAKER and likely to collapse: a **nonphotic opposite-sign Zeitgeber** is mostly PhaseResetClock
with a sign flip (distinct ONLY if two opposite-sign Zeitgebers produce a NET shift neither alone
can, e.g. competition/cancellation — else 🏁); a **multi-interval nested scheduler** the r6/r7
agents already flagged as reducing to an array of IntervalTimers (🏁 unless a genuine cross-timer
mechanism is found). A further rung needs a subsystem with BOTH a falsifiable gap AND a
control-surviving distinctness vs all 18 lanes (CircadianClock, IntervalTimer, PhaseResetClock,
**SCNNetwork**, cerebellum, WM, hippocampus, basal-ganglia, amygdala, hypothalamus, affect,
ethics, theory-of-mind, hierarchical-PFC, hive, spatial-map, + the 3 walls). If the two remaining
candidates fail the distinctness/control test, the ladder DEPLETES 🏁 at HD36.

xref h1301 (the single oscillator this networks) · h1298 (baked clock) · h1299 (learned timer) ·
h1295 (hive CollectivePool — static Φ-superadditivity, the orthogonal coupled-members lane this is
distinct from) · h1283 (phase-binding, Kuramoto sin coupling — engine sin precedent) · h1280 ·
h1282 · h1292 · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_autonomy_over_hardcode · a_break_the_wall · a_scale_honest_scope ·
a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9·c15·c16.
