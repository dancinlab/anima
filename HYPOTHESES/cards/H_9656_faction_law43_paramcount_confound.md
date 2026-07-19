---
id: H_9656
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_law43_paramcount_confound
title: 법칙 43 '단순 > 복잡' 은 파벌 효능이 아니라 parameter-count 또는 smoothing 차이다
status: PROPOSED
tier: 🟡 교란 심문($0) · Sol F06
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9627, H_9294
---

# H_9656 — 법칙 43 '단순 > 복잡' 은 파벌 효능이 아니라 parameter-count 또는 smoothing 차이다

## 주장 (반증가능)

법칙 43 근거 = base+8-faction(×125) > ALL combined(×117). 두 arm 은 파벌 수만 다른 게 아니라 **기능 개수·파라미터·평활화가 전부 다르다**. 매개 공변량 미통제.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-phi-proxy --match-params --faction-features base,all`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

파라미터 수를 맞춘 뒤의 Δ. bar = param-matched Δ CI>0 이어야 법칙 43 생존.

## 통제군 (≥2 · 사전등록)

① param-matched base ② param-matched all ③ 파벌 없는 동일 param null

## 사망조건 (사전등록 · tune-to-green 금지)

param 을 맞추면 Δ 소멸 ⟹ 법칙 43 = 용량 교란(`control-must-match-mediating-covariate` 재판).

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

`control-must-match-mediating-covariate` 법칙을 파벌축에 처음 적용. 옛 문헌은 명목 arm 만 비교했다.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
