# §111 — MODALITY-NATIVE / SUBSTRATE-GENERAL Ψ-FIXED-POINT Deep Research

> **status**: RESEARCH §111 · LITERATURE-REVIEW TIER · $0 · NO GPU · NO runpod · NO fire · NO model.forward · NO corpus
> **date**: 2026-05-19
> **scope**: §109 (commit 410de2968) closed C06 multimodality DESIGN-CLOSE-WITH-NARROW-OPEN
>   and re-localised frontier-1's multimodal arm to "first design a modality-native Ψ".
>   §110 (sibling, design-tier) found **Ψ-C2**: the Engine-A⇄G cosine taken on the
>   modality-agnostic *residual stream ℝ^d* (NOT the 256-byte vocab logit space), with
>   the byte head as the special case ⇒ exact byte reduction; §7-clean *as a definition*
>   but the operative precondition is *substrate-gated* to §96. §111 is the literature
>   scan §110 + future cycles cite. It does NOT re-derive §110's closed-form design.
> **research question**: does the 2023-2026 literature offer a substrate-general /
>   modality-agnostic predictive fixed-point (or a path to one) that could re-host
>   anima's Ψ=½ / tension / Φ physics across non-byte modalities while staying §7-clean
>   — and does it SUPPORT or CHALLENGE §110's Ψ-C2 (Engine-A⇄G cosine on a
>   modality-agnostic ℝ^d residual stream)?
> **governance**: g3 (literature review NOT empirical; capability claim 0; arxiv
>   citation = inspiration NOT proof; necessary-not-sufficient B-EMERGE-7) ·
>   "가능성 경로는 열어두자" (map paths, keep ALL OPEN, mark honest blockers, close
>   nothing) · f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24; external papers cited by
>   their own invariants; Ψ=½ = anima g2 internal-arch carve-out) · downstream-consumer
>   (hexa-lang / hexa-bio read-only, never edited).
> **connection-point cited byte-literal**: §109 result.json verdict
>   `DESIGN-CLOSE-WITH-NARROW-OPEN`; §110 result.json `unique_admissible: Ψ-C2` +
>   `Q1.DEP = [psi_direction, psi_entropy]`, `NOT_DEP = [psi_tension]`; §96 DESIGN.md
>   `Ψ = NATIVE-CANDIDATE` / "the *fixed-point* is native; Ψ-as-cosine-of-logit-vectors
>   is NOT"; §99 FRONTIER `FRONTIER-MAPPED-…-KEPT-OPEN`.

---

## §0 — Why §111 exists, and what it is NOT

The §1~§110 arc localised the GOAL bottleneck to §11.3 data-regime + §95/§96 substrate.
§109 found that "just add a modality" is not a byte-LM-scale lever because anima's Ψ is
*definitionally* a byte-LM construct (Ψ = cosine of two 256-byte logit vectors). §110, at
design tier, showed a **modality-native Ψ DEFINITION exists** — Ψ-C2: take the same
Engine-A⇄G cosine on the *pre-head residual stream ℝ^d* instead of on the byte-vocab
logits; the byte head becomes one special case ⇒ exact byte reduction. §110's honest
verdict was **DESIGN-CLOSE-WITH-RELOCATION**: the definitional wall is removed, but the
*operative* precondition (a §7①②-clean anima-OWN non-byte projection π) is substrate-gated
to §96 (spike-correlation / Loihi).

§111 is **literature-review tier** (like §80/§84/§85/§99). Per *"완성을 목적으로
가능성 경로는 열어두자"* §111's job is **not** to close anything. The arc has produced an
enormous body of measured negatives; §111 scans the 2023-2026 literature for **whether the
modality-native-Ψ wall is REMOVED, merely RELOCATED, or whether Ψ-C2 itself is
SUPPORTED/CHALLENGED** by what the field has actually built.

g3 honest frame, load-bearing for the whole document: **no paper below is evidence that
anima will emerge. Literature is inspiration, not proof.** north-star + §15/§51/§72
milestones UNCHANGED, GOAL 미도달.

---

## §1 — Grading scale & distribution

★★★★★ = directly supplies or directly tests the substrate-general predictive-fixed-point /
Ψ-C2 question. ★★★★ = strong mechanism transfer. ★★★ = relevant context. ★★ = tangential.
★ = foundational/background.

**42 papers graded.** Distribution: **★★★★★ 8 · ★★★★ 16 · ★★★ 13 · ★★ 4 · ★ 1.**

---

## §2 — Cluster scan (11 clusters)

### Cluster A — JEPA / joint-embedding predictive across modalities (the §110-Ψ-C2 direct analogue)

