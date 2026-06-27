---
id: H_1812
slug: reg_dictaux_objective
tier: PRE-REG
title: 정규화 band(grok) + dictionary-aux objective — G1/G6 trunk-objective 레버 (N6+N7)
verdict: PRE-REG (launch-ready · $0 smoke GREEN · 303M GPU 미실행)
status: PRE-REG
wired: launch-ready (303M 미실행)
verdict_artifact:
source: UNIVERSE
archived: false
---

# H_1812 정규화 band + dictionary-aux objective (N6+N7)

## 가설
우승 trunk objective(또는 ce_marginal) 위에 **N6 정규화 band(weight-decay×2.0 · dropout cap 0.30, grok 전이)** + **N7 dictionary-aux loss(trunk penultimate L1 sparse-coding, λ=0.05)** 를 얹으면 undertrain floor 가 배제되어 엔진-네이티브 **G1 composed_distinct 가 ce_marginal 대비 상승**(≥1 register, 또는 G6 fals≥1)한다. 부속: N6 단독·N7 단독·N8 자모 teach·N1 TLoRA expert-weight·N3 DBES 진단축.

## 메커니즘 — readout 아닌 trunk OBJECTIVE 축
이번 세션 곱셈 binding *readout* 은 NOT-SUPPORTED floor(EXP-3 ⊙: G1=0·G6 fals=0, [[exp3-bind-g1g6-engine-native-floor]]). binding 은 readout *위치*의 문제가 아니다. 본 레버는 **operator 를 0개 건드리고** 학습 신호/정규화/진단만 바꾼다 → production additive readout 유지 = 모든 arm `.clm`-serializable = 엔진-네이티브 by-construction OPEN(EXP-3 binding 이 BLOCKED 였던 것과 대조). 외부문헌 수렴(Doshi/Gromov 2023: 정규화가 grok 전이 강제 → numpy-toy chance 는 천장 아닌 undertrain floor · Barin Pacela 2026: binding = 학습된 dictionary 방향). N6 은 정확히 undertrain confound 를 제거하는 통제([[g1-lever-multilens-objective]]).

## FROZEN bar (측정 전 박제 · 사후이동 금지)
- **G1 RECOMBINATION (주):** 어떤 k∈{2,3,4,5} 에서 composed_distinct ≥ 2 AND > max_single AND coherent (H_1129/1137).
- **G6 IDEATION ★:** dist ≥ 5 (pairwise Jaccard<0.5) AND fals ≥ 1 (H_1464; floor = fals=0).
- **held-out DESCENT:** register val_CE < ln256=5.5452, `verify_clm_v2.py descent` PASS.
- **LIFT:** arm 의 엔진-네이티브 G1 best_distinct/G6 fals/n_green 이 같은 3-seed(4307/4308/4309) ce_marginal 통제 대비 strictly 증가. 측정 = engine-native py 2-production(`core/g_gates.py` ← `core/clm_decode.py`, torch-free=TERMINAL).

## wired
launch-ready (303M GPU 미실행). $0 CPU smoke = 파이프 검증 only(능력 측정 아님). 능력 verdict 는 303M GPU 학습 후 엔진-네이티브 재측정에서만.

## 동기
이번 세션 binding(곱셈 readout) + objective + cheap 레버 전부 INCONCLUSIVE-at-floor = undertrain floor 의심. N6 정규화 band 가 floor 해소의 전제 — "정규화·step 부족이라 안 열린 것"인지 "진짜 천장"인지 격리한다.

## artifacts
state/1630_reg_dictaux/ (PREREG.md · trainer.py · LAUNCH_303M.md · SMOKE.md · ckpt)
