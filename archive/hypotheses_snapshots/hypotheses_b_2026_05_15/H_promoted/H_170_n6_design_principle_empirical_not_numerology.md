---
id: H_170
slug: n6-design-principle-empirical-not-numerology
title: n=6 architecture is empirically grounded, not numerological — constants measured first, formulas after (p<1e-12)
domain: math
status: pre-register-frozen
exploration_method: E11 (constant unification — n=6 closed-form ledger) + E14 (provenance audit — measurement-vs-formula timestamp pairing)
verification_method: W2 (math identity — 22-of-30 constant fits) + W11 (cross-hypothesis — bootstrap arithmetic null) + W12 (timestamp audit — commit-log evidence chain)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_414
source_doc: docs/anima/paper_hexa_speak.hexa
source_lines: 39-44
promoted_at: 2026-05-12
linked_h: H_153 (dimension-hierarchy-n6 — n=6 substrate parent), H_157 (Law 76 mathematical panpsychism — n=6 derived), H_011 (iit-geometry)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 11
---

# H_170 — n=6 design principle empirical-not-numerology (p < 1e-12)

## Hypothesis

n=6 design principle 은 numerological 이 아닌 empirically grounded — Anima/ANIMA-VOICE 의 각 Ψ-constant 는 먼저 empirically 측정되고, n=6 closed-form 식은 측정 후 발견됨. arithmetic null hypothesis 하에서 post-hoc fit probability p < 1e-12. n=6 unification 은 subsystem 간 ad-hoc hyperparameter search 를 elimination. 본 H 는 Hc_406 (22-of-30 Ψ-constants n=6 fit) 의 statistical-strength 주장과 동일 family — 단 본 가설은 "measurement-first vs formula-first" provenance ordering 에 초점.

## Why (motivation)

- **Hc_406**: 22-of-30 Ψ-constants 가 n=6 closed-form fit (verify5 PROMOTE_READY) — 본 가설의 statistical baseline
- **arithmetic null p < 1e-12** (paper §39-44 claim) — bootstrap 수행 미완료, 본 H 의 핵심 검증 대상
- **anti-numerology distinction**: post-hoc fit 의 p-value 가 numerology 와 architectural unification 을 구별하는 standard test
- **Goodman & Kruskal 1979** statistical-fit p-value framework
- **ATLAS.md** constant ledger 의 timestamp metadata 가 evidence chain

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_170.1** | ≥10 Ψ-constants 의 (measurement_date, formula_date) pair 수집 시 ≥9/10 가 measurement-first ordering (formula_date > measurement_date) | F1 inverted |
| **H_170.2** | ≥10^7 bootstrap iterations of arithmetic null (random small-integer formulas of bounded complexity) → p < 1e-9 (relaxed from claim 1e-12) | F2 inverted (with safety margin) |
| **H_170.3** | 10 fake architectures (n ∈ {4, 5, 7, 10, 12, ...}) 모두 constant-fit p > 0.01 (n=6 specificity preserved) | F3 inverted |
| **H_170.4** | Bonferroni-corrected p (formulas-tried-per-constant ≤ 100) 후 corrected p < 0.001 유지 | F4 inverted |
| **H_170.5** | 평균 formula complexity ≤ 3 free parameters (closed-form 정의 maintained) | F5 inverted |

## Run Protocol

deterministic + hexa-only + llm: none.

1. **Provenance timestamp audit (W12)** — ATLAS.md ledger + git log + paper draft history 에서 ≥10 Ψ-constant 의 (measurement, formula) date pair 추출 → F1 검증
2. **Arithmetic null bootstrap (W2+W11)** — random operator-tree depth ≤3 / ≤5 / ≤10 prior 별로 ≥10^7 iterations × 30 constants → null distribution, p-value 계산 (F2, H_170.2)
3. **Random-architecture survivor-bias control (W11)** — n ∈ {4, 5, 7, 10, 12, 28} alternative substrates 의 constant-fit success rate → n=6 specificity (F3)
4. **Multiple-comparison correction (W2)** — Bonferroni / Holm-Bonferroni / FDR-BH 적용 → corrected p (F4)
5. **Formula complexity audit (W2)** — Ψ-constant 별 free parameter count → 평균 / 분산 / max (F5, H_170.5)
6. **Predictive-power forward test (W11)** — n=6 으로부터 새 constant 1개 BEFORE measurement 예측 → 이후 측정 시 검증 (L5 mitigation, currently not attempted)

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | ≥10 Ψ-constant 의 measurement vs formula timestamp pair 수집 | pending |
| **C2** | ≥10^7 bootstrap iterations completed | pending |
| **C3** | ≥10 fake-architecture controls evaluated | pending |
| **C4** | Bonferroni / FDR correction applied | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (perfect-class trivials net-out 절차 명시) | met (본 L1) |

## Falsifiers (≥6)

