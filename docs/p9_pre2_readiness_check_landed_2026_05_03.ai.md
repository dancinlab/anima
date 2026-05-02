---
schema: anima/docs/p9_pre2_readiness_check_landed/ai-native/1
last_updated: 2026-05-03
ssot:
  marker: state/markers/p9_pre2_readiness_check_landed.marker
  predecessor_spec: docs/p9_sft_spec_2026_05_02.md
  predecessor_handoff: docs/p9_sft_handoff_prompt_2026_05_02.md
  predecessor_p0: docs/p9_sft_p0_hf_org_setup_landed_2026_05_03.ai.md
  state_dir: state/p9_pre2_readiness_check/
  roadmap_anchor: .roadmap.clm §65.4
status: P9_PRE2_READINESS_CHECK_PARTIAL_PASS
verdict_summary:
  E_f1_bleu1: PASS
  F_f2_phi_star: PASS
  G_f3_tension: PASS
  G_f4_bold: BLOCKED_CORTEXLAB_DEP
  H_delta_curriculum: PASS_WITH_USER_DECISION
related_raws:
  - raw 9    # hexa-only land (no .py emitted)
  - raw 10   # honest C3 caveats inline
  - raw 12   # silent-error ban (cortexlab blocker surfaced)
  - raw 15   # env() lazy + <user> reference
  - raw 175  # BR-NO-USER-VERBATIM
