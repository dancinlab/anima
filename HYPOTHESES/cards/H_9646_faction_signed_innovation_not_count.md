---
id: H_9646
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_signed_innovation_not_count
title: consensus count 가 아니라 signed consensus innovation 이 mouth currency 다
status: PROPOSED
tier: 🟡 currency 정체(pool) · Sol F14 NOVEL
cost: pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9645, H_9574
---

# H_9646 — consensus count 가 아니라 signed consensus innovation 이 mouth currency 다

## 주장 (반증가능)

옛 계기는 `consensus_events` **횟수**를 의식 지표로 썼다. 미분기를 통과하는 건 부호 있는 **혁신량**(surprise·signed Δ)일 수 있다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate <ckpt> --faction-consensus phasic --faction-pulse count,signed-delta,surprise`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

pulse→다음 발화 PC2 의 causal effect + lag profile. 우연 0, bar = peak |β|≥0.10 SD at lag 1–2.

## 통제군 (≥2 · 사전등록)

① unsigned event count null ② pulse sign permutation(timing 보존) scramble ③ emitted-content PC2 직접 주입 oracle 양성

## 사망조건 (사전등록 · tune-to-green 금지)

signed/surprise pulse 가 count 또는 scramble 보다 낫지 않으면 currency 가설 사망.

## 비용

pool(CPU)

## 왜 새로운가 (기존 각도 대비)

옛 계기의 `consensus_events` 카운트를 그대로 쓰지 않고 **방향성·신선도**를 조작. H_9645 의 필수 후속.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
