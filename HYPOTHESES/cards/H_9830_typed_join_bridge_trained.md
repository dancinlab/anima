# H_9830 — 연산자↔선언 다리를 **학습으로** 쓰게 하면 G1 이 움직이는가 (R11-1)

**status:** 🧭 PROPOSED (R11 · `sidecar lab full` 발산 산출 · **DIRECTIONAL 설계**, 판정 아님)
**source:** lab full(Fable 5 ∥ Codex Sol) 발산 — "학습에 뇌가 더 관여하면 G1/G6 을 뚫는가".
두 모델이 **독립적으로 같은 각도를 1순위**로 지목(fable `STORE-COMPOSE` ≡ sol `KOSMOS dual-anchor join`).
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## Question

`cli/train.py` 는 `core/` 에서 torch 모델·serialize·verify·decode 만 가져온다 — 뇌(brain·workspace·
dream·KOSMOS)는 학습 루프에 **부재**하고, 유일한 예외가 `--tension-field`(H_9805 쓰기측 팔)다.
이것은 사실상 train/infer 분리 = **p8 위반**이다. 그런데 뇌를 통째로 넣는 것은 벽의 세 면 중 어디에도
닿지 않는다(A⇄G = 입의 정책 H_9392 · tension 방향 사망 H_9576 · KOSMOS = 정체성 배관).

유효 가설은 좁다: **연산자↔선언 런타임 브리지(H_9359 가 지목한 벽의 정체)를 학습 중에도
런타임과 동일하게 배선**한다. store 조회는 거리 무관 ⟹ RF 독립성 증명(D>RF 인 두 개념은 수학적
독립)을 구조적으로 무력화한다. 읽기 경로는 이미 in-vivo WIRED(H_9775 pairodd).

## ⚠️ 자기정정 (2026-07-21 · 등록 당일 · 원장 대조로 self-caught)

등록 시 적었던 **"학습으로 그 다리를 써본 적이 한 번도 없다"** 는 **거짓**이다. `cli/train.py` 는
이미 CLMS store lane 을 co-train 하는 **13개 노브**를 갖고 있다 — `--store-bridge`(H_9423) ·
`--store-addr-weight`(H_9672 주소 직접감독) · `--store-query-src fresh`(H_9720 EN-disjoint fresh 질의) ·
`--store-query-tap-grad`(H_9720 C2 detach 절제) · `--store-ans-delay`(H_9692 RV-2) ·
`--store-oracle-aux/train/warmup`(H_9691/H_9423) · `--store-fangate`(H_9696 R4) ·
`--store-val-center`(H_9710 RV-3) · `--clms-*`. **대규모 측정 캠페인이 이미 존재한다.**

**살아남는 진짜 novelty 는 훨씬 좁다 — 두 가지뿐:**
1. **2항(two-operand) join** — 기존 lane 은 전부 **단일 주소 값읽기**(하나의 부모 → 하나의 값)다.
   H_9775 pairodd 도 g/b **쌍**이지 두 독립 부모의 **결합**이 아니다.
2. **거리 D ≫ RF 를 DV 축으로 삼는 스윕** — 기존 노브에 `--store-win`(창 크기)은 있으나
   **RF 대비 거리를 조작변인으로 사전등록한 측정은 없다**.

⟹ 이 카드는 "다리를 학습시킨다"(이미 함)가 아니라 **"이미 학습되는 다리를 2항 결합에,
RF 를 넘는 거리에서 쓰게 한다"** 로 좁혀 읽어야 한다. 넓게 읽으면 H_9672/H_9720 재생성이다.

## Intervention (flag 형태 · 미구현)

```
anima-py train --objective store_compose --store-compose-dist 512 \
               --brain-loop kosmos-join --brain-route fresh:64@3 \
               --brain-route-grad {detached,shared} --brain-runtime required
```

