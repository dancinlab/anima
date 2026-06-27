---
id: H_1815
slug: cls_sep_complete
tier: PRE-REG
title: 해마 CLS pattern separation + completion — 재조합 재료 직교화 생물 G1 레버
verdict: PRE-REG (launch-ready · $0 smoke GREEN · 303M GPU 미실행)
status: PRE-REG
wired: launch-ready (303M 미실행)
verdict_artifact:
source: UNIVERSE
archived: false
---

# H_1815 CLS pattern separation + completion (생물 렌즈 #1)

## 가설
anima 의 G1 재조합벽은 트렁크가 **합칠 개념들의 표현을 분리(직교화)하지 못해서** 생긴다. A·B 가 penultimate 에서 엉켜 있으면(entangled) 모델은 둘을 구별되는 재료로 잡고 합성할 수 없다. 해마 보완학습계(CLS)의 **DG pattern separation(직교화·sparsen)** 으로 재료를 분리하고 **CA3 pattern completion(부분 cue→전체 복원)** 으로 합성을 가능케 하면 G1 이 floor 위로 올라온다 (arxiv 2507.11393 · Marr-Albus expand+sparsen+decorrelate). a_no_llm_frame_trap 정합: 해마 계보([[h1227-immune-clonal-memory]] · [[h1288-eviction-policy]])의 미탐색 축 = 저장 아닌 *재료 직교화*.

## 메커니즘 — 곱셈 readout 아닌 trunk-표현(OBJECTIVE) 축
직전 세션 확정: 곱셈 binding operator 를 readout 에 끼우면 floor + non-additive readout 은 `.clm` 직렬화 BLOCKED([[exp3-bind-g1g6-engine-native-floor]]). → CLS 는 trunk penultimate(post `norm_out`, pre `readout`)에 거는 2 보조 손실:
- **L_sep** = penultimate 채널 간 off-diagonal correlation energy → 0(직교화) + 약한 L1 sparsity(Marr-Albus sparsen).
- **L_complete** = 채널 일부 마스킹(부분 cue) 후 작은 linear head 가 전체 코드 복원(MSE, CA3 autoassociative). head 는 학습 전용(직렬화 전 폐기).
production additive readout(Conv1d d→V)은 세 arm 전부 동일 → 모든 `.clm` engine-native G1 by-construction OPEN(EXP-3 binding BLOCKED 아님). trunk OBJECTIVE 1차 레버 [[g1-lever-multilens-objective]] 일관.

## FROZEN bar (측정 전 박제)
- **G1 RECOMBINATION (주):** k∈{2,3,4,5} 에서 composed_distinct ≥ 2 AND > max_single AND coherent (H_1129/1137).
- **G6 IDEATION ★:** dist ≥ 5 AND fals ≥ 1 (H_1464).
- **held-out DESCENT:** val_CE < ln256, `verify_clm_v2.py descent` PASS.
- **LIFT:** L_sep(±L_complete) arm 의 엔진-네이티브 G1 이 ce_marginal 대비 strictly 증가. 측정 = engine-native py 2-production(`core/g_gates.py` ← `core/clm_decode.py`, TERMINAL).

## wired
launch-ready (303M GPU 미실행). $0 smoke = 파이프 검증 only.

## 동기
이번 세션 binding+objective+cheap 레버 전부 INCONCLUSIVE-at-floor = undertrain 의심(N6 정규화가 floor 해소 전제). 생물 렌즈 1순위로 "재료 직교화"가 floor 위로 G1 을 올리는지 측정.

## artifacts
state/1640_cls_sep_complete/ (PREREG.md · trainer.py · gpu_launch.sh · smoke.sh · ckpt)
