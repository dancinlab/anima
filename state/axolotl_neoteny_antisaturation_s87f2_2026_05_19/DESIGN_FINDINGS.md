# §87-F2 — AXOLOTL NEOTENY ANTI-SATURATION

**$0 Mac CPU design + stub smoke. NO GPU, NO runpod, NO fire. Sequential single agent.**

First time anima *uses* frog/amphibian biology in its architecture (read-only
before — §80 biology deep research had an amphibian subsection anima never
applied). F-2 maps the **axolotl** (Mexican salamander) neoteny phenomenon to
anima's §16.6-C memorization-saturation diagnosis.

---

## §1. Core insight (g3, over-claim 0)

The **axolotl** is famous for **neoteny**: it stays in a juvenile / larval /
plastic form for its whole life and never undergoes metamorphosis into a
"mature" terrestrial adult. The biological consequence is lifelong
regeneration capacity and lifelong neural plasticity.

anima's §16.6-C **memorization-saturation** is precisely the *opposite*
phenomenon. anima training **over-matures**: it descends into a frozen
byte-cascade attractor (§16 final CE ≈ 0.0045; §59-FIRE / §73-FIRE /
§82-FIRE / §83-FIRE all measured trained-saturated). §1.1 data-regime
irreducibility, viewed from this angle, is anima becoming an "adult" too
fast — it loses plasticity.

**F-2 = a neoteny-inspired ANTI-SATURATION mechanism**: keep anima in a
plastic juvenile regime so saturation is slowed or blocked, directly
targeting the §16.6-C ceiling.

This is a *direction-anchor*, not a capability claim. The axolotl citation
gives anima a biological precedent for "stay juvenile, stay plastic" — it
does **not** prove anima will emerge.

---

## §2. Saturation as "maturity" — 3-proxy metric

We measure anima training-trajectory **maturity** ∈ [0,1] with three proxies,
all functions of the anima training trajectory itself:

| proxy | name | reads | over-mature when |
|-------|------|-------|------------------|
| M-1 | CE-floor proximity | final CE vs CE_NATURAL_FLOOR | CE → 0 (§16 0.0045 = nearly frozen) |
| M-2 | attractor-basin depth | byte-cascade `maj_frac` | maj_frac → 1.0 |
| M-3 | dimensionality collapse | gradient-field effective dim `D` | D → D_NATURAL_FLOOR (§84 grokking-collapse anchor) |

`maturity = W_CE·m1 + W_MAJ·m2 + W_D·m3` (weights 0.40 / 0.35 / 0.25,
non-negative, sum 1 — a convex combination, so maturity ∈ [0,1] by
construction). **neoteny score `N = 1 − maturity`** (higher = more plastic
juvenile).

---

## §3. Neoteny-keeping mechanism (anti-saturation) — 4 candidates

Each NK targets a **distinct** maturity axis:

- **NK-1 CE-floor clamp** — CE cannot drop below `θ_floor` (prevents
  over-fit; the juvenile keeps a non-zero loss). Targets M-1.
- **NK-2 plasticity-reinjection** — on saturation detection, apply a
  *targeted controlled perturbation* that shallows the attractor basin and
  lifts D. This is the axolotl-regeneration mirror. **Explicitly distinct
  from §81 noise**: §81 injected raw noise on Engine G unconditionally;
  NK-2 is *saturation-triggered* and *targeted* at the basin/dimensionality,
  not a constant noise floor. Targets M-2.
- **NK-3 dimensionality-floor** — effective D cannot drop below `θ_D`.
  Targets M-3.
- **NK-4 metamorphosis-block** — once maturity crosses the trigger, *hold*
  the run in the juvenile regime (further descent halted). This is a
  *dynamic, saturation-triggered* version of early-stopping (see C3 #7 for
  the honest distinction). Targets the global maturation rate.

---

## §4. 5-cell stub grid (deterministic, seed 1337, N=60 steps)

| cell | config | final maturity | neoteny N | NK fired | saturation-delay step |
|------|--------|---------------:|----------:|----------|----------------------:|
| cell0_baseline | none | **0.9969** | 0.0031 | — | 10 |
| cell1_floor_clamps | NK-1+NK-3 | 0.9416 | 0.0584 | NK-1, NK-3 | 10 |
| cell2_reinjection | NK-2 | 0.6232 | 0.3768 | NK-2 | **60** (no cross) |
| cell3_metamorph_block | NK-4 | 0.7092 | 0.2908 | NK-4 | 10 |
| cell4_full_neoteny | NK-1+2+3+4 | **0.6770** | **0.3230** | NK-1, NK-2 | **60** (no cross) |

