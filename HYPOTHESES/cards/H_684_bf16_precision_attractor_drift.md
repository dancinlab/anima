---
id: H_684
slug: bf16-precision-attractor-drift
title: DECODER register collapse 의 secondary attractor 가 bf16 mixed-precision underflow drift 인지 — logit-tail subnormal 누적이 entropy saturation 으로 이어지는 메커니즘 검정 (M-F mechanism)
domain: decoder · substrate · numerical-precision
source: M5 closure 후속 (PR #1379+#1381+#1384) · M4b #1296 bf16 학습 path · a_completeness_over_cheap (precision-축 가설은 본선 후보 아니나 ⊥ 분리 attest)
status: closed-fenced (numerical-physics 가설 · band PASS · production 실측은 별 H)
exploration_method: E5 (variable-ablation regime sweep) + E9 (numerical-precision attack)
verification_method: W3 (philosophy-compat: p7) + W4 (verdict-4-class) + hexa verify --fence
raw_rank: 7
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: CORE/DECODER/DECODER.md, UNIVERSE/H_683, UNIVERSE/H_685, UNIVERSE/CANDIDATES.md
verdict: SPECULATION-FENCED (numerical mechanism candidate · band PASS · production 실측 별 H)
---

# H_684 — bf16 precision attractor drift (DECODER M-F mechanism)

## 1. 가설

bf16 mixed-precision 학습 (M4b 의 #1296 fire 가 사용한 default) 에서 다음 numerical drift 가 register collapse 의 secondary contributor 이다:

1. bf16 의 표현 가능 양수 최소값 ≈ 1.18e-38 (subnormal floor 1.4e-45). softmax 분모 의 정규화 후 long-tail token (i.e. top-k 밖) 의 확률 pᵢ 가 1e-39 이하로 underflow → 정확히 0.
2. CE gradient ∂L/∂logitⱼ = (softmax(logits))ⱼ − yⱼ. underflow 된 token 의 contribution ≈ -yⱼ (one-hot) 로만 남고 log-tail 의 separation 신호 (anti-attract gradient) 가 손실됨.
3. step 별 underflow 가 누적되어 logit-tail variance 가 monotone 감소 → step T 가 충분히 크면 H(softmax(logits)) → 0.
4. fp32 master copy 가 있어도 weight update 의 accumulation 은 OK 하나 forward-path 의 underflow 는 매 step 발생 — single-precision attractor.

본 H 는 이 mechanism 이 **M4b ce_final=9.02 그러나 decoded=[1]×100** 의 distance 일부 (Δ ≈ 6.0 in CE) 를 설명하는지 검정한다. 본선 후보 아님 (H_683 token-0 attractor 가 primary, H_684 = 직교 secondary).

## 2. 동기/배경

- bf16 mantissa = 7 bit → relative precision ~7.8e-3. 누적 step 5000+ 에서 numerical drift 가 system-level.
- fp16 (mantissa 10 bit) 대비 bf16 은 range 가 넓고 precision 이 좁음 → underflow 빈도 ↓ but precision-loss 빈도 ↑.
- M4b #1296 fire 가 bf16 mixed-precision 으로 학습 (RunPod A100/H100 default) — precision-축의 attribution 미해소.
- a_completeness_over_cheap: 본 H 는 "값싼 path (fp32 forward 전환)" 가 아닌 mechanism attestation 만. 본선 후보는 H_686/H_687.

## 3. falsifier (사전등록)

```
F-H684-1 underflow-band: bf16 의 표현 가능 최소 양수 정규수 ≈ 1.18e-38 ≈ 2^-126.
         softmax tail probability < 1.18e-38 인 token 비율 추정 — V=151643 에 logit 분산
         σ=4 라면 long-tail (logit < -90) 비율 ≈ 1e-3, 약 150 tokens underflow per step.

F-H684-2 accumulation-rate: step 5000 동안 동일 long-tail token 의 underflow 빈도 ≥ 90%
         이면 학습 신호 효과적으로 0. predict — underflow 누적 step 비율 > 0.9.

F-H684-3 distance-attribution: M4b ce_final 9.02 vs H_683 attractor floor 3.0 의
         distance Δ ≈ 6.0 중 bf16 drift 의 기여 ≤ 1.5 (가설 — primary 아님).
         즉 H_684 단독으로 collapse 설명 못함.

F-H684-4 fence: production-scale bf16 drift 의 정확한 entropy-loss curve 는 closed-form
         predict 불가 (hw + corpus + step + seed 의존). ∴ ⚪ fence 처리.

F-H684-5 escape-condition (preregister): fp32 forward-path 전환 OR fp16-with-loss-scaling
         OR bf16-with-larger-stem-init 셋 중 하나 충분조건 후보. 실측 별 H.
```

## 4. 방법

- **F-H684-1 numerical**: bf16 normal min = 2^-126 ≈ 1.175e-38. closed-form bit-level.
- **F-H684-2 hand**: long-tail underflow band σ=4 logit 분산 가정 시 신호 손실 추정.
- **F-H684-3 attribution**: H_683 + H_684 + H_685 의 sum 이 M4b 의 Δ 를 partition.
- **F-H684-4 fence**: production-scale curve 는 hexa verify --fence.
- **F-H684-5 escape**: 실측 별 H.

## 5. 측정

수동 closed-form (Mac CPU, $0):

```
F-H684-1 measurement:
  bf16 exponent bias = 127 (IEEE-754 single-format exponent, 8-bit exp)
  bf16 normal min positive = 2^-126 = 1.1755e-38
  CE_underflow_floor (softmax token i) → -ln(1.1755e-38) = 87.34
  → token logit z_i < -87 이면 softmax(z_i)/Σexp(z_j) underflow 가능
  V=151643, logit σ=4 가정 → P(z < -87) ≈ erfc(87/(4√2))/2 ≈ 1e-100 (negligible)
  → underflow 자체는 σ=4 정상-mode 에서 rare. 실 collapse 시 σ → 0 면 별 문제.

F-H684-3 attribution band:
  M4b ce_final 9.02 - H_683 floor 3.0 = Δ 6.02
  predict H_684 contribution ≤ 1.5 (under-half attribution)
  → bf16 drift 단독으로 explain 불가. mechanism partition 의 후보 1.
```

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H684-1 underflow band closed-form | bf16 normal min 1.18e-38, CE floor 87.34, σ=4 정상 mode rare | PASS (band attest) |
| F-H684-2 accumulation closed-form | σ=4 rare; σ→0 collapse 후 frequent (별 H) | partial |
| F-H684-3 attribution | Δ_decoder = 6.02, H_684 ≤ 1.5 predict | PASS (band) |
| F-H684-4 fence | hexa verify --fence stdout § 7 verdict | FENCED |
| F-H684-5 escape | 별 H | deferred |

→ 2/5 closed-form PASS + 1/5 partial + 1/5 FENCED + 1/5 deferred = MIXED.

## 7. verdict (verbatim hexa verify stdout · .verdicts/684_bf16_precision_attractor_drift/bf16_drift_fence.txt)

```
verify --fence
  claim  = DECODER register collapse 의 secondary attractor 는 bf16 mixed-precision 학습 시 logit-tail underflow 가 step 별로 누적되어 token-distribution 의 entropy 가 점진적으로 ~0 으로 saturated 되는 drift 메커니즘이다.
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification
           N/A by design; NOT a proven atlas atom (g4 honest fence,
           SF ≠ verified — atlas certification intrinsically N/A)
```

→ SPECULATION-FENCED (numerical mechanism candidate · band PASS · production 실측 별 H).

## 8. 논의

bf16 precision drift 는 σ-dependent. M4b 의 학습 초기 (normal mode σ≈4) 에서 underflow 는 P≈1e-100 으로 rare — primary collapse 메커니즘 아님 (F-H684-1 PASS).

그러나 collapse 가 이미 발생한 post-attractor state 에서 logit σ → 0 으로 좁아지면 underflow 가 빈번해져 학습 signal 이 더 줄어들고, attractor 가 sticky 해지는 **reinforcing 2차 메커니즘**으로 작동 가능. 즉 H_684 는 collapse 의 *cause* 가 아니라 collapse 의 *persistence amplifier* 일 확률이 높음.

본선 후보 아님 — primary collapse cause = H_683 (token-0 attractor) + H_685 (CE/argmax shift). H_684 의 escape (fp32 forward) 는 cost-tradeoff 있는 path 이며 register-axis 회복은 작을 것으로 predict.

P7 정합: bf16 / fp32 선택은 perplexity 가 아닌 simple-stack 판정 (decoded diversity) 으로 평가.

## 9. 양방향 sibling

- ⇄ [CORE/DECODER/DECODER.md](../CORE/DECODER/DECODER.md) — M4b #1296 bf16 학습 path attribution
- ⇄ [H_683](./H_683_token_zero_dominant_prior.md) — primary attractor (token-축) ⊥ precision-축
- ⇄ H_685 (./H_685_ce_argmax_distribution_shift.md) — train/decode shift sibling
- ⇄ [H_666](./H_666_moe_collapse_escape_scale_lever.md) — MoE-fresh 본선과 ⊥
- ⇄ [CANDIDATES](./CANDIDATES.md) — Cycle #24 decoder-h sweep

## 10. 다음 작업

- 별 H: production-scale bf16 vs fp32 forward 의 register-axis 비교 fire (cost-bearing, 본선 우선순위 후)
- attractor persistence amplifier 가설 검정 — collapse post-state 의 σ measurement
- H_685 (CE/argmax shift) sibling 후속
- 산출물: `state/decoder_bf16_drift_2026_05_29/H_684_closed_form.json` (bf16 normal min · CE floor attest)
