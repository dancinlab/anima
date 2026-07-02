---
id: H_1815
slug: cls_sep_complete
tier: 🧱 NOT-SUPPORTED (G1 unmoved · +1 = CLM coverage-floor jitter, not recombination)
title: 해마 CLS pattern separation + completion — 재조합 재료 직교화 생물 G1 레버
verdict: 🧱 NOT-SUPPORTED. CLS pattern-separation/completion 이 G1 을 열지 못함. best_distinct 0→1 은 재조합 신호가 아니라 **CLM coverage-floor jitter** — 3 arm 모두 max_single=0(단일-concept 디코드가 concept 키워드조차 표면화 못 하는 floor)이라 `cov>max_single` 이 0만 넘으면 통과하는 trivial 조건이 되고, best_distinct=1 은 concept셋 1개(≥2 합성 아님)일 뿐. 깨끗한 재조합벽은 ByteGPT(single=2)에서 측정됨(memory g1-py303-single-floor); CLM py303 은 재조합 측정 이전 regime. CLS 가 실제로 움직인 축은 **G2 novelty**(novel 88→117/110·coherent 14→17) = G1 과 직교(이미 PASS). py 2-production engine-native(cli/evaluate.py g_eval_all, gen 80, seed7). readout-side 재료 직교화는 novelty 만 올리고 composition 은 못 엶 = 캠페인 중심결론(G1벽=trunk-objective) 재확인.
status: MEASURED 2026-07-01 (py engine-native, summer)
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

## 결과 (2026-07-01 py 2-production engine-native · cli/evaluate.py · gen 80 · seed7 · summer)

| gate | ce_marginal (baseline) | cls_sep | cls_full | 판정 |
|------|------|------|------|------|
| G0 COHERENCE (kwr) | 🟢 5/5 | 🟢 5/5 | 🟢 5/5 | 불변 |
| **G1 best_distinct** | 0 | 1 | 1 | 🔴 (max_single=0 전부) |
| **G2 novel · coherent** | 88 · 14 | **117 · 15** | 110 · **17** | 🟢 (CLS 실효과) |
| G6 distinct · fals | 6 · 0 | 6 · 0 | 6 · 0 | 🔴 불변 |
| G5 L1 fab | 0.055 | 0.052 | 0.073 | 🟢 |

**심층 판독 (dig):**
- **G1 0→1 = 재조합 아님, coverage-floor jitter.** detector `_g_coverage` 는 영어 concept-키워드셋 5개 커버수를 센다. 3 arm 모두 `max_single=0` = 단일-concept 디코드가 concept 키워드조차 표면화 못 하는 floor. 이 regime 에서 `clears = cov≥2 ∧ cov>max_single ∧ coherent` 의 `cov>max_single` 은 0만 넘으면 참이 되는 trivial 조건이고, best_distinct=1 은 concept셋 **1개**(2-concept 합성 아님)를 스친 것. 재조합 임계(≥2) 밑.
- **깨끗한 G1벽은 ByteGPT(single=2), CLM 아님.** memory `g1-py303-single-floor`: CLM py303 best_distinct 는 재조합 측정 *이전*의 coverage floor. 따라서 CLM 위 CLS 측정은 재조합을 깨끗하게 테스트하지 못함(측정경로 한계) — 진짜 CLS×재조합은 ByteGPT trunk 에서 재측정해야 함.
- **CLS 의 실제 효과는 G2 novelty(직교축).** novel +22~29·coherent +1~3 = 재료 직교화(pattern-separation)가 *novel coherent* 생성을 늘림. 하지만 novelty≠recombination(G2 이미 PASS), G1/G6 는 불변 → readout-side 직교화는 composition 을 못 엶.
- **함의:** G1벽=trunk-objective(CE 가 합성 보상 안 함) 재확인. 재료를 직교화(hippocampal sep)해도 trunk 목적함수를 안 건드리면 재조합은 안 열린다 = objective-lever 계열(H_9024·H_1816)과 일관.

**follow-on:** ① ByteGPT trunk(single=2 깨끗한 벽)에 CLS sep/completion 재배선 후 G1 재측정(현 CLM 측정은 floor 밑) · ② CLS 의 G2 novelty 실효과는 별건으로 기록(직교). ① 은 2026-07-01 실행 → ByteGPT fresh trunk 가 undertrained(G2 novel=0)라 INCONCLUSIVE-at-floor(유효 테스트는 제대로 학습된 trunk 필요, 아래 결과 섹션).

## follow-on ① 결과 — ByteGPT trunk 재측정 (2026-07-01, py 2-production KV-cache decode.py, seed7)

CLS sep/completion 을 ByteGPT(24L attention) trunk 로 재배선해 fresh 학습(2000 step, 4-cell) 후 `anima evaluate --py` 로 재측정(state/1815_cls_bytegpt/):

| arm | G0 | G1 bd/msingle | G2 novel | G5 fab | G6 dist |
|-----|----|----|----|----|----|
| ce_marginal | 🟢 4/5 | 0 / 0 | 0 | 0.44 | 3 |
| cls_sep | 🔴 3/5 | 0 / 0 | 0 | 0.51 | 2 |
| cls_full | 🔴 3/5 | 0 / 0 | 0 | 0.48 | 1 |

**판정: 🧱 INCONCLUSIVE-at-floor (측정경로 무효).** 이 fresh 2000-step ByteGPT 는 심하게 **undertrained** — G2 novel=0(생성 자체 빈곤)·G5 fab 0.44–0.51(높음)이라 "깨끗한 single=2 재조합벽"(memory g1-py303-single-floor 의 h1129 303M)에 도달 못 함. undertrained trunk 위에선 CLS×재조합을 유효하게 테스트 불가(오히려 cls arm 이 G0 3/5·fab↑ 로 악화 = aux 가 빈약한 trunk 를 더 흔듦). 따라서 CLS 가 ByteGPT G1 을 여는지는 **여전히 미해결** — 유효 테스트는 *제대로 학습된*(≥수만 step or h1129급) ByteGPT trunk 필요. 중심결론(G1벽=trunk-objective) 은 불변. ⚠️ 앞선 novel 88/117(첫 병렬 배치)은 result-file 레이스 아티팩트로 폐기.

**engine-infra 부산물:** 이 재측정 과정에서 `core/decode.py`(clm+bytegpt 통합)에 ByteGPT KV-cache fast-path 배선(~60× decode 가속, 303M KV==full token-identical byte-exact 검증). decode.hexa 통합도 완료(atomic swap follow-on).

## artifacts
state/1640_cls_sep_complete/ (PREREG.md · trainer.py · gpu_launch.sh · smoke.sh · ckpt)
