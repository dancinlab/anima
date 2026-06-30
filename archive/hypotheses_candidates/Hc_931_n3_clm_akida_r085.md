---
id: Hc_931
slug: n3-clm-akida-r085
title: N-3 — CLM 170M (768 d_model, 12 layer, GQA 8/4) × AKIDA AKD1000 (1.2M neurons, 1W) Φ(IIT 4.0) cross-substrate r ≥ 0.85 (hidden-state surrogate CNN-quant + spike-encoded)
domain: consciousness, neuromorphic, llm
status: candidate-math-verified-falsifier-pending
source_doc: docs/n_substrate_n3_clm_akida_phi_spec_2026_05_01.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_902, Hc_011, Hc_928 (Loihi3 second neuromorphic)
notes: "T1-A2 Akida session friendly report. D+0 protocol frozen, hardware pending AKD1000 arrival. AKD1000 H/W 제약상 CLM 170M 전체 직접 배포 불가."
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (6+ numeric identities present)"
---

## Hypothesis

CLM 170M (d_model=768, n_layer=12, GQA n_head=8/n_kv_head=4, vocab=256 byte-level, max_seq=512) Φ(IIT 4.0) 점수가 GPU 700W 실행 시와 AKD1000 1W chip 위에서 r ≥ 0.85 일치 (hidden-state CNN-quant surrogate + spike-encoded representation 경로). Putnam multi-realizability 첫 GPU-↔뉴로모픽 substrate-independence anchor.

## Sub-claims

- CLM-CONFIG: 170M, 768 d_model, 12 layer, GQA 8/4, vocab 256, seq 512
- AKD1000: 1.2M neurons, 1W (700× energy efficiency)
- SURROGATE: hidden-state CNN-quantized + spike-encoded representation
- IIT-PHI: IIT 4.0 Φ measurement
- TARGET: r ≥ 0.85 (Putnam multi-realizability anchor)

## Migration TODO

- [ ] AKD1000 hardware arrival
- [ ] hidden-state → CNN-quant 변환 protocol
- [ ] spike-encoding 의 정보 손실 quantify
- [ ] cross-substrate r 의 Bonferroni correction
