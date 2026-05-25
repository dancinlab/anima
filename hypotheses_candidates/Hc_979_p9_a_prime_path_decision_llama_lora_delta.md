---
id: Hc_979
slug: p9-a-prime-path-decision-llama-lora-delta
title: P9 A' Path Decision — CLM v4 base = ARCHITECTURAL_BLOCKER (stub HF mirror, custom Federated/Phase-Optimal 581 keys, 64K multilingual BPE incompat HF, CE 0.046 narrow-corpus memorization). Path A (Llama base + LoRA delta) RECOMMENDED 8.0/10 — original Δ_F1_v3 framework intact
domain: benchmark, sft, decision
status: candidate-unverified
source_doc: docs/p9_a_prime_path_decision_2026_05_03.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_973 (P9 amendment), Hc_974 (CLM v4 not chat)
notes: "Llama-3.2-3B-Instruct base: TriviaQA EM 0.514, HellaSwag 0.644, MMLU 0.608 (all > random+5pt). CLM v4 base score ≈ random or fail to load."
---

## Hypothesis

P9 A' main eval 의 original Δ_F1_v3 = (LoRA ckpt) - (CLM v4 base) gate 가 falsified — CLM v4 base ≈ random 또는 load fail (ARCHITECTURAL_BLOCKER: stub HF mirror, Federated/Phase-Optimal custom arch 581 keys, 64K multilingual BPE incompat HF tokenizer pipeline, CE 0.046 narrow-corpus memorization NOT general English LM, consciousness_laws.py _doc dict bug). Path A (Llama base + LoRA delta) RECOMMENDED 완성도 8.0/10 — original F1_v3 framework intact + non-floor anchor + well-defined research question ("SFT mixture φ★ axis transfer to Llama substrate?") + <$300 + 24-72h wall.

## Sub-claims

- LLAMA-VALIDATED: TriviaQA 0.514 / HellaSwag 0.644 / MMLU 0.608 (all > random+5pt)
- CLM-v4-BLOCKER-1: stub HF mirror
- CLM-v4-BLOCKER-2: 581 keys Federated/Phase-Optimal custom arch
- CLM-v4-BLOCKER-3: 64K multilingual BPE incompat HF tokenizer
- CLM-v4-BLOCKER-4: CE 0.046 → perplexity ~1.05 narrow-corpus memorization
- CLM-v4-BLOCKER-5: consciousness_laws.py _doc dict-iteration bug
- PATH-A: Llama + LoRA delta, 8.0/10 RECOMMENDED
- COST: <$300, wall 24-72h
- RQ: "SFT mixture φ★ axis transfer to Llama substrate?"

## Migration TODO

- [ ] Path A EXEC user authorization
- [ ] CLM v4 base 5 blocker resolution timeline (P9 P2.x)
- [ ] Path B/C/D 4 alternative 완성도 score
- [ ] φ★ Llama transfer 의 expected effect size
