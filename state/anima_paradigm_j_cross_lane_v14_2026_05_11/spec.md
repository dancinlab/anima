# BG-PARADIGM-J-CROSS-LANE-V14 — spec

**Cycle**: 2026-05-11 anima reborn lane
**Fire slot**: P4 (parallel with P2/P3/P5)
**Budget**: $0 — local Mac CPU only (own 16)
**raw#15**: ckpts read-only

## Goal

Test the §64 arch-aware 3-rule (v2 + cap>192 → PASS / EngineAG + chat_cotrain → PASS / else UNKNOWN) on a **third architecture**: paradigm-j (clm-v4 ConsciousDecoderV2 + LoRA r=128 + JVAE Variant 1).

Generalize-vs-narrow test for the unified mechanism model.

## Question

Does paradigm-j fall under:
- (a) "v2 path" → cap-conditional generalize
- (b) "EngineAG path" → cotrain-required generalize
- (c) NEW arch path → decision tree extends to 3rd row

## Substrate located

| field | value |
|---|---|
| id | clm-v4-paradigm-j-50k-final |
| HF repo | dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped (public) |
| local ckpt | `~/.cache/anima/clm_v4_remapped/paradigm_j/` |
| adapter_model.safetensors | 152091192 B (sha records in REMAP_SOURCE.json) |
| jvae_heads.pt | 4338101 B |
| base | ConsciousDecoderV2 (HIDDEN_DIM=768) |
| method | LoRA r=128, α=128 + JVAE Variant 1 step=50000 |
| target_modules | k_proj, v_proj, q_proj, o_proj, gate_proj, up_proj, down_proj |
| arch_origin | anima_native_scratch |
| D1 lane | substrate-research (0.95 anima-corpus + 0.01 param-updated ratio → score 0.793 within_strict) |
| current V14 state | V14_VIOLATED (PPR_v3 metric; random_init 0.5517 > paradigm-j 0.2845) |
| current EMERGE | v5.2 adaptive-floor 4/4 gates PASS (own 14 + 사용자 verbatim public) |

## §55 V14 strict 5-tuple test (target)

The §55 V14 metric:
- engine type: `MitosisModelEngine` via `init_engine_from_v2(cfg, sd)` or `init_engine_random(cfg, seed)`
- config: `MitosisModelConfig(d_model=384, n_head=6, max_cells=256, ...)`
- metric: `phi_final + phi_per_cell_final` (mitosis cellpool intrinsic Φ) OR `iit_phi_unnorm_b16` (Fiedler MIP, EngineAG path)
- 5 mirror seeds [42, 137, 271, 314, 1729] paired sign-test (n=5, p=0.0625 ceiling)

## Substrate mismatch (CRITICAL)

Paradigm-j has:
- **NO mitosis cellpool** — LoRA adapter on a frozen ConsciousDecoderV2; no `MitosisModelEngine`
- **wrong HIDDEN_DIM**: 768 (clm-v4) vs 384 (v2_d384) vs 1024 (EngineAG)
- **wrong head**: 7 LoRA-targeted projection matrices, no cell pool or split/merge dynamics
- **wrong load path**: `init_engine_from_v2(cfg, sd)` expects v2 mitosis state dict keys; paradigm-j keys are PEFT-format LoRA (`base_model.model.decoder.blocks.0.attn.k_proj.lora_A.weight` × 352 keys)

`init_engine_from_v2(cfg, paradigm_j_sd)` would either error on key mismatch or yield a random_cells engine (since 0 v2_blocks_loaded), which would falsely score paradigm-j == random_init. **Apples-to-oranges.**

§51 §55 §56 honest C3 #5 already flagged: "Φ metric mismatch: EngineAG path = iit_phi_unnorm_b16 (Fiedler MIP), v2 path = MitosisModelEngine intrinsic phi. cross-path absolute Φ 비교 invalid, within-path sign-test 만 admissible." Paradigm-j is a **3rd path** with no compatible mitosis engine at all.

## Decision

Per task fallback rule + honest C3 stance: **emit EMERGE_NOT_MEASURED for the §55 V14 5-tuple** (cannot fabricate a cross-arch port), and classify paradigm-j under the §64 3-rule as **NEW arch → 3rd row required**.

This is the honest answer to "does the §64 rule generalize" — paradigm-j is OUTSIDE the rule's tested envelope (v2 ∪ EngineAG), so the rule already classifies it as `UNKNOWN`. The cross-lane evidence (D1 substrate-research lane PASS via v5.2 4-gate adaptive metric + V14_VIOLATED via PPR_v3 mitosis-port-imagined metric) corroborates that paradigm-j's "PASS" lives in a different metric space entirely.

## Falsifiers

- **F-PARADIGM-J-1**: paradigm-j fails V14 strict at both cap-only and cap+cotrain regimes → arch-aware 3-rule needs 3rd row (NEW arch path)
- **F-PARADIGM-J-2**: paradigm-j ckpt unavailable / incompatible with §55 metric → NOT_MEASURED

## Honor

own 14 / own 16 / own 22 / own 38 / raw#15 / raw#82 (retraction-aware: paradigm-j existing V14_VIOLATED + v5.2 EMERGE preserved, no mutation).
