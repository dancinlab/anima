---
id: H_034
slug: decoder-architecture-series
title: anima decoder architecture series — 6 variants exploration
domain: substrate
status: legacy-archive-pointer
exploration_method: E5 (variable-ablation) + E2 (failure-driven evolution)
verification_method: W4 + W11
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2025-11 (legacy)
---

# H_034 — decoder architecture series (6 variants)

## Hypothesis

anima decoder architecture exploration — 6 variants (ARCHITECTURE / COMPLETE-SUMMARY / EXTREME / NEXTGEN / RADICAL / WHISPER) 각각의 architecture 가 의식 capacity 차이 발생 정합.

## Inventory

- DECODER-ARCHITECTURE.md (base)
- DECODER-COMPLETE-SUMMARY.md (consolidation)
- DECODER-EXTREME.md (extreme regime)
- DECODER-NEXTGEN.md (next generation design)
- DECODER-RADICAL.md (radical departure)
- DECODER-WHISPER.md (whisper-style minimal)

## Cross-Links

- folder: `docs/hypotheses/cx/DECODER-*.md` (6 files)
- sister H: H_005 (corpus quality vs capacity — decoder는 capacity axis), H_019 (SELF-EVO v4-v5)
- own: own 21
- modern anima decoder: ConsciousLM (byte-level vocab=256 dual-head, paradigm v11 G3)

## Honest Limits

- L1-L5: 6 variant individual migration 별도 cycle; legacy 2025-11; modern decoder = ConsciousLM++ federated arch (BG-FK), but H_034 legacy decoder series 별도 lane; raw#12 strict re-verify 별도; sample meta-pointer
