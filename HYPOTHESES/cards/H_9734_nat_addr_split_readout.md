---
id: H_9734
group: g1-labfull-R
series: R8 divergence (lab full · Fable 5 · H_9683 arm-S seed-fragility bypass) · 2026-07-17
date: 2026-07-17
slug: nat_addr_split_readout
title: NAT-ADDR-SPLIT — H_9683 1차 DV 를 seed-robust 주소축으로 분리해 RV-winner 없이 판독가능화
status: PROPOSED · DIRECTIONAL design only (lab-full divergence)
tier: ⭐ R8 최우선 · pool GPU (기존 산출물 그대로 · fresh 2-seed)
cost: pool GPU (arm-N/arm-S/OFF × 2 seed · 산출물 재빌드 0)
source: Fable 5 divergence — H_9672 해리(주소 2-seed robust ⊥ 값읽기 seed-취약)를 판독축으로 역이용
related: H_9683, H_9672, H_9691
---

# H_9734 — NAT-ADDR-SPLIT (H_9683 을 지금 판독가능하게 만드는 축 분리)

## 프레임

H_9683 의 arm-S(양성통제)는 값읽기(ORACLE/P1) bar 에서 seed-fragile 이다(H_9672: seed7
ORACLE 0.99 vs seed11 0.50). 그러나 같은 fire 의 **주소축은 2-seed robust** 하다 — seed-11
붕괴 속에서도 addr_top1 0.984 · addr_mass 0.962(seed-7 0.948 급). 그리고 H_9683 원 카드가
이미 제3결과를 사전등록해 뒀다: "addr_top1 높고 P1 낮음 = 주소는 섰으나 값읽기 익사".
⟹ **1차 DV 를 주소전이(addr_top1·addr_mass·addr-gap)로 승격**하면 양성통제가 seed-robust
축 위에 서고, H_9683 은 H_9691 RV-winner 를 기다리지 않고 판독가능해진다.

기전 정합성: H_9683 이 겨냥한 자연어휘 교란(byte-bag 위치맹·anagram/부분어 키충돌)은
**주소경로를 먼저 때린다** — 즉 주소축은 대체 판독면이 아니라 사전등록된 기전이 상륙하는
바로 그 면이다. key census(nat 0.9880 ≈ nonce 0.9875)가 byte-공간 분리 동등을 시사하므로
양방향 모두 살아있는(falsifiable) 검정이다: 학습된 W_q 공간에서 충돌이 재출현하면 KILL,
안 하면 전이 🟢.

## 최소 결정실험 (engine-native · 신규코드 0)

```
anima-py train --corpus <arm_N|arm_S>.txt --init py303_full.clm \
  --store-addr-weight 1.0 --seed {3,17}          # + OFF arm: --store-addr-weight 0 (arm-N 어휘)
anima-py evaluate <ckpt> --xbind <manifest>.json  # addr-audit(addr_top1·addr_mass)·addr-gap·P1·ORACLE·flip
```
- seed {3,17} = fresh (7=소각 · 11=취약실증 · **13=H_9691 confirm 예약 — 사용금지**).
- 산출물 5종 바이트-동일 검증 그대로 — 바뀌는 것은 사전등록 판정표뿐(발사 전 재동결 = 합법·burned-gate 아님).

## Frozen falsifier (발사 전 동결)

- **계기 게이트(양성통제·per-seed)**: arm-S addr_top1 ≥.95 ∧ addr_mass ≥.90 — 양 seed 필수
  (donor 실측 0.984/0.948–0.962 아래 여유). 미달 ⟹ INSTRUMENT-DEAD, arm-N 미개봉.
- 🟢 NAT-ADDR 전이: arm-N addr_top1 ≥.90 ∧ addr-gap(SEEN−held, addr_top1 기준) ≤.20 — 양 seed ·
  anagram-충돌 제외면 1차(포함면 병기·H_9683 통제 ④ 상속).
- 🔴 어휘-주소 벽: arm-N addr_top1 ≤.60 양 seed (arm-S 게이트 동일 fire 통과 조건).
- ⚪ 중간대 또는 seed 불일치 = INVALID-underpowered (fresh +1 seed 또는 중단 · 1-seed 읽기 금지).
- 값읽기 지표(ORACLE·P1·flip) = **DIAGNOSTIC-ONLY** 기록. windfall 조항: arm-S 값읽기가
  우연히 2/2 통과하면 H_9683 원 판정표 그대로 보너스 개봉(추가비용 0) — 단 사전등록된
  기대치는 '미통과'다.

## 통제군 (≥2)

1. arm-S nonce (양성 · 주소축 게이트).
2. `--store-addr-weight 0` OFF arm (음성 · Stage1.5 부트스트랩 교착 재현: addr_top1 ≤.60 기대).
3. shuffle floor (H_9683 상속).
4. anagram 제외/포함 2채점면 (H_9683 상속).

## Honest scope · kill-list · 병렬세션

- 주장 축소가 본질: 🟢 이면 "감독-주소 레버의 **주소학습**이 자연어휘에 전이" — 값읽기
  전이는 PENDING(H_9736 rider 로 RV-winner 위에서 회수). a_scale_honest_scope.
- kill-list 저촉 0: seed-7 미사용 · 1-seed 읽기 없음 · RV-sweep 대리발사 없음 · bar 이동은
  발사 전 재동결(소각 전) — H_9372 위반 아님.
- 병렬세션 침범 0: origin/main 배선 레버만 사용 · seed {7,11,13} 회피 · GPU 는 pool 해방 대기
  (a_dont_kill_live_compute).
