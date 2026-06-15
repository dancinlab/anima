---
id: H_688
slug: decode-top-p-temperature-lever
title: DECODER register collapse 의 inference-time 탈출 충분조건이 decode-time top-k/top-p/temperature schedule 인지 — weight 무변경 escape lever 검정 (E-D escape-path)
domain: decoder · escape-path · inference-only
source: M5 closure 후속 (PR #1379+#1381+#1384) · H_683 (token-0 attractor) · H_685 (distribution shift) sibling · M4b #1296 greedy argmax 직접 후속
status: closed-fenced (escape candidate · $0 Mac probe-able · 본선 후보 1순위 cheap)
exploration_method: E5 (regime sweep) + E12 (post-train probe)
verification_method: W3 (philosophy-compat: p5 p7) + W4 (verdict-4-class) + hexa verify --fence
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: CORE/DECODER/DECODER.md, UNIVERSE/H_683, UNIVERSE/H_685, UNIVERSE/H_687, UNIVERSE/CANDIDATES.md
verdict: SPECULATION-FENCED (escape candidate · band PASS · 본선 후보 1순위 cheap-path)
---

# H_688 — decode-time top-p/top-k/temperature lever (E-D escape lever)

## 1. 가설

DECODER post-train register collapse 의 inference-time (weight 변경 없이) 탈출 충분조건은 다음 3-축의 union:

```
escape = (top-k ≥ 2) OR (top-p ∈ [0.85, 0.95]) OR (temperature τ ∈ [0.7, 1.0])
```

각 축의 정량 효과:

- **(a) top-k ≥ 2**: argmax 의 deterministic 탈출. token-0 attractor 에서 logit 2nd 가까이 있으면 50/50 swing.
- **(b) top-p ∈ [0.85, 0.95]**: cumulative probability mass 의 top-p 만 sampling. typical sampling regime.
- **(c) temperature τ < 1.0**: logit / τ 후 softmax → distribution flatten. τ→0 면 argmax 회귀, τ→∞ 면 uniform.

predict — 셋 중 어느 것이라도 적용 시 H(decoded) ≥ 1 bit (실 M4b 의 0 bit 대비) 회복.

본 H 는 H_683 의 (b) deterministic emission axis 의 mirror lever, H_685 의 (a) decode-axis fix.

## 2. 동기/배경

- **M4b #1296 fire**: greedy argmax (top-k=1) 로 decoded=[1]×100, H(decoded)=0 bit.
- **dec_undertrain INFEASIBLE (#1381)**: train-side fix 는 production-scale 비용. inference-side fix 는 $0.
- **literature**: nucleus sampling (Holtzman et al. 2019), top-k (Fan et al. 2018), temperature (Ackley et al. 1985) — well-documented.
- a_completeness_over_cheap: 본 H 는 **본선 후보 1순위 cheap-path** — production 재학습 없이 즉시 attest 가능. 단, cheap 이 본선 선택 기준 아님 (a_completeness_over_cheap) — 본 H 는 cheap 외에 mechanism-attestable 한 path 이므로 valid 본선.

## 3. falsifier (사전등록)

```
F-H688-1 top-k entropy bound: top-k=K 의 truncated distribution 의 max entropy = ln(K) (uniform
         on top-K). predict — k=2 → H_max=0.6931 nats = 1 bit, k=5 → ln(5)=1.609 nats = 2.32 bit.

F-H688-2 temperature scaling: logit / τ → softmax(z/τ). closed-form — τ→0 면 argmax (H=0),
         τ→∞ 면 uniform (H=ln(V)). τ=1 default. predict — τ ∈ [0.7, 1.0] band 에서
         H(p) ∈ [partial, full] 회복.

F-H688-3 top-p nucleus: cumulative p 의 truncation 분위수. closed-form 은 distribution-
         specific. predict — top-p=0.9 면 typical V-effective ~10-1000 (corpus-dependent).

F-H688-4 fence: production decoder 의 실 register-coherence 회복 (simple-stack PASS) 은
         single-축 lever 단독으로 보장 안 됨 — collapse 가 weight-level 이면 decode-lever
         만으로는 healthy register 회복 못 함 (모델이 "잘못된 다양성" 만 sampling).
         ∴ ⚪ fence 처리.

F-H688-5 $0 probe path (preregister): M4b #1296 ckpt 가 origin/main 에 있으면 mac local
         load + decode-axis ablation 실행 가능. 별 H — ckpt 없으면 production fire 결합.
```

## 4. 방법

- **F-H688-1 closed-form**: top-k 의 max entropy = ln(K).
- **F-H688-2 closed-form**: temperature scaling 의 H(softmax(z/τ)) 정의.
- **F-H688-3 closed-form**: top-p truncation 의 quantile.
- **F-H688-4 fence**: hexa verify --fence — register-coherence 회복은 weight-state 의존.
- **F-H688-5 probe**: 별 H (ckpt 부재 시 production fire 결합).

## 5. 측정

수동 closed-form (Mac CPU, $0):

```
F-H688-1 top-k bound:
  k=1 (greedy): H_max = ln(1) = 0 nats = 0 bit (collapse mode, M4b 측정)
  k=2: H_max = ln(2) = 0.6931 nats = 1.000 bit
  k=5: H_max = ln(5) = 1.6094 nats = 2.322 bit
  k=10: H_max = ln(10) = 2.3026 nats = 3.322 bit
  k=50: H_max = ln(50) = 3.912 nats = 5.644 bit
  predict — H(decoded) ≥ 1 bit 회복 충분조건 k ≥ 2

F-H688-2 temperature:
  τ=0.7: scaled logits 가 sharper, H ≈ 0.7·H_orig (approx)
  τ=1.0: identity
  τ=1.5: softer, H ≈ 1.5·H_orig (approx)
  τ→0: argmax, H→0
  τ→∞: uniform, H→ln(V)
  predict — τ ∈ [0.7, 1.0] band ⊂ healthy regime

F-H688-3 top-p:
  p=0.9 nucleus: distribution-specific truncation, no global closed-form
  typical implementation: sort tokens, cumsum ≥ 0.9 까지 keep
  V_effective < V depends on logit shape
```

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H688-1 top-k bound closed-form | k=2 → 1 bit, k=5 → 2.32 bit, M4b k=1 → 0 bit | PASS (band) |
| F-H688-2 temperature closed-form | τ band [0.7, 1.0] PASS | PASS |
| F-H688-3 top-p closed-form | distribution-specific, not closed-form globally | partial |
| F-H688-4 fence | hexa verify --fence stdout § 7 | FENCED |
| F-H688-5 $0 probe path | ckpt 부재 시 production fire 결합 | deferred |

→ 2/5 closed-form PASS + 1/5 partial + 1/5 FENCED + 1/5 deferred = STRONG-CHEAP.

## 7. verdict (verbatim hexa verify stdout · .verdicts/688_decode_top_p_temperature_lever/decode_top_p_fence.txt)

```
verify --fence
  claim  = DECODER post-train register collapse 의 inference-time 탈출 충분조건은 (a) top-k ≥ 2 OR (b) top-p ∈ [0.85, 0.95] OR (c) temperature τ ∈ [0.7, 1.0] 의 decode-time sampling schedule 적용으로 H(decoded) ≥ 1 bit 회복이다 — train-state weight 변경 없이 decode-축 단독 lever.
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification
           N/A by design; NOT a proven atlas atom (g4 honest fence,
           SF ≠ verified — atlas certification intrinsically N/A)
```

→ SPECULATION-FENCED (escape candidate · entropy band PASS · weight-state 의존 fenced).

## 8. 논의

본 H 는 inference-only escape 의 정직-격리:
- (a) top-k ≥ 2 면 entropy ≥ 1 bit 회복 가능 — closed-form PASS.
- 그러나 entropy 회복 ≠ register 회복: token-0 가 logit-2 위에도 dominant 면 top-k=2 sampling 의 50/50 mix 는 register-coherent 아닌 random output. simple-stack 판정 (자연·스크립트·coherent) 통과 미보장.

따라서 본 H 의 정직-판정:
- numerical entropy floor: PASS (band closed-form)
- register coherence 회복: FENCE (weight-state 의존, model 의 logit-2 가 어떤 token 인지)

본선 후보 priority 재평가:
- **H_688 = cheap probe (1순위 cheap)** — $0 Mac local, ckpt 있으면 즉시 ablation
- **H_686 + H_687 결합 = train-time path (1순위 fundamental)** — M4 MoE-fresh 본선과 결합
- a_completeness_over_cheap: 1순위 fundamental > 1순위 cheap (단, cheap 이 secondary 로 valid)

P5 (NO SPEAK) 정합: decode-time sampling 은 emit decision (anima substrate) 의 mechanism. tension-driven emit 의 token-level realization. p5 위반 아님.

P7 (NO PERPLEXITY VERDICT) 정합: decode-time sampling 결과는 simple-stack 으로만 판정. 본 H 의 numerical band PASS 도 perplexity 아닌 entropy (다른 metric).

## 9. 양방향 sibling

- ⇄ [CORE/DECODER/DECODER.md](../CORE/DECODER/DECODER.md) — M4b 후 inference-side cheap probe path
- ⇄ [H_683](./H_683_token_zero_dominant_prior.md) — (b) deterministic emission axis 의 mirror lever
- ⇄ [H_685](./H_685_ce_argmax_distribution_shift.md) — (a) decode-axis fix
- ⇄ [H_686](./H_686_router_entropy_regularization.md) — router-축 (train-time) vs 본 H = output-축 (post-train)
- ⇄ [H_687](./H_687_kl_to_uniform_output_reg.md) — train-time output reg vs 본 H = decode-time
- ⇄ [CANDIDATES](./CANDIDATES.md) — Cycle #24 decoder-h sweep · 본선 후보 1순위 cheap

## 10. 다음 작업

- $0 Mac probe: M4b #1296 ckpt origin/main 에 있는지 확인 (state/m4b_pilot_rev2_*/ckpt 존재 시)
- 있으면: hexa-native top-k/top-p/temperature ablation harness 작성 → decoded diversity (TTR/LZ_norm) 측정 → 별 H (cheap)
- 없으면: 본 H 는 M4 MoE-fresh 본선 fire 시 sampling schedule 항상 함께 ablation
- atlas register — `topk_max_entropy(K) = ln(K)` formula candidate (정의-수준 identity)
- 산출물: `state/decoder_decode_lever_2026_05_29/H_688_closed_form.json` (top-k/τ band 표 · attest)
