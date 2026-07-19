---
id: H_9641
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_factorized_context_not_partition
title: 파벌의 효능은 '분할' 이 아니라 서로 다른 개념을 동시에 보존하는 factorized context 에서 나온다
status: PROPOSED
tier: 🟡 기전 재지정(pool) · Sol F10
cost: pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_1764, H_9639
---

# H_9641 — 파벌의 효능은 '분할' 이 아니라 서로 다른 개념을 동시에 보존하는 factorized context 에서 나온다

## 주장 (반증가능)

분할 자체가 아니라, 두 개념이 서로를 덮어쓰지 않고 **동시에 살아있는 문맥**이 이득의 정체일 수 있다. 그렇다면 파벌은 factorization 의 한 구현일 뿐 본질이 아니다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-mode runtime --faction-context factorized,shared`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

두 개념 동시 readback + held-out D-acc. bar = factorized 가 shared 대비 Δ≥0.10.

## 통제군 (≥2 · 사전등록)

① shared context null ② 랜덤 factorization scramble ③ oracle factorized 양성

## 사망조건 (사전등록 · tune-to-green 금지)

factorized ≈ shared ⟹ 기전 재지정 실패(분할이 본질).

## 비용

pool(CPU)

## 왜 새로운가 (기존 각도 대비)

H_1764(Coalition Blackboard 공유작업공간)와 반대 방향 — 합치지 않는 것이 이득인가.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
