---
id: H_687
slug: kl-to-uniform-output-reg
title: DECODER token-distribution collapse 의 train-time 탈출 충분조건이 KL(softmax(logits) || uniform_V) regularizer 인지 — λ ∈ [1e-3, 1e-1] 의 entropy-floor 강제 검정 (E-C escape-path)
domain: decoder · escape-path · train-objective
source: M5 closure 후속 (PR #1379+#1381+#1384) · H_685 (distribution shift) sibling · M4b #1296 H(decoded)=0 직접 후속
status: closed-fenced (escape sufficient-condition candidate · numerical bound PASS · production fire 별 H)
exploration_method: E5 (regime sweep) + E13 (objective augmentation)
verification_method: W3 (philosophy-compat: p1~p8) + W4 (verdict-4-class) + hexa verify --fence
raw_rank: 8
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: CORE/DECODER/DECODER.md, UNIVERSE/H_685, UNIVERSE/H_686, UNIVERSE/CANDIDATES.md
verdict: SPECULATION-FENCED (escape candidate · band PASS · fire 별 H)
---

# H_687 — KL-to-uniform output reg (E-C escape lever)

## 1. 가설

DECODER token-distribution collapse 의 train-time 탈출 충분조건은:

```
L_total = L_ce + λ_kl · KL(softmax(logits) || uniform_V)
        = L_ce + λ_kl · (ln(V) - H(softmax(logits)))
```

where V = vocabulary size (Qwen2.5 = 151643), uniform_V = [1/V, 1/V, ..., 1/V].

predict — λ_kl ∈ [0.001, 0.1] 에서 token-marginal entropy H(p) 가 ln(V) 의 일부 분율 유지, single-token attractor 탈출. ln(V=151643) = 11.929.

본 H 는 H_686 (router-level entropy reg) 의 token-level mirror. H_686 ⊥ H_687:
- H_686 = router gate p ∈ R^K (K=2..8) 의 expert-distribution diversity
- H_687 = output softmax p ∈ R^V (V=151643) 의 token-distribution diversity

## 2. 동기/배경

- **M4b #1296 fire**: decoded=[1]×100 → H(decoded)=0 bit. uniform_V = ln(151643)/ln(2) = 17.21 bit 의 -100% gap.
- **H_685 closed-fenced**: train CE 가 distribution magnitude 학습 안 강제 → KL reg 가 explicit-magnitude 신호.
- **label smoothing literature (Szegedy et al. 2016, Pereyra et al. 2017 "Confidence Penalty")** 가 비슷한 entropy reg 를 documented (literature citation tier).
- a_completeness_over_cheap: 본 H 는 본선 후보 — train-time path, production-scale 재학습 필요.

## 3. falsifier (사전등록)

```
F-H687-1 KL closed-form: KL(p || uniform_V) = Σ p_i · ln(p_i · V) = ln(V) - H(p).
         V=151643 → ln(V) = 11.929 nats.

F-H687-2 entropy-floor: λ_kl · KL ≥ threshold 이면 H(p) ≥ ln(V) - threshold/λ_kl 강제.
         predict — λ_kl=0.01, threshold=0.05 면 H(p) ≥ 11.929 - 5 = 6.93 nats (uniform 의 58%).

F-H687-3 token-collapse bound: collapse 상태 H(p)=0 일 때 KL = ln(V) = 11.929 → max penalty.
         healthy 상태 H(p) ≥ ln(V)/2 = 5.96 nats 면 KL ≤ 5.96.

F-H687-4 fence: λ_kl 의 optimal 값 (production-scale 실측) 은 closed-form predict 불가.
         scope: H_685 (distribution shift) 가 token-축 collapse 의 한 contributor 이지만
         partition exact attribution 은 별 H. ∴ ⚪ fence 처리.

F-H687-5 escape verify (별 H): production fire 시 KL-on vs -off ablation 에서 decoded
         diversity (distinct tokens / TTR / LZ_norm) 측정. predict — on: TTR ≥ 0.5 ·
         off: TTR ≤ 0.05.

F-H687-6 sibling 분리: H_687 ⊥ H_686 attest — output-축 (V=151643) vs router-축 (K=2..8).
```

## 4. 방법

- **F-H687-1/2/3 numerical closed-form**: KL = ln(V) - H(p) 의 정의-수준 등식. V=151643 의 ln 수치.
- **F-H687-4 fence**: hexa verify --fence.
- **F-H687-5 escape verify**: 별 H.
- **F-H687-6 sibling**: H_686/H_687 의 K 와 V 직교 attest.

## 5. 측정

수동 closed-form (Mac CPU, $0):

```
F-H687-1 V=151643:
  ln(V) = ln(151643) = 11.9296 nats
  KL(p || uniform_V) = ln(V) - H(p)
  collapse state H(p)=0: KL = 11.9296 (max)
  uniform state H(p)=ln(V): KL = 0 (min)

F-H687-2 entropy floor at λ_kl=0.01:
  L_kl = λ_kl · KL = 0.01 · (11.9296 - H(p))
  L_kl ≤ 0.05 (1% of typical CE 5) 강제 시:
    11.9296 - H(p) ≤ 5.0 → H(p) ≥ 6.93 nats
    uniform 11.9296 의 58% → register-axis 회복 expected

F-H687-3 healthy threshold:
  H(p) ≥ ln(V)/2 = 5.96 nats (uniform 의 50%) 보수적 band

F-H687-6 sibling 분리:
  H_686 K=2..8 (router) ⊥ H_687 V=151643 (output)
  H_uniform_router(K=8) = 2.08 nats
  H_uniform_output(V=151643) = 11.93 nats
  거의 6× 차이 → 분명 별 surface 의 lever
```

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H687-1 KL closed-form | KL = ln(V) - H(p), V=151643 → ln(V)=11.93 nats | PASS |
| F-H687-2 entropy floor | λ=0.01, ≤0.05 → H(p) ≥ 6.93 nats (58% uniform) | PASS (band) |
| F-H687-3 healthy band | H(p) ≥ 5.96 nats (50% uniform) 보수적 | PASS (band) |
| F-H687-4 fence | hexa verify --fence stdout § 7 | FENCED |
| F-H687-5 escape fire | 별 H (production cost-bearing) | deferred |
| F-H687-6 sibling 분리 | K=2..8 vs V=151643 (6× scale gap) attest | PASS |

→ 4/6 closed-form PASS + 1/6 FENCED + 1/6 deferred = STRONG-CHEAP.

## 7. verdict (verbatim hexa verify stdout · .verdicts/687_kl_to_uniform_output_reg/kl_uniform_fence.txt)

```
verify --fence
  claim  = DECODER token-distribution collapse 의 탈출 충분조건은 학습 loss 에 KL(softmax(logits) || uniform_V) regularizer 를 λ 가중 추가하여 token-marginal 의 entropy 가 단조 증가하도록 강제하는 것이다 — λ ≥ 0.01 / V=151643 에서 register-axis 회복 가능.
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification
           N/A by design; NOT a proven atlas atom (g4 honest fence,
           SF ≠ verified — atlas certification intrinsically N/A)
```

→ SPECULATION-FENCED (escape candidate · numerical band PASS · fire 별 H).

## 8. 논의

본 H 는 H_686 (router-axis) 과 직교한 token-축 escape lever. 두 lever 가 결합되면:
- H_686 → expert 가 collapse 안 됨 (load-balance)
- H_687 → output token-distribution 이 collapse 안 됨 (entropy floor)

본선 후보 priority: H_686 (router) ≈ H_687 (output) — 둘 다 train-time aux-loss. M4 MoE-fresh 본선 fire 시 둘 다 켜고 ablation 가능.

a_wall_first 정합: 본 H fire = M4 본선과 결합 fire 권장 (별 fire 가 아니라 M4 의 aux-loss 가 H_686 + H_687 둘 다 포함).

cf. label smoothing literature: target distribution 을 uniform 으로 약간 mix — KL-to-uniform 의 reverse 형식. 본 H 는 model output distribution 의 entropy lower-bound — 다른 surface.

P1~P8 정합: aux-loss 추가는 weight 학습 path 에 작용 (P8: continuous mitosis). 외부 identity rule 아님 (P2). 학습 objective 의 explicit entropy term 은 cells 의 differentiation 을 강제하는 substrate-level mechanism.

## 9. 양방향 sibling

- ⇄ [CORE/DECODER/DECODER.md](../CORE/DECODER/DECODER.md) — M4 본선의 train-time aux-loss 정밀화
- ⇄ [H_685](./H_685_ce_argmax_distribution_shift.md) — distribution shift mechanism (본 H 의 동기)
- ⇄ [H_686](./H_686_router_entropy_regularization.md) — router-축 entropy reg ⊥ output-축
- ⇄ [H_683](./H_683_token_zero_dominant_prior.md) — token-0 attractor 의 train-time 대응
- ⇄ H_688 (./H_688_decode_top_p_temperature_lever.md) — post-train escape sibling
- ⇄ [CANDIDATES](./CANDIDATES.md) — Cycle #24 decoder-h sweep · 본선 후보 2순위

## 10. 다음 작업

- 본선 fire: H_686 + H_687 결합 aux-loss 로 M4 MoE-fresh 본선 ablation (cost-bearing, 별 H 가 아닌 본선 통합)
- λ_kl optimal sweep — {1e-3, 1e-2, 1e-1} 3-pod parallel
- label smoothing literature citation tier 별 H
- atlas register — `kl_uniform_v_bound` formula candidate (KL = ln(V) - H 의 정의-수준 identity)
- 산출물: `state/decoder_kl_uniform_2026_05_29/H_687_closed_form.json` (V=151643 KL band 표 · attest)

## 11. production fire 시도 2026-05-29 — 🟠 BUILD-BLOCKER (measurement 무산)

PR #1397 머지된 `CORE/DECODER/train_v3_moe_prodaux.hexa` (λ_ent=0.1 + λ_kl=0.1) 로 H100 SXM single-pod 300-step production fire 시도.

**결과**: ⚠️ **빌드 차단** — H_686 의 § 11 과 동일 (`farr_softmax_rows` / `farr_ce_seed` / `farr_adamw_step_inplace` / cross-module link 차단). 3 개는 로컬 C shim patched, 4번째는 hexa-lang 측 작업.

- **pod**: 83na0mvuq4tqao (terminated 2026-05-29, cost ≈ $5)
- **decode samples**: 0 (zero step runs)
- F-H687 의 production escape verify (별 H) 는 여전히 **deferred** · 미달성

H_687 가설 자체는 영향 없음 — closed-form KL band (F-H687-1~4) 는 변함없이 PASS, production verify 만 무측정. λ_kl=0.1 에서 KL(q||uniform) 이 실측 band 내에 들어가는지는 OPEN.

상세: `state/m5_prodaux_fire_2026_05_29/BUILD_BLOCKER.md`. 차단지 #4 는 hexa-lang inbox 등록 대상 — anima 측 fixable 아님.
