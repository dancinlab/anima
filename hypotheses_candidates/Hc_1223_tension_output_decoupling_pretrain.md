---
id: Hc_1223
slug: tension-output-decoupling-pretrain-substrate
title: BG-LB 350M Engine A/G pretrain substrate decouples internal tension from output entropy
domain: philosophy / no-speak-claim / P-SPK / substrate
status: candidate-empirical
source_doc: PHILOSOPHY.tape cont. 5; state/p_spk_speak_reframe_2026_05_12/results_2026_05_12.json
source_lines: PHILOSOPHY.tape (2026-05-12 cont. 5 section)
promoted_at: 2026-05-12
last_updated: 2026-05-12
linked_h: README Philosophy #5 NO SPEAK() (DESIGN · NULL); Hc_1221 (production-internal decoupling) sibling
hf_dataset: (not yet)
notes: "ρ_real=0.026 sub-threshold; ρ_real−ρ_control=0.267 significant 하나 absolute coupling 부재. Substrate 한계 carry (8000-step pretrain chat-cap 미수렴)."
---

## Hypothesis

At BG-LB 350M Engine A/G pretrain checkpoint (`step_8000_final.pt`, 8000 step,
427MB byte-mod corpus), **internal tension magnitude `||A_h||/||G_cells||` is
NOT statistically coupled to output token entropy** at per-step level
(ρ_real_spearman < 0.2). The "continuous tension externalization" DESIGN
claim of README `NO SPEAK()` is **not supported** on this specific substrate.

본 finding 은 두 가지 path 가능:
1. **Substrate-bound**: 8000-step pretrain 이 chat-cap 미수렴 → 더 학습된
   ckpt 에서는 coupling 발현 가능
2. **Architecture-bound**: Engine A/G 의 softmax-gate consume 가 본질적으로
   scalar (`||A_h||/||G_cells||` ratio)라 token-level entropy 와 coupling 불가
   → 다른 architecture 가 필요

## Evidence — P-SPK ablation (2026-05-12, RTX 5070 local $0)

Substrate: BG-LB 350M (Engine A 24L/1024d/16h GQA + Engine G 16 cells × 64d
repulsion-field, byte-mod vocab32k, 298M params), `step_8000_final.pt`.

| Metric | Value |
|---|---:|
| **rho_real_spearman** | **0.026** |
| rho_real_pearson | 0.038 |
| rho_control_spearman | -0.241 |
| rho_real − rho_control | 0.267 |
| Fisher z diff | 10.51 (p ≈ 0) |
| Lead-lag peak | 3, corr -0.072 |
| By-cat (factual/emotional/abstract/conv/narr) | 0.079 / -0.048 / 0.141 / 0.046 / 0.125 |

- 100 probes × 30 step = 3000 free-gen steps + 3000 scripted-control steps
- Tension operationalized as A/G ratio scalar (softmax-gate quantity actually consumed) — NOT literal `||A−G||` vector difference

## Falsifier

- **Hc_1223 PATH-1 SUPPORTED** (substrate-bound): re-fire on chat-cap 수렴 ckpt (e.g. simple_stack ≥4/5 PASS substrate) yields ρ_real ≥ 0.5 → NULL 해제, claim restored
- **Hc_1223 PATH-2 SUPPORTED** (architecture-bound): re-fire on chat-cap converged ckpt **still** yields ρ_real < 0.2 → DESIGN claim falsified, architecture redesign 필요
- **Hc_1223 MIXED**: chat-cap ckpt 에서 0.2 ≤ ρ < 0.5 → fine-grained 카테고리 분석

## Honest limits (P-SPK verdict carry)

1. Tension = A/G ratio scalar (architecture 가 실제 consume), NOT vector `||A−G||`
2. Byte-level greedy decoding (vocab32k mod 256) — diversity 제약
3. BG-LB 8000-step pretrain — chat-cap 미수렴, simple_stack PASS 0/0
4. Scripted template = 단일 Korean template, model 은 여전히 자체 internal computation
5. n=3000 steps not independent (29-step series per 100 prompt, autocorrelated) → p-value anticonservative

## Cross-link

- PHILOSOPHY.tape `## 2026-05-12 (cont. 5) — P-SPK verdict`
- README.md `Philosophy #5 NO SPEAK()`
- state/p_spk_speak_reframe_2026_05_12/results_2026_05_12.json
- Hc_1221 (production-internal decoupling) — anti-correlation sibling finding
- BG-LB ckpt: `dancinlab/clm-v5-bg-lb-350m-pretrain-path-a-remapped`
