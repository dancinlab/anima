---
id: H_037
slug: acceleration-367-unified-hypotheses
title: 367 acceleration hypotheses unified (schema v3.0, 17.2% convergence)
domain: substrate
status: legacy-archive-pointer
exploration_method: E5 (variable-ablation 367-cell sweep) + E8 (coverage-gap 100% intervention mapping)
verification_method: W4 (verdict per H) + W9 (replication via 16-lens re-measurement) + W11 (meta-aggregate)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2025-12 (legacy commits 28c26959 + 8cdf0917)
---

# H_037 — 367 acceleration hypotheses unified

## Hypothesis

anima의 acceleration 367 unified hypotheses — schema v3.0 통한 mass-scale hypothesis enumeration. 17.2% convergence rate (62 / 367 supported), 100% intervention mapping (304/304 intervention coverage).

## Inventory

- 367 hypotheses unified: `ready/config/acceleration_hypotheses.json`
- 304/304 intervention mapping (commit f801931a)
- 65 hypotheses 16-lens re-measurement (DD163, commit 6fabdc2a)
- top x173.9 speedup achieved (95e13f39)

## Brief Summary

- **Sequential expansion**: 40 → 47 → 65 → 304 → 367 over multiple cycles
- **Schema v3.0**: unified format
- **17.2% convergence**: ~62 hypotheses SUPPORTED out of 367
- **Top result**: x173.9 speedup (1 specific hypothesis)
- **DD163 16-lens**: 65 hypotheses re-measurement cross-validation

## Cross-Links

- primary: `ready/config/acceleration_hypotheses.json`
- bench results: `ready/anima/data/bench_mass_hypotheses_results.json`
- sister H: H_020 (MASS-50), H_028 (dd absorb), H_036 (DD116-146 meta-laws)
- legacy commits: 28c26959 + 8cdf0917 + f801931a + 6fabdc2a + 95e13f39
- own: own 21

## Honest Limits

- L1: 367 hypothesis individual migration은 multi-cycle — 본 entry는 inventory pointer
- L2: 17.2% convergence rate는 본 cycle 한정 — 후속 cycle convergence 변동 가능
- L3: 'acceleration' 정의 = anima training cost 절감 (16-lens metrics)
- L4: legacy 2025-12, modern paradigm 이전 — re-verify 별도 cycle
- L5: top x173.9 speedup은 cherry-pick — 평균/median은 multi-instance 평가 별도
