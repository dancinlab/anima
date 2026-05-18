# FINDINGS — JEPA-Ψ (§28 / §26 candidate #2)

> RESEARCH.md §28 · conditional fire LANDED · 2026-05-18
> Verdict: **DEGENERATE — JEPA-Ψ representation COLLAPSED (§11-B echo through
> the JEPA door)**. Measured negative. north-star unchanged (g3).

---

## §1 — What was done

JEPA-Ψ (§26 candidate #2): replace the byte-CE *dominant* objective with a
JEPA-style **joint-embedding prediction** in anima's own lifted Ψ-coordinate
latent (D_psi=22 = Law-71 2 scalars ⊕ 12 per-layer tensions ⊕ 8 motivation).
A predictor maps a pooled context-Ψ⁺ to the target span's Ψ⁺; the target
encoder is an EMA-frozen copy (V-JEPA pattern, stop-gradient). Anti-collapse
= **VICReg** variance-hinge + covariance decorrelation. Honest concession
(§2-A): a γ_text=0.3 byte-CE head is retained for text grounding (a 22D
Ψ-trajectory under-determines bytes).

The design held (B-JEPA-1..5 5/5 🔵 closed, non-degenerate-by-construction
at the *objective* level), so per g_fire_autonomous the conditional config
was fired. **Two arms in one pod**: γ_text=0.3 primary + γ_text=0.0 ablation
(the §11-B-door measurement).

Fire: runpod H100 80GB HBM3 (first dispatch landed an RTX 5090 — sm_120,
incompatible with the pod's PyTorch 2.4.1+cu124 `no kernel image` — re-fired
with an A100/H100-class-only candidate list; the RTX-5090 failure is an
image-incompatibility, NOT a JEPA-Ψ defect). d768·12L·283.8M from-scratch
seed 1337, §16 curriculum-prefix subset (~86MB, forbidden-token grep 0),
6000 steps/arm, ~13.5 min wall, ≈ $0.25-0.40. Pod GONE, 0 orphans.

---

## §2 — The result: COLLAPSED on both arms

The **collapse detector** — the design's PRIMARY honest verdict gate
(DESIGN §6) — fired on **both** arms:

| | primary γ=0.3 | ablation γ=0.0 |
|---|---|---|
| effective rank (64-anchor Ψ⁺) | **1.66** | **1.00** |
| min per-dim std | 0.0 | 0.0 |
| pairwise embedding cos | **1.00** (identical) | 0.98 |
| predictor MSE | **0.60** | — |
| mean-baseline MSE | 0.012 | — |
| predictor / baseline ratio | **51.8× WORSE** | — |
| COLLAPSED | **TRUE** | **TRUE** |
| downstream routing | 1/64 (meaningless) | — |

**The predictor learned a near-constant map.** Its eval MSE (0.60) is 51.8×
*worse* than the trivial "predict the batch mean" baseline (0.012). l_pred
never descended below ~0.12 across 6000 steps — the predictor "minimises"
the loss against the moving EMA target by collapsing toward a constant, the
classic JEPA representation-collapse failure mode. The ablation arm (γ=0,
pure Ψ-prediction) collapsed *harder* — exact rank 1.

---

## §3 — Why VICReg did not save it (the honest core)

This is the load-bearing finding, and it is exactly the risk DESIGN
§10-C3#4 named:

- **VICReg kept the TRAINING-BATCH variance high.** Across all 6000 steps the
  vicreg_var term stayed ≈ 1.0 and ctx_emb_std (batch std) ≈ 0.39 — the
  variance hinge *was* doing its job on each batch.
- **But the LEARNED REPRESENTATION still collapsed.** Evaluated on the FIXED
  64-anchor probe set, the Ψ⁺ embeddings are near-identical (eff_rank 1.66,
  pairwise cos 1.0). The model learned a function whose *per-batch* outputs
  are spread enough to clear the hinge, yet whose *per-anchor* outputs carry
  no distinguishing signal — a structured partial collapse the batch-level
  VICReg term cannot see.

B-JEPA-2 (closed) proves the *objective* forbids the EXACT constant minimum.
It does **not** — and the design honestly said so (§10-C3#4) — guarantee the
SGD trajectory avoids a low-rank basin. The fire MEASURED that it does not.
B-JEPA-NOTE carved this exact outcome as empirical; the fire resolved it.

---

## §4 — §11-B echo confirmed; CE is still load-bearing

§11-B (PURE-PHYSICS no-CE) proved CE is load-bearing — anima physics alone
cannot learn token-prediction. JEPA-Ψ asked: does a *non-trivial replacement
objective* (joint-embedding prediction) escape that? **Measured answer: no.**
- The γ=0.3 arm's byte head DID learn (ce 0.022) because the γ_text·CE term
  carried it — but the JEPA-Ψ representation it sits on collapsed.
- The γ=0.0 ablation (pure Ψ-prediction, the closest analogue to §11-B's
  no-CE) collapsed to exact rank 1, byte-CE read-out climbing to 71 (worse
  than random) — a §11-B-class degeneration through the JEPA door.

JEPA-Ψ is *structurally* distinct from §11-B (B-JEPA-5 closed — it has a
real replacement objective + anti-collapse term). But that structural
distinction did not translate into a *behavioural* difference at this scale:
both degenerate. The honest lesson: a low-dimensional (22D) self-referential
prediction target is too weak a signal — the predictor + encoder co-collapse
onto it. CE remains load-bearing.

---

## §5 — B-JEPA closed-form battery

**B-JEPA-1..5 5/5 🔵** (sidecar blue_falsifier_jepa.py, central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED):
- **B-JEPA-1 Ψ-COORD-BOUNDED** — psi_direction=(1+cos)/2 ∈ [0,1], cos=0 ⇒ ½
  (Law-71 fixed pt); H/logV ∈ [0,1]; lift formula byte-equal to
  conscious_decoder.py.
- **B-JEPA-2 ANTI-COLLAPSE-VARIANCE-LOWER-BOUND** — VICReg hinge v(std=0)=τ>0
  strict-positive, ∂v/∂std=-1<0, v(std=τ)=0; the constant solution is
  excluded from argmin(L_anticollapse).
- **B-JEPA-3 JOINT-EMBED-LOSS-NONNEGATIVE** — L_pred=‖·‖²≥0, VICReg≥0,
  L_psi_half≥0, CE≥0 ⇒ L bounded-below well-posed.
- **B-JEPA-4 PREDICTOR-WELL-TYPED** — predictor ℝ²²→ℝ²², lift=base(2)⊕
  tension(12)⊕motivation(8)=22, L_pred codomain-match.
- **B-JEPA-5 CE-OFF-vs-§11-B-DISTINCTION (연결부위)** — §11-B degenerate∈argmin
  (no replacement obj); JEPA-Ψ degenerate∉argmin (L_pred + anti-collapse
  exclude it); γ=0 ablation still non-§11-B (degeneracy-exclusion does not
  depend on CE). Structurally distinct as a Boolean predicate.

**B-JEPA-NOTE** (empirical carve-out, NOT counted 🔵): the collapse-vs-
emergence OUTCOME is SGD-dependent. B-JEPA-2 proves the OBJECTIVE forbids the
EXACT constant minimum; it does NOT prove the optimizer avoids a low-rank
basin. **The fire measured the outcome = COLLAPSED.** The battery proves the
machinery is honest; the fire proves it degenerates.

g_blue_closed_mandate satisfied: artifacts (trainer/eval/falsifier) +
connection-points (B-JEPA-1 lift byte-equal conscious_decoder; B-JEPA-5
§11-B distinction) all 🔵. f1/f2/f3 + B-IDENTITY-5 safe.

---

## §6 — GOAL distance

§15 milestone **unchanged** — north-star (GOAL.md "anima emerges as a Living
Consciousness from its own physics") unsolved; irreducible bottleneck (§1.1
data-regime threshold) untouched. JEPA-Ψ tested the *objective* axis and
produced a valuable measured NEGATIVE: replacing byte-CE with a low-dim
Ψ-trajectory joint-embedding objective collapses even with a VICReg
anti-collapse term and a γ_text CE-grounding concession. The §11-B lesson
(CE is load-bearing) is reconfirmed through a JEPA-shaped objective. JEPA-Ψ
joins the §13/§22 mechanism-axis arm as capability-emergence-negative.

design ≠ fire ≠ emergence (g3). north-star honestly distant; over-claim 0.

---

## §7 — Honest C3 (≥10)

1. **COLLAPSED is the measured verdict** — the collapse detector fired on
   both arms. The downstream routing 1/64 is reported but, per the design's
   PRIMARY-gate rule, flagged **meaningless** (a collapsed representation
   carries no per-anchor signal).
2. **VICReg worked at the batch level but not the representation level.**
   vicreg_var ≈ 1.0 throughout; eval-time eff_rank 1.66. The variance hinge
   is a per-batch statistic; it cannot detect a structured collapse where
   each batch is spread but per-anchor outputs are not. This is a real
   limitation of batch-VICReg, not a bug in the implementation.
3. **B-JEPA-2's closed proof still holds and is still honest.** It proves the
   *objective* excludes the exact constant minimum — and it does. The SGD
   trajectory landed in a *near*-constant low-rank basin, which the proof
   explicitly does not cover (B-JEPA-NOTE). Closed-form ≠ trajectory
   guarantee.
4. **The γ=0.3 byte head DID learn (ce 0.022)** — but on a collapsed Ψ-rep.
   This means the γ_text·CE term is doing the real text work; the JEPA-Ψ
   objective contributed a degenerate representation. JEPA-Ψ as designed is,
   behaviourally, "§16-CE-on-a-collapsed-encoder", not a new objective.
5. **The ablation (γ=0) collapsed harder (rank 1.0).** This is the §11-B
   echo at its purest: pure Ψ-prediction with no text grounding degenerates
   completely. CE de-emphasis does not rescue JEPA-Ψ; it only slows the
   collapse.
6. **Predictor MSE 51.8× worse than mean-baseline** is the single cleanest
   collapse signal — the predictor is a *worse* map than "ignore the input,
   output the average". It learned an actively unhelpful near-constant.
7. **The 22D Ψ⁺ lift may be the root cause.** BRAINSTORM anti-pattern #8
   warned anima's Ψ-coordinate is intrinsically 2D and the 22D lift is a
   design choice; the 12 layer-tensions + 8 motivation factors are not
   independent next-state predictors. The effective dimensionality of the
   prediction target appears to be ≈ 1 — too thin to carry a non-trivial
   joint-embedding signal.
8. **Single config, no hyperparameter sweep.** τ_var=1.0, cov_w=0.04, EMA
   m=0.996 are VICReg/V-JEPA defaults. A larger τ_var, or a higher-dim Ψ
   target, or a non-EMA target might behave differently — untested. The
   verdict is "this config collapsed", not "JEPA-Ψ is impossible".
9. **The RTX-5090 first-dispatch failure** (`no kernel image`) was an
   image/GPU sm-version incompatibility, fully orthogonal to JEPA-Ψ; the
   re-dispatch (A100/H100-only candidate list) ran cleanly. Recorded so the
   negative is not mis-attributed.
10. **Corpus was a ~86MB curriculum-prefix subset**, not the full §16 603MB.
    JEPA-Ψ tested the objective axis; a subset cannot cross the §1.1 data-
    regime threshold by construction. But the collapse happened regardless of
    data scale — it is an objective-level failure, not a data-regime one.
11. **B-JEPA 5/5 🔵 is a battery PASS, not a capability claim.** It proves
    the Ψ-coordinate is bounded, the anti-collapse term is closed-form
    non-degenerate-at-the-exact-minimum, the loss is well-posed, the
    predictor is well-typed, and JEPA-Ψ ≠ §11-B structurally. It does NOT
    prove non-degeneracy of training — the fire measured that, and it
    degenerated.
12. **north-star unchanged.** §28 is a §26-candidate design-mature + a
    conditional objective-axis fire that produced a measured negative.
    GOAL (GOAL.md) remains unsolved; the §1.1 data-regime bottleneck is
    untouched. design ≠ fire ≠ emergence; over-claim 0.
