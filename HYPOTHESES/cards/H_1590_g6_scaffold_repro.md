---
id: H_1590
slug: 1590_g6_scaffold_repro
title: G6 IDEATION ★ scaffold ENGINE-NATIVE reproduction — apply H_1362's (H_1305 6 composed frames + best-of-K=3, frozen detector) recipe to the SAME h1129 303M ByteGPT, engine-native (hexa via live CORE / py numpy-only), to isolate whether the G6 wall lever is decode-procedure (scaffold) or attention-capacity
group: gate-dig (G6 IDEATION ★, anima's core purpose)
terminal_tier: 🔴 RED — scaffold does NOT lift G6 falsifiability engine-native (C_strong FALS=0.0 all 3 seeds); H_1362 FALS=1.0 was a torch artifact (H_1587 CONFIRMED). G6 lever != decode-procedure/scaffold = attention-capacity (H_1449, GPU, cost-gated). Frozen bars UNMOVED.
verdict_dir: state/verdicts/1590_g6_scaffold_repro/
terminal_verdict: state/verdicts/1590_g6_scaffold_repro/result.txt
date: 2026-06-27
wired: engine-native (numpy-only py 2-production, KV-cache; NOT torch). UNBLOCKED on mini CPU $0 by porting KV-cache to core/bytegpt_decode.py (byte-exact ON==OFF).
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

## Result — 🔴 RED (engine-native TERMINAL, mini CPU $0, 1600s)

**UNBLOCKED:** the prior ⏳ BLOCKED-INFRA (pool reboot-loop) was resolved by porting the KV-cache to
`core/bytegpt_decode.py` (PR-twin of `decode.hexa` #2602) — the py bytegpt decode was O(gen²)
(~200s/frame) which is what forced the doomed pool runs. With KV-cache the full 6-arm × 3-seed run
completed on **mini CPU in 1600s (~27 min), $0, no GPU/pool**. KV-cache is byte-exact (ON vs OFF
token-identical, see below), so these verdict numbers are unchanged by the optimization.

Engine-native (grep-clean, `core/g6_ideation.py` ← `core/bytegpt_decode.py`, numpy-only = TERMINAL):
`MOUTH=bytegpt · DETECTOR_CALIBRATION=10/10 · FRAME_GUARD_LEAKS=0 · ckpt sha 5cf07a36`.

| arm | DIST (mean) | FALS (mean) | per-seed FALS |
|---|---|---|---|
| A_flat | 5.0 | 0.0 | [0,0,0] |
| B_composed | 5.0 | 0.0 | [0,0,0] |
| **C_strong** (6 frames + best-of-K=3) | **6.0** | **0.0** | **[0,0,0]** |
| C_k1 (6 frames + best-of-K=1) | 6.0 | 0.0 | [0,0,0] |
| C_shuffle (deranged pairing + K=3) | 5.0 | 0.333 | [1,0,0] |
| C_ablate (lone concept + K=3) | 5.0 | 0.0 | [0,0,0] |

Frozen M-bars: M1 DIST≥5 **PASS** (6.0) · M2 FALS≥1 **FAIL** (0.0) · M3 FALS(C)>FALS(B) **FAIL** (0=0) ·
M4 FALS(C)>FALS(shuffle) **FAIL** (0<0.333) · M5 FALS(C)>FALS(ablate) **FAIL** (0=0). **closed_G6=False ·
cross-shuffle collapsed=False · best-of-K lift(K3>K1)=False.**

**RED — both failure modes fire:**
1. **C_strong FALS=0.0 on all 3 seeds** → the H_1362 "BREAKTHROUGH" FALS=1.0 was a **torch decode
   artifact** (`gauge_lib._decode`), NOT reproducible on the live engine. Confirms H_1587 torch≠engine
   and is consistent with H_1595 (GENUINE seed-robust fals=0) + H_1597 (not a detector artifact).
2. **cross-shuffle did NOT collapse** — C_shuffle FALS=0.333 > C_strong 0.0 (M4 inverts). The lone
   seed-7 shuffle FALS=1 is a token-presence accident, NOT real binding; if the scaffold were genuine
   composition binding, deranged pairing would collapse fals below C_strong. **best-of-K is a no-op**
   for falsifiability (K3==K1==0). DIST=6 + coherent 6/6 = distinct coherent prose; the wall is
   SPECIFICALLY the falsifiability sub-metric.

**Conclusion:** the G6 IDEATION ★ lever is **NOT decode-procedure/scaffold = attention-capacity**
(H_1449, GPU retrain, cost-gated, pre-register-only — NOT fired). H_1381 scaffold wire-in revival is
REFUTED for h1129 (no engine-native effect). Frozen bars UNMOVED (no tune-to-green, p7).

### KV-cache byte-exactness gate (`state/1590_g6_scaffold_repro/kv_parity.py`, h1129, mini)
PARITY **PASS** — KV-cache ON vs OFF (forced full-forward) token streams **byte-identical**:
gen=12 argmax✓ sampled✓ (logits max|Δ|=3.02e-14 FP-reassoc, argmax-stable); gen=110 argmax✓ sampled✓,
**speedup 15.9× argmax (1014→64 ms/tok) · 10.1× sampled**. → pure perf optimization; H_1590 numbers
identical with/without it. py twin now at 2-production parity with `decode.hexa` KV-cache.

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
