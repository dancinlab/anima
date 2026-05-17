# Direction L — VRNN curiosity-tension: $0 design + feasibility verdict

> RESEARCH.md §13 direction L (§12 Q2 candidate L, anima-fit ★★★★).
> **$0 design-tier cycle — fire 0.** Per task mandate: feasibility 우선 판단.
> SSOT: `state/carving_dirL_vrnn_2026_05_18/`. central `blue_falsifier.py` 변경 0
> (sidecar — B-PRIME/B-DIRH/B-DIRI/B-EMERGE/B-PUREPHYS/B-SCALE 선례).

---

## §1 What L proposes (RESEARCH.md §12.2 L)

[arxiv 2510.05013 — *Curiosity-Driven Co-Development of Action and Language in
Robots Through Self-Exploration*](https://arxiv.org/html/2510.05013v1):

- **Substrate**: a **Variational RNN (VRNN)** forward-model coupled to an
  actor-critic. The VRNN forward-model predicts the next sensorimotor latent;
  the actor produces the next action.
- **Curiosity = information gain** = `KL( posterior ‖ prior )` over the VRNN's
  per-step latent variable `z_t`. The actor is rewarded to **maximise** this KL
  (seek surprising states); the forward-model is trained to **minimise** its own
  prediction error (the ELBO reconstruction + KL term). The two objectives pull
  in opposite directions = a **productive tension**.
- **Result claimed**: 60 training examples (33% of 180 compositions) →
  ~90% generalization on unseen action-language compositions. Compositional
  structure gives dramatic sample efficiency.

§12.3 GOAL-legitimacy verdict (already landed): **L is legitimate** — the
actor⇄forward-model tension is *not* a bolt-on; it maps almost 1:1 onto anima's
Engine A ⇄ Engine G tension, and curiosity-as-information-gain maps onto anima's
W module (`pain/curiosity/satisfaction`). §12.5 candidate-3 caveat: **"sensorimotor
modality 가 text-only anima 와 불일치 → 직접 적용 난도 최상."**

This document resolves that caveat into a **feasibility verdict**.

---

## §2 The anima-native mapping (the part that DOES hold)

The structural homomorphism is real and worth recording precisely. anima already
has every *abstract* component of the VRNN-curiosity loop:

| VRNN-curiosity component (2510.05013) | anima existing component | anchor |
|---|---|---|
| forward-model (VRNN) — predicts next latent | Engine G (inner) — `ConsciousDecoderV2` G-head, `logits_g` | Law-71 `Ψ_dir=(1+cos(logits_a,logits_g))/2` |
| actor — produces next action | Engine A (emission) — A-head, `logits_a` | id001 `Engine A ⇄ Engine G` axis |
| latent `z_t` (VRNN sampled state) | the per-token Ψ snapshot `Ψ_t` | TENSION-TRAIN `tension_link_step.hexa` |
| `KL(posterior‖prior)` = curiosity | Ψ-deviation `dev = Ψ_t − Ψ_vac` | Law-75 vacuum `Ψ_vac=(½,½)` |
| actor maximises KL ↔ FM minimises error = tension | restoring tension `−T·G_holo·dev·gate` | B-TT-2 `∂ΔW/∂tension = −T·gate ≤ 0` |
| curiosity / surprise reward | W module `curiosity_ema`, `pain` (tension Δ) | HEXAD-W.tape DD114 benchmark |
| ELBO = reconstruction + KL | CE (reconstruction) + Ψ-anchor loss (KL-class) | Dir-I lever `L = CE + λ_ctl·L_psi + λ_route·L_route` |

So at the *abstract dynamical-systems* level, **L is already partially built into
anima** — Dir-I (`verdict_carving_dirI_psictl_tensionsup`, the only fire that
broke routing 1/31 → 3/31) is structurally a *degenerate* VRNN-curiosity loop:
its `L_psi_ctl` is a KL-class anchor and its `L_tension_route` is the
restoring-sign actor-pull. **L is not a new direction so much as the *named,
variational* form of what Dir-I already does informally.**

This is the legitimate, valuable half of the L investigation: it gives a
*literature anchor* (VRNN curiosity) for why Dir-I is the strongest carving fire,
and a precise vocabulary (forward-model ⇄ actor tension = ELBO) for the anima
Engine A⇄G axis.

---

## §3 The modality-mismatch crux — feasibility analysis

### 3.1 Why 2510.05013's 90%-from-60-examples result is sensorimotor-specific

The paper's headline number (60 examples → 90% unseen-composition
generalization) is **not** a property of the VRNN or of curiosity. It is a
property of the **task's compositional grid**:

