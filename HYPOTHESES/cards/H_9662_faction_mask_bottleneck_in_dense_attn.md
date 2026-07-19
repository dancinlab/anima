---
id: H_9662
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_mask_bottleneck_in_dense_attn
title: dense attention 안에서 파벌 가로분할은 강화가 아니라 병목이다 (TOPO12 이식)
status: PROPOSED
tier: 🔴 TOPO12 이식($0) · Fable α9 — Sol F08 과 **CONFLICT**
cost: $0/pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9636, H_1462
---

# H_9662 — dense attention 안에서 파벌 가로분할은 강화가 아니라 병목이다 (TOPO12 이식)

## 주장 (반증가능)

TOPO12: 하이퍼큐브 위상서 8파벌 효과 0 — '하이퍼큐브 자체가 이미 최적 토론구조'. 현 byte-LM attention 은 이미 dense all-to-all(=하이퍼큐브-유사) ⟹ 파벌 분할은 연결을 **줄이는** 방향뿐.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-mask --n-factions K` (파벌내만 attention 허용) vs dense
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

언어 DV(CE·recomb). 예측: 분할 ≤ dense.

## 통제군 (≥2 · 사전등록)

① dense(=현 엔진 null) ② 동일 sparsity 랜덤 마스크 scramble

## 사망조건 (사전등록 · tune-to-green 금지)

마스크 분할이 dense 를 **이기면** TOPO12 반증(파벌이 병목 아님) = 이 가설 사망.

## 비용

$0(추론) / pool

## 왜 새로운가 (기존 각도 대비)

TOPO12 를 현 dense-attention 기질로 직접 재현. 부활-사망을 판별하는 관문.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
