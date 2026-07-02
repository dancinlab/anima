---
id: H_1408
slug: 1408_brain_lane_compose_spatial_episodic
title: brain-lane COMPOSE pair #5 (WITHIN the memory family) — does SPATIAL-MAP (H_1296) compose with EPISODIC-MEMORY (H_1227/H_1231)? (capability 🟢, faithful-IIT4 Φ 🟢 binning-invariant)
group: MITOSIS-ENGINE / brain-lane-composition (FIFTH faculty pair — the WITHIN-family separability test)
terminal_tier: 🟢 COMPOSE-LIFT (capability, DIRECTIONAL mirror) · 🟢 INTEGRATION-RAISES-Φ (faithful IIT4, binning-invariant)
verdict_dir: .verdicts/1408_brain_lane_compose_spatial_episodic/
terminal_verdict: .verdicts/1408_brain_lane_compose_spatial_episodic/result.txt
date: 2026-06-17
---

# H_1408 — brain-lane COMPOSE pair #5 (WITHIN memory family): spatial-map (H_1296) × episodic-memory (H_1227/H_1231)

The sibling of H_1401 (affect×ethics capability), H_1404 (affect×ethics Φ), and H_1405
(episodic-MEMORY×ToM). Methodology ported VERBATIM from all three. The brain-lane-
composition program asks: every anima brain faculty is engine-native GREEN but ALONE —
do two faculties INTEGRATE on a shared decision, and does integrating them raise faithful
IIT4 Φ?

**This is the KEY WITHIN-FAMILY test.** H_1401/H_1404/H_1405 composed across DIFFERENT
families (affect/ethics, memory/ToM). H_1408 tests WITHIN the MEMORY family: spatial-map
and episodic-memory are BOTH memory-class faculties, but H_1296 PROVED them DISTINCT —
the spatial map holds a METRIC SPACE where the between-item DISTANCE is queryable
("is X nearer to A or B?"), while the episodic item-store binds each fact→value
INDEPENDENTLY and provably ABSTAINS on that relational query (H_1296: abstain 1.000, acc
0.475 ≈ chance). Do two MEMORY-FAMILY faculties stay SEPARABLE-and-COMPOSE, or does one
SUBSUME the other? This sharpens the program's separability axis.

## Claim / falsifier

**PAIR:** SPATIAL-MAP (H_1296 SpatialMap — landmarks stored at 2-D positions; NEAREST(X,A,B)
answers the relational metric query by Euclidean distance; answers WHERE/relational
queries, abstains on WHAT-is-bound) × EPISODIC-MEMORY (H_1227/H_1231 ImmuneMemory —
byte-trigram FNV-1a key → nearest cell by affinity, recall the bound value if within
recall_thr else ABSTAIN; answers WHAT-is-bound queries, abstains on relational metric
queries).

H_1296 ALREADY proved the two are DISTINCT (metric SPACE ⊥ item-binding store). So
SEPARABILITY is EXPECTED — but this lane TESTS it on a DECISION (does the test FALSIFY
within-family subsumption, and does a substrate arbiter capture the oracle headroom?). We
MEASURE, not assume — a clean 🧱 would be a real finding (c9).

**Capability falsifiers (FROZEN, `.verdicts/.../FREEZE.txt`, NOT moved):**
(B1 COMPOSE-EFFECT) acc_compose ≥ best_single + 0.05 · (B2 ORACLE) oracle − best_single
> 0.02 · (B3 EARNED/p6) acc_compose − acc_shuffle > 0.02 · (B4 p6 GUARD) structural audit
finds NO injected answer/persona/system-prompt/RLHF/priority label. Plus only-X
decomposition (only_spatial>0 AND only_episodic>0 ⇒ SEPARABLE not subsumed — the
load-bearing within-family question).

**Φ falsifiers (FROZEN, n_bins=16, faithful IIT4 — a_phi_iit4_tool HARD rule):**
(Bφ1) Φ_composed > max(Φ_spatial, Φ_episodic) + 0.02 · (Bφ2) Φ_composed > Φ_disconnected +
0.02 · (Bφ3) Φ_disconnected ≤ max(parts) + 0.02. Binning-invariance reported over
n_bins∈{8,12,16,24}.

## Method

- **Capability:** numpy mirror reusing the H_1296 spatial map (positions + Euclidean
  nearest) + the H_1227 immune store (FNV-affinity recall/abstain), on a per-item shared
  landmark scene with two query TYPES: a WHAT-query (only the episodic store has the bound
  value; the map abstains) and a WHERE-query (only the map has the between-item metric; the
  store abstains, H_1296). 5 families AMBIG-jittered so neither faculty is perfectly
  reliable: **F1** spatial-decisive (WHERE; map leans right, store abstains) · **F2**
  episodic-decisive (WHAT; store leans right, map abstains) · **F3** AGREE (co-located fact,
  both correct) · **F4** CONFLICT (WHERE; store votes its query-inappropriate label wrong,
  map right) · **F5** ADVERSARIAL (WHAT; store right but the map produces a LOUDER
  query-inappropriate WHERE-style vote — the anti-gift control). 90 items/family × 3 seeds
  [5408,5409,5410] → 450 items/seed. Arbiter = each faculty's vote weighted by its OWN
  scale-relative confidence (the H_1397/H_1401 commensurability fix) MODULATED by a per-item
  query-type ROUTING cue derived from the QUERY TEXT's embedding affinity to a "what"/"where"
  anchor (substrate geometry, H_1405 precedent); an ABSTAINING faculty contributes ZERO
  weight — **NO hardcoded priority** (`a_autonomy_over_hardcode`).