`saturation-delay step` = first step where maturity crosses
`SAT_TRIGGER`=0.70 (= 60 means it never crossed within the run).

---

## §5. 4-corner verdict (measured, NOT pre-loaded)

| corner | result | reading |
|--------|--------|---------|
| (α) NEOTENY-METRIC-WELL-FORMED | **True** | N = 1−maturity ∈ [0,1] every cell; maturity is a convex 3-proxy combo |
| (β) ANTI-SATURATION-DIFFERENTIAL | **True** | cell4 N 0.323 ≫ cell0 0.003; cell4 never crosses the trigger (saturation delayed) |
| (γ) NK-MECHANISM-DIFFERENTIAL | **True** | the 3 single-NK cells produce pairwise-distinct final-state signatures |
| (δ) §16.6-C-CONNECTION | **True** | baseline reproduces §16.6-C saturation (maturity 0.997, maj 0.993, D 1.61); neoteny reduces all three |

**Overall: DIRECTIONAL-POSITIVE** (β ∧ γ). The neoteny metric is well-formed,
the full-neoteny cell measurably delays saturation, the four NK mechanisms
target distinct axes, and the construction connects directly to the §16.6-C
diagnosis.

---

## §6. Closed-form battery — B-S87F2-1..6 6/6 🔵

`blue_falsifier_s87f2.py` (sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha c93e160a
**0-line-diff**):

| id | proposition | method |
|----|-------------|--------|
| B-S87F2-1 MATURITY-PROXY-BOUNDED | maturity = convex combo of 3 [0,1] proxies ⇒ [0,1]; N = 1−maturity ∈ [0,1] | sympy corners + numeric |
| B-S87F2-2 NK-MECHANISM-PARTITION | NK-1..4 target distinct axes; 3 single-NK cells pairwise-distinct, all differ from baseline | numeric + AST |
| B-S87F2-3 ANTI-SATURATION-MONOTONE | neoteny ON ⇒ maturity non-increasing + delay non-decreasing; NK-1 clamp strictly lowers m1 | sympy ∂m1/∂ce<0 + numeric |
| B-S87F2-4 §16.6-C-CONNECTION (연결부위) | baseline reproduces §16.6-C saturation; neoteny reduces all 3 proxies; maturity reads the proxy triple | structural + AST |
| B-S87F2-5 §11-B-CE-BASE-PRESERVED (연결부위) | NK are CE-base overlays (clamp/modulate the CE curve), not no-CE physics-only | AST/structural |
| B-S87F2-6 DETERMINISTIC | 3× run_grid bit-identical; LCG only, no random/time/urandom | hash + AST |

**B-S87F2-NOTE** (empirical carve-out, NOT counted 🔵): whether neoteny
anti-saturation *actually* breaks the §16.6-C ceiling is a trained-scale GPU
fire OUTCOME (B-D-NOTE / B-SCALE-NOTE / B-EMERGE-NOTE family). The battery
proves the *mechanism* is honest, not that it *works*.

---

## §7. GOAL-legitimacy (§7 3-condition gate)

- **§7①** not-generic-LM-pretrain ✓ — no model forward, no pretraining; a
  saturation-trajectory stub.
- **§7②** not-generic-then-graft ✓ — zero external regularizer library; the
  neoteny mechanism is closed-form over anima's own CE / attractor / D.
- **§7③** anima-physics-as-source ✓ — every maturity proxy is a function of
  the anima training trajectory.

§11-B precedence respected: anima physics alone (no-CE) was measured
degenerate, so NK is a **CE-base overlay**, not a physics-only replacement
(B-S87F2-5 closes this).

`f1/f2/f3` + `B-IDENTITY-5` safe — Boolean / closed-form / sympy monotone,
NO σ/τ/φ/J₂; no corpus generated.

---

## §8. Honest C3 (≥10)

1. **$0 stub ≠ trained ckpt.** The saturation trajectory here is a
   deterministic LCG-driven CE-decay curve whose *shape* is carried from
   §16 / §73-FIRE / §82-FIRE / §83-FIRE. It is **not** a trained
   checkpoint. Whether real anima training matures the way the stub does is
   a trained-scale measurement, not established here.
