# H_9839 — 꿈의 타깃을 기하 중점에서 선언규칙 파생으로 교체한다 (R12-2)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측

`core/dream_compose.py`(124줄) 헤더가 스스로 밝힌다: 두 co-replay 앵커를
**"coord midpoint · tension5 mean · radius max · lane=dream"** 으로 섞는
**"a designed geometric law (NOT a learned semantic insight, c9)"**. 즉 현재 꿈은
**좌표 평균**이지 의미 합성이 아니다. `dc_coreplayed` / `dc_compose_window` / `dc_cosine` 보유.

## 가설

기하 중점은 **정의상 가법적**이다(두 벡터의 평균에는 새 결합정보가 없다) — H_9304 가 잰
비가법 정보 ≈ 0 과 정확히 같은 자리에 있다. 타깃을 **선언된 재조합 규칙의 파생**으로 바꾸면
H_9287(재조합 대수는 물리 정보를 더한다)이 측정한 정보를 꿈이 실제로 제조한다.

## Intervention (flag 형태 · 미구현)

```
anima-py train --dream-target {midpoint,rule-derived,shuffled} --dream-mix 0.10 --lang en
```

`midpoint` = 현행 재현(음성 기준선) · `rule-derived` = 처치 · `shuffled` = 주변분포 동일 통제.

## Arms + controls

| arm | 읽는 법 |
|---|---|
| `midpoint` | **사전등록 실패 기준선** — 처치가 이걸 못 이기면 꿈 각도 전체가 죽는다 |
| `shuffled` | 붕괴해야 (주변분포만 같음) |
| 크기맞춘 실제 corpus | "데이터가 늘었다" 배제 |

## H_9831 과의 관계 (중복 아님)

H_9831 은 **혼합비·replay 정책**(error vs uniform)이 DV 였다. 이 카드는 **타깃 자체의 대수**가
DV 다 — `midpoint` 기준선이 여기 처음 사전등록된다. 두 카드는 직교하며 같은 발사에 합칠 수 있다.

## $0 스크리너

`dc_compose_dream_anchor` 가 순수 스칼라라 ckpt 불요. 토이 store 위에서 midpoint vs rule-derived
가 만든 데이터의 **교차경계 정보량을 H_9844(mi_compress)로 직접 측정** — 학습 전에 판별된다.

**related:** H_9304 · H_9287 · H_9831 · H_9844
