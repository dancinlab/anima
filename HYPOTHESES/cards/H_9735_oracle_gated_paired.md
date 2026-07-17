---
id: H_9735
title: ORACLE-gated PAIRED-SEED — conditional value-reading, bias-trap neutralized (CONTINGENT on RV death)
tier: PROPOSED (R8 · lab full Fable+Sol 수렴 · CONTINGENT: RV 전멸 후에만 발사 · DIRECTIONAL design)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9735 (R8·P3) — 조건부 값읽기 (편향함정 무해화 · RV 전멸 시에만)

**Origin.** `sidecar lab full` 2026-07-17 — Fable(H_9735) + Sol(FULL-CELL PAIRED-SEED) 수렴.
내(origin)가 제안한 seed-pairing 우회를 두 모델이 **편향함정 명시 + 무해화 장치**로 정식화. DESIGN ONLY.

**Claim (one line).** "값-기계가 살아난 seed 에서 자연어휘가 값을 죽이는가"라는 **조건부 estimand** 만
측정한다 — 무조건부 seed-robustness 는 주장하지 않는다.

## 🕳️ 편향함정의 정체 (양 모델 독립 지목)
```
E[Y_N | Y_S pass] ≠ E[Y_N]
```
arm-S 통과 조건화 = 공통 seed-quality 높은 표본만 남김 = 상향편향. **seed-pairing 만으로는 안 사라진다**
(pairing 은 분산·공통고장만 줄임). 단 이 편향은 **"nat lookup 은 seed-robust"라는 무조건부 주장 대비로만**
존재 — 그건 [[H_9691]] 의 estimand 이지 이 카드의 것이 아니다. **조건부 결과에서 무조건부 문장을 쓰는
순간만** 편향이 생긴다.

## 무해화 3장치 (사전등록 · 진짜 잔여 교락 = 어휘×seed 상호작용을 가름)
1. **해리 autopsy ($0 · evaluate 가 이미 방출)** — arm-N 실패 seed 에서 addr_top1/addr_mass 개봉:
   addr 생존 ∧ val 미분화 = seed-11 과 같은 **신뢰성 등급**(RV 레버가 구제할 부류) vs addr 붕괴 =
   **RV 로도 못 고치는 진짜 어휘벽**. 후속이 완전히 다르다.
2. **불일치 셀 falsification** — `S−N+` 셀이 점유되면 "값-기계 상태 M 은 어휘-독립" 가정 자체가 반증
   ⟹ 설계가 스스로 **INVALID 자기신고**.
3. **전 seed 공개보고** — 게이트 탈락 seed 침묵 드롭 = tune-to-green ⟹ K개 전부 표로
   ([[polarity-split-before-headline]] 동형).

## Minimal decisive experiment (⚠️ CONTINGENT — RV-1~3 전멸 공표 후에만)
fresh **K=5 {3,5,17,23,29}** N/S 쌍대 = **10× 303M CPT**. 각 ckpt 에 lookup·oracle·flip·shuffle·addr-audit.
추가학습 없이 **N-ckpt ↔ S-manifest 교차평가**(train-basin 효과 vs eval-key 효과 분리).
4셀 `S+N+ · S+N− · S−N+ · S−N−` **모두 공개**.

## Frozen falsifier (사전등록)
- readable = `arm-S ORACLE ≥ .90`; **readable ≥ 2 없으면 종료**.
- **조건부 생존**: 모든 readable seed 서 arm-N `P1-bal ≥ .75 ∧ flip ≥ .90`.
- **조건부 kill**: readable ≥ 2 서 arm-N `P1-bal ≤ .60 ∧ addr_top1 ≥ .90`(주소는 섰으나 값 익사).
- `S−N+` 발생 or 결과 혼재 = M-어휘독립 가정 반증 ⟹ 단순 조건부 해석 중단.

## Controls · Cost · kill-list
통제 ① paired arm-S ② OFF ③ shuffle floor ④ flip ⑤ N/S manifest 교차평가. corpus $0 · GPU **10+ CPT
(가장 비쌈)**. K=5 서 readable≥2 확률 ≈0.81(p=.5 가정)이나 효과확률 정밀추정 검정력은 아님.
⚠️ **CONTINGENT 게이트 필수**: RV winner 존재 시 발사이유 소멸([[H_9736]] 이 더 쌈) — RV-1~3 전멸
공표 후에만. Kill-list: 전 seed 공개 ∧ fresh seed 면 저촉 없음. **"nat lookup seed-robust"로 서술 =
즉시 저촉**(estimand 누출).
