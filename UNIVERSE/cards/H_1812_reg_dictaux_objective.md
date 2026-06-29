---
id: H_1812
slug: reg_dictaux_objective
tier: NOT-SUPPORTED (DIRECTIONAL-positive)
title: 정규화 band(grok) + dictionary-aux objective — G1/G6 trunk-objective 레버 (N6+N7)
verdict: NOT-SUPPORTED at frozen bar · DIRECTIONAL-positive — n6n7 vs ce_marginal G1 best_distinct 0→1 · G6 dist 4→5 · G0 2/5→4/5 (예측 방향, bar 미달); N6 단독·N7 단독 둘다 floor = lift 는 INTERACTION/synergy; 2000-step·seed4307 단일 (PREREG 4000 미달); 엔진-네이티브 py 2-production core/g_gates.py --gen 80; 4000-step ING follow-on
status: DONE (303M engine-native G0-G6)
wired: engine-native (py 2-production core/g_gates.py ← core/clm_decode.py, torch-free numpy = TERMINAL-eligible)
verdict_artifact: state/verdicts/1630_reg_dictaux/H_1812.txt
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

## 결과 (303M engine-native G0-G6 · `cli/evaluate.py`→`core/g_gates.py` --gen 80 torch-free numpy = TERMINAL)

학습 = clm303_clean 4칸 register · CLMConvMoE L4·d3784·E2→E3 (345.665M) · seed4307 · **2000-step**
(PREREG 4000 미달 — matrix 가 병렬 에이전트 2000-step). 4 arm 모두 held-out 4/4 register DESCENT
(overfit 없음, lossF~1.17).

| gate | ce_marginal | n6n7 | n6_grok | n7_dictaux |
|---|---|---|---|---|
| G0 | 🔴 2/5 | 🟢 **4/5** | 🔴 2/5 | 🔴 3/5 |
| **G1** | 🔴 dist=**0** | 🔴 dist=**1** | 🔴 0 | 🔴 0 |
| G2 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 |
| G5 | 🔴 .49 | 🔴 .47 | 🔴 .56 | 🔴 .49 |
| **G6★** | 🔴 d4·f0 | 🔴 **d5**·f0 | 🔴 d3·f0 | 🔴 d0·f0 |
| CLOSURE | 🔴 | 🔴 | 🔴 | 🔴 |

**verdict = NOT-SUPPORTED at frozen bar · DIRECTIONAL-positive.** n6n7 이 control 대비 G1 0→1·G6 dist
4→5·G0 2/5→4/5 로 **예측 방향 lift**(H_1602 objective-축 flat-floor 와 대조 — 신호를 바닥에서 떼어냄).
단 G1 bar(≥2)·G6 fals bar(≥1) **미달** → frozen bar NOT-SUPPORTED. **ablation: N6 단독·N7 단독 둘 다
floor(오히려 G6 악화) → lift 는 어느 component 도 아닌 INTERACTION/super-additive synergy.** 핵심 질문
(undertrain vs 구조벽): **부분적 undertrain, interaction-gated** — 신호가 움직였으니 hard 천장 아니나
강도 부족. 결정 follow-on = **PREREG 4000-step + multiseed{4307,4308,4309}** (0→1 이 더 큰 step 에서
→2+ 되나). artifact = `state/verdicts/1630_reg_dictaux/H_1812.txt`(4-arm 엔진-네이티브 raw).

## wired
engine-native (py 2-production `core/g_gates.py` ← `core/clm_decode.py`, torch-free numpy = TERMINAL).
ckpt PULL 완료(4×176MB .clm + sha256, `state/1630_reg_dictaux/ckpt/`). 4000-step 재측정 = ING follow-on.

## 동기
이번 세션 binding(곱셈 readout) + objective + cheap 레버 전부 INCONCLUSIVE-at-floor = undertrain floor 의심. N6 정규화 band 가 floor 해소의 전제 — "정규화·step 부족이라 안 열린 것"인지 "진짜 천장"인지 격리한다.

## artifacts
state/1630_reg_dictaux/ (PREREG.md · trainer.py · LAUNCH_303M.md · SMOKE.md · ckpt)
