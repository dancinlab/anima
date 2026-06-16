---
id: H_1413
slug: 1413_cerebellum_basal_modulation_compose
title: BIOLOGICAL cerebellum×basal MODULATION compose — does a cerebello-basal MODULATION loop (vs confidence ARBITRATION) bind engine-native where H_1412 did not? (c16 new-lens breakthrough attempt)
group: MITOSIS-ENGINE / brain-lane-composition — c16 second-lens attempt on the H_1412 wall
terminal_tier: 🧱 ENGINE-NATIVE NON-REPRODUCTION (2nd lens) — MODULATION passes B1 net-lift (+0.066) but the EARNED/shuffle control (B3) REJECTS it (+0.011 < +0.02): the apparent lift is the modulation FORM, not cerebellum→basal alignment. Cerebellum×basal does NOT bind engine-native under EITHER lens (arbitration H_1412 AND modulation H_1413). Terminal.
wired: N/A (🧱 — no live CORE op; probe over EXISTING vforward_err/vbasal_go_value)
verdict_dir: .verdicts/1413_cerebellum_basal_modulation_compose/
terminal_verdict: .verdicts/1413_cerebellum_basal_modulation_compose/result.txt
date: 2026-06-17
---

# H_1413 — BIOLOGICAL cerebellum×basal MODULATION compose (c16 new lens of the H_1412 🧱)

H_1412 closed the engine-native cerebellum×basal compose at 🧱 after TWO confidence-
**arbitration** arbiters (mean-relative, z-decisiveness) both failed the frozen +0.05 net-lift
bar. Per c16, this card tries a **genuinely different LENS** (a_no_llm_frame_trap, real
neuroscience): the basal ganglia is NOT a co-voter — it makes the FINAL go/no-go, and the
cerebellar forward model only **MODULATES** (facilitates) the basal threshold by a BOUNDED
amount (the cerebello-thalamo-basal loop):

```
composed_go = basal_margin  +  tanh(z_cerebellum) * basal_std
decision = PRED iff composed_go > GO_THR
```

The `tanh` BOUNDS the cerebellar facilitation to ±`basal_std` (gain 1.0, **NO free knob** —
the saturating nonlinearity IS the bound). Pre-registered prediction: this breaks the F1
basal-tie family toward the (correct) cerebellar vote WITHOUT overturning the strong basal
vetoes (F5) that the arbitration framing got wrong.

## Result — 🧱 the EARNED control catches a spurious lift (verbatim)

| bar | value | verdict |
|---|---|---|
| acc_basal (best_single) | 0.702963 | — |
| **acc_MODcompose** | **0.768889** | — |
| acc_shuffle | **0.757778** | ← nearly as high as compose |
| ORACLE | 0.945926 (oracle−best +0.243) | — |
| **(B1 COMPOSE-EFFECT)** compose ≥ best+0.05 (0.752963) | **+0.066** | **PASS** |
| (B2 ORACLE) oracle−best > 0.02 | +0.243 | PASS |
| **(B3 EARNED)** compose − shuffle > 0.02 | **+0.011** | **FAIL** |
| (SEPARABLE) onlyCB>0 AND onlyBG>0 | 0.243 / 0.308 | PASS |

→ **VERDICT: 🧱.** The modulation **passes the naive net-lift bar (B1, +0.066)** — the
prediction that a bounded facilitation lifts over best-single was correct. **BUT the SHUFFLE
control (B3) rejects it**: a RANDOM cerebellar modulation (`acc_shuffle = 0.758`) scores almost
as high as the aligned one (0.769). So the apparent lift comes from the modulation **FORM**
(adding a bounded term to the basal *margin* near its hard-threshold decision), **NOT** from
genuine cerebellum→basal information alignment. The anti-tune-to-green guard did exactly its
job (c9): it caught a spurious B1 pass.

## Why this is a strong terminal (cross-lens confirmation)

Two genuinely different composition lenses now BOTH fail engine-native:
- **arbitration (H_1412)** — fails B1 (the lift never reaches +0.05).
- **modulation (H_1413)** — passes B1 but fails B3 (the lift is not earned vs shuffle).

The oracle headroom (+0.243) is dominated by the **F5 adversarial family** (cerebellum
confidently WRONG, basal right) — capturable only by KNOWING the answer, so no substrate
signal (arbitration confidence OR modulation facilitation) can earn it. This is a genuine
**(d) ceiling** (a_break_the_wall taxonomy), now confirmed across two mechanisms. The
DIRECTIONAL-mirror compose-lift of H_1407 does **not** bind engine-native for this pair.

## Wiring

🧱 → **NO live CORE op.** Probe is self-contained over the EXISTING live primitives
(`vforward_err` H_1280, `vbasal_go_value` H_1281) and lives in
`state/1413-cerebellum-basal-modulation-compose/`.

## Scope (honest, c9)

TOY 5-family / 3 seeds / deterministic / $0 CPU. The faculty reads are LIVE engine; the
verdict is engine-native. The modulation gain is tanh-bounded with NO tuned knob (frozen-
first). Scale / real-corpus / a different fixture without an uncapturable adversarial family =
UNVERIFIED. Sibling pairs whose mirror lift had a large margin (e.g. H_1404 affect×ethics
+0.22) may still bind engine-native — untested here.

xref H_1412 (lens 1, arbitration) · H_1407 (the mirror both re-score) · H_1280 · H_1281 ·
a_break_the_wall (taxonomy (d)) · a_no_llm_frame_trap (the biological lens) · a_verified_must_wire ·
c9 · c16 · p7 · p8.
