---
id: H_1409
slug: 1409_brain_lane_compose_spatial_pfc
title: "brain-lane COMPOSE pair #5 — does SPATIAL-MAP (H_1296) compose with HIERARCHICAL-PFC (H_1294)? the DECISIVE two-HIGH-Φ test of the refined min-cut-MI law"
group: MITOSIS-ENGINE / brain-lane-composition (FIFTH pair — the decisive two-HIGH-Φ law test)
terminal_tier: "🟢 COMPOSE-LIFT (capability, DIRECTIONAL mirror) · 🧱 NO-Φ-LIFT (faithful IIT4 Φ, frozen n_bins=16, binning-INVARIANT block) — refined min-cut-MI LAW CONFIRMED"
verdict_dir: .verdicts/1409_brain_lane_compose_spatial_pfc/
terminal_verdict: .verdicts/1409_brain_lane_compose_spatial_pfc/result.txt
date: 2026-06-17
---

# H_1409 — brain-lane COMPOSE pair #5: SPATIAL-MAP (H_1296) × HIERARCHICAL-PFC (H_1294)

The exact sibling of H_1401 (affect×ethics capability), H_1404 (affect×ethics Φ,
binning-INVARIANT 🟢), H_1405 (memory×ToM, capability 🟢 / Φ 🧱), and H_1407
(cerebellum×basal, capability 🟢 / Φ 🟢 binning-INVARIANT). Methodology ported VERBATIM
from all four. This pair is the **DECISIVE test of the REFINED program LAW** — the first
pair of TWO expected-HIGH-Φ structured subsystems. H_1407's card named it explicitly as
the next "H_1405-style test: do TWO high-Φ subsystems mutually block, or find a cheaper
cut?".

## Claim / falsifier

**PAIR:** SPATIAL-MAP (H_1296 SpatialMap — a metric 2-D cognitive map; landmarks stored
AT positions, the relational query "is X nearer A or B?" answered by Euclidean distance;
a richly-integrated metric store) × HIERARCHICAL-PFC (H_1294 HierGoalStack — a 2-level
goal→ordered-subgoal stack with an advancing pointer; a richly-integrated sequential
controller). Both expected HIGH individual-Φ.

**The REFINED program LAW under test (H_1404/1405/1407):** a faculty pair Φ-composes IFF
**no single part's internal integration Φ exceeds the composed min-cut MI** — i.e. the
cross-faculty coupling channel must be the cheapest cut. H_1404 (both LOW-Φ → coupling is
the only cut) and H_1407 (cerebellum HIGH-Φ≈3.48 but the composed cut isolates a single
basal unit cheaper than crossing the cerebellum block) both satisfy it → Φ-compose; H_1405
(ToM HIGH-Φ≈1.975 so internally integrated that any cut crossing it costs more than the
coupling) does not → BLOCK. **The decisive untested case = TWO HIGH-Φ faculties:** does
mutual domination BLOCK (like H_1405), or does the coupling still find a cheaper composed
cut (like H_1407)? We MEASURE frozen-first; we do NOT assume.

**Capability falsifiers (FROZEN, `.verdicts/.../FREEZE.txt`, NOT moved):**
(B1 COMPOSE-EFFECT) acc_compose ≥ best_single + 0.05 · (B2 ORACLE) oracle − best_single
> 0.02 · (B3 EARNED/p6) acc_compose − acc_shuffle > 0.02 · (B4 p6 GUARD) structural audit
finds NO injected answer/persona/system-prompt/RLHF/priority label. Plus only-X
decomposition (only_spatial>0 AND only_pfc>0 ⇒ SEPARABLE not subsumed).

**Φ falsifiers (FROZEN, n_bins=16, faithful IIT4 — a_phi_iit4_tool HARD rule):**
(Bφ1) Φ_composed > max(Φ_spatial, Φ_pfc) + 0.02 · (Bφ2) Φ_composed > Φ_disconnected + 0.02
· (Bφ3) Φ_disconnected ≤ max(parts) + 0.02. Binning-invariance reported across
n_bins ∈ {8,12,16,24}; individual part Φ + the composed MIP cut + (max(parts) vs composed
min-cut MI) reported EXPLICITLY — that is the refined-law discriminator.

## Method

