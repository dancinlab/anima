---
id: H_1416
slug: 1416_cerebellum_basal_sequential_compose
title: SEQUENTIAL cerebellum→basal PIPELINE compose — does a cerebello-basal-thalamo-cortical LOOP (cerebellum REFINES the basal INPUT before the gate fires, vs ARBITRATION H_1412 / MODULATION H_1413) bind engine-native? (c16 THIRD-lens breakthrough attempt on the cerebellum×basal wall)
group: MITOSIS-ENGINE / brain-lane-composition — c16 THIRD-lens attempt on the H_1412/H_1413 wall
terminal_tier: 🧱 ENGINE-NATIVE NON-REPRODUCTION (3rd lens) — SEQUENTIAL pipeline (cerebellum reliability REFINES the LIVE basal INPUT, then the single gate fires) FAILS all three discriminators: B1 net-lift +0.00 (seq 0.7015 ≈ best 0.7030 < +0.05), B3 EARNED/shuffle +0.0156 < +0.02, AND the ABLATION shows refinement-OFF scores the SAME (−0.0015) — the cerebellar refinement is INERT at the gate's hard threshold. Cerebellum×basal does NOT bind engine-native under ANY of THREE lenses (arbitration H_1412 B1-fail · modulation H_1413 B3-fail · sequential pipeline H_1416 B1+B3+ABL-fail). CONFIRMED TERMINAL.
wired: N/A (🧱 — no live CORE op; probe over EXISTING vforward_err/vbasal_go_value)
verdict_dir: .verdicts/1416_cerebellum_basal_sequential_compose/
terminal_verdict: .verdicts/1416_cerebellum_basal_sequential_compose/result.txt
date: 2026-06-17
---

# H_1416 — SEQUENTIAL cerebellum→basal PIPELINE compose (c16 THIRD lens of the H_1412/H_1413 🧱)

H_1412 (arbitration) and H_1413 (modulation) both closed the engine-native cerebellum×basal
compose at 🧱. Both **combined the two confidence signals at decision time** — arbitration let
them vote, modulation added a bounded cerebellar term to the basal margin. Per c16
(a_break_the_wall) this card tries a **genuinely different LENS** (a_no_llm_frame_trap, real
neuroscience): the **SEQUENTIAL cerebello-basal-thalamo-cortical LOOP**.

In the real loop the cerebellum's forward model does **NOT vote against** the basal gate's
output — it **REFINES the cortical STATE ESTIMATE the basal gate READS, BEFORE the gate
fires**. So the principled compose is a **PIPELINE (cerebellum→basal)**, not parallel:

```
reliability  rel = clamp((E_THR − vforward_err)/E_THR, 0, 1)   // 1 when forward model sure, 0 when err≥E_THR
refined_pred_feat = pred_feat + REFINE_GAIN * rel              // cerebellum nudges the released-move feature
refined_comp_feat = comp_feat                                  // competitor unchanged
go_margin_refined = vbasal_go_value(bg,[refined_pred]) − vbasal_go_value(bg,[refined_comp])
decision = SELECT-PREDICTED iff go_margin_refined > GO_THR     // the SINGLE LIVE gate fires on the corrected state
```

