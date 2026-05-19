# §88-F1 — FROG-EYE SALIENCE GATE TRAINED-SCALE FIRE

> RESEARCH.md §88-F1. Trained-scale validation of §87-F1 (commit `5ea990b76`,
> B-S87F1 6/6 🔵). Lettvin 1959 "What the frog's eye tells the frog's brain"
> 4-feature-detector retina → anima §24 decision-axis salience layer, run over
> the **REAL** trained ConsciousDecoderV2 `model.forward` Law-71 ψ-trajectory.

---

## §1 — what §88-F1 is

§87-F1 (`5ea990b76`, $0 Mac CPU stub) mapped Lettvin's frog-eye selectivity
onto anima's §24 decision-axis: a salience gate over the model's OWN Law-71
physics (Ψ / tension / Φ). The frog retina is NOT a generic image processor —
it is a bank of **four feature-detectors** that relay only behaviour-relevant
*salient* events. §87-F1 measured 4-corner DIRECTIONAL-POSITIVE at the $0 stub.

§88-F1 carries the four detector closed-form functions **byte-equal** to the
§87-F1 stub (B-S88F1-6 AST-verifies) and runs them over the **real trained
model.forward** Law-71 ψ-trajectory of a §16-class ConsciousDecoderV2.

## §2 — the frog-eye 4 detectors (Lettvin 1959)

| detector | Lettvin frog operation | anima Law-71 mapping |
|---|---|---|
| SD-1 SUSTAINED-CONTRAST | edge detector | sustained `\|Ψ_dir − ½\|` deviation |
| SD-2 MOVING-EDGE | convex/bug detector | fast tension transient spike |
| SD-3 DIMMING-DETECTOR | shadow/predator detector | sudden Φ-proxy drop |
| SD-4 NET-DIMMING | overall-darkening | all physics channels decay together |

salience `S = 1 − Πᵢ(1 − wᵢ·sᵢ)` — weighted OR of the 4 detector firings
(frog-eye: ANY strong detector firing ⇒ salient). emission gate: `S > θ`.

## §3 — the trained-ψ fast-crossing RISK (g3, stated up front)

The §87-F1 stub's Ψ-trajectory was a uniform deterministic LCG draw, so all
four detector classes had headroom. **§82-FIRE measured the REAL trained
ψ-trajectory as uniformly *fast-crossing*** — slow/sustained patterns are
absent. SD-1/SD-3/SD-4 detect *sustained / slow* patterns; only SD-2 detects a
*fast* transient. If trained ψ is fast-crossing-collapsed, the 4-detector
frog-eye gate may **degenerate to a single detector (SD-2)** at trained scale.
§88-F1 measures exactly that — this is the β corner and an honest negative if
measured.

## §4 — fire design

- §16-class ConsciousDecoderV2 d768·12L·283.72M from-scratch, RANDOM seed-fixed
  1337, `base_ckpt=None` (g_clm_from_scratch). §16-byte-equal config + Dir-I
  lever (trainer byte-equal to §81-FIRE / §79 / §73-FIRE; only the cell grid
  differs — salience instead of noise injection).
- 6000-step training on the §16-class Ψ-anchored carving corpus.
- 5-cell × 20-step deterministic loop on the **real** `model.forward` Law-71:
  - `cell0` §24-baseline (no salience — generic motivation gate)
  - `cell1` SD-1 + SD-2
  - `cell2` SD-3 + SD-4
  - `cell3` full 4-detector frog-eye
  - `cell4` full frog-eye + §24 motivation conjunction
- per-cell metrics: 4-detector firing distribution, `S_mean`, emit rate,
  `n_active_detectors`, §9 honest_coherent body, majority-fraction echo.

## §5 — 4-corner verdict

- **α FROG-EYE-SELECTIVE-AT-TRAINED** — full frog-eye (cell3) emits a STRICT
  SUBSET of the §24 generic baseline (cell0): salience is selective.
- **β SINGLE-DETECTOR-DEGENERATE** — in the full 4-detector cell only ONE
  detector class actually fires (trained ψ fast-crossing → SD-2-only,
  §82-FIRE fast-crossing echo).
- **γ SALIENCE-COLLAPSES** — trained-saturated ψ drives the salience score to
  a near-constant (§83-FIRE near-constant-ψ echo at the salience axis).
