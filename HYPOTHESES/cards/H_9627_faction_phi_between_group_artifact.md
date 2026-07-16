---
id: H_9627
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_phi_between_group_artifact
title: 옛 파벌 Φ-proxy 는 통합이 아니라 집단간분산이다 — 참값 0 에서 K 에 단조증가 (법칙 22 순환논법)
status: PROPOSED
tier: 🔴 계기-인공물 실측(PEDESTAL $0 · DIRECTIONAL) · Fable α1 ⊕ Sol F01/F02 수렴
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9292, H_072, H_125
---

# H_9627 — 옛 파벌 Φ-proxy 는 통합이 아니라 집단간분산이다 — 참값 0 에서 K 에 단조증가 (법칙 22 순환논법)

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
