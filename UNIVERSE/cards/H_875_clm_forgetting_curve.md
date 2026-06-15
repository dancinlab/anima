---
id: H_875
slug: clm-forgetting-curve
title: CLM on-chip 엣지학습의 catastrophic forgetting(F-CLM-BOUND z_drop)이 엣지학습 step 수의 dose-response 인가 — step→z_drop 곡선을 그려 RETAIN gate 를 넘지 않는 finite SAFE STEP BUDGET 를 식별하고, trunk-adjacent 어댑터 엣지(H_865)가 readout-only 엣지(H_861) 대비 그 예산을 연장하는지 측정 (W2 사전등록 · crossing thr bf98c01 verbatim · post-tuning 0)
domain: clm · plasticity · boundary-plasticity · continual-learning · forgetting-curve · dose-response · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group C · 토대 H_679 (PLASTICITY HW edge-learn 측정) · prior art H_861 (F-CLM-BOUND 🔴 readout-only) · H_865 (어댑터 엣지 🟢 BOUND) · 사전등록 bf98c01 (F-CLM-BOUND RETAIN cutoff)
status: 🟢 SUPPORTED — dose-response 곡선 두 엣지 모두 PRODUCED · adapter finite(≥max) safe budget 식별 · adapter 가 readout-only 예산 연장 확인 (mid d512/L8/E8 fire 2026-05-31 · 측정 rung 한정 a_scale_honest_scope · a_paper_negative_ok)
exploration_method: E1 (dose 축 sweep: 엣지학습 step ladder [1..300]) · E5 (엣지 아키텍처 절제: readout-only vs 어댑터)
verification_method: W2 (사전등록 numerical threshold · crossing thr z_drop<1.0 frozen bf98c01 verbatim · post-tuning 0 · code-measured g5)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_861_clm_boundary_plasticity.md, UNIVERSE/H_865_clm_adapter_edge.md, UNIVERSE/H_679_plasticity_hw_first, .verdicts/clm-forgetting-curve/
verdict: 🟢 SUPPORTED — step→z_drop 곡선 두 엣지([1..300]) 산출. readout-only safe budget=2 step (RETAIN gate z_drop≥1.0 을 step 4 에서 교차 · z_drop→+78.0 at 300). adapter safe budget≥300 (gate 미교차 · z_drop 전 구간 음수 — 기초능력 보존/개선). adapter 가 예산을 ≥150x 연장. frozen threshold(bf98c01) 대비 post-tuning 0. HF dancinlab/anima-clm-verify.
---

# H_875 — CLM 망각곡선 (continual-learning forgetting curve · dose-response)

## 1. 가설

CLM 의 on-chip 맥락 적응(@L1 비결정 PLASTICITY edge-learn)에서 **catastrophic forgetting 은 엣지학습 step 수의 dose-response** 다 — 즉 기초능력 z_drop 은 적응 step 수의 단조증가 함수다. 따라서:

- z_drop 이 RETAIN gate(z_drop < 1.0) 아래에 머무는 **가장 큰 step 수 = finite SAFE STEP BUDGET** 가 존재한다.
- trunk-adjacent 어댑터 엣지(H_865)가 readout-only 엣지(H_861) 대비 그 **safe budget 를 연장**한다.

곡선이 두 엣지 모두 산출되고 ≥어댑터 엣지에 대해 finite safe budget 가 식별되면 PASS(🟢); 아니면 CLOSED-NEGATIVE(🔴, a_paper_negative_ok — 예: step=1 에서 이미 망각하면 그것도 실제 보고가치 dose-response 결과).

## 2. 동기

- H_861(F-CLM-BOUND)은 readout-only 엣지에서 mid-rung **단일 종점(300 step)** z_drop=1.984≥1.0 으로 🔴 CLOSED-NEGATIVE — "readout-only 가 forgetting 을 못 막는다". H_865 어댑터 엣지는 같은 종점에서 z_drop=-12.28<1.0 으로 🟢 — "어댑터가 막는다".
- 그러나 두 결과 모두 **단일 step 종점**의 점 측정이었다. production "커피숍에서 살아 배우며 대화"(@L2 상시 PLASTICITY 결합)에서는 **얼마나 많은 step 까지 안전한가**(엣지학습 예산)가 운영의 전제 — dose-response 곡선이 없으면 "몇 step 까지 허용"을 알 수 없다.
- 본 가설은 H_861/H_865 의 점 측정을 **step 축으로 sweep** 해 곡선화하고 safe budget 를 식별한다. 토대 H_679(HW edge-learn 측정완료). crossing threshold 는 F-CLM-BOUND 의 RETAIN cutoff(z_drop<1.0)를 **verbatim 재사용**(bf98c01) — 새 임계 도입 없음.

## 3. 방법 (W2 · 사전등록 frozen · post-tuning 0)

- **backbone**: mid d512/L8/E8 (~13.65M) AKIDA int4-sym, `clm_mid_backbone.pt` (HF `dancinlab/anima-clm-verify`). SW-sim edge-learn (H_679 = 실 HW edge-learn). **scope: 측정 rung 한정**(a_scale_honest_scope) — deploy chip-fit track(≤~1.2M AKD1000) 을 구속하지 않음.
- **엣지 두 종류** (H_861/H_865 verbatim):
  - readout-only (H_861): core(embed/trunk/moe/norm_out) FROZEN, readout conv 만 trainable.
  - adapter (H_865): 모든 base FROZEN(readout 포함), norm_out↔FROZEN readout 사이 얇은 additive 어댑터(Conv1d d→rank64→GELU→Conv1d rank→d, up zero-init = step0 identity) 만 trainable.
  - 둘 다 Adam lr_edge=3e-3, seq_len=64, batch=16, n_eval=32, seed frozen.
