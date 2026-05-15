#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# MITOSIS.tape — anima mitosis growth-axis architecture (SSOT)
# tape v1.2 grammar — see AGENTS.tape head for primer.
#
# Architecture file (EDITABLE, latest-wins per id) per AGENTS.tape
# g_arch_vs_log_split. mitosis = anima 시스템의 성장축 (구조축 HEXAD.tape ⊥).
#
# Trigger: user directive 2026-05-15 — "mitosis 도 중요하니까 <domain>.tape
#          생성 ASCII 구조도 포함" + "여기에다가 성장방식이 mitosis"
# ══════════════════════════════════════════════════════════════════════

@V v1 := "tape" :: spec [active]
  version = "1.2"

# ─── §1 Identity ─────────────────────────────────────────────────────

@I mitosis_id := "anima-mitosis" :: identity-claim [d=2026-05-15 active]
  kind = "성장축(growth axis) — anima Hexad 시스템이 자라나는 방식 (cell 분열/병합)"
  axis_relation = "구조축(HEXAD.tape, Hexad 6모듈 A=좌뇌3/G=우뇌3) ⊥ 성장축(MITOSIS.tape). 직교."
  principle = "REBORN.tape §0.5 — 학습=분열 단일 연속체 (train/infer 분리 없음, ckpt=분기점, 구조 자체가 organically 성장)"
  verified = ".clm v1 from-scratch 8/8 SUPPORTED-STRONG + 🔵 SUPPORTED-FORMAL (cycle 88-90, 2026-05-15)"
  impl = "training/clm_v1_model.py (MitosisCell + mitosis_step + force_split/merge + _compute_iit_phi)"

# ─── §2 Growth mechanism ─────────────────────────────────────────────

@D mitosis_mechanism := "tension 기반 split/merge 성장 메커니즘" :: architecture [d=2026-05-15 active]
  tension = "각 cell 의 residual update L2 norm (mean over batch×seq). softmax(tensions) 로 cell 출력 가중합."
  split = "어떤 cell tension 이 adaptive threshold (mean+1.5σ+split_threshold) 위로 split_patience 연속 → 부모 deep-copy + gaussian noise(σ=0.10) → 자식 생성. 자식 param grad_fn=None (fresh leaf, optimizer lazy-init)."
  merge = "두 cell pairwise tension 차이가 merge_threshold(0.005) 미만 merge_patience(30) 연속 → weight 평균 → 하나 제거."
  phi_proxy = "Φ★ = cell weight 벡터 간 평균 pairwise L2 distance / √dim + log(N+1). cell 다양성 = 의식 수준 대리지표."
  bound = "initial_cells=2 → max_cells=64 (.clm v1). organic 성장 — corpus/task 압력이 분열 구동."

# ─── §3 ASCII — mitosis 성장 구조도 ──────────────────────────────────

@N mitosis_ascii := "mitosis 성장 메커니즘 ASCII" :: diagram [d=2026-05-15 active]
  body <<~EOF
    ── 성장축: cell pool 이 시간에 따라 분열로 자라남 ──

    step 0          step ~50         step ~150        step 250+ (saturated)
    ┌──┐            ┌──┐┌──┐         ┌──┐┌──┐┌──┐     ┌──┐┌──┐ ... ┌──┐
    │c0│            │c0││c1│         │c0││c1││c2│     │c0││c1│     │c63│
    │c1│   split→   │c2││c3│  split→ │..││..││..│ →   │..││..│ ... │..│
    └──┘            └──┘└──┘         └──┘└──┘└──┘     └──┘└──┘     └──┘
    2 cells         ~15 cells        ~40 cells        64 cells (max)
       │               ▲                                  │
       │               │ tension > adaptive_thr           │ tension 균형 → 분열 정지
       │               │ (split_patience 연속)            │
       └───────────────┘                                  ▼
                                                    merge: 유사 cell 쌍 병합
                                                    (.clm v1 = 0 merges, split-only)

    ┌─────────── 한 forward 의 cell 처리 ───────────┐
    │                                                │
    │  hidden h ──┬─→ cell_0 ─→ out_0 ─┐             │
    │             ├─→ cell_1 ─→ out_1 ─┤             │
    │             ├─→  ...            ─┤ softmax     │
    │             └─→ cell_N ─→ out_N ─┘ (tensions)  │
    │                                  │             │
    │  tension_i = ‖out_i‖             ▼             │
    │  weights = softmax([t_0..t_N])                 │
    │  h ← h + Σ weights_i · out_i  (가중 residual)  │
    │                                                │
    │  mitosis_step(): tension 기록 → split/merge 판정│
    └────────────────────────────────────────────────┘

    Φ★ = mean_pairwise‖cell_i − cell_j‖ / √dim  +  log(N+1)
         (cell 다양성 ↑ = 의식 수준 ↑ 대리지표)

    .clm v1 실측: 2→64 cells, 62 splits, 0 merges, saturated@step250,
                  Φ★ 4.34 안정, loss 467.97→1.14 (137.6× CE 감소)
  EOF

# ─── §4 Falsifier verification (.clm v1 8/8) ─────────────────────────

