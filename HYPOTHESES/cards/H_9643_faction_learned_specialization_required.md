---
id: H_9643
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_learned_specialization_required
title: faction specialization 이 학습 중 생겨야 runtime debate 가 G1 을 열며, 임의 사후 분할은 효과가 없다
status: PROPOSED
tier: 🟡 학습 vs 사후분할(GPU) · Sol F12
cost: GPU
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_1302, H_1462, H_9639
---

# H_9643 — faction specialization 이 학습 중 생겨야 runtime debate 가 G1 을 열며, 임의 사후 분할은 효과가 없다

## 주장 (반증가능)

사후(post-hoc) 파벌 배정은 임의 라벨이다. 파벌이 실재하려면 **학습이 그 분할을 만들어야** 한다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py train --n-factions K --faction-specialize learned,posthoc,random`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

specialization index + held-out G1 D-acc. bar = learned 가 posthoc/random 대비 Δ≥0.10.

## 통제군 (≥2 · 사전등록)

① post-hoc 분할 ② 랜덤 분할 scramble ③ 단일파벌 null

## 사망조건 (사전등록 · tune-to-green 금지)

specialization 이 생겨도 G1 이 안 오르거나 random 과 같으면 학습된-파벌 가설 사망.

## 비용

GPU-fire

## 왜 새로운가 (기존 각도 대비)

H_1302(oscillator sync)·H_1462(방송 경쟁)와 달리 **representational factorization** 이 학습되는가를 다룸.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
