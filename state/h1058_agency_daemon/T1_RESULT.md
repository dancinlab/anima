# H_9269 Φ-leg — T1 POSITIVE CONTROL RESULT (real e1_slw_303m .clm)

**Verdict: T1 PASS — instrument confirmed. leg-b Φ = EVALUABLE (T3).**
Instrument-verification GREEN. Does NOT change the H_9269 🧱 KILL (that was decided by legs a+c, veto byte-identical across seeds). This only certifies that the redesigned Φ context (#3339 Part A) makes faithful-IIT4 Φ **decision-VARYING** on the real pre-MoE trunk — so the old Φ-flatness was a **regime property (constant consumed bytes), not an instrument/IIT4/unitization defect**.

## Run provenance
- ckpt: `e1_slw_303m.final.clm` (293MB, H_9269 daemon ckpt · d=3784 V=256 L=4 K=3)
- script: `t1_phi_variance_control.py` (#3339, FROZEN acceptance — run verbatim, no flag/bar edits)
- corpus: 4-cell register corpus `clm303_clean_corpus/{gen,sns}_{ko,en}.txt` (HF `dancinlab/anima-corpus-*`)
- draw: seed 20260712 · T=64 · 16 calib + 32 scored natural + 4 contrasts (2 constant-byte, 2 period-2)
- host: **summer** (pool, free — RTX5070 box, CPU numpy) · precision **fp32** (see note) · cost **$0**
- artifacts (this dir): `T1_RESULT.json` (raw), `T1_run.log` (stdout verbatim)

## STEP-0 gate — faithful IIT-4.0 mirror proof (`prove_mirrors_at_n(5)`)
PROVEN before scoring (a_phi_iit4_tool, no proxy):
- big-Φ ring5_s31 / s24: mirror=2.999999999 vs stdlib_hexa_ref=2.999999999, |Δ|=1.34e-10 OK
- faithful_phi n5 dim6 nb2: mirror=4.000000 vs stdlib_hexa_ref=4.000000, |Δ|=7.97e-10 OK
- matched-path n=5: big-Φ=18.185180, faithful=0.029795 · deterministic re-run True · faithful-units==bits.T (no continuous leak)

## FROZEN acceptance vs measured (VERBATIM bars, both maps)

| macro-map | sd(Φ) natural (bar ≥0.005) | distinct @4sf (bar ≥8/32) | families differ | PASS |
|---|---|---|---|---|
| `top_calib_variance` | **0.02193** (4.4×) | **31/32** | True | ✅ |
| `random`             | **0.02208** (4.4×) | **31/32** | True | ✅ |

Family class-means (Φ @4sf) — the positive-control signature (structure → high Φ, constant → 0):

| macro-map | mean natural | mean period-2 | mean constant |
|---|---|---|---|
| `top_calib_variance` | 0.04035 | 0.01212 | 0.00000 (≈3.2e-10) |
| `random`             | 0.02551 | 0.02825 | 0.00000 (≈3.2e-10) |

- Constant-byte windows → Φ≈0 (no informational structure) on BOTH maps; natural windows carry real Φ; the 3 families are not all Φ-equal. All three FROZEN sub-conditions met on both maps.
- frozen unit indices: tcv=[213,754,1071,1596,2132] · random=[143,1281,2301,2688,2838] (signal-blind, calib∩scored=∅).

## T3 evaluability
leg-b EVALUABLE iff distinct ≥ max(10, 20%·32=7) AND sd(Φ)≥0.005 AND null width>0.
- distinct 31 ≥ 10 ✅ · sd 0.022 ≥ 0.005 ✅ · sd>0 ⇒ F-shuffle null width>0 ✅ → **EVALUABLE**.

## Precision note (fp32 on the free host — decision-equivalent to fp64)
Canonical default is fp64; summer's 30G RAM can't hold the fp64 lean load (guard peak ~31.9GB > 28.8 avail), so the run used `ANIMA_DTYPE=float32` (lean peak ~17.8GB). This is decision-equivalent for T1: fp32 rounding is ~1e-6 in the trunk state → Φ perturbations far below both the 4sf distinctness grid (1e-4) and the sd bar (0.005), so fp32 **cannot manufacture** the observed 0.022 sd / 31-distinct variance, and higher precision can only **reduce** noise, never add signal. The observed variance is content-driven and real. The STEP-0 faithful-IIT4 gate is dtype-independent (stdlib mirror on fixed states) and PROVEN. A fp64 rerun on a ≥48G host is available if ever contested but would not change PASS/FAIL.

## What this does / does not mean
- ✅ The #3339 Part A redesign (true-consumed-bytes context + T=64) resolves real Φ variance on the 303M pre-MoE trunk → the Φ instrument is **confirmed**; leg-b is EVALUABLE for FUTURE Φ-dependent falsifiers.
- ⚠️ It does NOT run such a falsifier: that still needs Part B (varying-consumed-bytes daemon regime, `PARTB_REGIME_PREREG.md`, design-only) + a target H.
- ⚠️ It does NOT reopen H_9269 🧱 KILL — that verdict rests on legs a+c (veto byte-identical across 3 seeds = stage-schedule reflex). Recorded here as **instrument-verification GREEN** only.
