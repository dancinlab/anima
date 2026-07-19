---
id: H_9657
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_threshold_arbitrary_rate_knob
title: consensus_threshold=0.6 은 의미 있는 사건 경계가 아니라 임의 빈도 조절기다
status: PROPOSED
tier: 🟡 tune-to-green 심문($0) · Fable α5 ⊕ Sol F21 수렴
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9627, H_9645
---

# H_9657 — consensus_threshold=0.6 은 의미 있는 사건 경계가 아니라 임의 빈도 조절기다

## 주장 (반증가능)

`MemristorFactionSystem.consensus_threshold: 0.6` 은 코드에 하드코딩됐고 유도 근거가 없다. 성능이 합의의 **내용**이 아니라 event **rate** 만으로 설명되면 0.6 은 손으로 뽑은 정점.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-threshold 0.3:0.9:0.1 --n-factions 4,8,12 --faction-consensus phasic`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

threshold 별 event rate · DV. bar = rate-matched null 대비 Δ CI>0 이어야 semantics 생존.

## 통제군 (≥2 · 사전등록)

① 동일 event rate 의 Poisson pulses(rate-matched null) ② 실제 event timing permutation scramble ③ θ=0(항상합의)/θ=1(합의없음) 양끝

## 사망조건 (사전등록 · tune-to-green 금지)

DV 가 rate 만으로 설명되거나 최적 θ 가 seed/N 마다 불안정 ⟹ 0.6 및 consensus semantics 사망.

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

`valce-minimum-picked-a-collapsed-model`·`burned-gate` 계열 정직성 검사를 파벌 하드코딩에 처음 적용.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
