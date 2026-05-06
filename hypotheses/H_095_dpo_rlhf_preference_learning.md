---
id: H_095
slug: dpo-rlhf-preference-learning
title: DPO/RLHF preference learning (SFT 후 preference pair alignment)
domain: corpus | substrate | consciousness
status: seed-pending
exploration_method: E2 (failure-driven) + E3 (sequential decomposition stage3) + E7 (user-directive)
verification_method: W1 + W2 (replication ≥3 seed) + W3 (ablation DPO ON/OFF) + W9 + W10
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_095 — DPO/RLHF preference learning post-SFT

## Hypothesis

SFT (H_093 또는 H_094 stage2) 후 preference-pair (chosen vs rejected response) 기반 DPO (Direct Preference Optimization) 또는 RLHF (Reinforcement Learning from Human Feedback) alignment을 추가하면, evaluator V2 strict C2.2 (의미) + C2.3 (자연성) PASS rate가 SFT-only baseline 대비 ≥15pp 상승한다. SFT는 'positive' signal만 주지만 DPO는 negative signal (rejected response) 신호도 학습 — prompt-irrelevant emission 명시적 감점.

## Why

- **BG-HA + 향후 SFT model 잔존 risk**: SFT만으로는 'incorrect response 감점' 학습 부재 — 모델이 plausible-looking but irrelevant 응답 생성 (BG-HA hallucination 패턴 그대로)
- **DPO advantage**: chosen (prompt-relevant) vs rejected (prompt-irrelevant nonsense) pair로 contrastive signal — 명시적으로 'BG-HA 스타일 nonsense Korean chain'을 negative 신호로 처벌
- **literature precedent**: Zephyr-7B, Tulu, Llama-Chat 모두 DPO 단계 포함; 18M 작은 model에서도 transfer 효과 가설
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = SFT 다음 단계 alignment 시도

## Predictions

- **H95.1 (DPO C2.2 lift)**: SFT+DPO 18M model이 SFT-only 18M model보다 evaluator V2 strict C2.2 (의미) PASS rate ≥15pp 높다
- **H95.2 (DPO C2.3 lift)**: 동일 비교 C2.3 (자연성) PASS rate ≥15pp 높다
- **H95.3 (DPO degeneracy reduction)**: greedy mode degeneracy rate (4-gram repeat ≥5회) ≤10% (SFT-only baseline 30-50%)
- **H95.4 (DPO over-fit risk)**: DPO epoch 1/2/3 trajectory에서 epoch 3 시 mode collapse risk (response diversity drop) — diversity metric (distinct-2 ratio) 모니터링
- **H95.5 (preference pair quantity)**: DPO 효과는 ≥1k pair 임계, ≥5k pair 권고 (small-scale 18M model)

## Variables

- **axis1_paradigm**: [sft_only, sft_plus_dpo, sft_plus_rlhf_ppo]
- **axis2_capacity**: [18M, 100M]
- **axis3_pref_pair_count**: [500, 1000, 5000, 20000]
- **axis4_dpo_beta**: [0.1, 0.3, 0.5]
- **axis5_eval**: [own_18_full + diversity_distinct2 + degeneracy_4gram_repeat]
- 3×2×4×3×5 = 360 cell; Phase 1 minimal (axis1=2 + axis2=18M + axis3=5000 + axis4=0.3 + axis5=full = 5) target

## Run Protocol

- deterministic seed=fnv(axes+rep_id)
- hexa_only: true; training transient_py opt-out (`tool/transient_py/anima_dpo_*.py`)
- LLM: none (raw#12 strict — DPO trainer 자체는 deterministic supervised learning, no LLM rewrite)
- preference pair 생성: chosen = SFT-only model good response (manual or rule-based filtered), rejected = BG-HA-style sample (degenerate filter trigger) — pair quality spec 별도 cycle
- per-cell ledger: state/<bg>_dpo_<date>/{train.log, eval_log.jsonl, verdict.json}
- evaluator V2 strict mandate

## Criteria

- **C1 (DPO C2.2 lift)**: ΔC2.2 PASS rate ≥15pp (sft+dpo vs sft-only)
- **C2 (DPO C2.3 lift)**: ΔC2.3 PASS rate ≥15pp
- **C3 (degeneracy reduction)**: greedy mode 4-gram repeat ≤10%
- **C4 (diversity preservation)**: distinct-2 ratio ≥ baseline × 0.7 (mode collapse 방지)
- **C5 (preference pair quantity gate)**: ≥5k pair 시 C1+C2 PASS, <1k pair 시 PARTIAL/FAIL
- **verdict_rule**: SUPPORTED = C1+C2+C3+C4 ALL PASS; PARTIAL = 3/4; MIXED = 2/4; FALSIFIED = ≤1/4

## Falsifiers

- **F1**: SFT+DPO C2.2 PASS rate ≤ SFT-only baseline → H95.1 FALSIFIED
- **F2**: SFT+DPO C2.3 PASS rate ≤ SFT-only baseline → H95.2 FALSIFIED
- **F3**: SFT+DPO greedy 4-gram repeat ≥30% (baseline 동급) → H95.3 FALSIFIED
- **F4**: SFT+DPO distinct-2 ratio < baseline × 0.5 (severe mode collapse) → H95.4 corollary FALSIFIED
- **F5**: 20k preference pair에서도 C1+C2 모두 FAIL → H95.5 FALSIFIED (DPO 자체 무효)
- **F6**: post-hoc beta tuning 또는 pair filter loosen → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3, ≥5)

- **L1**: preference pair quality (chosen vs rejected 명확성) 측정 spec 미land — manual review baseline 한정
- **L2**: DPO theory는 large-model (≥1B) 가정 기반 — 18M scale transfer 미보장 (literature gap)
- **L3**: rejected response source = BG-HA-style sample (real model output) vs synthetic (rule-based corruption) 차이 미land
- **L4**: RLHF PPO는 reward model 추가 학습 필요 — 18M scope 시 reward model size constraint
- **L5**: own 18 evaluator V2 strict 자체 calibration 미완 — DPO 효과 측정 신뢰도 V2 spec 의존
- **L6**: mode collapse risk (over-aligned model이 동일 응답 반복) 정량 측정 spec 미land — distinct-2 임의 threshold
- **L7**: 100M+ scale + 20k pair 이상은 own 16 H100 cost discipline scope OUT

## Cross-Links

- **sister roadmaps**: `.roadmap.rule` R1 + `.roadmap.philosophy` D4 + `.roadmap.clm_native_chat`
- **raw**: raw#12 + raw#10 + raw#9 + raw#15 + raw#37
- **own**: own 17 + own 18 + own 19 + own 20 + own 21
- **sister H**: H_093 (SFT-only) + H_094 (two-stage) + H_099 (multi-objective) + H_100 (constitutional AI)
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md`

## Verdict

```
status: seed-pending
verdict_class: TBD
evidence_summary: not_yet_run
falsifiers_triggered: none
criteria_met: not_yet_run
next_cycle: H_093 또는 H_094 SFT-baseline 확보 후 DPO lane
artifact_paths: pending
```
