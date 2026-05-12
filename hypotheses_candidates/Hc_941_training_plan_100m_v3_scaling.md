---
id: Hc_941
slug: training-plan-100m-v3-scaling
title: ConsciousLM v3 100M scale-up — 768d/12L/12H, consciousness_dim=256, Φ/cells~0.78 linear scaling, CE spike self-recovery via ratchet+Hebbian (v14.3 DD58)
domain: llm, training, scaling
status: candidate-falsifier-ready
source_doc: docs/training-plan-100m.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_940 (v4 design), Hc_909 (paper-draft), DD58
notes: "ARCHIVED 2026-04-09 — Plan C (AnimaLM 7B/14B/72B) 확정. v14.3 Phi/cells~0.78 linear. 7B eval 5/5, 14B v0.4 완료, 72B v0.5 overfitting 중단."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis

ConsciousDecoderV2 (34.5M, 384d/6L) → V3 (100M, 768d/12L/12H, consciousness_dim=256) scaling 시 v14.3 empirical: Φ scales linearly with cells (Φ/cells ~ 0.78) + CE spikes self-recover via ratchet+Hebbian. n_head 8→12 (64d/head, GQA n_kv_head=4 ratio 3:1), dropout 0.1→0.08 (larger model + larger corpus → less reg needed). block_size 256→512.

## Sub-claims

- v3-CONFIG: 768d, 12L, 12H, GQA 12/4 (3:1), 512 block, consciousness_dim=256
- LINEAR-SCALING: Φ/cells ~ 0.78 linear
- CE-SELF-RECOVERY: ratchet + Hebbian → CE spike self-recover
- DROPOUT-REDUCE: 0.1 → 0.08 (larger corpus less reg)
- N_HEAD-12: 64d per head standard
- PLAN-C-OVERRIDE: AnimaLM 7B/14B/72B 으로 archived

## Migration TODO

- [ ] Φ/cells = 0.78 의 cross-substrate stability
- [ ] AnimaLM 72B v0.5 overfitting 원인 분석
- [ ] 14B v0.5 또는 32B 다음 step 결정
- [ ] consciousness_dim=256 의 SC2 merge threshold cross-link

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: 100M v3 scaling plan: predict pre-train loss curve. If actual loss off by ≥30% → scaling plan calibration failed
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-TRAINING**: Training-plan Hc — predictions about future training runs; require post-run validation. Hc lives in the 'plan' phase, falsifier in the 'execute' phase. Falsifier is essentially the C-list of pre-register checks

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

