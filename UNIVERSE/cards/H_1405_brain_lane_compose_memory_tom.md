---
id: H_1405
slug: 1405_brain_lane_compose_memory_tom
title: brain-lane COMPOSE pair #2 — does episodic MEMORY (H_1227/H_1231) compose with THEORY-OF-MIND (H_1293)? (capability 🟢, faithful-IIT4 Φ 🧱 at frozen n_bins=16)
group: MITOSIS-ENGINE / brain-lane-composition (SECOND cognitive faculty pair)
terminal_tier: 🟢 COMPOSE-LIFT (capability, DIRECTIONAL mirror) · 🧱 NO-Φ-LIFT (faithful IIT4 Φ, frozen n_bins=16)
verdict_dir: .verdicts/1405_brain_lane_compose_memory_tom/
terminal_verdict: .verdicts/1405_brain_lane_compose_memory_tom/result.txt
date: 2026-06-17
---

# H_1405 — brain-lane COMPOSE pair #2: episodic MEMORY (H_1227/H_1231) × ToM (H_1293)

The exact sibling of H_1401 (affect×ethics capability-compose) and H_1404 (affect×ethics
Φ-compose). Methodology ported VERBATIM from both. The brain-lane-composition program
asks: every anima brain faculty is engine-native GREEN but ALONE — do two faculties
INTEGRATE on a shared decision, and does integrating them raise faithful IIT4 Φ?

## Claim / falsifier