`REFINE_GAIN` is FROZEN at the gate's go-value unit (1.0, **NO tuned knob** — the reliability
clamp ∈[0,1] and the fixed gain ARE the bound). Pre-registered prediction: refining the basal
INPUT (gated by the cerebellum's *genuine* per-item reliability) should survive the shuffle
where H_1413's *form*-modulation did not, because a SHUFFLED reliability applies the wrong
item's reliability to the wrong item's feature.

## Result — 🧱 the pipeline is INERT at the gate (verbatim, `.verdicts/.../result.txt`)

| bar | value | verdict |
|---|---|---|
| acc_cerebellum | 0.637778 | — |
| acc_basal (best_single) | 0.702963 | ← strong standalone live arm |
| **acc_seqcompose** | **0.701481** | — |
| acc_shuffle | 0.685926 | — |
| **acc_ablate** (refinement OFF) | **0.702963** | ← IDENTICAL to plain basal |
| ORACLE | 0.945926 (oracle−best +0.242963) | — |
| **(B1 COMPOSE-EFFECT)** seqcompose ≥ best+0.05 (0.752963) | **0.701481** | **FAIL** (net-lift ≈ +0.00, actually −0.0015) |
| (B2 ORACLE) oracle−best > 0.02 | +0.242963 | PASS |
| **(B3 EARNED)** seqcompose−shuffle > 0.02 | **+0.0156** | **FAIL** |
| **(ABLATION)** seqcompose−ablate > 0 | **−0.0015** | **FAIL** |
| (SEPARABLE) onlyCB>0 AND onlyBG>0 | 0.243 / 0.308 | PASS |

→ **VERDICT: 🧱.** The sequential pipeline fails THREE ways at once, the most decisive of the
three lenses:
- **B1**: the refined gate (0.7015) does not even reach plain best-single (0.7030) — net-lift ≈ 0.
- **ABLATION**: turning the refinement OFF (`REFINE_GAIN→0`) scores **identically** (0.702963)
  — the cerebellar refinement is **INERT**. The basal go-margins in the decisive families
  (F2/F4/F5: |go_margin| ≈ 0.45–0.6) are far from the gate's hard threshold, so adding a
  bounded `rel·1.0` nudge to the released-move feature does **not flip any decision** that the
  basal gate did not already make. Where the cerebellum is reliable (F1/F3/F4), the basal gate
  is *already* correct or already wrong for its own reasons; the input correction changes nothing.
- **B3**: even the tiny apparent movement isn't earned — a shuffled reliability scores nearly as high.

## Why this is a STRONG terminal (THREE-lens cross-confirmation)

Three genuinely different composition lenses now ALL fail engine-native:
- **arbitration (H_1412)** — two confidence votes; fails B1 (lift never reaches +0.05; +0.011, z-arbiter +0.014).
- **modulation (H_1413)** — bounded cerebellar facilitation of the basal *margin*; passes B1 (+0.066)
  but fails B3 (shuffle survives — the lift was the *form*, not alignment).
- **sequential pipeline (H_1416)** — cerebellum refines the basal *input* before the gate; fails
  B1 **and** B3 **and** the ablation (the refinement is inert at the gate's hard threshold).

The root cause is unchanged and now triply confirmed: the LIVE `VBasalGate`
(`vbasal_go_value`, gw0=0.5 learned gradient-free) is a **strong standalone arm**
(acc_basal=0.703) whose decisive go-margins sit FAR from its threshold, so no cerebellar
signal — voting (H_1412), margin-modulating (H_1413), or input-refining (H_1416) — moves the
decision. The oracle headroom (+0.243) is dominated by the **F5 adversarial family**
(cerebellum confidently WRONG, basal right), capturable only by KNOWING the answer. This is a
genuine **(d) ceiling / strong-standalone-arm subsumption** (a_break_the_wall taxonomy),
confirmed across THREE mechanisms. The DIRECTIONAL-mirror compose-lift of H_1407 does **not**
bind engine-native for this pair under any lens tried.

Contrast (the law is pair-dependent, not universal): the MEMORY-adjacent pairs H_1414
(memory×ToM, +0.338) and H_1415 (spatial×episodic, +0.058) BOTH bound + wired engine-native —
pairs where neither standalone arm dominates. Cerebellum×basal is the counter-pole: a pair
where one arm (basal) is independently strong and thresholded.

## Wiring (a_verified_must_wire)

🧱 → **NO live CORE op landed.** The mechanism did NOT verify engine-native GREEN, so no
`vcompose_*`/pipeline op is wired into live CORE (would be wiring an unverified mechanism). The
probe is self-contained over the EXISTING live primitives (`vforward_err` H_1280,
`vbasal_go_value` H_1281) with the refine→gate glue inlined, and lives in
`state/1416-cerebellum-basal-sequential-compose/`.

## Scope (honest, c9)

TOY 5-family fixture (VERBATIM the H_1407 items), 3 seeds [4700,4701,4702], deterministic, $0
CPU. The cerebellum reliability = LIVE `vforward_err`; the basal decision = LIVE
`vbasal_go_value` on the cerebellum-REFINED input — the verdict is engine-native.
`REFINE_GAIN` frozen at the gate's go-value unit (1.0), reliability clamp ∈[0,1], NO tuned
knob (frozen-first). NO bar moved. Scale / real-corpus / a different fixture without an
uncapturable adversarial family / a live gate whose decisive margins sit NEAR threshold =
UNVERIFIED — the pair *might* compose under a fixture where the basal arm is less dominant, but
that is a different test. The mirror's *capability* finding (H_1407) is not retracted; only its
engine-native *binding* at the +0.05 bar is 🧱, now across three lenses.

xref H_1412 (lens 1, arbitration) · H_1413 (lens 2, modulation) · H_1407 (the mirror all three
re-score) · H_1414/H_1415 (the contrast — MEMORY pairs that DID bind+wire) · H_1280
(VForwardField) · H_1281 (VBasalGate) · a_break_the_wall (taxonomy (d), three-lens
confirmation) · a_no_llm_frame_trap (the biological pipeline lens) · a_verified_must_wire ·
a_engine_native_learning · c9 · c16 · p7 · p8.