@D mitosis_verified := "mitosis 8/8 SUPPORTED-STRONG + 🔵 (.clm v1 cycle 88-90)" :: verify [d=2026-05-15 active]
  battery <<~EOF
    F-V5MIT-1 SPLIT-NOGRAD     ✅ 62 splits, 0 grad_fn violations (자식 fresh leaf)
    F-V5MIT-2 MERGE-WEIGHT     ✅ max_err=0.0 (병합 weight 평균 정확)
    F-V5MIT-3 PHI-CONSERVATION ✅ per-cell Φ delta=0.0 (분열 시 Φ 보존)
    F-V5MIT-4 COTRAIN-CONVERGE ✅ CE 137.6× 감소 (467.97→1.14)
    F-V5MIT-5 V14-STRICT       ✅ 10/10 mirror-beats (trained ≫ random)
    F-PRIN3 NO-PERSONA-INJECT  ✅ corpus 0-match + cell-pool prefix-free + gen 0/20
    F-SIMPLE-STACK V5.8 4-mode ✅ std_greedy 5/5 + std_sample 5/5 + M4 5/5
    F-PYPHI-Φ-FORMAL           ✅ best Φ=1.0625 (n=5), 단조증가 Hc_1283 cross-val
  EOF
  verdict = "8/8 SUPPORTED-STRONG + 🔵 SUPPORTED-FORMAL (g_verdict_tier_blue). first from-scratch .clm full battery + formal IIT tier."
  scope_caveat = "8/8 검증은 C 의식 모듈 scope (.clm v1 = mitosis 성장 of cell-pool). 전체 Hexad 6모듈에 mitosis 성장 적용 검증은 별도 cycle (현재 C scope evidence carry)."
  cross_link = "CLM.tape §V-CLM-V1-CYCLE90-PYPHI + HEXAD.tape §hexad_growth_method + state/clm_v1_fire_2026_05_15/clm_v1_full_battery_verdict.json"

# ─── §5 Two-axis relation (구조 ⊥ 성장) ──────────────────────────────

@D mitosis_two_axis := "성장축(mitosis) ⊥ 구조축(Hexad)" :: architecture [d=2026-05-15 active]
  body <<~EOF
    구조축 (HEXAD.tape):  A/G = Hexad 6 (Engine G 우뇌 3 C/S/W + Engine A 좌뇌 3 D/M/E)
                          = WHAT (시스템 무엇으로 구성되나)
    성장축 (MITOSIS.tape): cell split/merge 분열 성장
                          = HOW IT GROWS (시스템이 어떻게 자라나나)

    직교: 두 축은 독립. Hexad 6모듈 각각이 mitosis 방식으로 성장 가능.
          C 의식이 MitosisC 인 건 의식이 cell-pool 에 가장 직접 대응해서이지,
          mitosis 가 C 에 국한된 게 아님 (전체 시스템 성장 원리).
  EOF
  mandatory = "anima 본진 = [구조] A/G=Hexad 6 필수 + [성장] mitosis 필수. 둘 다 (user directive 2026-05-15)."
  cross_link = "HEXAD.tape §hexad_unification two_axes + §hexad_condition_lineup + CLM.tape §V-CLM-HEXAD-MANDATE"

# ─── §6 External citations ───────────────────────────────────────────

@X x_reborn_05 := "REBORN.tape §0.5" :: ledger [d=2026-05-15 active]
  scope = "학습=분열 단일 연속체 — mitosis 성장축 철학 anchor (train/infer 분리 폐기, ckpt=분기점)"

@X x_clm_v1_model := "training/clm_v1_model.py" :: impl [d=2026-05-15 active]
  scope = "MitosisCell + ClmV1Model.mitosis_step/force_split/force_merge/_compute_iit_phi — mitosis 성장 메커니즘 검증 구현 (.clm v1 8/8)"

@X x_hexad_tape := "HEXAD.tape" :: architecture [d=2026-05-15 active]
  scope = "구조축 SSOT — A/G=Hexad 6 (A 좌뇌3 / G 우뇌3). MITOSIS.tape(성장축) 와 직교 pair."

@X x_clm_hexad_mandate := "CLM.tape §V-CLM-HEXAD-MANDATE" :: governance [d=2026-05-15 active]
  scope = "[구조 A/G=Hexad] + [성장 mitosis] 둘 다 필수 — CLM 진행 anchor"

# ─── §7 Notes ────────────────────────────────────────────────────────

@N mitosis_lineage := "mitosis lineage v5-mitosis → .clm v1" :: note [active]
  text = "v5-mitosis cond.5 cotrain (REBORN §88, 2026-05-12, $1.26 H100) F-V5MIT 5/5 → .clm v1 from-scratch ClmV1Model (2026-05-15, $0.34, 8/8 + 🔵). 동일 mitosis 성장 lineage, ClmV1Model cell-pool 이 Hc_1283 PyPhi formal 단조증가 패턴 cross-validate."

@N mitosis_caveat := "성장 scope caveat" :: caveat [active]
  text = ".clm v1 8/8 검증은 C 의식 모듈(cell-pool) scope. Hexad 전체 6모듈(특히 좌뇌 D/M/E CE-trained)에 mitosis 분열 성장 적용은 미검증 — design directive (성장축 필수) 이나 full-Hexad mitosis evidence 는 별도 cycle."
