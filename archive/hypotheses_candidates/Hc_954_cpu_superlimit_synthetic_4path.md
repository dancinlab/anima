---
id: Hc_954
slug: cpu-superlimit-synthetic-4path
title: F axis — htz CPU synthetic 4-path Φ measurement (Gaussian random weight surrogate, seeded). |ΔΦ|/Φ_avg < 0.05 ALL 6 pairs gate pre-signal. measurement geometry path-dependent bias 검증
domain: phi-measurement, methodology
status: candidate-unverified
source_doc: docs/upstream_notes/cpu_superlimit_synthetic_4path_proposal_20260422.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_934 (7-axis F), H100 #83 launch
notes: "H100 #83 launch 전 substrate independence pre-signal. NO H100, NO real corpus, NO weight training. $0 (htz already-paid CPU)."
---

## Hypothesis

H100 × 4 launch (#83) gate `|ΔΦ|/Φ_avg < 0.05` (ALL 6 pairs) 의 pre-signal 을 htz CPU synthetic 4-path Φ measurement 으로 확보 가능. 핵심 가설: Φ measurement 자체가 substrate-independent numerical signature 를 가지면 random/synthetic weight 도 4-path Φ patterned divergence 보임 → CPU 분포가 H100 실측 envelope.

## Sub-claims

- p1: random Gaussian 8B (seed 0xCA75E1) — Qwen3-8B surrogate
- p2: random Gaussian 8B (seed 0xCA75E2) — Llama-3.1-8B surrogate
- p3: random Gaussian 14B (seed 0xCA75E3) — Ministral-3-14B surrogate
- p4: random Gaussian 31B (seed 0xCA75E4) — Gemma-4-31B surrogate
- STRATIFIED-SUB-SAMPLE: 32M random subset 실측, capacity normalization (Δφ/trainable_params_exact)
- ANTI-HYPOTHESIS: synthetic Φ ≠ trained Φ surrogate (단순 noise floor + path-dependent geometric bias)
- GATE-PRE-SIGNAL: |ΔΦ|/Φ_avg < 0.05 satisfied on synthetic?

## Migration TODO

- [ ] CPU synthetic 결과 분포 vs H100 실측 envelope
- [ ] capacity normalization formula 정당성
- [ ] family_axis = Gaussian uniform 시 path-dependent geometric bias 정량화
- [ ] D1-D5 decision tree pre-trigger
