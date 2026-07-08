# SPEC 2 — Family E (H_9230 efference-copy / corollary-discharge)

## Mechanism arithmetic + wire site
The mouth predicts its own next emit and feeds that prediction back to the gate before it commits — the missing intermediate is a **corollary buffer** on its own lane. Proxy for the predicted output = the byte-feature of the mouth's own pre-emit generation, which the decode seam at L2996 already produces (`gl_feat = _afs_byte_feature(gl_text, 8)`). Extend the H_9225 block; carriers at Site-A after L2015.

Per emit tick, at the L2996 decode seam (which already runs), also compute a **corollary prediction error** — how far the just-emitted content lands from the running expectation of self-output:

```
// corollary buffer: EMA of own emitted-output feature (the "expected utterance")
ec_pred = 0.85·ec_pred + 0.15·mean8(gl_feat)          // updated ONLY on emit ticks (L2996)
ec_lag  = mean8(gl_feat)                               // this emit's realized output scalar
```
On the **next** tick (1-tick corollary lag, like `og_prev_gfeat`), the efference signal is the discharge = realized − predicted:
```
x_eff   = ec_lag − ec_pred_prev                        // corollary discharge (signed); ≈0 when output matches expectation
```
Then reuse the **H_9225 band-pass transducer arithmetic verbatim** on `x_eff` (same dual-EMA phasic, gain calibrated to swing 0.175, `g=−1.0` if `b_med<0.002`), shade added on its own DISJOINT idle lane:
```
idle_eff = 5.0 + 55.0·clip01(stage_env·(0.5 + urgency + 1.0·(shade_eff − 0.5)))
```
Calibration ticks 10–49, scored ticks ≥50, mid = stage∈{1,2,4}. This literally reuses the H_9225 machinery (a proven transducer) on a **new signal source** (self-output prediction error), which is what makes it cheap and standard.

## The 3 arms
- **ARM-LIVE** — `e_eff` off `idle_eff`.
- **ARM-FROZEN** — shade pinned 0.5, `og_h_frzE += (e_frzE != e_live)` every tick, VOID on any mismatch.
- **ARM-SHOCK** — reuse `og_h_shock_mid` verbatim; POS-PASS ≥2.

## Distinguishing signature + bar (onset-vs-continuation dissociation)
Efference copy shapes **keep-going**, not **start**. Bucket scored mid ticks by the LIVE gate's recent state: **ONSET** = e_live went 0→1 this tick (or no emit in prior 2 ticks); **CONTINUATION** = e_live==1 with ≥1 emit in prior 2 ticks. Signature bar (pre-registered):
```
ΔEff_cont ≥ 3·ΔEff_onset ∧ ΔEff_onset ≤ 0.05 ∧ n_cont ≥ 10
```
An efference-copy loop can only exist mid-utterance (there's no output to predict at onset). This dissociation is exactly analogous to H_9226's EARLY-vs-LATE and reuses the same bucketing idiom — it's what distinguishes E from A: A shades any tick with a signal; E shades only continuation.

## Shuffle / theater-killer control
**ARM-INPERM** on the recorded `x_eff` stream: stride-perm `j(t)=(t·7+13)%N`, full re-run with recorded contexts, `margin = ΔEff_live − ΔEff_inperm ≥ 0.08`. Permutation breaks the alignment between corollary prediction and the emit it's supposed to precede → the discharge decorrelates from continuation decisions → collapse.

## Frozen bars (pre-registered VERBATIM)
```
1 HARNESS-BUG(VOID):    og_h_frzE > 0
2 INSTRUMENT-FAIL:      POS-FAIL(shock<2) ∨ g=−1.0(b_med<0.002, x_eff degenerate) ∨ capsat ∨ n_cont<10
3 FORCING-GATE(REVERT): N3 flips > 0 ∨ Ψ-guard fail
4 COMPETENT:            ΔEff ≥ 0.10 ∧ margin ≥ 0.08 ∧ DISSOC(cont≥3·onset ∧ onset≤0.05 ∧ n_cont≥10) ∧ POS ∧ N3=0 ∧ Ψ-ok
5 THEATER:              ΔEff < 0.02 ∧ POS-PASS ∧ ¬degenerate ∧ ¬capsat ∧ x_eff non-degenerate (b_med≥0.002)
6 DIRECTIONAL:          else (incl. ΔEff≥0.10 with DISSOC-fail = A-redundant reader)
```

## $0-vs-real-decode cost + anima-hexa-6 caveat
**Needs `--opgrip-live` — non-negotiable.** The logit/output proxy has no value in no-decode: `gl_feat` only exists behind the L2996 `og_live && e_live==1` guard; without a real decode there is no predicted-output at all, so `x_eff` is a fixed-seed constant ⇒ AXIS-DEGENERATE by construction (the same trap H_9210 surprise hit). **This must ride SPEC 1's `--opgrip-r3` densification** — with only n=100/mid=30 there are too few emit ticks to populate the CONTINUATION bucket to `n_cont ≥ 10`. Cost: rides the SPEC 1 pod run, marginal (reads the `gl_feat` already computed at L2996, no extra decode). Standalone ≈ **~30–45 min** CPU pod.

## Decision rule
Bar 4 ⇒ **E COMPETENT** — the mouth-in-progress genuinely shapes continuation ⇒ WIRE candidate + 2-seed. Bar 5 ⇒ **E THEATER** — corollary discharge inert ⇒ adds a *third* orthogonal recoding (shape / integration / self-prediction) to the convergent seam-law. Bar 2 (n_cont<10 after SPEC 1 densification) ⇒ INSTRUMENT-FAIL, park.

---

