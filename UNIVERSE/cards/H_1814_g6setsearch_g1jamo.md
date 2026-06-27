---
id: H_1814
slug: g6setsearch_g1jamo
tier: PRE-REG
title: G6 diverse-set-search + G1 자모 teach-signal — teach-signal 형태 trunk-objective 레버 (N4+N8)
verdict: PRE-REG (launch-ready · $0 smoke GREEN · 303M GPU 미실행)
status: PRE-REG
wired: launch-ready (303M 미실행)
verdict_artifact:
source: UNIVERSE
archived: false
---

# H_1814 G6 diverse-set-search + G1 자모 teach-signal (N4+N8)

## 가설
두 *teach-signal 형태* 레버(둘 다 readout 위치 아닌 학습 신호 측):
- **N8 (자모 teach · G1, SCRIPT 2604.12377):** trunk penultimate 에서 Hangul 음절의 (초·중·종)성 자모 클래스를 예측하는 작은 aux head 로 subcharacter compositional 구조를 명시 teach signal 로 주입 → "재조합 재료가 분해돼야 결합 가능" (ko-jamo-mitosis H_1316/1321 🟢 계보).
- **N4 (diverse-set-search · G6, 2606.10587):** 학습 중 주기적으로 G6 "if A, then B:" frame 에서 K 연속을 샘플해 engine-aligned diversity(`_g6_jaccard`<0.5)+falsifiability(`_g6_is_falsifiable`) reward(g_gates 채점 detector 바로 그것, LLM-judge 금지)로 diverse+falsifiable set 멤버 likelihood 를 올리는 set-level objective.

결합(n4n8_both)이 단독보다 super-additive 인가 INERT 인가.

## 메커니즘 — readout 아닌 teach-signal(OBJECTIVE) 축
곱셈 binding readout NOT-SUPPORTED floor(EXP-3: 전 9 arm G1=0·G6 fals=0, [[exp3-bind-g1g6-engine-native-floor]]). G1 진짜 레버 = trunk OBJECTIVE([[g1-lever-multilens-objective]], depth/binding-lane/data-presence 전부 falsify; 외부문헌 Furrer/Barin Pacela/Doshi-Gromov 수렴). 1602 가 손실 *형태*를 바꿨다면 본 실험은 그 위에서 두 *teach-signal 형태* 레버(RESEARCH §92 제언 4·5). G6 병목은 decode 가 아니라 생성 다양성+검증가능성([[h1590-g6-scaffold-torch-artifact]] "lever≠decode"). 전부 additive readout 유지 → `.clm` engine-native OPEN.

## FROZEN bar (측정 전 박제)
- **G1 RECOMBINATION:** k∈{2,3,4,5} 에서 composed_distinct ≥ 2 AND > max_single AND coherent (H_1129/1137).
- **G6 IDEATION ★ (주 N4):** dist ≥ 5 (Jaccard<0.5) AND fals ≥ 1 (H_1464).
- **held-out DESCENT:** val_CE < ln256, `verify_clm_v2.py descent` PASS.
- **LIFT:** n8_jamo→G1 · n4_setsearch→G6 가 baseline(표준 CE) 대비 strictly 증가. 측정 = engine-native py 2-production(`core/g_gates.py` ← `core/clm_decode.py`, TERMINAL).

## wired
launch-ready (303M GPU 미실행). $0 smoke = 파이프 검증 only.

## 동기
이번 세션 binding+objective+cheap 레버 전부 INCONCLUSIVE-at-floor = undertrain 의심. teach-signal(재료 disentangle / set-search diversity)이 floor 위로 G1/G6 를 올리는지 측정.

## artifacts
state/1632_g6setsearch_g1jamo/ (PREREG.md · trainer.py · LAUNCH_SPEC_303M.md · SMOKE.log · ckpt)
