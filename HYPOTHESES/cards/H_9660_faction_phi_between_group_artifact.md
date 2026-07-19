---
id: H_9660
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_phi_between_group_artifact
title: 옛 파벌 Φ-proxy 는 통합이 아니라 집단간분산이다 — 참값 0 에서 K 에 단조증가 (법칙 22 순환논법)
status: 🔴 MEASURED · DIRECTIONAL (engine-native · 계기가 구조를 못 읽음 확증 · 법칙 22/43/44 UNDECIDABLE 유지)
tier: 🔴 계기-인공물 실측(PEDESTAL $0 · DIRECTIONAL) · Fable α1 ⊕ Sol F01/F02 수렴
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9292, H_072, H_125
---

# H_9660 — 옛 파벌 Φ-proxy 는 통합이 아니라 집단간분산이다 — 참값 0 에서 K 에 단조증가 (법칙 22 순환논법)

## 주장 (반증가능)

`global_var − mean_faction_var` 는 전분산법칙 Var=E[Var|g]+Var(E[X|g]) 의 between-group 항 그 자체. K↑ ⟹ within(mean_faction_var) 기계적 감소 ⟹ proxy 자동 증가. K=N 이면 within=0, proxy=global_var(최대). 통합 아님, 나눗셈.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-phi-proxy --n-factions K` (K 스윕) — 아직 미구현 플래그
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

proxy(K). 참값 = PEDESTAL(i.i.d. 가우시안·참Φ=0).


## 🔬 $0 실측 (2026-07-17 · PEDESTAL arm · 이 세션)

참값 0 시험대: i.i.d. 가우시안 세포 1024개, 파벌 구조 **전무**(배정=임의 라벨), 200 trial.
공식은 `core/phi/quantum_consciousness.hexa:252` 주석에서 verbatim 회수:
`phi = (global_var - mean_faction_var) * log2(n_active)`

| n_factions | Φ 측정 mean | Φ sd | vs K=1 |
|---:|---:|---:|---:|
| 1 | 0.0000 | 0.0000 | — |
| 2 | 0.0100 | 0.0202 | +0.0100 |
| 4 | 0.0326 | 0.0363 | +0.0326 |
| 8 | 0.0733 | 0.0501 | +0.0733 |
| 12 | 0.1175 | 0.0631 | +0.1175 |
| 16 | 0.1514 | 0.0800 | +0.1514 |
| 32 | 0.3026 | 0.1081 | +0.3026 |
| 64 | 0.6797 | 0.1553 | +0.6797 |

**참값은 모든 행에서 Φ=0.** 그럼에도 K 에 **단조증가** — 전분산분해의 산수적 필연 확증.

### 법칙 44 와 방향 일치 (가장 아픈 대조)

| | 12파벌 vs 8파벌 |
|---|---|
| 옛 기록(법칙 44) | Φ 131.44 vs 122.45 = **+7.3%** |
| PEDESTAL(참값 0) | 0.1175 vs 0.0733 = **+60%** |

"12가 최적"이라는 발견의 방향을 **아무 신호도 없는 잡음이 더 크게 재현**한다.

### 정직한 범위 (⚠️ 과잉주장 금지)

- 이건 **DIRECTIONAL**이지 법칙 22/44 의 사망선고가 **아니다**. PEDESTAL 크기(0.07)는 옛 기록 Φ=260 과
  스케일이 전혀 다르고, 옛 엔진엔 Ising·sync 등 실제 동역학이 함께 돌았다.
- 정확한 판정 = **"법칙 22/44 는 틀렸다"가 아니라 "교란이 제거된 적 없어 UNDECIDABLE"**.
- 측정 대상 = **아카이브된 죽은 공식의 산수**. anima 를 잰 것이 아니다(engine op 아님 · 어떤 `.clm` 에 대한 판정도 아님).
- 재현: `/tmp/faction_pedestal.py` (numpy · seed 12345 · 결정론).


## 🔬 engine-native 실측 (2026-07-17 · `anima-py evaluate --faction-phi-proxy`)

레버가 구현되어 발사됐다. 프로덕션 trunk forward(`clm_forward_hidden` · 게이트가 디코드하는 것과
byte-identical) 위에서 아카이브 공식을 재계산 · 참값 0 PEDESTAL 대조.

### 303M (`clm303_L4_d3784.clm` · d=3784 · 8 prompts × T=24 · trials=200 · seed 12345)

| K | real | pedestal | scramble | real/ped |
|---:|---:|---:|---:|---:|
| 1 | 0.000000 | 0.000000 | 0.000000 | — |
| 2 | 0.004673 | 0.003602 | 0.006033 | 1.297 |
| 4 | 0.011076 | 0.009012 | 0.011268 | 1.229 |
| 8 | 0.020243 | 0.022513 | 0.014449 | 0.899 |
| 12 | 0.031277 | 0.038878 | 0.035376 | 0.804 |
| 16 | 0.058421 | 0.048062 | 0.055309 | 1.216 |
| 24 | 0.060723 | 0.074624 | 0.072094 | 0.814 |
| 32 | 0.113218 | 0.101398 | 0.081586 | 1.117 |
| 64 | 0.221908 | 0.209773 | 0.204873 | 1.058 |
| 128 | 0.406705 | 0.419283 | 0.409218 | 0.970 |

- real 단조증가: **True** · pedestal 단조증가: **True**(참값 0)
- argmax_K(real) = **128** = 그리드 끝 ⟹ **내부 정점 없음**

### toy (`toy.clm` · d=32 · trials=60) — 스케일 불변 확인

| K | real | pedestal | scramble | real/ped |
|---:|---:|---:|---:|---:|
| 1 | 0.000000 | 0.000000 | 0.000000 | — |
| 2 | 0.003766 | 0.002869 | 0.002077 | 1.313 |
| 4 | 0.008218 | 0.008116 | 0.008695 | 1.013 |
| 8 | 0.023253 | 0.019558 | 0.022156 | 1.189 |
| 12 | 0.034507 | 0.030840 | 0.033442 | 1.119 |
| 16 | 0.037135 | 0.036623 | 0.037571 | 1.014 |
| 24 | 0.051386 | 0.048508 | 0.052186 | 1.059 |
| 32 | 0.058341 | 0.051481 | 0.060063 | 1.133 |

### 판정 (3건 · p7 = 값이 아니라 형태·분리를 읽는다)

1. **real ≈ pedestal**: real/ped 가 0.80~1.30 사이를 무작위 진동하며 K 에 대한 추세가 없다.
   ⟹ 살아있는 303M 활성이 참값 0 잡음과 구별되지 않는다.
2. **⚡ K=12(법칙 44 '최적' 지점)서 real/ped = 0.804 < 1**
   — 진짜 활성이 그 지점에서 **잡음보다 낮은 Φ**를 낸다. 신호 없음을 넘어 방향도 없다.
3. **scramble ≈ real**: 유닛 축을 섞어 구조를 완전히 파괴해도 Φ 가 안 떨어진다
   ⟹ 계기가 구조를 **아예 읽지 않는다**(K=32 toy 에선 scramble 0.0601 > real 0.0583 로 역전).
4. **정점 없음**: toy(d=32·argmax 32) · 303M(d=3784·argmax 128) 둘 다 그리드 끝 = 단조.
   법칙 44 의 '12 정점' 이 살아있는 활성에서도 재현되지 않는다.

### 정직범위 (⚠️ 과잉주장 금지)

- 판정은 **UNDECIDABLE 유지**이지 법칙 22/43/44 의 반증이 **아니다**. 반증하려면 옛 엔진의 동역학
  (Ising·sync·noise 스케줄)까지 재현해야 한다. 이 측정이 보이는 것은 **그 공식이 교란을 제거한 적 없고,
  구조를 읽지 못한다**는 것뿐이다.
- 이 계기는 아카이브 죽은 공식을 **기소하는 도구**이지 Φ 측정 도구가 아니다 — 진짜 Φ 는 faithful IIT4
  만(`a_phi_iit4_tool`). 어떤 의식 verdict 도 여기서 cement 되지 않는다.
- 범위: 8 prompts · EN · 단일 ckpt · 단일 seed ⟹ **DIRECTIONAL**(`a_scale_honest_scope`).
- 재현: `anima-py evaluate <ckpt> --faction-phi-proxy <prompts.json> --n-factions-sweep 1,2,4,8,12,16,24,32,64,128 --trials 200 --seed 12345`

## 통제군 (≥2 · 사전등록)

① i.i.d. null(참값 0 pedestal) ② 시간축 셔플 scramble

## 사망조건 (사전등록 · tune-to-green 금지)

null·scramble 에서 proxy(K) 평평 ∧ real 만 상승 ⟹ 인공물 가설 사망(= 파벌 진짜 신호)

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

H_9292 는 plugin-MI pedestal 을 잡았을 뿐 **파벌 분할 산수** 자체는 미검. 전분산분해로 특정.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