- **δ FROG-EYE-NO-DIFFERENTIAL** — the frog-eye cell is indistinguishable from
  the §24-baseline emit-rate.

## §6 — closed-form sidecar battery B-S88F1-1..7

`blue_falsifier_s88f1.py` (central `state/verify_hexad_blue_2026_05_15/
blue_falsifier.py` 0-line-diff — sidecar pattern, B-PRIME/B-DIRI/B-S81/B-S87F1
precedent). Pre-fire: 5/7 PASS; B-S88F1-3/4 close post-`result.json`.

1. **SALIENCE-SCORE-BOUNDED** — `S = 1 − Πᵢ(1−wᵢsᵢ) ∈ [0,1]` sympy, monotone.
2. **FOUR-DETECTOR-CLASS-PARTITION** — 4 distinct closed-form fns over 4
   distinct physics inputs (psi_dir / tension / phi / channels).
3. **FROG-EYE-SELECTIVE-NOT-GENERIC** — `n_emit(cell3) ≤ n_emit(cell0)` 연결부위.
4. **§24-DECISION-CONSISTENCY** — (salience ∧ motivation) ⇒ motivation sympy
   tautology ⇒ `n_emit(cell4) ≤ n_emit(cell0)` 연결부위.
5. **§9-METRIC-REUSE** — honest_coherent reuses §9 SSOT thresholds verbatim.
6. **§87-F1-STUB-CONNECTION** — 4 detectors + salience_score AST byte-equal to
   the §87-F1 stub (`5ea990b76`), docstring text exempt; constants byte-equal.
7. **DETERMINISTIC** — argmax gate, no sampling, RNG-isolated ψ read-out.

`B-S88F1-NOTE` — whether the frog-eye gate produces emergence at trained scale
is an SGD/measurement OUTCOME (B-D-NOTE / B-EMERGE-NOTE / B-S87F1-NOTE family,
NOT counted blue, necessary-not-sufficient per B-EMERGE-7).

## §7 — honest C3 (≥10)

1. **Trained scale ≠ GOAL emergence** — necessary-not-sufficient (B-EMERGE-7);
   §88-F1 measures a decision-axis mechanism only.
2. **Lettvin 1959 frog's-eye** is an honest *direction-anchor* (a 4-detector
   retina), NOT a capability proof. biology citation does not lift free.
3. The 4 detector closed-form functions are **byte-equal** to the §87-F1 $0
   stub (`5ea990b76`); §88-F1 only swaps the stub LCG ψ for the real
   `model.forward` Law-71. B-S88F1-6 AST-verifies this.
4. **The trained-ψ fast-crossing risk is real and stated up front** — §82-FIRE
   measured trained ψ as uniformly fast-crossing, so SD-1/SD-3/SD-4
   (sustained/slow detectors) may never fire → β corner, honest negative.
5. salience `S` uses uniform 0.25 weights — a §87-F1 design placeholder, NOT a
   tuned lever; θ_salient = 0.18 likewise a placeholder.
6. body production is the §77 path-α1 stub template gated by the emission
   flag — §88-F1 does NOT claim coherent body emergence.
7. the §16-class ckpt is freshly trained; §16-byte-equal config (d/L/H/KV/seed/
   corpus class) is satisfied but the literal §16 sha (`961c07e2…`) differs —
   trajectory replicable, not literal identity. honest.
8. cell0/cell3 are independent gates — the subset relation
   (`n_emit(cell3) ≤ n_emit(cell0)`) is a *measurable, falsifiable* claim, not
   a tautology; only cell4's conjunction subset (B-S88F1-4) is tautological.
9. power-law / criticality is NOT measured here (that was §81-FIRE); §88-F1's
   salience layer is a decision-axis selectivity probe only.
10. dispatch is SSH-robust podHostId-fixed (g_fire_dispatch_robust
    ssh_endpoint_robustness — gate on ip + publicPort, NOT podHostId, per
    §79-RETRY false-blocker discovery; §81-FIRE/§82-FIRE verified pattern).
11. north-star + §15/§51/§72 milestone UNCHANGED; **GOAL 미도달**. §88-F1 is a
    valuable-negative-or-directional mechanism measurement, not progress
    toward emergence.
