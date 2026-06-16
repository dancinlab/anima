---
id: H_1420
slug: 1420_memory_basal_multilens
title: "MEMORY×BASAL compose WALL — MULTI-LENS breakthrough attempt: do basal-gated recall (A), memory-valued gate (B, the tom_basal shape), OR complementary conflict-gating (C) bind engine-native where H_1417 P2's confidence-arbiter (net-lift +0.0496) missed by 0.0004? (a_break_the_wall MULTI-LENS + per-lens ABLATION)"
group: MITOSIS-ENGINE / brain-lane-composition — c16 MULTI-LENS attempt on the memory×basal engine-bind wall (the most promising of the three remaining walls)
terminal_tier: "🧱 ENGINE-NATIVE NON-BINDING — CONFIDENT-TERMINAL across THREE biology-faithful cortico-basal lenses (FOUR mechanisms counting H_1417 P2's arbiter). Lens A basal-gated recall: B1 −0.16 · B3 −0.052 · ABLATION INERT (compose 0.535 < ablate 0.642 — gating actively HURTS). Lens B memory-valued gate (the EXACT shape that bound ToM×basal in H_1418 P5): B1 −0.119 · B3 −0.013 · ABLATION INERT (compose 0.580 == basal standalone 0.6985 with margin removed). Lens C complementary conflict-gating: B2/B3/SEP/ABLATION all PASS (gate NON-inert, ablation +0.127) but B1 FAIL net-lift +0.043 < +0.05 — the same borderline miss as H_1417 P2's +0.0496. MULTI-LENS confirmed (d) ceiling / strong-standalone-arm subsumption; NO bar moved, frozen-first."
wired: N/A (🧱 — no live CORE op; probe over EXISTING immune_grow_recall / vbasal_go_value)
verdict_dir: .verdicts/1420_memory_basal_multilens/
terminal_verdict: .verdicts/1420_memory_basal_multilens/result.txt
date: 2026-06-17
---

# H_1420 — MEMORY×BASAL compose: MULTI-LENS breakthrough attempt (c16, a_break_the_wall)

H_1417 P2 (memory×basal) closed the engine-native compose at 🧱 with the STANDARD
scale-relative confidence ARBITER (parallel vote): net-lift **+0.0496**, missing the
frozen +0.05 B1 bar by **0.0004**. That razor-thin miss made it the **most promising**
of the three remaining engine-bind walls. And H_1418 P5 proved ToM×basal **DID** bind
(net-lift +0.096) — so basal is **not** intrinsically un-composable. Per the freshly
strengthened **a_break_the_wall** (commit 3304edc65), a (d)-ceiling cannot be declared
terminal from one lens: it needs **MULTI-LENS** confirmation (≥2-3 genuinely different
principled lenses, **each with a shuffle AND an ablation control**), and the **ABLATION
is decisive** — if mechanism-OFF scores the same as compose, the mechanism is INERT ⇒
ceiling. This card tries three biology-faithful cortico-basal lenses (a_no_llm_frame_trap),
**NOT** a re-tune of the arbiter.

## The three lenses (real cortico-basal neuroscience)

