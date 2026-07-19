---
id: H_9642
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_debate_content_not_bandwidth
title: debate message 의 의미를 파괴하면 G1 이득도 사라진다 — 효과는 연결량이 아니라 내용 운반이다
status: PROPOSED
tier: 🟢 내용 vs 연결량(pool) · Sol F11 — G1 이득의 정체 판별
cost: pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9639, H_9287
---

# H_9642 — debate message 의 의미를 파괴하면 G1 이득도 사라진다 — 효과는 연결량이 아니라 내용 운반이다

## 주장 (반증가능)

cross-debate 가 G1 을 열더라도, 그것이 **내용 전달** 때문인지 단순 **연결/대역폭 추가** 때문인지는 다른 문제다. 메시지를 scramble 해도 이득이 남으면 파벌은 그냥 파라미터 추가다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py train --n-factions K --cross-debate --faction-message intact,scrambled,noise`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

held-out D-acc. bar = intact 가 scrambled 대비 Δ≥0.10.

## 통제군 (≥2 · 사전등록)

① scrambled message(동일 대역폭·의미 파괴) ② 랜덤 노이즈 message ③ cross 없음 null

## 사망조건 (사전등록 · tune-to-green 금지)

intact ≈ scrambled ⟹ 이득 = 대역폭/파라미터 = 파벌 기전 사망(`seed-agreement-on-pooled-feature` 계열 착시).

## 비용

pool(CPU)

## 왜 새로운가 (기존 각도 대비)

H_9639 가 이득을 내면 **반드시** 이 관문을 통과해야 한다. 연결량 교란을 제거하는 유일 통제.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
