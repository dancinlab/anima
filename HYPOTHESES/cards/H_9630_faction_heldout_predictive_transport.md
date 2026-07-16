---
id: H_9630
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_heldout_predictive_transport
title: 법칙 22 가 진짜면 Φ 가 아닌 held-out 예측량에서도 같은 partition 이 무작위 partition 을 이긴다
status: PROPOSED
tier: 🟢 축 생존조건($0) · Sol F05 — 유일한 '진짜면 통과' 관문
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9627, H_9628
---

# H_9630 — 법칙 22 가 진짜면 Φ 가 아닌 held-out 예측량에서도 같은 partition 이 무작위 partition 을 이긴다

## 주장 (반증가능)

Φ-proxy 는 오염됐으나(H_9627), 파벌 분할이 **진짜 구조**를 잡았다면 Φ 밖의 독립 DV(held-out 예측)에서도 그 분할이 랜덤 분할을 이겨야 한다. 계기를 갈아끼워도 살아남는가.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-partition learned,random --faction-dv heldout-ce`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

held-out CE(또는 D-acc). bar = learned partition 이 random 대비 Δ CI>0.

## 통제군 (≥2 · 사전등록)

① 랜덤 분할 scramble(동일 K·동일 크기) ② 단일 파벌 null ③ oracle 분할 양성

## 사망조건 (사전등록 · tune-to-green 금지)

learned ≈ random ⟹ 파벌 분할은 Φ 산수 밖에서 아무것도 아님 = **축 사망**.

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

H_9627/9628 이 계기를 죽여도 이 관문 하나가 축을 살릴 수 있다. Φ 를 버리고 재는 첫 각도.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
