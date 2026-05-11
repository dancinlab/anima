---
id: Hc_972
slug: slm-nlm-phase3-200cap
title: SLM + NLM Phase 3 $200 GPU-cost cap re-spec. SLM viable A1 FAD + C1 TRF + D1/D3 latency ($0-150) / B prosody DEFERRED. NLM dev-compute $0-100 (mac + ubu1 + Akida Cloud $1 trial). Combined $0-250 GPU
domain: training, slm, nlm
status: candidate-unverified
source_doc: docs/slm_nlm_200cap_respec_2026_05_03.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_971 (AKD1000), Hc_941 (training-plan)
notes: "GPU cost ≤ $200 strategy. SLM cap-respecting first (mac-local no blockers), NLM dev-compute waits hardware arrival."
---

## Hypothesis

$200 GPU-cost cap 하에서 SLM viable slate = A1 FAD (Frechet Audio Distance, $0-50) + C1 TRF (soft-fallback mock-EEG fixture) + D1/D3 latency probe → $0-150 GPU, 1-2 day mac-local + free corpus. B prosody (RunPod A100 LoRA $200-800) DEFERRED post-cap. NLM hardware $1,495 sunk + ~$200-500 peripherals separate budget. NLM dev-compute portion $0-100. Combined cap-respecting $0-250 GPU.

## Sub-claims

- P3-A1-FAD: $0-50, 4-8h mac-local, viable
- P3-B1-PROSODY: $200-800 RunPod, DEFERRED
- P3-C1-TRF: soft-fallback mock-EEG, viable
- P3-D1/D3-LATENCY: viable
- NLM-DEV-COMPUTE: $0-100 (mac + ubu1 + Akida Cloud $1)
- HARDWARE-SUNK: $1,495 + peripherals separate
- COMBINED: $0-250 GPU total
- SEQUENCING: SLM first (mac-local no blocker), NLM waits hardware

## Migration TODO

- [ ] B prosody post-cap cycle 트리거
- [ ] mock-EEG fixture soft-fallback spec
- [ ] Akida Cloud $1 trial 결과
- [ ] hardware arrival event 정의