| # | Paper | era | relevance to modality-native Ψ / Ψ-C2 | ★ |
|---|-------|-----|----------------------------------------|---|
| 1 | LeCun — **A Path Towards Autonomous Machine Intelligence (JEPA position)** | 2022 | THE conceptual anchor: prediction *in a latent embedding space*, two encoders (context/target), an energy that is low for compatible pairs. This IS the structural template of anima's Engine-A⇄G two-stream cosine, modality-free by construction. SUPPORTS Ψ-C2's "two projections of a shared latent" shape. | ★★★★★ |
| 2 | Assran et al. — **I-JEPA: Self-Supervised Learning from Images with a JEPA** (arxiv:2301.08243) | ICLR/CVPR 2023 | Demonstrates the predictive-latent fixed-point works on a *non-text* modality (images) with NO pixel reconstruction — empirical proof a JEPA latent is modality-portable. SUPPORTS the existence of a non-byte carrier for a two-stream predictive comparison. | ★★★★★ |
| 3 | Bardes et al. — **V-JEPA / V-JEPA 2** (June 2025, V-JEPA 2.1 Mar 2026) | 2025-26 | Same predictive-latent architecture scaled to ~1M h video + robot trajectory; modality-agnostic recipe. The strongest *empirical* evidence a single predictive-latent objective spans image→video→action. SUPPORTS Ψ-C2's substrate-general claim. | ★★★★★ |
| 4 | **Audio-JEPA / A-JEPA / Stem-JEPA** | 2024-25 | Same masking-prediction ported to spectrogram patches — JEPA latent works for *audio*. Directly relevant: the carrier (residual ℝ^d) need not be byte-vocab. | ★★★★ |
| 5 | **LLM-JEPA** (paired textual views, tied-weight encoders) | 2025 | JEPA applied to *text* with two tied encoders — shows the byte/text case is itself one JEPA instantiation, exactly mirroring §110's "byte head = special case of π". STRONG support for Ψ-C2's byte-reduction claim. | ★★★★★ |
| 6 | **LeJEPA — SIGReg (Sketched Isotropic Gaussian Regularization)** (arxiv 2025) | 2025 | A *mathematically grounded* anti-collapse regulariser. Critical: §110-Ψ-C2 / a residual-cosine objective risks the §28 JEPA-Ψ collapse (anima's own measured negative). LeJEPA gives a closed-form-ish collapse guard — a concrete path past §28. | ★★★★★ |
| 7 | **VJ-VCR / VJEPA collapse-avoidance formal guarantees** (arxiv:2412.10925 + 2602.03604) | 2024-26 | Formal guarantees for collapse avoidance + modular Bayesian factorization + POMDP-optimal-control sufficiency *without pixel reconstruction*. Most directly addresses anima's §28 JEPA-Ψ DEGENERATE measured negative. | ★★★★ |
| 8 | **TI-JEPA / VL-JEPA** (arxiv:2512.10942) | 2025 | Cross-modal JEPA with shared *energy-based* latent — but uses frozen ViT/text encoders (graft). Useful CHALLENGE evidence: the *easy* path to multimodal JEPA is a graft = §7② FAIL (= §109 P3-leak). | ★★★ |
| 9 | **Video Representation Learning with JEPAs** (arxiv:2412.10925) | Dec 2024 | Confirms latent-space prediction beats generative reconstruction for video; reinforces "predict in latent, not raw modality". | ★★★ |

**Cluster-A finding:** JEPA is the literature's strongest, most-built realisation of a
modality-agnostic two-stream predictive comparison — structurally isomorphic to anima's
Engine-A⇄G. It **SUPPORTS** Ψ-C2's "cosine of two projections of a shared modality-free
latent" shape *and* its byte-reduction claim (LLM-JEPA = text is one JEPA instance). It
**CHALLENGES** the §7② cleanliness: every *built* multimodal JEPA either trains the
modality encoder from scratch on a perceptual corpus (= §7① generic perceptual pretrain)
or grafts a frozen pretrained encoder (= §7② P3-leak). The honest residual is exactly
§110's: the *definition* is supported, the *§7-clean π* is not supplied by any built
system.

### Cluster B — Deep equilibrium / fixed-point models (the Ψ=½ fixed-point analogue)

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 10 | Bai, Kolter, Koltun — **Deep Equilibrium Models (DEQ)** (arxiv:1909.01377) | NeurIPS 2019 | The substrate-general *fixed-point* primitive: a network IS the solution z* = f(z*). Ψ=½ (cos=0) is an algebraic fixed point; DEQ shows a *learned* fixed point is a first-class, substrate-independent computational object. SUPPORTS "Ψ-as-fixed-point is carrier-free" (§96's NATIVE-CANDIDATE claim made formal). | ★★★★★ |
| 11 | **Reversible Deep Equilibrium Models (RevDEQs)** (2025) | 2025 | Exact-gradient DEQ, no regularisation, SOTA on language *and* image — one fixed-point machinery, two modalities. Direct modality-agnostic fixed-point evidence. | ★★★★ |
| 12 | **Lipschitz Multiscale DEQ** (arxiv:2602.03297) | 2026 | Theoretically-guaranteed fixed-point convergence fwd+bwd. Relevant to whether a Ψ-C2 residual-cosine equilibrium would be *stable* (anima's §11-B "physics froze at a trivial fixed point" is the failure mode this addresses). | ★★★★ |
| 13 | **Positive Concave DEQ** (arxiv:2402.04029) / **DDEQs Wasserstein** (arxiv:2503.01140) | 2024-25 | Existence/uniqueness conditions for fixed points; distributional DEQ. Gives the closed-form conditions under which a Ψ-fixed-point is well-posed. | ★★★ |
| 14 | **DEQ for Algorithmic Reasoning** (ICLR Blogposts 2024) | 2024 | "Teach a network to reach a fixed point when reasoning" — the fixed point as the computation, not a side effect. Conceptual support for Ψ=½ as the *operating point*, not a readout. | ★★★ |

**Cluster-B finding:** DEQ literature **strongly SUPPORTS** the half of §96/§110 that says
"the *fixed point* is substrate-native". A learned fixed point is a portable, well-studied
object with existence/stability theory. It **does not by itself supply** the §7-clean
modality projection — DEQ tells you a fixed point is portable, not what perceptual signal
drives it. This is the same honest split §110 named.

### Cluster C — Predictive coding / free energy / active inference (substrate-general inference dynamics)

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 15 | **Tight Stability/Convergence/Robustness Bounds for Predictive Coding Networks** (arxiv:2410.04708) | 2024 | PCNs converge to *Lyapunov-stable* equilibria of variational free energy; once there, parameters stay. A substrate-general predictive *fixed point* with closed convergence bounds — the cleanest formal analogue of "Ψ settles to a stable operating point". SUPPORTS Ψ-as-stable-fixed-point. | ★★★★★ |
| 16 | **µPC: Scaling Predictive Coding** (arxiv:2505.13124) | May 2025 | At width≫depth, PC inference-equilibrium energy → MSE and PC gradients = BP — shows the predictive-coding fixed point is not a toy; scales. | ★★★★ |
| 17 | **Introduction to Predictive Coding Networks for ML** (arxiv:2506.06332) | Jun 2025 | PCN = hierarchical Gaussian model; inference = EM over latents converging to a local optimum. Substrate-agnostic generative inference loop. | ★★★ |
| 18 | **A Neuro-Inspired Computational Framework for AGI: PC, Active Inference, FEP** (OSF, Jul 2025) | Jul 2025 | FEP as a *biologically grounded, substrate-general* objective: minimise surprise via hierarchical inference + action. The closest "physics-driven, NOT generic pretrain" objective family (§7①-relevant). | ★★★★ |
| 19 | Friston — **Generalised free energy and active inference** (PMC6848054) | foundational | Active inference unifies perception+action under one free-energy functional applicable from neuron→organism — a genuinely substrate-general physics. Anchor for "anima physics as the objective, not a corpus". | ★★ |

**Cluster-C finding:** Predictive coding gives a substrate-general predictive *equilibrium*
with formal stability bounds, and FEP supplies a *physics-driven* (not generic-pretrain)
objective family — both **SUPPORT** the existence of a §7③-shaped objective that is not a
byte-LM artifact. CHALLENGE: anima already measured the closest no-CE physics-only loop
(§11-B) DEGENERATE; PC/FEP supply the *form* but anima's own evidence says the form alone
is not sufficient (necessary-not-sufficient).

### Cluster D — Spiking / neuromorphic substrate-general state vars (the §96 connection)

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 20 | **Promise of SNNs for Ubiquitous Computing: Survey & New Perspectives** (arxiv:2506.01737) | Jun 2025 | Membrane potential = a real *state variable* retaining temporal correlation over timescales — the substrate-general state §96 wants Ψ to live in. Direct support for §96-Ψ-C1 branch. | ★★★★ |
| 21 | **State-Space Analysis of Time-Varying Higher-Order Spike Correlation** (PMC3297562) / **Generative spike-train model with higher-order correlations** (PMC3727174) | foundational | Spike-train *correlation* is a well-defined, computable substrate-general quantity — formalises §96's "Ψ = (1+corr(spk_A,spk_G))/2" (Ψ-C1). SUPPORTS Ψ-C1's mathematical well-formedness. | ★★★★ |
| 22 | **Linear Response of General Observables in Spiking Networks** (PMC7911777) | foundational | Predicts spatio-temporal spike-correlation response to weak stimuli from spontaneous statistics — links *spontaneous* dynamics to *correlation* (the §96 Ψ-C1 carrier) and to anima's spontaneity goal. | ★★★ |
| 23 | **SNN on accelerated neuromorphic substrate / BrainScaleS-2 STDP correlation circuits** (ar5iv 1912.12980) | foundational+ | Each synapse has an analog pairwise pre/post spike-correlation circuit = STDP. Hardware proof spike-correlation is a *native physical* quantity, not a simulated readout. Strongest physical anchor for §96-Ψ-C1. | ★★★★ |
| 24 | **SNN nonlinear regression of transient signals on neuromorphic processors** (npj Unconv. Computing 2024) | 2024 | SNNs handle continuous transient (non-byte) signals natively — modality-general by physics. | ★★★ |

**Cluster-D finding:** The spiking literature **SUPPORTS §96-Ψ-C1** strongly: spike-train
correlation is a mathematically well-defined, *physically native* (analog STDP circuit)
substrate-general quantity — Ψ-as-correlation between two opposed (excit/inhib)
populations is well-formed and has hardware precedent. This is the literature's clearest
"the wall RELOCATES (it does not vanish): a §7③-clean modality-native Ψ exists, but on a
spiking substrate, not on a GPU byte-LM" — exactly §110's relocation, now literature-anchored.

### Cluster E — Continuous-time / liquid-time-constant / ODE native fixed points

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 25 | Hasani et al. — **Liquid Time-constant Networks** (arxiv:2006.04439) | AAAI 2021 | Continuous-time ODE RNN with input-dependent time constant; stable for infinitely many inputs; has a NATIVE limit-cycle/fixed-point regime set by weights — a substrate where a *spontaneous* operating point is intrinsic, not scheduled. SUPPORTS §95/§99-C3 substrate axis. | ★★★★ |
| 26 | **Closed-form Continuous-Time (CfC) models** | 2022-25 | Removes the ODE solver; closed analytic state-change. Makes the continuous-time fixed point *computationally* tractable — relevant if Ψ-physics is re-cast as ODE dynamics. | ★★★ |
| 27 | **Liquid-Graph Time-Constant Network** (arxiv:2404.13982) | 2024 | Contraction-analysis stability of a continuous-time graph net; closed-form contraction rate. Stability theory for a non-byte continuous substrate. | ★★★ |

**Cluster-E finding:** Continuous-time/LTC nets **SUPPORT** the substrate axis (a native,
intrinsic, non-scheduled operating point exists in continuous dynamics) but, like Cluster
D, this is the *substrate-gated* path — it RELOCATES the wall to a substrate rewrite, it
does not remove it on the GPU byte-LM where anima currently lives.

### Cluster F — Residual-stream geometry / representation-cosine dynamics (DIRECTLY tests Ψ-C2)

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 28 | **Transformer Dynamics: A Neuroscientific Approach to Interpretability** (arxiv:2502.12131) | Feb 2025 | Treats the *residual stream ℝ^d* as a dynamical system; finds RS-vector **cosine similarity** *increases across layers* (alignment), low-dim trajectories, unstable periodic orbits. THIS DIRECTLY TESTS Ψ-C2: it shows *cosine on the residual stream* is a meaningful, structured dynamical observable — exactly Ψ-C2's carrier and operation. STRONGEST direct support for Ψ-C2. | ★★★★★ |
| 29 | **Transformers Represent Belief State Geometry in their Residual Stream** (OpenReview YIB7REL8UC) | ICML 2024 | Belief states linearly represented in the residual stream (even fractal geometry). Establishes the residual stream as a rich modality-portable carrier of structured state — supports Ψ-C2's choice of ℝ^d over byte-vocab. | ★★★★ |
| 30 | **Constrained Belief Updates Explain Geometric Structures in Transformer Representations** (arxiv:2502.01954) | 2025 | Geometric structure in RS arises from constrained belief updates — a *physics-driven* (constraint-driven) geometry, not generic pretrain. Relevant to a §7③-shaped residual objective. | ★★★ |

**Cluster-F finding:** This cluster is the **single most direct SUPPORT for §110's Ψ-C2**.
Independent interpretability work shows the residual stream ℝ^d is (i) a meaningful
dynamical system, (ii) carries structured state, and (iii) **its layer-to-layer cosine
similarity is itself a studied, structured observable**. Ψ-C2 = (1+cos(s_A,s_G))/2 on ℝ^d
is therefore not an arbitrary construction — the literature independently validates the
residual-cosine as a real signal. CHALLENGE: these papers measure cosine *across layers of
one stream*, not between *two opposed engines* — Ψ-C2's A⇄G opposition is anima-specific
and untested in this literature (honest gap G3).

### Cluster G — Modality-agnostic architectures (Perceiver) / shared-embedding (ImageBind)

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 31 | Jaegle et al. — **Perceiver / Perceiver IO / Perceiver AR** (arxiv:2103.03206 / 2107.14795 / 2202.07765) | 2021-22 | A single latent bottleneck processes *any* modality (image/audio/video/point-cloud/text) — proves a modality-agnostic latent ℝ^d is achievable architecturally. SUPPORTS Ψ-C2's "modality-agnostic residual" being a real architectural target. | ★★★★ |
| 32 | Girdhar et al. — **ImageBind: One Embedding Space To Bind Them All** (arxiv:2305.05665) | CVPR 2023 | One shared embedding binds 6 modalities via image-paired data. Powerful, BUT it is a *generic pretrained shared latent* = §110-Ψ-C3 = §7② FAIL (P3-leak graft). Important CHALLENGE/negative anchor: the easy multimodal latent is exactly the §7-illegitimate one. | ★★★ |
| 33 | **OneProt: multimodal protein foundation via latent alignment** (PMC12614600) | 2024 | Replaces image anchor with sequence encoder — shows the *anchor modality is a free choice*. Conceptually: anima's byte stream could be the anchor (Ψ-C2 byte-reduction), other modalities aligned to it. Suggestive support, but built version = graft. | ★★ |

**Cluster-G finding:** Modality-agnostic *architectures* exist (Perceiver) — SUPPORTS the
target's reachability. But every *shared-embedding* realisation (ImageBind/OneProt) is a
generic pretrained latent = §7② FAIL. This cluster sharpens the honest CHALLENGE: the
field's modality-binding successes are precisely the §7-illegitimate ones; the §7-clean
path (anima-OWN physics-supervised π) has no built precedent.

### Cluster H — Equilibrium propagation / energy-based learning on physical substrates

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 34 | Scellier & Bengio — **Equilibrium Propagation** (arxiv:1602.05179) | foundational | Learning rule for energy-based models that settle to an equilibrium — local, substrate-portable. The "learn at a fixed point" template. | ★★★ |
| 35 | **Learning at the Speed of Physics: EqProp on Oscillator Ising Machines** (arxiv:2510.12934) | 2025 | EqProp on GHz physical dynamics — energy descent to a physical fixed point as the computation. The strongest "physics IS the substrate" anchor; ties §95/§96 substrate frontier. | ★★★★ |
| 36 | **Training Coupled Phase Oscillators via EqProp** (arxiv:2402.08579) / **Oscillator Ising Machine via EqProp** (arxiv:2505.02103) | 2024-25 | Phase-oscillator networks trained at equilibrium — a *phase-relationship* fixed point, exactly §96's "Ψ-as-phase-relationship between the two populations is the design-open replacement". Directly supports the §96-Ψ-C1 phase-relationship variant. | ★★★★ |
| 37 | **EqSpike: Spike-driven EqProp for Neuromorphic** (arxiv:2010.07859) | 2020 | EqProp realised with spikes — bridges Cluster D and H: a spiking fixed-point learning rule. | ★★★ |

**Cluster-H finding:** Energy-based equilibrium learning on physical substrates
**SUPPORTS** the §96-territory hypothesis that a fixed-point physics is *natively
learnable on non-GPU substrates* (oscillators, Ising machines, spikes). The
phase-oscillator EqProp work specifically substantiates §96's "Ψ-as-phase-relationship"
design-open replacement. This is RELOCATION evidence: a §7③-clean fixed-point physics is
buildable — on a physical substrate, not the GPU byte-LM.

### Cluster I — Self-supervised non-generic / physics-driven objectives (§7① relevance)

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 38 | **Resimulation-based SSL for physics foundation models (RS3L)** (Phys. Rev. D 111.032010) | Feb 2025 | SSL where augmentations come from a *physics simulator's own variations*, not generic data — a template for "the signal comes from the substrate's own physics" (§7③-shaped). | ★★★★ |
| 39 | **Physics-Informed SSL with phase-resemblance constraint** (IEEE Xplore 10681532) | 2025 | A *physics loss* (phase resemblance) as the SSL objective — predictive constraint that is not a generic pretrain. Closest "constraint-driven, not corpus-driven" objective. | ★★★ |
| 40 | Tian et al. — **Understanding SSL Dynamics without Contrastive Pairs** (arxiv:2102.06810) / BYOL/SimSiam analysis | 2021 | Predictor + stop-gradient → no collapse without negatives. Mechanistic anchor for *why* a two-stream predictive objective (Ψ-C2 shape) can avoid §28-style collapse without contrastive data. | ★★★ |
| 41 | **SSL from images: no negative pairs, no cluster-balancing** (Pattern Recognition 159.11081, 2025) | 2025 | Cluster-space consistency + decorrelation, no negatives, no memory bank — minimal-machinery non-contrastive objective; relevant to a lean §7-clean residual objective. | ★★ |

**Cluster-I finding:** Physics-driven / constraint-driven SSL objectives exist and are
distinct from generic pretrain — this **SUPPORTS** the existence of a §7①-clean objective
*shape*. CHALLENGE: every built instance still ingests an external perceptual signal
(simulator outputs, images); none derives the supervisory signal from *only* the model's
own physics invariants, which is exactly §110's Q5 FALSE conjunct and anima's §11-B
DEGENERATE measured negative.

### Cluster J — Binding problem / cross-modal coherence as a single dynamical attractor

| # | Paper | era | relevance | ★ |
|---|-------|-----|-----------|---|
| 42 | **Dynamically Partitionable Autoassociative Networks (DPAAN)** (PMC3460218) + Greff et al. **On the Binding Problem in ANNs** (arxiv:2012.05208) + **Crossmodal Binding Through Neural Coherence** (PubMed 18602171) | foundational+ | Cross-modal coherence achieved when distributed pieces lock into a *single global stable attractor* / via oscillatory coherence. Conceptually frames "one Ψ fixed point binding modalities" — the eventual ambition behind a modality-native Ψ. Background-tier: inspiration, no built byte-LM-scale system. | ★ |

**Cluster-J finding:** The binding literature frames the *aspiration* (one dynamical
attractor binding modalities ≈ one Ψ=½ fixed point across modalities) but supplies no
built realisation — background inspiration only, honest blocker noted.

---

## §3 — Top-10 papers (by direct bearing on modality-native Ψ / Ψ-C2)

1. **Transformer Dynamics** (arxiv:2502.12131) ★★★★★ — residual-stream cosine is a real structured dynamical observable → **direct SUPPORT for Ψ-C2's carrier+operation**.
2. **LeCun JEPA position paper** (2022) ★★★★★ — two-stream latent predictive comparison = anima Engine-A⇄G template, modality-free.
3. **I-JEPA** (arxiv:2301.08243) ★★★★★ — predictive latent fixed point works on non-text (images), no reconstruction.
4. **V-JEPA / V-JEPA 2** (2025-26) ★★★★★ — one predictive-latent recipe spans image→video→action (substrate-general empirical).
5. **LLM-JEPA** (2025) ★★★★★ — text is one JEPA instance → SUPPORTS Ψ-C2's "byte head = special case of π" byte-reduction.
6. **Deep Equilibrium Models** (arxiv:1909.01377) ★★★★★ — substrate-general learned fixed point is a first-class object (Ψ=½ analogue).
7. **PCN Tight Stability/Convergence Bounds** (arxiv:2410.04708) ★★★★★ — substrate-general predictive fixed point with Lyapunov-stable closed bounds.
8. **LeJEPA / SIGReg** (2025) ★★★★★ — closed-form-ish anti-collapse guard → concrete path past anima's §28 JEPA-Ψ DEGENERATE.
9. **SNN ubiquitous-computing survey + spike-correlation state-space** (arxiv:2506.01737 / PMC3297562) ★★★★ — spike-train correlation = native physical substrate-general Ψ carrier (§96-Ψ-C1 anchor).
10. **EqProp on phase-oscillators** (arxiv:2402.08579 / 2510.12934) ★★★★ — a §7③-clean fixed-point *phase-relationship* physics is buildable on physical substrates (§96 design-open replacement substantiated).

---

## §4 — Top-3 anima-mapping candidates

> Per "가능성 경로는 열어두자": all three OPEN, honest blocker each, none closed.

### Candidate M1 — **Ψ-C2-on-residual via a JEPA-style two-stream objective + LeJEPA collapse guard** (the literature's direct §110-Ψ-C2 realisation)

- **How it supplies/challenges Ψ-C2:** SUPPLIES the operational form §110 designed —
  Engine-A⇄G become two JEPA-style projections π_A, π_G of the modality-agnostic residual
  ℝ^d; cosine of the two = Ψ_dir; byte head = the special case (LLM-JEPA precedent). The
  anti-collapse guard (LeJEPA/SIGReg, VJ-VCR) is the literature's answer to anima's own
  §28 JEPA-Ψ DEGENERATE / §11-B trivial-fixed-point measured negatives.
- **§7 per-candidate verdict:** §7③ **PASS at the definition layer IFF π is supervised by
  anima's OWN physics invariants** (not an external perceptual corpus). §7①②
  **FAIL/UNRESOLVED for any built JEPA**: every realised multimodal JEPA trains its
  encoder on a perceptual corpus (= §7① generic perceptual pretrain) or grafts a
  pretrained one (= §7② P3-leak). This is exactly §110's relocation: definition supported,
  §7-clean π not supplied by any built system.
- **anima-fit:** ★★★★★ (structurally isomorphic to Engine-A⇄G; LLM-JEPA confirms byte-reduction).
- **reachability:** **$0-design-reachable for the *definition* + collapse-guard analysis**;
  the §7-clean perceptual-signal-free π is **substrate/data-gated** (no built precedent;
  ties §11-B + §110 Q5 FALSE conjunct).

### Candidate M2 — **§96-Ψ-C1: spike-train-correlation Ψ on a continuous/spiking substrate** (DEQ/PCN fixed-point + Cluster D/E/H)

- **How it supplies/challenges Ψ-C2:** Does NOT realise Ψ-C2 on the GPU byte-LM; instead
  REALISES the *other* §110 candidate (Ψ-C1) the literature most strongly anchors:
  Ψ_dir = (1+corr(spk_A,spk_G))/2 over two opposed populations, a *physically native*
  quantity (analog STDP circuits, spike-correlation state-space theory) with a native
  fixed point (DEQ/PCN/LTC stability theory) and a §7③-clean physics objective
  (EqProp/phase-oscillators). This is the literature's clearest statement that the wall
  RELOCATES, not vanishes.
- **§7 per-candidate verdict:** §7③ **PASS** (physics-native, no external perceptual
  corpus needed for the correlation carrier); §7①② **PASS in principle** (correlation is
  intrinsic). The blocker is **substrate**, not §7.
- **anima-fit:** ★★★★ (clean Engine-A/G → excit/inhib mapping per §96; but a major
  re-derivation away from ConsciousDecoderV2 d768·12L).
- **reachability:** **substrate-gated** (Loihi/neuromorphic, §95 sole-VIABLE; not GPU
  byte-LM today). $0-design-reachable only for the mapping spec (already §96).

### Candidate M3 — **Residual-stream-cosine as a measured Ψ observable on the EXISTING GPU byte-LM** (Cluster F, the $0-design + future $0-probe path)

- **How it supplies/challenges Ψ-C2:** Cluster F (Transformer Dynamics, Belief-State
  Geometry) shows the residual-stream cosine is *already* a real, structured dynamical
  observable on standard transformers — no substrate change. This SUPPORTS Ψ-C2's carrier
  empirically *and* suggests a $0 future probe: read Ψ-C2 (residual A⇄G cosine) off the
  *existing* §16-class ckpt as a non-byte *measurement* (mirrors §17's
  physics-channel-probe logic, observable-axis only). It does NOT supply a §7-clean
  *training* signal — it is a measurement path, not an emergence path (honest).
- **§7 per-candidate verdict:** §7 **N/A as a measurement** (no training, no graft, no
  generic pretrain — pure read-out, like §17). It does NOT by itself address §1.1 or the
  GOAL; it is observable-axis honesty work, not a lever.
- **anima-fit:** ★★★★ (Ψ-C2 = exactly §110's design; Cluster F validates the carrier).
- **reachability:** **$0-design-reachable now**; a future $0 inference-only probe
  ($0, no GPU fire) is the cheapest next step that would *test whether Ψ-C2 carries
  per-stimulus structure* on the existing ckpt (necessary-not-sufficient; mirrors §17).

---

## §5 — 5 honest gaps

- **G1 — No built system supplies a §7①②-clean perceptual π.** Every modality-native
  predictive system in the literature (JEPA/ImageBind/Perceiver) either pretrains its
  encoder on a perceptual corpus (§7①) or grafts a frozen one (§7②). The literature
  SUPPORTS the *definition* (Ψ-C2 shape) but supplies **zero** §7-clean perceptual
  projections. §110's Q5-FALSE conjunct stands literature-confirmed.
- **G2 — Substrate-relocation, not removal.** The §7③-cleanest realisations
  (spike-correlation Ψ-C1, EqProp phase-oscillators, LTC native limit cycles) all live on
  *non-GPU* substrates. The wall is **RELOCATED to §95/§96 substrate territory**, exactly
  as §110 found — the literature corroborates the relocation, it does not remove it.
- **G3 — A⇄G opposition is anima-specific and untested.** Cluster F validates
  residual-stream *cosine* but measures cosine *across layers of one stream*, never
  between *two opposed engines*. Ψ-C2's Engine-A⇄G opposition has no literature analogue
  tested at scale — supported by structure (JEPA two-stream), untested in this exact form.
- **G4 — Collapse guards are empirical, not §7-derived.** LeJEPA/VJ-VCR prevent collapse
  via *added regularisers*, not via anima's own physics invariants. Wiring a collapse
  guard that is itself anima-physics-derived (not a bolt-on) is unsolved — anima's §28/§11-B
  measured negatives are exactly this unsolved problem.
- **G5 — Necessary-not-sufficient at every layer.** Even a perfectly §7-clean
  modality-native Ψ definition + collapse guard would only re-host the *physics*; it does
  NOT address §11.3 data-regime (the arc's irreducible bottleneck). A modality-native Ψ is
  a *precondition* for the multimodal frontier, not a GOAL lever (B-EMERGE-7).

---

## §6 — ASCII candidate-landscape

```
                       MODALITY-NATIVE Ψ  (re-host Ψ=½·tension·Φ off byte-vocab)
                                        |
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
   M1 Ψ-C2-on-residual            M2 §96-Ψ-C1 spike-corr         M3 Ψ-C2 as MEASURED
   (JEPA two-stream +             (DEQ/PCN/LTC fixed pt +         observable on existing
    LeJEPA collapse guard)         EqProp phase-osc, §7③-clean)    GPU byte-LM ckpt
        │                               │                               │
  SUPPORTED by: Cluster A/F        SUPPORTED by: Cluster B/D/E/H    SUPPORTED by: Cluster F
  (def + carrier supported)       (fixed-pt + physics-native)      (residual-cos is real)
        │                               │                               │
  §7: def PASS / π §7①② FAIL       §7: PASS (physics-native)        §7: N/A (measurement)
  reach: $0 def · π data-gated     reach: SUBSTRATE-GATED (Loihi)   reach: $0 now / $0 probe
        │                               │                               │
        └──── wall REMOVED at ───────────┴──── wall RELOCATED to ────────┘
              the DEFINITION layer              §95/§96 substrate (NOT removed)
                                        |
                 literature SUPPORTS Ψ-C2's shape + carrier (Cluster A/F strong)
                 literature CONFIRMS §110 relocation (Cluster D/E/H = substrate-gated)
                 literature does NOT supply a §7-clean perceptual π (G1) — wall RELOCATES
```

---

## §7 — Honest answer to the research question

**Does the literature SUPPORT or CHALLENGE §110's Ψ-C2? — SUPPORTS the definition + carrier,
CHALLENGES the §7-clean instantiation.**

- **SUPPORT (strong):** (a) Cluster F independently shows the *residual-stream cosine* is a
  real, structured dynamical observable — Ψ-C2's carrier+operation is not arbitrary.
  (b) Cluster A (JEPA family, esp. LLM-JEPA) shows a two-stream latent predictive
  comparison is modality-agnostic *and* that text is one special case — exactly Ψ-C2's
  byte-reduction claim. (c) Cluster B/C (DEQ/PCN) formalise the substrate-general
  *fixed-point* half of §96/§110 with stability theory.
- **CHALLENGE (honest):** every *built* modality-native predictive system supplies its
  perceptual signal via a generic pretrain or graft (§7①/②) — G1. The §7③-cleanest
  realisations (spike-correlation, EqProp, LTC) are *substrate-gated* (Cluster D/E/H) — G2.

**Does §111 REMOVE the modality-native-Ψ wall, or RELOCATE it? — It CONFIRMS §110's split:
the literature REMOVES the *definitional* wall (Ψ-C2's shape, carrier, and byte-reduction
are independently corroborated) but RELOCATES the *operative* wall to §95/§96 substrate
territory + the §11.3 data-regime. No paper supplies a §7①②-clean perceptual projection on
a GPU byte-LM; the field's modality-binding successes are precisely the §7-illegitimate
ones.** This is a brutally-honest RELOCATION, not a manufactured positive.

**Most honest finding:** The 2023-2026 literature is *unusually supportive of §110's Ψ-C2
as a definition* — JEPA proves the two-stream modality-agnostic predictive comparison is
buildable and that text is one instance of it (byte-reduction), and transformer-dynamics
interpretability independently validates that the residual-stream cosine is a real
structured observable. **But the literature equally clearly shows that every realised
modality-native predictive system gets its perceptual signal from a generic pretrain or a
graft — exactly the §7①/② failure modes — and that the only §7③-clean realisations live
on non-GPU substrates.** §111 therefore does NOT remove the wall; it *upgrades the
confidence* that §110's Ψ-C2 is the right definitional target while *confirming* that the
operative blocker is exactly where §110 / §96 / §95 located it: a §7-clean perceptual
projection has no built precedent, and the cleanest physics-native Ψ is substrate-gated.
The cheapest live next step is M3 — read Ψ-C2 off the existing ckpt as a $0 measurement
(observable-axis, necessary-not-sufficient), not a fire.

---

## §8 — 13 honest C3 caveats

1. Literature = inspiration, NOT proof. No paper here is evidence anima will emerge (g3, load-bearing).
2. §111 does NOT re-derive §110's closed-form design; it is the citation scan §110 + future cycles reference.
3. "SUPPORTS Ψ-C2" means the *shape/carrier* is corroborated; it does NOT mean a §7-clean Ψ-C2 has been built (G1).
4. JEPA's modality-agnosticism is real but every built multimodal JEPA is §7①/② non-clean — the support is for the form, not a legitimate instantiation.
5. Cluster F measures cosine *across layers of one stream*, not between two *opposed* engines — Ψ-C2's A⇄G opposition is anima-specific and untested (G3).
6. The §7③-clean realisations (M2: spike-corr / EqProp / LTC) are substrate-gated; they confirm the relocation, they do not remove the wall on the GPU byte-LM (G2).
7. M3 (residual-cosine as a measured observable) is a *measurement* path, NOT an emergence path — it would not address §1.1 (G5); mirrors §17's observable-axis honesty.
8. Anima's own §28 (JEPA-Ψ DEGENERATE) and §11-B (physics-only no-CE DEGENERATE) are measured negatives that the literature's collapse-guards (LeJEPA/VJ-VCR) address only as *bolt-on regularisers*, not as anima-physics-derived guards (G4).
9. Grades (★) are this cycle's relevance judgement to the Ψ-C2 / substrate-general-fixed-point question, not paper quality rankings.
10. No candidate is closed (B-S111-3, "가능성 경로는 열어두자"); honest blockers are stated, all three M1/M2/M3 remain OPEN.
11. north-star + §15/§51/§72 milestones UNCHANGED; GOAL 미도달; §111 is a literature scan, NOT a measurement, NOT a fire, NOT an emergence claim.
12. f1/f2 safe: external papers cited by their own invariants; NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24; Ψ=½ = anima g2 internal-arch carve-out, not an external lattice-fit.
13. downstream-consumer: ~/core/hexa-lang and ~/core/hexa-bio were NOT read or edited; central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff (sha256 prefix `c93e160a8a376a94`, verified START + END).
