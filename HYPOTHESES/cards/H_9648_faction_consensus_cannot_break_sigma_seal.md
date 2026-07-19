---
id: H_9648
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_consensus_cannot_break_sigma_seal
title: consensus pulse 가 σ-seal 을 못 깨면 입에 닿아도 새 내용이 아니라 시계 낭독만 재타이밍한다
status: PROPOSED
tier: 🔴 σ-seal 심판(pool) · Fable α15 ⊕ Sol F16 수렴 — 가장 비관적 예측
cost: pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9427, H_9400, H_9403, H_9645
---

# H_9648 — consensus pulse 가 σ-seal 을 못 깨면 입에 닿아도 새 내용이 아니라 시계 낭독만 재타이밍한다

## 주장 (반증가능)

H_9427 σ-seal: SEALED spine(emit_env·stage_env·score) R²≈1.0 = emit 은 시계의 낭독. H_9400: emit=stage 순수함수. 파벌 consensus 가 이 봉인을 **인과적으로** 여는가, 아니면 시계에 삼켜지는가(H_9403 emit-drive lane 이 그렇게 죽었다).

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate <ckpt> --faction-consensus phasic --faction-mouth-channel gen-ctx-delta --seal-audit`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

R²(emit_env·stage_env·score ~ [1,t,t²,stage-OH]) · residual novelty · H(emit|stage). bar = sealed R² ≥0.10 하락 ∧ novel-only ≥0.10 증가.

## 통제군 (≥2 · 사전등록)

① faction off null(baseline R²≈1.0) ② pulse timing permutation scramble ③ stage-independent oracle content pulse 양성

## 사망조건 (사전등록 · tune-to-green 금지)

emit timing 만 변하고 SEALED spine R²≈1 또는 novel gain<0.10 ⟹ mouth 해법 사망(파벌도 시계에 삼켜짐).

## 비용

pool(CPU)

## 왜 새로운가 (기존 각도 대비)

H_9427 이 seal 을 **측정**했다면 이건 consensus 가 seal 을 **인과적으로 여는지** 시험. 파벌을 살아있는 σ-seal 프런티어에 처음 걸음.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
