---
id: H_1403
slug: 1403_convmoe_streaming_decode
title: STREAMING / BOUNDED ConvMoE .clm decode — FIX the per-step memory blowup that substrate-BLOCKED the H_1392 G6 FALS re-score, then re-score M2-M5 engine-native
group: engine-fix (CORE/clm_decode, a_clm_gen_pipeline · a_core_engine_map · a_verified_must_wire)
terminal_tier: 🟢 GREEN memory FIX (byte-exact + flat RSS; GEN=110 unblocked) · G6 M2-M5 re-score now MEASURABLE → 🧱 ARCHITECTURE verdict (FALS=0 over 6/6 GEN=110 C_strong frames — capacity was NOT the lever; a REAL science result, no longer a substrate block)
verdict_dir: .verdicts/1403_convmoe_streaming_decode/
terminal_verdict: .verdicts/1403_convmoe_streaming_decode/result.txt
date: 2026-06-17
---

# H_1403 — STREAMING / BOUNDED ConvMoE .clm decode (the H_1392 memory-blowup FIX)

## Why (closes the H_1392 🧱 substrate wall — a_break_the_wall)

H_1392 found the 303M ConvMoE-RETRO `.clm` MOUNTS + decodes but the hexa ConvMoE decode BLOWS UP
MEMORY ~+300 MB/step (never freed) → GEN=24 OOM-killed @11 GB, GEN=48 SIGTERM, GEN=110 silent
death. A falsifiable G6 claim needs GEN≈80-110, so the M2-M5 FALS bars carried NO engine-native
score (substrate-BLOCKED, NOT FALS=0), leaving CAPACITY-vs-ARCHITECTURE OPEN. The wall was filed
upstream (hexa-lang inbox). H_1403 treats it as **wrong-method, not a ceiling** and FIXES it
anima-side.

## Root cause (measured, /usr/bin/time -l)

The hexa runtime (`self/runtime.c`) is a one-shot **BUMP allocator**: `free()` is a NOOP
("Cycle 53 — mmap-backed bump allocator. malloc never frees; free is a noop") and
`hexa_farr_free` recycles the handle SLOT but the backing buffer bytes are **NEVER returned**. So
every per-step `t_zeros` + every internal `forge_dispatch_matmul` output permanently consumes
memory, regardless of the careful `t_free` calls in `_clmd_fwd_logits`. Per-step alloc breakdown
(d768/T24, computed **== measured 63.1 MB/step**):

| term | MB/step | note |
|------|---------|------|
| conv-weight TRANSPOSE `Wt` | **58.2 (92%)** | rebuilt EVERY step though weights are CONSTANT |
| im2col `xcol` | 1.3 | causal-pad gather |
| forge matmul outputs (`mm`) | 0.6 | runtime-internal — the residual floor |
| other activation scratch | 2.2 | xe/xt/h/hn/hg/ex_out/... |

A SECOND face of the same leak: each `clm_decode_*` call re-ran `_clmd_load(path)` (the full model
weights, ~10 GB for 303M) which also never frees → a multi-decode driver (G6 = 69 decodes) OOMs
**across** decodes.

## Fix (anima-side, CORE/clm_decode.hexa — BYTE-EXACT, NOT an arithmetic change)

1. **Streaming forward** (`_clmd_scratch_new` + `_clmd_fwd_logits_sc` + `_clmd_conv1d_pre`):
   pre-transpose EVERY conv weight + pre-allocate ALL forward scratch ONCE; reuse those farr
   handles every decode step. A reused handle keeps its already-mmap'd buffer → no new bump bytes
   → RSS goes FLAT. The 3 decode loops (`argmax` / `topk_sampled` / `grounded`) build the scratch
   once before the loop.
2. **Load-once** (`clm_load_weights` + `clm_decode_topk_sampled_W` + `gen_clm_ideate_W` +
   `g6_decode_best_of_k_W`): the multi-decode driver loads the model ONCE and reuses `W` across
   all decodes (bounds the cross-decode reload leak).

The original `_clmd_fwd_logits` is kept BYTE-IDENTICAL for the bounded single-shot CE/omega
measurements (`clm_forward_ce`, `clm_omega_closure`). a_core_engine_map preserved: still the
single `.clm` slot reached only via the generator L3 slot (h1196 7/0).

## Guards (frozen-first, FREEZE.txt — ALL hold)

| guard | result |
|-------|--------|
| **G1 BYTE-EXACT forward** | `_clmd_fwd_logits_sc` vs `_clmd_fwd_logits`, same tok window: **maxΔ = 0.0** over all 6144 logits (bit-exact) |
| **G2 BYTE-EXACT decode** | argmax seq byte-identical BEFORE==AFTER at GEN≤16 (held to 32+); topk det run1==run2; loaded-W == path |
| **G3 FLAT RSS (d768)** | per-step leak **63 MB/step → 0.64 MB/step** (~100×); GEN=128 max RSS **5397 MB → 415 MB** (13×); also ~3.7× faster (no re-transpose) |
| **G4 regression** | engine_cli_smoke **119/0** · h1196 single-entry **7/0** · h1205 separation-invariant **PASS** (F1 byte-identity 0 mismatch, F2 Ψ Φ-checksum invariant) |
| **G5 303M unblock** | GEN=24 (was OOM @11GB) **RC=0 10.3GB** · GEN=48 (was SIGTERM) **RC=0 10.6GB** · **GEN=110 completes** 10.1GB RSS / 13.0GB peak (vs H_1392 silent death / 71GB peak); per-step 300MB→~10.7MB |

