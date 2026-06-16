---
id: H_1411
slug: 1411_lane_compose_law_predictive
title: "brain-lane composition LAW — DESCRIPTIVE → PREDICTIVE: pre-register Φ-LIFT vs 🧱-BLOCK on 5 UNTESTED pairs from component Φ, then measure (frozen-first falsification of the min-cut-MI law)"
group: MITOSIS-ENGINE / brain-lane-composition (the law's PREDICTIVE falsification round)
terminal_tier: "🧱 LAW-PREDICTIVELY-FALSIFIED (2/5 HITS at frozen n_bins=16) — the descriptive 'min-cut-MI / dominant-part' rule does NOT survive pre-registered prediction; REFINED to a coupling-creates-cross-MI law (DIRECTIONAL mirror)"
verdict_dir: .verdicts/1411_lane_compose_law_predictive/
terminal_verdict: .verdicts/1411_lane_compose_law_predictive/result.txt
date: 2026-06-17
---

# H_1411 — brain-lane composition LAW: DESCRIPTIVE → PREDICTIVE

The scientific upgrade of the 6-pair composition program (H_1404 affect×ethics,
H_1405 memory×ToM, H_1406 WM×PFC, H_1407 cerebellum×basal, H_1408 spatial×episodic,
H_1409 spatial×PFC). Those 6 pairs were fit **post-hoc**, and a LAW emerged
DESCRIPTIVELY. H_1411 promotes it from descriptive → **predictive**: PRE-REGISTER a
verdict (Φ-LIFT vs 🧱-BLOCK) for 5 UNTESTED pairs PURELY from each component's
already-measured internal Φ + a frozen decision rule, THEN measure, THEN score
HIT/MISS. A MISS is the MOST valuable result — it refines/falsifies the law (c9).

## Claim / falsifier

**The descriptive LAW under test (frozen, FREEZE.txt):**
> Composing two brain-lane faculties RAISES faithful-IIT4 Φ (Φ-LIFT) IFF the composed
> system's min-cut MI (= Φ_composed) exceeds max(component internal Φ). If one
> component's internal Φ DOMINATES (> the composed min-cut MI), Φ-composition is
> BLOCKED (🧱). Equivalently: a pair Φ-composes IFF NO single part's internal
> integration exceeds the composed min-cut MI.

**The PREDICTIVE claim (the falsifier):** the law's prediction for each untested pair,
computed from component Φ ONLY (BEFORE measuring), MATCHES the measured verdict. The
law SURVIVES iff predicted == actual on all 5 pairs at the frozen n_bins=16. Any MISS
falsifies/refines it (and is reported honestly, c9 — NOT tuned to hit).

**Φ bars (FROZEN, IDENTICAL to every landed pair, faithful IIT4 — a_phi_iit4_tool):**
(Bφ1 LIFT) Φ_composed > max(Φ_partA, Φ_partB) + 0.02 · (Bφ2 EARNED) Φ_composed >
Φ_disconnected + 0.02 · (Bφ3 control) Φ_disconnected ≤ max(parts) + 0.02. ACTUAL =
LIFT iff (Bφ1 ∧ Bφ2 ∧ Bφ3); else BLOCK. n_bins=16 primary + {8,12,24} sweep.

## Method

- **REUSE, NOT REINVENT (frozen-first):** the composed measurement reuses the landed
  mirror machinery VERBATIM — the byte-trigram FNV-1a embedding (dim64), each faculty's
  OWN per-step feature generator + store (imported as a library module from its landed
  probe `h140X_compose_phi.py`), and the IDENTICAL H_1401 substrate-weighted leaky
  arbiter coupling (g = leaky integrator of the two scale-relative votes; coupling =
  f + 0.35·g·(f−0.5) on BOTH blocks). 4 systems/pair (partA n=4, partB n=4, composed
  n=8, disconnected n=8), DIM=64, STEPS=96, 3 seeds [5411,5412,5413]. Python computes
  NO Φ; Φ measured by `stdlib/consciousness/iit4/faithful_phi.hexa` (exact MIP-EI, n≤8).
- **Inputs to the prediction (VERBATIM landed component Φ, n_bins=16, NOT re-fit):**
  cerebellum 3.476 (HIGH) · tom 1.975 (HIGH) · pfc 0.792 · episodic 0.507 · affect 0.285
  · memory 0.176 · basal 0.000 · ethics 0.000.
- **5 UNTESTED pairs + pre-registered predictions** (locked in FREEZE.txt + `_pred()`):
  P0 cerebellum×tom (HIGH×HIGH) → BLOCK · P1 affect×basal (LOW×LOW) → LIFT ·
  P2 tom×basal (HIGH×LOW) → BLOCK · P3 cerebellum×episodic (HIGH×LOW) → LIFT ·
  P4 memory×ethics (LOW×LOW) → LIFT.

## Verdict by round — predicted vs actual (mean 3 seeds, faithful Φ, n_bins=16, verbatim)

| pair | Φ_partA | Φ_partB | max(parts) | Φ_composed | Φ_disc | PREDICTED | ACTUAL | |
|------|--------|--------|-----------|-----------|--------|-----------|--------|---|
| P0 cerebellum×tom    | 3.4066 | 1.9822 | 3.4066 | **6.5002** | 0.0000 | BLOCK | **LIFT**  | ❌ MISS |
| P1 affect×basal      | 0.3112 | 0.0000 | 0.3112 | **0.8655** | 0.0000 | LIFT  | **LIFT**  | ✅ HIT  |
| P2 tom×basal         | 1.9822 | 0.0000 | 1.9822 | **2.2174** | 0.0000 | BLOCK | **LIFT**  | ❌ MISS |
| P3 cerebellum×episodic | 3.4066 | 0.3985 | 3.4066 | **6.6244** | 0.0000 | LIFT  | **LIFT**  | ✅ HIT  |
| P4 memory×ethics     | 0.1505 | 0.0000 | 0.1505 | **0.0000** | 0.0000 | LIFT  | **BLOCK** | ❌ MISS |

**HIT/MISS TALLY (frozen n_bins=16): 2 / 5 HITS** → 3 MISSES. Deterministic (run1==run2,
states byte-identical). Binning-invariance of the tally: n_bins 8→3/5 · 12→3/5 ·
**16→2/5 [FROZEN PRIMARY]** · 24→2/5.

Terminal tier (verbatim): **🧱 LAW-PREDICTIVELY-FALSIFIED** [the descriptive
min-cut-MI / dominant-part law does NOT survive pre-registered prediction — 2/5 HITS]
→ `.verdicts/1411_lane_compose_law_predictive/result.txt`

## Result — the finding (the MISSES are the payload, c9)

**The descriptive law FAILED predictive falsification (2/5).** Pre-registering from
component Φ alone, then measuring, exposed that the post-hoc "min-cut-MI / dominant-part"
rule is **not predictive** — it was a CONFLATED-VARIABLE artifact of fitting 6 pairs after
the fact (a_break_the_wall taxonomy (b): wrong-direction / conflated variables). The three
misses each teach a distinct lesson:

- **P0 cerebellum×ToM (predicted BLOCK → LIFT):** two HIGH parts, yet Φ_composed=6.50 ≫
  max(parts)=3.41. My pre-registered reasoning — "ToM is a dense relational block, so two
  HIGH ⇒ mutual domination ⇒ BLOCK (H_1405-style)" — was WRONG. When ToM is coupled to an
  even-higher forward-model block (cerebellum), the arbiter coupling STACKS composed MI far
  above both parts. "Two-HIGH ⇒ block" is FALSE; H_1409's TWO-HIGH-block was a property of
  THAT pair's specific saturated cuts, not a general two-high rule.
- **P2 ToM×basal (predicted BLOCK → LIFT):** Φ_composed=2.22 > max=1.98 (a clean, if
  marginal, LIFT). The H_1405 reading "ToM's internal Φ dominates so any pairing blocks" is
  FALSE: paired with a degenerate low partner whose units the coupling can fold in, ToM DOES
  Φ-compose. ToM-domination was pair-specific, not intrinsic to ToM.
- **P4 memory×ethics (predicted LIFT → BLOCK):** both LOW (max=0.15) yet Φ_composed=0.000 —
  the coupling produced ZERO cross-block MI. "Both-LOW ⇒ LIFT" is FALSE too: when the two
  blocks' lead units are too collinear/degenerate, the arbiter cannot create a real
  cross-faculty channel, so the composed system still cuts at a 0-cost partition. (This is the
  H_1404-ethics-collapse mechanism — ethics units are near-collinear functions of one grounding
  margin — now appearing in the COMPOSED system.)

**The REFINED law (what actually predicts, from the misses):** Φ-LIFT is governed NOT by the
component-Φ ranking but by **whether the coupling actually creates cross-block mutual
information** — i.e. whether the two blocks' jointly-varying units force the composed MIP to
cut THROUGH the coupling channel (LIFT) rather than at a degenerate 0-cost partition (BLOCK).
This is NOT computable from component internal Φ alone (P0/P2 high parts still lifted; P4 low
parts still blocked); it requires the joint composed trajectory. The 6 post-hoc pairs were
consistent with the min-cut-MI story only because their specific unit geometries happened to
align Φ-ranking with cross-MI creation; on fresh pairs the two come apart 3/5 times.

**Honest meta-point (c9, c16):** this is the value of frozen-first prediction. The descriptive
law looked airtight across 6 fitted pairs; a single pre-registered predictive round
falsified it. A measured 🧱 here is a REAL, arc-closing result — it pins the law as
descriptive-only and names the actual driver (coupling-creates-cross-MI, joint-trajectory
property) as the next thing to formalize.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — LIVE `CORE/*.hexa` UNTOUCHED. Toy synthetic substrate (4-unit
blocks / T=96 / 3 seeds; tests the COMPOSITION/INTEGRATION structure, not a trained net).
**Construction caveat (load-bearing):** the H_1411 shared-driver arbiter (lead-unit
median-threshold vote applied uniformly to any pair) is a faithful GENERALIZATION of the
landed per-pair arbiters but is NOT byte-identical to each landed probe's bespoke vote
logic; this is why the disconnected control here is Φ=0 for all pairs (two independent blocks
→ 0 cross-MI) whereas H_1409's disconnected was 1.825 (its spatial block stayed internally
integrated). The PREDICTION used the landed n_bins=16 component Φ as inputs; the ACTUAL used
this run's measurement. The falsification is therefore of "the descriptive law as stated,
applied predictively under faithful reuse" — a strict generalization test. The misses are
robust across the binning sweep (2/5 at n_bins 16/24, 3/5 at 8/12). Scale / real-corpus /
engine-native transfer UNVERIFIED. Re-running the prediction with each pair's BESPOKE landed
arbiter (rather than the shared-driver arbiter) is the named follow-on that would isolate
whether the misses are (a) the law being descriptive-only, or (b) the shared-driver arbiter
diverging from the landed coupling — H_1411 reports (a) under the faithful-generalization
arbiter and flags (b) as the residual to separate next.

