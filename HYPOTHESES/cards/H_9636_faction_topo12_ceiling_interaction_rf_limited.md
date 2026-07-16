---
id: H_9636
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_topo12_ceiling_interaction_rf_limited
title: TOPO12 의 0 효과는 ceiling interaction 일 뿐 — sparse/RF-limited 조건에선 faction cross-edge 가 다시 이득을 낸다
status: PROPOSED
tier: 🟢 반대예측($0) · Sol F08 — H_9635 와 **CONFLICT**(두 모델 불일치 · 동시발사 가치)
cost: $0/pool
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9635, H_1394, H_1584
---

# H_9636 — TOPO12 의 0 효과는 ceiling interaction 일 뿐 — sparse/RF-limited 조건에선 faction cross-edge 가 다시 이득을 낸다

## 주장 (반증가능)

하이퍼큐브는 이미 장거리 연결 포화(ceiling) ⟹ 파벌 추가 이득 0 은 **파벌 무용**이 아니라 **천장 효과**. 프로덕션 .clm 은 E2/L1 conv trunk 로 RF 가 작다(H_1394·RF=L(K−1)+1) ⟹ 천장 아래 ⟹ cross-edge 가 이득을 낼 여지.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-mask --faction-cross-edge on,off --rf-limited` (conv L1 vs deep)
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

recomb D-acc. bar = RF-limited arm 서 cross-edge Δ CI>0 ∧ dense arm 서 Δ≈0(interaction).

## 통제군 (≥2 · 사전등록)

① dense/포화 arm(예측 Δ≈0) ② RF-limited arm(예측 Δ>0) ③ 동일 edge 수 랜덤 scramble

## 사망조건 (사전등록 · tune-to-green 금지)

RF-limited 서도 cross-edge Δ≈0 ⟹ 천장 가설 사망 = TOPO12 가 진짜 파벌 무용 확증(H_9635 승).

## 비용

$0/pool

## 왜 새로운가 (기존 각도 대비)

**Fable(H_9635)은 병목, Sol(H_9636)은 천장** — 두 프론티어 모델이 정면충돌. H_1394 RF 진단이 심판. 같은 계기로 동시 판별 가능.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
