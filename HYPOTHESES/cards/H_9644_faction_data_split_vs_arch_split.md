---
id: H_9644
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_data_split_vs_arch_split
title: 파벌 이득 = 데이터-분할이지 아키텍처-분할이 아니다
status: PROPOSED
tier: 🟡 데이터 vs 구조(pool/GPU) · Fable α14
cost: pool/GPU
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9304, H_9639
---

# H_9644 — 파벌 이득 = 데이터-분할이지 아키텍처-분할이 아니다

## 주장 (반증가능)

`corpus --n-clusters K`(토픽 분할 커리큘럼)와 `train --n-factions K`(구조 분할)는 혼동돼 있다. G1 벽이 이미 DATA 벽으로 판정났다(H_9304).

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py corpus --n-clusters K` vs `anima-py train --n-factions K`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

모든 DV(recomb·CE). 예측: 데이터분할 ≥ 구조분할이면 파벌 아키텍처 잉여.

## 통제군 (≥2 · 사전등록)

① 단일 코퍼스 null ② 랜덤 클러스터 배정 scramble

## 사망조건 (사전등록 · tune-to-green 금지)

구조-파벌이 데이터-클러스터를 유의하게 이기면 ⟹ 아키텍처가 실재 레버(잉여 가설 사망).

## 비용

pool / GPU-fire

## 왜 새로운가 (기존 각도 대비)

`g1-wall-is-data-not-estimator`(H_9304) 를 파벌축에 이식. 두 혼동된 분할을 분리.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
