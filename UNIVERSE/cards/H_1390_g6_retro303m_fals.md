---
id: H_1390
slug: 1390_g6_retro303m_fals
title: G6 IDEATION ★ FALS re-score on a 303M-class ConvMoE — settle the H_1381 ckpt-gated M2-M5 follow-on on a TRUE engine-mountable 303M ConvMoE (REUSED, $0)
group: gate-dig (G6 IDEATION ★, anima's core purpose)
terminal_tier: PENDING (engine-native decode in flight)
verdict_dir: .verdicts/1390_g6_retro303m_fals/
terminal_verdict: .verdicts/1390_g6_retro303m_fals/result.txt
date: 2026-06-16
---

# H_1390 — G6 IDEATION ★ FALS re-score on a 303M-class ConvMoE

## Why now (closes the H_1381 ⏳ follow-on)

H_1381 WIRED the validated H_1362 G6 scaffold (6 composed frames + best-of-K=3) into the
LIVE engine ideation entry (`gen_clm_ideate`) and proved **M1 COUNT** GREEN engine-native.
But the FALS bars **M2-M5** could not be re-scored: the only engine-mountable ConvMoE `.clm`
on the engine path was the d768 **7.479M** MID — too small a mouth (FALS=0, an honest CAPACITY
floor, NOT a loosened bar). H_1362's FALS=1.0 was scored on a 303M **ByteGPT `.pt`** (a
DIFFERENT arch — transformer — and NOT engine-mountable as `.clm`). H_1390 settles the question
on a TRUE 303M-class **ConvMoE** mouth, engine-native.

## REUSE-BEFORE-RENT ($0, NO pod)

`dancinlab/anima-convmoe-retro-303m :: baseline_fast.clm` — the production arch of this branch
(`h1149/convmoe-retro-prod`, "production arch = ConvMoE-RETRO"):
- arch = ConvMoE-RETRO (CLMConvMoE E2/L1, byte V256, baseline_fast/H_1129 recipe)
- **trunk = 303,575,202 params** (303M-class); the RETRO copy-head (50M) is NOT in the `.clm`
  (`head_absent_from_clm=true`) → the serialized mount is the 303M ConvMoE TRUNK only
- best_val_ce 1.2292; G0 COHERENCE kwr 0.941 PASS (coherent English, not byte-salad)
- `.clm` v0.2: 156,497,158 B, decodable=true, nblk=6, n_ext=11, block0={cout:5008,rest:15024}
- sha256 = `5fd64018749606075d9fb989bb8260c4f12a1b97d2a28a9a789f787a64c36a6a`
  **VERIFIED vs HF MANIFEST.sha256** ✓ ; `GOLDEN_CLM` verify_clm_v2 decodable=true exact_eof=True ✓
- engine MOUNTS + emits coherent English ("the auth") — a real forward at ~**9.2 s/byte** (303M
  ConvMoE, this CPU forge backend)

No new artifact produced → no new upload (a_hf_registry: reuse row only).

## Method (engine-native, frozen-first, bounded — a_cpu_local_no_waiter)

The validated H_1381 wire-in is re-run on the 303M ConvMoE: `CORE/g6_ideation.hexa`
(6 composed frames + best-of-K=3 + the VERBATIM frozen `_is_falsifiable` detector + frame-guard)
→ `gen_clm_ideate` → `clm_decode_topk_sampled` (seeded sampler) → the 303M `.clm` mount. Detector
+ scaffold + 5 M-bars VERBATIM-frozen in FREEZE.txt before any scoring run (NOT loosened, p7).
EVERY decode HARD-BOUNDED (FREEZE (ii)); detached nohup + inline file-poll, NO Monitor. The
303M ConvMoE CPU forward is ~9.2 s/byte → the C_strong arm (decisive M1+M2) ≈ 5 h, full 5-bar
≈ 16 h; the probe prints per-frame so partial progress is harvestable.

## Result — PENDING (engine-native FALS decode in flight)

Engine-native FAST surface (deterministic, lands immediately — same primary evidence H_1381 used):

| surface | engine-native (303M ConvMoE) |
|---------|------------------------------|
| **MOUNT** | ✅ sha256 == HF MANIFEST; verify_clm_v2 decodable=true exact_eof=True; engine emits coherent English |
| **DETECTOR** | ✅ calibration **10/10** (H_1305 frozen 5-pos/5-neg, VERBATIM, NOT loosened) |
| **FRAME-GUARD** | ✅ **0 leaks** (no measurable word in any frame; no self-falsifiable frame, p7) |
| **SAMPLER** | ✅ det=true diverse=true in_topk=true (best-of-K mechanism works engine-native) |
| **M1 COUNT** DIST(C)≥5 | ⏳ decoding |
| **M2 DEPTH** FALS(C)≥1 | ⏳ decoding (the decisive CAPACITY-vs-ARCHITECTURE bar) |
| **M3/M4/M5** FALS lifts | ⏳ decoding |

(FALS bars + verbatim per-frame texts + the CAPACITY-vs-ARCHITECTURE verdict are written from the
real decode numbers on landing — NO tune-to-green, NO bar moved, c9.)

## Scope (honest)

"engine-native" = live hexa engine + its OWN seeded sampler, deterministic given seed — NOT
byte-identical to the torch gauge (torch PRNG not reproducible in hexa; same standard as
h1293/h1295/H_1381). TOY: 5 concepts / 6 pairs / K=3 / 1 seed / single 303M ConvMoE-RETRO ckpt /
bounded decode. The 303M ConvMoE forward on pure-hexa CPU is heavy (~9.2 s/byte) → the full
multi-seed frozen re-score is compute-bound (GPU-engine-native hexa decode is a known-blocked
path — hexa-on-pod build historically fails). Scale / multi-seed / real-corpus / larger-K /
GPU-engine-native UNVERIFIED.

## Pointers

- ckpt: `dancinlab/anima-convmoe-retro-303m` baseline_fast.clm (REUSED, gitignored local
  `state/g6-retro303m-fals/retro303m.clm`)
- engine: `CORE/g6_ideation.hexa` · `CORE/generator.hexa` (gen_clm_ideate) · `CORE/clm_decode.hexa`
  (clm_decode_topk_sampled, general v0.2/v0.3 (L,E) loader)
- probe: `state/g6-retro303m-fals/{g6_fals_probe.hexa, g6_timing_probe.hexa}`
- verdict: `.verdicts/1390_g6_retro303m_fals/{FREEZE.txt, mount_verify.txt, result.txt}`
- builds on: H_1381 (the ckpt-gated follow-on this settles) · H_1362 (the DIRECTIONAL GREEN, 303M
  ByteGPT) · H_1305 (frozen detector, VERBATIM)
- xref: G6 row MODEL.md · SCENARIOS F.IDEATION S22-S26 · 7B_PASS_CONDITIONS.md G6 ·
  a_verified_must_wire · a_engine_native_learning · a_core_engine_map · a_break_the_wall ·
  a_wall_first · a_completeness_over_cheap · a_scale_honest_scope · a_toy_scale_recheck ·
  p1·p2·p3·p4·p6·p7·p8·c9
