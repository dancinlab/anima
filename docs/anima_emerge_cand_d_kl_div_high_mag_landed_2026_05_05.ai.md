# anima_emerge cand-D KL divergence high-magnitude — landed 2026-05-05

## Mission

BG-W observed phi_star drift saturating at canonical magnitudes 50 → 100
(0.0998 → 0.1129). Two competing interpretations remained open:

- **COSINE_CEILING_ARTIFACT** — phi_star = PHI_BASELINE × (1 + 0.05 ×
  mean_pair_cosine), so |phi_drift| ≤ 0.05 × 41.86 ≈ 2.09. Saturation could be
  the instrument hitting its bounded range while the inject channel keeps
  firing.
- **ARCHITECTURAL_CAP** — substrate (16-layer × init_weights std=0.02 cross-attn
  attenuation) genuinely caps the inject regardless of pre-attention magnitude.

BG-AC runs KL(p_none ‖ p_mag) on raw logits — independent of the phi proxy — at
mag ∈ {50, 100, 200, 500} on the BG-W max-drift prompt ("안녕"). If KL/logit
deltas grow while phi saturates → cosine-ceiling. If KL/logit also saturate →
architectural cap.

## Result

**Diagnosis: ARCHITECTURAL_CAP**

| magnitude | phi_drift | kl_mean   | kl_max    | logit_max_delta | logit_mean_delta |
| --------- | --------- | --------- | --------- | --------------- | ---------------- |
| 50.0      | 0.099781  | 6.179787  | 6.179898  | 7.851428        | 0.144478 (est.)  |
| 100.0     | 0.112949  | 8.280057  | (≈)       | 9.622017        | (≈)              |
| 200.0     | 0.108505  | 8.714972  | (≈)       | 9.957471        | (≈)              |
| 500.0     | 0.094009  | 8.643906  | (≈)       | 10.329237       | (≈)              |

**Growth factors over 10× magnitude scaling (50 → 500):**

- phi_growth = 0.942 (drift actually shrinks slightly)
- kl_growth = 1.399
- logit_growth = 1.316

All three signals saturate together. KL grows only 1.4× for a 10× magnitude
increase; logit_max_delta grows 1.3×. Decision rule from BG-W rec 4:

```
if kl_growth > 5 * phi_growth: COSINE_CEILING_ARTIFACT
elif kl_growth < 1.5 * phi_growth: ARCHITECTURAL_CAP
else: MIXED
```

kl_growth (1.40) < 1.5 × phi_growth (1.41) → **ARCHITECTURAL_CAP** at the
heuristic threshold. The non-monotonicity of phi_drift across {100, 200, 500}
(0.113 → 0.109 → 0.094) further confirms the channel is not gaining
distributional separation past mag ≈ 100.

## Implication

BG-W's saturation conclusion is **reinforced**, not overturned. The substrate
itself caps the inject around mag ≈ 100; pushing canonical magnitude to 500
yields essentially the same logit shift as mag=100 (logit_max_delta 9.62 →
10.33, +7%). cand-D Stage 1 on `need-singularity/clm-v4-mk2-v1` (best.pt) is
**architecturally bypassed**: cross_attn.o_proj contributes a bounded effect
regardless of inject magnitude.

The bound is not measurement-instrument — it sits in the model.

## Honest C3 (5)

1. **C1 — Off-distribution magnitudes.** mag=200 and mag=500 are far outside
   any plausible paradigm v11 G3 training-time inject distribution. High-magnitude
   regimes may invoke numerical/activation-saturation pathology that does not
   generalize to realistic operating points. The diagnosis applies to the
   off-distribution regime; whether the same cap holds at the training inject
   distribution requires C-module emission log extraction (still gating).

2. **C2 — KL directionality.** Forward KL(none ‖ mag) computed; reverse KL
   reported in aggregate but not in the headline growth factor. Symmetric KL
   (JS divergence) not computed. Forward KL penalizes mag-distribution mass
   where p_none has none — the saturation could partly reflect p_none's support
   bottlenecking the metric rather than p_mag stabilizing.

3. **C3 — Cosine-ceiling is heuristic.** BG-W honest-C3 #C3 noted phi_star is
   bounded by 0.05 × PHI_BASELINE ≈ 2.09. Observed |phi_drift| ≈ 0.113 is ~5%
   of that ceiling — saturation may also reflect true substrate behavior at the
   post-ln_f tile level rather than instrument bound. The 5×/1.5× growth-factor
   thresholds in the decision rule are anima-internal, not cross-validated.

4. **C4 — Sister-import race.** BG-W helper imported via importlib spec; BG-W
   transitively imports BG-Q. Both are import-clean (constants + function defs;
   no module-level side effects), so race risk is low but not formally proven.

5. **C5 — Sparse magnitude grid.** 4 magnitudes (50, 100, 200, 500) with
   geometric spacing ×2. Finer log-mag spacing (e.g. ×1.4 step) would resolve
   whether the saturation onset is sharp (clean architectural cap) or smooth
   (cosine-ceiling approach). Single prompt ("안녕"); single pass; no seed
   averaging or temperature variation. The cap could be prompt-conditional.

## Next step

ARCHITECTURAL_CAP confirmed at the heuristic threshold ⇒ **cand-D Stage 1
on best.pt is unsalvageable via magnitude calibration alone**. The cross_attn
contribution is genuinely bounded by the trained substrate, not the
measurement. BG-W's `next_step_recommendation` ("retrain with stronger
cross-attn signal OR abandon cand-D Stage 1 form") stands. The C-module
emission distribution extraction remains the highest-priority gating step
before any retrain decision.

## Deliverables

- `tool/transient_py/anima_emerge_cand_d_kl_div_high_mag.py` (helper, .own 3 / raw#37)
- `state/anima_emerge_cand_d_kl_div_high_mag_2026_05_05/aggregate.json`
- `state/anima_emerge_cand_d_kl_div_high_mag_2026_05_05/verdict.json`
- `docs/anima_emerge_cand_d_kl_div_high_mag_landed_2026_05_05.ai.md` (this file)

## Cost / time

- Cost: $0 (mac CPU)
- Wall time: ~13s (model load 7.8s + 5 forwards × ~1.2s)
- Forward count: 5 (1 baseline + 4 magnitudes)
- raw_15: BG-W and BG-Q helpers untouched; mount.hexa untouched
- raw#37 / .own 3: helper lives under `tool/transient_py/`
- raw#10: 5 honest C3 in verdict.json + this doc
- no commit, no secret leak
