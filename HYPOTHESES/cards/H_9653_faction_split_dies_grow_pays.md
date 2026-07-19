---
id: H_9653
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_split_dies_grow_pays
title: 파벌 split 은 죽고 grow 만 낸다 (MITOSIS 법칙의 가로축 이식)
status: PROPOSED
tier: 🟡 MITOSIS 이식(GPU) · Fable α16
cost: GPU
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9313, H_1568, H_9639
---

# H_9653 — 파벌 split 은 죽고 grow 만 낸다 (MITOSIS 법칙의 가로축 이식)

## 주장 (반증가능)

`a_mitosis_train`: growth 🟢, from-scratch split 🔴. H_9313: 분할의 지능 벽 = 추정기 계급. 파벌은 **가로 분할** — 이 법칙이 가로축에도 적용되는가.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py train --n-factions K --faction-mode split,grow` (split=기존용량 쪼갬 · grow=세포 추가 후 신파벌)
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

recomb 또는 Φ. 예측(a_mitosis): split 🔴, grow 🟢.

## 통제군 (≥2 · 사전등록)

① split-mode(H_9313 예측=사망) ② grow-mode ③ 단일파벌 null

## 사망조건 (사전등록 · tune-to-green 금지)

split ≈ grow ⟹ MITOSIS 법칙이 파벌을 못 다스림(파벌은 순수 가로분할·세로 성장 무관).

## 비용

GPU-fire

## 왜 새로운가 (기존 각도 대비)

`mitosis-wall-is-estimator-class`(H_9313)를 파벌축에 이식. 가로분할 × 세로성장 교차.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
