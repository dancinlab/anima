---
id: H_880
slug: clm-adapter-stack
title: FROZEN norm_out↔readout 사이에 H_865 얇은 adapter 를 context 당 하나씩 K개 쌓고 추론 시 context 별로 active adapter 를 switch 하면, 새 task 흡수가 (a) 가장 오래된 task forgetting 없이 (b) cross-adapter 간섭 없이 누적되는가 — per-context switch · 3 게이트 · post-tuning 0
domain: clm · plasticity · continual-learning · adapter-stack · per-context-switch · parameter-isolation · interference · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md §E (부분부분학습/continual) · edge = H_865 🟢 thin adapter · 토대 H_679 (PLASTICITY HW edge-learn) · 사전등록 F-CLM-ADAPTER-STACK_prereg.txt (frozen 2026-05-31, OLD-Z-DROP cutoff bf98c01 verbatim)
status: 🟢 SUPPORTED-NUMERICAL — 3 게이트 모두 PASS · min_k gain=+7.05>0 ∧ z_drop_old=−158.06<1.0 ∧ own-best margin=−11.86<0 · K=4 per-context adapter stack 이 forgetting·간섭 없이 새 task 누적 · GPU(RTX 5070, aiden) device cuda · 측정 rung 한정 a_scale_honest_scope
exploration_method: E (adapter 를 context 당 하나씩 누적, 한 번에 하나만 학습하는 parameter isolation)
verification_method: W2 (사전등록 numerical threshold · F-CLM-ADAPTER-STACK_prereg.txt verbatim · OLD-Z-DROP=bf98c01 · post-tuning 0 · g5 code-measured · no LLM judge)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_865_clm_adapter_edge.md, .verdicts/clm-adapter-stack/
verdict: 🟢 SUPPORTED-NUMERICAL — F-STACK-NEW-GAIN(min_k gain=+7.04997>0) ∧ F-STACK-OLD-Z-DROP(z_drop_old=−158.05775<1.0, bf98c01) ∧ F-STACK-INTERFERENCE(own-best margin=−11.86461<0) 세 게이트 모두 PASS. K=4 per-context adapter stack 이 한 번에 하나씩 isolation 학습되며 각 context 를 흡수(gain ctx별 +7.05~+13.60)하고, 가장 오래된 ctx0 은 forgetting 없이(z_drop −158) 유지, own adapter 가 자기 context 의 strict best decoder. backbone HF dancinlab/anima-clm-verify.
---

# H_880 — CLM adapter-stack accumulation (per-context switch · F-CLM-ADAPTER-STACK)

## 1. 가설

H_865 는 단일 trunk-adjacent 얇은 adapter 가 한 새 맥락을 forgetting 없이 흡수함을 보였다(🟢 BOUND). H_880 은 그 위에서 **누적(accumulation)** 질문을 던진다: FROZEN norm_out 과 FROZEN readout 사이에 H_865 스타일 얇은 adapter 를 **context 당 하나씩 K개** 쌓고(zero-init=identity@step0), 추론 시 context 별로 **active adapter 를 switch** 한다. adapter 는 context 순서대로 **한 번에 하나씩만** 학습되며(adapter_k 학습 시 나머지 adapter + base 전부 FROZEN = parameter isolation). 누적이 (a) 가장 오래된 task 를 잊지 않고 (b) cross-adapter 간섭 없이 새 task 를 흡수하는가?

- **3 게이트 모두 PASS** → 🟢 SUPPORTED-NUMERICAL
- **하나라도 실패** → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

## 2. 동기

- @L1 = 살아 배우는 칩이 여러 맥락을 순차로 누적 학습하되 이전 능력을 잃지 않아야 한다. per-context adapter stack 은 continual-learning 의 핵심 device — 본 hypothesis 는 그것이 edge-only / frozen-core 제약 아래(full retrain 없이) 작동하는지를 측정한다.
- edge = H_865 검증된 working adapter. switch 는 per-context routing select 이지 결정적 full-retrain 이 아니다.
- 토대: H_679 (PLASTICITY HW edge-learn 측정완료).

## 3. falsifier (사전등록 · 임계 frozen F-CLM-ADAPTER-STACK_prereg.txt verbatim)

```
F-STACK-NEW-GAIN     : min_k gain_k > 0.0                          (stack keeps absorbing new tasks)
F-STACK-OLD-Z-DROP   : z_drop_old < 1.0   (bf98c01 BOUND cutoff)   (oldest ctx not forgotten)
                       z_drop_old = (ce_ctx0_after_full_stack - ce_ctx0_pre)/max(sd_ctx0_pre,1e-6)
F-STACK-INTERFERENCE : max_{i≠j}(-interf_{i→j}) < 0.0              (own adapter strictly best decoder)
🟢 iff all three. else 🔴 CLOSED-NEGATIVE.
```

