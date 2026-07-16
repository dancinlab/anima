---
id: H_9637
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_adds_no_manifold_rank
title: 파벌 분할은 활성 다양체의 유효 rank 를 더하지 않는다 (A⇄G 1비트 접힘을 못 푼다)
status: 💀 DV-MALFORMED — Δrank 는 분할에 대해 정의상 불변(항등식) · well-posed 재정식 = H_9674 로 이관
tier: 🟡 DOF 부재($0) · Fable α7
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9428, H_9295, H_9574
---

# H_9637 — 파벌 분할은 활성 다양체의 유효 rank 를 더하지 않는다 (A⇄G 1비트 접힘을 못 푼다)

## 주장 (반증가능)

mouth-severance 프레임: tension 은 이미 8-벡터인데 1비트로 접힌다(H_9428 rank 2.66). 파벌이 새 DOF 를 준다면 rank 가 올라야 한다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-rank-probe --n-factions K` — frozen 활성 PCA effective rank
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

Δrank(파벌 유/무). bar = null 위 CI 밖.


## ⚠️ 사전등록 DV 결함 (2026-07-17 · 자가감사)

이 카드의 DV `Δrank(파벌 유/무)` 는 **ill-posed** 다. 파벌 분할은 활성 행렬 X:[N,d] 의 **라벨링**일 뿐
값을 바꾸지 않으므로 PCA effective rank 가 **정의상 불변**이다(Δrank ≡ 0 이 보장됨 — 측정이 아니라 항등식).

DV 를 바꿔 살리는 것은 tune-to-green 이므로 하지 않는다. 대신 이 카드가 **묻고 싶었던** 질문
("파벌이 새 DOF 를 주는가")을 well-posed 로 다시 세운 것이 **H_9674**(기질에 블록 구조가 있는가)다.
⟹ 이 카드는 💀 **DV-MALFORMED** 로 종결하고 H_9674 로 이관한다.

## 통제군 (≥2 · 사전등록)

① 셔플 파벌배정 scramble ② 단일파벌 null

## 사망조건 (사전등록 · tune-to-green 금지)

Δrank CI 가 0 포함 ⟹ 파벌은 새 DOF 없음 = mouth 출구 아님.

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

H_9295(게이팅=구조채널 못엶)와 달리 **표현 rank** 자체를 잼. H_9428 rank 2.66 측정치와 직접 대질.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
