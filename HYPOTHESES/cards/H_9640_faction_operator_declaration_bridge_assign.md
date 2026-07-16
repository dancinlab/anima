---
id: H_9640
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_operator_declaration_bridge_assign
title: cross-debate 가 H_9359 '연산자↔선언 런타임 다리' 를 문자 그대로 놓는다
status: PROPOSED
tier: 🟢⭐ G1 아키텍처 다리(GPU) · Fable α13 NOVEL
cost: GPU
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9359, H_9267, H_9304, H_9423
---

# H_9640 — cross-debate 가 H_9359 '연산자↔선언 런타임 다리' 를 문자 그대로 놓는다

## 주장 (반증가능)

H_9359 = 벽의 정체 = 연산자↔선언 런타임 다리 부재. 파벌을 2개로 놓고 **연산자 파벌 / 선언 파벌** 로 명시 배정하면 cross-debate 가 곧 그 다리다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py train --n-factions 2 --faction-assign operator,declaration --cross-debate`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

held-out **연산자-적용-선언** D-acc. 우연 0.5, bar ≥0.9.

## 통제군 (≥2 · 사전등록)

① cross 없음(intra-only = 현 G1 fail) ② 배정 scramble ③ 데이터-다리(H_9267 XBIND corpus) 대조

## 사망조건 (사전등록 · tune-to-green 금지)

아키텍처 다리 D-acc ≈ 우연 ⟹ 다리는 데이터지 구조 아님(`g1-wall-is-data-not-estimator` 확증) = 파벌 사망.

## 비용

GPU-fire

## 왜 새로운가 (기존 각도 대비)

H_9359 진단을 **파벌 배정으로 문자 그대로** 구현. H_9267(데이터 크랙)과 아키텍처-vs-데이터 대질. H_9423(공학습 store-bridge)의 구조판.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
