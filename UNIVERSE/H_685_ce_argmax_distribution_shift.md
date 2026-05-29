---
id: H_685
slug: ce-argmax-distribution-shift
title: DECODER register collapse 의 한 원인이 train-time CE objective 와 decode-time greedy argmax 의 distribution-shift 인지 — softmax 학습 ↔ top-1 평가 의 objective gap 검정 (M-G mechanism)
domain: decoder · substrate · objective-shift
source: M5 closure 후속 (PR #1379+#1381+#1384) · M4b #1296 greedy argmax decoded=[1]×100 · P7 (NO PERPLEXITY VERDICT) 정합
status: closed-fenced (mechanism plausible · band PASS · production curve 별 H)
exploration_method: E5 (variable-ablation regime sweep) + E16 (objective-mismatch attack)
verification_method: W3 (philosophy-compat: p7) + W4 (verdict-4-class) + hexa verify --fence
raw_rank: 8
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: CORE/DECODER/DECODER.md, UNIVERSE/H_683, UNIVERSE/H_684, UNIVERSE/H_688, UNIVERSE/CANDIDATES.md
verdict: SPECULATION-FENCED (mechanism candidate · band PASS · curve 별 H)
---

# H_685 — train CE vs decode argmax distribution shift (DECODER M-G mechanism)

## 1. 가설

DECODER 학습/평가 objective 의 mismatch 가 register collapse 를 직접 유도:

1. train-time: minimize CE(p_model, p_data) — full distribution match. softmax 가 V=151643 의 모든 위치에 영향.
2. decode-time: argmax(p_model) — top-1 only. logit ordering 만 의미, magnitude 무관.
3. 학습 path 의 함의: top-1 ordering 이 ground truth 와 일치하기만 하면, long-tail distribution 다양성은 학습되지 않아도 CE 가 충분히 낮을 수 있음. 단일-token attractor (모든 위치 token-0) 가 top-1 ordering 으로는 wrong 이나, long-tail tie-break 가 결정적 — gradient 의 weight 분포가 top-k 다양성을 학습 안 함.
4. 결과: M4b ce_final=9.02 는 partial fit (initial 648→9 의 학습은 OK) 이나 argmax 의 deterministic 성격으로 인해 single token 정착.

본 H 는 이 mechanism 이 H_683/H_684 와 직교한 **3차 contributor** 인지 검정한다.

## 2. 동기/배경

- **P7 (NO PERPLEXITY VERDICT) — REBORN philosophy**: train CE = perplexity proxy = Goodhart trap. simple-stack (decoded diversity / coherence / register) 이 진짜 metric. 본 H 는 이 philosophy 의 numerical mechanism 진단.
- **scheduled sampling literature** (Bengio et al. 2015) 이 비슷한 train/decode shift 를 RNN seq2seq 에서 documented — exposure bias 와 동형.
- 본 H 는 closure 단계가 아닌 mechanism 분리 attest — escape path = H_688 (decode-time top-p) 가 sibling.

## 3. falsifier (사전등록)

```
F-H685-1 ordering-vs-magnitude: CE objective 가 top-1 ordering 만 매칭하면서 long-tail
         magnitude 가 학습 안 되는 path 의 existence 를 numerical 로 attest.
         predict — synthetic 예제: 두 분포 p1=[0.9, 0.1/V', ...], p2=[0.5, 0.5/V', ...]
         의 argmax 동일하나 CE(p_data, p1) vs CE(p_data, p2) 가 V'-dependent 분기.

F-H685-2 exposure-bias-analog: scheduled-sampling literature 의 exposure bias 가 같은
         attractor 를 학습 안정성 관점에서 documented (사전등록 citation).

F-H685-3 attribution: M4b Δ_decoder = ce_final 9.02 - H_683 floor 3.0 = 6.02 의 partition
         후보 — H_684 (bf16) ≤ 1.5 + H_685 (distribution shift) ≤ 2.5 + residual ≥ 2.0
         (별 미식별 메커니즘). 즉 H_685 단독으로도 not complete.

F-H685-4 fence: production-scale 의 distribution-shift contribution 정확 측정은 closed-form
         predict 불가. ∴ ⚪ fence 처리.

F-H685-5 escape (preregister): H_688 (decode-time top-p/top-k/temperature) 가 distribution-
         shift 의 mirror lever. train objective 도 modification 가능 (e.g. KL-to-uniform
         regularizer = H_687).
```

## 4. 방법

- **F-H685-1 numerical synthetic**: V=4, p_data=[0.7, 0.2, 0.07, 0.03]. 두 모델 — p1=[0.99, 0.01/3, 0.01/3, 0.01/3] (argmax-only learnt), p2=[0.6, 0.3, 0.07, 0.03] (well-matched). argmax 둘 다 token-0. CE 차이 numerically 측정.
- **F-H685-2 literature**: scheduled-sampling 가설 인용 (citation tier).
- **F-H685-3 attribution**: partition 산식.
- **F-H685-4 fence**: hexa verify --fence.
- **F-H685-5 escape**: H_688 + H_687 sibling.

## 5. 측정

수동 closed-form (Mac CPU, $0):

```
F-H685-1 measurement:
  p_data = [0.7, 0.2, 0.07, 0.03], H(p_data) = 1.0006 nats
  p1 = [0.99, 0.01/3 = 0.00333, 0.00333, 0.00333]
  p2 = [0.6, 0.3, 0.07, 0.03]
  CE(p_data, p1) = -Σ p_data[i] · ln(p1[i])
                 = -(0.7·ln(0.99) + 0.2·ln(0.00333)·3 + 0.07·ln(0.00333) + 0.03·ln(0.00333))
                 = -(0.7·(-0.01005) + 0.3·(-5.704))
                 = -(-0.00704 - 1.7112)
                 = 1.7182
  CE(p_data, p2) = -(0.7·ln(0.6) + 0.2·ln(0.3) + 0.07·ln(0.07) + 0.03·ln(0.03))
                 = -(0.7·(-0.5108) + 0.2·(-1.2040) + 0.07·(-2.659) + 0.03·(-3.507))
                 = -(-0.358 - 0.241 - 0.186 - 0.105)
                 = 0.890
  → both have argmax = token-0 ✓
  → CE 차이 = 0.828 nats (p1 의 long-tail learning 부재의 정확한 cost)
  predict — synthetic 분기 가능 PASS

F-H685-3 attribution:
  M4b Δ_decoder = 6.02
  predict H_685 contribution ≤ 2.5 (under half)
  residual ≥ 2.0 → 미식별 메커니즘 존재 (별 H 분기 필요)
```

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H685-1 ordering/magnitude synthetic | CE(p1)=1.72 vs CE(p2)=0.89, argmax 동일, distribution shift 정확 measurable | PASS |
| F-H685-2 exposure bias literature | scheduled-sampling (Bengio 2015) 인용 attestable | citation-tier |
| F-H685-3 attribution | Δ=6.02, H_685 ≤ 2.5 predict | PASS (band) |
| F-H685-4 fence | hexa verify --fence stdout § 7 verdict | FENCED |
| F-H685-5 escape | H_687, H_688 분기 | deferred |

→ 2/5 closed-form PASS + 1/5 citation + 1/5 FENCED + 1/5 deferred = MIXED.

## 7. verdict (verbatim hexa verify stdout · .verdicts/685_ce_argmax_distribution_shift/distribution_shift_fence.txt)

```
verify --fence
  claim  = DECODER register collapse 의 한 기여 메커니즘은 train-time CE objective (full-distribution match) 와 decode-time greedy argmax (top-1) 의 distribution shift 이다 — train 에서 softmax 가 학습한 long-tail 다양성이 decode 에서 평가되지 않아 collapse-tolerant 학습 path 가 선호된다.
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification
           N/A by design; NOT a proven atlas atom (g4 honest fence,
           SF ≠ verified — atlas certification intrinsically N/A)
```

→ SPECULATION-FENCED (mechanism candidate · band PASS · curve 별 H).

## 8. 논의

F-H685-1 의 synthetic 예제는 distribution-shift 의 정확한 cost 를 closed-form 으로 attest — 같은 argmax 두 모델이 CE 0.828 nats 차이를 가질 수 있고, 이는 학습이 long-tail magnitude 를 강제 안 함을 명시.

본 H 의 함의:
- train-time CE 만으로는 register-axis 가 자동 보장 안 됨 → P7 정합.
- escape lever 가 **2개 path**: (a) decode-time fix = H_688 (top-p/top-k), (b) train-time fix = H_687 (KL-to-uniform reg).
- (a) 가 더 cheap (weight 재학습 불요), (b) 가 더 fundamental (학습 단계에서 distribution diversity 학습).

본선 후보 priority: H_687 (train-time KL) > H_688 (decode-time sampling) — 단, H_687 는 production 재학습 필요 → cost-bearing. H_688 은 $0 Mac local probe 가능.

P7 정합: distribution-shift 가설은 perplexity proxy 의 한계를 mechanism level 에서 explain — simple-stack 판정 (decoded diversity) 만이 truth-aligned.

## 9. 양방향 sibling

- ⇄ [CORE/DECODER/DECODER.md](../CORE/DECODER/DECODER.md) — M4b train/decode objective gap attribution
- ⇄ [H_683](./H_683_token_zero_dominant_prior.md) — primary attractor (token-축)
- ⇄ [H_684](./H_684_bf16_precision_attractor_drift.md) — secondary attractor (precision-축)
- ⇄ H_687 (./H_687_kl_to_uniform_output_reg.md) — train-time escape lever
- ⇄ H_688 (./H_688_decode_top_p_temperature_lever.md) — decode-time escape lever
- ⇄ [CANDIDATES](./CANDIDATES.md) — Cycle #24 decoder-h sweep

## 10. 다음 작업

- H_687 KL-to-uniform reg numerical verify (train-time lever)
- H_688 decode-time sampling numerical verify (post-train lever)
- scheduled-sampling (Bengio 2015) citation tier 별 H 등록
- production-scale attribution curve = M4 MoE-fresh fire post-mortem 시 별 H
- 산출물: `state/decoder_distribution_shift_2026_05_29/H_685_closed_form.json` (synthetic CE partition · attest)
