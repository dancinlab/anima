#!/usr/bin/env tape
# CLM.log.tape — append-only event history sibling of CLM.tape
# (v1.2 architecture-vs-history split, 2026-05-14).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — per-cycle measurement records from .clm Phase fires
# (chronological, oldest first; section headers preserved for cycle context)

# ── §5 §92 v5 DDP 결과 land (옵션 D) ─────────────────────────────────────────

@D ddp_result_size :: clm-tape [ok]
  text = "n_params = 5,373,430,016 (~5.37B) — Phase 3 7B 의 76% size class"

@D ddp_result_compute :: clm-tape [ok]
  text = "wall = 24185.6s (6.72hr) · cost = $86.82 · ddp world_size=4 (per_gpu_batch=2, effective=8) · freeze_mitosis=1"

@D ddp_result_metrics :: clm-tape [ok]
  text = "ce_final_avg100 = 0.0646 (낮음) · aux_final = 1.208 · ent_gate_final = 5.543/5.545 (최대값) · wmax_final = 0.190 · n_active>.01 = 8.0/256 cells · gate_max = 0.0072 (dead routing)"

@D ddp_result_falsifiers :: clm-tape [ok]
  text <<~EOF
    F-V5MIT regression: **3/5 FAIL**
      F-V5MIT-1 SPLIT-NOGRAD FAIL (freeze_mitosis=1 로 splits=0, baseline 미산출)
      F-V5MIT-2 MERGE-WEIGHT PASS
      F-V5MIT-3 PHI-CONSERVATION PASS
      F-V5MIT-4 COTRAIN-CONVERGE PASS (ce 0.065 ≪ 1.0)
      F-V5MIT-5 V14-STRICT FAIL

    F-PERSONA-4a routing (top-K MoE): **KL_PASS_NULL_FAIL**
      KL = 1.4903, null permutation 1.36±0.25, z = 0.51 p = 0.31 (null 안 통과)
      (soft gate) KL = 0.0005, z = 2.33 (cf. PSCC §52 v7 z=2.75 first signal)

    F-PERSONA-4b content (M4 aggregated cosine): **FAIL**
      cos_dist = 2.34e-4, null = 1.75e-4 ± 6.3e-5, z = 0.94 p = 0.14
      (v2 carry z = 3.20, §44 PSCC reference)
  EOF

@D ddp_result_verdict :: clm-tape [ok]
  text <<~EOF
    **§92 v5 DDP verdict**: 5.37B Phase 3-class 시도 **INCONCLUSIVE**.

    Positive: cotrain converge (ce 0.065), 7B-class wall feasibility 입증 ($86.82,
    6.72hr 4×GPU), DDP 인프라 작동.

    Negative: F-V5MIT 3/5 FAIL (V14-STRICT 재현), F-PERSONA-4a soft gate z=2.33
    < 3.0 strict (§52 v7 z=2.75 와 동일 ballpark), F-PERSONA-4b FAIL.

    **Off-track for canonical Phase 3**: arch 가 Engine A/G dual-engine 아니라
    v5-mitosis 1L + 256 cells substrate. fire_keyword `OK CLM PHASE 3 7B FIRE`
    와 무관 — 본진 ladder entry 미시도. cost $86.82 가 Phase 3 envelope $200-600
    의 14-43% 소진했지만 Engine A/G path 진척 0.

    **그러나** size feasibility + DDP infra + V14 mirror behavior 의 evidence
    는 Phase 3 Engine A/G fire 시 carry-forward 가치.
  EOF
