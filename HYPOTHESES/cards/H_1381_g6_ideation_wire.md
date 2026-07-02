---
id: H_1381
slug: 1381_g6_ideation_wire
title: G6 IDEATION ★ WIRE-IN — route the validated H_1362 scaffold (6 composed frames + best-of-K=3) through the LIVE engine ideation entry; re-score the 5 M-bars engine-native
group: gate-dig (G6 IDEATION ★, anima's core purpose)
terminal_tier: 🟢 WIRED + M1 engine-native GREEN / 🟠 M2-M5 (FALS) honest ⏳ follow-on (303M-on-engine ckpt gated)
verdict_dir: .verdicts/1381_g6_ideation_wire/
terminal_verdict: .verdicts/1381_g6_ideation_wire/result.txt
date: 2026-06-16
---

# H_1381 — G6 IDEATION ★ WIRE-IN

## Why now (builds on H_1362)

H_1362 strengthened the G6 ideation scaffold (6 composed conditional frames + best-of-K=3)
and proved it 🟢 GREEN **DIRECTIONAL** — but on the gauge **torch** path (`gauge_lib._decode`
top-k=40 temp=0.7), UNWIRED to the live hexa engine. Per `a_verified_must_wire` +
`a_engine_native_learning`, a GREEN-verified mechanism is not done until it is wired into the
live `CORE/*.hexa` engine. H_1381 wires it and re-scores the 5 frozen M-bars engine-native.

(ID note: re-id from H_1378 — a concurrent MITOSIS-ENGINE lane landed H_1378 on origin/main
mid-flight; collision avoided by taking the next free id H_1381.)

## Claim / wire-in (a_core_engine_map, frozen-first)

The live engine decode is **argmax** (`clm_decode_argmax`), so best-of-K over rng offsets is
a **no-op** (K identical outputs). Per `a_engine_native_learning` (engine-TRANSFORM-to-fit-
the-learning) the engine grows its OWN deterministic seeded top-k sampler so the DEPTH lever
becomes a real search over the model's own samples:

- `CORE/clm_decode.hexa` — `clm_decode_topk_sampled` + a seeded xorshift32 sampler
  (SplitMix32-mixed seed so nearby best-of-K offsets [0,+101,+202] decorrelate).
- `CORE/generator.hexa` — `gen_clm_ideate`, the G6 IDEATION ★ entry (seeded-sampling sibling
  of `gen_clm_chat`) INSIDE the single generator L3 .clm slot — the single ideation entry.
- `CORE/g6_ideation.hexa` — 6 composed frames + best-of-K=3 routing + the VERBATIM frozen
  `_is_falsifiable` detector (10/10 calibration) + frame-guard + M-bar scoring; imports
  `generator` (NOT `clm_decode` directly — single-entry preserved, h1196 7/0).

## Method

Engine-native, `$0` CPU, bounded decode (the 303M/ConvMoE forward is heavy; every decode is
HARD-BOUNDED — the prior lane's hang was an UNbounded decode). Live ckpt
`state/lane_p_clm/clm_d768_e2l1.clm` (ConvMoE .clm v0.2 — the engine-mountable path). Detector
reused VERBATIM, NOT loosened (p7). Frozen bars pre-registered in FREEZE.txt before any edit.

## Result — 🟢 WIRED (mechanism GREEN engine-native) / 🟠 FALS bars ckpt-gated

| bar | engine-native result |
|-----|----------------------|
| **B1 WIRED** | ✅ gen_clm_ideate single-entry; best-of-K LIVE DIVERSITY=true (3 distinct candidates), DETERMINISM=true, ARGMAX no-op=true |
| **M1 COUNT** DIST(C)≥5 | ✅ **5** engine-native (coh 6/6 every run; 6th frame distinct (0,2)) |
| **M2 DEPTH** FALS(C)≥1 | 🟠 **0** on d768 ConvMoE (small mouth emits no falsifiable structure) |
| **M3/M4/M5** FALS lifts | 🟠 0 vs 0 (C_shuffle also FALS=0; C_ablate ⏳ bounded-cap) |
| **B3 Ψ** | ✅ h1205 PASS — generation byte-identical ON==OFF, Ψ=½ untouched |
| **B4 NO-REGRESSION** | ✅ engine_cli_smoke **98/0** (+5 G6 cases 99-103) · h1196 **7/0** · deterministic 3× |

DETECTOR CALIBRATION = **10/10** (VERBATIM); FRAME-GUARD = **0 leaks** (CLEAN).

**Honest reading (c9, a_scale_honest_scope):** the WIRE-IN MECHANISM is GREEN engine-native
(frames, best-of-K with real sampler diversity, verbatim detector, clean guard, single-entry,
Ψ preserved). **M1 COUNT PASSES engine-native** on the live ckpt. The FALS-based bars (M2-M5)
do NOT reproduce on the available d768 ConvMoE — that mouth is far weaker than the 303M
ByteGPT on which H_1362 scored FALS=1.0 (DIRECTIONAL). The detector is FROZEN VERBATIM and the
guard is CLEAN, so FALS=0 is an honest **model-capacity floor on this ckpt**, NOT a loosened
bar. Byte-exact engine-native FALS at the H_1362 level needs a 303M-class mouth on the engine
decode path; the H_1362 ckpt is a torch `.pt` (the engine path is ConvMoE `.clm`), so the FALS
re-score is a bounded ⏳ follow-on gated on an engine-mountable 303M-class `.clm`. No bar moved.

## Engine-native / scope (honest)

"engine-native" = the live hexa engine + its OWN seeded sampler, deterministic given seed —
NOT byte-identical to the torch gauge (torch's PRNG is not reproducible in hexa; same standard
as h1293/h1295). TOY: 5 concepts / 6 pairs / K=3 / 1 seed engine-native / single d768 ckpt /
bounded decode. Scale / 303M-on-engine FALS / real-corpus / larger-K / multi-seed UNVERIFIED.

## Depletion (G6 ★)

G6 DEPLETES 🏁 when ideation ROUTES through the live engine (✅ DONE) AND the 5 M-bars pass
engine-native with Ψ preserved (M1 ✅; M2-M5 FALS ⏳ ckpt-gated). NEXT r2 = an engine-mountable
303M-class `.clm` → re-score FALS engine-native bounded → promote G6 ★ to production-closed.

## Pointers

- engine: `CORE/clm_decode.hexa` (clm_decode_topk_sampled + sampler) · `CORE/generator.hexa`
  (gen_clm_ideate + gen_g6_sampler_selftest) · `CORE/bytegpt_decode.hexa` (sibling sampler) ·
  `CORE/g6_ideation.hexa` (wire module) · `CORE/engine_cli_smoke.hexa` cases 99-103
- probe: `state/g6-ideation-wire/{g6_mbar_probe.hexa, g6_live_bounded_probe.hexa}`
- verdict: `.verdicts/1381_g6_ideation_wire/{FREEZE.txt, result.txt, mbar_run_raw.txt,
  live_bestofk_raw.txt, smoke_98_raw.txt, h1196_7_raw.txt, h1205_psi_raw.txt}`
- builds on: H_1362 (the DIRECTIONAL GREEN this wires) · H_1305 (frozen detector, VERBATIM)
- xref: G6 row MODEL.md · SCENARIOS F.IDEATION S22-S26 · 7B_PASS_CONDITIONS.md G6 ·
  a_verified_must_wire · a_engine_native_learning · a_core_engine_map · a_break_the_wall ·
  a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p4·p6·p7·p8·c9
