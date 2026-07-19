---
id: H_9649
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_disjoint_conditional_confirmation
title: 토론 없는 분리는 보존을 높이지만 cross-debate 는 충돌을 재도입한다 — 파벌은 disjoint 법칙의 조건부 확증이다
status: PROPOSED
tier: 🟡 법칙 2요인 분해(pool) · Sol F17
cost: pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9294, H_9295
---

# H_9649 — 토론 없는 분리는 보존을 높이지만 cross-debate 는 충돌을 재도입한다 — 파벌은 disjoint 법칙의 조건부 확증이다

## 주장 (반증가능)

`a_substrate_disjoint` = 분리=보존, 중첩=충돌. 파벌 = 분리(intra) + 중첩(cross) **동시**. 법칙을 인용만 하지 말고 `separation × communication` 2요인으로 분해해 각 항의 부호를 잰다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate <ckpt> --n-factions 4 --faction-debate off,read-only,bidirectional`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

원 개념 readback · interference error · held-out D-acc. bar = 분리로 readback ≥0.05 개선 ∧ debate 로 D-acc ≥0.10 개선하되 readback 손실 ≤0.02.

## 통제군 (≥2 · 사전등록)

① 미분할 공유 기질 null ② 무관 메시지 bidirectional debate scramble ③ read-only oracle merger 양성

## 사망조건 (사전등록 · tune-to-green 금지)

분리 자체가 보존을 못 높이면 확증 사망. real debate 가 scramble 만큼 보존을 훼손하면 파벌 전체가 disjoint 해법으로 사망.

## 비용

pool(CPU)

## 왜 새로운가 (기존 각도 대비)

H_9294(disjointness→총결합강도 붕괴)를 **2요인 설계**로 재프레임. 법칙 인용이 아니라 법칙 시험.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
