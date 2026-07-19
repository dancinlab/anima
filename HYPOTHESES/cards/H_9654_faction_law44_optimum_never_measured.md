---
id: H_9654
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_law44_optimum_never_measured
title: 법칙 44 'σ(6)=12 가 최적 파벌 수' 는 K>12 를 한 번도 재지 않았다 — 2점(12 vs 8) 비교 + 수론적 prior 일 뿐
status: 🔴 MEASURED · DIRECTIONAL (K>12 최초 측정 — 정점 없음 · argmax=그리드끝 · K=12 서 real<pedestal)
tier: 🔴 아카이브 감사 실측($0) · '정점 12' = 미측정 주장 · Fable α2 ⊕ Sol F03
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9627, H_067, H_125
---

# H_9654 — 법칙 44 'σ(6)=12 가 최적 파벌 수' 는 K>12 를 한 번도 재지 않았다 — 2점(12 vs 8) 비교 + 수론적 prior 일 뿐

## 주장 (반증가능)

아카이브 전수 grep: 16·24·32 파벌 Φ 기록 **0건**. 법칙 44 의 유일 근거 = 12-faction Φ=131.44 > 8-faction Φ=122.45(+7.3%). 12 는 σ(6)=12(6의 약수합 · H_067 perfect-number architecture)라는 **수론 미학**에서 먼저 정해졌고 사후 2점으로 확증됐다. PEDESTAL 은 같은 방향을 +60% 로 재현(0.1175 vs 0.0733) — 참값 0 에서.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-phi-proxy --n-factions-sweep 1,2,4,8,12,16,24,32,64`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

proxy 의 **단조성**. 순수산수 예측=단조증가(정점 없음). 법칙 44 주장=12서 정점(K=16 이 12보다 낮아야).


## 🔬 $0 아카이브 감사 (2026-07-17 · 이 세션)

`archive/hypotheses_snapshots/` 전수 grep — **16·24·32 파벌 Φ 기록 0건**.

법칙 44 의 전체 근거(`RESEARCH-FINDINGS-20260329.md:9`):
```
| 44 | σ(6)=12가 최적 파벌 수 | 12-faction Φ=131.44 > 8-faction Φ=122.45 (+7.3%) |
```
**2점 비교가 전부.** K=16 이 12보다 낮다는 측정이 없으므로 **정점(optimum)은 측정된 적이 없다**.

### 12 는 어디서 왔나 — 측정이 아니라 수론

`H_067_perfect_number_architecture.md:40` :
```
consciousness arch exposes σ(6)=12 factions / φ(6)=2 min cells / τ(6)=4 stages / sopfr(6)=5 axes
```
12 = σ(6) = 6의 약수합(1+2+3+6). **완전수 미학에서 먼저 정해지고 사후 2점으로 확증**됐다.
같은 문서군이 φ(6)=2 → "engine states 2개(A·G)", τ(6)=4 → "4 stages" 도 같은 방식으로 유도한다.

### 교차 긴장 (아카이브 내부 모순)

`H_125_law_212`: "evolution converges on **few factions (4)**; 4-faction = local optimum under
evolution; 12-faction = global optimum **when preset**" — 진화가 자유롭게 고르면 **4** 로 갔고,
12 는 **사람이 미리 박았을 때만** 최적이다. 이 문서 자신이 "4 vs 12 gap may collapse under
different fitness function" 이라고 적어뒀다.

### 판정

- 법칙 44 = **UNMEASURED CLAIM**(반증된 게 아니라 애초에 측정 안 됨).
- PEDESTAL(H_9627)이 참값 0 에서 12>8 을 +60% 로 재현 ⟹ 법칙 44 의 +7.3% 는 신호로 읽을 근거 없음.
- 정점의 실재는 K∈{16,24,32,64} 를 재기 전엔 **판정 불가**.


## 🔬 K>12 스윕 실측 (2026-07-17 · `--faction-phi-proxy --n-factions-sweep …,64,128`)

아카이브가 한 번도 재지 않은 K>12 를 engine-native 로 쟀다(303M · d=3784).

| K | real | pedestal | real/ped |
|---:|---:|---:|---:|
| 8 | 0.020243 | 0.022513 | 0.899 |
| **12** | **0.031277** | **0.038878** | **0.804** |
| 16 | 0.058421 | 0.048062 | 1.216 |
| 24 | 0.060723 | 0.074624 | 0.814 |
| 32 | 0.113218 | 0.101398 | 1.117 |
| 64 | 0.221908 | 0.209773 | 1.058 |
| 128 | 0.406705 | 0.419283 | 0.970 |

- **정점 없음**: argmax_K(real) = 128 = 그리드 끝. K=16·24·32·64·128 이 전부 K=12 보다 **높다**.
  ⟹ 법칙 44 의 '12 = 최적' 은 살아있는 활성에서 재현되지 않는다.
- K=12 에서 real/ped = **0.804 < 1** — 진짜 활성이 참값 0 잡음보다 낮다.
- 아카이브가 K>12 를 안 쟀기에 '정점'은 **미측정 주장**이었고, 재보니 **정점 자체가 없다**.

### 정직범위
법칙 44 의 반증이 아니라 **그 주장이 애초에 측정 없이 세워졌고, 측정하니 지지되지 않는다**는 것.
옛 엔진 동역학 미재현 ⟹ DIRECTIONAL. 8 prompts · EN · 단일 ckpt · 단일 seed.

## 통제군 (≥2 · 사전등록)

① 산수 null(i.i.d. — 반드시 단조) ② rank-8 합성 양성(8서 정점 나와야 계기 유효)

## 사망조건 (사전등록 · tune-to-green 금지)

real 활성이 K=16,24,32 서 **계속 상승(단조)** ⟹ 법칙 44 반증 = 순수 산수. 양성대조서 정점 미출현 ⟹ 계기 무효(판정불가).

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

법칙 22(단조 2.1×) vs 법칙 44(정점12) 의 **내부모순**을 처음 대질. 어느 각도도 K>12 를 안 쟀다.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