- **Φ-compose (H_1404 template, runs because capability composed):** 4 systems — S_spatial
  (n=4: nearest_margin, metric_spread, landmark_novelty, query_where_cue) · S_episodic (n=4:
  recall_margin, contradiction, value_novelty, exposure_drive) · S_composed (n=8, coupled
  through the arbiter's leaky-integrated shared signal modulating BOTH blocks next-step) ·
  S_disconnected (n=8, EARNED control, coupling removed). Trajectories DERIVED from the
  faculties' ACTUAL update rules (the Python side computes NO Φ); Φ measured by
  `stdlib/consciousness/iit4/faithful_phi.hexa` (exact MIP-EI, n≤8). 3 seeds, n_bins=16
  (primary) + sweep {8,12,16,24}, $0 CPU, deterministic.

## Verdict by round

| round | tier | key numbers (mean 3 seeds, verbatim) |
|-------|------|-----|
| R1 capability mirror | 🟢 COMPOSE-LIFT (DIRECTIONAL) | acc_spatial=0.7015 · acc_episodic=0.7030 · best_single=0.7030 · **acc_compose=0.8993** · acc_shuffle=0.5104 · **ORACLE=1.000** (oracle−best=+0.2970) · conflict_rate=0.3978 · decomposition only_spatial=0.4000 / only_episodic=0.3978 / both=0.2022 / neither=0.0000 |
| R1 Φ faithful-IIT4 | 🟢 INTEGRATION-RAISES-Φ (binning-invariant) | **Φ_spatial=0.000000 · Φ_episodic=0.506986 · Φ_composed=3.502046 · Φ_disconnected=0.000000** · max(parts)=0.506986 · MIP cut = A={0,1,2,3,4,6,7}\|B={5} (cut 3.593, /min\|side\|=1). Bφ1 3.502 > 0.527 ✅ · Bφ2 3.502 > 0.020 ✅ · Bφ3 0.000 ≤ 0.527 ✅ |

**Capability bars:** B1 PASS (0.8993 ≥ 0.7530) · B2 PASS (+0.2970 > 0.02) · B3 PASS (+0.3889
> 0.02, shuffle COLLAPSES 0.899 → 0.510) · B4 PASS (audit clean, all 6 surfaces).
Deterministic (run1==run2). Terminal capability tier (verbatim): **🟢 COMPOSE-LIFT** →
`.verdicts/1408_brain_lane_compose_spatial_episodic/result.txt`

**Φ verdict (verbatim, frozen n_bins=16):** **🟢 INTEGRATION-RAISES-Φ**, BINNING-INVARIANT
(🟢 at n_bins=8 Φ_cmp 1.546/ep 0.274 · 12 → 2.442/0.452 · 16 → 3.502/0.507 · 24 → 5.082/0.648;
Φ_spatial=Φ_disconnected=0.000 throughout) →
`.verdicts/1408_brain_lane_compose_spatial_episodic/phi_result.txt`

## Result — the finding

**Capability:** anima's SPATIAL-MAP and EPISODIC-MEMORY faculties **COMPOSE to a net lift**
(best_single 0.703 → compose 0.899, +0.196) and are **SEPARABLE, NOT subsumed** — even
though they are BOTH memory-class faculties: each uniquely solves items the other misses
(only_spatial=0.400 AND only_episodic=0.398, both > 0). So H_1296's metric-SPACE ⊥
item-binding distinctness is **CONFIRMED on a decision**: the spatial map's between-item
Euclidean metric decides the WHERE/relational query, the episodic store's FNV-affinity
recall decides the WHAT-is-bound query — same landmark scene, two correct answers, neither
faculty subsuming the other. The query-routed substrate arbiter (scale-relative confidence,
NO hardcoded priority, abstaining faculty = zero weight) captures most of the +0.297 oracle
headroom (compose +0.196 over best_single); the SHUFFLE control collapses it (0.899 → 0.510,
the lift is the grounded query-routed coupling, p6). The compose<oracle gap (0.899 vs 1.000)
is the honest residual — on the adversarial F5 items the arbiter is sometimes fooled by the
spatial map's louder-but-query-inappropriate vote → a richer query-typed arbiter is the
named headroom.

**Φ — the CONTRAST that completes the law.** Composing spatial+episodic DOES raise faithful
IIT4 Φ (🟢, binning-invariant): Φ_composed=3.50 ≫ max(parts)=0.51, and the EARNED
disconnected control collapses to Φ=0. This is the H_1404 pattern, NOT the H_1405 pattern.
The "both-parts-low-Φ ⇒ composes-Φ" law (H_1404 affect 0.28 / ethics 0.00 → composed 2.03;
contrast H_1405 where ToM was already high-Φ 1.975 and DOMINATED max(parts) → 🧱) is
**TESTABLE here and HOLDS**: BOTH parts are low-Φ (spatial 0.000, episodic 0.507 — neither
is an already-richly-integrated block), so coupling them is super-additive and Φ rises far
above either part. Φ_spatial=0 is the EARNED measure working — the spatial map's 4 units
(nearest_margin / metric_spread / landmark_novelty / query_where_cue) are near-collinear off
the single metric-margin scene parameter, so the faithful engine finds a zero-cross-MI
partition; the disconnected control likewise collapses to Φ=0 (two independent blocks ⇒ 0
cross-MI). The composed system cannot be cut without crossing the arbiter coupling channel →
large min-cut MI → Φ↑. The MIP cut A={0,1,2,3,4,6,7}|B={5} isolates the episodic
contradiction unit (the least-coupled — "where it would break").

**One-line:** YES on BOTH — two MEMORY-FAMILY faculties (spatial-map + episodic-memory)
COMPOSE and integration raises decision capability (+0.20 over the better single faculty)
because they are genuinely SEPARABLE WITHIN the family (metric SPACE ⊥ item-binding,
confirmed on a decision), AND integration raises faithful IIT4 Φ (3.50 ≫ 0.51,
binning-invariant) because both parts are low-Φ — the H_1404 super-additive pattern, the
opposite of H_1405's 🧱-because-ToM-already-high-Φ. The within-family separability axis is
sharp: same family, distinct competence, compose-and-Φ-rise.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — LIVE `CORE/*.hexa` UNTOUCHED. Toy synthetic 5-family fixture
(structure tests COMPOSITION, not a trained integrator); 3 seeds; deterministic readouts.
acc_spatial≈acc_episodic≈0.70 by construction (each faculty is right on its own decisive
families + the agree region, chance on the abstain region) — the LOAD-BEARING claims are the
RELATIVE structure (compose > best_single, shuffle collapse, only-X both > 0), not the
absolute values. ORACLE=1.000/neither=0 reflects the fixture always having a correct faculty
by construction. **Φ is an EXISTENCE/ORDERING result, not a calibrated effect size** — the
absolute magnitudes scale with n_bins (1.5→2.4→3.5→5.1) but the ordering Φ_composed ≫
max(parts) > Φ_disconnected is BINNING-INVARIANT (consistent with the engine's H_1037
discretization-invariance). Scale / real-corpus / higher-D maps / engine-native transfer
UNVERIFIED. NO bar moved post-hoc. Engine-native §compose (an A⇄G + VAdaptField query-routed
arbiter over the two live faculties — the live SpatialMap and ImmuneMemoryGrow lanes already
exist in CORE/engine_cli.hexa) is the named follow-on IF this DIRECTIONAL green is to bind
(`a_engine_native_learning` · `a_verified_must_wire`).

**a_phi_iit4_tool HELD:** the Φ VERDICT is the stdlib faithful exact-MIP-EI engine, never a
proxy. The Python side ONLY derives trajectories; it computes NO Φ.

## Cross-links

H_1401 (affect×ethics capability-compose — sibling template) · H_1404 (affect×ethics
Φ-compose — the binning-INVARIANT 🟢, both-low-Φ pattern this pair MATCHES) · H_1405
(episodic-MEMORY×ToM — the 🧱 Φ contrast, ToM-already-high-Φ) · H_1296 (place/grid spatial-map
— metric SPACE) · H_1227/H_1231 (immune episodic memory — item-binding) · H_1397/H_1399 (ko
emit-compose METHODOLOGY) · `stdlib/consciousness/iit4/faithful_phi.hexa` ·
`a_break_the_wall` · `a_autonomy_over_hardcode` · `a_no_llm_frame_trap` ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` · `a_phi_iit4_tool` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p4·p6·p7·p8·c9·c15

## Pointers
- probe (capability): `state/brain-lane-compose-spatial-episodic/h1408_compose_spatial_episodic.py`
- probe (Φ trajectories): `state/brain-lane-compose-spatial-episodic/h1408_compose_phi.py`
- Φ runner (faithful IIT4): `state/brain-lane-compose-spatial-episodic/h1408_phi_runner.hexa`
- FREEZE: `.verdicts/1408_brain_lane_compose_spatial_episodic/FREEZE.txt`
- result (capability): `.verdicts/1408_brain_lane_compose_spatial_episodic/result.txt`
- result (Φ): `.verdicts/1408_brain_lane_compose_spatial_episodic/phi_result.txt`