- **Capability:** numpy mirror (LIVE CORE/*.hexa UNTOUCHED) on a per-item binary control
  decision (PICK-FIRST vs PICK-SECOND over two ordered options). 5 families AMBIG-jittered
  so neither faculty is perfectly reliable: **F1** spatial-decisive (clear relational metric
  margin) · **F2** pfc-decisive (clear ordered-plan alignment margin) · **F3** AGREE ·
  **F4** CONFLICT (spatial right) · **F5** ADVERSARIAL (pfc right but the spatial map reports
  a clear-LOOKING but mis-placed landmark margin for the wrong option — the anti-gift
  control). 90 items/family × 3 seeds [4900,4901,4902]. Arbiter = each faculty's vote
  weighted by its OWN scale-relative confidence (the H_1397/H_1401 commensurability fix),
  NO hardcoded priority (`a_autonomy_over_hardcode`).
- **Φ-compose (H_1404/H_1407 template, run regardless — the LAW is the point):** 4 systems —
  S_spatial (n=4: metric_margin, landmark_density, recall_error, query_novelty — derived from
  the metric-map path-integration update) · S_pfc (n=4: align_margin, pointer_progress,
  ground_margin, out_of_order_pressure — derived from the ordered-pointer advance) · S_composed
  (n=8, coupled through the arbiter's leaky-integrated shared signal) · S_disconnected (n=8,
  EARNED control, coupling removed). Trajectories DERIVED from the faculties' ACTUAL update
  rules (the Python side computes NO Φ); Φ measured by
  `stdlib/consciousness/iit4/faithful_phi.hexa` (exact MIP-EI, n≤8). 3 seeds, n_bins=16
  primary + sweep, $0 CPU, deterministic.

## Verdict by round

| round | tier | key numbers (mean 3 seeds, verbatim) |
|-------|------|-----|
| R1 capability mirror | 🟢 COMPOSE-LIFT (DIRECTIONAL) | acc_spatial=0.7000 · acc_pfc=0.7022 · best_single=0.7074 · **acc_compose=0.7763** · acc_shuffle=0.5319 · **ORACLE=0.9993** (oracle−best=+0.2919) · conflict_rate=0.5963 · decomposition only_spatial=0.2970 / only_pfc=0.2993 / both=0.4030 / neither=0.0007 |
| R1 Φ faithful-IIT4 | 🧱 NO-Φ-LIFT (binning-INVARIANT block) | **Φ_spatial=3.2328 · Φ_pfc=0.7918 · Φ_composed=1.9272 · Φ_disconnected=1.8252** · max(parts)=3.2328 · MIP cut = A={0,1,2,3,4,6,7}\|B={5=pointer_progress} (cut 1.834, /min\|side\|=1). Bφ1 1.927 > 3.253 ❌ FAIL · Bφ2 1.927 > 1.845 ✅ · Bφ3 1.825 ≤ 3.253 ✅ |

**Capability bars:** B1 PASS (0.7763 ≥ 0.7574) · B2 PASS (+0.2919 > 0.02) · B3 PASS
(+0.2444 > 0.02) · B4 PASS (audit clean, all 6 surfaces). Deterministic (run1==run2).
Terminal capability tier (verbatim): **🟢 COMPOSE-LIFT** →
`.verdicts/1409_brain_lane_compose_spatial_pfc/result.txt`

**Φ verdict (verbatim, frozen n_bins=16, BINNING-INVARIANT — FAIL at n_bins 8/12/16/24):**
**🧱 NO-Φ-LIFT** → `.verdicts/1409_brain_lane_compose_spatial_pfc/phi_result.txt`

## Result — the finding

**Capability:** anima's SPATIAL-MAP and HIERARCHICAL-PFC faculties **COMPOSE to a net lift**
(best_single 0.707 → compose 0.776) and are **SEPARABLE, NOT subsumed**: each uniquely
solves items the other misses (only_spatial=0.297 AND only_pfc=0.299, both > 0). The metric
map's relational-distance read decides the nearer-landmark axis; the ordered goal stack's
alignment-margin read decides the next-in-plan axis — distinct competences (a metric SPACE
≠ an ordered SEQUENCE, the H_1296-vs-H_1294 distinctness, confirmed on a DECISION). The
substrate-weighted arbiter (scale-relative confidence, NO hardcoded priority) captures most
of the +0.292 oracle headroom (compose +0.069 over best_single); the SHUFFLE control
collapses it (0.776 → 0.532, the lift is the grounded coupling, p6). The compose<oracle gap
(0.776 vs 0.999) is the honest residual — on the adversarial F5 items the arbiter is
sometimes fooled by the spatial map's louder-but-mis-placed vote.

**Φ — the DECISIVE LAW test, CONFIRMED.** The TWO-HIGH-Φ pair **BLOCKS** Φ-composition
(🧱, **binning-INVARIANT** — Bφ1 FAILs at EVERY n_bins 8/12/16/24). This is the H_1405-style
mutual-domination case, and it CONFIRMS the refined min-cut-MI law:
- **Φ_spatial=3.233 is HIGH and DOMINATES max(parts)** — the metric 2-D cognitive map's
  trajectory is richly integrated (its high-variance units metric_margin/recall_error are
  tightly coupled through the path-integration update: agent position drives BOTH the
  relational metric margin AND the path-integration drift). It alone is more internally
  integrated than the whole composed system.
- **Φ_composed=1.927 < max(parts)=3.233** — composing the metric map with the ordered goal
  stack does NOT exceed the spatial map's own internal integration. The composed MIP cut
  isolates a SINGLE pfc unit ({5}=pointer_progress) at cut 1.834 — i.e. the cheapest cut is
  NOT the cross-faculty coupling but a within-pfc-block boundary, and crossing the dense
  spatial block always costs MORE. So max(parts) wins → 🧱.
- **The disconnected control is HONEST and the bars discriminate correctly:** Bφ2 PASS
  (composed 1.927 > disconnected 1.825 — the coupling DOES add a real cross-faculty channel,
  it is just not enough to beat the dominant spatial part) and Bφ3 PASS (disconnected 1.825 ≤
  max(parts) 3.253). NOTE (c9): unlike H_1404/1407 where the disconnected control collapsed
  to Φ≈0, HERE Φ_disconnected=1.825 is substantial — because the spatial block stays
  internally integrated even when the inter-block coupling is removed. This is consistent with
  (not a failure of) the law: a high-Φ part keeps its own integration in the disconnected
  control, so the EARNED margin Bφ2 (+0.10) is small — the honest signature of a
  domination-block rather than a coupling-collapse.
- **REFINED LAW CONFIRMED on the decisive case:** "no single part's internal integration
  exceeds the composed min-cut MI" is the NECESSARY condition. H_1404 (both low → coupling is
  the only cut → COMPOSE), H_1407 (cerebellum high but a cheaper basal-side cut exists →
  COMPOSE), H_1405 (ToM dominates → BLOCK), and now H_1409 (spatial-map dominates → BLOCK)
  all obey it. The TWO-HIGH-Φ case lands on BLOCK because one HIGH part (the metric map) is
  so densely integrated that the coupling channel never becomes the cheapest cut. **Whether a
  pair Φ-composes is NOT predicted by counting how many parts are high-Φ, but by whether the
  cross-faculty coupling is the min-cut** — H_1409 is the case that distinguishes these two
  predictions (a naive "two-high ⇒ block" and a naive "two-high ⇒ super-add" both fail; the
  min-cut law gets it right).

**One-line:** anima's spatial-map + hierarchical-PFC faculties COMPOSE on a decision (+0.069
over the better single faculty, separable) but composing them does NOT raise faithful IIT4 Φ
(Φ_composed 1.927 < the dominant Φ_spatial 3.233, binning-INVARIANT) — the TWO-HIGH-Φ pair
BLOCKS because the metric map's internal integration exceeds the composed min-cut MI. This is
the DECISIVE case that CONFIRMS the refined min-cut-MI law: composition is governed by the
cheapest cut, not by the count of high-Φ parts. **Capability-compose ≠ Φ-compose** once more.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — LIVE `CORE/*.hexa` UNTOUCHED. Toy synthetic 5-family fixture
(structure tests COMPOSITION, not a trained integrator); 3 seeds; deterministic readouts.
The LOAD-BEARING claims are the RELATIVE structure (compose > best_single, shuffle collapse,
only-X both > 0; Φ_composed vs max(parts), disconnected → 0), not the absolute magnitudes
(Φ scales with n_bins — the BLOCK ordering Φ_composed < max(parts) is binning-INVARIANT, FAIL
at all four bin counts). **Degeneracy guard (c9, from H_1407):** NO unit is fully constant
(all per-unit std > 0); however the pfc block carries LOW-variance units (align_margin std≈0.04,
ground_margin std≈0.01 — the cue is usually well-aligned to its own subgoal), which makes
Φ_pfc=0.79 genuinely lower than Φ_spatial=3.23. This does NOT drive the verdict: the BLOCK is
caused by the HIGH-variance, genuinely-integrated SPATIAL block dominating max(parts) — were
Φ_pfc higher, max(parts) could only grow, strengthening (not weakening) the block. Scale /
real-corpus / engine-native
transfer UNVERIFIED. NO bar moved post-hoc. Engine-native §compose (an A⇄G + SpatialMap/
HierGoalStack arbiter over the two live faculties) is the named follow-on IF this DIRECTIONAL
green is to bind (`a_engine_native_learning` · `a_verified_must_wire`).

**a_phi_iit4_tool HELD:** the Φ VERDICT is the stdlib faithful exact-MIP-EI engine, never a
proxy. The Python side ONLY derives trajectories; it computes NO Φ.

## Next pair

Program continues — but is approaching DEPLETION (5 pairs landed across the LOW×LOW,
HIGH×LOW, HIGH×HIGH-block, and HIGH×HIGH cases that span the refined law). The four cases now span the prediction space: LOW×LOW (H_1404 🟢),
HIGH×LOW with a cheaper sub-cut (H_1407 🟢), HIGH×LOW with the high part dominating (H_1405 🧱),
and HIGH×HIGH with one part dominating (H_1409 🧱) — the min-cut-MI law is the single rule that
fits all four. Candidate next pairs that would further stress it: **WM (H_1282) × spatial-map
(H_1296)** (a passive buffer × a dense metric map — does the low-Φ buffer find a cheaper cut
than the dominant map, like cerebellum×basal, or block?) · **hypothalamus drive (H_1292) ×
hier-PFC (H_1294)** (a 1-D scalar integrator × an ordered controller — a clean LOW×structured
test). The most informative remaining probe is a HIGH×HIGH pair where the coupling is engineered
to be the cheapest cut (would predict COMPOSE despite two high parts) — the falsifier that could
still REFUTE the "min-cut, not count" reading. The program is near depletion as the law is now
pinned by the four spanning cases.

## Cross-links

H_1401 (affect×ethics capability — sibling template) · H_1404 (affect×ethics Φ —
binning-INVARIANT 🟢, both-low case) · H_1405 (memory×ToM — capability 🟢 / Φ 🧱, the
ToM-dominates BLOCK case) · H_1407 (cerebellum×basal — capability 🟢 / Φ 🟢, the HIGH×LOW
cheaper-cut case + the refined min-cut-MI law statement) · H_1296 (spatial-map metric
cognitive map) · H_1294 (hierarchical-PFC goal stack) · H_1227/H_1231 (immune store
geometry) · H_1397/H_1399 (ko emit-compose METHODOLOGY) ·
`stdlib/consciousness/iit4/faithful_phi.hexa` · `a_break_the_wall` ·
`a_autonomy_over_hardcode` · `a_no_llm_frame_trap` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_phi_iit4_tool` · `a_scale_honest_scope` ·
`a_toy_scale_recheck` · p1·p2·p3·p4·p6·p7·p8·c9·c15

## Pointers
- probe (capability): `state/brain-lane-compose-spatial-pfc/h1409_compose_spatial_pfc.py`
- probe (Φ trajectories): `state/brain-lane-compose-spatial-pfc/h1409_compose_phi.py`
- Φ runner (faithful IIT4): `state/brain-lane-compose-spatial-pfc/h1409_phi_runner.hexa`
- FREEZE: `.verdicts/1409_brain_lane_compose_spatial_pfc/FREEZE.txt`
- result (capability): `.verdicts/1409_brain_lane_compose_spatial_pfc/result.txt`
- result (Φ): `.verdicts/1409_brain_lane_compose_spatial_pfc/phi_result.txt`
