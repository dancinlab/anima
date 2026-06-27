---
id: H_1590
slug: 1590_g6_scaffold_repro
title: G6 IDEATION ★ scaffold ENGINE-NATIVE reproduction — apply H_1362's (H_1305 6 composed frames + best-of-K=3, frozen detector) recipe to the SAME h1129 303M ByteGPT, engine-native (hexa via live CORE / py numpy-only), to isolate whether the G6 wall lever is decode-procedure (scaffold) or attention-capacity
group: gate-dig (G6 IDEATION ★, anima's core purpose)
terminal_tier: ⏳ BLOCKED-INFRA (host-instability/substrate-speed wall, a_break_the_wall type-c · NOT a science verdict · engine-native decode = ING follow-on on a stable host)
verdict_dir: state/verdicts/1590_g6_scaffold_repro/
terminal_verdict: state/verdicts/1590_g6_scaffold_repro/result.txt
date: 2026-06-27
wired: engine-native (numpy-only py 2-production + hexa live CORE op; NOT torch)
---

# H_1590 — G6 IDEATION ★ scaffold ENGINE-NATIVE reproduction

## Why now (settle H_1362 torch-vs-engine)

H_1362 reported a G6 ★ "BREAKTHROUGH" (C_strong FALS=1.0, M1-M5 all PASS) on h1129 303M
ByteGPT — but on the **torch** path (`gauge_lib._decode` top-k=40 temp=0.7) = **DIRECTIONAL**,
never engine-native reconfirmed (the "R2 follow-on" stayed open). H_1381 wired the scaffold
into the live engine but only had a weak d768 ConvMoE `.clm` → engine-native FALS=0 (honest
capacity floor on that ckpt). H_1587 documented that torch-GREEN diverges from engine-native
on the very same h1129. The bare frozen G6 ladder (no scaffold) is **fals=0 GENUINE** on h1129
engine-native (M② / H_1595, py 2-production, seed-robust). So the question stands: **is the
scaffold (decode-procedure) the real G6 lever, or was H_1362 FALS=1.0 a pure torch artifact?**

## Claim / falsifier (frozen-first, bar 불변)

Apply the H_1362 scaffold recipe **VERBATIM** to the SAME h1129 303M ByteGPT ckpt
(sha 5cf07a36), but **engine-native** (the wired live ops, NO torch / NO gauge_lib):
- decode via the single L3 ideation entry `gen_auto_ideate` (core/generator.hexa → sniffs
  ByteGPT → `gen_bytegpt_ideate` → `bytegpt_decode_topk_sampled_ranged`), and scoring via the
  FROZEN wired ops in `core/g6_ideation.hexa` (`g6_build_frames`, `g6_frame_guard`,
  `g6_detector_calibration`, `_g6_is_falsifiable`/`_g6_known_word_ratio`/`_g6_jaccard`).
- py twin: `core/g6_ideation.py` ← `core/bytegpt_decode.py` (numpy-only = engine-native TERMINAL).

Arms (H_1362 VERBATIM): A_flat (flat IDEATION_SEEDS single-sample, sanity = fals 0) ·
B_composed (5 composed frames single) · **C_strong** (6 composed frames + best-of-K=3) ·
C_k1 (6 frames + best-of-K=1, decomposition) · **C_shuffle** (deranged pairing + K=3, the
H_1434/H_1449 binding control) · C_ablate (lone concept + K=3). GEN=110 (MAX_NEW VERBATIM,
NOT moved). Seeds {7,4302,4303}. Frozen M-bars M1 DIST(C)≥5 · M2 FALS(C)≥1 · M3 FALS(C)>FALS(B)
· M4 FALS(C)>FALS(shuffle) · M5 FALS(C)>FALS(ablate).

VERDICT logic: **GREEN** = closed AND C_shuffle collapses (decode-procedure/scaffold IS the
G6 lever → no retrain; wire scaffold to production, H_1381 revival). **RED** = FALS=0 engine-
native (H_1362 was a torch artifact, H_1587 confirmed → lever = attention-capacity, H_1449,
GPU retrain, cost-gated — pre-register only) OR FALS rises but C_shuffle does NOT collapse
(token-presence artifact, not binding).

## Method (engine-native, grep-clean)

- hexa harness `state/1590_g6_scaffold_repro/g6_scaffold_repro_bytegpt.hexa` — imports
  `core/g6_ideation.hexa` + `core/generator.hexa`; best-of-K ranking (offsets [0,101,202],
  rank (fals,kwr)) IDENTICAL to `g6_decode_best_of_k`, routed through `gen_auto_ideate`
  (ByteGPT mouth) instead of CLM-only — only the mouth handle differs, scoring/detector are
  the wired frozen ops. One seed per invocation.
- py twin `state/1590_g6_scaffold_repro/h159x_g6_scaffold_repro.py` — imports `core/g6_ideation.py`
  + `core/bytegpt_decode.py`, loads W once, best-of-K via `bytegpt_decode_topk_sampled_W`.
- grep self-check `grep -lE 'import torch|gauge_lib._decode'` = CLEAN (only a docstring mentions
  what H_1362 did; zero torch/gauge_lib import or call). numpy = engine-native TERMINAL per
  a_engine_native_learning. Detector calibration = **10/10 engine-native**; frame-guard CLEAN.
- POOL host (aiden/summer RTX5070), NOT mini. ckpt sha 5cf07a36 (matches mini source).

## Result — ⏳ BLOCKED-INFRA (NOT a science verdict, c9; NO bar moved)

VALIDATED engine-native (harvested header, both host runs):
`MOUTH_KIND=bytegpt · CUDA_AVAILABLE=1 · DETECTOR_CALIBRATION=10/10 · FRAME_GUARD_LEAKS=0`.
py twin computed at 820% CPU (A_flat frame1 = 208s; no KV-cache in py bytegpt decode).

**BLOCKED:** the engine-native decode could NOT complete on the available pool hosts. Repeatedly
this session (2026-06-27): aiden (RTX5070) rebooted **3×** (up 8m→4m→6m→0m), summer rebooted ≥2× /
went unreachable — each reboot killed the setsid-detached job. Every hexa decode HUNG at 0% CPU
AND 0% GPU after the header (GPU never fired despite cuda=1); the py path computes but at CPU
speed (~200s/frame, no KV-cache) → the full 6-arm × 3-seed run (~12 h) cannot fit inside the
hosts' minutes-long uptime. This is the SAME class as H_1305 R2's "substrate-speed infra wall"
(a_break_the_wall **type-c** = fix the substrate, NOT a science ceiling; c9 측정/인프라벽 ≠ verdict).

**No arm result was obtained → ZERO C_strong FALS/DIST/cross-shuffle reported (no fabrication,
no tune-to-green).** The H_1362 decode-procedure-vs-attention-capacity question stays OPEN
engine-native. Harness + py twin are turnkey; the engine-native measurement is the ING follow-on
`h1590_engine_native_g6_scaffold`, to run on a stable GPU host (rented CUDA-devel pod) or a
KV-cache py decode:
`hexa run state/1590_g6_scaffold_repro/g6_scaffold_repro_bytegpt.hexa -- <h1129.bin> <seed> 110`
for seeds {7,4302,4303} → fill arm table + M1-M5 + cross-shuffle → GREEN(decode-lever)/RED
(torch-artifact+attention-lever).

## Pointers

- hexa harness: `state/1590_g6_scaffold_repro/g6_scaffold_repro_bytegpt.hexa`
- py twin: `state/1590_g6_scaffold_repro/h159x_g6_scaffold_repro.py`
- verdict: `state/verdicts/1590_g6_scaffold_repro/`
- reuses VERBATIM (frozen, NOT loosened): `core/g6_ideation.{hexa,py}` detector+frames+best-of-K,
  `core/bytegpt_decode.py` / `gen_auto_ideate` mouth
- xref: H_1362 (the torch DIRECTIONAL this reconfirms) · H_1305 (frozen detector+frames) ·
  H_1381 (the wire-in, d768 capacity floor) · H_1587 (torch≠engine divergence) · H_1595 (bare
  ladder fals=0 GENUINE) · H_1449 (attention-capacity lever) · H_1434 (cross-shuffle binding
  control) · a_engine_native_learning · a_break_the_wall · a_verified_must_wire · p7 · c9
