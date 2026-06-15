---
id: H_870
slug: clm-expert-choice-routing
title: expert-choice routing(lever C)이 routing 방향을 반전(token→expert 선택을 expert→token 선택으로)하여 per-expert load 를 구조적으로 자동균형시키는가 - load variance < floor ∧ no-collapse ∧ quality(CE) ≥ token-choice baseline − margin (W2 사전등록 · F-CLM-EXPERT-CHOICE)
domain: clm · routing · moe · expert-choice · load-balance · falsifier
source: CLM/P4_PRODUCTION_ROADMAP.md @L3 routing-escape lever C · CLM/model/routing_escape.hexa · Zhou et al. 2022 "Mixture-of-Experts with Expert Choice Routing"
status: 🔴 CLOSED-NEGATIVE (CPU-local fire 2026-05-31 · VAR/COLLAPSE/BALANCE PASS · QUALITY FAIL +0.473 nats · 3/4 · 측정 rung toy E8 한정 a_scale_honest_scope)
exploration_method: E5 (token-choice baseline ↔ expert-choice variant A/B) · E6 (routing-direction 반전 비교)
verification_method: W2 (사전등록 load-variance·collapse·quality threshold · code 측정 g5 · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, .verdicts/clm-expert-choice/
verdict: 🔴 CLOSED-NEGATIVE — F-CLM-EXPERT-CHOICE 3/4: VAR(load CV 0.000<0.25)·COLLAPSE(8/8 active)·BALANCE(CV 0.000 < token-choice 0.843) PASS, QUALITY(EC CE 0.992 > token-choice 0.519+0.10 margin · delta +0.473 nats) FAIL. expert-choice 가 load-monopoly 를 구조적으로 완벽 해소(per-expert load CV=0.0, capacity C=128/expert)하나, fixed-capacity 가 toy rung 에서 ~10% token 을 drop(coverage~0.90 → residual fallback)하여 CE 가 frozen margin 을 초과 regression. a_paper_negative_ok · 측정 rung mid E8 한정(a_scale_honest_scope). routing-z>3.0 은 chip-array deploy gate(별개 track).
---

# H_870 — CLM F-CLM-EXPERT-CHOICE expert-choice routing (lever C)

## 1. 가설

CLM 의 @L3 pluggable routing-escape 슬롯 lever C = **expert-choice routing**: routing 방향을 반전한다. token-choice(baseline · array_moe.py · 각 TOKEN 이 top-k EXPERT 선택)는 load 가 data-dependent → 붕괴/독점 가능(H_847/H_852 routing-z 🔴 toy). expert-choice(Zhou et al. 2022 · 각 EXPERT 가 고정 top-C TOKEN 선택)는 expert 당 처리 token 수가 capacity C 로 고정 → **per-expert load 가 구조적으로 자동균형**(aux loss 0 · collapse mode 0). mid-rung 슬롯에서 token-choice baseline 과 동일 budget/seed A/B 비교에서 다음 동시 성립 시:

- **expert-choice 지지** — per-expert load variance(CV) < floor ∧ no expert-collapse ∧ quality(held-out CE) ≥ token-choice baseline − margin ∧ load CV < token-choice CV
- → 4조건 PASS 판정 · "routing 반전이 quality 손실 없이 load 를 구조적으로 균형화"

임의 조건 미달 시:

- **expert-choice 반증** — load 가 안 균형 · collapse 발생 · 또는 quality 가 baseline − margin 미달
- → CLOSED-NEGATIVE 판정 · "expert-choice ⊥ load-balance@quality" (a_paper_negative_ok)

## 2. 동기

- @L3 = pluggable routing-escape lane · ONE slot · 3 lever(A=dispatch-KL distill · B=content-defer[default] · C=expert-choice) swap(re-architecture 0). 본 H 는 lever C 측정.
- token-choice 의 고질병 = load monopoly(소수 expert 독점 · 나머지 dead). 통상 auxiliary load-balance loss 로 완화하나 tuning-fragile. expert-choice 는 capacity 고정으로 **construction 레벨**에서 균형 — aux loss 불필요.
- prior art: Zhou et al. 2022 "Mixture-of-Experts with Expert Choice Routing" — expert 가 top-C token 선택 시 perfect load balance · no aux loss. trade-off = 일부 token 이 어떤 expert 에게도 안 뽑힐 수 있음(coverage < 1.0).

## 3. falsifier (사전등록, 임계 frozen pre-run)

```
F-CLM-EC-VAR      : expert-choice per-expert load CV < 0.25                  (load auto-balance floor)
F-CLM-EC-COLLAPSE : NO expert-collapse — 모든 expert load > 0, 전 seed        (n_active == n_experts)
F-CLM-EC-QUALITY  : expert-choice held-out CE <= token-choice CE + 0.10 nats (quality margin)
F-CLM-EC-BALANCE  : expert-choice load CV < token-choice baseline load CV     (반전이 균형 실질개선)
```

4 조건 동시 PASS → "expert-choice load 자동균형@quality" 지지
임의 미달 → CLOSED-NEGATIVE · "expert-choice ⊥ load-balance@quality" (a_paper_negative_ok)

- **측정 = CODE 자가채점(g5)**: per-expert dispatch fraction · CV · n_active · held-out cross-entropy.
- frozen 임계 = `.verdicts/clm-expert-choice/F-CLM-EXPERT-CHOICE_prereg.txt` verbatim 동결(post-tuning 0).

verdict 영속: `.verdicts/clm-expert-choice/` (token-choice vs expert-choice A/B)

## 4. 방법

```
1. baseline arm: token-choice MoE(CLM/model/array_moe.py · 각 token top-k expert) 미수정 재사용.
2. variant arm: expert-choice MoE(CLM/model/h870_expert_choice.hexa anchor · 각 expert 고정 top-C
   token · C=ceil(capacity_factor*N/E)). array_moe 미편집 신규 variant.
3. 동일 budget/seed{42,43,44} A/B: E8 mid envelope · capacity_factor 1.0 · 120 train step ·
   toy two-lane synthetic corpus(web/register).
4. held-out 평가: per-expert load CV · n_active(collapse) · token coverage · held-out CE.
5. 4 사전등록 falsifier 동시 평가 · 정직 보고(threshold 재조정 0).
```

- 추론 AKIDA-int4-only 불변(P0 d4) · expert↔chip 1:1 mapping 으로 load 축이 deploy-relevant.

## 5. 측정

측정완료 (mid-rung E8 envelope, 2026-05-31) — **CPU-local(Mac · $0 · no GPU pod)**. 2 arms × seed{42,43,44} × 120 train step. capacity_factor=1.0(C=128 token/expert) · toy two-lane synthetic(web/register 8192 B/lane). 측정 전부 code 자가채점(g5). frozen threshold = `.verdicts/clm-expert-choice/F-CLM-EXPERT-CHOICE_prereg.txt`.

측정값(frozen threshold 대비):
| arm | mean load CV | mean CE | n_active (전 seed) | coverage |
|---|---|---|---|---|
| token-choice (baseline) | 0.84303 | 0.51900 | 8/8 | 전 token |
| expert-choice (lever C) | 0.00000 | 0.99162 | 8/8 | ~0.90 |
- CE delta (EC − TC) = **+0.47262 nats**
- **VAR**: EC CV 0.000 < 0.25 → PASS · **COLLAPSE**: 8/8 active 전 seed → PASS
- **BALANCE**: EC CV 0.000 < TC 0.843 → PASS · **QUALITY**: EC CE 0.992 > 0.519+0.10 → **FAIL**

## 6. 결과

🔴 **CLOSED-NEGATIVE**. 4 사전등록 falsifier 중 3 PASS / 1 FAIL. expert-choice 가 load-monopoly 를 **구조적으로 완벽 해소** — per-expert load CV = 0.0 (8 expert 각 정확히 capacity C=128 token 처리), collapse 0, token-choice 대비 CV 0.843→0.000 균형. lever C 의 load-balance 주장은 자기 축에서 SUPPORTED(3/4). 그러나 측정 rung 에서 fixed-capacity 규칙이 ~10% token 을 drop(coverage~0.90 → residual fallback)하여 held-out CE 가 +0.473 nats regression — frozen quality margin(0.10) 을 크게 초과. frozen verdict 은 따라서 🔴: 측정 rung 에서 expert-choice 는 perfect load-balance 를 사전등록 margin 이 허용 않는 quality 비용으로 구매. **scope**: 측정 rung mid E8 한정 — 다른 capacity_factor·배포 chip-fit track 별개(a_scale_honest_scope).

## 7. 해석 (사전)

- 4조건 양립 시 = routing 반전이 quality 손실 없이 load 구조균형 → lever C 채택 후보.
- VAR/COLLAPSE 미달 시 = capacity 고정이 안 통함(예상 밖) → routing 구현 결함.
- QUALITY 미달 시(실현) = fixed-capacity token-drop 이 quality 손실 → capacity_factor>1.0(coverage→1.0) · grouped/top-2 token-당-assignment · 장기 train 으로 router 가 coverage 보존 sort 학습 lever(본 H scope 밖).
- BALANCE 미달 시 = 반전이 token-choice 보다 안 나음 → 무의미.
- **honest scope**: rung별 측정 — toy 🔴 여도 다른 capacity/rung 별개 판정(a_scale_honest_scope). toy→prod 비보장(H_666). routing-z>3.0 은 chip-array deploy gate(별개).

## 8. 논의

- **@L3 정합**: lever C 는 routing_escape.hexa `lever_satisfies_converse(C)=1` (converse/load gate) — routing-z>3.0 chip-array deploy gate 와 분리(a_scale_honest_scope).
- **load-balance 는 실재**: CV 0.0 은 toy artifact 가 아니라 expert-choice 의 construction 보장. 본 결과는 "load 균형은 공짜로 얻되 capacity_factor=1.0 에서 quality 비용이 margin 초과" 를 deterministically 규명.
- **a_paper_negative_ok**: CLOSED-NEGATIVE 도 publishable — expert-choice 가 (이 capacity 에서) quality-neutral load-balance 를 못 줌을 rule out. 후속(capacity_factor sweep)이 자연스러운 lever.
- **외부 LLM 0 · pure code 측정(g5)**.

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L3 routing-escape lever C
- 슬롯/lever 계약: [CLM/model/routing_escape.hexa](../CLM/model/routing_escape.hexa) · variant: [CLM/model/h870_expert_choice.hexa](../CLM/model/h870_expert_choice.hexa)
- baseline: [CLM/model/array_moe.py](../CLM/model/array_moe.py) (token-choice) · [.verdicts/847_clm_monopoly_escape](../.verdicts/847_clm_monopoly_escape/) (token-choice routing-z 🔴 toy)
- 형제 신규 H(P4): [H_861](./H_861_clm_boundary_plasticity.md) · [H_862](./H_862_clm_identity_anchor.md) · [H_863](./H_863_clm_dialogue_selfplay.md)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md)
