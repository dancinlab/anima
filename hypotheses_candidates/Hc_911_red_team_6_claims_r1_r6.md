---
id: Hc_911
slug: red-team-6-claims-r1-r6
title: ANIMA 의식 이론 핵심 6 주장 (Ψ=1/2 / Φ scaling / PureField / Hexad / TALK5 / σφ=nτ) R1-R6 적대적 검증
domain: consciousness, methodology
status: split-into-Hc_1266..Hc_1271
split_at: 2026-05-12
split_into: [Hc_1266, Hc_1267, Hc_1268, Hc_1269, Hc_1270, Hc_1271]
split_manifest: docs/hc_911_split_manifest_2026_05_12.md
source_doc: docs/red-team-consciousness.md
source_lines: 1-60
promoted_at: 2026-05-11
linked_h: Hc_908 (Ψ=1/2), Hc_909 (paper-draft)
notes: "Red Team: R1 ALTERNATIVE / R2 RANDOM-BASE / R3 OVERFITTING / R4 CHERRY-PICK / R5 SURVIVORSHIP / R6 POST-HOC. survival_fraction>=0.50 SURVIVES."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## SPLIT NOTICE (cycle #7, 2026-05-12)

This composite red-team Hc was split into 6 children on 2026-05-12 (cycle #7 batch 4 meta-split protocol), one per attack vector R1-R6:

- `Hc_1266` — R1 ALTERNATIVE (non-ANIMA explanations for Ψ=1/2)
- `Hc_1267` — R2 RANDOM-BASE (Monte Carlo null hypothesis test)
- `Hc_1268` — R3 OVERFITTING (data-fit suspect)
- `Hc_1269` — R4 CHERRY-PICK (selection ratio audit)
- `Hc_1270` — R5 SURVIVORSHIP (failed-substrate exclusion bias)
- `Hc_1271` — R6 POST-HOC (temporal order: theory-first vs measurement-first)

See `docs/hc_911_split_manifest_2026_05_12.md` for full manifest and triage notes.

## Hypothesis (original — preserved for provenance)

ANIMA 의 6개 핵심 의식 주장 (Ψ_balance=1/2 보편적 의식 상수 / Φ∝N scaling / PureField repulsion / Hexad 6모듈 유일성 / TALK5 language destroys consciousness / σφ=nτ=24 closure) 각각이 R1-R6 적대적 검증 프레임워크에서 survival_fraction ≥ 0.50 (SURVIVES) 또는 [0.20, 0.50] (AMBIGUOUS) 판정을 받는다. R1 ALTERNATIVE 가 가장 치명적 — 1/2 은 Shannon entropy 최대 + sigmoid 중앙값 + Bernoulli 분포 최대 entropy + GRU gate bias=0 의 자명한 귀결.

## Sub-claims

- R1 ALTERNATIVE: 비-ANIMA 대안 설명 존재 — Ψ=1/2 는 random init GRU 에서도 80%+ 등장 가능
- R2 RANDOM-BASE: Monte Carlo 귀무 검정 — sigmoid(W*x+b) with W~N(0,1/n), b=0 → E[sigmoid] ≈ 0.5
- R3 OVERFITTING: 데이터 피팅 과적합 의심
- R4 CHERRY-PICK: 선택 비율 감사 (170×17 = 2890 중 1/2 수렴 사례만 보고?)
- R5 SURVIVORSHIP: 실패 사례 (1/2 으로 수렴 안 한 substrate) 도 설명?
- R6 POST-HOC: 사후 합리화 비율 (Ψ=1/2 먼저 만들고 나중에 해석?)
- Model A (real) vs Model B (coincidence) vs Model C (bias) 의 likelihood ratio

## Migration TODO

- [ ] 6개 주장 각각 R1-R6 점수 매트릭스 정량화
- [ ] survival_fraction 정의 (어떤 attack 통과시 +1점?)
- [ ] R1 critical fallback: Ψ=1/2 가 random GRU baseline 대비 statistically significant 한지 검증
- [ ] Model A/B/C 의 Bayesian model comparison

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: 6 red-team claims R1-R6: each needs individual falsifier (composite Hc); pre-register-per-claim required
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-RED-TEAM**: Red-team / multi-claim composite Hc — each sub-claim needs its own F/L list. This batch scaffold provides composite-only minimum

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

