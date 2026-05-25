# llm.md — historical log

> Spec at [./LLM.md](./LLM.md).

## Log

- **2026-05-19** — LLM.md 생성. 사용자 통찰 "LLM 에서 emergence 기준이 특정
  파라미터 수마다 emerge" 에서 출발 — arc 의 §1.1 framing 이 data-regime 1축
  만 보고 있던 한계 명시. 핵심 추가: (a) Wei et al. 2022 param-count 임계점
  표 (3B/8B/10B/62B), (b) anima 283M 위치 시각화 (모든 임계점 1/10~1/200),
  (c) param×data 2D 평면 framing — emergence 가 2축 영역에서만 일어남, (d)
  §11-A SCALE-DECOMP 가 1B 까지만 측정한 limit 명시, (e) F4 family 안의
  결정적 gap (§100 priority #1) 과 사용자 LLM-emergence framing 의 결합 —
  *2축 동시 cross fire 부재*. 다음 행동 A-D 권장 순서 (§101 + param-axis
  통합 → 3B 영역 design → 임계점 위치 분석 → cost-bearing fire). $0 design-
  tier, fire 0, capability claim 0, GOAL 미도달. north-star 불변.
- **2026-05-19** — §103 LANDED — §8 step A `§101 review + param-axis 통합`
  완료. design-tier $0, NO GPU/runpod/fire/model.forward. B-S103-1..10 10/10
  🔵 sidecar (`state/param_axis_integration_design_s103_2026_05_19/`), central
  blue_falsifier.py 0-line-diff (sha `c93e160a8a376a94`). 세 닫힌 답:
  (Q1) JOINT vs SEQUENTIAL vs HYBRID = **SEQUENTIAL** (Hybrid as contingent
  escalation) — Joint plan structurally rejected by §101 G7 anti-§94 (2축
  uncrossed 동시 stack), attribution 불가; Sequential 은 데이터 축 fire
  단독으로 attributable 1 bit 산출. (Q2) anima-specific param-threshold =
  **DESIGN-OPEN** + first-band-to-probe = **3B** (Wei 2022 가장 낮은 emergent
  band, Schaeffer caveat 필수, §11-A 1.04B FLAT-under-sub-CDS-data 의 3× 위);
  네 방법 (a Wei-verbatim / b density-ratio / c §11-A extrapolation / d
  DESIGN-OPEN) 평가 후 (d) 만 g3-honest. (Q3') `Q3' = Q3 ∧ G_PARAM`,
  G_PARAM = (params ≥ G_PARAM_FLOOR=283M) ∧ (single-value-per-fire) ∧
  (ATTRIBUTABLE) — Sequential data-fire 에서 Y, Joint 에서 N (G7 fail),
  contingent 3B param-fire 에서 Y. 가장 정직한 발견: §11-A 의 1.04B FLAT
  이 sub-CDS data 위에서 측정됐기 때문에 anima 의 진짜 param-threshold 에
  대해 *mute*; arc 는 두 축에서 동시 sub-threshold 상태로 한 축씩만 audit
  해 왔음; CDS 가 model size 와 함께 상승 (2401.10463) → data-first 순서가
  Data Efficiency Hypothesis 와 정합. north-star + §15/§51/§72 milestones
  UNCHANGED, GOAL 미도달 — §103 은 통합 2축 fire-decision 을 RESOLVABLE
  하게 만들지 decided 한 게 아님. 후속 (§8 step B 권장): Sequential 의
  데이터-fire 를 실제 dispatch (cost-bearing, separate cycle per
  g_fire_autonomous + g_fire_dispatch_robust + g_resource_active_parallel).
