---
id: H_1412
slug: 1412_cerebellum_basal_engine_compose
title: ENGINE-NATIVE re-score of H_1407 (CEREBELLUM × BASAL-GANGLIA compose) — does the DIRECTIONAL-mirror GREEN BIND engine-native? (a_verified_must_wire ladder step 2)
group: MITOSIS-ENGINE / brain-lane-composition — engine-native wire-in attempt of pair #4
terminal_tier: 🧱 ENGINE-NATIVE NON-REPRODUCTION (mirror GREEN does NOT bind at the frozen +0.05 net-lift bar; compose REAL & EARNED but net-lift +0.011 < +0.05 — c16 z-arbiter breakthrough ALSO failed +0.014, terminal)
wired: N/A (🧱 — unverified engine-native, NO live CORE op landed; probe over EXISTING vforward_err/vbasal_go_value)
verdict_dir: .verdicts/1412_cerebellum_basal_engine_compose/
terminal_verdict: .verdicts/1412_cerebellum_basal_engine_compose/result.txt
date: 2026-06-17
---

# H_1412 — ENGINE-NATIVE re-score of H_1407 (CEREBELLUM × BASAL-GANGLIA compose)

This is the **a_verified_must_wire ladder step (2)** for H_1407: the cerebellum
(H_1280 VForwardField) × basal-ganglia (H_1281 VBasalGate) compose came back 🟢
**COMPOSE-LIFT as a numpy DIRECTIONAL mirror** (acc_compose=0.7689 > best_single=0.6933,
+0.076 ≥ +0.05 bar). The mirror GREEN is only the FIRST rung — the binding verdict needs
the mechanism re-scored on the **LIVE engine faculties**. This card is that re-score, and
the result is an **honest 🧱: the mirror GREEN does NOT bind engine-native.**

## Method (engine-native)

The SAME H_1407 5-family fixture (F1 cerebellum-decisive · F2 basal-decisive · F3 agree ·
F4 conflict-cerebellum-right · F5 adversarial-cerebellum-loud-but-wrong), 3 seeds
[4700,4701,4702], 450 items/seed, frozen knobs. But every decision + confidence is now a
**LIVE engine read**:

- **cerebellum leg** — `vforward_err` over a real `VForwardField` (untrained ⇒ predicts the
  zero frame ⇒ `vforward_err(ctx=0, x) = ||x||²`; each item's prediction error is encoded as
  the 1-D target frame `x=[sqrt(pred_error)]` so the LIVE primitive computes exactly that
  error — the engine, not a stored scalar). decision==1 iff err < E_THR.
