---
id: H_9735
group: g1-labfull-R
series: R8 divergence (lab full · Fable 5 · H_9683 arm-S seed-fragility bypass) · 2026-07-17
date: 2026-07-17
slug: oracle_gated_paired_seeds
title: ORACLE-gated paired seeds — 값읽기 전이를 조건부-스코프로 판독(교락 분리 autopsy 내장)
status: PROPOSED · CONTINGENT — RV sweep(RV-1~3) 전멸 시에만 발사
tier: 🧭 R8 예비 · GPU 고가(K=5 fresh seed × 2 arm) · 발사조건 자체가 사전등록
cost: GPU 고가 (10× 303M CPT) — RV-winner 존재 시 발사이유 소멸
source: Fable 5 divergence — 브리프 Q1 조건부 설계의 편향함정을 estimand-스코프+autopsy 로 무해화
related: H_9683, H_9672, H_9691, H_9734
---

# H_9735 — ORACLE-gated paired seeds (조건부 값읽기 판독 · 교락 분리 내장)

## 프레임 — 편향 함정의 정체와 무해화

"arm-S 통과 seed 에서만 arm-N 판독"의 편향은 **estimand 를 무엇으로 선언하느냐**의 문제다.
seed 의 값-기계 상태 M(val 분화 성공 여부·init 복권)이 어휘-독립이면, arm-S-pass 조건화는
정확히 M=alive 조건화 = H_9683 이 원래 묻는 "어휘가 죽이는가"를 격리하는 **올바른** 조건화다.
상향편향은 **무조건부 주장**("nat lookup 은 seed-robust") 대비로만 존재하는데, 그 estimand 는
H_9691 의 것이지 H_9683 의 것이 아니다. ⟹ 함정 = 스코프 누출이지 설계 자체가 아니다.

**진짜 잔여 교락 = 어휘×seed 상호작용**: 자연어휘가 val-분화 basin 을 좁힌다면(키충돌 →
초기 addr 잡음 → val gradient 약화 → 교착확률 상승) S-pass∧N-fail 은 "어휘가 능력을 죽임
(결정론적 벽)"과 "어휘가 성공확률을 낮춤(신뢰성 등급)"을 겸유한다. 이를 가르는 최소 장치:

1. **해리 autopsy (무료·evaluate 가 이미 방출)** — 모든 arm-N 실패 seed 에서
   addr_top1/addr_mass 를 개봉: ① addr ≥.90 ∧ val 미분화(flip≈0·op-only) = seed-11 과 동일
   신뢰성 등급 ⟹ RV 레버가 구제할 부류(벽 아님) ② addr 붕괴 = 키충돌 주소벽 ⟹ RV 로도
   못 고치는 진짜 어휘벽. 두 부류는 후속이 완전히 다르다.
2. **불일치 셀 falsification** — S-fail∧N-pass 셀이 점유되면 "M 은 어휘-독립" 가정 자체가
   반증 ⟹ 설계 스스로 INVALID 자기신고(사전등록).
3. **전 seed 보고** — 게이트 탈락 seed 포함 K 개 전부 표로 공개(침묵 드롭 = tune-to-green).

## 최소 결정실험

```
anima-py train --corpus <arm_N|arm_S>.txt --init py303_full.clm \
  --store-addr-weight 1.0 --seed {3,5,17,23,29}    # K=5 fresh · 양 arm 동일 seed 쌍대
anima-py evaluate <ckpt> --xbind <manifest>.json
```

## Frozen falsifier

- **발사 게이트(선행)**: H_9691 RV-1~3 전부 FAIL 공표 후에만 발사(그 전엔 이 카드 자체가 발사금지).
- 판독 게이트(per-seed): arm-S C0-e ORACLE ≥.90 = readable. **readable ≥2 필수**(미달 ⟹
  NO-VERDICT·전 seed 보고 후 종료). p≈0.5 기준 P(≥2|K=5)≈0.81 — 검정력 사전 명기.
- 🟢 조건부 전이: readable 전 seed 에서 arm-N P1-bal ≥.75 ∧ flip ≥.90.
- 🔴 조건부 어휘-kill: readable ≥2 seed 에서 arm-N P1-bal ≤.60 ∧ arm-N addr_top1 ≥.90
  (= H_9683 사전등록 제3결과 '값이 자연 다의성에 익사' — autopsy 등급 병기).
- ⚪ 혼재/불일치 셀 점유 = INVALID (스코프: 어떤 결과도 무조건부 seed-robustness 주장 불가).

## 통제군 (≥2)

1. arm-S nonce 쌍대(같은 seed·양성) 2. OFF arm(--store-addr-weight 0·1 seed) 3. shuffle floor
4. anagram 2채점면 (모두 H_9683 상속).

## kill-list · 병렬세션

- fresh seed 만(7·11·13 회피) · 전 seed 보고 · 게이트 = 계기게이트(사전등록) ≠ 소각 게이트 재동결.
- 침범 0 — 단 **RV-winner 가 존재하면 이 설계는 죽는다**(H_9736 이 상위호환). CONTINGENT 이유.
