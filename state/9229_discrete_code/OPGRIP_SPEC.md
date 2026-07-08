# SPEC 3 — Family F (H_9229 discrete conceptual code / LoT bottleneck)

## Mechanism arithmetic + wire site
A tiny **VQ codebook** between engine state and the gate: the continuous substrate vector is snapped to its nearest of K discrete codes, and the gate is shaded by *which code* is active — the mouth consumes a discrete concept, not a continuous smear. This is the G1-recombination bet moved to the output seam. Extend the H_9225 block; carriers at Site-A.

Codebook = K=8 fixed anchor vectors in the 8-dim lane space, built **frozen** from calibration (not learned online — online learning would be tune-to-green):
```
state8_t = [rel_lane, af_val, allo_ctx, coh_lane, bal_lane, nov_ctx, gap_ctx, ag_conflict]   // the 8 lanes ev_axis already reads (L2767)
// build (tick 50, from ticks 10-49): K=8 codes = per-axis {low, high} split at each lane's calib median
//   → code_id = 8-bit index, one bit per lane (state8[a] ≥ med[a]) — a product code over the 8 lanes
code_id_t = Σ_a 2^a · (state8_t[a] ≥ med_a ? 1 : 0)                     // ∈ [0,255], but only K visited codes matter
```
Codebook shade = each visited code carries a **frozen per-code bias** = the sign of that code's mean deviation from the population-neutral over calibration (so the shade is content-addressed, not magnitude-driven):
```
code_bias[c] = clip(Σ_a sign(med_a_of_code_c − global_med_a), −1, +1) / 8     // frozen at tick 50
shade_vq = clip01(0.5 + G_vq · code_bias[code_id_t])                          // G_vq calibrated to swing 0.175
idle_vq  = 5.0 + 55.0·clip01(stage_env·(0.5 + urgency + 1.0·(shade_vq − 0.5)))  // own DISJOINT lane
```
The discreteness is the point: emit changes at **code boundaries** (a self-event flips one lane bit → a different code → a different frozen bias), not smoothly with the underlying continuous value.

## The 3 arms
- **ARM-LIVE** — `e_vq` off `idle_vq`.
- **ARM-FROZEN** — shade pinned 0.5, `og_h_frzF += (e_frzF != e_live)` every tick, VOID on mismatch.
- **ARM-SHOCK** — reuse `og_h_shock_mid`; POS-PASS ≥2.

## Distinguishing signature + bar (the G1 composition test at the seam)
Two signatures, both pre-registered:

**(S1) Code-selection** — a self-event selects a distinct code that changes emit: `ΔEff ≥ 0.10 ∧ margin ≥ 0.08` (baseline transducer-competence).

**(S2) Composition above additive floor — the G1 test, moved to the output seam.** Pick two lanes A, B (e.g. `coh_lane` = self-coherence, `ag_conflict` = tension). Measure emit-shade effect of each singly (code differs in only bit A; only bit B) vs the **combined held-out code** (both bits set — a code whose bias is NOT the sum of the singles because `code_bias` reads the joint sign pattern). Bar:
```
ΔEff_AB − (ΔEff_A + ΔEff_B) ≥ 0.05  ∧  the combined code is NOT visited in calibration (held-out)
```
i.e. non-additive interaction at the seam. This is precisely the g1-census / trunk-obj additive-floor test (`measurement-metalaw-form-tunable-bind-earned`: FORM tunable, BIND earned) — a bit-product code is *by construction* only main-effect-additive unless the substrate genuinely puts non-additive weight on the joint pattern. A positive here would be the first BIND signal anywhere, at the seam.

## Shuffle / theater-killer control
**ARM-SHUFFLE-CODEBOOK** (primary, THEATER-killer): randomly permute the `code_bias[]` assignment (fixed derangement, e.g. `c → (c·37+11)%256`) — same K codes, same visit frequencies, same marginal shade distribution, only the code→bias mapping scrambled. If ΔEff survives the shuffle, the effect is carried by shade *magnitude/frequency* not by *which concept* → THEATER. Bar: `margin_cb = ΔEff_live − ΔEff_shufcb ≥ 0.08`. Plus **ARM-INPERM** (tick-order stride-perm) as secondary, same as A/B.

## Frozen bars (pre-registered VERBATIM)
```
1 HARNESS-BUG(VOID):    og_h_frzF > 0
2 INSTRUMENT-FAIL:      POS-FAIL(shock<2) ∨ n_visited_codes < 4 (bottleneck never engaged)
                        ∨ combined code AB never held-out-testable (n_AB < 10)
3 FORCING-GATE(REVERT): N3 flips > 0 ∨ Ψ-guard fail
4 COMPETENT:            S1(ΔEff≥0.10 ∧ margin≥0.08) ∧ margin_cb≥0.08 ∧ POS ∧ N3=0 ∧ Ψ-ok
5 COMPETENT+BIND (rare): COMPETENT ∧ S2(ΔEff_AB−(ΔEff_A+ΔEff_B)≥0.05, held-out) — G1 signal at the seam
6 THEATER:              ΔEff < 0.02 ∧ POS-PASS ∧ n_visited≥4 ∧ margin_cb<0.08 (magnitude not concept)
7 DIRECTIONAL:          else
```

## $0-vs-real-decode cost + honest INSTRUMENT-FAIL risk
**Needs `--opgrip-live` + SPEC 1 densification.** The `state8` lanes are quasi-static in an unstimulated no-decode run (same starvation as B), so `n_visited_codes` collapses to 1–2 ⇒ bar 2 INSTRUMENT-FAIL. It requires the SPEC 1 tape to move the lanes across code boundaries and enough emits to fill the AB composition bucket. Cost: rides the SPEC 1 pod run (reads existing lanes, no extra decode) ≈ marginal; standalone ≈ **~30–45 min** CPU pod.

**What makes it likely INSTRUMENT-FAIL vs real (honest):** even fully densified, the composition test (S2) needs the held-out combined code visited ≥10 times on scored mid ticks with the singles also well-sampled — a 3-way sampling constraint on a starved axis. And S2's *positive* is the same wall four independent lenses have already hit (`substrate-framebreak-g1-combination-operator`, `g1g6-wall-engine-innocent-3axis`: additive floor everywhere, trained constructive bind never shown at 303M). The honest prior is **S2 fails → F lands at bar 4 (transducer-competent, no BIND) or bar 6 (THEATER)**. F is worth running not because S2 is expected positive but because it's the *only* remaining place to test the G1 bind claim at the output seam rather than the trunk objective — a negative here is a valuable fifth convergent lens; it is not a tune-to-green target.

---

