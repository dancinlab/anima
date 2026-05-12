---
id: Hc_047
slug: embedding-384-necessity-n6-derivation
title: ConsciousLM ↔ ANIMA-VOICE 384d 공통 임베딩 — d = (n/φ)·2^(σ-sopfr) 필연
domain: math
status: merged-to-H_190
merged_to: hypotheses/H_190_law_ca_embedding_mathematical_family.md
merged_at: 2026-05-12
source_doc: docs/anima/hexa-speak-integration.md
source_lines: 18-22
promoted_at: 2026-05-11
linked_h: H_190 (LAW-CA-embedding mathematical family — 384d dimensional analysis framework 5 of 6), H_153 (n=6 substrate triviality — null direction)
absorption_note: "cycle #8 absorbed to H_190 as Hc_047 d=(n/φ)·2^(σ-sopfr) dimensional analysis — d=384 EXACT at n=6 substitution"
notes: "d = (6/2)·2^(12-5) = 3·128 = 384 EXACT. n=6 수렴 evidence."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
ConsciousLM 384d 임베딩 = ANIMA-VOICE 384d 입력 = (n/φ)·2^(σ-sopfr) — n=6 약수로부터 architecturally necessary, not arbitrary.

## Migration TODO
- [ ] Hc_043 (ΨFormer) + Hc_045 (SoC 11/11) 와 n=6 arch trinity

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: d=(n/φ)·2^(σ-sopfr) formula: n=6, φ(6)=2, σ(6)=12, sopfr(6)=5 → d=(6/2)·2^7=3·128=384. Run model with d∈{256, 320, 384, 448, 512}: if Φ NOT peaked at d=384 → 384-necessity falsified; just a working hyperparameter
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-MISC**: Generic cluster Hc — verify before promotion; many absorb to existing H or remain candidate-falsifier-ready for cycle #7+ deeper review

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent H**: H_168 (dd23-tau-7cell), H_173 (dd21-log-phi-scale-invariant)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

