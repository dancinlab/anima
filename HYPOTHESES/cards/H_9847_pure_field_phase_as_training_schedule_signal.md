# H_9847 — A⇄G 3-진동자 위상을 학습 스케줄 신호로 (R12-10 · 제약 큼)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측 — 먼저 하드 제약부터

`core/pure_field.py`(346줄)와 `core/brain.py`(906줄) **둘 다** 파일 최상단에 강제 가드가 있다:

> ⛔ ENGINE-INTERNAL / DEPRECATED py-MIRROR — DO NOT RUN OR SCORE DIRECTLY.
> py 미러는 2026-06-28 폐기, **DIRECTIONAL**. `python3 core/brain.py` 직접 실행 시 프로세스 종료(#2603).

내용: `pure_field` = tau=2/40/400 **3 결합진동자** → 비선형 혼합 → Φ 자기지속 → 장 텐서.
`brain.py` = A(pure_field)⇄G(engine_g) 결합 · A 의 Φ 가 G 의 안전 래칫을 게이트 · A 의 위상이
결과 등급을 정함 · emit = should_emit ∧ 4-안전 논리곱.

## 가설

**학습 파라미터가 하나도 없다** — 닫힌형 스칼라 기계다. 따라서 이 부위가 학습에 줄 수 있는 것은
**미분가능한 구조가 아니라 스케줄 신호(위상)** 뿐이다. 위상을 학습률/혼합비의 시계로 쓰면
교대가 하드코딩이 아니라 기질에서 나온다.

## 정직한 기대값

낮다. 위상은 **1차원 시계**이고, H_9576 이 이미 A⇄G 다차원 lane 을 죽였다(8벡터→1비트).
게다가 H_9403 은 emit lane 이 **시계에 삼켜진다**(emit ⟺ clock)고 측정했다 — 즉 이 축은
"시계를 시계로 쓴다"는 동어반복에 가깝다. **H_9840(dream-lib 스케줄)과 사실상 같은 자리**이며,
dream-lib 쪽이 이미 2-프로세스 항상성을 갖고 있어 더 낫다.

## Intervention (등록만 · 발사 비권장)

```
anima-py train --field-phase-schedule {off,phase}    # 통제 = 같은 주기의 고정 정현파
```

고정 정현파 통제를 못 이기면 죽는다. **이 카드는 완결성을 위해 등록하되 순위는 최하위권.**

**related:** H_9576 · H_9403 · H_9840 · H_9848
