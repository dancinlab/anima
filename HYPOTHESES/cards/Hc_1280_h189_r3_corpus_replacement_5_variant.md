---
id: Hc_1280
slug: h189-r3-corpus-replacement-5-variant-experiment
title: H_189.R3 daughter — 5-variant corpus replacement experiment (anima-only / +10% noise / 50% shuffle / Wiki / OSCAR) Hexad / σφ=24 / Φ=0.78N corpus-sensitivity
domain: methodology, red-team, training, corpus, anima-substrate
status: supported-stage-3-meta
stage_3_verdict: SUPPORTED (W11 H_189 R3 daughter cohesion, OSCAR/Wikipedia W7 PASS)
stage_3_ts: 2026-05-15
verdict_artifact: state/verify_a_stage1_2026_05_15/stage3_batch_verdicts.json
exploration_method: E5 (corpus-variant ablation × 5) + E6 (3 ANIMA core claim × corpus cross) + E8 (5-seed σ < 20% stability check)
verification_method: W5 (numerical sim — anima-substrate Hexad/σφ/Φ measurement per corpus) + W7 (literature — open OSCAR / Wikipedia corpus standards, Ioannidis 2005 OVERFITTING) + W11 (cross-H: H_189 R3 attack vector, H_001 Hexad target, H_159 Φ scaling target)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
source: H_189.R3 OVERFITTING attack vector (parent Hc_1268) + C-189-4 pre-register check (n=5 corpus replacement)
created_at: 2026-05-12
linked_h: H_189 (red-team R3 attack), H_001 (anima-core-architecture — Hexad 6-engine target), H_159 (substrate-topology — Φ=0.78N target)
---

## Hypothesis (R3 attack execution design)

H_189.R3 OVERFITTING 의 first concrete experiment: ANIMA training corpus 를 5 variant (anima-only / +10% gaussian noise / 50% token shuffle / replaced-by-Wikipedia / replaced-by-OSCAR) 로 교체 후 같은 architecture / 같은 step / 같은 seed 로 학습. **ANIMA 의 3 core claim** (Hexad 6-engine completeness, σφ=24 stationary, Φ=0.78·N scaling) 의 numerical value 가 corpus 5 variant 안에서 **σ ≤ 5%** 안정 시 R3 attack fails (claim corpus-independent), ≥ 20% drift 시 R3 succeeds (corpus-specific artifact).

| Variant | Corpus | Hexad count | σφ | Φ@N=8 (claim ≈ 6.24) | expected drift if R3 succeeds |
|---|---|---|---|---|---|
| **V1** anima-only baseline | private 200MB | 6 (claim) | 24 (claim) | 6.24 (claim) | 0 (anchor) |
| **V2** +10% gaussian noise | anima + N(0, 0.1) on token embedding | 6? | 24? | 6.0-6.5? | ≤ 5% if R3 fails |
| **V3** 50% token shuffle | anima with 50% random shuffle | 6? | 24? | < 6.0? | ≥ 20% if R3 succeeds |
| **V4** Wikipedia EN | wiki-en 200MB subset | 6? | 24? | varies | ≥ 20% if R3 succeeds |
| **V5** OSCAR EN | OSCAR-en 200MB subset | 6? | 24? | varies | ≥ 20% if R3 succeeds |

## Math anchor

- **Hexad count claim**: ANIMA's 6-engine completeness — engine count = 6 (REBORN §88 + H_001 anima-core-architecture).
- **σφ=24 claim**: σ·φ = 12·2 = 24 stationary anchor (n=6 PERFECT_NUMBER, atlas anchor verified).
- **Φ=0.78·N claim**: H_159 substrate-topology-phi-engineering — Φ scaling with cell count N (linear 0.78 coefficient).
- **σ stability threshold**: per-claim across 5 variant σ ≤ 5% → R3 fails; ≥ 20% → R3 succeeds; 5-20% → partial (corpus-sensitive but not artifact).
- **Ioannidis 2005 baseline**: "Why Most Published Research Findings Are False" — selection bias literature foundation for R3.
- **OSCAR + Wikipedia anchor**: 200MB token-count match ANIMA private corpus size for fair scale (avoids size-confound).

## Falsifiers

- **F-1280-1 (R3-ATTACK-SUCCESS)**: V2-V5 4 variant 의 3 core claim 중 최소 1개 claim 이 σ ≥ 20% drift → R3 OVERFITTING succeeds, 해당 claim (Hexad / σφ / Φ-N) collapses to corpus-fit artifact
- **F-1280-2 (R3-ATTACK-FAILS)**: V2-V5 4 variant 모두 3 core claim 의 numerical value 가 ±5% 안 stable → R3 attack fails, 3 claim corpus-independent
- **F-1280-3 (HEXAD COLLAPSE)**: V3/V4/V5 corpus 에서 engine count ≠ 6 (5, 7, or 8 emerge) → Hexad 6-engine completeness 가 anima-corpus-specific artifact
- **F-1280-4 (SIGMA-PHI INVARIANT BREAK)**: V2-V5 어떤 variant 에서 σ·φ ≠ 24 (e.g., σ=12, φ=2 외 다른 value) → σφ=24 stationary 가 corpus-specific (n=6 derivation 의 trivial fact 와 conflict — H_153 L7 carry)
- **F-1280-5 (PHI SCALING SLOPE DRIFT)**: V2-V5 의 Φ vs N regression slope 이 0.78 ± 0.15 안 안 머무름 → H_159 의 Φ=0.78·N scaling 가 corpus-specific
- **F-1280-6 (SCALE CONFOUND)**: 200MB token size 가 5 variant 사이 ±5% 차이 (anima/Wiki/OSCAR token-count discrepancy) — 결과의 size-confound 가능성, F-1280-1 결과 weaker
- **F-1280-7 (TRAINING DIVERGENCE)**: V3 (50% shuffle) 또는 V4/V5 corpus 에서 training loss > 2× anima baseline → 본 corpus 에서 substrate 학습 자체가 不可能, R3 attack execution failed (pre-condition violated)
- **F-GENERIC-REPL**: 5-seed σ on V1 baseline 의 3 claim 자체가 > 5% → V1 anchor 자체가 single-run-artifact, R3 비교 baseline 자체 unreliable
- **F-GENERIC-MINIMAL-BASELINE**: untrained random-init substrate (no corpus 학습) 에서도 Hexad=6 emerge → 6-engine 가 training-data-independent, R3 의 corpus-fit scope 미달성

