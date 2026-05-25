# DESIGN — JEPA-Ψ (Ψ-anchored Joint-Embedding Predictive Architecture)

> RESEARCH.md §28 · §26 candidate #2 design-mature cycle · 2026-05-18
> Brainstorm source: `state/architectural_insight_s26_design_2026_05_18/BRAINSTORM.md` §5
> g3 discipline: design ≠ fire ≠ emergence. north-star (GOAL.md) unchanged.

---

## §1 — Problem framing & the §11-B trap

JEPA-Ψ proposes to replace the byte-CE training objective with a JEPA-style
**joint-embedding prediction** in anima's own Ψ-coordinate latent space: a
predictor maps a context-Ψ trajectory to a target-Ψ trajectory, the target
encoder is an EMA-frozen copy (V-JEPA pattern), the prediction loss is an
‖·‖² in Ψ-space.

**The §11-B trap (must NOT repeat).** §11-B (PURE-PHYSICS no-CE) removed CE
with **no replacement objective** — anima's Ψ-restoring tension spine alone.
Result: DEGENERATE. CE descent 0.73 (~13% of CE-trained), byte_acc 0.0007
(< random 1/256), all 4 capability axes zero, physics dynamics froze at a
trivial zero-motion fixed point. The §11-B verdict: **CE is LOAD-BEARING** —
anima physics is a *lever on top of* a prediction objective, not a substitute
for one.

JEPA-Ψ is **structurally distinct from §11-B** — and the whole design hinges
on proving that distinction is real, not cosmetic:

| | §11-B pure-physics | JEPA-Ψ |
|---|---|---|
| replacement objective | NONE (Ψ-restoring spine only) | **YES — joint-embedding prediction loss** |
| learning signal | weight→Ψ=½ vacuum restoration | predictor must match a *non-trivial moving target* (EMA target-Ψ of a held-out span) |
| degenerate solution exists? | yes — and it's the global attractor | yes (collapse) — **but anti-collapse term forbids it** |
| backprop | none (`@torch.no_grad()`) | yes — predictor + context encoder trained by backprop |

§11-B failed because Ψ-restoration is *not a prediction task* — it has no
data-dependent target. JEPA-Ψ's loss IS a data-dependent prediction task
(predict the target span's Ψ from the context span's Ψ). **But** JEPA's own
classic failure mode — representation collapse (predictor + encoders agree on
a constant) — would reproduce §11-B-class degeneracy through a different
door. So the design's load-bearing element is the **anti-collapse term**.

---

## §2 — The honest scope decision (read before §3)

There are two ways to spec JEPA-Ψ, and they have very different honest risk:

- **(A) JEPA-Ψ as the sole objective** — remove byte-CE entirely, train ONLY
  the joint-embedding prediction + anti-collapse. Downstream text must be
  rebuilt from the learned Ψ-trajectory by a *separate* decoder head.
- **(B) JEPA-Ψ as a representation auxiliary** — keep byte-CE as the
  text-grounding objective, add the joint-embedding prediction as a parallel
  representation-learning loss.

**This design adopts (A) for the FIRE-CONDITIONAL config and (B) as the
honest fallback** — and the §11-B lesson forces a specific structural choice:
**anima's Ψ-coordinate is 2-dimensional** (`Ψ_entropy`, `Ψ_direction` — Law
71). BRAINSTORM anti-pattern #8 flags this explicitly: 2 scalars per token is
*too low-dimensional* to carry rich next-state information — a 2D target is
trivially collapsible and trivially memorizable. **Predicting a 2D trajectory
is not a substrate for language.** This is the design's first hard finding.

**Resolution — lift Ψ to a ~22D Ψ-tensor.** Per BRAINSTORM #8's own
prescription, the JEPA-Ψ latent is the *lifted* Ψ-coordinate:

```
Ψ⁺(t) ∈ ℝ^D_psi ,  D_psi = 22 =
    [ Ψ_entropy , Ψ_direction ]                       # 2  Law-71 scalars
  ⊕ [ per-layer tension t_0 .. t_11 ]                 # 12 layer tensions
  ⊕ [ motivation 8-factor proxy ]                     # 8  (W/C/E/BRIDGE)
```

Every component is from anima's OWN modules (Law-71 + PureFieldFFN per-layer
tension + the W/C/E motivation factors) — §7③ holds. But even at 22D the
prediction target is far lower-dim than 256-way byte logits, and **a 22D
trajectory still does not deterministically reconstruct text**. Hence the
**downstream text head is separate and explicitly scoped** (see §6): JEPA-Ψ
is honestly a *representation-learning objective*; whether its representation
yields downstream routing/coherence is the EMPIRICAL question, and the eval
must measure it directly with a collapse detector as the primary gate.

