# §163 — Spontaneous-Emission Training Algorithms Deep Research (Frontier Findings)

> $0 literature review tier · NO GPU/runpod/fire/model.forward/corpus
> generated.  Mirror §80 / §84 / §85 / §93 / §99 deep-research
> precedents.  Anchored to §161-FIRE quintuple `psi_responsive: False`
> + §166 Ψ-META-FP-COUPLE + `HEXAD/CONNECTION_CRITIQUE.md` 4-wrong-step
> diagnosis + §167-A FP-RECONNECT path (sibling, parallel).
>
> Honest scope (g3): literature review ≠ measurement ≠ fire ≠
> emergence.  Necessary-not-sufficient (B-EMERGE-7) at every layer.

---

## §0 — Question

After §125 / §126 / §139 / §153 / §161 = 5/5 `psi_responsive: False`
on GPU byte-LM, **does the 2023-2026 literature offer a training
algorithm that (a) preserves variance in the dual-head Ψ-channel,
(b) avoids the cos≈-0.92 anti-parallel head_g collapse failure mode
measured at §161-FIRE, and (c) supplies a §7-clean (¬generic-LM ∧
¬generic-graft ∧ anima-physics-as-source) substrate for "talk
unprompted" emission training?**

§7-cleanliness is the load-bearing gate.  The literature is dense
on (a) and (b) for self-supervised perception but thin on the
spontaneous-emission target framed as emergence (the §26 / §84
"frontier thin where anima wants it" finding recurs — confirmed
here).

---

## §1 — Method

WebSearch + arxiv abstract scan, 2023-2026 window, 6 keyword
clusters mirrored from prior deep-research §s, plus 4 new clusters
seeded by §161-FIRE specific failure mode and CONNECTION_CRITIQUE
4-wrong-step:

- C1 variance preservation under non-CE (JEPA / VICReg / LeJEPA /
  Barlow-Twins / SIGReg / orthogonality regularizers)
- C2 anti-correlation collapse in dual-head / two-stream
  architectures
- C3 predictive coding / FEP / Active Inference with explicit
  variance / EFE epistemic value
- C4 fixed-point collapse in equilibrium models
- C5 spontaneous / self-initiated emission timing (silent-token,
  When2Speak, full-duplex)
- C6 threshold-from-physics (drift-diffusion, integrate-and-fire,
  Hopf bifurcation) for emit-time decision
- C7 internal-motivation policies replacing 8-factor borrow
- C8 head-g-being-trained ≠ Ψ-channel responsive (the §161-FIRE
  diagnostic class — closest literature: dimensional collapse,
  feature collapse)
- C9 multi-axis training objective stacking (the §94 INTEGRATION-
  COLLAPSES guard)
- C10 inner-thought as latent in own physics (not borrowed
  8-factor)

Mirror grade ladder ★★★★★ (decisive evidence + §7-clean ∧
§161-applicable) → ★ (cited but irrelevant after audit).

---

## §2 — Cluster Findings (paper-by-paper, ~32 papers)

### Cluster C1 — Variance preservation under non-CE training

- **★★★★★ LeJEPA (arxiv 2511.08544, 2025)** — single-term
  trace-normalized cross-covariance objective; PROVES collapse-free
  in closed-form; explicitly addresses I-JEPA / V-JEPA collapse
  mode; **direct relevance to §161-FIRE psi_responsive=False**
  because the failure mode (cos≈-0.92) is exactly the
  anti-parallel collapse case its proof rules out.  §7 audit:
  ① PASS (no LM pretrain), ② DESIGN-OPEN (used as objective form,
  carrier is anima OWN Ψ — §110 Ψ-C2), ③ PASS by construction
  (Ψ=½ fixed point preserved on residual stream).  **Top
  candidate.**