- **Lens A — BASAL-GATED RECALL:** the basal ganglia GATES which memory drives behaviour.
  The LIVE `vbasal_go_value` go/no-go decides whether the LIVE `immune_grow_recall` value
  is RELEASED or SUPPRESSED (no-go ⇒ fall back to the gate's own action). Sequential
  gate-on-output, NOT a parallel vote. ABLATE: gate always GO ⇒ memory standalone.
- **Lens B — MEMORY-VALUED GATE:** memory's recall MARGIN supplies the value/utility the
  basal threshold reads (memory margin = the gate's input feature). **This is EXACTLY the
  shape by which `tom_basal_compose` (H_1418 P5) BOUND** — the composed-arm margin valuing
  the gate. ABLATE: memory margin ignored ⇒ basal standalone.
- **Lens C — COMPLEMENTARY (conflict-only) GATING:** agree ⇒ shared vote; abstain ⇒ the
  other; in CONFLICT the gate releases memory iff its recall margin out-values the gate's
  go-margin (substrate-scaled), else the gate's action wins. ABLATE: in conflict always
  take memory (gate inert) ⇒ fixed memory-wins rule.

Memory leg = LIVE `immune_grow_recall` + L2 affinity margin (ImmuneMemoryGrow). Basal leg
= LIVE `vbasal_go_value` over a gradient-free-trained VBasalGate (brain.hexa, value-passed
like `spatial_episodic_compose` / `tom_basal_compose`). Fixture = the SAME 5-family
structure as H_1417, N_PER_FAMILY=90 → 450 items/seed, 3 seeds/lens, deterministic. Gate /
value thresholds = substrate MEAN go-margin / mean recall-margin (NOT tuned).

## FROZEN bars (IDENTICAL to H_1407/1414/1415/1417 — NOT moved) + per-lens ABLATION

(B1) compose ≥ best+0.05 · (B2) oracle−best > 0.02 · (B3) compose−shuffle > 0.02 ·
(SEP) only_mem>0 ∧ only_basal>0 · (ABLATION) compose−ablate > 0. BOUND 🟢 iff all five for
SOME lens; else 🧱.

## Result — 🧱 across all three lenses (verbatim, `.verdicts/.../result.txt`, run1==run2 byte-identical)

| lens | acc_mem | acc_basal | best | compose | shuffle | ablate | net-lift (B1) | comp−shuf (B3) | comp−abl (ABL) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** basal-gated recall | 0.6422 | 0.6948 | 0.6948 | 0.5348 | 0.5867 | 0.6422 | **−0.16 FAIL** | **−0.052 FAIL** | **−0.107 FAIL — INERT** | 🧱 |
| **B** memory-valued gate (tom_basal shape) | 0.6237 | 0.6985 | 0.6985 | 0.5800 | 0.5933 | 0.6985 | **−0.119 FAIL** | **−0.013 FAIL** | **−0.119 FAIL — INERT** | 🧱 |
| **C** complementary conflict-gating | 0.6215 | 0.7052 | 0.7052 | 0.7481 | 0.5763 | 0.6215 | **+0.043 FAIL** | +0.172 PASS | +0.127 PASS | 🧱 |

(All lenses B2/SEP PASS — oracle headroom +0.25~+0.27 and both arms separable are REAL.)

**VERDICT (verbatim): 🧱 CONFIDENT-TERMINAL — all 3 cortico-basal lenses FAIL their controls.**
→ `.verdicts/1420_memory_basal_multilens/result.txt`

## Why this is a STRONG terminal (MULTI-LENS cross-confirmation, the ABLATION payload)

Four mechanisms now fail engine-native on memory×basal:

- **arbiter (H_1417 P2)** — parallel scale-relative confidence vote: B1 net-lift **+0.0496 < +0.05** (the original razor-thin miss; B2/B3/SEP all PASS).
- **Lens A (basal-gated recall)** — the hard gate doesn't just fail to help, it **HURTS**: compose 0.535 sits BELOW both standalone arms and even below the ablation (memory-standalone 0.642). The go/no-go suppresses *correct* memory recalls in the X-decisive families because the gate's go-margin (trained to a fixed positive go-weight) does not track per-item memory correctness. ABLATION decisive: turning gating OFF scores **+0.107 higher** ⇒ the mechanism is worse than inert.
- **Lens B (memory-valued gate)** — the **exact shape that BOUND ToM×basal** (H_1418 P5). For memory it is **INERT**: with the memory margin removed, compose collapses to basal standalone (0.6985) — i.e. the memory-margin value never flips a gate decision (compose 0.580 ≈ the gated-but-valueless path). The recall margin (a saturated L2 affinity, near-constant across families) carries **no per-item discriminative utility** the gate can threshold on, unlike the ToM belief margin which did. This is the load-bearing dissociation: **value-margin composition is faculty-specific, not a universal gate recipe.**
- **Lens C (complementary conflict-gating)** — the **only** lens whose gate is NON-inert (ablation +0.127, shuffle collapses +0.172) — the conflict-region gate genuinely earns routing. But it STILL **cannot clear +0.05** (net-lift **+0.043**), landing on the same razor edge as the arbiter's +0.0496. The capturable conflict structure exists, but the basal go-margin captures only ~+0.043 of the +0.25 oracle headroom — short of the bar.

**Root cause (now triply confirmed, consistent with H_1417's refined law):** engine-bind is
gated by **arbiter-CAPTURE of the oracle headroom**, not arm strength. For memory×basal the
LIVE `immune_grow_recall` affinity margin **saturates** (near-constant L2 across families), so
it carries little per-item routing signal — every gate-based lens that reads that margin
(B value, C confidence) tops out at ~+0.043~+0.049 capture, just under +0.05. The basal
go-margin (trained to a fixed go-weight) is likewise per-item-flat. Neither faculty supplies
the conflict-discriminating signal needed to capture the +0.25 headroom past the bar. This is a
genuine **(d) ceiling / strong-standalone-arm subsumption** (a_break_the_wall taxonomy),
MULTI-LENS confirmed across four mechanisms.

**Contrast (the bind is pair-dependent, not universal):** ToM×basal (H_1418 P5, +0.096) and
memory×ToM (H_1414, +0.338) BOTH bound — pairs where the composed arm's margin (witnessed-belief
affinity) carries real per-item utility. Memory×basal is the counter-pole: the immune affinity
margin saturates, so no gate lens — voting (H_1417), hard-gating (A), valuing (B), or
conflict-routing (C) — captures enough headroom.

## Wiring (a_verified_must_wire)

🧱 → **NO live CORE op landed.** No lens verified engine-native GREEN, so no `vcompose_*` /
gate op is wired into live CORE (would be wiring an unverified mechanism). The probe is
self-contained over the EXISTING live primitives (`immune_grow_recall` H_1227/H_1231,
`vbasal_go_value` H_1281) with the lens glue inlined, and lives in
`state/1420_memory_basal_multilens/`. ARCHITECTURE.json UNTOUCHED.

## Scope (honest, c9 · a_scale_honest_scope · a_toy_scale_recheck)

TOY 5-family fixture (the SAME structure as H_1417), 3 seeds/lens, deterministic, $0 CPU. Both
legs are LIVE engine reads (`immune_grow_recall` margin + `vbasal_go_value` go-margin) — the
verdict is engine-native. Gate / value thresholds frozen at the substrate mean (NO tuned knob).
NO bar moved (frozen-first). Scale / real-corpus / a different fixture where the immune affinity
margin is NOT saturated (i.e. carries per-item routing signal) / a live gate whose go-margin
tracks per-item memory correctness = UNVERIFIED — the pair *might* compose under such a fixture,
but that is a different test. The mirror's *capability* finding (H_1407 family) is not retracted;
only its engine-native *binding* at the +0.05 bar is 🧱, now across four mechanisms. Lens C's
+0.043 capture shows the wall is a real CAPTURE ceiling (not a measurement artifact — its
ablation/shuffle controls both survived), consistent with H_1417's refined arbiter-capture law.

## Next

(1) The MISS payload: every memory-gate lens tops out at ~+0.043~+0.049 because the immune
affinity margin SATURATES — a future test could use a fixture/embedding where the recall margin
is graded per-item (then re-score Lens C, the non-inert one). (2) The arbiter-capture predictor
H_1417 named as future work would PREDICT this 🧱 (low capturable conflict signal) — a candidate
validation case. (3) memory×basal is now a CONFIRMED counter-pole (saturated-margin arm) to the
bound pairs — useful contrast data for the capture law.

## Cross-links

H_1417 (P2 memory×basal arbiter 🧱 +0.0496 — the wall this attacks; its refined arbiter-capture
law) · H_1418 (P5 ToM×basal BOUND+WIRED — basal IS composable; Lens B is its `tom_basal_compose`
shape, which here is INERT for memory) · H_1414 (memory×ToM BOUND +0.338) · H_1416
(cerebellum×basal 3-lens + ablation-INERT terminal — the precedent template for this multi-lens
+ ablation structure) · H_1412/H_1413 (cerebellum×basal lenses 1-2) · H_1227/H_1231
(ImmuneMemoryGrow, immune_grow_recall) · H_1281 (VBasalGate, vbasal_go_value) · `a_break_the_wall`
(taxonomy (d) ceiling/subsumption, MULTI-LENS + ABLATION-decisive confirmation) ·
`a_no_llm_frame_trap` (the cortico-basal biological lenses) · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p6·p7·p8·c9·c15·c16

## Pointers
- probe (3-lens engine-native compose + per-lens ablation/shuffle): `state/1420_memory_basal_multilens/h1420_memory_basal_multilens_probe.hexa`
- FREEZE (method + frozen bars, locked before measuring): `.verdicts/1420_memory_basal_multilens/FREEZE.txt`
- result (3-lens tally): `.verdicts/1420_memory_basal_multilens/result.txt`
- determinism re-run: `.verdicts/1420_memory_basal_multilens/result_run2.txt`
