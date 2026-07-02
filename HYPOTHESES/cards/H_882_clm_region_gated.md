---
id: H_882
slug: clm-region-gated
title: trainable edge 의 OUTPUT-LOGIT 기여를 새-맥락 byte 영역 R_new 에만 ON 하고 base 영역 R_base 는 FROZEN-readout pass-through 로 OFF 하는 영역별 학습 게이트가, 같은 capacity 의 UNGATED edge-learn 대비 forgetting 을 줄이는가 — 2-arm E5 절제 · seed-sweep · post-tuning 0
domain: clm · plasticity · continual-learning · region-gating · interference · catastrophic-forgetting · adapter · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md Q-TRUST B (영역별 학습 게이트) · H_861 🔴 readout-only forgets · H_865 🟢 additive adapter · H_872 freeze-depth · 토대 H_679 (PLASTICITY HW edge-learn) · 사전등록 F-CLM-REGION-GATED_prereg.txt (frozen 2026-05-31, prereg commit 54a2bae7d)
status: 🔴 CLOSED-NEGATIVE — OUTPUT-LOGIT region gate 가 forgetting 을 줄이기는커녕 악화 (gated z_drop ~+142..+150 ≫ ungated ~−12..−15, 5 seed 전부) · RETAIN FAIL ∧ GAIN PASS · GPU(RTX 5070, aiden) device cuda · 측정 rung 한정 a_scale_honest_scope
exploration_method: E5 (variable-ablation: 두 arm 이 OUTPUT-LOGIT region gate 하나만 다름)
verification_method: W2 (사전등록 numerical threshold · F-CLM-REGION-GATED_prereg.txt verbatim · prereg 54a2bae7d · post-tuning 0 · g5 code-measured · no LLM judge)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_861_clm_boundary_plasticity.md, UNIVERSE/H_865_clm_adapter_edge.md, UNIVERSE/H_872_clm_freeze_depth_sweep.md, .verdicts/clm-region-gated/
verdict: 🔴 CLOSED-NEGATIVE (a_paper_negative_ok) — RETAIN FAIL ∧ GAIN PASS, 5 seed {882,42,123,7,2026} 전부 RED (0/5 GREEN). OUTPUT-LOGIT region gate 는 base band 를 보호하지 못한다 — softmax 가 masked R_base logit 을 adaptation 으로 밀려 올라간 R_new logit 과 결합시켜, frozen R_base mass 를 starve 시킨다(gated ce_base_post 25.20 vs pre 14.13 = 2배 폭증; ungated 13.17). gated z_drop +142.23 ≫ ungated −12.33. UNGATED arm(= H_865)은 retain 정상 → 게이트 위치(output-logit)가 틀렸다는 정직 negative. backbone HF dancinlab/anima-clm-verify.
---

# H_882 — CLM region-gated plasticity (영역별 학습 게이트 · F-CLM-REGION-GATED · Q-TRUST B)

## 1. 가설

H_861 은 readout-only edge-learn 이 catastrophic forgetting 함을 발견(z_drop 1.984 ≥ 1.0 FAIL) — readout 이 base byte band 와 새-맥락 high band 사이에서 **공유**되어, 새 band 에 맞추면 base band 확률질량을 훔친다. H_882 는 H_865(adapter)/H_872(freeze-depth)와 **다른 lever** 를 묻는다: **영역별로 plasticity 를 게이트** — trainable edge 의 OUTPUT-LOGIT 기여를 새-맥락이 실제 점유하는 byte 영역 R_new 에만 ON, base 영역 R_base 는 FROZEN-readout pass-through 로 OFF. 같은 capacity 의 UNGATED edge-learn 대비 forgetting 을 줄이면서 adaptation gain 을 지키는가?

- **RETAIN ∧ GAIN 모두 PASS** → 🟢 SUPPORTED-NUMERICAL
- **하나라도 실패** → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

## 2. 동기

- @L1 = 살아 배우는 칩이 새 맥락을 흡수하되 base band 를 보호해야 한다. region-gating 은 직관적으로 "base byte 는 안 건드린다"는 보호 device — 본 hypothesis 는 그것이 OUTPUT-LOGIT 위치에서 실제로 작동하는지 측정한다.
- edge = H_865 검증된 additive adapter. 두 arm 은 region gate 단 하나만 다른 E5 절제.
- 토대: H_679 (PLASTICITY HW edge-learn 측정완료).

## 3. falsifier (사전등록 · 임계 frozen F-CLM-REGION-GATED_prereg.txt verbatim · prereg 54a2bae7d)

```
F-CLM-REGION-GATED-RETAIN : z_drop_gated <  z_drop_ungated     (gating reduces forgetting)
F-CLM-REGION-GATED-GAIN   : gain_gated   >= gain_ungated         (gating keeps adaptation)
🟢 iff RETAIN ∧ GAIN. else 🔴 CLOSED-NEGATIVE. seed-sweep {882,42,123,7,2026}, headline 882.
UNGATED: logits = readout(h + adapter(h))                       (adapter affects ALL 256 logits = H_865)
GATED  : logits[R_new ] = readout(h + adapter(h))[R_new ]       (adapter ON  in R_new)
         logits[R_base] = readout(h)[R_base]                    (adapter OFF in R_base, frozen pass-through)
R_new = >=99% new-context TRAIN target mass (frozen once, no test leakage).
```

