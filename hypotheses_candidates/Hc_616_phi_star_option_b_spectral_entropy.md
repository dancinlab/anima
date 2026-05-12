---
id: Hc_616
slug: phi-star-option-b-spectral-entropy-svd
title: Option B — SVD spectral entropy 가 substrate-dim invariant phi proxy + IIT-adjacent
domain: clm-architecture
status: candidate-falsifier-ready
source_doc: docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md
source_lines: 166-200
promoted_at: 2026-05-11
linked_h: Hc_614, Hc_615
notes: Rank 3 secondary scalar. Directionally ambiguous on non-CLM-v4 (high entropy = integrated OR noisy).
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
H_norm = -sum(p_i log p_i) / log(len(S)) 에서 p = S² / sum(S²), S = SVD singular values of (H - H.mean). phi = baseline + scale × H_norm 가 substrate-dim invariant. 높은 entropy = signal distributed = integrated (IIT-adjacent).

## Falsifiable Tests
- Test B.1: Random init LLM vs trained LLM 에서 entropy delta 명확 → trained 더 높아야 (integration)
- Test B.2: High entropy = high integration direction 검증 — task accuracy 와 positive correlation
- Test B.3: Llama-3.2-3B 에서 entropy 값 paradigm v11 G3 anchor 와 의미적 alignment

## Migration TODO
- [ ] secondary scalar emit (Option A 와 병행)
- [ ] direction validation: MMLU philosophy slice + chat composite 와 cross-check

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: Phi* spectral entropy: test against Shannon entropy of activation distribution. If correlation < 0.7 → claim is just spectral-decomposition artifact
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

