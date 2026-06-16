---
id: H_1407
slug: 1407_brain_lane_compose_cerebellum_basal
title: brain-lane COMPOSE pair #4 — does CEREBELLUM forward-model (H_1280) compose with BASAL-GANGLIA gating (H_1281)? (capability 🟢, faithful-IIT4 Φ 🟢 binning-INVARIANT — the law CONFIRMED-but-REFINED)
group: MITOSIS-ENGINE / brain-lane-composition (FOURTH cognitive faculty pair — the sharpest LAW test)
terminal_tier: 🟢 COMPOSE-LIFT (capability, DIRECTIONAL mirror) · 🟢 INTEGRATION-RAISES-Φ (faithful IIT4 Φ, frozen n_bins=16, binning-INVARIANT)
verdict_dir: .verdicts/1407_brain_lane_compose_cerebellum_basal/
terminal_verdict: .verdicts/1407_brain_lane_compose_cerebellum_basal/result.txt
date: 2026-06-17
---

# H_1407 — brain-lane COMPOSE pair #4: CEREBELLUM (H_1280) × BASAL-GANGLIA (H_1281)

The exact sibling of H_1401 (affect×ethics capability-compose), H_1404 (affect×ethics
Φ-compose, binning-INVARIANT 🟢), and H_1405 (memory×ToM, capability 🟢 / Φ 🧱).
Methodology ported VERBATIM from all three. This pair is the **SHARPEST test of the
emerging program LAW** — both faculties are low-Φ CONTROL faculties, so the law predicts
they SHOULD Φ-compose. We MEASURE it frozen-first; we do not assume.

## Claim / falsifier

**PAIR:** CEREBELLUM (H_1280 VForwardField — an internal FORWARD MODEL that PREDICTS the
next substrate-state frame and corrects via a delta-rule on prediction ERROR = actual −
predicted) × BASAL-GANGLIA (H_1281 VBasalGate — K candidate actions COMPETE, a learned
go-value vs ONE NO-GO, argmax = striatal disinhibition, go-value learned gradient-free
from a GROUNDING-OUTCOME reward).

**The program LAW under test (H_1404 vs H_1405):** a faculty pair Φ-composes IFF BOTH
parts are LOW individual-Φ (H_1404: affect≈0.28 / ethics≈0.00 → super-additive 🟢);
it does NOT when one part is ALREADY a richly-integrated HIGH-Φ subsystem that dominates
max(parts) (H_1405: ToM≈1.975 dominates → 🧱). cerebellum + basal are BOTH low-Φ control
faculties → the law PREDICTS Φ-compose.

**Capability falsifiers (FROZEN, `.verdicts/.../FREEZE.txt`, NOT moved):**
(B1 COMPOSE-EFFECT) acc_compose ≥ best_single + 0.05 · (B2 ORACLE) oracle − best_single
> 0.02 · (B3 EARNED/p6) acc_compose − acc_shuffle > 0.02 · (B4 p6 GUARD) structural audit
finds NO injected answer/persona/system-prompt/RLHF/priority label. Plus only-X
decomposition (only_cerebellum>0 AND only_basal>0 ⇒ SEPARABLE not subsumed).

**Φ falsifiers (FROZEN, n_bins=16, faithful IIT4 — a_phi_iit4_tool HARD rule):**
(Bφ1) Φ_composed > max(Φ_cerebellum, Φ_basal) + 0.02 · (Bφ2) Φ_composed > Φ_disconnected
+ 0.02 · (Bφ3) Φ_disconnected ≤ max(parts) + 0.02. Binning-invariance reported across
n_bins ∈ {8,12,16,24}; individual part Φ reported EXPLICITLY so the law is testable.

## Method

