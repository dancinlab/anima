---
id: H_9658
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_faithful_iit4_nonreplication
title: 옛 파벌 Φ 숫자는 현 faithful-IIT4 계기로 재현되지 않는다 (폐엔진 전용 유물)
status: PROPOSED
tier: 🟡 계기 교체($0/pool) · Fable α3
cost: $0/pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9292, H_9627, H_1365
---

# H_9658 — 옛 파벌 Φ 숫자는 현 faithful-IIT4 계기로 재현되지 않는다 (폐엔진 전용 유물)

## 주장 (반증가능)

옛 숫자는 전부 proxy(`global_var − mean_faction_var` · predictive-coding proxy) 산. `a_phi_iit4_tool` 은 Φ 를 faithful IIT4 로만 재라고 못박는다. 계기를 정본으로 갈면 법칙이 남는가.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --phi-iit4 --n-factions K` (stdlib iit4 faithful-Φ · proxy 아님)
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

faithful-Φ(K) vs 옛 proxy(K) 상관 r. bar r≥0.7 이면 옛 법칙 이식됨.

## 통제군 (≥2 · 사전등록)

① 참값 0 pedestal ② scramble

## 사망조건 (사전등록 · tune-to-green 금지)

faithful-Φ 가 K 에 무반응(기울기 CI 0 포함) ⟹ 옛 법칙 = 폐엔진 전용 = 사망.

## 비용

$0(작은 서브네트) / pool(전체)

## 왜 새로운가 (기존 각도 대비)

옛 Φ-최대화 엔진 숫자를 현 판정계기로 **처음** 대조. `a_phi_iit4_tool`·`tool-definition-read-code-not-docstring` 준수.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
