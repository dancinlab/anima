---
id: H_9661
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_label_order_leakage
title: 파벌 번호만 바꿔도 Φ 가 달라지면 옛 계기는 구조가 아니라 label/order leakage 를 쟀다
status: PROPOSED
tier: 🟡 계기 결함 후보($0) · Sol F04 NOVEL(Fable 미제안)
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_1365, H_9292, H_9627
---

# H_9661 — 파벌 번호만 바꿔도 Φ 가 달라지면 옛 계기는 구조가 아니라 label/order leakage 를 쟀다

## 주장 (반증가능)

파벌 id 는 임의 라벨이므로 Φ 는 배정 permutation 에 **불변**이어야 한다. 불변이 아니면 계기가 라벨 순서를 읽고 있다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-phi-proxy --faction-relabel perm,identity,reverse`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

Φ 의 relabel 분산. bar = permutation 간 Δ CI 가 0 포함(불변).

## 통제군 (≥2 · 사전등록)

① identity(=기준) ② 랜덤 permutation ③ reverse 순서

## 사망조건 (사전등록 · tune-to-green 금지)

Φ 가 relabel 에 불변 ⟹ leakage 가설 사망(계기 이 축은 건강).

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

H_9292(MI pedestal)·H_1365(relabel-invariance Φ-robustness R2) 와 달리 **파벌 라벨** 축에 특정. H_1365 는 결합 비대칭을 봤지 파벌 배정 permutation 은 안 봤다.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