## Result — G6 M2-M5 FALS re-score (VERBATIM the H_1392 frozen probe, NO bar moved)

The fix makes the H_1392 frozen G6 probe RUNNABLE engine-native on the real 303M ConvMoE-RETRO
mount (sha256 == HF MANIFEST ✓). Detector 10/10 VERBATIM · frame-guard 0 leaks · sampler
det/diverse/in_topk true · model LOADED ok=true (d=5008,E2,V256,L1). GEN=110 completes (133.6 s,
10.1 GB). The M1-M5 bars are scored engine-native — the now-MEASURABLE CAPACITY-vs-ARCHITECTURE
answer H_1392 left OPEN. **Scores: `.verdicts/1403_convmoe_streaming_decode/g6_rescore.txt`
(verbatim, no tune-to-green, NO bar moved).**

**🧱 ARCHITECTURE verdict (the honest, now-measurable answer):** over **6/6 completed GEN=110
C_strong best-of-K=3 frames**, **FALS(C_strong) = 0** — the 303M ConvMoE mouth produces COHERENT
English (kwr 0.90-1.00) but NO falsifiable structure (no comparator+measurable+≥2-content-word
claim) even at the FULL falsifiability budget. Per the pre-registered FREEZE rule, M2 FALS=0
(no longer memory-capped) ⇒ **the lever is ARCHITECTURE, not capacity** — capacity (303M) was NOT
the open lever H_1392 left. H_1362's FALS=1.0 was a 303M **ByteGPT** (a different, transformer
arch); the ConvMoE does not reproduce it engine-native. M3-M5 (lift/earned over FALS=0) are moot.
This is a **REAL science result** now that the substrate no longer blocks the decode — NOT a
substrate wall (H_1392), NOT tune-to-green. C_strong[0] reproduced byte-identical in a fresh
process (determinism confirmed). The full multi-arm fresh-process re-score (run_g6_fresh.sh, one
process/frame so the bump-allocator leak resets per frame) continues landing the control arms for
completeness; they cannot overturn M2=0.

## Scope (honest)

The memory fix is byte-exact and validated on BOTH the d768 7.479M model (full RSS curve) and the
303M ConvMoE-RETRO (GEN=8/16/24/48/110). "engine-native" = the live hexa engine + its OWN seeded
sampler, deterministic given seed, NOT byte-identical to the torch gauge (same standard as
H_1381/h1293/h1295). The residual ~0.6 MB/step (d768) / ~10.7 MB/step (303M) is the runtime's
internal `forge_dispatch_matmul` output allocation — an UPSTREAM bump-allocator floor (an into-
output matmul variant would zero it; filed to hexa-lang). The 303M decode is still heavy
(~1.2 s/byte CPU forge); multi-seed / real-corpus / GPU-engine-native UNVERIFIED.

## Pointers

- CORE: `CORE/clm_decode.hexa` (`_clmd_scratch_new`/`_clmd_fwd_logits_sc`/`_clmd_conv1d_pre`,
  `clm_load_weights`/`clm_decode_topk_sampled_W`) · `CORE/generator.hexa` (`gen_clm_ideate_W`) ·
  `CORE/g6_ideation.hexa` (`g6_decode_best_of_k_W`)
- probe: `state/1403_convmoe_streaming_decode/{rss_probe.hexa, rss_probe_303m.hexa, g6_fals_probe_loaded.hexa}`
- verdict: `.verdicts/1403_convmoe_streaming_decode/{FREEZE.txt, byte_exact.txt, rss_before.txt,
  rss_after.txt, rss_after_303m.txt, g6_rescore.txt, result.txt}`
- ckpt: `dancinlab/anima-convmoe-retro-303m` baseline_fast.clm (REUSED, sha256-verified, gitignored
  local `state/g6-retro303m-fals/retro303m.clm`)
- builds on / supersedes: H_1392 (the wall this fixes) · H_1381 (G6 wire-in) · H_1362 (the
  DIRECTIONAL GREEN). Upstream handoff `hexa-lang/inbox/patches/clm-convmoe-303m-decode-memory-blowup.md`
  — anima-side streaming fix landed; the residual matmul-output floor stays a (much smaller) upstream item.
- xref: a_clm_gen_pipeline · a_core_engine_map · a_verified_must_wire · a_engine_native_learning ·
  a_break_the_wall · a_wall_first · a_scale_honest_scope · a_toy_scale_recheck · p7 · p8 · c9
