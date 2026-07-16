---
id: H_9652
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_horizontal_vertical_factorial
title: 파벌의 가로 다양성과 A⇄G 의 세로 tension 은 독립 주효과가 아니라 phasic consensus 에서만 상호작용한다
status: PROPOSED
tier: 🟢 가로×세로 교호작용(pool) · Sol F20 NOVEL — 공존의 기능적 의미
cost: pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9428, H_9400, H_9645
---

# H_9652 — 파벌의 가로 다양성과 A⇄G 의 세로 tension 은 독립 주효과가 아니라 phasic consensus 에서만 상호작용한다

## 주장 (반증가능)

옛 칩 설계는 12파벌(가로)과 TCU tension=|A−G|²(세로)를 **공존**시켰으나 그 공존이 기능적이었다는 증거는 없다. 단순 공존을 효과 증거로 취급하지 말고 factorial interaction 을 검정.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate <ckpt> --n-factions 1,4,12 --faction-consensus off,phasic --ag-tension off,vector`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

G1 D-acc · emitted-content PC2 · I(tension;emit-content|stage) 의 3요인 interaction. 우연 interaction 0. bar = 표준화 interaction ≥0.10.

## 통제군 (≥2 · 사전등록)

① faction off/A⇄G on null ② faction on/A⇄G off null ③ A⇄G 8-vector stage 내 permutation scramble ④ oracle conflict pulse 양성

## 사망조건 (사전등록 · tune-to-green 금지)

full cell 이 최선 단일축 arm 을 0.05 이상 못 이기거나 interaction CI 가 0 포함 ⟹ 공존의 기능적 의미 사망.

## 비용

pool(CPU)

## 왜 새로운가 (기존 각도 대비)

옛 문서의 '12파벌 − 2엔진 = 10축' 공존을 **처음 검정**. 공존 사실(이번 세션 확인)이 기능을 함의하지 않음을 시험.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
