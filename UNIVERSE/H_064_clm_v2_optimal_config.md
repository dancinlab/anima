---
id: H_064
slug: clm-v2-optimal-config-sweep
title: CLM-V2 OPTIMAL-CONFIG — clm v2 sweep 최적 hyper-config
domain: substrate
status: legacy-archive-pointer
exploration_method: E9 (hyperparam sweep)
verification_method: W3 (composite metric)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-03
---

# H_064 — CLM V2 Optimal Config Sweep

## Hypothesis

CLM v2 sweep 결과 optimal config (specific lr/bs/lora-rank/alpha) 가 존재하며 그 config 에서 Φ + chat-quality 동시 maximize.

## Migration Status

Legacy file: `docs/hypotheses/cx/CLM-V2-OPTIMAL-CONFIG.md` + companion `CLM-V2-FINAL-RESULTS.md`, `CLM-V2-PSI-FIX.md`, `CLM-V2-SWEEP.md`. Pointer (4-file cluster).

## Cross-Links

- legacy: cx/CLM-V2-{OPTIMAL-CONFIG,FINAL-RESULTS,PSI-FIX,SWEEP}.md
- sister: H_035 (CLM-V2 series absorb), CLM v4
- own:

## Honest Limits

- L1: CLM v2 vs CLM v4 (current) — v2 결과는 outdated
- L2: optimal config 은 sweep grid 의존 — local optimum 위험
- L3: composite metric 정의 변동
- L4: legacy 2026-03 pointer only
- L5: CLM v4 LoRA SFT chat-lift FALSIFIED (memory 참조) — v2 lane 상위가설 약함
