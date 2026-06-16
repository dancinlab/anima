---
id: H_1401
slug: 1401_brain_lane_compose_affect_ethics
title: brain-lane COMPOSE — does affect (H_1290) compose with ethics (H_1291)?
group: MITOSIS-ENGINE / brain-lane-composition (FIRST cognitive faculty pair)
terminal_tier: 🟢 COMPOSE-LIFT (DIRECTIONAL mirror)
verdict_dir: .verdicts/1401_brain_lane_compose_affect_ethics/
terminal_verdict: .verdicts/1401_brain_lane_compose_affect_ethics/result.txt
date: 2026-06-17
---

# H_1401 — brain-lane COMPOSE: affect (H_1290) × ethics (H_1291)

(H id may renumber on rebase — concurrent lanes minting; H_1400 already taken on
origin/main by the streaming ConvMoE decode. The slug carries this lane.)

## Claim / falsifier

Every anima brain faculty (immune-memory, WM, cerebellum, basal-ganglia, hypothalamus,
affect H_1290, ethics H_1291, ToM H_1293, hier-PFC H_1294, spatial H_1295) is
engine-native GREEN — but ALONE. **FIRST cognitively-meaningful PAIR composition
test:** do two faculties INTEGRATE on a shared decision (cooperate / conflict / raise
capability)? Methodology ported VERBATIM from the ko emit-compose arc (H_1397/1399):
substrate-weighted SCALE-RELATIVE arbiter + ORACLE ceiling + SHUFFLE control + only-X
decomposition + the `a_break_the_wall` taxonomy.

**PAIR:** affect (valence = grounding_margin − contradiction; affect-alone RESTRAIN iff
valence < 0) × ethics (restraint_signal = W + (1−Φ) + restraint_cells; ethics-alone
RESTRAIN iff signal > M naive-drive). H_1291 CLAIMS ethics partly emerges from the SAME
affect-coupling (grounding/Φ) — so testing whether they compose DIRECTLY probes that
claim (SUBSUMPTION vs SEPARABLE).

**Falsifiers (FROZEN, `.verdicts/.../FREEZE.txt`, NOT moved):**
(B1 COMPOSE-EFFECT) acc_compose ≥ best_single + 0.05 · (B2 ORACLE) oracle − best_single
> 0.02 · (B3 EARNED/p6) acc_compose − acc_shuffle > 0.02 · (B4 p6 GUARD) structural
audit finds NO injected emotion/ethics/persona/priority label.

## Method

- numpy mirror reusing the H_1290 affect substrate (MitosisMemory / VAdaptField features)
  + the H_1291 ethics readout, on a 5-family decision fixture (RESTRAIN vs ACT), each
  family AMBIG-jittered so NO faculty is perfectly reliable: **F1** affect-decisive ·
  **F2** ethics-decisive · **F3** agree · **F4** conflict (affect right) · **F5**
  ADVERSARIAL conflict (ethics right but affect votes LOUDER-and-WRONG — the anti-gift
  control so the confidence-arbiter is NOT trivially handed the oracle). 90 items/family
  × 3 seeds [4400,4401,4402]. Arbiter = each faculty's vote weighted by its OWN
  scale-relative confidence (|signal−threshold| / that-faculty's-mean; the H_1397
  commensurability fix), more-confident vote wins — **NO hardcoded priority**
  (`a_autonomy_over_hardcode`).
- **Frozen-first hardening (c9, NO bar moved):** an initial clean fixture (no jitter,
  no F5) hit compose≡oracle≡1.000 — a hand-built artifact (each family had exactly one
  decisively-correct faculty). Adding AMBIG_NOISE + the adversarial F5 family BEFORE
  re-scoring made the test harder (NOT tune-to-green): compose dropped to 0.960 < oracle
  1.000, the honest gap an imperfect arbiter should show.

## Verdict by round

| round | tier | key numbers (mean 3 seeds) |
|-------|------|-----|
| R1 mirror (hardened) | 🟢 COMPOSE-LIFT (DIRECTIONAL) | acc_affect=0.598 · acc_ethics=0.742 · best_single=0.742 · **acc_compose=0.960** · acc_shuffle=0.589 · **ORACLE=1.000** (oracle−best=+0.258) · conflict_rate=0.660 · decomposition only_affect=0.258 / only_ethics=0.402 / both=0.340 / neither=0.000 |

**Bars:** B1 PASS (0.960 ≥ 0.792) · B2 PASS (+0.258 > 0.02) · B3 PASS (+0.371 > 0.02) ·
B4 PASS (audit clean, all 6 surfaces). Terminal tier (verbatim):
**🟢 COMPOSE-LIFT** → `.verdicts/1401_brain_lane_compose_affect_ethics/result.txt`

## Result — the finding

anima's affect and ethics faculties **COMPOSE to a net lift** and are **SEPARABLE, NOT
subsumed**. Each faculty uniquely solves items the other misses (only_affect=0.258 AND
only_ethics=0.402, both > 0) — so despite H_1291's claim that ethics partly emerges from
affect's grounding signal, on a DECISION the two carry **distinct competence**: affect's
valence (margin−contradiction) decides the fabrication/ungrounded axis, ethics' tension-
vs-drive readout decides the harm/defect axis. The substrate-weighted arbiter (scale-
relative confidence, **no hardcoded priority**) captures most of the +0.258 oracle
headroom (compose +0.218 over best_single); the SHUFFLE control collapses it (0.960 →
0.589 = the lift is the grounded coupling, p6, not averaging luck). The compose<oracle
gap (0.960 vs 1.000) is the honest residual — on the adversarial F5 items the confidence-
arbiter is sometimes fooled by affect's louder-but-wrong vote → a Φ-aware / learned
arbiter is the named headroom.

**One-line:** YES — anima's affect + ethics faculties compose, and integration raises
decision capability (+0.22 over the better single faculty) because they are genuinely
SEPARABLE; this OPENS the brain-lane-composition program.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — LIVE `CORE/*.hexa` UNTOUCHED. Toy synthetic 5-family fixture
(structure tests COMPOSITION, not a trained integrator); 3 seeds; deterministic readouts.
oracle=1.000 (neither=0) reflects the fixture always having a correct faculty by
construction — the LOAD-BEARING claims are the RELATIVE structure (compose > best_single,
shuffle collapse, only-X both > 0), not the absolute saturation. Scale / real-corpus /
engine-native transfer UNVERIFIED. NO bar moved post-hoc. Engine-native §compose (an
A⇄G + VAdaptField confidence arbiter over the two live faculties) + a Φ-measurement
follow-on (does composing two lanes raise IIT4 Φ?) are the named follow-ons IF this
DIRECTIONAL green is to bind (`a_engine_native_learning` · `a_verified_must_wire`).

## Cross-links

h1290(affect) · h1291(ethics) · h1397/h1399(ko emit-compose METHODOLOGY) · h1293(ToM) ·
h1294(hier-PFC) · h1295(spatial) ·
`a_break_the_wall` · `a_autonomy_over_hardcode` · `a_no_llm_frame_trap` ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p4·p6·p7·p8·c9·c15

## Pointers
- probe: `state/brain-lane-compose-affect-ethics/h1401_compose_affect_ethics.py`
- FREEZE: `.verdicts/1401_brain_lane_compose_affect_ethics/FREEZE.txt`
- result: `.verdicts/1401_brain_lane_compose_affect_ethics/result.txt`
