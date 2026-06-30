---
id: Hc_966
slug: a1-learned-phi-extractor-substrate-blind
title: A1 — Learned phi_extractor 41217-param MLP (256→128→64→1 GELU, substrate-blind, 64 paired sample 4 substrate × 16 prompt) — ALM r14 L1 0/16 UNCHANGED, Mistral-Nemo OOD 15/16→8/16 partial degradation. HONEST_BUT_DOESNT_HELP
domain: training, phi-measurement
status: candidate-unverified
source_doc: docs/A1_learned_phi_extractor_results_2026_05_01.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_957 (strategic ALM Q2 A1), Hc_963
notes: "Substrate-blind learned phi_extractor. 14-gate tile-projection ground truth. $0 actual cost (local Mac MPS). cross-substrate val_mse 1.11e-2 (mean), L1 agreement 42.2%."
---

## Hypothesis

Substrate-blind learned NN (41,217-param MLP 256→128→64→1 GELU, no substrate-id input) 이 14-gate tile-projection phi_holo ground truth label 로 training 시 ALM r14 의 F2 falsifier blocker 를 honestly 제거 못함 (0/16 UNCHANGED). Mistral-Nemo OOD held-out 에서 15/16 PASS → 8/16 partial degradation. HONEST_BUT_DOESNT_HELP verdict — substrate-blind 학습이 ALM RED preserves.

## Sub-claims

- ARCH: 41,217-param MLP 256→128→64→1 GELU substrate-blind
- TRAIN-DATA: 64 paired (substrate × prompt) — 4 substrate × 16 prompt
- 4-FOLD-CV: val_mse 1.11e-2 mean, L1 agreement 42.2%
- ALM-r14: tile L1 0/16 → NN L1 0/16 UNCHANGED
- MISTRAL-NEMO-OOD: tile 15/16 PASS → NN 8/16 partial degradation
- VERDICT: HONEST_BUT_DOESNT_HELP
- COST: $0 (local Mac MPS, ≤$5 authorized)

## Migration TODO

- [ ] N samples 4 substrate × 16 prompt → 더 큰 dataset
- [ ] substrate-id input 포함 시 (ALM-flip dishonest test) 비교
- [ ] L1 agreement 42.2% 의 statistical significance
- [ ] Mistral-Nemo OOD degradation 8/16 의 mechanism