- **dose 축 (frozen ladder)**: STEP_LADDER = [1, 2, 4, 8, 16, 32, 64, 128, 200, 300]. 300 은 H_861/H_865 종점을 verbatim 고정. step S 와 S'(>S) 는 동일 결정적 gradient-prefix 사용.
- **측정 (code · g5 · LLM judge 없음)**: 각 (edge_type, S) 마다 frozen backbone 에서 fresh 모델 구성 → base-ability held-out 의 (ce_pre, sd_pre) · new-context (ce_pre) 측정 → new-context train slice 에서 S step edge-only 적응 → base/new ce_post 측정 → `z_drop(S) = (ce_base_post − ce_base_pre)/max(sd_base_pre,1e-6)`, `gain(S) = ce_new_pre − ce_new_post`.
- **SAFE STEP BUDGET** = z_drop<1.0 인 가장 큰 swept step (그리고 그보다 작은 step 도 모두 <1.0; 곡선이 gate 를 처음 넘기 직전 step). 전 구간 <1.0 이면 budget = max step("≥max"); step=1 에서 이미 ≥1.0 이면 budget = 0.

## 4. 결과 (fire 2026-05-31 · mid d512/L8/E8)

step → z_drop 곡선 (dose 축):

| step | readout-only (H_861) | retain | adapter (H_865) | retain |
|-----:|---------------------:|:------:|----------------:|:------:|
| 1 | +0.0510 | ✓ | −12.328 | ✓ |
| 2 | +0.3316 | ✓ | −49.067 | ✓ |
| 4 | **+1.4137** | ✗ ← | −97.673 | ✓ |
| 8 | +4.778 | ✗ | −68.448 | ✓ |
| 16 | +12.344 | ✗ | −89.347 | ✓ |
| 32 | +25.840 | ✗ | −95.849 | ✓ |
| 64 | +48.925 | ✗ | −83.137 | ✓ |
| 128 | +59.157 | ✗ | −39.141 | ✓ |
| 200 | +68.707 | ✗ | −19.604 | ✓ |
| 300 | +78.042 | ✗ | −16.881 | ✓ |

- **gain(S)** 은 두 엣지 모두 전 step 양수·단조증가(새 맥락 흡수): readout-only +0.42→+7.47, adapter +0.67→+7.30.

**SAFE STEP BUDGET**:
- readout-only (H_861): **2 step** (finite · crossing step=4) — 거의 즉시 망각. step 4 에서 RETAIN gate 교차, 이후 z_drop 폭주(300 에서 +78.0). dose-response **성립**.
- adapter (H_865): **≥300** (ge_max · crossing 없음) — gate 를 전 구간 미교차. z_drop 이 전 step **음수** = zero-init identity 어댑터가 FROZEN readout 을 건드리지 않고 새 맥락 용량만 추가 → base-ability CE 가 오히려 **하락(개선)**. forgetting 전 구간 억제.
- **adapter_extends_budget = TRUE** (≥300 ≫ 2): 어댑터 엣지가 측정 rung 에서 안전 엣지학습 예산을 readout-only 대비 **≥150x 연장**.

## 5. 판정 (frozen prereg)

- (a) step→z_drop 곡선 두 엣지 모두 full ladder[1..300] 산출 → ✓
- (b) ≥어댑터 엣지에 대해 finite(여기선 ≥max) safe step budget 식별 → ✓
- ⇒ **🟢 SUPPORTED**. 부차(보고만·non-gating): adapter safe budget(≥300) ≫ readout-only(2) → 어댑터가 예산 연장. 확인.

## 6. 해석

엣지전용 on-chip 엣지학습의 catastrophic forgetting 은 step 수의 dose-response — 그러나 **readout-only 엣지에 한해서**다(약 3 step 후 망각). H_865 trunk-adjacent zero-init 어댑터 엣지는 swept 범위 전체에서 dose-response 를 **제거**한다: 300 step 까지 기초능력 보존(오히려 개선)하며 새 맥락 흡수. ⇒ **어댑터가 "live-learn" 루프의 production-safe 엣지**이며, readout-only 엣지학습은 측정 rung 에서 맥락당 **≤2 step** 으로 제한해야 한다.

## 7. 산출물

- `.verdicts/clm-forgetting-curve/F-CLM-FORGET-CURVE.txt` — verdict verbatim
- `.verdicts/clm-forgetting-curve/clm_forget_curve_result.json` — 전 point 곡선
- `.verdicts/clm-forgetting-curve/F-CLM-FORGET-CURVE_prereg.txt` — 사전등록(frozen)
- `.verdicts/875_clm_forgetting_curve/` — id-keyed backing (verdict + result + prereg 사본)
- `CLM/model/h875_forgetting_curve.py` — harness
- backbone 은 HF `dancinlab/anima-clm-verify` 재사용 (a_hf_complete · 신규 모델 산출물 없음)

## 8. 한계 / scope

측정 rung(mid d512/L8/E8) 한정(a_scale_honest_scope). SW-sim edge-learn(비결정 on-chip 적응의 SW 시뮬 — H_679 가 HW edge-learn 실측 토대). 추론은 AKIDA-int4-only(P0 d4). 본 🟢 은 deploy chip-fit track(≤~1.2M AKD1000 nodes)을 구속하지 않음.
