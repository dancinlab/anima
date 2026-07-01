# H_1824 — COMPOSITIONAL-DATA-COVERAGE THRESHOLD (G1 recombination, orthogonal family #1)

**slug:** coverage_threshold
**tier:** 🔵 PRE-REGISTERED (frozen-first, p7 no tune-to-green)
**lane:** permanent G1-recombination-wall campaign — orthogonal family #1 (data-coverage axis)
**status:** PRE-REGISTERED → firing

## Frame (why this is NOT a 6th operator)

The G1 recombination wall has been falsified across the ENTIRE combination-operator
family: additive (H_1816), Hadamard (H_1818/1819), constructive HRR/circular-conv
(H_1823), binder-drop readouts (H_162x), +objective (H_1602/1819) — mouth AND
substrate both floor at G1 best_distinct≈0. The campaign exhausted ONE family
(operator/readout/objective).

`a_break_the_wall` (d): a confident terminal 🧱 requires **≥2 orthogonal lenses**
falsified, each with control+ablation. This lane fires the **data-coverage axis**,
which was NEVER varied in our 4-cell clean corpus. External literature converges on
data coverage as a **THRESHOLD effect**, not a continuum:
- An & Du (NeurReps 2025): systematicity R²=0.73 vs compositional density of input.
- PMC11685529: compositional generalization emerges above a data-coverage threshold.

Our clm303 clean corpus (`state/clm303_clean_corpus/{gen,sns}_{ko,en}.txt`) has a
FIXED, never-measured compositional density. If recombination is a data-threshold
phenomenon, the wall could be a *coverage floor*, not a structural floor.

## Hypothesis (frozen)

**G1 composed_distinct lifts above floor (≥2 ∧ >max_single ∧ coherent on ≥2/3) when
the training corpus crosses a compositional-density threshold — i.e. when the corpus
is dense in compound/derived words whose meaning = composition of their parts, AND
the lift is MONOTONE with density (LOW < MID < HIGH).**

A compound/derived word = a token whose meaning composes from sub-parts:
en: rainbow, sunlight, airport, bookshelf, notebook, keyboard, ... (closed-class
detection via a productive-affix + hyphen + known-compound heuristic)
ko: 무지개, 햇빛, 공항, 책상, ... (syllable-block n-gram compound heuristic + affix).

## Design (pre-registered before firing — p7)

### Corpus variants (3, by compositional-density binning)
From the 4 existing clean cells, build 3 variants, each keeping the 4-cell register
split (a_chat_registers) so the only varied axis is compositional density:
- **LOW**  — filter OUT sentences dense in compound/derived tokens (density floor).
- **MID**  — as-is baseline (no compositional re-weighting).
- **HIGH** — oversample sentences dense in compound words (+ optional compound-word
             curriculum injection at the head). Density ceiling.

**fail-loud (a_chat_registers):** measure & log actual compound-density per variant
(compounds per 1k tokens, per cell). If NOT monotone LOW<MID<HIGH the variant build
is INVALID → abort (no silent skip). Per-cell byte counts logged; 4 cells required.

### Models
Standard production CLMConvMoE 303M via `cli/train.py --canon --steps 4000 --bf16`
(L4·d3784·E2→Emax3, the SAME clean 303M ConvMoE path the prior campaign used).
One model per density variant × seeds {7, 4302} = 6 models.
proportional sampling (anti-memorization), --val-frac 0.05 --val-every 200.

### Frozen bars
1. **G1 lift:** composed_distinct ≥2 ∧ >max_single ∧ coherent on ≥2/3 decodes.
2. **MONOTONE:** G1(LOW) < G1(MID) < G1(HIGH) — the threshold-effect signature.
3. **overfit guard (INVALIDATES verdict if fails):** held-out 4/4 register
   val_CE < ln256 DESCENT (`verify_clm_v2.py descent`). A non-DESCENT model's
   G1 is uninterpretable (memorization, H_1579), so its verdict is void.

### Measurement (engine-native-py 2-production, DIRECTIONAL)
`python3 cli/evaluate.py <clm> --corpus <4 cells> --gen 80` (= g_gates
gen_auto_ideate via generator L3, same forward core as serving). Footer line =
`CLOSURE` / `G1 RECOMBINATION`. py 2-production = DIRECTIONAL (terminal = hexa
`anima evaluate`); sufficient for floor/lift screen, GREEN claim → hexa-confirm
follow-on.

## Verdict tiers (verbatim from g0g6 — c9 honest, negative is a result)
- 🟢 if G1 lift ∧ MONOTONE(LOW<MID<HIGH) ∧ 4/4 DESCENT all variants.
- 🟠 if mixed (e.g. HIGH lifts but not monotone, or single-seed only).
- 🧱 if floor (G1=0 across all density variants) → data-coverage axis FALSIFIED =
  one of the ≥2 orthogonal lenses `a_break_the_wall` requires before terminal.

## Cost
~$4-6 (1 GPU pod, 3 variants × 2 seeds × ~31min train + evals). Owner released
the cost-gate ("1,2,3 go").

## Artifacts
- `state/g1_coverage_threshold/` — corpus variant builder, density report, trainer
  wrapper, run_pod.sh, ckpts, g0g6 outputs, RESULT.md.

## DIRECTIONAL toy cheap-gate (2026-07-02)

🧱 DIRECTIONAL-FLOOR (toy cheap-gate screen, 2026-07-02, aiden $0, torch=DIRECTIONAL). Operator-agnostic factored toy(NF8·E4·C12, fixed 12-combo held-out), training-coverage sweep {16..52}/52 × 3 seed: TEST acc n(hi−chance≥+0.15)=0/3, 52/52 coverage서도 미학습 조합 chance floor. → data-coverage 는 held-out 재조합 안 엶 (H_1599 EN-exposure floor 확장). objective(H_6162)·regularization(H_6161)·data 3축 전수 controlled-toy FLOOR = G1 axis-invariant(DPI). ⚠️toy-scale(a_toy_scale_recheck): full-corpus $4-6 test 가 terminal이나 toy가 floor 예측→LOW priority. state/1824_compositional_data_coverage_threshold/RESULT.md.