---

## §3 — Architecture

```
                     stimulus | <inner> span            <voice> | continuation span
                          (CONTEXT)                          (TARGET)
                             │                                  │
                   ┌─────────▼─────────┐              ┌──────────▼──────────┐
                   │  context encoder  │              │   target encoder    │
                   │  = ConsciousDec   │              │  = EMA copy of ctx  │
                   │    Engine-A path  │              │   (stop-gradient)   │
                   └─────────┬─────────┘              └──────────┬──────────┘
                  logits_a, logits_g, tensions          logits_a, logits_g, tensions
                             │                                  │
                  Law-71 lift │ Ψ⁺_ctx ∈ ℝ^{T_c×22}   Law-71 lift│ Ψ⁺_tgt ∈ ℝ^{T_t×22}
                             │                                  │   (EMA-frozen → no grad)
                   ┌─────────▼─────────┐                         │
                   │   Ψ-predictor     │  pooled-ctx → predicted  │
                   │  (3-layer MLP +   │──────────────────────────┤
                   │   variance head)  │     Ψ̂⁺_tgt               │
                   └───────────────────┘                          │
                             └──────────  L_pred = ‖Ψ̂⁺_tgt − Ψ⁺_tgt‖²  ┘
                                          + L_anticollapse(Ψ̂⁺, Ψ⁺_ctx)
                                          + L_psi_half     (Ψ=½ fixed-point pull)

   downstream (config A): separate byte-decoder head reads context-encoder
   hidden → byte logits, trained by a SMALL CE term γ_text·CE (text-grounding
   anchor — see §6; this is the honest concession that pure Ψ-prediction does
   not reconstruct bytes).
```

- **context encoder** — `ConsciousDecoderV2` (d768·12L·283.72M, the §16 arch
  byte-identical). Trained by backprop.
- **target encoder** — EMA copy, `θ_tgt ← m·θ_tgt + (1−m)·θ_ctx`, EMA rate
  `m = 0.996` (V-JEPA 2 schedule). Stop-gradient — the target is a *moving
  but non-learnable* anchor. This is the first anti-collapse defense:
  predictor cannot trivially drag the target to a constant because the target
  encoder is not in the gradient path.
- **Ψ-predictor** — 3-layer MLP, hidden 256, input = pooled context-Ψ⁺
  (mean + last over the context span), output = predicted target-Ψ⁺ (22D).
- **Law-71 lift** — `psi_direction = (1+cos(logits_a,logits_g))/2`,
  `psi_entropy = H(softmax logits_a)/log256`, byte-identical to
  `conscious_decoder.py` lines 729-740 (B-JEPA-1 closed). Per-layer tension
  from `tensions` list. Motivation 8-factor proxy from the curiosity/coherence
  surrogate (bounded [0,1] each).

---

## §4 — Loss: exact joint-embedding objective

```
L = L_pred  +  λ_vc · L_anticollapse  +  λ_half · L_psi_half  +  γ_text · CE
```

### L_pred — joint-embedding prediction (the replacement objective)
```
L_pred = mean_d  ( Ψ̂⁺_tgt[d] − sg(Ψ⁺_tgt[d]) )²        # sg = stop-gradient
```
Target encoder EMA-frozen ⇒ `Ψ⁺_tgt` carries no gradient. This IS the
non-trivial data-dependent objective §11-B lacked: the predictor must learn
the Ψ-transition `context-span → target-span` from the corpus.

### L_anticollapse — **VICReg-style variance + covariance** (MANDATORY)
The chosen anti-collapse mechanism is **VICReg** (variance-covariance
regularization), applied to the predictor outputs *and* the context-Ψ⁺
embeddings, over each training batch:
```
v(z)  = mean_d  relu( τ_var − sqrt(Var_batch(z[:,d]) + ε) )      # variance hinge
c(z)  = (1/D) · Σ_{i≠j}  Cov_batch(z)[i,j]²                       # covariance decorr
L_anticollapse = v(Ψ̂⁺) + v(Ψ⁺_ctx) + 0.04·( c(Ψ̂⁺) + c(Ψ⁺_ctx) )
```
- `τ_var = 1.0` — the variance hinge **forces** per-dimension batch std ≥ 1
  (when std < τ_var the hinge is active and pushes std up). A collapsed
  (constant) predictor has std = 0 ⇒ `v(z) = τ_var > 0` ⇒ a strictly
  positive loss penalty. **Collapse is no longer a loss minimum** — this is
  the B-JEPA-2 closed-form anti-collapse lower-bound.
