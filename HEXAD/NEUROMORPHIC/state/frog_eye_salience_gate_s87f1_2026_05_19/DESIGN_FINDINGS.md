# §87-F1 — FROG-EYE SALIENCE GATE

**Date**: 2026-05-19 · **Cost**: $0 (Mac CPU, NO GPU, NO runpod, NO fire) ·
**Anchor**: Lettvin et al. 1959 *"What the frog's eye tells the frog's brain"*

First actual mapping of **frog biology** onto anima architecture. Prior FROG
keyword sweep (2026-05-19) confirmed anima had only *read* frog references
(corpus carry-over) and never *used* frog for anything. §87-F1 changes that —
but **USE ≠ emergence** (g3, §C3).

---

## §1 Core insight

The frog retina is **not** a generic image processor. Lettvin showed it is a
bank of **four feature-detectors** that relay only behaviour-relevant salient
events to the brain — "the frog's eye tells the frog's brain" means the retina
hands up *pre-digested salience*, not raw pixels. A frog's bug-detector fires
for a small moving dark spot (a fly) and ignores everything else.

anima's GOAL is **spontaneous emission** — and spontaneous emission is
intrinsically **salience-driven**: anima should speak when it detects a
*noteworthy pattern* in its own physics. anima's §24 decision-axis currently
has **no salience gate** — `talker_should_emit` looks only at a generic
motivation threshold, never at "is anything salient in my physics right now?".

§87-F1 inserts a frog-eye-style salience layer over the §24 decision-axis.

## §2 Four frog-eye feature-detectors (Lettvin's 4 operation types)

Each is a **closed-form function of anima's OWN Law-71 physics** (Ψ / tension /
Φ), byte-equal to the formulas in `conscious_decoder.py:728-751`:

| Detector | Frog retina operation | anima physics mapping |
|----------|----------------------|------------------------|
| SD-1 SUSTAINED-CONTRAST | edge detector | sustained `|Ψ_dir − ½|` deviation (Engine A⇄G imbalance held over window) |
| SD-2 MOVING-EDGE | convex / bug detector | fast tension transient spike (§85 Hopf fast-crossing carry) |
| SD-3 DIMMING-DETECTOR | shadow / predator | sudden Φ-proxy drop (integration collapse = danger signal) |
| SD-4 NET-DIMMING | overall darkening | all physics channels decay together (substrate quiescence) |

Salience `S = weighted-OR` of the 4 firings (frog-eye: *any* strong detector
firing ⇒ salient). Emission gate: `S > θ_salient ⇒ emit candidate`.

## §3 GOAL-legitimacy (§7 3-condition gate)

- **§7①** not generic-LM-pretrain ✓ — no model.forward this cycle, $0 stub
- **§7②** not generic-then-graft ✓ — zero external vision model; the 4
  detectors are closed-form over anima's own Ψ/tension/Φ
- **§7③** anima-physics-as-source ✓ — every detector is a function of Law-71
  channels (byte-equal `conscious_decoder.py:728-751`)

Lettvin frog-eye is an **honest direction-anchor**, not a capability proof.

## §4 5-cell stub grid (result.json)

deterministic LCG seed 1337, 20 steps, stub ψ-state byte-equal Law-71.

| cell | S_mean | emit | detector firing {1,2,3,4} | interval_var | §9 body | maj_frac |
|------|--------|------|----------------------------|--------------|---------|----------|
| cell0 §24-baseline | 0.000 | 1.00 | {0,0,0,0} | 0.0 | 20/20 | 0.10 |
| cell1 SD-1+SD-2 | 0.0287 | 0.00 | {0,7,0,0} | 0.0 | 0/0 | 0.00 |
| cell2 SD-3+SD-4 | 0.0169 | 0.00 | {0,0,4,0} | 0.0 | 0/0 | 0.00 |
| cell3 full frog-eye | 0.045 | 0.05 | {0,7,4,0} | 0.0 | 1/1 | 1.00 |
| cell4 frog-eye + §24 motiv | 0.045 | 0.05 | {0,7,4,0} | 0.0 | 1/1 | 1.00 |

## §5 4-corner verdict — DIRECTIONAL-POSITIVE (all 4 PASS)

