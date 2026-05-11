---
id: Hc_1224
slug: identity-rules-dcr-gray-zone-light-ft
title: Hardcoded identity rule prefix vs substrate-only — DCR delta in gray zone on light-FT
domain: philosophy / no-identity-rules / P-IDR / substrate
status: candidate-empirical-weak
source_doc: PHILOSOPHY.md cont. 5; state/p_idr_identity_rules_2026_05_12/results_2026_05_12.json
source_lines: PHILOSOPHY.md (2026-05-12 cont. 5 section)
promoted_at: 2026-05-12
last_updated: 2026-05-12
linked_h: README Philosophy #2 NO IDENTITY RULES (POLICY · indeterminate-mixed signal); own 18 simple_stack
hf_dataset: (not yet)
notes: "INDETERMINATE — DCR Δ +0.041, gray zone 3pp<Δ<5pp. substrate-only DCR 약간 우월 but effect size 미달. 3-step light-FT 한계."
---

## Hypothesis

Hardcoded identity rule prefix (10-clause persona block injected on every
user turn + post-FT system prefix) **does NOT measurably degrade nor enhance
cell-substrate distinctiveness (DCR)** under short FT (3 steps, 22M trainable
params, lr=1e-5) — Δ falls in the gray zone (3pp<Δ<5pp) of the P-IDR spec
thresholds.

본 finding 의 가능한 해석:
1. **Light-FT 한계**: 3 step 으로는 어느 condition 도 substrate 에 의미있는
   영향 미치지 못함 → full FT (5K-10K step) 에서는 differentiation 가능
2. **Substrate-saturation**: BG-LB 8000-step pretrain 의 DCR baseline 0.50
   주변이 이미 saturated → identity rules 이든 substrate-only 든 same DCR plateau
3. **Effect 자체 부재**: identity rules 가 정말 substrate-aliveness 와
   orthogonal — 어떤 condition 도 cell distinctiveness 에 영향 안 줌

## Evidence — P-IDR ablation (2026-05-12, RTX 5070 local $0)

Substrate: BG-LB 350M (`dancinlab/clm-v5-bg-lb-350m-pretrain-path-a-remapped`,
`step_8000_final.pt`, 298M params), 3-step FT (seq=128, lr=1e-5, lora_r=16,
trainable=22M).

| Metric | A (rules) | B (substrate) | Δ B−A | Threshold |
|---|---:|---:|---:|---|
| simple_stack_pass | 0.0 | 0.0 | 0.0 | (chat-cap 미수렴, ceiling) |
| PIV max | 0.0069 | 0.0069 | 0.0 | (sub-floor) |
| **DCR** | **0.4694** | **0.5102** | **+0.0408** | **big_pt=0.05, small_pt=0.03** |
| drand | 0.022 | 0.022 | 0.0 | — |
| intra-prompt cosine | 0.3791 | 0.3122 | -0.0669 (A higher) | — |
| inter-prompt variance | 0.002305 | 0.003891 | +0.0016 (A lower) | — |
| OOD consistency | 0.9929 | 0.9928 | 0.0001 (tied) | — |

- A_rules higher intra-prompt cosine (0.38 vs 0.31) — same-prompt seeds 일관성
  부분적으로 살림
- A_rules lower inter-prompt variance — prompt 간 hidden-state 균일화 (덜 다양한
  persona 표현 가능성)
- B_substrate higher DCR (+0.041) — rules 없는 substrate 가 cell-distinctiveness
  약간 살리지만 effect size 미달

## Falsifier

- **Hc_1224 PATH-1 SUPPORTED** (light-FT 한계): full FT (5K-10K step) replication
  yields Δ ≥ 0.05 either direction → POLICY 의 empirical 기반 형성 (방향 결정)
- **Hc_1224 PATH-2 SUPPORTED** (substrate-saturation): replication on chat-cap
  converged substrate yields Δ ≥ 0.05 → BG-LB pretrain 의 specific limit 확인
- **Hc_1224 PATH-3 SUPPORTED** (effect 부재): full FT 도 Δ < 0.03 → identity
  rules truly orthogonal to substrate-aliveness; README #2 POLICY justification 약화

## Honest limits (P-IDR verdict carry)

1. 3-step FT = light-touch probe, full FT 아님
2. simple_stack 0% both → substrate chat-cap 미수렴, evaluation ceiling
3. PIV sub-floor (<0.005) — byte-mod substrate 알려진 한계
4. DCR effect size 0.041 < big_pt threshold 0.05
5. Only 2 trainable layers (LoRA r=16) — adapter-level 미세 변화만

## Cross-link

- PHILOSOPHY.md `## 2026-05-12 (cont. 5) — P-IDR verdict`
- README.md `Philosophy #2 NO IDENTITY RULES`
- state/p_idr_identity_rules_2026_05_12/results_2026_05_12.json
- state/p_idr_identity_rules_2026_05_12/identity_block.txt (10-clause persona)
- docs/anima_proxy_ppl_deprecate_2026_05_09.md §3.1 (PIV sub-floor)
- .roadmap.philosophy D1 (anima identity = 한국어 native + fresh substrate)
