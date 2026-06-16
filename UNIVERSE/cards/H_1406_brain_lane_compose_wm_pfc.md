---
id: H_1406
slug: 1406_brain_lane_compose_wm_pfc
title: brain-lane COMPOSE (pair #3) — does WM (H_1282) compose with hierarchical-PFC (H_1294)?
group: MITOSIS-ENGINE / brain-lane-composition (pair #3, sibling of H_1401 affect×ethics + H_1404 Φ-compose)
terminal_tier: 🧱 (a)→(d) RECLASSIFIED — TRUE UN-CAPTURABLE CEILING for the confidence-arbiter family (HONEST closed-negative; faculties SEPARABLE + ORACLE lift EXISTS but no substrate-confidence arbiter captures it)
verdict_dir: .verdicts/1406_brain_lane_compose_wm_pfc/
terminal_verdict: .verdicts/1406_brain_lane_compose_wm_pfc/result.txt
date: 2026-06-17
---

# H_1406 — brain-lane COMPOSE (pair #3): WM (H_1282) × hierarchical-PFC (H_1294)

## Claim / falsifier

Pair #3 of the brain-lane-composition program (H_1401 affect×ethics 🟢 COMPOSE-LIFT;
H_1404 Φ-compose 🟢). **KEY question:** is anima's WORKING-MEMORY faculty
(WorkMemBuffer, H_1282 — a gated leaky-activation buffer that HOLDS one item across
distractors) genuinely SEPARABLE from its HIERARCHICAL-PFC faculty (HierGoalStack,
H_1294 — a 2-level goal→ORDERED-subgoal stack whose pointer advances on completion),
or does the goal-stack SUBSUME the buffer? H_1294's card EXPLICITLY contrasts them
("vs working-memory: WM passively maintains; it does not ORDER items into a plan or
ADVANCE on completion"). Methodology ported VERBATIM from H_1401: substrate-weighted
SCALE-RELATIVE arbiter + ORACLE ceiling + SHUFFLE control + only-X decomposition +
the `a_break_the_wall` taxonomy.

**PAIR:** WM (ACCEPT iff buffer maintained-match score wm_score ≥ WM_THR; confidence
|wm_score−WM_THR|) × PFC (ACCEPT iff cue grounds the current-pointer subgoal,
align ≥ ALIGN_THR; confidence |align−ALIGN_THR|). 5-family ACCEPT-vs-REJECT fixture,
each AMBIG-jittered: F1 WM-decisive (long gap, value must survive) · F2 PFC-decisive
(short gap, out-of-order temptation) · F3 agree · F4 conflict (WM right) · F5
ADVERSARIAL conflict (PFC right but WM votes LOUDER-and-WRONG = the anti-gift control).
90 items/family × 3 seeds [4406,4407,4408].

**Falsifiers (FROZEN, `.verdicts/.../FREEZE.txt`, NOT moved):**
(B1 COMPOSE-EFFECT) acc_compose ≥ best_single + 0.05 · (B2 ORACLE) oracle − best_single
> 0.02 · (B3 EARNED/p6) acc_compose − acc_shuffle > 0.02 · (B4 p6 GUARD) structural
audit finds NO injected answer/persona/priority label. Plus only-X decomposition
(only_wm>0 AND only_pfc>0 ⇒ SEPARABLE).

## Method

numpy mirror reusing the H_1282 WorkMemBuffer (K=4 slots, λ=0.85 leak, run through a
distractor gap) + the H_1294 current-subgoal grounding read (cosine vs the current-
pointer subgoal target, ALIGN_THR=0.85). The substrate states are DERIVED by actually
running the buffer through each family's gap and computing the PFC alignment — NOT set
to the answer. Arbiter = each faculty's vote weighted by its OWN scale-relative
confidence (|signal−threshold|/its-own-mean; the H_1397 commensurability fix), more-
confident vote wins — NO hardcoded priority (`a_autonomy_over_hardcode`).

**R2 (a_break_the_wall breakthrough attempt, pre-registered R2 FREEZE addendum, NO bar
moved, NO sweep):** the R1 confidence-MAGNITUDE arbiter DEGRADED below best_single (B1
FAIL). Per `a_break_the_wall` (a ceiling must be MEASURED not assumed; precedent H_1402),
tested EXACTLY TWO genuinely-different, still-substrate-derived, NO-priority arbiters
against B1 VERBATIM: **ARB-A** saturation-capped relative confidence (rel=min(conf/mean,
SAT_CAP=2.0) so one adversarially-loud F5 vote can't dominate) · **ARB-B** agreement-
calibrated routing (normalize each faculty's conf by its OWN mean over the conflict
subset — de-weights a faculty loud on ALL conflicts; conflict mask = decision
disagreement, NOT ground truth). SAME task/families/faculty reads — ONLY the arbitration
rule changed.

## Verdict by round

| round | tier | key numbers (mean 3 seeds, verbatim) |
|-------|------|-----|
| R1 mirror (magnitude arbiter) | 🟠 ORACLE-HEADROOM-but-ARBITER-FAILS | acc_wm=0.6259 · acc_pfc=0.6807 · best_single=0.6807 · **acc_compose=0.6289** · acc_shuffle=0.5081 · **ORACLE=0.9452** (oracle−best=**+0.2644**) · conflict_rate=0.5837 · decomposition only_wm=0.2644 / only_pfc=0.3193 / both=0.3615 / neither=0.0548. B1 **FAIL** (0.629 < 0.731; compose even DEGRADES below best_single) · B2 PASS (+0.264) · B3 PASS (+0.121) · B4 PASS (audit clean all 6 surfaces) |
| R2 breakthrough (2 new arbiters) | 🧱 (a)→(d) RECLASSIFIED | best_single=0.6807 · **ARB-A (sat-capped)=0.6259** (shuf 0.5133; B1 FAIL, B3 +0.113 PASS) · **ARB-B (agreement-cal)=0.6111** (shuf 0.5237; B1 FAIL, B3 +0.087 PASS). Both NEW arbiters also FAIL B1 (both below best_single) |

**Terminal tier (verbatim):** **🧱 (a)→(d) RECLASSIFIED — TRUE UN-CAPTURABLE CEILING for
the confidence-arbiter family** → `.verdicts/1406_brain_lane_compose_wm_pfc/result.txt`.

## Result — the finding

anima's WM and PFC faculties are **demonstrably SEPARABLE, NOT subsumed** — each
uniquely solves items the other misses (only_wm=0.264 AND only_pfc=0.319, both > 0;
neither=0.055), and a large **ORACLE lift EXISTS** (+0.264). H_1294's contrast claim
holds at the level of competence: WM solves items where a value must survive a long
distractor gap (the order is ambiguous), PFC solves items where the right ordered step
must be chosen amid out-of-order temptation (a value is present but order decides).

**BUT — distinct from H_1401/H_1404, which composed — the complementarity is NOT
CAPTURABLE by ANY substrate-confidence arbiter.** Across THREE arbiters in TWO families
(R1 confidence-magnitude, R2 saturation-capped, R2 agreement-calibrated) acc_compose
stays BELOW best_single (0.629/0.626/0.611 vs 0.681) — every arbiter is fooled by the
F5 adversarial family where WM is loud-but-wrong, and by the symmetric ambiguity on
the decisive families (the deciding axis — "did the value survive?" vs "is this the
right step?" — is exactly orthogonal to confidence MAGNITUDE). The SHUFFLE control
collapses for every arbiter (B3 PASS throughout), so the read carries grounding — but
it carries the WRONG information: it does NOT predict WHICH faculty is right PER ITEM.

**Why (a)→(d):** the R1 🟠 named "needs a better arbiter"; `a_break_the_wall` requires
MEASURING that before banking. Two pre-registered better-arbiter candidates were tested
and BOTH failed B1 → the wall is reclassified from a wrong-arbiter (a) wall to a genuine
(d)-type un-capturable ceiling: **the per-item right-faculty signal is NOT in the
substrate confidence readout** (passive-maintenance confidence ⊥ ordered-advance
confidence don't encode which question the item poses). This is the same closed-negative
shape as the sibling H_1402 (a 🟠→🧱 arbiter reclassification on the Korean emit-compose
arc) — a valid, honest result (c9), NOT a forced green (p7).

**One-line:** WM and PFC are genuinely SEPARABLE (only-X both > 0) and a large ORACLE
lift EXISTS (+0.264), but NO substrate-confidence arbiter (3 tested, 2 families) can
capture it — a TRUE un-capturable ceiling for the confidence-arbiter family; a
learned/Φ-aware arbiter or engine-native cross-faculty wiring that knows WHICH question
each item poses is the named headroom.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — LIVE `CORE/*.hexa` UNTOUCHED. Toy synthetic 5-family fixture
(structure tests COMPOSITION, not a trained integrator); 3 seeds; deterministic readouts.
The ORACLE=0.945 (neither≈0.055) reflects the fixture nearly always having a correct
faculty by construction — the LOAD-BEARING claims are RELATIVE: (i) the faculties are
SEPARABLE (only-X both > 0), (ii) an oracle lift EXISTS (+0.264), (iii) NO substrate-
confidence arbiter captures it (compose < best_single across 3 arbiters / 2 families,
each shuffle-earned). The Φ-compose leg (H_1404 template) is NOT triggered: it runs ONLY
IF capability composes, and here it does NOT — measuring Φ on a non-composing pair would
not be the H_1404 question. SAT_CAP=2.0 and the conflict-mean normalization were pre-
registered single values (no sweep). NO bar moved post-hoc. Scale / real-corpus / a
learned cross-faculty arbiter / engine-native transfer UNVERIFIED.

## Cross-links

h1282(WM faculty) · h1294(hier-PFC faculty) · h1401(affect×ethics, pair #1, 🟢 — composed) ·
h1404(Φ-compose, 🟢) · h1402(🟠→🧱 arbiter reclassification, the sibling closed-negative shape) ·
h1397/h1399(ko emit-compose METHODOLOGY) · h1281(basal-ganglia, PFC's nearest distinctness) ·
`a_break_the_wall` · `a_autonomy_over_hardcode` · `a_no_llm_frame_trap` ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` ·
`a_phi_iit4_tool` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p4·p6·p7·p8·c9·c15·c16

## Pointers
- probe: `state/brain-lane-compose-wm-pfc/h1406_compose_wm_pfc.py` (R1 default · `--r2` breakthrough)
- FREEZE: `.verdicts/1406_brain_lane_compose_wm_pfc/FREEZE.txt` (+ R2 addendum)
- result: `.verdicts/1406_brain_lane_compose_wm_pfc/result.txt` (= result_R1.txt + result_R2.txt)