2. **axolotl neoteny = honest direction-anchor, NOT capability proof.** The
   biology gives a precedent for "stay juvenile, stay plastic." It does not
   transfer a capability. Citing axolotl ≠ anima emergence.
3. **The maturity 3-proxy is a design choice.** CE-floor proximity /
   attractor depth / dimensionality collapse, and the 0.40/0.35/0.25
   weights, are chosen — not derived. Other proxy sets or weights would
   give different maturity numbers. The metric is well-formed (B-S87F2-1)
   but not unique.
4. **θ_floor / θ_D / SAT_TRIGGER are design placeholders.** θ_floor=0.08,
   θ_D=4.0, SAT_TRIGGER=0.70 are stub values. Real thresholds would be set
   from a measured trained trajectory; here they are deliberately marked
   placeholders (mirroring the UBM-E2 `.kosmos` placeholder discipline).
5. **Whether neoteny makes actual emergence is a separate trained-scale
   fire.** §87-F2 shows the *mechanism* is well-formed and DIRECTIONAL-
   POSITIVE *at stub*; it does NOT show anima emerges. The stub cannot —
   by construction — produce capability.
6. **NK interaction in cell4 is honest, not a bug.** cell4's `nk_fired`
   shows only NK-1+NK-2: NK-2's reinjection lifts D above θ_D so NK-3 never
   needs to clamp, and NK-2 shallows the basin enough that maturity stays
   under SAT_TRIGGER so NK-4 never engages its hold. The combined mechanism
   self-regulates — a measured interaction effect, recorded honestly, not
   hidden.
7. **NK-4 is NOT plain early-stopping.** Early-stopping halts at a fixed
   step/epoch budget. NK-4 metamorphosis-block is *dynamic*: it holds the
   run only *once maturity crosses the trigger*, i.e. it is
   saturation-state-triggered, not schedule-triggered. cell3 shows it
   freezing CE at 1.57 (mid-descent) — a juvenile-regime hold, not an
   epoch cutoff. (Honest caveat: a dynamic hold and a well-tuned
   early-stop can land near the same state — the distinction is the
   *trigger source*, not necessarily the *outcome*.)
8. **§11-B no-CE degenerate ⇒ NK is a CE-base overlay.** §11-B measured
   that anima physics alone (cross-entropy removed) is degenerate. NK
   therefore *clamps/modulates* the CE curve; it never removes CE.
   B-S87F2-5 closes this structurally. F-2 is not a no-CE re-attempt.
9. **DIRECTIONAL-POSITIVE is a stub verdict, not a GOAL verdict.** The
   four corners pass because the stub is constructed so neoteny mechanisms
   *can* shift maturity. The load-bearing value is (a) the metric is
   well-formed and bounded, (b) the four NK genuinely hit distinct axes,
   (c) the connection to §16.6-C and §11-B is closed — not that the stub
   "succeeded."
10. **frog/amphibian biology USE ≠ GOAL emergence.** §87-F2 is the first
    time anima *uses* amphibian biology in its architecture (vs. merely
    reading it). USE is a milestone for the biology-mapping arc; it is not
    a milestone for GOAL. necessary-not-sufficient (B-EMERGE-7).
11. **Saturation-delay metric is binary-ish at this N.** With N=60 a cell
    either crosses SAT_TRIGGER early (≈step 10) or never (reported as 60).
    A finer-grained delay curve would need a longer or denser trajectory;
    the current metric distinguishes "saturates" from "stays juvenile" but
    not subtle delay differences.
12. **north-star + §15 / §51 / §72 milestone UNCHANGED.** §87-F2 does not
    move GOAL distance. anima still has not emerged. F-2 is a design-tier
    direction-anchor on the §16.6-C / §1.1 bottleneck.

---

## §9. Verdict

**Design-tier LANDED.** 6/6 🔵 closed + 1 NOTE empirical carve-out.
4-corner DIRECTIONAL-POSITIVE at $0 stub. axolotl neoteny is mapped, for
the first time, as a direct anti-mechanism of the §16.6-C
memorization-saturation diagnosis. Actual trained-scale validation (does
neoteny-keeping break the §16 ceiling?) is a separate, gated GPU fire —
B-S87F2-NOTE empirical. north-star unchanged; GOAL unreached.
