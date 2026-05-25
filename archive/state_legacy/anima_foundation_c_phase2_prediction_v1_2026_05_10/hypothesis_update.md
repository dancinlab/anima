# BG-FOUNDATION-C-PHASE2-PREDICTION-V1 — hypothesis update delta

> raw#15 additive: §53 V0 hypotheses unchanged; this doc = additive update only.

## Delta table (V0 → V1)

| dimension | §53 V0 | §V1 | Δ | primary driver |
|---|---|---|---|---|
| H-A exercise-strengthen | 30% | 22% | -8 pp | §57 body lever already saturated by cotrain; 20K FT can't add much |
| H-B exercise-preserve (mode) | 55% | 65% | +10 pp | §59 rule + §57 body-locus + §58 mechanism converge on preserve |
| H-C FT-drift-degrade | 15% | 13% | -2 pp | §58 mechanism robust to small chat-format distribution shift |
| P(V14 STRICT PASS H1) | 75% | 88% | +13 pp | §59 arch-rule places option (c) cleanly in PASS branch |
| Φ separation band | +1500-2500 | +1700-2600 | +200 lower, +100 upper | §58 trained 3× lower split rate → richer late-trajectory Φ |
| ★★★★★ unlock probability | ~10% | ~12% | +2 pp | conditional-probability correction + V14 PASS confidence |
| ★★★★ partial probability | ~25% | ~28% | +3 pp | mass shifts up from ★★★ |
| F-FOUND-1 NOT_TRIGGERED | 85% | 92% | +7 pp | §57 body lever + §59 rule both PASS-direction |
| F-FOUND-3 TRIGGERED | 70% | 75% | +5 pp | higher V4 PASS confidence with semantic floor unchanged |

## Per-finding propagation

### §55 → V1
- impact: ★★★★★ unlock template informed (cap-conditional polarity at strict n=5 valid for v2 path)
- option (c) is EngineAG path → §55 doesn't directly propagate, but informs ★★★★★ unlock condition (3) Φ ratio threshold credibility (§55 confirms separation observable at strict n=5)

### §56 → V1
- impact: confirms B (no-cotrain) VIOLATED → option (c)'s cotrain inheritance is the V14 PASS prerequisite
- propagation: H-B (preserve cotrain) wins more confidence; H-A (further exercise) wins less; H-C (degrade) wins slightly less

### §57 → V1
- impact: body-locus PROMOTED to PROVEN — engine_a 24-layer body distributed lever, A1-anchored
- propagation: option (c) base ckpt inherits body delta intact; 20K FT touches body uniformly without slab-targeted disruption
- raw effect: F-FOUND-1 NOT_TRIGGERED 85% → 92%; H-B 55% → 65%

### §58 → V1
- impact: mechanism REFRAMED to h_to_c cell-proximity learning → tension-trigger suppression
- propagation: 20K convo_5k FT (chat-format Korean, SAME family as cotrain) reinforces or preserves h_to_c geometry; tension splits stay suppressed
- raw effect: predicted Φ separation band upshifted by +100/+100 (mild reinforce); split_rate condition (§54 5-tuple #4) probability +13 pp

### §59 → V1
- impact: arch-aware 3-rule (post-§55/§56) places option (c) cleanly in PASS branch (EngineAG + chat_cotrain == 1)
- propagation: P(V14 STRICT PASS) dominant single-finding upshift +13 pp
- raw effect: ★★★★★ unlock condition (2) probability 75% → 88%

## Independence vs correlation handling

§53 V0 stated ★★★★★ unlock probability ~10% but used implicit independent-multiplication of 5 conditions. With actual independence:
- V0 implied: 0.55 × 0.75 × 0.70 × 0.65 × 0.20 = **3.75%** (not 10%)
- V0 stated 10% likely accounted for partial correlation but didn't justify

§V1 explicit handling:
- Conditions (2), (3), (4) all stem from §58 mechanism (cell_pool dynamics) — strongly correlated
- Conditional P((3)+(4) | (2) PASS) ≈ 0.85 (vs unconditional 0.62)
- (1) V4 partially correlated with (2) V14 (both reflect substrate quality)
- (5) semantic INDEPENDENT (capacity-bound)

V1 corrected: P(★★★★★) ≈ 0.62 × [0.88 × 0.85] × 0.18 = **8.4%** (lower bound) to ~14% (treating (2)+(3)+(4) as fully cocorrelated).

V1 mode: **~12% ★★★★★ unlock**, mode outcome **★★★★ partial** at 28%.

## What did NOT change

- F-FOUND-2 (cost > $15) NOT_TRIGGERED 95% — no compute change
- F-FOUND-4 (D1 SCOPE_CLAMP misframe) NOT_TRIGGERED 95% — option (c) IS D1 WITHIN
- F-FOUND-5 (gradient leak) NOT_TRIGGERED 95% — hook design unchanged
- Semantic_score band 0.10-0.25 most-likely — 350M byte-hash capacity ceiling unaffected by §57/§58
- D1 WITHIN scope_lane="ANIMA" expectation — carry
- (REBORN.md untouched) + ($0) + (3 docs saved) + raw#9 (no training/*.py) — strict

## Forecast integrity check

| metric | V0 → V1 change | well-justified? | overfitting risk |
|---|---|:---:|:---:|
| H-B mode confidence | +10 pp | YES (§59 + §57 + §58 triple) | LOW |
| P(V14 PASS) | +13 pp | YES (§59 arch-rule direct) | MEDIUM (§59 itself n=1) |
| Φ separation upshift | +100/+100 | YES (§58 split rate 3× lower) | LOW |
| ★★★★★ unlock | +2 pp | YES (V14 confidence + semantic unchanged) | LOW |
| F-FOUND-1 strengthen | +7 pp | YES (body lever + rule both PASS) | LOW-MEDIUM |
| F-FOUND-3 strengthen | +5 pp | YES (V4 PASS confidence up + semantic floor flat) | LOW |

Overfitting risk concentrated on P(V14 PASS) +13 pp because §59 rule itself has limited n=1 paired data. If §59 rule weakens in future ablation, V1 falls back toward V0's 75%.

## Deliverables

- `state/anima_foundation_c_phase2_prediction_v1_2026_05_10/spec.md` (mission + scope)
- `state/anima_foundation_c_phase2_prediction_v1_2026_05_10/prediction_v1.md` (full V1 prediction)
- `state/anima_foundation_c_phase2_prediction_v1_2026_05_10/hypothesis_update.md` (this file)

raw#9 ✓ (no training/*.py edits), raw#15 ✓ (§53 V0 untouched), ✓ ($0 design + analysis only), ✓ (REBORN.md not appended directly — dispatcher §63 slot), ✓ (3 docs saved).