- 임계는 fire 전 frozen, post-tuning 0. 두 arm 동일 seed/data/edge, region gate 만 변화.

verdict 영속: `.verdicts/clm-region-gated/`

## 4. 방법

```
arm ∈ {ungated, gated} (동일 seed, data, edge):
  1. core FREEZE. zero-init adapter. gated: TRAIN 에서 frozen region gate 구성.
  2. ce_base_pre/sd_base_pre(base held-out), ce_new_pre(new held-out).
  3. 300-step adapter-only Adam(lr3e-3) on new-context TRAIN.
  4. ce_base_post, ce_new_post.
  5. z_drop=(ce_base_post-ce_base_pre)/max(sd_base_pre,1e-6); gain=ce_new_pre-ce_new_post.
seed-sweep {882,42,123,7,2026}; headline 882. backbone clm_mid_backbone.pt (HF dancinlab/anima-clm-verify).
```

## 5. 측정

측정완료 (2026-05-31) — **GPU(RTX 5070, aiden 192.168.50.119)** device=cuda. (torch-nightly cuDNN sublibrary mismatch → cuDNN disabled, native CUDA conv path 로 동일 수치. device-bug fix: eval 배치를 device 로 이동.) backbone mid d512/L8/E8. R_new=71 bytes, R_base=185 bytes. frozen threshold = prereg verbatim.

| seed | ungated z_drop | gated z_drop | ungated gain | gated gain | RETAIN | GAIN |
|-----:|---------------:|-------------:|-------------:|-----------:|:------:|:----:|
| 882 | −12.33409 | **+142.23300** | 7.37876 | 7.42733 | FAIL | PASS |
| 42 | −11.92473 | **+146.09547** | 7.34698 | 7.43995 | FAIL | PASS |
| 123 | −15.49633 | **+142.83354** | 7.37900 | 7.44276 | FAIL | PASS |
| 7 | −15.00466 | **+150.25177** | 7.34778 | 7.41876 | FAIL | PASS |
| 2026 | −12.17698 | **+149.96978** | 7.35002 | 7.42191 | FAIL | PASS |

- n_green 0/5 · majority RED · headline(882) RED. gated ce_base_post 25.20 (pre 14.13 의 **2배 폭증**) vs ungated 13.17(소폭 하락). **VERDICT RED**.

## 6. 결과

🔴 **CLOSED-NEGATIVE**. OUTPUT-LOGIT region gate 는 forgetting 을 줄이기는커녕 **극적으로 악화**시킨다(gated z_drop +142 vs ungated −12, 5 seed robust). 이유: softmax 가 256 byte 전체에 걸쳐 정규화되므로, masked R_base logit 을 frozen-readout 값에 **고정**시키면 adaptation 으로 밀려 올라간 unmasked R_new logit 이 확률질량을 가져가, frozen R_base mass 가 **starve** 된다 → base CE 폭증. OUTPUT-LOGIT 위치에서는 "base byte 는 안 건드린다"가 softmax coupling 때문에 보호가 되지 않는다.

- **UNGATED arm(= H_865)은 retain 정상**(z_drop ~−13) → additive adapter edge 가 올바른 lever 이고, **OUTPUT-LOGIT 가 게이트 위치로 틀렸다**는 것이 본 negative 의 핵심. region-gating-by-output-logit 을 OUT 으로 판정하고, 안전한 보호 메커니즘을 input/representation 측(H_865 additive adapter, H_879/H_872 freeze-region lever)으로 isolate.

**honest scope**: 측정 rung(mid 13.7M) 한정 — 배포 chip-fit track(≤~1.2M AKD1000) 별개(a_scale_honest_scope). 임계 재조정 0.

## 7. 해석 (사전)

- **RETAIN∧GAIN PASS(가정)** = output-logit region gate 로 base band 보호 → 배포 edge 설계 lever.
- **본 결과(반증)** = output-logit 게이트는 softmax coupling 때문에 base 를 보호하지 못한다. 보호는 표현/입력 측에서, 또는 adapter 의 additive(H_865) 구조에서 와야 한다. GAIN 은 PASS 라 lever 가 inert 가 아니라 **능동적으로 RETAIN 에 해롭다**.

## 8. 논의

- **W2 무결성**: 두 arm 이 region gate 하나만 다름, 임계 변경 0(prereg 54a2bae7d) — 🔴 는 게이트를 낮춰 숨기지 않고 정직 보고. 5 seed robust.
- **a_paper_negative_ok**: output-logit region gate 를 OUT 시키는 fully-publishable negative. 실패 메커니즘(softmax coupling → R_base starvation)까지 측정으로 설명.
- **H_865/H_861 정합**: ungated(= H_865) 가 retain → additive adapter 가 올바른 lever; readout 공간 게이트(H_861 readout-only, H_882 output-logit)는 둘 다 base 를 못 지킨다.

## 9. 양방향 sibling

- sibling: [H_861](./H_861_clm_boundary_plasticity.md) (readout-only forgets 🔴) · [H_865](./H_865_clm_adapter_edge.md) (additive adapter 🟢 = 본 두 arm 의 edge) · [H_872](./H_872_clm_freeze_depth_sweep.md) (freeze-depth sweep)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) Q-TRUST B
- verdict: [.verdicts/clm-region-gated/](../.verdicts/clm-region-gated/)