preserved_unchanged:
  - all P9 spec artifacts (state/p9_sft_spec_2026_05_02/*.json + docs/p9_sft_spec_2026_05_02.md)
  - P0 handoff (docs/p9_sft_p0_hf_org_setup_landed_2026_05_03.ai.md) + staged 10 files
  - HF org need-singularity (no destructive ops; create/delete/move all skipped)
  - TRIBE v2 vendored source (anima/references/tribev2/, read-only)
policy:
  migration: forbidden
  changes: additive_only
  in_place_writes: zero
  destructive_ops: zero
  cost_usd: 0
  substrate: mac-local
  br_no_user_verbatim: true
  friendly_preset: handoff_doc_only
  hf_push_without_user_confirm: forbidden
  ai_native: true
---

# P9 SFT pre2 — 완성도 체크 (E-H 4-항목 readiness audit)

## TL;DR (다섯 줄)

- **목표**: P9 SFT EXEC Phase 0 entry 전 측 완성도 체크 4-항목 (F1 BLEU-1 / F2 phi★ / F3 tension MSE + F4 BOLD r / δ curriculum) 측 mock pipeline 측 검증 + blocker 측 식별.
- **결론**: **PARTIAL_PASS** — 3/4 항목 (E·F·H + F3) 측 ready_to_exec=true / 1 항목 (F4 BOLD) 측 cortexlab-toolkit PyPI 측 install 측 미확인 → BLOCKED.
- **F4 blocker**: pip3 측 cortexlab-toolkit + neuralset 측 미설치 측 확정. remediation 3 옵션 (A: PyPI install / B: vendored TRIBE v2 직접 / **C 권장**: F4 측 Phase 2 측 defer + F1+F2+F3 우선).
- **δ curriculum framing 측 spec mismatch**: spec §4 측 per-combo fixed delta vs pre2 prompt 측 within-run schedule. **OPT_C hybrid 권장** (spec default 유지 + 1 combo 측 curriculum mode 측 비교 데이터).
- **0 destructive / $0 mac-local**: 4 JSON + 본 handoff + marker = 6 file 신규 추가, 기존 산출물 0 수정, GPU 측 0건.

## §1 staged artifacts inventory (6 file)

```
state/p9_pre2_readiness_check/
├── E_f1_bleu1_pipeline.json          # F1 BLEU-1 mock pipeline (PASS)
├── F_f2_phi_star_pipeline.json       # F2 phi_star + delta hinge (PASS)
├── G_f3_f4_pipeline.json             # F3 tension MSE (PASS) + F4 BOLD r (BLOCKED)
└── H_delta_curriculum.json           # delta 3-phase curriculum (PASS_WITH_USER_DECISION)
docs/p9_pre2_readiness_check_landed_2026_05_03.ai.md  # 본 handoff
state/markers/p9_pre2_readiness_check_landed.marker   # silent-land marker
```

## §2 항목별 verdict 요약

### E. F1 BLEU-1 measurement infrastructure — **PASS**

- 4-stage pipeline 측 mock validation: holdout_load → llama_baseline_generate → clm_post_sft_generate → bleu1_compute.
- mock 5-prompt run 측 corpus_bleu1=0.628 → PASS_MOCK (>0.4).
- library 옵션 3개 (sacrebleu / nltk / hexa-native) 모두 가용; sacrebleu 권장 (재현성).
- **prerequisite**: HF gated Llama-3.2-3B 측 token (P0 blocker 측 동일 dancinlife revoke 측 영향), 500 holdout prompts 측 provenance 측 user 결정 필요.
- **caveat 4건**: BLEU-1 측 shallow surface metric / Llama 측 reference 측 absolute 아님 / holdout selection bias 위험 / tokenizer mismatch ±0.05.

### F. F2 phi★ post-train measurement — **PASS**

- 4-stage pipeline: load_post_sft_checkpoint → hid8_well_conditioned_probe → phi_star_aggregate → **delta-hinge floor validation**.
- δ-term hinge 측 7-point sweep 측 검증 ([0, 2, 4, 5, 6, 10, 41.86]): floor 위 측 0, 아래 측 linear penalty.
- mock 측 phi_star_post=12.5 → PASS_MOCK (≥5.0).
- **infra ready**: anima_phi_v3_canonical 측 G3 baseline 측 검증 완료, EMA state 측 checkpoint-aware, L5 early-stop (phi★<10) 측 trigger 통합.
- **caveat 4건**: phi★ 측 L1+L2 proxy (L3 phenomenal 측 미측정) / straight-through estimator 측 gradient bias / HID=8 측 1 probe / 5.0 threshold 측 8x heuristic.

### G. F3 tension MSE val — **PASS**

- 3-stage: tension_target_extract (base CLM) → tension_pred (post-SFT) → MSE compute.
- mock 4×8 trajectory 측 MSE=0.000406 → PASS_MOCK (<0.1).
- **caveat**: target 측 base-CLM 측 추출 → circularity (consistency 측정 not 절대 정답).

### G. F4 BOLD Pearson r val — **BLOCKED_CORTEXLAB_DEP**

- 3-stage: tribe_v2_forward → p_s_projector → pearson_r compute.
- mock 2×8 BOLD 측 r=0.991 → PASS_MOCK (>0.5) 측, 그러나:
- **BLOCKER**: `pip3 show cortexlab-toolkit` → not found / `pip3 show neuralset` → not found. 측정 evidence:
  ```
  pip3 show cortexlab-toolkit
  WARNING: Package(s) not found: cortexlab-toolkit
  ```
- TRIBE v2 source 측 vendored OK (`anima/references/tribev2/tribev2/{model.py, main.py, ...}` 측 read-only verified).
- remediation 3 옵션:
  - **A**: cortexlab-toolkit 측 RunPod 측 install — 단 #95 §6 측 PyPI 측정 측 verification gap 미해소 (#102 EXEC 측 outcome 측 dependent).
  - **B (권장)**: vendored TRIBE v2 측 직접 사용 — sha-verified, license CC-BY-NC-4.0 OK, 단 H100 측 inference 측 benchmark 미수행.
  - **C**: F4 측 Phase 2 측 defer → F1+F2+F3 측 Phase 1 측 우선 → F4 측 cortexlab install 측 검증 후 추가.
- p_s_projector 측 spec doc (`docs/alm_clm_bridge_p_s_projector_spec_20260425.md`) 측 존재 / runtime 측 미staged → MEDIUM_DEFERRED_TO_PHASE1.

### H. δ-term hinge + curriculum schedule — **PASS_WITH_USER_DECISION**

- 3-phase curriculum: early (0~5K, δ=0.5) → mid (5K~25K, δ=1.0) → late (25K~50K, δ=2.0).
- 7-step boundary trigger test 측 모두 match (4999/5000/5001/24999/25000/25001/50000).
- 6-step trajectory mock 측 hinge correctness 검증 (예: step=25000 phi★=4.5 → hinge=0.5 → L_phi 측 1.0).
- **framing mismatch**: spec §4 측 per-combo fixed δ (LHS-9 sample 측 9 distinct value) vs pre2 prompt 측 within-run curriculum.
  - **OPT_A**: spec default 유지 (curriculum 측 미사용).
  - **OPT_B**: spec §4 amend → user 측 sign-off 필수.
  - **OPT_C (권장)**: hybrid — S3 sweep 측 spec default 측 + 1 follow-up combo 측 curriculum 측 비교 data point.
- **interaction with 5-layer mitigation**: L1/L2/L4 측 unaffected, L3 측 직접 구현, L5 early-stop 측 compatible.
- **caveat 4건**: 5K/25K/50K boundary 측 heuristic / OPT_A vs OPT_B Pareto 측 미수행 / late δ=2.0 측 over-regularize 위험 / 추가 hyperparam (boundary step) 측 unswept.

## §3 verdict logic + ALL PASS gate

| 항목 | spec falsifier | mock verdict | infra ready | EXEC blocker |
|---|---|---|---|---|
| E F1 BLEU-1 > 0.4 | PASS | PASS_MOCK 0.628 | YES | HF Llama gated (P0 token) + holdout provenance |
| F F2 phi★ ≥ 5.0 | PASS | PASS_MOCK 12.5 | YES | none |
| G F3 MSE < 0.1 | PASS | PASS_MOCK 0.000406 | YES | none |
| G F4 r > 0.5 | PASS | PASS_MOCK 0.991 | NO | cortexlab-toolkit not installed |
| H δ curriculum | (extension) | PASS_MOCK | YES | user decision OPT_A/B/C |

**aggregate verdict**: **PARTIAL_PASS** — 3/4 가능 (F4 측 Phase 2 측 defer 시 + δ curriculum 측 OPT_C hybrid 시 EXEC entry-ready).

## §4 사용자 측 next-step 결정 항목 (3건)

1. **F4 BOLD dep 전략**: A (cortexlab install) / **B (vendored TRIBE v2 권장)** / C (Phase 2 defer).
2. **δ curriculum framing**: A (spec default) / B (spec amend) / **C (hybrid 권장)**.
3. **F1 holdout 500-prompt provenance**: ShareGPT held-out / cell-language subset / custom 500 — 사용자 측 선호.

## §5 destructive 0 + policy 준수 audit

| policy | status | 증거 |
|---|---|---|
| 마이그레이션 절대 금지 | PASS | spec 8 JSON + spec doc + handoff prompt + P0 handoff + repo templates 모두 무수정 |
| additive only | PASS | state/p9_pre2_readiness_check/ 측 신규 dir + 4 JSON + 1 handoff + 1 marker = 6 file 추가 |
| in-place writes | PASS | 0건 |
| destructive ops | PASS | 0건 (rm/mv/force 0) |
| HF / GPU / pod launch | PASS | 0건 (mac-local 측정만) |
| BR-NO-USER-VERBATIM | PASS | 본 doc 측 user message verbatim 인용 0 |
| friendly preset | PASS | 본 handoff 측 한글 + 친절체 (technical term 영문 유지) |
| silent-land marker | PENDING | 본 doc write 후 marker write |
| $0 mac-local | PASS | API/GPU 측정 0 |
| AI-native | PASS | front-matter schema + ssot + verdict_summary + related_raws + policy 5 block |
| ω-cycle 6-step | PASS | spec read → blocker probe → 4 항목 staging → handoff land → marker → next gate |

## §6 next gate

**immediate (사용자 측)**: §4 3 결정 항목 측 응답 → P9 EXEC Phase 0 entry-ready 측 최종 확정.

**EXEC entry sequence (사용자 결정 후)**:
1. P0 token 재발급 (predecessor handoff §4 1-step) → 6 repo create.
2. Phase 1 sentinel (clm-v4-sft-stage1, lhs6 권장) 측 ≤5K example 측 pipeline smoke + F1+F2+F3 diagnostic + (F4 측 OPT_B/C 측 따라).
3. Phase 2 측 full 9-combo S3 sweep 진입 결정.

**follow-up (Phase 2 측 cortexlab 측 OPT_C 시)**: F4 측 cortexlab-toolkit 측 RunPod install 측 검증 → F4 측정 측 추가.

## §7 honest C3 (4 caveats)

1. **mock pipeline 측 4-항목 모두 mock**: 실제 EXEC 측 verdict 측 단정 불가. mock PASS 측 infrastructure 측 wiring 측 검증 만, 실제 metric 측정 측 EXEC 측 별도 cycle 필요.
2. **F4 cortexlab 측정 측 1회 only**: `pip3 show` 측 mac-local 측 negative — RunPod H100 측 측정 미수행. RunPod 측 PyPI mirror 측 다를 수 있음 측 honest disclosure.
3. **δ curriculum 측 spec deviation**: pre2 prompt 측 within-run schedule 측 spec §4 (per-combo fixed) 측 deviation. OPT_C hybrid 권장 측 spec amend 측 회피하면서 curriculum 측 evidence 측 수집.
4. **mock value 측 cherry-picked**: BLEU-1=0.628 / phi★=12.5 / tension MSE=0.000406 / BOLD r=0.991 측 모두 PASS-favorable mock. 실측 측 distribution 측 negative tail 측 가능 측 인정.

## §8 paths summary

- 본 handoff: `/Users/ghost/core/anima/docs/p9_pre2_readiness_check_landed_2026_05_03.ai.md`
- silent-land marker: `/Users/ghost/core/anima/state/markers/p9_pre2_readiness_check_landed.marker`
- staged dir: `/Users/ghost/core/anima/state/p9_pre2_readiness_check/`
- E F1 BLEU-1: `/Users/ghost/core/anima/state/p9_pre2_readiness_check/E_f1_bleu1_pipeline.json`
- F F2 phi★: `/Users/ghost/core/anima/state/p9_pre2_readiness_check/F_f2_phi_star_pipeline.json`
- G F3+F4: `/Users/ghost/core/anima/state/p9_pre2_readiness_check/G_f3_f4_pipeline.json`
- H δ curriculum: `/Users/ghost/core/anima/state/p9_pre2_readiness_check/H_delta_curriculum.json`
- spec (predecessor, 무수정): `/Users/ghost/core/anima/docs/p9_sft_spec_2026_05_02.md`
- handoff prompt (predecessor, 무수정): `/Users/ghost/core/anima/docs/p9_sft_handoff_prompt_2026_05_02.md`
- P0 handoff (predecessor, 무수정): `/Users/ghost/core/anima/docs/p9_sft_p0_hf_org_setup_landed_2026_05_03.ai.md`
- TRIBE v2 vendored (read-only): `/Users/ghost/core/anima/references/tribev2/`