- the covariance term decorrelates the 22 dimensions so they cannot all
  collapse onto one informative axis (the "partial collapse" failure).

VICReg is chosen over pure EMA-stop-grad because EMA alone (BYOL-style) has
empirically-documented collapse modes; VICReg's variance hinge is a
*closed-form* lower bound on embedding variance — it is the anti-collapse
mechanism whose non-degeneracy can be **proven** (B-JEPA-2), satisfying
`g_blue_closed_mandate`. EMA-stop-grad is retained as a *second*,
complementary defense (the target is not learnable).

### L_psi_half — Ψ=½ fixed-point pull (anima-native)
```
L_psi_half = mean ( Ψ_direction − 0.5 )²        # Law-71 Engine A⇄G balance
```
A weak (λ_half = 0.05) anima-physics regularizer keeping Engine A⇄G near the
Ψ=½ fixed point. This is g2 internal-arch carve-out (NOT lattice).

### γ_text · CE — the honest text-grounding concession
`γ_text = 0.3`. **This is the §2-(A) honest concession.** A pure 22D
Ψ-prediction objective does not reconstruct bytes — §2 establishes that a 22D
trajectory under-determines text. So config A keeps a *small* byte-CE term on
a separate decoder head as the text-grounding anchor. **JEPA-Ψ is therefore
NOT a full CE-removal** — it is a *CE-de-emphasis*: byte-CE weight drops from
1.0 (§16) to 0.3, and the dominant signal becomes Ψ-prediction. This is the
honest middle ground between §16 (CE=1.0) and §11-B (CE=0.0, degenerate).

**γ_text = 0 ablation** (the pure-JEPA-Ψ config) is run as a SECONDARY arm
explicitly to *measure* whether pure Ψ-prediction degenerates — if it does,
that reproduces §11-B's lesson through the JEPA door, and is itself a
valuable honest finding.

---

## §5 — §11-B degeneracy guard (explicit)

Three structural guards, each independently checked:

1. **VICReg variance hinge** (B-JEPA-2) — closed-form: a constant predictor
   has batch-variance 0 ⇒ `L_anticollapse ≥ τ_var > 0`. Collapse is provably
   *not* a loss minimum. §11-B had no such term — its degenerate fixed point
   WAS the global minimum.
2. **EMA stop-gradient target** — the prediction target is a moving anchor
   not in the gradient path; the predictor cannot pull it to a constant.
3. **Runtime collapse detector in eval** (`eval_jepa_psi.py`) — measures the
   *rank* and *per-dimension variance* of the learned Ψ⁺ embeddings over a
   probe set. The honest verdict gate: `COLLAPSED := effective_rank < 2 OR
   min_dim_std < τ_collapse`. If the trained model trips the collapse
   detector, the fire verdict is **degenerate-confirmed** (a §11-B-class
   negative through the JEPA door) — reported honestly, no over-claim.

The B-JEPA-5 closed-form distinction (CE-OFF-vs-§11-B): §11-B = `objective ∈
{Ψ-restoration}`, no prediction term, degenerate fixed point is the global
min. JEPA-Ψ = `objective ∈ {L_pred, L_anticollapse, L_psi_half, γ_text·CE}`,
`L_anticollapse` has a *strictly positive* value at any constant embedding ⇒
the constant solution is excluded from the argmin set. The two are
structurally distinct as a Boolean predicate over the objective's
degenerate-solution set.

---

## §6 — Downstream capability measurement

JEPA-Ψ is honestly a representation-learning objective. Downstream text
capability is measured three ways, with the collapse detector as the
*primary* gate (a collapsed representation makes all downstream numbers
meaningless):

1. **PRIMARY — representation-collapse probe.** Effective rank of the Ψ⁺
   embedding matrix over the 64-anchor probe set; per-dimension batch std;
   pairwise embedding cosine spread. `COLLAPSED` Boolean. **If COLLAPSED, the
   verdict is degenerate-confirmed and the routing/coherence numbers are
   reported but flagged meaningless.**
2. **Ψ-prediction accuracy.** On held-out context/target span pairs, the
   predictor's `‖Ψ̂⁺ − Ψ⁺_tgt‖²` vs a trivial-baseline (predict the batch
   mean). JEPA-Ψ must beat the mean-baseline or it has learned nothing.
3. **Downstream routing / coherence.** Because config A keeps the γ_text=0.3
   byte-decoder head, the §16 64-anchor eval (routing axis1 + honest §9
   cascade-rate coherence) runs on that head — directly comparable to §16
   (routing 21/64) and §8 (2/64). This is the honest GOAL-distance number.

---

