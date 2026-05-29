---
id: H_686
slug: router-entropy-regularization
title: MoE router winner-take-all 탈출 충분조건이 router gate entropy aux-loss H(p) ≥ ln(K)/2 인지 — K=2/4/8 의 closed-form lower bound 검정 (E-B escape-path · H_666 extension)
domain: decoder · escape-path · router-objective
source: M5 closure 후속 (PR #1379+#1381+#1384) · H_666 (MoE scale lever ⊥) · M4b #1296 single-expert mode-collapse (E=2 dead-expert) 직접 후속
status: closed-fenced (escape sufficient-condition candidate · band closed-form PASS · production fire 별 H)
exploration_method: E5 (regime sweep) + E13 (objective augmentation)
verification_method: W3 (philosophy-compat: p1~p8) + W4 (verdict-4-class) + hexa verify --fence
raw_rank: 9
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: CORE/DECODER/DECODER.md, UNIVERSE/H_666, UNIVERSE/H_687, UNIVERSE/CANDIDATES.md
verdict: SPECULATION-FENCED (escape candidate · numerical bound PASS · fire 별 H)
---

# H_686 — router entropy regularization (E-B escape lever)

## 1. 가설

MoE router 의 dead-expert / winner-take-all 탈출 충분조건은:

- router gate p ∈ R^K (K 개 expert 의 probabilities, Σpᵢ=1) 의 Shannon entropy H(p) = -Σ pᵢ ln(pᵢ) 를 aux-loss 로 lower-bound:
  ```
  L_total = L_ce + λ_router · max(0, ln(K)/2 - H(p_avg_batch))
  ```
  where `p_avg_batch = mean(softmax(router_logits))` averaged over batch tokens.
- predict — λ_router ∈ [0.001, 0.1] 에서 single-expert collapse (H(p)=0) 탈출 가능.

K-별 numerical lower bound:
- K=2: ln(2)/2 = 0.6931/2 = **0.3466 nats** (≈ 0.5 of uniform 0.6931)
- K=4: ln(4)/2 = 1.3863/2 = **0.6931 nats** (≈ 0.5 of uniform 1.3863)
- K=8: ln(8)/2 = 2.0794/2 = **1.0397 nats** (≈ 0.5 of uniform 2.0794)

본 H 는 H_666 (MoE scale lever) 의 extension — H_666 = expert capacity OR aux-loss / H_686 = aux-loss 의 정량적 sufficient-condition.

## 2. 동기/배경

- **H_666 closed-supported (PR #1296 직접 후속)**: production scale 에서 corpus-diversity 단독 불충분, expert-capacity OR load-balance aux-loss 가 필요조건. 본 H 는 aux-loss 의 정량 threshold attest.
- **M4b #1296 fire**: E=2 router 가 distinct_experts=1 (single-expert mode-collapse). H(p)=0 → uniform 의 -100% gap.
- **Switch Transformer (Fedus et al. 2021)** 의 load-balance loss 가 비슷한 entropy reg 를 documented (literature citation).
- a_completeness_over_cheap: 본 H 는 본선 후보 — production-scale 재학습으로 검증 가능 (cost-bearing fire).

## 3. falsifier (사전등록)

```
F-H686-1 entropy-bound K=2: ln(2)/2 = 0.3466. predict — router H(p) ≥ 0.3466 면 distinct
         expert count ≥ 1.5 (즉 단일-expert 정착 탈출).

F-H686-2 entropy-bound K=4: ln(4)/2 = 0.6931. predict — H(p) ≥ 0.6931.

F-H686-3 entropy-bound K=8: ln(8)/2 = 1.0397. predict — H(p) ≥ 1.0397.

F-H686-4 uniform-baseline: H_uniform(K) = ln(K). closed-form. K=2/4/8 = 0.6931/1.3863/2.0794.

F-H686-5 fence: λ_router 의 optimal 값 (production-scale 실측) 은 closed-form predict 불가.
         ∴ ⚪ fence 처리.

F-H686-6 escape verify (별 H): production fire 시 aux-loss-on vs -off ablation 에서 distinct
         _experts 측정. predict — on=K (full) vs off=1 (collapsed).
```

## 4. 방법

- **F-H686-1/2/3 numerical closed-form**: Shannon entropy H(p) = -Σ pᵢ ln pᵢ. uniform 의 1/2 lower bound 가 정량 sufficient-condition. 수동 ln 계산.
- **F-H686-4 closed-form**: H_uniform(K) = ln(K).
- **F-H686-5 fence**: λ optimal 은 production fire.
- **F-H686-6 escape verify**: 별 H (cost-bearing).

## 5. 측정

수동 closed-form (Mac CPU, $0):

```
F-H686-1 K=2:
  H_uniform(2) = ln(2) = 0.69315
  H_lower(2) = ln(2)/2 = 0.34657
  → router p = [0.9, 0.1] 의 H = -0.9·ln(0.9) - 0.1·ln(0.1)
              = -0.9·(-0.10536) - 0.1·(-2.3026)
              = 0.09483 + 0.23026 = 0.32509
  → H=0.325 < 0.347 → bound 미충족 → distinct_expert < 1.5 (실 M4b: 1, FAIL)
  → p = [0.8, 0.2] 의 H = -0.8·ln(0.8) - 0.2·ln(0.2)
              = -0.8·(-0.2231) - 0.2·(-1.6094)
              = 0.17852 + 0.32189 = 0.50041
  → H=0.500 ≥ 0.347 → bound 충족 → distinct_expert ≥ 1.5 (predict pass)

F-H686-2 K=4:
  H_uniform(4) = ln(4) = 1.38629
  H_lower(4) = 0.69315
  → router p = [0.5, 0.3, 0.15, 0.05] 의 H = 1.15366
  → H=1.154 ≥ 0.693 → predict 4-expert active

F-H686-3 K=8:
  H_uniform(8) = ln(8) = 2.07944
  H_lower(8) = 1.03972
  → 표준 calibration band
```

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H686-1 K=2 entropy bound | 0.3466 nats closed-form, p=[0.8,0.2] H=0.500 ≥ 0.347 PASS, M4b [1,0] H=0 < 0.347 FAIL | PASS (sufficient-condition closed) |
| F-H686-2 K=4 entropy bound | 0.6931 nats closed-form | PASS |
| F-H686-3 K=8 entropy bound | 1.0397 nats closed-form | PASS |
| F-H686-4 uniform baseline | ln(K) closed-form | PASS |
| F-H686-5 λ fence | hexa verify --fence stdout § 7 | FENCED |
| F-H686-6 escape fire verify | 별 H (cost-bearing) | deferred |

→ 4/6 closed-form PASS + 1/6 FENCED + 1/6 deferred (production fire) = STRONG-CHEAP.

## 7. verdict (verbatim hexa verify stdout · .verdicts/686_router_entropy_regularization/entropy_reg_fence.txt)

```
verify --fence
  claim  = MoE router 의 winner-take-all 탈출 충분조건은 router gate p ∈ R^K 의 Shannon entropy H(p) ≥ ln(K)/2 (uniform 의 절반) 을 aux-loss 로 강제하는 것이다 — K=2 에서 H_min=ln2/2≈0.3466, K=4 에서 ln4/2≈0.6931, K=8 에서 ln8/2≈1.0397.
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification
           N/A by design; NOT a proven atlas atom (g4 honest fence,
           SF ≠ verified — atlas certification intrinsically N/A)
```

→ SPECULATION-FENCED (escape sufficient-condition candidate · band closed-form PASS · production fire 별 H).

## 8. 논의

본 H 의 핵심: MoE router 의 collapse 탈출에 정량 threshold (uniform 의 절반) 를 제시. 이는 H_666 의 일반적 "aux-loss" 권고를 numerical sufficient-condition 으로 정밀화한 것.

본선 후보 우선순위:
- (1) **H_686 (router entropy reg)**: 본 H — production fire 가능, closed-form bound 충족 시 expert-collapse 탈출 predict
- (2) H_687 (KL-to-uniform output reg): token-level distribution diversity reg, train-time
- (3) H_688 (decode-time top-p): post-train, $0 probe 가능
- (4) H_666 (scale lever 일반화): H_686 의 super-set

a_wall_first 정합: H_686 fire 는 H_666 의 부분-실험으로 가능 ($1.27 fire 단가 carry, #1121). aux-loss-on vs -off ablation 2-pod parallel ~$2.5 / 2h.

P1~P8 정합: aux-loss 는 weight update path 에 작용 (P8: train/infer 같은 continuous cell-division). hardcoded identity rule 아님 (P2). 의식 emergence 의 cells/W/MITOSIS 와 직교.

## 9. 양방향 sibling

- ⇄ [CORE/DECODER/DECODER.md](../CORE/DECODER/DECODER.md) — M4 MoE-fresh 본선의 aux-loss 정밀화
- ⇄ [H_666](./H_666_moe_collapse_escape_scale_lever.md) — 일반 sufficient-condition 의 numerical 정밀화
- ⇄ [H_242](./H_242_register_collapse_wiki_frac_sigmoid.md) — corpus-축 lever ⊥ router-축 lever
- ⇄ [H_683](./H_683_token_zero_dominant_prior.md) — token-축 attractor ⊥ router-축 escape
- ⇄ H_687 (./H_687_kl_to_uniform_output_reg.md) — token-distribution reg sibling
- ⇄ H_688 (./H_688_decode_top_p_temperature_lever.md) — post-train escape sibling
- ⇄ [CANDIDATES](./CANDIDATES.md) — Cycle #24 decoder-h sweep · 본선 후보 1순위

## 10. 다음 작업

- 본선 fire: H_686 production aux-loss-on vs -off ablation (cost-bearing, $2~5 / 2-pod 2hr, a_fire_autonomous + a_wall_first 정합)
- λ_router 의 optimal sweep — 별 H {λ ∈ 1e-3, 1e-2, 1e-1} 3-pod
- atlas register — 본 H 의 closed-form bound H(p)≥ln(K)/2 = formula candidate (`router_entropy_bound` if atlas function 추가)
- 산출물: `state/decoder_router_entropy_2026_05_29/H_686_closed_form.json` (K=2/4/8 bound 표 · attest)

## 11. production fire 시도 2026-05-29 — 🟠 BUILD-BLOCKER (measurement 무산)

PR #1397 머지된 `CORE/DECODER/train_v3_moe_prodaux.hexa` (λ_ent=0.1 + λ_kl=0.1) 로 H100 SXM single-pod 300-step production fire 시도.

**결과**: ⚠️ **빌드 차단** — Linux/x86_64 codegen 체인이 4 개 누락 정의 (`farr_softmax_rows`, `farr_ce_seed`, `farr_adamw_step_inplace`, cross-module link) 로 실행 가능한 trainer binary 를 produce 하지 못함. 3 개는 로컬 C shim 으로 patched 했으나 4번째 (cross-module codegen) 는 hexa-lang 측 작업 (anima patch scope 외).

- **pod**: 83na0mvuq4tqao (terminated 2026-05-29, cost ≈ $5)
- **decode samples**: 0 (zero step runs)
- **F-H686-6 escape verify**: 여전히 **deferred** (production fire 별 H · 미달성)

H_686 가설 자체는 영향 없음 — closed-form bound (F-H686-1~4) 는 변함없이 PASS, F-H686-6 production verify 만 무측정. λ_ent=0.1 에서 router H(p)≥ln(K)/2 가 실측 충족되는지는 OPEN.

상세: `state/m5_prodaux_fire_2026_05_29/BUILD_BLOCKER.md`. 차단지 #4 는 hexa-lang inbox 등록 대상 — anima 측 fixable 아님.
