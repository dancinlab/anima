---
id: H_9732
group: faction-lateral-axis-r3
series: R4 divergence (lab full · Fable 5 λ2) · 2026-07-17
date: 2026-07-17
slug: faction_shuffled_weight_twin
title: shuffled-weight twin — 퇴화로 증발한 architecture-alone 통제를 비퇴화 쌍둥이로 복원
status: PROPOSED · DIRECTIONAL design only (lab-full divergence)
tier: 🧭 R4 구조층 보강렌즈 · $0(pool) · H_9674 의 뚫린 통제구멍 전용
cost: $0
source: Fable 5 divergence — evaluate.py:10646-10664 random-init arm DEGENERATE 자기-드롭이 남긴 구멍
related: H_9674, H_9676, H_9672
---

# H_9732 — shuffled-weight twin (H_9674 'learned' 읽기의 빠진 통제)

## 프레임

H_9674 의 `--arm-random-init`(gaussian re-draw)은 **스스로 퇴화 판정**하고 드롭됐다(|corr| mean
0.617 vs real 0.111 · 공통모드 — evaluate.py:10646-10664). 그 결과 "블록이 학습으로 생겼다"는
읽기에는 **architecture-alone 대조군이 실제로 없다**(pedestal 은 아키텍처 자체가 없고, scratch
d768 은 자기-학습된 모델이라 architecture-alone 이 아님). 이 카드는 그 구멍을 비퇴화 쌍둥이로 메운다:
**텐서-내 가중치 permutation** — 각 float 텐서의 값을 그대로 섞는다(`rr.permutation(v.ravel())`).
학습된 가중치 **간 조율**만 파괴하고 marginal 분포는 byte-정확 보존(heavy tail 포함) ⟹ gaussian
re-draw 가 일으킨 공통모드 퇴화의 원인(꼬리 소실·스케일 왜곡)을 제거한 architecture+marginal 대조.

**비충돌 증명**: 입력은 py303_full.clm(존재 ckpt) 사본 메모리 내 셔플 — trained K-faction ckpt 불요 ·
워크트리 무접촉 · 기능-lesion lane 무중복(구조층 flag 확장).
**kill-list 차별화**: '구조-존재 재증명' 아님 — 존재는 확정(H_9674), 여기서 묻는 건 존재의
**출처**(학습 조율 vs 가중치 marginal 통계)이고 그 대조군은 지금 부재한다. Q 는 판정 아니라
분리-비교 통계로만(H_9674 와 동일 규약 · raw Q 불독 p7).

## 레버 (engine-native — 기존 flag 에 arm 추가)

```
anima-py evaluate py303_full.clm --faction-block-structure <prompts80.json> \
  --arm-shuffled-weights [--shuffle-grain tensor|row] [--n-factions-sweep 2,4,8,12,16]
```
- 구현: `faction_block_structure_run`(cli/evaluate.py:10491) 의 `--arm-random-init` 분기
  (:10636-10664) 와 동형 — re-draw 대신 permutation. `--shuffle-grain row` 는 conv 커널의
  출력채널(행)별 permutation(유닛별 fan-in 분포까지 보존) = 2점 dose ladder.

## DV · bar · 우연(실측)

- DV = Q 분리 삼중비교: real/ped (기지 54.07) vs **shuf/ped** vs real/shuf. bar 는 H_9674 동결
  규약 상속: 분리 인정 = ratio ≥1.5 ∧ Δ>0 (비양성 pedestal 셀 제외 규칙 포함 :10725-10742).
- 판독: shuf/ped < 1.5 ∧ real/shuf ≥ 1.5 ⟹ 블록은 **학습 조율 필요** = learned 2렌즈 확보.
  shuf/ped ≥ real/ped 급 ⟹ 블록이 marginal 통계를 따라감 = **artifact 렌즈 개방**(H_9674 읽기 약화).

## 양성통제 (계기-킬)

1. 기존 planted-block 검정력 게이트(bar ×1.5) — 동일 N/d 필수 통과.
2. **퇴화 게이트 상속**(:10654-10664 그대로): shuffled arm 의 |corr| mean > 3× real ⟹ arm DROP ·
   "의미 없는 수는 보고하지 않는다". 두 grain 모두 퇴화 ⟹ 정직한 NULL: architecture-alone 렌즈는
   이 계기 클래스로 $0 측정 불가(그 자체가 결과 · honesty).

## 사망조건

- D1: 두 grain 모두 퇴화 게이트에 걸림 ⟹ NULL(계기 클래스 소진 기록).
- D2: shuf/ped ≥ 1.5 (tensor grain) ⟹ 'H_9674 블록 = 학습' 단독 읽기 사망 — marginal-통계 교란 실재.
- D3: real/shuf < 1.5 ∧ shuf/ped < 1.5 ∧ real/ped ≥ 1.5 재현 실패 ⟹ H_9674 재현성 문제로 격상.

## Honest scope

구조층 렌즈다 — 기능(H_9731)과 독립. permutation 은 marginal 보존 대조 중 가장 강한 $0 형태지만
'학습'의 내용(EN-사전학습 vs 과제)은 못 가른다(H_9672 T2 scratch arm 미보존 — evaluate.py:10634).