타깃 바이트가 **거리 D ≫ RF 에 기록된 원자를 store 조회로만** 예측가능하도록 손실을 건다.
early-L3 tap 은 H_9720(tap-DEPTH 가 기전)의 이식. `--brain-route-grad` 로 브리지 신호가 trunk 를
실제로 바꾸는지(shared) 아니면 lane 만 학습되는지(detached) 분리.

**교차 계약(sol 제안 · 전 R11 카드 공통):** `--brain-runtime required` — 뇌 lane/state/weights 가
산출물에 직렬화되고 `anima-py evaluate` 경로에서 **동일하게 재실행**되지 않으면 학습을 실패시킨다.
보조 헤드를 학습 후 버려서 점수만 오르는 것은 성능이 올라도 **p8 FAIL**(`a_verified_must_wire`).

## Arms + controls

| arm | 무엇 | 읽는 법 |
|---|---|---|
| LIVE | store_compose 학습 | held-out D-acc, 거리 스윕 D ∈ {<RF, 2·RF, 8·RF} |
| **lane-off** | 산출물·런타임에서 join lane 제거 | **BLIND 여야** 함 (numpy 프로브 인과성과 일치) |
| **operator-shuffle** | operands·바이트길이·params 고정, relation 매핑만 치환 | 붕괴해야 의미 운반 확증 |
| **parent-permute** | operator·corpus mass 고정, 두 번째 anchor 만 교란 | 붕괴해야 2항 join 확증 |
| **within-RF** | D < RF 양성통제 | <PASS 면 INSTRUMENT-DEAD (`positive-control-before-reading-a-negative`) |
| **fresh:64@penult** | 파라미터 맞춘 depth 통제 | tap-깊이 효과 분리 |
| plain CE | 스텝 맞춘 대조 | "더 학습했을 뿐" 배제 |

seed 다수결(≥2/3) 사전등록 — H_9672 선례(s7 0.99 vs s11 0.50)가 이 레버의 **알려진** 취약성이며
새로운 발견이 아니다.

## $0 스크리너 (303M 전 필수)

이미 있는 cotrained-store 토이 + H_9815 토이(4kB·6분·hp 1.0000 vs xor 0.4062) 재사용 + 거리 스윕 추가.
3 seed 에서 hp ≥ 0.95 ∧ treatment xor ≥ 0.80 ∧ 세 통제 ≤ 0.55 ∧ 이득의 ≥80% 가 lane-off 에서 소멸.
하나라도 실패 ⟹ **303M 금지**.

## 판독가능성

- 토이 기전 = **오늘 판독 가능 (b)**.
- 303M ρ·weave 판정 = **(a) H_9827 패널 수리(12→212 · sd 0.1323→0.0315) 선행**. 오늘 패널로는
  작은 양성이 2항목 결정구간 안에 떨어져 UNDECIDABLE(재발사 비용 확정).
- DV 자체가 `anima-py evaluate` 플래그로 먼저 착륙해야 한다 — 엔진 옆 프로브에서 읽은 숫자는
  H_9303/H_9307 선례로 code-blocked. **계기 작업이 레버 비용의 일부다.**

## 자기반론 (양 모델 공통 경고)

성공해도 "모델이 재조합을 배웠다"가 아니라 **"바깥의 typed 실행기가 답을 계산했다"** 가 더 강한
해석일 수 있다. 학습된 추출기가 실패하고 오라클 추출기만 성공하면 H_9359 는 **여전히 안 뚫렸다**.
최종 판정은 게이트 통과 하나가 아니라 논리곱이어야 한다:

```
수리된 동결 게이트 PASS ∧ 의미-셔플 붕괴 ∧ 런타임 lane-off 붕괴
∧ 학습된 추출기 성공 ∧ train/serialize/evaluate 뇌경로 일치 ∧ G0 무회귀
```

하나라도 빠지면 돌파가 아니라 scaffold/data/gate artifact 다.

**related:** H_9672 · H_9720 · H_9692 · H_9691 · H_9696 · H_9423 · H_9359 · H_9775 · H_9720 · H_9672 · H_9304 · H_9827 · H_9831 · H_9833