**a_phi_iit4_tool HELD:** the Φ VERDICT is the stdlib faithful exact-MIP-EI engine, never a
proxy. The Python side ONLY derives trajectories; it computes NO Φ.

## Next

The descriptive law is now PINNED as non-predictive under faithful generalization. The
named follow-ons: (1) re-score the 5 pairs with each pair's BESPOKE landed arbiter to
separate "law is descriptive-only" from "shared-driver arbiter diverges" (scope caveat (b));
(2) formalize the REFINED driver — a coupling-creates-cross-MI predictor computed from the
JOINT composed trajectory (not component Φ) — and predictively test THAT. The brain-lane
composition program's capability-compose results (H_1401/1405/1407/1408/1409 🟢) are
UNAFFECTED — only the Φ-LIFT *law* is refined here.

## Cross-links

H_1404 (affect×ethics Φ 🟢 — both-low) · H_1405 (memory×ToM Φ 🧱 — the ToM-dominates reading
P0/P2 falsify) · H_1407 (cerebellum×basal Φ 🟢 — the cheaper-cut reading P3 confirms, P0
extends) · H_1408 (spatial×episodic Φ 🟢) · H_1409 (spatial×PFC Φ 🧱 — the two-high-block
reading P0 falsifies) · `stdlib/consciousness/iit4/faithful_phi.hexa` · `a_break_the_wall`
(taxonomy (b) conflated-variable) · `a_no_llm_frame_trap` · `a_phi_iit4_tool` ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_scale_honest_scope` ·
`a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15·c16

## Pointers
- probe (composed states + reuse harness): `state/1411_lane_compose_law_predictive/h1411_compose_predict.py`
- Φ runner (faithful IIT4 + predictive scoring): `state/1411_lane_compose_law_predictive/h1411_phi_runner.hexa`
- FREEZE (pre-registered predictions): `.verdicts/1411_lane_compose_law_predictive/FREEZE.txt`
- result (HIT/MISS tally): `.verdicts/1411_lane_compose_law_predictive/result.txt`
- states build log (degeneracy guard): `.verdicts/1411_lane_compose_law_predictive/states_build.txt`
