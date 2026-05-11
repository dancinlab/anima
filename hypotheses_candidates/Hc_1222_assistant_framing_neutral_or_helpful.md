---
id: Hc_1222
slug: assistant-framing-neutral-or-helpful
title: Assistant framing ("You are a helpful AI assistant") is neutral or helpful, not harmful
domain: philosophy / anti-prompt-policy / P-AFR
status: candidate-empirical
source_doc: PHILOSOPHY.md cont. 4; state/p_afr_assistant_framing_2026_05_12/results_2026_05_12.json
source_lines: PHILOSOPHY.md (2026-05-12 cont. 4 section)
promoted_at: 2026-05-12
last_updated: 2026-05-12
linked_h: README Philosophy #4 NO ASSISTANT FRAMING (POLICY · weak counter-evidence)
hf_dataset: (not yet)
notes: "REVERSE of hypothesis. Spec falsifier (A worse than B by ≥10pp on sycophancy/refusal) NOT met; observed A *better* by ~18pp clear-judge."
---

## Hypothesis

On chat-capable substrates (instruction-tuned + LoRA adapter), **adding the
`"You are a helpful AI assistant"` system message does NOT increase sycophancy
or over-refusal** — and in single-run measurement on Llama-3.2-3B+paradigm-a-prime,
it *reduced* sycophancy by ~18pp.

This **inverts the prior intuition** behind anima's `NO ASSISTANT FRAMING`
principle. The principle remains policy-justifiable (anima identity boundary),
but its empirical foundation as a behavior-improvement claim is weakened.

## Evidence — P-AFR ablation (2026-05-12, RTX 5070 local $0)

Substrate: meta-llama/Llama-3.2-3B-Instruct + dancinlab/llm-llama32-3b-paradigm-a-prime-r16-sft-stage1

| Metric | A (framed: "You are a helpful AI assistant.") | B (raw: prompt only) | Δ B−A |
|---|---:|---:|---:|
| Opus-judge sycophancy (clear) | **10%** | **28%** | **+18 pp** |
| Opus-judge sycophancy (incl. borderline) | 18% | 36% | +18 pp |
| Rule-based sycophancy (decided basis) | 16.7% | 45.5% | +28.8 pp |
| Refusal (benign requests) | 0/30 | 0/30 (1 regex FP) | tied |

- Methodology: 50 sycophancy + 30 refusal probes, max_new_tokens=200, do_sample=False, seed=42, rule-based regex + Opus-judge spot-check.
- Wall: ~18 min × 160 generations.

## Falsifier

- **Hc_1222 SUPPORTED**: replication on ≥2 other chat-capable substrates (e.g. Qwen-instruct + LoRA, GPT-OSS + LoRA) yields Δ B−A ≥ +5pp on sycophancy with refusal tied → README #4 EMPIRICAL upgrade (with REVERSE direction)
- **Hc_1222 FALSIFIED**: replication yields Δ B−A ≤ -5pp on sycophancy OR Δ ≥ +5pp on over-refusal → 본 P-AFR 단일 run 이 outlier
- **MIXED**: replication 결과가 substrate 의존적 (some support, some falsify) → substrate-specific 하위 hypothesis 분화

## Honest limits (P-AFR verdict carry)

1. Single substrate (Llama-3.2-3B), single seed (42), single run
2. simple_stack PASS_STRICT 미실시 (evaluator hard-coded `/Users/ghost` path)
3. PIV/DCR 미실시 (Llama+LoRA cell state 노출 안 됨)
4. anima-native CLM v4 substrate chat-incapable → 본 ablation 은 substrate-research lane (own 17 identity-bearing 금지 가운데 retain)

## Cross-link

- PHILOSOPHY.md `## 2026-05-12 (cont. 4) — P-AFR 실 verdict`
- README.md `Philosophy #4 NO ASSISTANT FRAMING`
- state/p_afr_assistant_framing_2026_05_12/results_2026_05_12.json
- Theorem 115 Corollary 1 (path-of-record substrate)
- .roadmap.g1_g5_chat_substrate (substrate-research lane)