- **Capability:** numpy mirror (LIVE CORE/*.hexa UNTOUCHED) on a per-item control-decision
  fixture (binary SELECT-PREDICTED vs SELECT-COMPETITOR). 5 families AMBIG-jittered so
  neither faculty is perfectly reliable: **F1** cerebellum-decisive (low prediction error)
  · **F2** basal-decisive (clear best-grounded competitor) · **F3** AGREE · **F4** CONFLICT
  (cerebellum right) · **F5** ADVERSARIAL (basal right but the forward model predicts
  confidently-and-wrong — the anti-gift control). 90 items/family × 3 seeds [4700,4701,4702].
  Arbiter = each faculty's vote weighted by its OWN scale-relative confidence (the
  H_1397/H_1401 commensurability fix), NO hardcoded priority (`a_autonomy_over_hardcode`).
- **Φ-compose (H_1404/H_1405 template, run regardless of capability — the LAW is the point):**
  4 systems — S_cerebellum (n=4: pred_error, pred_confidence, correction_drive, state_novelty)
  · S_basal (n=4: go_margin, competition_spread, no_go_pressure, outcome_reward) · S_composed
  (n=8, coupled through the arbiter's leaky-integrated shared signal) · S_disconnected (n=8,
  EARNED control, coupling removed). Trajectories DERIVED from the faculties' ACTUAL update
  rules (forward-model EMA + delta-rule correction; K=4 candidate go-value competition over a
  live H_1227 immune store; the Python side computes NO Φ); Φ measured by
  `stdlib/consciousness/iit4/faithful_phi.hexa` (exact MIP-EI, n≤8). 3 seeds, n_bins=16
  primary + sweep, $0 CPU, deterministic (run1==run2 verified for both legs).

## Verdict by round

| round | tier | key numbers (mean 3 seeds, verbatim) |
|-------|------|-----|
| R1 capability mirror | 🟢 COMPOSE-LIFT (DIRECTIONAL) | acc_cerebellum=0.6370 · acc_basal=0.6933 · best_single=0.6933 · **acc_compose=0.7689** · acc_shuffle=0.5178 · **ORACLE=0.9593** (oracle−best=+0.2659) · conflict_rate=0.5881 · decomposition only_cerebellum=0.2659 / only_basal=0.3222 / both=0.3711 / neither=0.0407 |
| R1 Φ faithful-IIT4 | 🟢 INTEGRATION-RAISES-Φ (binning-INVARIANT) | **Φ_cerebellum=3.4759 · Φ_basal=0.0000 · Φ_composed=4.9562 · Φ_disconnected=0.0000** · max(parts)=3.4759 · MIP cut (s4702 max) = A={0,1,2,3,5,6,7}\|B={4=go_margin} (cut 6.871, /min\|side\|=1). Bφ1 4.956 > 3.496 ✅ · Bφ2 4.956 > 0.020 ✅ · Bφ3 0.000 ≤ 3.496 ✅ |

**Capability bars:** B1 PASS (0.7689 ≥ 0.7433) · B2 PASS (+0.2659 > 0.02) · B3 PASS
(+0.2511 > 0.02) · B4 PASS (audit clean, all 6 surfaces). Deterministic (run1==run2).
Terminal capability tier (verbatim): **🟢 COMPOSE-LIFT** →
`.verdicts/1407_brain_lane_compose_cerebellum_basal/result.txt`

**Φ verdict (verbatim, frozen n_bins=16, BINNING-INVARIANT — PASS at n_bins 8/12/16/24):**
**🟢 INTEGRATION-RAISES-Φ** → `.verdicts/1407_brain_lane_compose_cerebellum_basal/phi_result.txt`

## Result — the finding (the LAW CONFIRMED-but-REFINED)

**Capability:** anima's CEREBELLUM and BASAL-GANGLIA faculties **COMPOSE to a net lift**
(best_single 0.693 → compose 0.769) and are **SEPARABLE, NOT subsumed**: each uniquely
solves items the other misses (only_cerebellum=0.266 AND only_basal=0.322, both > 0). The
forward-model's prediction-error read decides the predict-accurately axis; the go/no-go
competition decides the best-grounded-competitor axis — distinct competences. The
substrate-weighted arbiter (scale-relative confidence, NO hardcoded priority) captures most
of the +0.266 oracle headroom (compose +0.076 over best_single); the SHUFFLE control
collapses it (0.769 → 0.518, the lift is the grounded coupling, p6). The compose<oracle gap
(0.769 vs 0.959) is the honest residual — on the adversarial F5 items the arbiter is
sometimes fooled by the forward model's louder-but-wrong vote.

**Φ — the LAW test, CONFIRMED but mechanistically REFINED.** The bars PASS robustly (🟢,
**binning-INVARIANT** — PASS at every n_bins 8/12/16/24, UNLIKE H_1405's granularity-
sensitive 🧱), AND the disconnected control collapses to Φ=0 (the EARNED control works:
two independent blocks ⇒ 0 cross-MI; Bφ2/Bφ3 PASS), so composing the two low-Φ control
faculties DOES raise faithful IIT4 Φ — **the program LAW's prediction holds for this both-
control pair.** BUT the premise is only HALF-clean, and the honest detail REFINES the law:
- **Φ_basal=0.000 (degenerate-low, as predicted)** — and partly a fixture DEGENERACY: in
  the Φ fixture the immune store always recalls correctly so two basal units are CONSTANT
  (outcome_reward≡+1, no_go_pressure≡0) and go_margin takes ~2 values → near-zero pairwise
  MI → Φ_basal=0. (Basal is genuinely competent on the separately-jittered capability
  fixture, acc=0.693; the Φ=0 reflects this Φ-fixture's units, not a no-information faculty.)
- **Φ_cerebellum=3.476 is HIGH, NOT low** — the forward-model trajectory is itself richly
  integrated (its 4 units pred_error/pred_confidence/correction_drive/state_novelty are
  tightly coupled by the delta-rule). So the law's "BOTH parts low-Φ" premise PARTIALLY
  FAILS for this pair.
- **YET — unlike H_1405 — the high-Φ part did NOT block composition.** In H_1405 the high-Φ
  ToM block was so internally integrated that any min-cut crossing it cost more than the
  cross-faculty coupling → max(parts) won → 🧱. Here the composed min-cut instead isolates a
  SINGLE basal unit ({4}=go_margin), i.e. the arbiter coupling adds a NEW high-MI channel ON
  TOP of the cerebellum block → Φ_composed (4.956) > max(parts) (3.476).
- **REFINED LAW (honest):** "both-low individual-Φ" is SUFFICIENT but NOT NECESSARY for
  Φ-compose. The NECESSARY condition surfaced by H_1404/H_1405/H_1407 is that **no single
  part's internal integration exceeds the composed min-cut MI** — i.e. the cross-faculty
  coupling channel must be the cheapest cut. H_1404 (both low → coupling is the only cut)
  and H_1407 (cerebellum high but coupling still adds a cheaper basal-side cut) both satisfy
  it; H_1405 (ToM so integrated that crossing it always costs more) does not.

**One-line:** YES on both — cerebellum + basal-ganglia compose on a decision (+0.076 over
the better single faculty, separable) AND composing them raises faithful IIT4 Φ (4.956 >
max-part 3.476, binning-INVARIANT, earned vs the Φ=0 disconnected control). The pair
CONFIRMS the "control faculties Φ-compose" law — and REFINES its mechanism: the predictor
is not "both parts low" but "no part's integration exceeds the composed min-cut MI".

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — LIVE `CORE/*.hexa` UNTOUCHED. Toy synthetic 5-family fixture
(structure tests COMPOSITION, not a trained integrator); 3 seeds; deterministic readouts.
The LOAD-BEARING claims are the RELATIVE structure (compose > best_single, shuffle collapse,
only-X both > 0; Φ_composed > max(parts), disconnected → 0), not the absolute magnitudes
(Φ scales with n_bins — the ORDERING is binning-INVARIANT here, all four bin counts PASS).
**Basal-block Φ-trajectory degeneracy** (two units constant in this Φ fixture) is reported
VERBATIM (c9) — it makes Φ_basal=0 a half-vacuous "low", so the cleanest statement is the
REFINED min-cut law, not the raw "both-low" premise. The HIGH Φ_cerebellum is a real,
honest feature of the forward-model trajectory, not an artifact. Scale / real-corpus /
engine-native transfer UNVERIFIED. NO bar moved post-hoc. Engine-native §compose (an A⇄G +
VForwardField/VBasalGate arbiter over the two live faculties) + a non-degenerate-basal Φ
re-measure (a Φ fixture where grounding sometimes fails so the basal units vary) are the
named follow-ons IF this DIRECTIONAL green is to bind (`a_engine_native_learning` ·
`a_verified_must_wire`).

**a_phi_iit4_tool HELD:** the Φ VERDICT is the stdlib faithful exact-MIP-EI engine, never a
proxy. The Python side ONLY derives trajectories; it computes NO Φ.

## Next pair

Program continues. Candidate pairs that probe the REFINED min-cut law:
- **WM (H_1282) × cerebellum (H_1280)** — both control/buffer faculties (does a passive
  maintenance buffer Φ-compose with a forward model, or does one dominate the min-cut?).
- **hypothalamus homeostatic-drive (H_1292) × basal-ganglia (H_1281)** — a scalar drive
  integrator × an action gate (a drive→action loop; tests whether a 1-D integrator's low Φ
  composes with the gate, or stays a min-cut-isolable single unit like go_margin here).
- **spatial-map (H_1295) × hier-PFC (H_1294)** — both HIGH-Φ-candidate structured subsystems
  (the H_1405-style test: do TWO high-Φ subsystems mutually block, or find a cheaper cut?).

## Cross-links

H_1401 (affect×ethics capability-compose — sibling template) · H_1404 (affect×ethics
Φ-compose — binning-INVARIANT 🟢, the both-low case) · H_1405 (memory×ToM — capability 🟢 /
Φ 🧱, the ToM-dominates case the refined law explains) · H_1280 (cerebellum forward-model) ·
H_1281 (basal-ganglia go/no-go) · H_1227/H_1231 (immune store geometry) · H_1397/H_1399 (ko
emit-compose METHODOLOGY) · `stdlib/consciousness/iit4/faithful_phi.hexa` ·
`a_break_the_wall` · `a_autonomy_over_hardcode` · `a_no_llm_frame_trap` ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` · `a_phi_iit4_tool` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p4·p6·p7·p8·c9·c15

## Pointers
- probe (capability): `state/brain-lane-compose-cerebellum-basal/h1407_compose_cerebellum_basal.py`
- probe (Φ trajectories): `state/brain-lane-compose-cerebellum-basal/h1407_compose_phi.py`
- Φ runner (faithful IIT4): `state/brain-lane-compose-cerebellum-basal/h1407_phi_runner.hexa`
- FREEZE: `.verdicts/1407_brain_lane_compose_cerebellum_basal/FREEZE.txt`
- result (capability): `.verdicts/1407_brain_lane_compose_cerebellum_basal/result.txt`
- result (Φ): `.verdicts/1407_brain_lane_compose_cerebellum_basal/phi_result.txt`