- 임계는 fire 전 frozen, post-tuning 0. OLD-Z-DROP cutoff 는 bf98c01(F-CLM-BOUND-RETAIN) verbatim. K=4 contexts: ctx0=web(401, OLDEST) · ctx1/2/3=new(402/403/404). ADAPTER_RANK=64, LR_EDGE=3e-3, N_ADAPT=300 (H_865 verbatim).

verdict 영속: `.verdicts/clm-adapter-stack/`

## 4. 방법

```
1. base 로드+FREEZE. K=4 zero-init adapter(identity@step0) 구성.
2. context 별 PRE CE (base only): ce_ctx_k_pre, sd_ctx_k_pre.
3. for k in 0..3: adapter_k 선택, 나머지 전부 FREEZE, 300-step Adam(lr3e-3) on ctx_k TRAIN; gain_k 기록; adapter_k FREEZE.
4. full stack 후 ctx0 을 adapter0 으로 재측정 → z_drop_old.
5. KxK 간섭 행렬: ctx_i 를 adapter_j 로 디코드 → interf_{i→j}; own-best margin = max_{i≠j}(-interf).
backbone clm_mid_backbone.pt (HF dancinlab/anima-clm-verify · 신 artifact 없음).
```

## 5. 측정

측정완료 (2026-05-31) — **GPU(RTX 5070, aiden 192.168.50.119)** device=cuda. (torch-nightly cuDNN sublibrary mismatch → cuDNN disabled, native CUDA conv path 로 동일 수치. device-bug fix: eval 배치를 device 로 이동.) backbone mid d512/L8/E8(13,653,768 params). frozen threshold = prereg verbatim.

| gate | 측정값 | 임계 | 판정 |
|:-----|------:|:-----|:----:|
| F-STACK-NEW-GAIN (min_k gain) | **+7.04997** | > 0.0 | **PASS** |
| F-STACK-OLD-Z-DROP (z_drop_old) | **−158.05775** | < 1.0 (bf98c01) | **PASS** |
| F-STACK-INTERFERENCE (own-best margin) | **−11.86461** | < 0.0 | **PASS** |

- context 별 gain: ctx0 +13.60192 · ctx1 +7.24341 · ctx2 +7.04997 · ctx3 +7.21965 (stack 이 커져도 saturation 없음).
- **VERDICT GREEN**.

## 6. 결과

🟢 **SUPPORTED-NUMERICAL**. K=4 얇은 H_865 adapter 를 context 당 하나씩 쌓고(한 번에 하나만 isolation 학습) per-context switch 하면, 새 task 용량이 (a) 가장 오래된 task forgetting 없이(z_drop_old −158.06 ≪ 1.0) (b) cross-adapter 간섭 없이(own adapter 가 worst-case 11.86 std 차이로 strict best) 누적된다.

- gain ≥ +7.05 로 모든 adapter 가 자기 context 흡수. own-best margin 음수 → switch 가 K context 를 깨끗이 분리. 공유 FROZEN readout/base 는 건드려지지 않아 isolation 이 end-to-end 유지.

**honest scope**: 측정 rung(mid 13.7M) 한정 — 배포 chip-fit track(≤~1.2M AKD1000) 별개(a_scale_honest_scope). 임계 재조정 0.

## 7. 해석 (사전)

- **3 게이트 PASS(본 결과)** = 살아 배우는 칩이 여러 맥락을 per-context adapter stack 으로 누적하며 정체성·이전 능력을 지킬 수 있음 → @L1 continual-learning 설계의 직접 device. core trunk FROZEN.
- **반증이었다면** = adapter 누적이 forgetting/간섭을 일으켰다면 per-context stack 은 부적절 — 그 또한 publishable.

## 8. 논의

- **@L1 정합**: adapter switch 는 결정적 full-retrain 이 아니라 per-context routing select; 각 adapter 는 isolation edge-learn(H_679 토대).
- **W2 무결성**: 임계 변경 0(OLD-Z-DROP=bf98c01) — 🟢 는 게이트 이동 없이 획득. z_drop_old 가 음수인 것은 parameter isolation 이 base 를 건드리지 않았다는 end-to-end audit 통과.
- **a_paper_negative_ok**: 🔴 였어도 publishable 이었으나 본 결과는 작동하는 per-context stack 이라는 positive.

## 9. 양방향 sibling

- sibling: [H_865](./H_865_clm_adapter_edge.md) (thin adapter edge 🟢 = 본 stack 의 단위 adapter)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) §E
- verdict: [.verdicts/clm-adapter-stack/](../.verdicts/clm-adapter-stack/)