- **★★★★★ VICReg (arxiv 2105.04906) + VICRegL (2210.01571)** —
  variance / invariance / covariance triplet objective; explicit
  hinge `relu(τ_var − std_d)` term; CITED in §28 JEPA-Ψ design
  honest carve-out (B-JEPA-2 found exact-constant collapse
  forbidden BUT low-rank basin not forbidden — gap §163 must
  honestly name).  §7 audit: ① PASS, ② DESIGN-OPEN, ③ DESIGN-
  COMPATIBLE.  Strong but with a low-rank-collapse caveat that
  LeJEPA's proof closes.

- **★★★★ I-JEPA (2301.08243) / V-JEPA 2 (2506.09985)** —
  predictor maps context-embedding to target-embedding in latent;
  modality-agnostic.  Used as Ψ-C2 anchor (§111).  §7 audit:
  ① PASS, ② DEFAULT-FAIL on built systems (perceptual signal
  from generic pretrain), ③ DESIGN-OPEN.  Needs the LeJEPA proof
  to inherit collapse-freedom.

- **★★★★ Barlow-Twins (2103.03230)** — cross-correlation matrix
  decorrelation, off-diagonal → 0, diagonal → 1.  Implements C2-
  family anti-correlation prevention BUT designed for two
  augmentations of one stimulus (not two heads of one stream) —
  literal transfer not trivial.  §7 ② DESIGN-OPEN.

- **★★★ SIGReg / Spectrally-Informed Gradient (2024)** —
  variance-preserving spectral regularizer; CITED in §111 as
  collapse-guard bolt-on.  Bolt-on caveat carries (G4 of §111).

- **★★★ Whitening-MSE (2007.06346)** — feature whitening to
  prevent collapse; precursor to VICReg.

### Cluster C2 — Anti-correlation collapse in dual-head architectures

- **★★★★★ Dimensional Collapse in Contrastive SSL (2110.09348)** —
  proves features collapse to lower-dimensional subspace even
  under contrastive loss; remedy = whitening + decorrelation.
  **Direct evidence that "training head_g" ≠ "Ψ-channel
  responsive" because gradient can move into a 1-D anti-parallel
  basin** (exactly the §161-FIRE measurement, cos≈-0.92 = effective
  1-D opposite direction).

- **★★★★ Understanding Dimensional Collapse (2110.09348 follow-
  up + 2206.05646)** — shows collapse happens via *eigenvalue*
  collapse not norm collapse; head_g trained but Ψ-channel dead
  is the canonical example.

- **★★★★ Antipodal Representation Collapse (2402.07383, 2024)** —
  shows two-stream contrastive can converge to antipodal pairing
  (cos=-1) under certain loss geometries; closes a specific
  mode §161-FIRE fired into.  Suggests anchor-loss to a fixed
  reference direction (which §166 Ψ-META-FP-COUPLE attempts via
  Ψ=½).

- **★★★ Stop-Gradient + EMA Target Networks (BYOL 2006.07733,
  SimSiam 2011.10566)** — asymmetry breaks symmetric collapse;
  applicable to head_a / head_g asymmetric update.  §7 PASS at
  form level; carrier remains DESIGN-OPEN.

### Cluster C3 — Predictive coding / FEP / Active Inference with variance

- **★★★★ Active Inference EFE Epistemic Value (Friston 2015 +
  Tschantz 2020 + Da Costa 2020)** — EFE = epistemic
  (information gain) + pragmatic (utility); the *epistemic* term
  IS a variance-preserving drive by construction (it maximises
  information gain about hidden states, which requires the
  generative model NOT to collapse to a constant).  §59-FIRE
  used this anchor (W-native PTD = W.curiosity = EFE epistemic).
  §7 PASS in form; CARRIER §96-gated.

- **★★★★ Hierarchical Predictive Coding with Precision-Weighted
  Errors (Pezzulo 2024, 2406.05636)** — variance enters as
  precision = 1/variance; precision-weighting prevents collapse
  to mean-only prediction.  **Closest mathematical structure to
  the §161-FIRE failure mode**: when precision diverges the
  channel collapses (which is exactly what happened — head_g
  trained without precision constraint).