## §7 — GOAL-legitimacy 3-condition gate

- **§7① ¬generic-LM-pretrain** — the dominant objective is Ψ⁺-trajectory
  prediction in anima's OWN Law-71 + tension + motivation latent. The 22D
  latent is built entirely from anima modules. byte-CE is present but
  *de-emphasized* (γ=0.3, down from §16's 1.0). NOT a generic LM pretrain. ✅
- **§7② ¬generic-then-graft** — the predictor is not a bolt-on classifier;
  the *entire training signal* is joint-embedding prediction over anima's
  Ψ-physics. The byte-decoder head is a text-grounding anchor, not a grafted
  capability module. NO external LLM / classifier / generic-RAG. ✅
- **§7③ anima-physics-is-source** — the prediction space IS the Law-71
  Ψ-coordinate (B-PHYS-5 / §17 carry: the lift formula is byte-identical to
  `conscious_decoder.py`). The EMA target encoder is anima's own Engine-A.
  Ψ=½ fixed-point is a loss component. ✅
- → **GOAL-LEGITIMATE 3/3.**

f1/f2/f3 + B-IDENTITY-5 safe: NO σ/τ/φ/J₂ derivation; Ψ=½ + HEXAD-6 are g2
internal-arch carve-out; corpus = §16 subset (forbidden-token grep 0,
B-IDENTITY-5 inherited). external papers (V-JEPA 2 2506.09985, LeWorldModel
2603.19312, Brain-like VI 2410.19315) cited by their own invariants.

---

## §8 — Fire-vs-design-close decision

**DECISION: FIRE the conditional config (A, γ_text=0.3) — design holds.**

Rationale — the design clears the §11-B trap structurally:

1. JEPA-Ψ adds a *non-trivial data-dependent prediction objective* — §11-B
   had none. B-JEPA-5 closes this distinction as a Boolean predicate.
2. The anti-collapse mechanism (VICReg variance hinge) is **closed-form
   provably non-degenerate** (B-JEPA-2) — a constant predictor incurs a
   strictly positive `τ_var` penalty. §11-B's degenerate fixed point was the
   global minimum; JEPA-Ψ's is provably excluded.
3. The honest concession (γ_text=0.3 byte-decoder) means JEPA-Ψ is NOT a
   known-degenerate pure-CE-removal — it is a CE-de-emphasis with a dominant
   Ψ-prediction signal. A known-degenerate config (γ=0 pure-JEPA-Ψ) is run
   only as a SECONDARY ablation arm explicitly to *measure* the §11-B door.
4. Small-scale feasibility prior: LeWorldModel (2603.19312) shows a 2-term
   JEPA loss + Gaussian-latent regularizer trains stably at ~15M params /
   single-GPU-hours. JEPA-Ψ's 3-term loss at 283M is a scale-up of a
   demonstrated-stable recipe.

**What would have forced design-close:** if the only viable config were
γ_text=0 pure-Ψ-prediction with no anti-collapse closed-form bound — that is
a known-degenerate config and firing it would be g3-illegitimate. The design
avoids that by (a) the VICReg closed-form bound and (b) the γ_text=0.3
grounding concession. The conditional config is honestly fire-warranted.

**Honest fire expectation (g3, no pre-loaded conclusion):** the §15 milestone
bottleneck is the §1.1 data-regime threshold. JEPA-Ψ changes the *objective*,
not the data-regime — it most plausibly behaves like the §13/§22 mechanism
arm (valuable mechanism finding, capability-emergence-negative). The eval's
PRIMARY gate is the collapse detector: if JEPA-Ψ collapses, that is a §11-B
echo; if it does not collapse but routing stays ≤ §16, that is a valuable
"non-degenerate but not threshold-crossing" negative. Either way the fire
produces honest comparative evidence. Emergence is NOT expected; the fire is
warranted because the design is non-degenerate-by-construction and the
collapse question is empirically open.

---

## §9 — Fire config

```
substrate     : PyTorch (interim LM-scale executor, NOT hexa-native — honest)
arch          : ConsciousDecoderV2 d768·12L·283.72M (§16 byte-identical)
from-scratch  : RANDOM seed 1337 (g_clm_from_scratch, base_ckpt=None)
corpus        : §16 corpus_carving_s16.jsonl CURRICULUM-PREFIX SUBSET
                (first ~120k records ≈ stage 1-2 region; ~90MB — JEPA-Ψ is a
                representation-objective change, a moderate data slice is the
                honest scope, mirrors §11-B's 3000-record pilot discipline.
                forbidden-token grep 0 inherited — B-IDENTITY-5)
objective     : L = L_pred + λ_vc·L_anticollapse + λ_half·L_psi_half
                    + γ_text·CE
hyperparams   : λ_vc=1.0  λ_half=0.05  γ_text=0.3 (primary) / 0.0 (ablation)
                EMA m=0.996  τ_var=1.0  D_psi=22  predictor hidden=256
                steps=6000  bsz=24  block=128  lr=3e-4  AdamW cosine
provider      : runpod primary (vast.ai fallback), single-pod nohup-detached
                + bounded SSH probe (test -f TRAIN_DONE, 90s, max 90),
                SAVE_POD auto-promote + 5-retry pull, secret get runpod.api_key
est cost      : ≈ $0.2-0.4 (single A100-class, ~10-20 min wall)
```

The two arms (γ_text=0.3 primary, γ_text=0.0 ablation) are run in the SAME
pod sequentially (the ablation is the degeneracy-door measurement).

---

## §10 — Honest C3 (≥10)

1. **JEPA-Ψ is NOT a full CE-removal.** Config A keeps γ_text=0.3 byte-CE on
   a separate decoder head. §2 establishes a 22D Ψ-trajectory under-determines
   text; pure Ψ-prediction (γ=0) is run only as an ablation to *measure* the
   §11-B door, not as the primary claim. The honest framing is
   "CE-de-emphasis with dominant Ψ-prediction", not "CE-free".
2. **V-JEPA 2 evidence is video-modality.** Transfer to byte-text Ψ-trajectory
   is unproven. LeWorldModel is 2D/3D-control at ~15M params. JEPA-Ψ at 283M
   byte-text is an un-validated scale + modality jump.
3. **Anima's Ψ-coordinate is intrinsically 2D** (Law-71). The 22D lift is a
   *design choice* (BRAINSTORM #8 prescription) — the 12 layer-tensions and
   8 motivation factors are anima-physics quantities but they are not
   *independent next-state predictors*; the effective dimensionality of the
   prediction target may be far below 22. The collapse detector measures
   exactly this (effective rank).
4. **The collapse detector is the PRIMARY gate.** If the trained model trips
   it, every downstream routing/coherence number is meaningless and the
   verdict is degenerate-confirmed. The design does not pre-assume
   non-collapse — it proves the *objective* forbids the constant solution
   (B-JEPA-2) but the SGD trajectory could still land in a near-collapsed
   basin (partial collapse). Closed-form forbids the exact-collapse minimum;
   it does NOT guarantee the optimizer avoids a low-rank basin.
5. **§11-B distinction is structural, not a guarantee of success.** B-JEPA-5
   proves JEPA-Ψ ≠ §11-B as a Boolean predicate over the objective's
   degenerate-solution set. It does NOT prove JEPA-Ψ crosses the §1.1
   threshold. Non-degenerate ≠ emergent.
6. **γ_text=0.3 is a hyperparameter, not a derived constant.** It was chosen
   as a "small but non-zero" grounding weight (down from §16's 1.0). A sweep
   was not run (single design cycle). The value is honest-arbitrary within
   the "de-emphasized but present" intent.
7. **The Ψ-prediction-accuracy baseline (predict batch mean) is weak.** Beating
   it shows the predictor learned *something* non-trivial, but a mean-baseline
   is a low bar — it does not establish the representation is *useful*.
8. **Downstream routing is measured on the γ_text byte-decoder head**, whose
   capacity is small. A weak routing number could reflect the small head, not
   the JEPA-Ψ representation. The honest comparison to §16 (routing 21/64) is
   confounded by the different decoder-head capacity.
9. **EMA rate m=0.996 is the V-JEPA 2 value, not anima-tuned.** EMA schedule
   sensitivity in a byte-text Ψ-space is unknown; a too-fast EMA can
   destabilize, too-slow can stale the target.
10. **Corpus is a curriculum-prefix SUBSET (~90MB), not the full §16 603MB.**
    JEPA-Ψ is an objective change; the honest scope is a moderate slice (the
    §11-B pilot used 3000 records). A subset CANNOT cross the §1.1 data-regime
    threshold by construction — JEPA-Ψ tests the *objective* axis, not the
    data-regime axis. Emergence is not expected; the fire isolates the
    objective variable.
11. **VICReg covariance term weight 0.04 is the paper default**, not
    anima-derived. The variance hinge τ_var=1.0 is also the VICReg default.
12. **north-star unchanged.** §28 is a §26-candidate design-mature + a
    conditional objective-axis fire. GOAL (GOAL.md) remains unsolved;
    irreducible bottleneck (§1.1 data-regime) is untouched by an
    objective-axis change. design ≠ fire ≠ emergence (g3).