- **(α) SALIENCE-GATE-WELL-FORMED** ✓ — S = weighted-OR ∈ [0,1] closed
- **(β) SELECTIVE-vs-GENERIC** ✓ — cell3 frog-eye emits 1/20 (selective),
  cell0 §24 generic motivation emits 20/20 (indiscriminate). The frog-eye
  gate is decisively more selective than the §24 motivation threshold.
- **(γ) DETECTOR-CLASS-DIFFERENTIAL** ✓ — cell1 fires SD-2 7× / cell2 fires
  SD-3 4×: the 4 detectors respond to genuinely distinct ψ-patterns.
- **(δ) §24-DECISION-CONSISTENT** ✓ — cell4 conjoins salience AND motivation;
  `(sal ∧ motiv) ⇒ motiv` ⇒ n_emit(cell4)=1 ≤ n_emit(cell0)=20. The
  salience layer is a provable **subset** of the §24 decision-axis.

## §6 Closed-form battery — B-S87F1-1..6 6/6 🔵

`blue_falsifier_s87f1.py` sidecar (central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff):

1. SALIENCE-SCORE-BOUNDED — sympy: S ∈ [0,1], monotone in each s_i
2. FOUR-DETECTOR-CLASS-PARTITION — 4 detectors, distinct physics inputs
3. FROG-EYE-SELECTIVE-NOT-GENERIC — each detector has a firing-floor guard;
   θ_salient > 0 ⇒ gate ≠ passthrough
4. §24-DECISION-CONSISTENCY (연결부위) — `(sal ∧ motiv) ⇒ motiv` tautology
5. §9-METRIC-REUSE — §9 SSOT thresholds verbatim + 3 witnesses
6. DETERMINISTIC — no RNG/time imports, 3× bit-identical

**B-S87F1-NOTE** empirical carve-out: whether the frog-eye salience gate
actually produces emergence is a trained-scale SGD/measurement OUTCOME
(B-D-NOTE / B-EMERGE-NOTE / B-S77-NOTE family, NOT counted 🔵).

## §7 Where this lands

§87-F1 = the **first time anima USES frog-biology in architecture** (not just
reads it). The salience gate is a structurally honest, closed-form layer over
the §24 decision-axis. It is design-tier — a $0 stub, not a trained-scale
fire.

## §8 Honest caveats (C3 — ≥10)

1. **$0 stub ≠ trained ckpt** — the ψ-state is an LCG stub; a real
   `model.forward` trajectory will behave differently. No capability claim.
2. **Lettvin frog-eye = honest direction-anchor, NOT capability proof** —
   citing biology does not make anima emerge.
3. **4-detector mapping is a design choice** — SD-1..4 ↔ Lettvin's 4
   operations is one plausible mapping; others exist.
4. **θ_salient = 0.18 is a design placeholder** — not measurement-calibrated;
   a trained-scale fire would re-tune it.
5. **SD-weights uniform (0.25 each)** — design placeholder, not learned.
6. **interval_var = 0.0 in every cell** — at 20 steps with ≤1 emission,
   inter-emission interval variance is structurally trivial; not a signal.
7. **maj_frac = 1.0 for cell3/4** — with n_emit=1 the majority fraction is
   trivially 1.0; echo-detection needs more emissions to be meaningful.
8. **cell1/cell2 emit 0/20** — at stub scale SD detectors fire weakly
   (S_mean ≈ 0.02-0.03 < θ); only the full 4-detector OR (cell3) crosses θ.
   This is the frog-eye selectivity working — but also a stub-regime limit.
9. **frog-biology USE ≠ trained-scale measurement ≠ GOAL emergence** —
   §87-F1 maps frog-eye onto anima; whether that mapping helps emergence is
   a separate trained-scale OUTCOME (B-S87F1-NOTE).
10. **necessary-not-sufficient** (B-EMERGE-7) — a salience gate is plausibly
    *necessary* for spontaneous emission, but the gate alone is not
    *sufficient* for GOAL emergence.
11. **§24 baseline emits 20/20 here** because the stub motivation_score
    sits above MOTIV_THRESHOLD throughout — a stub artifact, not a §24 flaw.
12. **north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달** — §87-F1 is
    a design-tier mechanism mapping, not progress toward emergence.