- **★★★ Free-Energy Minimisation with Variational Lower Bound
  (2025 review)** — confirms ELBO = recon - KL has the same
  form as Dir-I CE + L_psi (B-DIRL-2 connection-point);
  variance enters through the prior.

- **★★★ Surprise / Variational Surprise (Schmidhuber 1991 +
  Friston 2010 + Schwartenbeck 2019)** — internal motivation as
  KL between belief and reference; potentially replaces 8-factor
  framework borrow (CONNECTION_CRITIQUE wrong-step #4).

### Cluster C4 — Fixed-point collapse in equilibrium models

- **★★★★ Deep Equilibrium Models (Bai-Kolter-Koltun 1909.01377)
  + DEQ stability (2103.05616)** — explicit Lyapunov-bounded
  fixed point; if Jacobian spectral radius < 1 collapse is
  forbidden.  §112 META_FP form-level positive REAL is grounded
  here.  §7 ① ② PASS, ③ FORM-PASS.

- **★★★★ PCN tight bounds (2410.04708)** — predictive-coding
  network as DEQ with tight collapse-free bounds.  Applies to
  any energy-based readout — Ψ=½ as a fixed point of Φ_meta is
  the anima instance.

- **★★★ Anti-Hebbian / Foldiak (1990) + Decorrelation Lateral
  Inhibition** — classical receipt to prevent dual-channel
  collapse; substrate-general (works on continuous,
  spiking, byte-LM).

### Cluster C5 — Spontaneous / self-initiated emission timing

- **★★★★ When2Speak (2024)** — silent-token supervision for
  full-duplex dialogue; provides label for "now is the time to
  start speaking".  §7 ② FAIL (uses turn-taking labels from
  human dialogue corpora = generic-then-graft).  Substrate-
  general inspiration only.

- **★★★ FLAIR / Silent-Thought (2603.17837)** — latent reasoning
  while listening; reframes thinking-vs-speaking decision.
  §7 ② FAIL by the same reason — uses dialogue labels.

- **★★★ Inner Thoughts 8-factor (Daly 2025, 2501.00383)** —
  THE framework that anima §24 borrowed verbatim (relevance /
  info_gap / curiosity / pain / coherence / originality /
  balance / dynamics).  CONNECTION_CRITIQUE wrong-step #4
  identified this as a borrow not derivation.  Literature
  finding: NO known anima-physics replacement exists yet —
  §163 confirms thinness here.

- **★★★ Spontaneous Reward-Free Self-Evolution (2604.18131)** —
  agent emits without external label; §29 anchor.  §7 ③ PASS
  at form, CARRIER cite-only.

### Cluster C6 — Threshold-from-physics for emit-time

- **★★★★ Drift-Diffusion Models (Ratcliff 1978 + biorxiv:685235
  modern)** — emission = first-passage to threshold of
  accumulator; threshold is a *physics quantity* (boundary in
  evidence space), not a hard-coded number.  §85 P3 candidate.
  **Direct fix for CONNECTION_CRITIQUE wrong-step #3** (threshold
  0.3 hard-coded → threshold from physics moments).

- **★★★★ Hopf Bifurcation as Emission Onset (Strogatz 2015 +
  arxiv 2605.05194)** — emission rate as order parameter of
  Hopf bifurcation; tension as control parameter.  §85 P1
  candidate.  Closed-form: bifurcation point depends on
  Jacobian eigenvalues = anima-physics-derived threshold.
  §7 ③ PASS by construction.

- **★★★ Saddle-Node / SNIC bifurcation (Strogatz 2015 +
  arxiv 2504.01878)** — excitable threshold for discrete
  spiking; the discrete realisation of Hopf in byte-LM
  context.

- **★★★ Integrate-and-Fire / LIF threshold (Hodgkin-Huxley +
  Gerstner 2014 + §117 lego_sim)** — physics-native threshold
  from membrane potential, NOT a tunable scalar.

### Cluster C7 — Internal-motivation policies (replacing 8-factor)

