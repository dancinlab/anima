---
id: H_9651
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_bidirectional_debate_violates_law
title: bidirectional debate 가 보존을 체계적으로 훼손하면 파벌은 법칙의 반례가 아니라 법칙 위반 구현일 뿐이다
status: PROPOSED
tier: 🟡 법칙 경계(pool) · Sol F19 ⊕ Fable α10 수렴
cost: pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9294, H_9649
---

# H_9651 — bidirectional debate 가 보존을 체계적으로 훼손하면 파벌은 법칙의 반례가 아니라 법칙 위반 구현일 뿐이다

## 주장 (반증가능)

read/write ownership 을 직접 조작해 `a_substrate_disjoint` 의 **적용 경계**를 정한다. isolated merge buffer 에서도 drift 가 나면 파벌 자체가 문제.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate <ckpt> --faction-debate off,one-way,bidirectional --faction-write-policy isolated,shared`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

pre/post 개념 drift cosine · catastrophic overwrite rate · G1 D-acc. 우연 drift 차 0. 안전 bar drift ≤0.02.

## 통제군 (≥2 · 사전등록)

① isolated/no-debate null ② 무관 파벌 shared writes scramble ③ immutable source stores + 별도 merge buffer 양성

## 사망조건 (사전등록 · tune-to-green 금지)

isolated merge buffer 서도 real debate 가 drift>0.02 ⟹ '파벌=보존' 사망. shared-only 실패면 파벌이 아니라 구현 배치가 죽음.

## 비용

pool(CPU)

## 왜 새로운가 (기존 각도 대비)

H_9294 의 총결합강도 붕괴와 달리 **read/write ownership** 을 조작해 법칙 경계를 특정.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