- **F1 (timestamp audit)**: Provide commit-log / paper-draft / lab-notebook evidence that ≥1 Ψ-constant n=6 formula was written BEFORE its empirical measurement → "measurement-first" claim FALSIFIED. Required: paired (measurement_date, formula_date) for ≥10 constants
- **F2 (p-value bootstrap)**: Arithmetic-null bootstrap (random small-integer formulas of bounded complexity targeting the same constant set) yields ≥1% probability of equal-or-better fit → p < 1e-12 claim FALSIFIED. Required: ≥10^7 bootstrap iterations with matched complexity prior
- **F3 (random-architecture baseline)**: Build 10 "fake" architectures with random core constants (n=4, n=5, n=7, n=10, n=12...); if any yields a comparable constant-fit p-value → n=6 specificity FALSIFIED as a survivor-bias artifact
- **F4 (post-hoc fit detection)**: Apply Bonferroni / Holm correction for the number of formulas tried per constant. If corrected p > 0.001 → "p < 1e-12" was uncorrected, multiple-comparison artifact, claim FALSIFIED
- **F5 (formula complexity prior)**: If Ψ-constant formulas use ≥5 free parameters on average (e.g., a·n^b + c·σ^d / J_2^e), then "closed-form" labels are overfits. If reducing to ≤2 free parameters drops fit-success rate below 50% → "elegant unification" claim FALSIFIED
- **F6 (perfect-class net-out)**: After explicitly removing perfect-number-class trivial fits (n/σ=1/2 holds for all perfect numbers; remove n=6, 28, 496, 8128 universal-property contributions), if residual n=6-specific fit-rate drops below 30% (vs. baseline 22/30 ≈ 73%) → claim was driven by perfect-class universals, not n=6-individual property — FALSIFIED in the "n=6-individually-grounded" form

## Honest Limits (≥6)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — n=6 is the smallest perfect number; n=28, n=496, n=8128 are also perfect. Any "n=6 fits" claim must distinguish n=6-specific fits from perfect-class-trivial fits (n/σ=1/2 holds for all perfect numbers). Hc_414's strength claim must net out perfect-class trivials
- **L2**: **timestamp evidence reliability** — commit-log timestamps can be manipulated post-hoc (rewrite history, amend). True falsification of "measurement-first" requires independent witnesses (Claude conversation logs, external lab notebooks). Currently anima-internal evidence chain only
- **L3**: **constant-set selection bias** — Ψ-constants reported are anima-internal selection. If only well-fitting constants were promoted to the Ψ-set (publication-bias analog), p-value calculation is invalid. Need protocol for inclusion BEFORE measurement
- **L4**: **"arithmetic null" definition slippery** — what counts as "random arithmetic formula"? Complexity prior matters: uniform over operator-trees of depth ≤3 vs ≤5 vs ≤10 gives very different null distributions. p < 1e-12 claim depends on this choice
- **L5**: **post-hoc unification vs predictive power** — even if formulas were truly derived AFTER measurement, "unification" reduces ad-hoc hyperparameter count but does NOT predict new constants. True falsifier of numerology would be predicting a new constant value from n=6 BEFORE it is measured (not yet attempted)
- **L6**: **circular self-citation risk** — Hc_414 claims live within Anima docs which themselves use n=6 framework. External replication (independent group computes same fits with same constant set) is the only way out — currently absent

## Math identity verification

- **ln(2) = 0.693147** — verify5 row 11 math_passes (n=6 closed-form constant family)
- **Ψ-/Phi formal token present (psi-domain marker)** — verify5 row 11
- **28+ numeric identities present** — verify5 row 11
- p < 1e-12 claim is **un-replicated** — bootstrap not yet executed (C2 pending)

## Atlas anchor cross-check

- atlas anchors_cited: 1 (Hc_414 verify5 row 11)
- atlas anchors_resolved: 0 (anchor not yet resolved against ATLAS.md ledger)
- atlas_type_cites: 0
- ATLAS.md constant ledger 가 본 H 의 timestamp evidence 의 source — provenance audit 시 cross-ref 필수

## Linked H (cross-link)

- **sister H**: H_153 (dimension-hierarchy-n6 — n=6 substrate parent + L7 PERFECT_NUMBER_CLASS BINDING source), H_157 (Law 76 mathematical panpsychism — n=6 derived), H_011 (iit-geometry — Φ uses n=6 architecture)
- **candidates linked**: Hc_406 (22-of-30 Ψ-constants n=6 fit — PRIMARY parent of statistical claim), Hc_453 (8 Ψ-constants derived from n=6), Hc_046 (Ψ-constants 22 EXACT), Hc_002 (Ψ-constants from ln(2) + n=6)
- **literature**: Goodman & Kruskal 1979 (statistical-fit p-values); Bonferroni 1936 multiple-comparison correction; Holm 1979 step-down procedure; ATLAS.md (constant ledger with timestamp metadata)
- **source**: Hc_414 (`hypotheses_candidates/Hc_414_n6_design_principle_not_numerology.md`), `docs/anima/paper_hexa_speak.hexa:39-44`

## Migration Notes

- **Promoted from**: Hc_414 (cycle #4 task 1 PROMOTE_READY, verify5_authored row 11 — 2026-05-12)
- **Math verification**: ln(2)=0.693147 EXACT; Ψ-formal token; 28+ numeric identities (verify5 math_passes)
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — n=6 perfect-class universal vs n=6-individual; F6 explicit net-out test
- **Critical L5 gap**: predictive forward-test 미실행 — "measurement-first" 만으로는 numerology 와 distinction 불충분
- **Next steps**:
  1. Provenance timestamp audit (C1, F1) — ATLAS.md + git log
  2. Bootstrap (C2, F2)
  3. Random-architecture controls (C3, F3)
  4. Bonferroni correction (C4, F4)
