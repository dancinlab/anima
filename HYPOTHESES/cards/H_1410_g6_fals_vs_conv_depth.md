# H_1410 — G6 IDEATION ★ FALS vs CONV-DEPTH (deep-mouth depth ladder L1→L4→L8)

slug: `1410_g6_fals_vs_conv_depth` · date 2026-06-17 · substrate **aiden-pool-CPU** (hexa `.clm` engine-native decode, NOT GPU — RTX 5070 미활용 측정확인) · frozen-first (c9, p7)

## CLAIM (the deep-mouth science)

H_1394 (E2/L1 303M ConvMoE) gave G6 **FALS=0**; H_1362's FALS=1.0 was a 303M ByteGPT
(L24 **transformer**, 다른 arch). H_1403 re-confirmed 303M ConvMoE-RETRO (L1) FALS=0
engine-native over 6/6 GEN=110 C_strong frames → 🧱 ARCHITECTURE (capacity was NOT the lever).

**OPEN:** was L1 the conv-FAMILY ceiling, or just the shallowest rung? The deep-mouth ladder
trained two deeper rungs at MATCHED ~303M params (width-compensated, clean depth⊥capacity):

| rung | trunk layers | d | params | eval_ce | sha256 |
|------|---|---|---|---|---|
| L4 | 4 | 3784 | 302.701M | 1.37688 | `34d40c9f…48f48a53` |
| L8 | 8 | 3020 | 302.613M | 1.36468 | `42f2dc3f…1e39a520959` |

**BAR:** does conv-DEPTH (L4, L8) LIFT FALS over the L1 H_1394/H_1403 FALS=0?

## METHOD (VERBATIM H_1392/H_1403 frozen G6 FALS detector + scaffold)

Probe `state/1410_g6_fals_vs_conv_depth/g6_fals_depth_probe.hexa` — BYTE-IDENTICAL to H_1403
`g6_fals_probe_loaded.hexa` except ckpt path from env `CKPT`. Imports live `CORE/g6_ideation.hexa`.
FROZEN: GEN=110, SEED=7, K=3, detector `_g6_is_falsifiable` verbatim, kwr-gate ≥0.5.
5 M-bars (verbatim): M1_COUNT DIST(Cs)≥5 · **M2_DEPTH FALS(Cs)≥1** (the depth-lift bar) ·
M3_LIFT Cs>B · M4_PAIR Cs>shuffle · M5_COMP Cs>ablate.

PRE-DECODE GUARDS (read on aiden 2026-06-17, BOTH rungs): DETECTOR_CALIBRATION=10/10 ✓ ·
FRAME_GUARD_LEAKS=0 ✓ · SAMPLER det/diverse/in_topk=true/true/true ✓ ·
L4 MOUNT ok=true d=3784 E=2 V=256 **L=4** ✓ · L8 MOUNT ok=true d=3020 E=2 V=256 **L=8** ✓
(both ckpt sha256 == FREEZE manifest, verified post-transfer to aiden).

## RESULT (engine-native, aiden-pool-CPU, seed=7, GEN=110, H_1403 streaming) — PARTIAL 2/6 per rung

Every C_strong frame that decoded scored **fals=FALSE** on BOTH deeper conv rungs:

| rung | frame | fals | kwr |
|------|-------|------|-----|
| L4 d3784 L=4 | C_strong[0] | **false** | 0.315789 |
| L4 d3784 L=4 | C_strong[1] | **false** | 0.888889 |
| L8 d3020 L=8 | C_strong[0] | **false** | 0.5 |
| L8 d3020 L=8 | C_strong[1] | **false** | 0.555556 |

FALS(C_strong) tally on frames that RAN: **L4 = 0/2, L8 = 0/2** (4/4 frames fals=false).
Deterministic: every fals/kwr is byte-identical across aiden's crash #1 (seed=7). NO frame at
any depth produced a falsifiable sentence — REPRODUCING the L1 H_1394/H_1403 FALS=0.

**M2_DEPTH FALS≥1 NOT met** at either rung (FALS=0 on every decoded frame). M1/M3/M4/M5 need
the full arm + control arms (moot at FALS=0 per FREEZE) and were NOT scored. NO bar moved (c9).

substrate note (c9, honest): hexa streaming `.clm` decode (`CORE/clm_decode.hexa`) is
**CPU-bound** — DEFINITIVE `nvidia-smi` on the clean host (no contending job): both decode lanes
at 99.9% CPU read GPU util=0%, mem=2 MiB, ZERO compute apps. The RTX 5070 is NOT utilized by the
hexa decode path. Engine-native hexa `.clm` throughout (verdict integrity preserved,
a_engine_native_learning); NO torch/.pt mirror substituted.

infra-cap (c9, c16 type-c — a_break_the_wall): the full 6/6 C_strong arm was NOT completed.
aiden (the only verified-correct hexa toolchain) CRASHED/rebooted TWICE under sustained dual-lane
CPU load and on crash #2 went hard-down ~24+ min (manual power-cycle needed, unavailable). summer
(2nd pool host) CANNOT compile the import closure (missing compiled stage1 module_loader; filed
hexa-lang/inbox/patches/pool-summer-missing-compiled-module-loader.md). mini is c17-forbidden.
This is an INFRASTRUCTURE wall, NOT a science ceiling, NOT a moved bar.

## VERDICT

🧱 **ARCHITECTURE (conv-FAMILY ceiling) — PARTIAL (2/6 per rung, infra-capped)**

Within the frames that ran (2/6 per rung, exceeding the FREEZE minimum of 1/rung, all
deterministic), conv-DEPTH (L4, L8) does NOT lift G6 FALS over L1 — every decoded frame
fals=false, reproducing H_1394/H_1403's FALS=0. This is consistent with the pre-registered rule
"FALS=0 at L4 AND L8 ⇒ 🧱 ARCHITECTURE is the conv-FAMILY ceiling (depth does NOT buy
falsifiability), NOT just an L1 artifact." The 🧱 direction is strongly indicated (4/4 fals=false)
but reported as PARTIAL pending the remaining 4 frames/rung on a stable pool host (follow-on, ING).

`wired: N/A` — measurement re-score (FALS detector over decode), no GREEN mechanism to wire.

## HONEST SCOPE (c9, a_scale_honest_scope)

- engine-native hexa `.clm` decode (NOT a torch/numpy mirror) — verdict-binding for the
  conv-FAMILY depth question.
- TOY/fixed: 6 C_strong composed frames, seed=7, GEN=110, K=3; deterministic given seed
  (NOT byte-identical to the torch gauge). Tests the detector over decoded bytes.
- DEPTH ladder = L1 (H_1394/H_1403 ref) + L4 + L8, all ~303M width-compensated (depth⊥capacity).
- p1/p2/p3/p4/p6 guard: probe reads ONLY the seeded sampler + frozen lexical detector —
  NO injected falsifiable-claim label, NO RLHF, NO persona, NO system prompt.

## POINTERS

- FREEZE `.verdicts/1410_g6_fals_vs_conv_depth/FREEZE.txt`
- result `.verdicts/1410_g6_fals_vs_conv_depth/result.txt`
- probe `state/1410_g6_fals_vs_conv_depth/g6_fals_depth_probe.hexa`
- raw logs `state/1410_g6_fals_vs_conv_depth/L4_aiden.log`, `L8_aiden.log`
- xref H_1394 · H_1403 (L1 ref) · H_1362 (ByteGPT FALS=1.0) · H_1392 (frozen detector) ·
  a_engine_native_learning · a_no_llm_frame_trap · a_scale_honest_scope · c9 · p7
