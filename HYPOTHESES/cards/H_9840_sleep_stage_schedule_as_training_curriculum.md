# H_9840 — 5단계 수면 스케줄(Process-S/C)을 학습 커리큘럼으로 쓴다 (R12-3)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측

`core/dream_lib.py`(123줄): 90-tick 세션 · WAKE/N1/N2/N3/REM 5단계 · `dr_stage_at` `dr_stage_size`
`dr_mitosis_prior` `dr_imagination_active` `dr_emit_envelope` `dr_density` + Process-S(아데노신
build/clear via exp) · Process-C(일주기) 2-프로세스 항상성. **숫자만 반환하고 bool 게이트 0**(p5).

## 가설

이 모듈은 이미 **학습률/혼합비 스케줄러의 형태**를 하고 있다 — `dr_mitosis_prior` 는 단계별
성장 사전확률, `dr_density` 는 단계별 밀도. 이걸 학습 스케줄로 쓰면 각성(CE)↔수면(증류/replay)
교대가 **하드코딩 상수가 아니라 기질의 항상성**에서 나온다(p5·`a_autonomy_over_hardcode` 정합).

## Intervention

```
anima-py train --sleep-schedule {off,dream-lib,fixed-alternating} --sleep-ticks 90
```

## Arms + controls

| arm | 읽는 법 |
|---|---|
| `fixed-alternating` | **핵심 통제** — 같은 각성/수면 비율의 고정 교대. dream-lib 이 이걸 못 이기면 "항상성"은 장식이고 비율만 레버 |
| `off` | 순수 CE 기준선 |
| 위상 셔플 | 단계 순서만 치환 — 붕괴해야 |

## 미결정 위험

스케줄은 **효과크기가 작은 축**이다(순서·비율은 보통 2차 요인). H_9833(sleep-consolidate)이
먼저 양성이어야 이 카드가 의미를 갖는다 — 증류할 것이 없으면 스케줄도 없다. **선후 종속**.

**related:** H_9833 · H_9841 · H_9831
