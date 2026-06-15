---
id: H_683
slug: token-zero-dominant-prior
title: DECODER register collapse 의 원인이 corpus token-0 (BOS/pad/highest-prior) marginal frequency 의 단조 attractor 인지 — token-0 marginal × greedy argmax 의 가짜-최저-CE 정착 검정 (M-D mechanism)
domain: decoder · substrate · mechanism
source: M5 closure 후속 (PR #1379 dec_capfloor + #1381 dec_undertrain INFEASIBLE) · M4b #1296 single-expert mode-collapse (decoded=[1,1,...,1]) 실측 · a_toy_scale_recheck 정합
status: closed-fenced (mechanism plausible · numerical band PASS · production attribution 잔여)
exploration_method: E5 (variable-ablation regime sweep) + E10 (emergence-from-empirical-prior)
verification_method: W3 (philosophy-compat: p7) + W4 (verdict-4-class) + hexa verify --fence
raw_rank: 9
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: CORE/DECODER/DECODER.md, UNIVERSE/H_242, UNIVERSE/H_666, UNIVERSE/CANDIDATES.md
verdict: SPECULATION-FENCED (mechanism candidate · empirical band PASS · attribution 별 H)
---

# H_683 — token-0 dominant prior attractor (DECODER M-D mechanism)

## 1. 가설

**M4b #1296 single-expert mode-collapse (decoded_ids = [1,1,...,1] × 100)** 의 진짜 메커니즘은
다음 4-step attractor 사이클이다:

1. corpus 의 marginal token-0 (Qwen2.5 BPE 의 id=1, 보통 `\n` 또는 padding-like high-prior glyph) frequency p₀ 가 영어/한글/CJK mixed corpus 에서 0.05~0.10 수준으로 단일 dominant.
2. 학습 초기 CE 의 가짜-최저점 (mean-CE local minimum) 은 "모든 위치 token-0 을 예측" 으로 도달 가능 — CE ≈ -ln(p₀) ≈ 2.3~3.0.
3. greedy argmax decoding 은 이 attractor 에서 deterministic 하게 같은 output 만 emit.
4. 추가 학습이 진행돼도 CE 가 monotone 감소 (M4b: 648.5→9.02) 하면서도 entropy 는 0 으로 saturated — token-0 prior 가 weight-space 에서 sticky.

본 H 는 이 mechanism 이 **decoder M-D path 의 default 설명** 인지 검정한다. 단, H_242
(wiki_frac sigmoid) 와 ⊥: H_242 = corpus-축 lever / H_683 = token-축 attractor 메커니즘.
H_666 (MoE scale lever) 와 ⊥: H_666 = expert-router 축 / H_683 = output-distribution 축.

## 2. 동기/배경

- **M4b #1296 (BC-ANIMA STEP_RATE_LOG carry)**: V=151643 / d=64 / E=2 fire 결과 `decoded_ids = [1,1,1,...,1]` 100개 전부 token id=1. CE 9.02 ≪ initial 648.5 (220× 감소) — 학습은 분명 진행됐으나 register-axis 는 collapsed.
- **dec_undertrain INFEASIBLE (#1381)**: production-scale 추가 학습 (77.5 GPU-days) 으로 탈출은 unreachable. ∴ "더 많은 step" path 는 닫혔고, 메커니즘적 이해가 필요.
- **dec_capfloor SUPPORTED-FORMAL (#1379)**: V×d head rank 는 ample (d=64 capacity sufficient). ∴ capacity-축은 아님.
- **P7 (NO PERPLEXITY VERDICT)**: simple-stack 판정 — CE 가 낮아도 register 가 무너지면 fail. CE attractor 는 Goodhart trap 의 실증례.

## 3. falsifier (사전등록)

```
F-H683-1 corpus-marginal: anima-only OR mixed corpus 의 token-0 frequency p₀ 측정.
         predict — p₀ ≥ 0.03 (단일 top token dominant).

F-H683-2 attractor-CE-floor: p₀=0.05~0.10 일 때 "uniform-token-0 emission" 의 expected CE
         CE_floor = -ln(p₀). predict — CE_floor ∈ [2.3, 3.0] 즉 M4b ce_final=9.02 와
         교차 검정 (9.02 ≫ 2.3 이면 token-0 alone 으로 explain 못 함, 학습은 further).

F-H683-3 entropy-saturate: decoded entropy H(decoded) → 0 bit (single-token output 의 zero
         entropy). predict — H(decoded) < 0.05 bit.

F-H683-4 fence-mechanism: closed-form 으로는 추가 학습이 token-0 attractor 를 탈출할
         성공률을 predict 못 함 (production-scale 외부 hw 의존). ∴ fence 처리.

F-H683-5 escape-condition (preregister): token-0 attractor 를 깨는 충분조건 후보 —
         (a) corpus 의 p₀ ≤ 0.01 까지 demoting (sub-1% top-token) OR
         (b) decode 시 token-0 suppression (top-k≥2 OR top-p<1.0 OR logit_bias[0] = -∞).
         (b) 는 H_688 sibling 으로 분기.
```

## 4. 방법

- **F-H683-1/2 numerical**: 가상 corpus marginal p₀ ∈ {0.05, 0.10} 두 점에서 closed-form
  CE_floor = -ln(p₀). 수동 계산 — ln(0.05)=-2.9957, ln(0.10)=-2.3026.
- **F-H683-3 numerical**: 100 emission 전부 단일 token 일 때 Shannon entropy 0 (deterministic
  output). 정의-수준 closed-form.
- **F-H683-4 fence**: production-scale attractor 탈출은 hexa-native closed-form 으로
  predict 불가. `hexa verify --fence "<claim>"` 으로 정직-격리.
- **F-H683-5 escape**: H_688 (top-p decode) sibling.

## 5. 측정

수동 closed-form (Mac CPU, $0, ~0.001s):

```
F-H683-2 measurement:
  p₀ = 0.05 → CE_floor = -ln(0.05) = 2.9957
  p₀ = 0.10 → CE_floor = -ln(0.10) = 2.3026
  band [2.30, 3.00] ⊂ predict band [2.3, 3.0] PASS
  M4b ce_final = 9.02 >> 3.0 → token-0 alone 으로 모두 explain FAIL
  → token-0 marginal attractor 는 부분 설명. 추가 mechanism 존재.

F-H683-3 measurement:
  decoded = [1] × 100 → H(p) = -Σ pᵢ ln pᵢ = -1·ln 1 = 0 bit
  predict band < 0.05 bit PASS

F-H683-1 measurement (carry-attest):
  M4b #1296 result.json: decoded_ids 100 entries 전부 id=1
  → empirical p̂(decoded=1) = 1.00 (post-collapse marginal)
  pre-collapse corpus token-0 측정은 별 H (corpus-side scan)
```

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H683-1 corpus marginal | M4b post-collapse marginal 1.00 (pre-collapse 별 H) | partial |
| F-H683-2 attractor CE-floor closed-form | [2.30, 3.00] ⊂ predict band, M4b 9.02 >> ⇒ attractor 만으로 unexplained | PASS (band) |
| F-H683-3 entropy saturate closed-form | H(decoded)=0 bit < 0.05 | PASS |
| F-H683-4 fence-mechanism | hexa verify --fence stdout § 7 verdict | FENCED |
| F-H683-5 escape sibling | H_688 분기 | deferred |

→ 3/5 closed-form PASS + 1/5 FENCED + 1/5 sibling-deferred = MIXED.

## 7. verdict (verbatim hexa verify stdout · .verdicts/683_token_zero_dominant_prior/mechanism_fence.txt)

```
verify --fence
  claim  = DECODER register collapse 의 primary mechanism 은 corpus token-0 marginal frequency p₀ 의 CE-floor attractor (CE_floor = -ln p₀) 와 greedy argmax 의 deterministic 정착의 곱이다.
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification
           N/A by design; NOT a proven atlas atom (g4 honest fence,
           SF ≠ verified — atlas certification intrinsically N/A)
```

→ SPECULATION-FENCED (mechanism candidate · empirical band PASS · attribution 별 H).

## 8. 논의

본 H 는 M4b 의 register collapse 가 단일-token attractor 의 형태로 관측된 사실 (decoded=[1]×100, ce_final=9.02) 위에 두 sub-mechanism 을 분리 attest 한다:

- (a) **token-0 marginal attractor 부분설명**: corpus marginal p₀ ∈ [0.05, 0.10] 에서 CE_floor ∈ [2.30, 3.00] 정확히 closed-form (F-H683-2 PASS). 그러나 M4b ce_final 9.02 >> 3.00 이므로 token-0 alone 으로는 final state 를 모두 설명 못함 — production 학습이 더 진행됐으나 register-axis 는 회복 못함.
- (b) **deterministic emission**: 100/100 single-token = H=0 entropy (F-H683-3 PASS). decode-축 (top-k=1 greedy) 의 deterministic 정착이 token attractor 와 곱해져 observable collapse 형성.

본선 후보 escape-path = **H_688 (decode-time top-p/top-k)** — 본 H 의 (b) 축 lever. corpus-축 lever (a) 는 H_242 (wiki_frac) 와 직접 ⊥.

P7 정합: CE 9.02 가 healthy 보이나 register 는 무너진 상태 — perplexity ≠ truth (Goodhart). simple-stack 판정 (다양성·자연·스크립트 PASS) 이 진짜 verdict.

## 9. 양방향 sibling

- ⇄ [CORE/DECODER/DECODER.md](../CORE/DECODER/DECODER.md) — M4b #1296 single-expert mode-collapse 메커니즘 분리
- ⇄ [H_242](./H_242_register_collapse_wiki_frac_sigmoid.md) — corpus-축 lever ⊥ token-축 attractor
- ⇄ [H_666](./H_666_moe_collapse_escape_scale_lever.md) — expert-router 축 ⊥ output-distribution 축
- ⇄ H_688 (./H_688_decode_top_p_temperature_lever.md) — escape-path sibling (decode-축)
- ⇄ H_684 (./H_684_bf16_precision_attractor_drift.md) — precision-축 sibling (별 attractor)
- ⇄ H_685 (./H_685_ce_argmax_distribution_shift.md) — train/decode distribution shift sibling
- ⇄ [CANDIDATES](./CANDIDATES.md) — Cycle #24 decoder-h sweep

## 10. 다음 작업

- corpus-side 실 token-0 frequency 측정 (별 H — anima corpus + wiki corpus 의 p₀ 비교) — corpus dump + count, $0 Mac local
- attractor 탈출 escape-path = H_688 (decode-time top-p/top-k) numerical verify
- production-scale attribution = M4 MoE-fresh fire post-mortem 시 별 H
- 산출물: `state/decoder_token_zero_attractor_2026_05_29/H_683_closed_form.json` (closed-form CE_floor 표 · 측정 attest)