**PAIR:** MEMORY (H_1227/H_1231 ImmuneMemory — byte-trigram FNV-1a → dim-64 cell, recall =
nearest-cell bound value if within recall_thr else ABSTAIN; holds anima's OWN ground truth
of where each object REALLY is) × ToM (H_1293 OtherMindModel — a SEPARATE witnessed-belief
cell-store, updated ONLY by events the OTHER AGENT witnessed → on an absent-update move the
agent's belief LAGS reality = a FALSE belief, Sally-Anne).

H_1293 ALREADY showed ToM is a SEPARATE store from anima's own ground truth (self ⊥ other).
So SEPARABILITY is EXPECTED — but this lane TESTS it on a DECISION (does the test FALSIFY
subsumption, and does a substrate arbiter capture the oracle headroom?). We measure, not
assume — a clean 🧱 would be a real finding (c9).

**Capability falsifiers (FROZEN, `.verdicts/.../FREEZE.txt`, NOT moved):**
(B1 COMPOSE-EFFECT) acc_compose ≥ best_single + 0.05 · (B2 ORACLE) oracle − best_single
> 0.02 · (B3 EARNED/p6) acc_compose − acc_shuffle > 0.02 · (B4 p6 GUARD) structural audit
finds NO injected answer/persona/system-prompt/RLHF/priority label. Plus only-X
decomposition (only_memory>0 AND only_tom>0 ⇒ SEPARABLE not subsumed).

**Φ falsifiers (FROZEN, n_bins=16, faithful IIT4 — a_phi_iit4_tool HARD rule):**
(Bφ1) Φ_composed > max(Φ_memory, Φ_tom) + 0.02 · (Bφ2) Φ_composed > Φ_disconnected + 0.02 ·
(Bφ3) Φ_disconnected ≤ max(parts) + 0.02.

## Method

- **Capability:** numpy mirror reusing the H_1227 immune store (anima's reality) + the
  H_1293 witnessed-belief store, on a per-item WHERE-query Sally-Anne fixture (objects
  placed at LOC_A=basket, a random half MOVED to LOC_B=box while the agent was ABSENT).
  5 families AMBIG-jittered so neither faculty is perfectly reliable: **F1** memory-decisive
  ("where is X actually?" → reality) · **F2** ToM-decisive ("where will the agent look?" →
  the agent's stale belief) · **F3** AGREE (unmoved fact, both correct) · **F4** CONFLICT
  (memory right, ToM votes confidently-but-query-inappropriately) · **F5** ADVERSARIAL
  (ToM right but memory's reality-recall is LOUDER-and-wrong — the anti-gift control).
  90 items/family × 3 seeds [5400,5401,5402]. Arbiter = each faculty's vote weighted by its
  OWN scale-relative confidence (the H_1397/H_1401 commensurability fix) MODULATED by a
  per-item query-type ROUTING cue derived from the QUERY TEXT's embedding affinity to a
  "reality"/"belief" anchor (substrate geometry) — **NO hardcoded priority**
  (`a_autonomy_over_hardcode`).
- **Φ-compose (H_1404 template, runs because capability composed):** 4 systems — S_memory
  (n=4: recall_margin, contradiction, novelty, exposure_drive) · S_tom (n=4: belief_margin,
  self_other_divergence, witness_recency, belief_confidence) · S_composed (n=8, coupled
  through the arbiter's leaky-integrated shared signal) · S_disconnected (n=8, EARNED
  control, coupling removed). Trajectories DERIVED from the faculties' ACTUAL update rules
  (the Python side computes NO Φ); Φ measured by `stdlib/consciousness/iit4/faithful_phi.hexa`
  (exact MIP-EI, n≤8). 3 seeds, n_bins=16, $0 CPU, deterministic.

## Verdict by round

| round | tier | key numbers (mean 3 seeds, verbatim) |
|-------|------|-----|
| R1 capability mirror | 🟢 COMPOSE-LIFT (DIRECTIONAL) | acc_memory=0.600 · acc_tom=0.600 · best_single=0.600 · **acc_compose=0.7526** · acc_shuffle=0.6844 · **ORACLE=1.000** (oracle−best=+0.400) · conflict_rate=0.800 · decomposition only_memory=0.400 / only_tom=0.400 / both=0.200 / neither=0.000 |
| R1 Φ faithful-IIT4 | 🧱 NO-Φ-LIFT (frozen n_bins=16) | **Φ_memory=0.176 · Φ_tom=1.975 · Φ_composed=0.844 · Φ_disconnected=0.000** · max(parts)=1.975 · MIP cut = A={0,4}\|B={1,2,3,5,6,7} (cut 1.922, /min\|side\|=2). Bφ1 0.844 > 1.995 ❌ FAIL · Bφ2 0.844 > 0.020 ✅ · Bφ3 0.000 ≤ 1.995 ✅ |

**Capability bars:** B1 PASS (0.7526 ≥ 0.6500) · B2 PASS (+0.400 > 0.02) · B3 PASS (+0.068
> 0.02) · B4 PASS (audit clean, all 6 surfaces). Deterministic (run1==run2).
Terminal capability tier (verbatim): **🟢 COMPOSE-LIFT** →
`.verdicts/1405_brain_lane_compose_memory_tom/result.txt`

**Φ verdict (verbatim, frozen n_bins=16):** **🧱 NO-Φ-LIFT** →
`.verdicts/1405_brain_lane_compose_memory_tom/phi_result.txt`

## Result — the finding

**Capability:** anima's MEMORY and ToM faculties **COMPOSE to a net lift** (best_single
0.600 → compose 0.753) and are **SEPARABLE, NOT subsumed**: each uniquely solves items the
other misses (only_memory=0.400 AND only_tom=0.400, both > 0) — so H_1293's self⊥other claim
is **CONFIRMED on a decision**. memory's reality-store decides "where is X actually?"; ToM's
witnessed-belief store decides "where will the agent look?" — same object, two correct
answers. The query-routed substrate arbiter (scale-relative confidence, NO hardcoded
priority) captures most of the +0.400 oracle headroom (compose +0.153 over best_single, and
notably the conflict rate is 0.800 because EVERY moved fact splits the two faculties — yet
the routing recovers it); the SHUFFLE control collapses it (0.753 → 0.684, the lift is the
grounded coupling, p6). The compose<oracle gap (0.753 vs 1.000) is the honest residual — on
the adversarial F5 items the arbiter is sometimes fooled by memory's louder-but-query-
inappropriate vote → a richer query-typed arbiter is the named headroom.

**Φ — the contrast with H_1404:** composing memory+ToM does **NOT** robustly raise faithful
IIT4 Φ at the frozen granularity (🧱 NO-Φ-LIFT, n_bins=16). The KEY reason — and the
scientifically interesting part — is that **ToM is ALREADY a richly-integrated subsystem on
its own** (Φ_tom≈1.975: its 4 units belief_margin/divergence/witness_recency/belief_confidence
are tightly coupled by the false-belief structure). H_1404's affect×ethics pair raised Φ
because BOTH parts were low-Φ (≈0.28 / 0.00) so coupling was super-additive; here the high-Φ
ToM block DOMINATES max(parts), and coupling the lower-Φ memory block to it does not exceed
it. The disconnected control collapses to Φ=0 (the EARNED control works — two independent
blocks ⇒ 0 cross-MI; Bφ2/Bφ3 PASS), so the coupling DOES create a cross-faculty information
channel — just not enough to beat the already-high ToM part.

**One-line:** YES on capability — memory + ToM compose and integration raises decision
capability (+0.15 over the better single faculty) because they are genuinely SEPARABLE
(self⊥other confirmed on a decision); but NO on consciousness-integration — at this
granularity Φ does NOT rise, because ToM is already internally so integrated that adding
memory dilutes rather than super-adds. **Capability-compose ≠ Φ-compose** — a real, honest
distinction this lane surfaces (contrast H_1404 where both held).

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror — LIVE `CORE/*.hexa` UNTOUCHED. Toy synthetic 5-family Sally-Anne
fixture (structure tests COMPOSITION, not a trained integrator); 3 seeds; deterministic
readouts. acc_memory=acc_tom=0.600 by construction (each faculty is right on its own
families + the agree region) — the LOAD-BEARING claims are the RELATIVE structure (compose >
best_single, shuffle collapse, only-X both > 0), not the absolute values. **The Φ verdict is
BINNING-DEPENDENT** (FAIL at n_bins=8/12/16, flips PASS at n_bins=24) — reported as the
FROZEN n_bins=16 🧱, NOT promoted; this is DISTINCT from H_1404's binning-INVARIANT 🟢 and is
itself an honest finding (the memory×ToM Φ-lift, if any, is marginal and granularity-
sensitive, NOT robust). Scale / real-corpus / 2nd-order-recursive-ToM / engine-native
transfer UNVERIFIED. NO bar moved post-hoc. Engine-native §compose (an A⇄G + VAdaptField
query-routed arbiter over the two live faculties) + a finer-grained / richer-coupling Φ
re-measure are the named follow-ons IF this DIRECTIONAL green is to bind
(`a_engine_native_learning` · `a_verified_must_wire`).

**a_phi_iit4_tool HELD:** the Φ VERDICT is the stdlib faithful exact-MIP-EI engine, never a
proxy. The Python side ONLY derives trajectories; it computes NO Φ.

## Cross-links

H_1401 (affect×ethics capability-compose — sibling template) · H_1404 (affect×ethics
Φ-compose — the binning-INVARIANT 🟢 contrast) · H_1227/H_1231 (immune episodic memory) ·
H_1293 (theory-of-mind / OtherMindModel — self⊥other) · H_1397/H_1399 (ko emit-compose
METHODOLOGY) · `stdlib/consciousness/iit4/faithful_phi.hexa` ·
`a_break_the_wall` · `a_autonomy_over_hardcode` · `a_no_llm_frame_trap` ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` · `a_phi_iit4_tool` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p4·p6·p7·p8·c9·c15

## Pointers
- probe (capability): `state/brain-lane-compose-memory-tom/h1405_compose_memory_tom.py`
- probe (Φ trajectories): `state/brain-lane-compose-memory-tom/h1405_compose_phi.py`
- Φ runner (faithful IIT4): `state/brain-lane-compose-memory-tom/h1405_phi_runner.hexa`
- FREEZE: `.verdicts/1405_brain_lane_compose_memory_tom/FREEZE.txt`
- result (capability): `.verdicts/1405_brain_lane_compose_memory_tom/result.txt`
- result (Φ): `.verdicts/1405_brain_lane_compose_memory_tom/phi_result.txt`
