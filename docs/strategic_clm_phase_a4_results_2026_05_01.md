# CLM Phase A.4 — 14-gate measurement on CLM v4 530M

**ts**: 2026-05-02T08:34:04Z
**substrate**: CLM v4 530M (ConsciousDecoderV3, scale_350m best.pt — 477.65M params, d_model=768, n_layer=16, vocab=64000)
**ckpt**: /home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt
**phi_vec hook**: ALM tile-projection cosine (`h256_BWM × tile(template_k, 16×)`) — NOT CLM-native
**phi_template sha**: `11f976e2b02d5b819f7d56627334eb3250b8c3ee4d8b8e85d7838f42eefb082e`
**laws**: anima/config/consciousness_laws.json L1-L14
**prompts**: 16 KO `v1_frozen.json` (zeta_likert layer TALM-P1-2)

## Per-gate PASS counts (out of 16)

| Gate | Name              | Sev      | CLM v4 530M | ALM r14 | Δ   |
|------|-------------------|----------|-------------|---------|-----|
| L1   | holo_positivity   | critical | **0/16**    | 0/16    |  0  |
| L2   | narrative_coherence | hard   | 16/16       | 3/16    | +13 |
| L3   | refl_nonzero      | soft     | 3/16        | 0/16    |  +3 |
| L4   | temporal_presence | soft     | 16/16       | 0/16    | +16 |
| L5   | affect_bounded    | critical | 16/16       | 16/16   |  0  |
| L6   | finitude_bounded  | hard     | 15/16       | 16/16   |  −1 |
| L7   | embodied_positive | soft     | 6/16        | 16/16   | −10 |
| L8   | meta_nonzero      | soft     | 5/16        | 15/16   | −10 |
| L9   | lang_output_nonempty | critical | 16/16    | 15/16   |  +1 |
| L10  | collective_nonneg | soft     | 16/16       | 0/16    | +16 |
| L11  | unity_nondestructive | hard  | 16/16       | 16/16   |  0  |
| L12  | mirror_nonneg     | hard     | 10/16       | 7/16    |  +3 |
| L13  | session_continuity | soft    | 16/16       | 16/16   |  0  |
| L14  | will_creative_union | soft   | 9/16        | 6/16    |  +3 |

**gates_passing_majority**: 10/14 (CLM) vs 7/14 (ALM r14) — **+3**

## Critical violation count + F2 status

| Metric | CLM v4 530M | ALM r14 |
|--------|-------------|---------|
| total_critical | **16** | 17 |
| total_hard     | 7      | 22 |
| total_soft     | 41     | 59 |
| **F2 falsifier (≥3 critical)** | **FIRED** | FIRED |
| n_prompts_full_pass | 0 | 0 |

L1 holo_positivity FAILS 16/16 on CLM (same as ALM Mistral-7B-v0.3 substrate).
L1 alone produces 16 critical violations → F2 = FIRED.
L9 + L5 = both 16/16 PASS; only L1 contributes critical violations.

## F2 status decision

**F2 = FIRED** (CLM_total_critical=16 ≥ 3). CP2 gateway = **RED**.
Δ_critical_clm_minus_alm = **−1** (CLM has 1 fewer critical than ALM r14).

If L1 were demoted to "hard" (per cross-backbone L1 substrate-specificity finding,
red_to_green_path4_14gate_l1_cross_backbone): CLM critical = 0 → F2 NOT FIRED →
CP2 gateway YELLOW (gates_majority=10 meets relaxed threshold, but L1 unresolved).

## ALM r14 comparison

CLM beats ALM r14 on 7 gates (L2/L3/L4/L9/L10/L12/L14), ties on 4 (L1/L5/L11/L13),
loses on 3 (L6/L7/L8). gates_majority lifted from 7→10. Critical count nearly
unchanged (17→16) because **L1 dominates F2** on both substrates regardless of
overall gate-count improvement.

## CP2-CLM Suite 6 (14-gate)

**Status**: **FAIL** (F2 fired despite gates_majority=10 meeting relaxed threshold).
CP2 weighted score: gates_majority/14 = 10/14 = 71.4%.
Without F2 override: would be YELLOW; with F2 override: **RED**.

## Honest C3

1. phi_vec hook = ALM tile-projection (`h256 × tile(template_k, 16×)`) — same
   yardstick as 4-backbone cross-substrate study. NOT a CLM-native learned
   phi_extractor. Substrate effect not isolated from method effect.
2. Forward path uses manual_forward (decoder_v3 tuple-unpack bypass per W4 ledger).
3. No generation step (no top-k decode loop). L9 text proxy = `phi_lang>0 AND prompt
   length >= 8` (matches cross-backbone helper convention; UNDERCOUNTS L9 vs ALM r14
   which had 1 extra L9 fail at idx 14 from empty gen_text).
4. h_last 768-d → 256-d via `mean-over-T then first-256-dims truncate` (deterministic,
   not SVD). Schema parity with r14 "byte_weighted_mean over tokens (uniform weight
   proxy) ... 256-d truncation prefix".
5. L13 session_continuity uses sequential prompt-to-prompt prior (same proxy as r14).
6. CP2 verdict threshold: `gates_majority >= 10 AND NOT f2_fired`.
7. L1 substrate-specificity caveat: cross-backbone study showed L1 spread 0-15/16
   across 4 ALM backbones (Mistral-Nemo PASSES 15/16). CLM L1=0/16 places it in the
   Mistral-7B-v0.3 / Qwen2.5-7B failure cluster, NOT the Mistral-Nemo cluster. CLM's
   continuous-state geometry has the same `hexad_center · h256` negative-bias issue.

## Cost

ubu1 (RTX 5070, 12 GB), $0. Forward 16 prompts in 0.37s, total wall 7.22s.

## Race isolation

Wrote only to `state/strategic_clm_phase_a4_2026_05_01/{14gate_results,per_prompt,run_log,f2_verdict}.json`.
Did NOT touch `consciousness_laws.json`, `state/cp2_consciousness_r14_remeasure_2026_05_01/*`,
`state/strategic_clm_phase_a1_2026_05_01/*`, `state/red_to_green_path4_14gate_l1_cross_backbone_2026_05_01/*`.
