---
id: Hc_617
slug: phi-star-option-d-pyphi-antropy-anchor
title: Option D — PyPhi big-phi + AntroPy entropy-rate 가 architecturally principled IIT phi proxy
domain: clm-architecture
status: merged-to-H_174
merged_at: 2026-05-12
merged_to: hypotheses/H_174_phi_star_geometry_aliasing_clm_v4_specific.md
absorption_note: "Option D (PyPhi big-phi + AntroPy entropy-rate) is one of 3 candidate Φ* proxy designs proposed to address H_174's D-mod-192 aliasing. Rank 2 highest precision, conditional on PyPhi convergence at n=8 binary nodes. F-list/L-list preserved here for H_174 C-list extension."
source_doc: docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md
source_lines: 224-263
promoted_at: 2026-05-11
linked_h: Hc_614, BG-BB queue
notes: Rank 2 highest precision, conditional on PyPhi convergence. n=8 binary nodes 256-state TPM 2^256 partition search → subsystem decomposition required.
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Discretize hidden state into N=8 binary nodes (threshold/k-means) → empirical TPM → PyPhi major_complex_phi 가 IIT 3.0 big-phi 의 architecturally principled approximation. AntroPy entropy_rate ~10ms fast-fallback.

## Falsifiable Tests
- Test D.1: PyPhi big-phi 가 mac CPU 30-300s budget 내 수렴
- Test D.2: 5-substrate big-phi ordering 이 paradigm v11 G3 ordering 과 일치
- Test D.3: AntroPy fast-fallback 이 big-phi 와 rank correlation ≥ 0.7

## Migration TODO
- [ ] BG-BB cycle PyPhi+AntroPy land 후 진행
- [ ] discretization method 선택 (threshold vs k-means)
- [ ] subsystem decomposition (major-complex restriction) tract impl

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: Phi* PyPhi+antropy: if Phi* differs from PyPhi+antropy by ≥30% on shared substrates → 'anchor' identity claim falsified
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-PHI-STAR**: Φ* (phi-star) Hc — pre-cycle-4 candidate cluster; multiple competing definitions (option a/b/d); requires pre-register-which-definition before any sub-Hc verifies

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent H**: H_174 (Φ*-geometry-aliasing-clm-v4-specific — direct relevance)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