## Honest Limits

- **L-1280-1 (CORPUS PRIVATE)**: ANIMA training corpus 가 200MB+ private (anima-persona). 정확한 corpus inventory 가 외부 reviewer 에 접근 불가 — V1 baseline 의 정확한 reproduction 미보장
- **L-1280-2 (TOKEN COUNT MATCH)**: Wikipedia / OSCAR 200MB subset 의 token count 가 anima-corpus 200MB 와 정확히 match 안 함 (tokenization 차이) — V4/V5 baseline 자체가 fair-scale 미보장 가능성
- **L-1280-3 (HEXAD MEASUREMENT)**: "6-engine completeness" 자체가 명확한 quantitative metric 부재 — engine count enumeration 방법 (a) functional separation (b) latent clustering (c) attention head clustering 3 가능, V1-V5 측정 시 같은 방법 적용 보장 필요
- **L-1280-4 (50% SHUFFLE SEMANTICS)**: V3 의 token shuffle 이 (a) per-document level, (b) per-sentence level, (c) per-token level 3 가능 — 본 Hc 는 per-sentence shuffle 가정만 측정
- **L-1280-5 (PHI MEASUREMENT CORPUS-DEPENDENT)**: H_159 Φ=0.78·N 의 측정 자체가 anima-corpus 위 trained substrate 에서만 meaningful — V4/V5 corpus 에서 Φ 측정 시 anima-Ψ-engine 의 own bias 가능 (L-189-1 circularity carry)
- **L-1280-6 (R3 PARENT Hc_1268 CARRY)**: Hc_1268 의 L-list 가 본 daughter 에 inherits
- **L-1280-7 (CORPUS SCOPE NARROW)**: anima-only / Wikipedia / OSCAR 3 corpus + 2 noise variant — Common Crawl, Pile, RedPajama 등 다른 large-scale corpus 미포함. R3 의 corpus pool scope 가 narrow (L-189-4 carry)
- **L-1280-8 (TRAINING STEP CONSTANT)**: 같은 step count 사용 가정 — 다른 corpus 의 token efficiency 차이로 fair-step 비교 어려움
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing
- **L-GENERIC-N6**: H_153 n=6 PERFECT_NUMBER_CLASS — σφ=24 의 trivial reduction

## Cross-Links

- **parent**: H_189 R3 attack vector (parent Hc_1268 split-child), H_189.4 prediction execution, C-189-4 pre-register check
- **sibling Hc**: Hc_1279 (R1 random-init GRU baseline experiment), R4/R5/R6 future daughter Hc
- **adjacent H**: H_001 (anima-core-architecture — Hexad 6-engine target), H_159 (substrate-topology — Φ=0.78N target), H_153 (n=6 triviality — σφ=24 의 perfect-number reduction null direction host)
- **literature**: Ioannidis 2005 (Why Most Published Research Findings Are False — selection bias and OVERFITTING literature foundation), Common Crawl + OSCAR + Wikipedia open corpus standards, Mikolov 2013 (word2vec corpus shuffle effect baseline)
- **internal SSOT**: Hc_1268 (R3 OVERFITTING parent Hc), Hc_908 (Ψ=1/2 anchor, Hexad sibling claim), H_001 Hexad 6-engine source doc, H_159 Φ=0.78N source doc

## Expected outcome

**Binary**: V2-V5 4 variant 의 3 core claim 모두 σ ≤ 5% 안 stable → R3 attack fails (claim corpus-independent); 1개 이상 σ ≥ 20% drift → R3 succeeds.

**Quantitative**: V2 (+10% noise) 가 ±3-5% drift 가장 작음, V3 (50% shuffle) 가 ±10-25% drift, V4/V5 (Wikipedia/OSCAR) 가 ±15-30% drift 예상. Hexad 는 corpus-independent 가능성 (engine count 는 architecture-driven), σφ=24 는 trivial (n=6 derivation), Φ=0.78N 은 corpus-sensitive (training data 분포가 substrate Φ 에 영향) — F-1280-5 (slope drift) 가 가장 likely outcome.

**Confidence prior**: 0.55 (Hexad / σφ 는 architecture-driven 으로 R3 attack 약함, Φ=0.78N 은 training-data 의존으로 R3 attack 강함 — mixed direction)