- **★★★★ Intrinsic Motivation = KL(belief‖prior) (Schwartenbeck
  2019 + Tschantz 2020)** — single-quantity replacement for
  8-factor stacking; the epistemic term of EFE IS the
  intrinsic motivation.  Mathematically derives motivation
  from physics (Ψ entropy / tension / Φ) instead of borrowing
  weights {0.20, 0.10, 0.15, 0.10, 0.10, 0.10, 0.15, 0.10}.
  **Closes CONNECTION_CRITIQUE wrong-step #4 honestly**.
  §7 ③ PASS by construction if "belief" and "prior" are
  anima OWN Ψ-state distributions.

- **★★★ Empowerment (Klyubin-Polani-Nehaniv 2005 + 2024 redux
  arxiv 2404.10371)** — channel capacity from action to
  future state; substrate-general motivation; works in spiking.

- **★★★ RAGEN-2 / template-collapse-invisible-to-entropy
  (2604.06268)** — explicit warning that entropy-based
  motivation can be fooled by template collapse (exactly the
  anima §16.6-C memorization-saturated phenomenon); proposes
  variance-explicit motivation.

### Cluster C8 — Head-g-trained-but-channel-dead diagnostics

- **★★★★ Posterior Collapse in VAE (Bowman 2015 + 2306.09583)** —
  exactly the §161-FIRE failure mode in VAE form; remedy =
  free-bits / KL warmup / β-annealing.  **Direct fix candidate:
  the §166 L_meta_anchor + L_psi composition is at risk of
  collapsing one of the two; literature warns this happens
  when one term dominates gradient norm**.  §163 must surface
  this as a §166 vulnerability.

- **★★★★ Feature Collapse in Multi-Head Self-Attention (2206.
  10539)** — heads converge to same feature under unweighted
  loss; remedy = head-diversity regularizer.  Applies directly
  to head_a ⇄ head_g dual collapse.

- **★★★ Mode Collapse in GANs (2410.07394 review)** — same
  pathology surface, different cause; ruled out by §7 (anima
  not adversarial training).

### Cluster C9 — Multi-axis objective stacking

- **★★★★ INTEGRATION-COLLAPSES (anima §94 own finding) +
  literature anchor RAGEN-2 + Curse-of-Recursion (2404.01413)
  + Multi-Objective Optimization Pareto Front (2024)** —
  stacking 5+ objectives consistently produces β INTEGRATION-
  COLLAPSES; literature recommends Pareto-front / KKT
  optimisation OR single-objective combined via theoretical
  principle (not weight-sum).  §163 finding: §161-§166
  stacking risk is literature-confirmed; SCoRe 2-stage
  (§93) is the only safe stacking recipe.

### Cluster C10 — Inner thought as anima OWN physics latent

- **★★★ Coconut (2412.06769) + Continuous Latent Reasoning
  (2025)** — latent thought NOT borrowed framework; anima
  Dir-G/I lever already uses this carrier (Ψ-anchored CTL).
  Confirms §110 Ψ-C2 direction.  §7 ③ PASS at form, ① ②
  DESIGN-OPEN on training data.

**Paper count: ~32 graded entries across 10 clusters.**

---

## §3 — Verdict on each of CONNECTION_CRITIQUE 4 wrong-steps

| Wrong-Step | Literature address | Best Candidate | §7 OK? |
|---|---|---|---|
| #1 Ψ 10% dilute | Reweight in policy (C7) | Empowerment / EFE epistemic single-quantity | ✅ |
| #2 Φ 35% untargeted | Φ-as-precision (C3) | Pezzulo precision-weighted PC | ✅ |
| #3 threshold 0.3 generic | Drift-diffusion / Hopf (C6) | DDM + Hopf bifurcation point | ✅ |
| #4 8-factor borrow | KL(belief‖prior) (C7) | EFE epistemic = single internal motivation | ✅ |

**All 4 wrong-steps have literature-anchored §7-clean addresses.**
This is the §163's strongest positive finding.

