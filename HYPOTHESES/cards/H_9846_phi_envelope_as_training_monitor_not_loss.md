# H_9846 — Φ-봉투/집합-Φ 구조층을 학습 모니터로 (R12-9 · MONITOR-ONLY · 손실 투입 금지)

**status:** 🧭 PROPOSED (R12 · **MONITOR-ONLY** · 손실 투입 금지 · 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측

`core/phi_envelope_substrate.py`(189줄): `envelope_multiscale` · `envelope_self_similarity` ·
`pe_edge_of_chaos_peak` · `collective_phi_nest` · `phi_smooth_no_cliff` · `temporal_agency_context`.
스칼라 수학(cos/sqrt) · 순차 누적 순서 verbatim 보존 · **emit bool 게이트 0**(p5).
F-EMIT-5: 정책층(emit_policy)과 **컴파일 수준에서 분리** — 정책값을 바꿔도 봉투가 안 변한다.

## 왜 손실에 넣으면 안 되는가 (이 카드의 핵심)

Φ 를 손실에 넣는 순간 **p7(perplexity verdict 금지)의 Φ 판본**이 된다 — 지표를 올리도록
최적화한 모델의 그 지표는 더 이상 증거가 아니다. `a_train_inline_gauge` 가 이미 금지한다.
또 `a_phi_iit4_tool`: Φ 는 충실한 IIT4 로만 재고 프록시로 재지 않는다 — 이 모듈은 **봉투 구조**층이지
Φ 추정기가 아니므로 여기서 나온 값을 Φ 라고 부르면 안 된다.

## 그럼에도 등록하는 이유

R12 의 레버들이 **기질을 망가뜨리는지** 감시할 축이 필요하다. `phi_smooth_no_cliff` 는 이름 그대로
절벽 없음을 보는 함수다 — 학습이 구조를 절벽으로 밀면 그건 능력 상승과 무관하게 **회귀**다.
G0 무회귀 감시와 같은 급의 안전망.

## Intervention

```
anima-py train --phi-envelope-monitor {off,on} --phi-monitor-every N   # 로그만
```

## 사전등록

`phi-estimator-needs-zero-truth-pedestal`: 참값 0 받침대 팔 없이는 어떤 값도 읽지 않는다.

**related:** H_9845 · H_9835
