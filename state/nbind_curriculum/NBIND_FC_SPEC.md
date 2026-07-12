# H_next NBIND-FC (negation Form-Coverage curve) — Fable frozen spec (2026-07-12)

> H_9272 wild-transfer FALSIFIED(augmentation-specific·flip1 0.290 붕괴) 후속 결정실험. verdict axis=F2(lexeme-novel flip1) over K의 slope: +0.15 crossing=coverage-density limit(crack-able) / flat-at-chance+live controls=surface-invariant-binding ceiling(terminal).

Ledger check done — precedent found and it matters: **H_6183/H_6184 (🟢 DIRECTIONAL)** already showed a *coverage-density phase transition* for G1 pair-recombination (HIGH coverage 0.85–0.95 vs LOW 0.0–0.25, arch-invariant, SHUF=0), flagged in memory as the last remaining low-cost G1 lever. But those covered **cell**-coverage. Your flip1=0.290 signature is a different axis: the flip machinery exists and fires, but only behind **memorized surface detectors** (wild negation is treated as a no-op → anti-flip below chance). So the open question is precisely **form**-coverage: does the flip operator abstract over negation *surfaces* as form diversity grows, or is it forever a per-surface template? That's the one axis that cleanly splits "coverage-density limit (crack-able)" from "surface-invariant-binding ceiling (terminal)". Read-side mechanisms are ledger-blocked (earned-terminal #3293/#3294 — retry = tune-to-green), and production-seasoning conflates scale+coverage+interference, so it can't give a clean verdict first.

# Frozen spec — H_next: NBIND-FC (negation Form-Coverage curve)

**One-line thesis:** hold the data budget fixed, sweep the number of drilled negation surface forms K, and read the verdict off the *slope* of held-out-form flip accuracy.

## (a) Setup · arms · controls

**Corpus:** same NBIND augmented P×N grid pipeline as H_9272 (NSMC predicates × negation), **fixed total rows/tokens across all arms** — K varies form *diversity* only, never data volume. Per-form frequency matched within each arm.

**Form inventory (form = distinct surface string pattern):** partition Korean negation into families — 안+V, -지 않- (each conjugation = a distinct form: 않다/않아/않았/않네/않고…), -지 못하-, 못+V, -지 말-, 아니다, 없- lexical compounds (재미없-, 맛없-…), -기는커녕/은커녕, NPI+neg (전혀/별로/결코/절대 ~않). **Reserve a FIXED never-trained set at every K**, stratified two ways:
- **F1 (conjugation-novel):** unseen conjugations of *trained* lexemes (shares negation-stem bytes, e.g. 않).
- **F2 (lexeme-novel):** wholly untrained negation lexemes, **zero shared negation-stem bytes** with any trained form (e.g. reserve the 못-family + 없- family + 커녕 entirely). Predicates in all eval rows are trained-known — only the form axis is novel.

**Arms:** K ∈ {3, 6, 12, 24} × 2 seeds. K=6 = your existing H_9272 ckpts (reuse, no retrain) → **6 new training runs**.

**Controls (per arm):** (C1) shuffle-model control as in H_9272; (C2) liveness = trained-form held-out-cell acc (must replicate PASS); (C3) flip0 wild affirmative (must stay >chance); V3 Korean-aware 4-cell balance, V5 two seeds, no max-of-controls — paired stats across K per the probe-defect census.

**Eval panels:** E1 = F1 flip1 acc · E2 = F2 flip1 acc (the verdict axis) · E3 = wild NSMC W-T/W-R as a function of K (secondary, practical-crack readout).

## (b) Frozen bars (pre-registered, no post-hoc)

- **COVERAGE-CRACK PASS:** F2 flip1 rises monotonically with K, Δ(K=24 vs K=3) ≥ +0.15, AND F2 main − shuffle-control ≥ 0.15 at K=24, both seeds. → coverage-density limit; wild emergence is drillable.
- **CEILING (FAIL):** F2 flip1 flat within ±0.10 of chance at ALL K including 24, while C2 ≥ 0.70 (model live). → surface-invariant binding = genuine 303M byte-LM ceiling candidate (terminal pending the γ-class measure-side exit, not more corpus).
- **Signature sub-read:** F2 flip1 < 0.40 at K=24 = anti-flip persists → detector-gated memorization *confirmed* (strong-form ceiling).
- **Split verdict (expected):** F1 passes, F2 fails → wall is refined to *lexeme-level* abstraction; wild transfer then hinges on E3: if W-T rises with K anyway (wild negation is mostly conjugation variants), the practical crack = drill the wild inventory (production-seasoning becomes the justified next fire).
- **INVALID:** C2 fails at high K (capacity/interference confound) — no verdict, rerun with capacity check.

## (c) Prediction + confidence

- F1 (conjugation-novel): generalizes, ≥0.65 by K=12 — **~75%** (byte-stem overlap + H_6184 coverage precedent).
- F2 (lexeme-novel): stays ≤0.55, flat — **~60%** (flip1=0.29 anti-flip says the detector, not the operator, is the bottleneck; CE gives no pressure to form an abstract NEG latent across disjoint surfaces). I expect the **split verdict**, with E3 wild rising to ~0.55–0.60 at K=24 — i.e., "crack-able in practice by inventory coverage, ceiling-ed in principle at lexeme abstraction."
- Note H_6183/6184 pull the other way (coverage phase transitions DO happen here) — that genuine tension is exactly why this is the decisive experiment.

## (d) Cost

GPU: 6 training runs at H_9272 scale + eval sweeps (K=6 arm free via ckpt reuse) — roughly **6× one H_9272 seed-run**; single pod, dedicated host per job per the pod policy. Not $0, but the cheapest experiment that can flip the terminal/crack-able verdict.

**Decision rule in one sentence:** the slope of F2 (lexeme-novel flip1) over K is the verdict — positive slope crossing +0.15 = coverage limit, flat-at-chance with live controls = surface-invariant-binding ceiling.