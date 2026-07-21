# H_9836 — 깊은 trunk(L≥8) 대조팔 — "뇌 덕분"을 **깊이 오귀인**과 가르는 필수 통제 (R11-7)

**status:** 🧭 PROPOSED (R11 · lab full 발산 · **DIRECTIONAL 설계**, 판정 아님 · **뇌 레버가 아니라 통제팔**)
**source:** fable `L5 DEEP-TRUNK L≥8` — **NOVEL**(sol 미언급). fable 정직 각주: raw 정보/$ 기준으로는
**이 비-뇌 팔이 보드에서 단일 최고의 303M 발사일 수 있다**.
**wired:** no — 미구현(`--layers 8` 자체는 존재 · 미실행).

## Question

프런티어 맵은 deep ConvMoE 를 **OPEN**(미실행)으로 두고 있고 도달가능성 프로브는 이미 양성이다:
`conv_L1 reach=0`(벽 재현) vs `conv_L8 reach=1.47e-3 REACHABLE`, lane-OFF 절제 = BLIND(lane 인과).
production `.clm` 이 E2/L1 단일 conv trunk 라 RF = L(K−1)+1 이 작고, 거리 D>RF 인 두 개념은
**수학적으로 독립 ⟹ 재조합 불가**(capacity 무관). H_1394 가 이를 격리(302.6M ConvMoE-L1 FALS=0
vs 303M L24 ByteGPT FALS=1.0).

## 왜 이 카드가 R11 에 있는가

**R11 의 모든 뇌 레버는 같은 발사 안에서 `--layers 8` 을 계산 맞춘 조건에서 이겨야 한다.**
못 이기면 "뇌를 학습에 넣어서 뚫었다"가 아니라 **재귀 깊이 오귀인**이다.

## Intervention

```
anima-py train --layers 8 …   # 계산·파라미터 맞춤, 뇌 레인 전부 OFF
```

## 판독가능성

- ρ·weave terminal = **(a) H_9827 패널 수리 선행**(다른 R11 카드와 동일).
- 단, 이 팔은 **뇌 가설과 독립적으로도 과학적 가치**가 있다 — 벽의 RF-bound 면을 직접 잰다.

**related:** H_1394 · H_1584 · H_9259 · H_9827 · H_9830