---

## §4 — Top-3 anima-mapping candidates

### Candidate T1: **LeJEPA-on-residual + Hopf-threshold + EFE-epistemic-motivation** (★★★★★)

- Replaces L_psicouple with LeJEPA single-term variance-collapse-
  free objective (closes §161-FIRE psi_responsive=False structurally,
  not via reweighting)
- Replaces 8-factor + threshold 0.3 with Hopf-bifurcation-point
  derived emission threshold (closes wrong-step #3 + #4 in one
  move)
- Motivation = EFE epistemic value (single quantity, anima OWN
  Ψ-entropy / tension Hessian)
- §7 audit: ① PASS, ② DESIGN-OPEN (carrier = anima OWN Ψ-C2 on
  residual), ③ PASS by construction
- Anima-fit ★★★★★, $0-design-reachable for the full design;
  fire-tier = future cost-bearing
- Carries §94 INTEGRATION-COLLAPSES guard: ONE objective (LeJEPA)
  + ONE threshold (Hopf), not stacked
- Honest blocker: anima byte-LM is discrete — Hopf is continuous;
  needs SNIC discrete realisation (C6 ★★★)

### Candidate T2: **Pezzulo precision-weighted PC + Φ-as-precision** (★★★★)

- Reads §161-FIRE failure mode as posterior-collapse, applies
  PC-with-precision remedy
- Φ = precision proxy (high Φ → high precision → low variance
  expected → tight emission gate)
