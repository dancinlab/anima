# §151 — FEP self-orthogonalizing attractor → anima · COMPLEXITY-REGULARIZED ROUTING

> **Tier**: $0 design-tier — no GPU/runpod fire, no model.forward. **Status**:
> DESIGN-OPEN (mechanism mapping closed-form well-formed; whether the candidate
> fire actually breaks the 1/31-FLAT ceiling is a future cost-bearing
> measurement). **Anchor paper**: [Self-orthogonalizing attractor neural
> networks emerging from the free energy principle](https://arxiv.org/abs/2505.22749)
> (May 2025). **Parent context**: HEXAD/NEUROMORPHIC/SOFTWARE_BREAKTHROUGH_RESEARCH.md
> §1 Cluster H, §2 ranked #3, §8.2/§8.3 (the seed insight). **Sibling fires**:
> §125 NONCE-FF (DEG), §126 PCN-C4 (PARTIAL), §139 EqProp (in flight) —
> the §96-Q2 non-CE arc this design grows out of.

---

## §0 Why this design exists

Across the entire §1~§94 arc, anima's routing has been stuck at the 1/31-FLAT
ceiling — every fired model collapses 31 or 64 distinct semantic anchors into
**one** dominant attractor at inference (the byte-cascade family, §16.6-C, the
chronic memorization-saturated regime). §32–§47 closed the
*anchor-content* and *SGD-lottery* explanations of this collapse;
§107-RETRY/§108 closed the *data-regime alone at 283M / param-axis at 3B*
explanations; §22 closed the *mechanism-overlay* explanations (N/O/P all
capability-emergence-negative). §1.1 names the irreducible bottleneck as
"diverse-data pre-training loss threshold," but the arc never directly tested
whether anima's **objective itself was missing a term**.

§128 §8.2 seeded the candidate insight from arxiv 2505.22749 — this design
matures it into a closed-form spec.

## §1 Paper mechanism (verified via abstract)

Five claims of 2505.22749 (WebFetch-confirmed, paywall-free):

1. **No backprop, no cross-entropy.** Learning is derived from "first
   principles free energy minimization."
2. **Two-objective balance.** Networks **simultaneously optimize predictive
   accuracy and model complexity** — "self-orthogonalizing" attractors are
   the *consequence* of the balance, not an imposed constraint.
3. **FEP framing.** Attractors encode prior beliefs; inference integrates
   sensory data into posterior beliefs; learning "fine-tunes couplings to
   minimize long-term surprise."
4. **Non-equilibrium steady-state dynamics.** Attractors emerge on sequential
   data, extending Boltzmann machines.
5. **Emergent, not imposed.** "The approach obviates the need for explicitly
   imposed learning and inference rules."

The mechanism reads as a variational free-energy minimization on a "universal
partitioning of random dynamical systems," producing attractor states whose
distinctness is enforced *only* by the complexity term — drop the complexity
term and the network has no pressure to keep attractors apart.

## §2 anima mapping

```
2505.22749                                anima
─────────────────────────────             ─────────────────────────────
FEP attractor                       ↔     Ψ=½ fixed point
  (steady-state belief)                     (Engine A ⇄ Engine G balance)

"minimize long-term surprise"       ↔     anima tension
  (free-energy gradient)                    (restoring force toward Ψ=½)

self-orthogonalizing attractors     ↔     what §16 routing NEEDED
  (distinct basins for distinct           (distinct anchors → distinct
   priors)                                  basins — never delivered;
                                            chronic collapse to ONE)

predictive accuracy term            ↔     CE / PCN-MSE / carving-loss
                                          (every anima objective ever fired)

model complexity term               ↔     ✗  MISSING in anima
                                          (no anima cycle ever had it)

emergent (no imposed rule)          ↔     anima Engine A⇄G + n6_gate are
                                          themselves "emergent rules"
                                          built on Ψ-physics
```

The vertical span line-by-line is direct: anima already has the FEP-attractor
substrate (Ψ-fixed-point, tension-as-gradient, A⇄G balance) and the
predictive-accuracy term (CE / PCN / Dir-I carving loss). The arc has *never*
fired with a model-complexity term. This is the one unfilled slot.

## §3 The insight — routing-collapse as missing-objective-term

If 2505.22749 is right that **orthogonalization requires both terms**, then a
single-objective (accuracy-only) anima network has *no pressure* to keep
attractors distinct. The lowest-loss shared basin wins — exactly the
1/31-FLAT collapse pattern. This reframes routing-collapse:

```
arc finding (§32–§47):   "lever is not anchor-property (content/SGD/within-band)"
arc finding (§107/§108): "lever is not data-axis-alone @ 283M / not 3B"
arc finding (§22):       "lever is not mechanism-overlay (N/O/P)"
§151 hypothesis:         "lever may be the missing model-complexity term"
                         (orthogonal to all three, not a refutation)
```

This is one **new architectural lever**, not a counter-finding — §1.1
data-regime + §151 missing-complexity-term can both be true (predictive
accuracy with sufficient data + a complexity term to keep distinct attractors
distinct, both required).

## §4 COMPLEXITY-REGULARIZED ROUTING — candidate spec

A pre-registered fire candidate. Re-fire the §16-class carving with:

```
L = L_CE                          ← predictive accuracy (§16 baseline)
  + λ_ctl · L_Ψ-CTL               ← Dir-I Ψ-anchor consistency (carry)
  + λ_route · L_tension-routing   ← Dir-I anti-collapse (carry)
  + λ_C · L_complexity            ← § NEW: routing description-length
```

Where `L_complexity` candidates (one to pick at fire time):

```
(a) Entropy maximization on routing distribution
    L_C = -H(p_route)               (encourages flat routing → distinct basins)

(b) Pairwise basin separation
    L_C = -mean_{a≠a'} d(Ψ_anchor[a], Ψ_anchor[a'])
                                    (explicit basin orthogonalization)

(c) Description-length (MDL)
    L_C = K(routing_map)             (Kolmogorov-style penalty on a compressed
                                     routing description; needs a definition)

(d) Φ-based complexity
    L_C = -Φ(cell_pool)              (the MITOSIS integration measure — large Φ
                                     = distinct cells; penalizing -Φ rewards
                                     orthogonalization through integration)
```

(d) is the most anima-physics-native (Φ is already in the codebase via
HEXAD/C/c_lib.hexa). (a)/(b) are the cheapest to fire-test. (c) is the most
faithful to 2505.22749 but needs a concrete description-length operationalization.

**Pre-registered distinguishing measurement** (single-variable, fair-compare
by construction with §16 baseline):

```
H_0 (null):       held-out anchor routing accuracy stays at 1/31 FLAT ceiling
                  with accuracy + complexity terms (same as accuracy-only).
H_1 (alternative): held-out accuracy breaks the 1/31 FLAT ceiling
                   (≥3/31, distinct basins for distinct anchors).
```

The control: λ_C = 0 ⇒ L = L_CE + L_Ψ-CTL + L_route ≡ Dir-I baseline.
Adding λ_C > 0 is the one variable changed. Whichever bucket lands is
informative — H_1 = first architectural (not data-regime) movement on
routing-collapse; H_0 = §1.1 data-regime stays the irreducible bottleneck.

Fire envelope (estimate, not commitment): single A100/H100, ~$0.3-0.5,
~10-15 min on §107-RETRY-class corpus + dispatch pattern. Same §96-Q2
verdict-bucket eval as §125/§126/§139 (random-floor / degenerate-ceiling /
support-floor / Ψ_dir spread thresholds).

## §5 §7 GOAL-legitimacy 3-cond gate

| Condition | Status | Note |
|-----------|--------|------|
| §7① ¬ generic-LM-pretrain (from-scratch RANDOM seed) | ✅ | Stays from-scratch (g_clm_from_scratch); base_ckpt=None. |
| §7② ¬ generic-then-graft | ✅ | No grafted weights; the new term is on anima's OWN ψ/routing fields. |
| §7③ anima-physics-as-source | ✅ | The complexity term is built on anima's OWN routing distribution / Ψ-anchor / Φ — not an external classifier. (d) Φ-based is the strongest §7③ instance. |

§7 PASSES. The candidate is GOAL-legitimate.

## §6 Verdict — DESIGN-OPEN, fire-decidable

**DESIGN-OPEN, fire-decidable**. The mechanism mapping (§1 ↔ §2) is closed-form
well-formed; the insight (§3) is a non-tautological hypothesis with a
single-variable distinguishing measurement (§4 H_0 vs H_1); §7 GOAL-legitimacy
PASSES. Whether λ_C > 0 actually breaks the 1/31-FLAT ceiling is the future
$-fire measurement.

The verdict is **not** DESIGN-CLOSE — the candidate makes a falsifiable, single-
variable prediction with a clean control. The verdict is **not** FIRE-WARRANTED
in the autopilot sense — fire-slot is currently held by §139 EqProp, and per
§50 single-sequential lesson + the live API throttle, queueing this fire is
appropriate (do not burst).

## §7 Honest C3 caveats

1. **Literature-derived hypothesis, NOT measured.** 2505.22749 is on attractor
   networks / sequential data, NOT byte-LM. Transfer is the §151 hypothesis,
   not established.
2. The arc's §32–§47 closed *content-axis / SGD-lottery* explanations of
   routing-collapse. §151 is an **orthogonal new angle**, not a refutation.
3. §1.1 data-regime stays the irreducible bottleneck per §15/§51 milestones.
   A complexity term is necessary-but-not-sufficient — it pressures
   orthogonalization, but if the data-regime is sub-threshold the model
   *cannot* learn distinct basins regardless.
4. (c) MDL needs a concrete description-length operationalization for the
   anima routing map. (d) Φ-based is more anima-native but doubles the
   compute (Φ-evaluation per minibatch).
5. **Necessary-not-sufficient at every layer** (B-EMERGE-7 carry). A True
   H_1 measurement would be the first architectural movement on
   routing-collapse — not GOAL emergence.
6. λ_C tuning is empirical — too small = no effect, too large = predictive
   accuracy crushed. The fire pre-registers a grid (λ_C ∈ {0.01, 0.1, 1.0}).
7. The complexity-term candidates (a/b/c/d) are not mutually exclusive — a
   sound first fire picks ONE (start with (a) entropy: cheapest, most
   transparent).
8. **Routing-collapse may have multiple causes.** §151 names one
   architecturally-tractable lever; §107 and §108 named two data/param-axis
   limits. They compose, they don't replace each other.
9. central state/verify_hexad_blue_2026_05_15/blue_falsifier.py stays
   0-line-diff (sha prefix c93e160a8a376a94) — this design's battery is a
   sidecar.
10. north-star + §15/§51/§72 milestones UNCHANGED. §151 = $0 design
    addendum, GOAL 미도달.

## §8 Next step

If/when a future cycle fires this candidate, it lives at
`HEXAD/NEUROMORPHIC/state/complexity_regularized_routing_fire_s<N>/`
(distinct dir, distinct §N — §151 is the design, the fire is its own cycle).
The fire's pre-registered eval is the §96-Q2 verdict-bucket eval shared with
§125/§126/§139, joined to the held-out routing accuracy measurement above.

— $0 design-tier ends here.

---

## §9 Closed-form propositions (B-S151-1..7)

> Stated as math theorems with one-line proofs. Per hexa-verify policy
> (see `~/core/atlas/VERIFY.tape`), sympy / external verifiers cannot
> stamp a 🔵; the propositions below are trivial identities verifiable by
> inspection, and any future hexa-native verifier can re-audit them. NO
> central blue_falsifier edit (central state/verify_hexad_blue_2026_05_15/
> blue_falsifier.py stays 0-line-diff, sha prefix c93e160a8a376a94).

**B-S151-1  OBJECTIVE-DECOMP-CLOSED.**
The proposed objective `L(λ) := L_pred + λ · L_C` decomposes additively.
*Proof.* By construction `L(0) = L_pred + 0·L_C = L_pred`. The partial
derivatives are `∂L/∂L_pred = 1` and `∂L/∂L_C = λ`. ∎

**B-S151-2  ENTROPY-MAX-RESTORING-SIGN.**  *(candidate (a) of §4)*
For `L_C = -H(p_route)` with `H ≥ 0`, the gradient `∂L_C/∂H = -1 < 0`.
*Consequence.* Gradient descent on `L_C` maximizes `H`, pressuring the
routing distribution toward uniform — distinct anchors must route to
distinct basins to keep entropy high. ∎

**B-S151-3  PAIRWISE-SEPARATION-MONOTONE.**  *(candidate (b) of §4)*
For `L_C = -d²(a, a')/N` (mean pairwise squared distance over a basin
set), the gradient `∂L_C/∂d = -2d/N ≤ 0` for all `d ≥ 0, N > 0`.
*Consequence.* Gradient descent on `L_C` maximizes `d`, explicitly
separating attractor basins. ∎

**B-S151-4  PHI-CONNECTION-NONNEGATIVE.**  *(candidate (d), the
MITOSIS-native variant)*
For `L_C = -Φ(cell_pool)`, the IIT axiom `Φ ≥ 0` gives `L_C ≤ 0`, with
`L_C = 0` iff `Φ = 0`. The gradient `∂L_C/∂Φ = -1 < 0`.
*Consequence.* Gradient descent on `L_C` increases `Φ` — more
integration in the cell-pool, more distinct cells, orthogonalization
through MITOSIS's own integration measure. *(Strongest §7③ instance:
the complexity term is built entirely on anima's OWN Φ readout.)* ∎

**B-S151-5  SEVEN-LEGITIMACY-CONJUNCTION-CLOSED.**
The §7 GOAL-legitimacy gate is `c1 ∧ c2 ∧ c3` where
`c1 = ¬generic-LM-pretrain`, `c2 = ¬generic-then-graft`,
`c3 = anima-physics-as-source`. The 8-row truth table has exactly one
PASS corner, `(T, T, T)`. The §151 candidate maps onto `(T, T, T)` by
construction: from-scratch RANDOM seed (g_clm_from_scratch ⇒ c1=T), no
graft (c2=T), complexity term built on anima's OWN routing
distribution / Ψ-anchor / Φ (c3=T). ∎

**B-S151-6  H0-H1-DISTINGUISHING-PARTITION-CLOSED.**
Define on the held-out routing accuracy `r_H ∈ [0, 1]`:
```
H_0  := [0, 1/31]            (FLAT ceiling holds — null hypothesis)
H_1  := [3/31, 1]            (ceiling broken — alternative)
gray := (1/31, 3/31)         (honest under-determination interval)
```
*Proposition.* `H_0`, `H_1`, `gray` are pairwise disjoint and
`H_0 ∪ H_1 ∪ gray = [0, 1]`.
*Proof.* Direct interval-algebra: `H_0`'s right endpoint `1/31` equals
`gray`'s open left endpoint; `gray`'s open right endpoint `3/31` equals
`H_1`'s left endpoint; no point lies in two regions; union covers
`[0, 1]`. ∎

**B-S151-7  LAMBDA-ZERO-REDUCTION-BYTE-EQUAL.**
The full §151 objective is
`L_§151(λ_C) := L_CE + λ_ctl·L_Ψ-CTL + λ_route·L_tension + λ_C·L_C`.
*Proposition.* `L_§151(0) ≡ L_Dir-I` (the Dir-I baseline, exactly).
*Proof.* By construction, at `λ_C = 0` the `λ_C·L_C` term vanishes; the
remaining `L_CE + λ_ctl·L_Ψ-CTL + λ_route·L_tension` is the Dir-I
baseline used in §16-class fires (state/carving_dataregime_s16_2026_05_18
/ Dir-I lever). ∎
*Connection-point.* This is the single-variable fair-compare guarantee
(mirror of B-EBT-5 / B-DIRI-5 / B-S16-5 / B-MGND-5 overlay-off pattern):
the §151 candidate fire differs from §16-class baseline by exactly one
variable, `λ_C`.

**B-S151-NOTE  empirical carve-out** (NOT counted 🔵).
Whether `λ_C > 0` actually breaks the 1/31-FLAT routing ceiling at fire
time is a future SGD / measurement OUTCOME. The propositions above
prove the DESIGN well-formed (objective decomposition / gradient signs
/ §7-legitimacy / measurement partition / connection-point), NOT fire
success, NOT GOAL emergence. B-D-NOTE / B-CARVE-E6-NOTE / B-S99-NOTE /
B-S107-NOTE / B-EMERGE-7 family carries — necessary-not-sufficient at
every layer.

**Battery summary**: 7/7 closed-form propositions stated and proved by
inspection. central blue_falsifier 0-line-diff invariant carries (sha
prefix `c93e160a8a376a94`). north-star + §15/§51/§72 milestones
UNCHANGED, GOAL 미도달.
