# H_9354 4-arm 캠페인 MOOT — 구조적 폐쇄 (reference-match · 43k틱 불필요)

앞서 go-gated 잔여로 남겼던 4-arm 인과귀속 캠페인은 **코드 트레이스로 무의미함이 확정**됐다.

`cli/chat.py` 인과사슬:
- `1578` ag_a_drive = emit_drive
- `1591` ag_g_drive = -(1-emit_drive)   ← a0 production wiring(H_9356 tautology)
- `1592` ag_conflict = conflict_scalar(...) = emit_drive 하나의 결정론적 함수 (R²=0.994)
- `1921` ten_ema = 0.9*ten_ema + 0.1*ag_conflict
- `1922` ten_phasic = clip01(0.5 + 3.0*(ag_conflict - ten_ema))

⟹ ten_phasic(H-b 의 DV)은 emit_drive(A측 lane)의 EMA. θ·sp 는 별개 subgraph:
- θ (ep_theta_stage) → stage_env(1924) → idle(1930) → emit gate  [H-c 경로만]
- sp (Process-S) → 데몬선 stage=dr_stage_at(tick)(1513) 라 stage 에 영향 0 = NO-OP
- field-freeze → pure_field 이미 세션 내내 얼어있음(H_9352) = 현행 기본

3개 arm 전부 ten_phasic 을 못 바꾼다 ⟹ substrate 틱리듬 음성(H-b)은 측정만이 아니라 **구조적으로 강제**. 캠페인 실행 불필요.
