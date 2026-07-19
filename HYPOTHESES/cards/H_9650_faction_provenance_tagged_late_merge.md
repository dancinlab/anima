---
id: H_9650
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_provenance_tagged_late_merge
title: cross-debate 가 source provenance 를 유지하면 중첩 없이 재조합할 수 있어 disjoint 법칙의 확장형이 된다
status: PROPOSED
tier: 🟢 법칙 확장형(pool) · Sol F18 NOVEL — 가장 건설적 각도
cost: pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_1764, H_9294, H_9267
---

# H_9650 — cross-debate 가 source provenance 를 유지하면 중첩 없이 재조합할 수 있어 disjoint 법칙의 확장형이 된다

## 주장 (반증가능)

`a_substrate_disjoint` 의 '중첩=충돌' 은 **메시지를 합칠 때** 성립한다. source identity 를 끝까지 태그로 보존하고 **late merge** 하면 충돌 없이 재조합할 여지 — 법칙의 반례가 아니라 확장.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate <ckpt> --xbind <manifest> --faction-message tagged,untagged --faction-merge late,early`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

D-acc · source-attribution accuracy · interference rate. 우연 attribution=1/N. bar = tagged-late 가 untagged-early 대비 D-acc ≥0.10 ∧ attribution ≥0.80.

## 통제군 (≥2 · 사전등록)

① untagged early averaging null ② provenance tag 만 permutation scramble ③ oracle source tags + oracle late selector 양성

## 사망조건 (사전등록 · tune-to-green 금지)

provenance tag 가 attribution/D-acc 를 못 높이거나 late merge 도 충돌을 못 줄이면 확장형 사망.

## 비용

pool(CPU)

## 왜 새로운가 (기존 각도 대비)

H_1764(Coalition Blackboard 공유작업공간)와 달리 **합치지 않는 typed transport**. `a_substrate_disjoint` 를 깨지 않고 재조합하는 유일 설계.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