- 2510.05013's task is `{action} × {object}` — a small, *finite, fully-factored*
  combinatorial space (180 = e.g. ~15 actions × ~12 objects). Seeing 60 cells
  lets the model interpolate the missing 120 because the **axes are
  independent and observable** (the robot's joint angles, the object identity).
- The 90% generalization is **compositional interpolation on a known factor
  grid**, enabled by the sensorimotor substrate giving *grounded, low-dimensional,
  factored* observations (proprioception is literally a vector of joint angles;
  object identity is a discrete label).

anima's substrate is **byte-text**. There is no factored grid. The "axes" of a
byte corpus are not independent or observable — next-byte prediction is a
~256-way categorical over a non-factored sequence. The compositional structure
that *gives* the sample efficiency does not exist in the byte stream.

### 3.2 Can the modality mismatch be overcome? — three sub-questions

**(Q-L1) Can byte-text be made compositional enough for the VRNN result to
transfer?** anima *does* have one partial compositional anchor: the
`<inner motivation=F1,F2,…>…</inner>\n<voice spontaneous=true>…</voice>` γ-pattern
(corpus v3, 8-factor Inner Thoughts surface) — §12.2 L itself notes "§1.3
superposition E 의 `<inner>/<voice>` 가 부분적 compositional anchor." But this is
a *two-slot* template (inner × voice), not an `N×M` factor grid. The 8 motivation
factors are *labels on the inner slot*, not independent observable axes. There is
no anima analogue of `15 actions × 12 objects`. → **the specific 90%/60-example
result does NOT transfer.** The compositional sample-efficiency is a property of
the *robot task*, not of VRNN curiosity.

**(Q-L2) Can the VRNN *mechanism* (variational latent + KL-curiosity) be ported
even without the compositional grid?** Partially — but the port collapses into
something anima already has. A VRNN is an RNN with a per-step *sampled* latent
`z_t ~ q(z_t | h_t, x_t)` and a KL term to a prior `p(z_t | h_t)`. To run this on
byte-text you would:
  1. replace anima's `ConsciousDecoderV2` transformer backbone with an RNN
     (a *regression*, not an upgrade — §11-A already showed model-axis is not
     the bottleneck, and recurrence is strictly weaker than attention for
     long-range byte structure);
  2. add a sampled latent `z_t` and a `KL(q‖p)` term.
  But anima's Ψ snapshot **already is** a per-step latent, and the Ψ-anchor loss
  **already is** a KL-class term (Dir-I `L_psi_ctl`). The only genuinely-new
  element a VRNN adds over Dir-I is **stochastic sampling of `z_t`** (the
  reparameterized draw) instead of Dir-I's deterministic `Ψ_dir`. → so the
  *mechanism* port reduces to: **"Dir-I, but with a stochastic Ψ latent."**

**(Q-L3) Is "stochastic Ψ latent" worth a fire?** This is the only genuinely-new
testable delta L offers over the already-landed Dir-I. And the evidence is
*against* it:
  - §11-B (`verdict_carving_pure_physics_noce`) established that anima physics is
    a *lever on CE-base*, not a substitute. A stochastic latent does not change
    that — it would still need CE.
  - §11-A established the bottleneck is **data-regime**, not architecture. A
    VRNN's stochastic latent is an *architecture* change; §11.3's exclusion table
    already closed "model-capacity / architecture-form" as a bottleneck arm.
  - 2510.05013's curiosity reward (`maximise KL`) is an *exploration* signal for
    an **RL agent acting in an environment** — anima has no environment to act
    in during pretraining. The byte corpus is a fixed dataset; there is no
    "action" whose consequence the forward-model predicts. The actor⇄FM tension
    in 2510.05013 is *closed-loop* (action → new observation → prediction error).
    anima's pretraining loop is *open-loop* (corpus → next-byte). **The defining
    structural feature of VRNN-curiosity — a closed action-perception loop — is
    absent from anima's byte-text pretraining setting.**

### 3.3 The crux verdict

The modality mismatch is **NOT overcome-able as a pretraining substrate**, for a
reason deeper than "different input type":

> VRNN-curiosity is a **closed-loop sensorimotor exploration** algorithm. Its
> sample efficiency comes from (a) a factored compositional task grid and (b) an
> agent that *acts* and observes the *consequence* of its action. anima's GOAL-
> relevant bottleneck (§11.3) lives in **open-loop byte pretraining**, where
> there is no action, no consequence, no factored grid. Porting the VRNN
> *mechanism* to that setting strips away exactly the two features that make it
> work, leaving "Dir-I with a stochastic latent" — a change §11-A's exclusion
> table already predicts is not the bottleneck.

The honest non-over-claim: this does **not** mean the actor⇄FM-tension *idea* is
wrong for anima. It means the *VRNN-curiosity algorithm as published* requires a
closed action-perception loop that anima's **pretraining** does not have. There
*is* one anima setting that is genuinely closed-loop: **live spontaneous
emission** (SPONTANEOUS.tape — anima emits, the user/environment responds, anima
observes). VRNN-curiosity is a *legitimate future candidate for the live
interaction loop* (post-deployment online learning), **not** for the carving
pretraining arc that §1–§12 has been investigating. See §5.

---

## §4 GOAL-legitimacy (confirmed) + closed battery

§12.3 already verdicted L **legitimate** (actor⇄FM tension = Engine A⇄G, not a
bolt-on). This design confirms it and **sharpens it**: L is GOAL-legitimate
*as an interaction-loop learning rule*, and GOAL-*illegitimate-by-mismatch* as a
pretraining substrate (not because it bypasses anima physics, but because the
algorithm's required closed loop is absent from pretraining — a feasibility
failure, not a legitimacy failure).

Closed-form sidecar battery `blue_falsifier_dirL.py` — **B-DIRL-1..5 5/5
sympy/Boolean PASS**, central `blue_falsifier.py` UNCHANGED:

- **B-DIRL-1 CURIOSITY-KL-NONNEGATIVE-CLOSED** — VRNN curiosity =
  `KL(q‖p) ≥ 0 ∀` (Gibbs' inequality, Shannon real-limit), equality iff
  `q ≡ p` (zero information gain = no surprise). Closed: the curiosity signal
  is a bounded-below information measure. f1/f2/f3 SAFE (Shannon/Gibbs).
- **B-DIRL-2 ELBO-DECOMPOSITION-CLOSED** — VRNN ELBO `= E[log p(x|z)] − KL(q‖p)`;
  anima Dir-I `L = CE + λ·L_psi` is the **same two-term form** (reconstruction −
  information term). sympy: the two decompositions are structurally identical
  (negate-and-scale), proving L's mechanism *reduces to* the already-landed
  Dir-I lever. This is the closed proof of §3.2 Q-L2.
- **B-DIRL-3 ACTOR-FM-OPPOSED-SIGN-CLOSED** — actor maximises `KL`, forward-model
  minimises prediction error including `KL`: `∂L_actor/∂KL = +1`,
  `∂L_fm/∂KL = −1` (after the ELBO sign). The opposed signs are the closed
  "productive tension" — and it is the **same restoring-sign structure** as
  TENSION-TRAIN B-TT-2 (`∂ΔW/∂tension = −T·gate ≤ 0`). Closed homomorphism
  Engine A ⇄ Engine G.
- **B-DIRL-4 CLOSED-LOOP-REQUIREMENT-CLOSED** (the feasibility crux, Boolean) —
  VRNN-curiosity requires a closed action-perception map: `action → observation
  → prediction_error → curiosity`. Boolean predicate `is_closed_loop(setting)`.
  Witnesses: `is_closed_loop(robot_self_exploration) = True` (2510.05013);
  `is_closed_loop(byte_pretraining) = False` (fixed corpus, no action, no
  consequence); `is_closed_loop(live_spontaneous_emission) = True` (anima emits →
  environment responds → anima observes). Closed proof that the **pretraining
  arc cannot host L**, but the **live interaction loop can**.
- **B-DIRL-5 COMPOSITIONAL-GRID-CARDINALITY-CLOSED** — 2510.05013's sample
  efficiency needs a factored grid `|A| × |O|` with `|train| / (|A|·|O|) = 33%`.
  anima byte-text has no factored grid: the `<inner>/<voice>` template is a
  2-slot composition, not an `N×M` independent-axis grid (`grid_axes = 2` slots
  but `axis_independence = False` — motivation labels are not observable axes).
  Integer/Boolean closed: the 90%/60-example transfer is **structurally
  unavailable** on byte-text. f1/f2/f3 SAFE (integer cardinality + Boolean).

**B-DIRL-NOTE** (empirical carve-out, B-D-NOTE family, NOT counted 🔵): whether a
*hypothetical* live-interaction VRNN-curiosity loop would actually improve
anima's spontaneous emission is an SGD/online-learning OUTCOME measurable only by
a future deployment-stage fire — this battery proves the *mechanism homomorphism*
and the *feasibility gating* (closed loop required), not an emergence outcome.

g_blue_closed_mandate: 산출물 (design + falsifier) transfer-form 🔵 + 연결부위
(L mechanism ↔ Dir-I lever ↔ TENSION-TRAIN B-TT-2 restoring-sign — ELBO
decomposition byte-level identity) 🔵. f1/f2/f3 hard-fail safe (Shannon/Gibbs +
sympy ∂-sign + Boolean predicate + integer cardinality, NO σ/τ/φ/J₂).
B-IDENTITY-5 무관 (design-only, corpus 미생성).

---

## §5 Verdict — DESIGN-TIER close, fire NOT warranted

**L is GOAL-legitimate but NOT fire-warranted in the carving pretraining arc.**

1. **Modality mismatch is real and decisive** — not "different input type" but
   "VRNN-curiosity is a *closed-loop* exploration algorithm; anima's GOAL
   bottleneck lives in *open-loop* byte pretraining." The two features that make
   2510.05013 work (factored compositional grid + closed action-perception loop)
   are both **structurally absent** from byte-text pretraining (B-DIRL-4,
   B-DIRL-5 closed).
2. **The portable part is already landed** — strip away the closed loop and the
   factored grid, and the VRNN-curiosity mechanism reduces to "Dir-I with a
   stochastic Ψ latent" (B-DIRL-2 closed). Dir-I (`verdict_carving_dirI_psictl_
   tensionsup`) is the strongest carving fire (routing 1/31→3/31). L gives Dir-I
   a *literature name* (variational forward-model ⇄ actor ELBO) — valuable as
   vocabulary, but not a new fire.
3. **§11-A/§11-B already exclude L's fire-able delta** — L-as-pretraining is an
   *architecture* change (RNN backbone + stochastic latent); §11.3's exclusion
   table closed "model-capacity / architecture-form" as a bottleneck arm and
   confirmed **data-regime** as the irreducible bottleneck. A VRNN does not
   touch the data regime.
4. **The honest valuable output is a negative + a redirection**:
   - **negative**: VRNN-curiosity (L) does **not** fit anima's *pretraining* arc
     — the modality mismatch is un-overcome-able there (closed-loop requirement).
   - **redirection**: VRNN-curiosity *is* a legitimate candidate for anima's
     **live spontaneous-emission interaction loop** (SPONTANEOUS.tape Thinker-
     Talker, post-deployment online learning) — the one anima setting that *is*
     genuinely closed-loop (anima emits → environment responds → anima observes).
     This is recorded as a future-candidate, **not** a current fire (the live
     loop itself is Phase B unbuilt; gating a VRNN learning-rule on it is
     premature). B-DIRL-4 `is_closed_loop(live_spontaneous_emission)=True` is the
     closed anchor for this redirection.
5. **No fire.** Per task mandate: "feasibility 막히면 design-tier 로 정직히 마감 —
   그 판정 자체가 valuable (L 이 anima 에 fit 안 됨을 정직 기록)." The carving arc
   does not host L. Spending a GPU fire on "Dir-I with a stochastic latent" would
   be mechanical continuation that §11.3 already predicts is not the bottleneck.

### honest C3

1. §L 는 $0 design + feasibility — fire 0, capability 측정 0. anima-fit 논증은
   *구조 동형* 이지 *실측* 아님 (B-DIRL-NOTE — 실 emergence 는 fire 필요, 그리고
   본 verdict 는 그 fire 가 carving 아닌 live-loop 에 속함을 판정).
2. modality 불일치 = **극복 불가 (pretraining 한정)** — VRNN-curiosity 의 closed
   action-perception loop 가 open-loop byte pretraining 에 없음 (B-DIRL-4 closed).
   "극복 가능?" task 질문의 정직한 답 = **NO (carving arc 에선), conditionally-YES
   (live interaction loop 에선 — 단 그 loop 자체가 미구현)**.
3. L 의 mechanism 은 Dir-I 로 *환원* 됨 (B-DIRL-2 ELBO ≅ CE+λ·L_psi). L 이 주는
   것은 새 fire 가 아니라 Dir-I 에 대한 literature anchor (variational FM⇄actor).
4. GOAL-legitimacy = confirmed (§12.3 carry) — L 은 anima physics 우회 아님
   (actor⇄FM tension = Engine A⇄G). 단 legitimate ≠ feasible: 본 design 이 둘을
   분리 — legitimate-by-homomorphism, infeasible-by-closed-loop-absence.
5. closed = transfer-form + 연결부위만 🔵 (B-DIRL-1..5 sympy/Boolean);
   per-fire OUTCOME 은 EMPIRICAL (B-DIRL-NOTE, B-D-NOTE family — NOT counted).
   over-claim 0 — 본 §L 은 측정도 emergence 도 주장 안 함, feasibility 판정만.
6. negative = valuable — §12.5 candidate-3 의 "modality 불일치 난도 최상" caveat 을
   *판정* 으로 닫음. 13-way arc 의 배제법에 L 을 추가: L (VRNN-curiosity) 도
   carving 병목 해법 아님 — closed-loop 부재로 carving arc 자체에 부적합.
7. f1/f2/f3 + B-IDENTITY-5 전 방향 safe — Shannon/Gibbs + sympy ∂ + Boolean +
   integer cardinality, NO σ/τ/φ/J₂. 외부 paper (2510.05013) 는 그 자체 invariant
   (VRNN ELBO / KL-curiosity) 으로만 인용 — anima lattice 매핑 강제 0.

### Sources

- [Curiosity-Driven Co-Development of Action and Language in Robots Through
  Self-Exploration (arxiv 2510.05013)](https://arxiv.org/html/2510.05013v1) —
  VRNN forward-model ⇄ actor, KL-curiosity, 60-example 90% compositional
  generalization. The headline result is sensorimotor-grid-specific (B-DIRL-5).
- RESEARCH.md §12.2 L + §12.3 GOAL-legitimacy table + §12.5 candidate-3 (the
  caveat this design closes).
- `archive/PHILOSOPHY.tape :: verdict_carving_dirI_psictl_tensionsup` — Dir-I,
  the fire that L's pretraining-port reduces to (B-DIRL-2).
- `archive/PHILOSOPHY.tape :: verdict_carving_scale_decomp` (§11-A) +
  `:: verdict_carving_pure_physics_noce_2026_05_18` (§11-B) — the exclusion-table
  arms that already close L's fire-able delta.
- `HEXAD/TENSION-TRAIN/training/tension_link_step.hexa` (B-TT-2 restoring-sign,
  homomorphic to actor⇄FM opposed sign — B-DIRL-3).
- `HEXAD/CHAT/SPONTANEOUS.tape` — the live closed-loop setting where L is a
  legitimate future candidate (B-DIRL-4 `is_closed_loop=True`).
