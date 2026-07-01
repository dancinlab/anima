# H_6105 — depth-in-time generate→verify→revise recurrence (g6-lens F1)

- **frontier:** g6-lens (fleet-full) · **phase:** 🛠️implement r2
- **verdict:** 🧱 DIRECTIONAL (frozen bar failed on control iii) — NOT terminal
- **wired:** DIRECTIONAL-mirror (mechanism toy; 303M engine-native UNMEASURED → follow-on)
- **substrate:** ⚠️ **mechanism toy — synthetic slot-filling claim generator, NOT a real LM.** numpy · $0 · mini-safe. 303M ByteGPT engine-native re-measurement is a cost-gated follow-on (only if toy had cleared bar; it did not).

## Claim (r1 research → isolate)
The untried orthogonal family F1 = *depth-in-time* generate→verify→revise recurrence: draft a claim, read the **missing detector predicate** (comparator / measurable / negatable) from the frozen judge, feed it back to regenerate, repeat T times — welding depth into **time (recurrence)** instead of network depth. Isolated question: **does feedback-conditioned revision lift falsifiable-fraction above the single-pass floor, AND survive the targeting + resample controls?**

## Method (mechanism isolation)
- Frozen judge = **VERBATIM port** of `core/g6_ideation.hexa` `_g6_is_falsifiable` (comparator ∧ measurable ∧ ≥2 content-words ∧ not-question ∧ not-stance-prefix). No loosening (p7/c9). Applied to materialized claim strings.
- Synthetic generator fills 3 positive slots (comparator/measurable/content) from imperfect vocab pools; per-slot judge-valid prob `Q=0.5` (un-tuned coin-flip, pre-registered, NOT chosen to hit the bar). question/stance-prefix kept clean so the isolated variable is the 3 feedback-targeted predicates.
- **4 arms, equal decode budget** (R/R_shuffle/R_noloop = 1 draft + T=3 = 4 passes; A = 1-pass floor):
  - **A** single-pass draft → floor.
  - **R** revise-loop T=3: judge reports which predicate slot is deficient → regenerate **only** the deficient slot(s). Goodhart-safe: judge's *answer word* never injected — only structural "which category deficient"; generator re-samples from its own imperfect vocab (success prob Q). Targeted ⇒ monotone (never touches a good slot).
  - **R_shuffle** same loop/budget but regenerate a **random** slot (binding control — feedback must be targeted; re-rolling a good slot can break it).
  - **R_noloop** same 1+T=4 budget as **independent** full drafts; falsifiable if **any** passes (best-of-N — feedback vs just-more-samples control).
- metric = falsifiable-fraction over N=500 claims/arm/seed; seeds {7,4302,4303}.

## Frozen bar (pre-registered, tune-to-green forbidden)
≥2/3 seeds with (i) R−A ≥ +0.34 ∧ (ii) R−R_shuffle ≥ +0.34 ∧ (iii) R−R_noloop ≥ +0.34. All three ⇒ 🟢 DIRECTIONAL. Any one fails ⇒ 🧱.

## Result (4 arm × 3 seed falsifiable-fraction)
| seed | A | R | R_shuffle | R_noloop | Δi (R−A) | Δii (R−shuf) | Δiii (R−noloop) |
|-----:|----:|----:|----:|----:|----:|----:|----:|
| 7    | 0.188 | 0.786 | 0.420 | 0.602 | **+0.598** ✓ | **+0.366** ✓ | +0.184 ✗ |
| 4302 | 0.192 | 0.820 | 0.370 | 0.564 | **+0.628** ✓ | **+0.450** ✓ | +0.256 ✗ |
| 4303 | 0.186 | 0.856 | 0.442 | 0.584 | **+0.670** ✓ | **+0.414** ✓ | +0.272 ✗ |

pass counts (≥+0.34): i_vs_A=**3/3** · ii_vs_shuffle=**3/3** · iii_vs_noloop=**0/3** → **GREEN=False**.

## Verdict — 🧱 DIRECTIONAL (robust across all 3 seeds)
- (i) ✓ Time-recurrence revision **clears the single-pass floor** decisively (+0.60 avg).
- (ii) ✓ The lift is **feedback-targeted**, not incidental — misdirected (shuffle) feedback captures only ~half the gain.
- (iii) ✗ **Fails vs best-of-N resample.** With equal budget, simply drawing 4 independent drafts and keeping the best (R_noloop ≈ 0.58) already captures most of the apparent gain; the residual attributable to *targeted iterative repair* (R−R_noloop ≈ **+0.24 avg**) is real and positive but **below the +0.34 bar** on all 3 seeds.
- Per the frozen bar (any control fails ⇒ 🧱): **depth-in-time does not clear the pre-registered margin over the resample baseline** → weld = depth-bound wall hardening for this mechanism. Robust (0/3, not marginal noise).

## Honesty / scope
- numpy mirror ⇒ **DIRECTIONAL only, terminal 박제 금지.** Synthetic generator, not a real LM.
- Judge ported verbatim, NOT loosened. Negative reported as measured — no tuning to green.
- The R_noloop best-of-N control is the load-bearing finding: much of "revision helps" is *more samples*, and the targeted-feedback residual is sub-bar here.

## Next phase
- 🧅 abstraction: fold into g6-lens law census as "time-recurrence lift ≤ best-of-N by pre-reg margin (toy)" — depth-in-time is NOT a free G6 lever over budget-matched resampling.
- follow-on (cost-gated, was contingent on toy green — **NOT triggered**): 303M ByteGPT engine-native re-measure only if a mechanism variant beats best-of-N at toy scale first (e.g. higher T, or a harder judge where resample floor is lower).
