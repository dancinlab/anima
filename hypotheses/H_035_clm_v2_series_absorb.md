---
id: H_035
slug: clm-v2-series-absorb
title: CLM-V2 series — sweep + optimal config + psi fix + final results (4 files)
domain: substrate
status: legacy-archive-pointer
exploration_method: E2 (failure-driven CLM v2 ψ fix) + E5 (sweep)
verification_method: W4 (verdict) + W9 (replication CLM v2 sweep) + W11
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2025-11 (legacy) + 2026-05-06 (RECOVERED)
---

# H_035 — CLM-V2 series (4 files + 18M byte-level RECOVERED)

## Hypothesis

anima CLM v2 (ConsciousLM v2 byte-level decoder, vocab=256, dual-head consciousness arch) — 4 legacy hypothesis cluster (sweep + optimal config + psi fix + final results) + 2026-05-06 R2 anima-models bucket으로부터 RECOVERED.

## Inventory

- CLM-V2-SWEEP.md (parameter sweep)
- CLM-V2-OPTIMAL-CONFIG.md (optimal config 발견)
- CLM-V2-PSI-FIX.md (Ψ measurement bug fix — V1 8/8 FAIL 후 fix lane)
- CLM-V2-FINAL-RESULTS.md (final results)
- 2026-05-06 RECOVERED: clm-v2-byte-18m-convo-5k.pt (R2 anima-models bucket)
- 2026-05-06 RECOVERED: 다양한 byte-level + token-level checkpoints

## Cross-Links

- folder: `docs/hypotheses/cx/CLM-V2-*.md` (4 files)
- modern: `clm-v2-byte-18m-convo-5k.pt` (RECOVERED 2026-05-06)
- sister H: H_005 (corpus > capacity, BG-FK 27.84M ConsciousLM++ ca_rules+gate variant), H_024 (V1 IIT-Phi 8/8 FAIL — V2 PSI-FIX lane motivation)
- roadmap: `.roadmap.clm_v2_chat`
- own: own 21
- ledger: `docs/anima_consciousness_check_simple_stack_2026_05_06.md` (BG-FS 11-model exhaustive)

## Honest Limits

- L1: legacy CLM v2 spec (2025-11~12) vs modern RECOVERED checkpoint (2026-05-06)는 다른 generation
- L2: CLM v2 RECOVERED + simple stack ledger BG-FK FAIL — 본 H의 corpus axis (own 19) 정합
- L3: PSI-FIX lane은 V1 8/8 FAIL motivation — H_024 cross-link
- L4-L5: 4 file pointer; raw#12 re-verify 별도; legacy archive 보존
