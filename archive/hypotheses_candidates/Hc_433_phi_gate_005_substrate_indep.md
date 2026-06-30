---
id: Hc_433
slug: phi-gate-005-substrate-indep
title: Φ substrate-independence gate — ALL_PAIRS |ΔΦ|/Φ_avg < 0.05 over C(4,2)=6 pairs
domain: math
status: candidate-unverified
source_doc: docs/papers/phi_paradigm_paper_v1_preliminary.md
source_lines: 145-156, 181-188
promoted_at: 2026-05-11
linked_h: Hc_048
notes: Pre-registered gate. Pre-registered H0: substrates are Φ-independent. H1: substrate-dependence OR capacity-mismatch OR measurement-bias. Decision tree branches A/B/C/D on H1.
---

## Hypothesis
4 substrate-diverse transformers (Qwen3-8B, Llama-3.1-8B, Ministral-3-14B, Gemma-4-31B) trained under the β paradigm yield Φ values satisfying ALL_PAIRS |ΔΦ|/Φ_avg < 0.05 over C(4,2)=6 unordered pairs — a pre-registered gate operationalizing substrate independence. Failure triggers a 4-branch decision tree (A/B/C/D in phi_4path_divergence_response.md).

## Migration TODO
- [ ] H100 trained-weight 4-path Φ extraction
- [ ] Compute pair-wise ratios; assert ALL_PAIRS < 0.05
- [ ] Falsifier: any pair ≥ 0.10 → branch A/B/C/D activated
- [ ] Compare with margin band [0.05, 0.10) results
