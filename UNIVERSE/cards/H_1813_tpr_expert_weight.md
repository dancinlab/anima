---
id: H_1813
slug: tpr_expert_weight
tier: PRE-REG
title: TPR expert-weight TLoRA + DBES 분화진단 — ConvMoE expert 내부 weight 구조 레버 (N1+N3)
verdict: PRE-REG (launch-ready · $0 smoke GREEN · 303M GPU 미실행)
status: PRE-REG
wired: launch-ready (303M 미실행)
verdict_artifact:
source: UNIVERSE
archived: false
---

# H_1813 TPR expert-weight TLoRA + DBES 진단 (N1+N3)

## 가설
G1 재조합벽 / G6 착상벽의 미탐색 구조 레버 = ConvMoE **expert 의 내부 weight 구조**(readout 위치 아님). expert conv weight 를 tensor-product 로 reparameterize(N1 TLoRA/TensorPoly, rank=8, 2405.16671)하여 "구조적(low-rank 텐서곱 = compositional) inductive bias 를 학습 weight 에 넣으면 재조합이 열리나"를 묻는다. N3(DBES, 측정-only)는 "재조합 안 됨 = expert 미분화?"를 expert 분화도(output 쌍 cosine·router entropy·usage Gini)로 인과 격리.

## 메커니즘 — 곱셈 readout 아닌 expert WEIGHT 축
곱셈 binding 을 readout 위치에서 이미 floor 냈다(EXP-3 ARM-BIND: G1=0 ∧ G6 fals=0, [[exp3-bind-g1g6-engine-native-floor]]). 본 패키지는 *다른 위치* = expert weight. **Greff 결합가설:** binding operator 는 학습 objective 와 결합했을 때만 lift(2012.05208 + Furrer + Barin Pacela) → N1 단독 + N1+학습신호(N7 dict-aux / N8 jamo) arm. 전부 production additive readout(Conv1d d→V) 유지 → TLoRA 는 직렬화 직전 dense conv weight 로 materialize → `.clm` engine-native by-construction OPEN(EXP-3 binding BLOCKED 아님). trunk OBJECTIVE/weight 축이 1차 레버라는 [[g1-lever-multilens-objective]] 일관.

## FROZEN bar (측정 전 박제)
- **G1 RECOMBINATION (주):** k∈{2,3,4,5} 에서 composed_distinct ≥ 2 AND > max_single AND coherent (H_1129/1137).
- **G6 IDEATION ★:** dist ≥ 5 AND fals ≥ 1 (H_1464).
- **held-out DESCENT:** val_CE < ln256, `verify_clm_v2.py descent` PASS.
- **LIFT:** tlora/tlora_dict arm 의 엔진-네이티브 G1/G6 가 ctrl 대비 strictly 증가. 측정 = engine-native py 2-production(`core/g_gates.py` ← `core/clm_decode.py`, TERMINAL).

## wired
launch-ready (303M GPU 미실행). $0 smoke = 파이프 검증 only.

## 동기
이번 세션 binding readout + objective + cheap 레버 전부 INCONCLUSIVE-at-floor = undertrain 의심. expert weight 의 구조적 bias 가 floor 위로 올리는지, expert collapse(미분화)가 G1 floor 의 원인인지 격리.

## artifacts
state/1631_tpr_expert_weight/ (PREREG.md · trainer.py · LAUNCH_SPEC_303M.md · SMOKE_LOG.md · ckpt)
