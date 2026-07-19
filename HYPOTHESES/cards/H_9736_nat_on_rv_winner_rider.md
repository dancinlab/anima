---
id: H_9736
group: g1-labfull-R
series: R8 divergence (lab full · Fable 5 · H_9683 arm-S seed-fragility bypass) · 2026-07-17
date: 2026-07-17
slug: nat_on_rv_winner_rider
title: NAT-on-RV-winner rider — H_9691 winner 레시피 위에 어휘 1-DOF 를 얹어 값읽기 전이 회수
status: PROPOSED · DEPENDENT — H_9691(또는 RV-2/3) winner 착륙이 선행조건
tier: 🤝 R8 협업형(침범 0) · 지금 $0 · winner 후 pool GPU
cost: $0 (등록·대기) → winner 후 pool GPU (arm-N/arm-S × fresh 2-seed)
source: Fable 5 divergence — 브리프 Q3 "합쳐 쏘기"의 침범 없는 형태 = in-flight sweep 합류가 아니라 winner-후 rider
related: H_9691, H_9683, H_9672, H_9734
---

# H_9736 — NAT-on-RV-winner rider (순서가 강제되는 유일한 조각을 가장 싸게 회수)

## 프레임

순서는 **부분적으로만** 강제된다: 주소축 전이는 지금 판독가능(H_9734)하지만, **무조건부
값읽기 전이**는 seed-robust 한 값-레시피 없이는 어떤 설계로도 벌 수 없다(H_9735 도 조건부
스코프까지만). 그 레시피를 만드는 것이 정확히 H_9691 의 lane 이다. ⟹ in-flight RV-sweep 에
어휘 인자를 지금 합류시키는 것은 ① 침범(a_parallel_session_compare) ② 그들 게이트의 1-DOF
오염(어휘 추가 = sweep 비용 2× + 실패 시 원인 귀속 불능)으로 **죽은 형태**고, 살아있는 협업
형태는 **winner-후 rider**: RV-winner 가 {7,11}+confirm13 게이트를 통과해 값읽기 레시피가
seed-robust 로 공표되면, 그 레시피 위에서 arm-N(자연어휘) vs arm-S(nonce)를 어휘 1-DOF 로
재발사 — arm-S 양성통제가 구조적으로 seed-robust 가 되어 H_9683 원 판정표가 무조건부로
개봉된다.

## 최소 결정실험 (winner 착륙 후)

```
anima-py train --corpus <arm_N|arm_S>.txt --init py303_full.clm \
  <winner 플래그: 예 --store-addr-weight 1.0 --store-oracle-aux w_orc> --seed {3,17}
anima-py evaluate <ckpt> --xbind <manifest>.json
```
- seed = fresh {3,17}: winner 선발에 {7,11,13}이 소비되므로 rider 는 그 표면을 재동결하지
  않는다(사전등록 · burned-gate 회피).

## Frozen falsifier

- 계기 게이트: arm-S 가 winner 게이트 표(ORACLE ≥.90 ∧ P1-bal ≥.75 ∧ addr-gap ≤.20 ∧
  flip ≥.90)를 fresh 양 seed 서 재현 — 미달 ⟹ winner 자체의 seed-robustness 재현실패로
  H_9691 lane 에 역보고(발견이지 실패 아님).
- 🟢 값읽기 전이: arm-N 이 동일 표를 양 seed 통과 (anagram-제외면 1차).
- 🔴 어휘-값 벽: arm-S 통과 ∧ arm-N P1-bal ≤.60 양 seed — autopsy(addr vs val)로 등급 병기.
- ⚪ 그 외 = INVALID-underpowered.

## 통제군 (≥2)

1. arm-S nonce on winner(양성) 2. winner-플래그 OFF arm(음성·레버귀속) 3. shuffle floor
4. anagram 2채점면.

## kill-list · 병렬세션

- 침범 0 의 형태 정의가 이 카드의 본질: **그들 sweep·카드·seed 표면 무접촉** — 등록+related
  링크만. winner 공표는 그들의 착륙물을 읽어서(read-only) 트리거.
- RV 전멸 시 이 카드는 발사불능 → H_9735 로 후퇴(상호배타 사전등록).