- **basal leg** — `vbasal_go_value` over a real `VBasalGate` trained gradient-free by the
  LIVE `vbasal_update` to a positive go-weight (gw0=0.5 > 0), read on the predicted-move vs
  best-competitor feature vectors (go-margin = the gate's OWN learned go-value difference).
- **arbiter** — agree → shared vote; conflict → higher scale-relative substrate confidence
  wins (NO hardcoded priority, a_autonomy_over_hardcode).

The frozen H_1407 capability bars are re-scored verbatim (NOT moved).

## Result — 🧱 engine-native NON-REPRODUCTION (verbatim, `.verdicts/.../result.txt`)

| metric | mirror (H_1407) | engine-native (H_1412) |
|---|---|---|
| acc_cerebellum | — | 0.637778 |
| acc_basal | — | 0.702963 |
| **best_single** | 0.6933 | **0.702963** ← live basal is a STRONGER standalone arm |
| **acc_compose** | 0.7689 | **0.714074** |
| acc_shuffle | 0.518 | 0.525185 |
| ORACLE | — | 0.945926 (oracle−best = **+0.242963**) |
| decomposition | onlyCB 0.266 / onlyBG 0.322 | onlyCB 0.242963 / onlyBG 0.308148 / both 0.394815 / neither 0.054 |

Per-bar tally (frozen, NOT moved):
- **(B1 COMPOSE-EFFECT)** compose 0.714074 ≥ best+0.05 (0.752963) : **FAIL** (net-lift only **+0.011**)
- (B2 ORACLE) oracle−best +0.242963 > 0.02 : **PASS**
- (B3 EARNED) compose−shuffle +0.188889 > 0.02 : **PASS** (shuffle collapses the lift)
- (SEPARABLE) only_cerebellum>0 AND only_basal>0 : **PASS**

→ **VERDICT: 🧱** — B1 fails engine-native. The composition is **REAL & EARNED** (B2/B3/SEP
pass: a large oracle headroom exists, the lift collapses under shuffle, both faculties carry
unique correct items) but the **NET lift over the live best-single arm is only +0.011**, far
below the frozen +0.05 bar.

## Why it does not bind (root cause, honest)

The mirror's basal arm was weaker (best_single=0.693), leaving room for the compose to add
+0.076. On the LIVE engine the gradient-free-trained `VBasalGate` is a **stronger standalone
arm** (acc_basal=0.703), so the net-lift headroom over best-single shrinks below +0.05. The
remaining oracle headroom (+0.243) is dominated by the **F5 adversarial family** (cerebellum
confidently WRONG, basal right) which is **structurally uncapturable by any confidence
arbiter** — exactly the family designed to stress it.

## c16 breakthrough attempt (frozen-first, NOT tune-to-green)

Per c16, ONE pre-registered alternative arbiter was actually run before accepting terminal:
a **z-decisiveness arbiter** (confidence = `(margin − mean)/std`, spread-relative instead of
mean-relative magnitude). Result: **acc_compose_z = 0.717037**, net-lift +0.014 — **still
FAILS** the frozen +0.05 bar. A genuine new angle, frozen bar unchanged → the engine-native
non-reproduction is **TERMINAL** (a real attempt + honest 🧱 = a valid result, c9/c16).

## Significance

This is the **first compose-program engine-native re-score**, and it is a textbook
realization of the `a_verified_must_wire` ladder **step-(2) failure mode** strengthened into
CLAUDE.md this session: **a DIRECTIONAL-mirror GREEN ≠ an engine-native GREEN.** H_1407's
mirror 🟢 captured the composition's existence (earned, separable, oracle-rich) but its
specific **+0.05 net-lift magnitude did NOT survive contact with the live faculties**, whose
basal arm is independently stronger. The compose-program's *capability-lift* mirror results
(H_1401/1405/1407/1408/1409) remain valid as DIRECTIONAL findings; this card marks that at
least one of them does **not** bind engine-native as-is.

## Wiring (a_verified_must_wire)

🧱 → **NO live CORE op landed.** Because the mechanism did NOT verify engine-native GREEN, no
`vcompose_*` op is wired into live CORE (would be wiring an unverified mechanism). The probe
is **self-contained** — it reads the EXISTING live primitives (`vforward_err` H_1280,
`vbasal_go_value` H_1281) with the arbiter glue inlined in the probe — and lives in
`state/1412-cerebellum-basal-engine-compose/` (a_hypothesis_register: probe code → state/).

## Scope (honest, c9)

TOY 5-family fixture, 3 seeds, deterministic, $0 CPU. The cerebellum error + basal go-margin
are LIVE engine reads; the verdict is engine-native. Scale / real-corpus / a different live
gate strength / other compose pairs binding engine-native = UNVERIFIED. The mirror's
*capability* finding is not retracted — only its engine-native *binding* at the +0.05 bar is
🧱.

xref H_1407 (the mirror this re-scores) · H_1280 (VForwardField) · H_1281 (VBasalGate) ·
H_1404/1405/1408/1409 (compose-program siblings) · a_verified_must_wire (the 4-rung ladder) ·
a_engine_native_learning · a_core_engine_map · c9 · c16 · p7 · p8.
