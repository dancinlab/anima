---
id: H_9638
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_optimum_is_measured_rank_not_12
title: 최적 파벌 수 = emit-직교 다양체의 측정된 유효 rank(≈2.66)이지 8/12 가 아니다
status: PROPOSED
tier: 🟡 숫자 재정박($0) · Fable α6
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9428, H_9628, H_067
---

# H_9638 — 최적 파벌 수 = emit-직교 다양체의 측정된 유효 rank(≈2.66)이지 8/12 가 아니다

## 주장 (반증가능)

옛 8/12 는 폐엔진 + 수론 미학(σ(6)=12)에서 나왔다. 현 기질의 측정된 rank 는 2.66(H_9428). 진짜 최적이 있다면 그 rank 근처여야 한다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-optimum --n-factions-sweep 1,2,3,4,8,12,16`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

argmax_K DV. 예측: 옛법칙=8/12 · 측정 rank=2~3.

## 통제군 (≥2 · 사전등록)

① null(정점 없음) ② rank-8 합성 양성(8서 정점 나와야 계기 유효)

## 사망조건 (사전등록 · tune-to-green 금지)

정점이 8/12 면 옛법칙 이식(이 가설 사망). ~3 이면 옛 숫자는 폐엔진 rank 유물.

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

파벌 카운트를 **측정된 다양체 rank** 에 처음 묶음. H_9628(정점 미측정)의 후속 — 정점이 존재한다면 어디인가.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
