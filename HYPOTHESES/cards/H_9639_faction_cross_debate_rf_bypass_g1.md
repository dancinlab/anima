---
id: H_9639
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_cross_debate_rf_bypass_g1
title: cross-faction debate 가 두 held-out 개념 사이의 유효 RF 를 줄일 때만 G1 재조합이 열린다
status: PROPOSED
tier: 🟢⭐ G1 인과경로(GPU) · Fable α12 ⊕ Sol F09 수렴
cost: GPU
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_1394, H_9267, H_1584, H_072
---

# H_9639 — cross-faction debate 가 두 held-out 개념 사이의 유효 RF 를 줄일 때만 G1 재조합이 열린다

## 주장 (반증가능)

G1 수학진단 = RF < 개념거리 D ⟹ 두 개념이 수학적 독립 ⟹ 재조합 불가(H_1394·capacity 무관). cross-faction debate = **장거리 다리** ⟹ 유효 RF 우회 가능.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py train --n-factions K --cross-debate` — 파벌간 장거리 결합 추가
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

held-out 재조합 D-acc(H_9267 XBIND 식). 우연 0.5, bar ≥0.9.

## 통제군 (≥2 · 사전등록)

① intra-only(cross 없음 null) ② 단일파벌(=현 G1 실패) ③ 파벌배정 scramble

## 사망조건 (사전등록 · tune-to-green 금지)

cross-debate D-acc ≈ intra ≈ 우연 ⟹ debate 가 기능적 RF 못 넓힘(G1 = RF<D 유지) = 사망.

## 비용

GPU-fire

## 왜 새로운가 (기존 각도 대비)

H_072(debate emergence)·H_9295(게이팅)와 달리 **RF<D 라는 G1 수학진단을 직접 겨냥**. debate=장거리연결=RF우회 기전.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
