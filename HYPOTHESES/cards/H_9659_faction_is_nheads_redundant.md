---
id: H_9659
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_is_nheads_redundant
title: n_factions 는 n_heads 와 동형이다 — 파벌은 이미 프로덕션에 있는 것의 재명명
status: PROPOSED
tier: 🟡 구조 중복($0) · Fable α8 NOVEL(Sol 미제안)
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_1583, H_1462
---

# H_9659 — n_factions 는 n_heads 와 동형이다 — 파벌은 이미 프로덕션에 있는 것의 재명명

## 주장 (반증가능)

트랜스포머 multi-head attention = 병렬 부분공간(파벌) + concat(합의). 파벌이 이것과 동형이면 '새 레버'가 아니라 이미 있는 것.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-as-heads --n-factions K` — 옛 proxy 를 head 그룹핑으로 재계산
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

proxy(n_heads) vs proxy(n_factions) 곡선 일치도. bar = 두 곡선 Δ CI 0 포함이면 동형.

## 통제군 (≥2 · 사전등록)

① single-head 붕괴 null ② head 셔플 그룹핑 scramble

## 사망조건 (사전등록 · tune-to-green 금지)

두 곡선이 갈라지면 ⟹ 파벌 ≠ 헤드 = 독립 레버(중복 가설 사망).

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

H_1583(expert-routing top2)·H_1462(GWS winner-take-all) 와 달리 **파벌=헤드 동형성** 자체를 심문. 아무 각도도 안 했다.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