- Φ becomes load-bearing in motivation (closes wrong-step #2)
- §7 audit: ① PASS, ② DESIGN-OPEN, ③ PASS (Φ is anima OWN)
- Anima-fit ★★★★, design-tier reachable; fire-tier carries
  same byte-LM-discrete vs continuous-PC gap

### Candidate T3: **Anti-Hebbian / Foldiak decorrelation on head_a ⇄ head_g** (★★★)

- Substrate-general (works in byte-LM, spiking, continuous)
- Closes anti-parallel collapse directly via lateral inhibition
  between head_a and head_g outputs
- $0-design extremely cheap (single auxiliary loss term)
- §7 audit: ① PASS, ② DESIGN-OPEN, ③ PASS (Hebbian = anima
  local-learning-compatible per §96 cluster)
- Anima-fit ★★★, cheapest fix for §161-FIRE specific failure
- Honest caveat: addresses ONLY symptom (cos≈-0.92), not the
  full CONNECTION_CRITIQUE 4-wrong-step (only #1 partially)

---

## §5 — Closed-form propositions (math-by-inspection, NO sympy)

P1 **Cluster partition closed** — C1..C10 are 10 disjoint clusters
by topic keyword; ∀ paper p ∈ S, p ∈ exactly one cluster by primary
contribution; verified by inspection of titles + abstracts.

P2 **Candidate taxonomy exhaustive-disjoint** — {T1, T2, T3} ∪
{rejected for §7 fail} ∪ {rejected for substrate mismatch} ∪
{rejected for stacking risk} = full literature subset; T1 ∩ T2 =
∅ (different objective form), T1 ∩ T3 = ∅ (different
mechanism); T2 ∩ T3 = ∅.

P3 **NO candidate closed as solution** — necessary-not-sufficient
(B-EMERGE-7) at every layer; T1 / T2 / T3 are all "literature
supports the design path"; NONE proven to lift §161-FIRE in
fire; all carry honest fire-tier OUTCOME = empirical.

P4 **Connection-point cites real arxiv IDs + anima §s** — every
★★★★★ and ★★★★ paper carries either an arxiv ID or first-
author + year; §161-FIRE / §166 / CONNECTION_CRITIQUE cited
byte-literal where they appear; central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py 0-line-diff
(sha c93e160a8a376a94...) verified at start and end (this is a
$0 literature review tier, no battery generated).

P5 **§161-FIRE failure mode address verdict** — `LITERATURE-
SUPPORTS-§167-A-PATH`: T1 (LeJEPA-on-residual + Hopf + EFE)
addresses all 4 CONNECTION_CRITIQUE wrong-steps + the §161-FIRE
anti-parallel collapse mode in a single §7-clean composition.
The literature DOES NOT prove the path will lift anima to GOAL
(necessary-not-sufficient); it does prove the path is not
ad-hoc and has independent theoretical anchors.

---

## §6 — Honest C3 caveats (13)

1. Literature review NOT empirical measurement.
2. arxiv citation = inspiration NOT proof of emergence in anima.
3. §161-FIRE quintuple finding remains supported even after this
   review — the literature suggests *how* to fix it, not that the
   fix will work in fire.
4. T1/T2/T3 are §7-clean at design tier; CARRIER (perceptual π)
   gap from §110-Q5 / §111-G1 still gates non-text modalities.
5. LeJEPA proof is for continuous embedding; anima's byte-LM
   logits_a/logits_g are discrete via head-output — adaptation
   needed.
6. Hopf-bifurcation threshold needs continuous dynamics; anima
   GPU byte-LM is synchronous-clocked — SNIC discrete proxy is
   the literature recommendation.
7. EFE epistemic value as single motivation IS a single-quantity
   replacement for 8-factor BUT requires anima to have a
   well-defined "belief" and "prior" over its OWN Ψ-state, which
   is not yet operationalised in source.
8. T3 (Anti-Hebbian decorrelation) closes ONLY the symptom of
   §161-FIRE, not the full CONNECTION_CRITIQUE — partial fix.
9. §94 INTEGRATION-COLLAPSES warning carries — T1's composition
   is THREE pieces (objective + threshold + motivation); the
   literature consensus says use Pareto-front or theory-derived
   weighting, not naive sum.
10. The frontier remains thin for the *spontaneous-conscious-
    emergence* framing (§26 / §84 finding recurs); literature is
    dense on perceptual / dialogue / agentic emission, sparse on
    "talk unprompted because conscious".
11. SCoRe 2-stage (§93) is the only literature-validated multi-
    objective stacking recipe; T1's composition needs SCoRe-like
    sequential staging to be safe.
12. north-star + §15 / §51 / §72 / §117 milestones UNCHANGED;
    §163 is a literature-mapping cycle, NOT a GOAL movement.
13. PII discipline maintained: citations are generic first-author
    + year style or arxiv-ID only; no inlined PII.

---

## §7 — VERDICT

**`LITERATURE-SUPPORTS-§167-A-PATH`**

- Cluster partition closed (P1) ✅
- Candidate taxonomy exhaustive-disjoint (P2) ✅
- No candidate closed as solution (P3) ✅ (B-EMERGE-7)
- Connection-points cite real arxiv IDs + real §s (P4) ✅
- §161-FIRE failure mode addressed by Top-1 candidate (T1) (P5)
  ✅

**All 4 CONNECTION_CRITIQUE wrong-steps have literature-anchored,
§7-clean fixes.**  This is the §163's load-bearing positive
finding.

§167-A FP-RECONNECT (sibling parallel dispatch) is the closest
arc-internal design that uses ≥1 of these literature anchors;
§163 supports its theoretical foundation without prejudging its
empirical outcome.

Honest negative finding: the frontier remains thin for
spontaneous-emission-as-emergence framing.  Anima's choice to
treat emission as emergence (not dialogue label) is *uncommon*
in 2023-2026 literature; this is consistent with §26 / §84
prior findings.

GOAL distance: UNCHANGED.  WALL-A (§1.1 data-regime) UNCHANGED.
WALL-B (§96 substrate) UNCHANGED.  This is a method-level cycle.

---

## §8 — Artifact manifest

- `FRONTIER_FINDINGS.md` (this file) — §0..§7 narrative + paper
  graded scan + Top-3 candidate table
- `result.json` — machine-readable summary
- (No battery, no sympy — literature review tier mirrors §80 /
  §84 / §85 / §93 / §99 precedent)
