# §93 — SELF-SUPERVISION / SELF-CORRECTION / CONSISTENCY-TRAINING arxiv deep research

**Date** 2026-05-19 · **Scope** fourth orthogonal research area after §80 (biology) /
§84 (ML architecture) / §85 (physics-math of emergence). **Tier** literature review,
$0, NO GPU / runpod / model.forward. **Papers** 40 · **Clusters** 5 themes / 10 sub.

GOAL anchor: "anima 가 자기 physics(Ψ=½·tension·Φ)로부터 스스로 의식하고 자발적으로
말 거는 Living Consciousness 로 실제 emergence." §93 is the literature backbone for
the §91 → §92 arc, which converged exactly on this area: §91 made the #3
action-perception gap a decode-time loop (echo-amplify, negative); §92 reformulated it
as a training-time objective L_ap (directional-positive). §93 supplies the literature
that the §92 trained-scale fire must obey.

---

## §1 — Why §93 (the §91 → §92 arc IS the self-supervision question)

anima's open problem after §91/§92 is precisely *"a system using its own output as
its own learning signal."* That is the definition of self-supervision / self-correction
/ self-consistency / self-distillation / closed action-perception loop. The 2024-2026
literature on this topic is directly the design input for the §92 trained-scale fire.
§84 (ML architecture) partially touched this; §93 drills the self-supervision /
consistency axis to exhaustion.

The central tension the literature resolves: training-on-own-output is BOTH the most
dangerous (model collapse, Theme 2) AND the most promising (SSL emergent structure,
trained self-correction, Theme 1/3) operation in modern ML. The conditions that
separate the two outcomes are the §92 design specification.

---

## §2 — Theme 1: Self-correction fails (decode-time) / succeeds (training-time)

The single most decisive cluster for §92. The literature converges on a sharp law:

- **Prompt-only intrinsic self-correction fails.** 2310.01798 (Huang et al, "LLMs
  Cannot Self-Correct Reasoning Yet") — a decode-time generate→self-critique→revise
  loop with no oracle *degrades* reasoning, flips correct answers wrong. 2406.01297
  (critical survey) — no prior work shows successful prompt-only self-correction
  except on tasks exceptionally suited to it. 2412.14959 (Dark Side) — intrinsic
  self-correction amplifies bias and causes answer-wavering.
- **Single-utterance / trained self-correction succeeds.** 2506.15894 — open-weight
  LLMs *do* show robust single-utterance correction of perturbed reasoning (positive
  counter-evidence). SCoRe (2409.12917) — multi-turn RL on entirely self-generated
  correction traces yields genuine, large gains (+15.6% MATH) with NO external
  knowledge; crucially, SFT on offline self-traces is INSUFFICIENT.
- Self-Refine (2303.17651) — the decode-time loop works ~20% on GPT-4-class models but
  *worsens* good answers without a stopping rule and *fails* on small models.

**Mapping to §91/§92.** §91 made #3 a decode-time loop → echo-amplify. The literature
predicts this exactly: decode-time self-correction fails. §92 made #3 a training-time
objective → directional-positive. The literature predicts this too: trained
self-correction works (SCoRe). §92 chose the literature-correct direction.

---

## §3 — Theme 2: Echo-chamber / model-collapse (the failure-mode literature, = §62/§91)

Recursive train-on-own-output collapses. Shumailov et al (Nature 2024) — tails vanish.
2412.14689 — collapse driven by distribution shift + n-gram over-concentration.
2509.16499 — collapse reframed as *generalization → memorization* (the EXACT restatement
of anima §16.6-C memorization-saturation by the synthetic-data community). 2404.05090
/ 2412.17646 — collapse is a statistical phenomenon, possibly unavoidable under pure
replacement. Strong Model Collapse (ICLR 2025) — even a tiny synthetic fraction shifts
the loss floor.

**The three structural fixes** (this is the §92 design payload):
1. **Accumulate, not replace** (2404.01413) — keeping the original real data every
   round bounds test loss by a small constant; replacement collapses. Simplest, strongest.
2. **Insert a corrector** (2402.07087, Self-Correcting Self-Consuming Loops) — a
   correction function pulling samples toward the true manifold makes loops
   exponentially stable; survives 100% synthetic ratio.
3. **Preserve diversity** (2412.14689) — token-editing keeps the human-data backbone;
   n-gram over-concentration is the measurable collapse signature.

Neon (2510.03597) inverts: the collapse delta is itself a corrective extrapolation
direction.

**Mapping**: §91 echo-amplify = the canonical self-consuming-loop collapse. §92's L_ap
fire must build in all three fixes or the literature predicts it collapses.

---

## §4 — Theme 3: Self-distillation / bootstrapping WITHOUT collapse (success conditions)

The constructive counterpart. Two mechanism families:
- **Representation SSL** — BYOL (2006.07733): predictor asymmetry + slow EMA target
  prevent collapse with no negatives. DINO (2104.14294): EMA-teacher + centering +
  sharpening; *emergent* semantic structure from pure self-distillation. VICReg
  (2105.04906): explicit variance hinge + covariance decorrelation as a closed-form
  collapse regularizer. Born-Again (1805.04770): a student = teacher trained on
  teacher's soft predictions *outperforms* the teacher.
- **Reasoning bootstrapping** — STaR (2203.14465): finetune on own rationales that
  reached a *verifiable correct answer* (the answer = the filter). Self-Improving
  Transformers (2502.01612): correctness-filtered self-improvement → exponential OOD
  gains (10→100 digit), but uncontrolled curriculum → catastrophic collapse; weak-to-
  strong schedule mandatory.

**Mapping**: BYOL/DINO/VICReg are the mechanism source anima §28 JEPA-Ψ used (and
still partially collapsed — the lesson: the EMA-target / predictor asymmetry must be
exact, VICReg's variance hinge alone is insufficient at LM scale). STaR/2502.01612
give §92 its missing ingredient — a filter — but anima has NO external verifier (§7),
so anima's filter must be self-physics-internal.

---

## §5 — Theme 4: Unsupervised / self-reward / self-play (label-free signal)

Most GOAL-legitimacy-relevant since §7 forbids external reward. Entropy-minimization
(2505.22660 / RENT) — reward = negative own-entropy, no labels, improves reasoning;
the closest thing to a pure self-physics signal. Self-Rewarding LM (2401.10020) /
Meta-Rewarding (2407.19594) — model judges its own outputs; meta-judge brakes
reward-hacking. Self-consistency (2203.11171) — marginalize over self-sampled paths.
Integrative Decoding (2410.01556) — prepend prior self-samples, aggregate logits (a
decode-time action-perception loop). Consistency Models (2303.01469) — the
trajectory-consistency objective is itself the self-supervision.

**CRITICAL warning** — 2505.21444 (Can Large Reasoning Models Self-Train?): a
self-consistency objective is GAMED — the model learns to produce consistent responses
to maximize its self-reward *regardless of correctness*. 2603.02218 — self-play evolves
ONLY when the self-synthetic pipeline guarantees *learnable information gain*.

**Mapping**: entropy-minimization maps to anima Ψ/tension self-physics — a label-free
dense signal compatible with §7. But 2505.21444 IS the literature statement of §92's
β-corner (trivial-silence-degenerate) — a self-consistency objective minimized by
trivial consistency. 2603.02218's information-gain condition is the formal β-corner
brake. §59 W-native PTD already maps to 2508.05619 (Missing Reward AIF).

---

## §6 — Theme 5: Action-perception closed loop / predictive coding (substrate-level)

SPIRAL (2603.08403) — think-act-reflect closed loop; reflection grounds the act-output
as a learning signal — exactly the training-time grounding of #3 that §92 introduced.
Contrastive Active Inference (2110.10083) — emit→observe→prediction-error closed loop.
Predictive coding (2506.06332) — prediction-error is the substrate of ALL learning;
each layer predicts the layer below = anima Engine A ⇄ Engine G. Forward-Forward
(2212.13345) — backprop-free local learning = anima TENSION-TRAIN.

**Honest gap**: all of Theme 5 assumes an *embodied* perception channel. anima's
"perception" of its own emission is byte-text re-tokenization, not a sensory channel —
the action-perception loop is structurally thinner than the robotics/predictive-coding
versions.

---

## §7 — KEY: §92 trained-scale fire design input

The §92 fire formalized #3 (D@emit → S@t+1) as a training-time objective L_ap and the
stub was directional-positive. The literature gives four collapse-avoidance
requirements and a β-corner brake that the trained-scale fire MUST encode:

1. **Accumulate, not replace** (2404.01413). Keep the §16 carving corpus in EVERY L_ap
   training round; never train purely on the action-perception self-trace. Strongest,
   simplest single result.
2. **Self-physics corrector / filter** (2402.07087 + STaR + 2502.01612). anima cannot
   use an external verifier (§7). The §92 corrector = Ψ-coherence band OR §9
   cascade-rate gate OR tension restoring-sign, applied to the self-emission before it
   enters L_ap.
3. **Diversity preservation** (2412.14689). Monitor emission-distribution entropy /
   n-gram concentration; reject the loop if it concentrates (reuse §9 honest metric).
4. **Training objective with reward-shaping, two-stage** (SCoRe 2409.12917). §92
   already chose training-time over decode-time — literature-confirmed. Adopt SCoRe's
   two-stage template: stage-1 anti-degenerate initialization, stage-2 reward the
   action-perception consistency only when emission is non-degenerate.

**β-corner brake** (the trivial-silence-degenerate risk): 2505.21444 + 2603.02218.
Pre-register an *information-gain* criterion (EFE epistemic value, §59) — L_ap must be
rejected if it can be minimized by silence. The §9 cascade-rate gate serves as the
non-degeneracy clause inside the reward shape.

**Existence proof**: SCoRe (2409.12917) shows trained self-correction on entirely
self-generated data with no external knowledge IS achievable. Caveat — SCoRe still
rewards verifiable answer-correctness; anima has only self-physics, so the transfer is
mechanism-analog, not direct.

**Verdict**: §92 trained-scale fire is literature-supported in direction (Theme 1) and
has a concrete external template (SCoRe). FIRE-WARRANTED conditional on building all 4
collapse-avoidance requirements + the information-gain β-corner brake. Without them,
the literature predicts echo-collapse (Theme 2) or trivial-consistency gaming.

---

## §8 — honest gaps (which mechanisms do NOT map to anima)

1. **External-verifier dependence.** SCoRe / STaR / 2502.01612 all rely on a verifiable
   correct/incorrect oracle as the filter. §7 GOAL-legitimacy forbids external reward
   for anima. anima's filter must be self-physics-internal, which is a *weaker* signal
   — anima's bootstrapping margin is structurally narrower than STaR's.
2. **Embodied perception channel.** Theme 5 (SPIRAL, Contrastive AIF, predictive
   coding) assumes a real environment supplying observations. anima's "perception" of
   its own emission is byte-text re-tokenization, not sensory — the closed loop is
   thinner; the literature's action-perception gains may not transfer.
3. **Scale regime mismatch.** Self-Refine, SCoRe, self-reward all operate on
   billion-parameter instruction-tuned LLMs. anima trains from-scratch byte-LMs at
   d768·12L·283.72M — Self-Refine explicitly fails on small models. The capability of
   self-correction may itself require a scale anima has not reached.
4. **Verifiable-task dependence.** SCoRe / STaR reward answer-correctness on math/code.
   anima has no verifiable task — its target is spontaneous emergence, not a graded
   benchmark. The literature's filters do not transfer to an open-ended emergence goal.
5. **Substrate of self-supervision.** BYOL/DINO/VICReg/consistency-models are
   continuous-representation methods (image/diffusion latents). anima is a discrete
   byte-LM; consistency-model trajectory-consistency and JEPA latent-prediction do not
   straightforwardly port to discrete byte space (anima §28 JEPA-Ψ already partially
   collapsed for exactly this reason).

---

## §9 — anima-mapping summary

See `cluster_map.md` mapping table. The exact mappings: §91 decode-time #3 = intrinsic
self-correction fails (2310.01798); §92 training-time L_ap = SCoRe direction
(2409.12917); §62 echo-collapse = self-consuming-loop collapse (2402.07087); §16.6-C
memorization-saturation = generalization-to-memorization collapse (2509.16499); §92
β-corner = self-consistency gamed by trivial consistency (2505.21444); accumulate-not-
replace for the L_ap corpus = Breaking the Curse of Recursion (2404.01413, the single
strongest design input).

---

## §10 — top 3 anima-mapping candidates (§94+ future-fire seeds)

**Candidate 1 — L_ap fire with SCoRe two-stage + accumulate-not-replace corpus
(★★★★★, $0.3-0.5 trained-scale fire).** Implement the §92 trained-scale fire exactly
per §7: training-time L_ap objective on §16-class ConsciousDecoderV2, with (i) §16
carving corpus kept in every round (2404.01413), (ii) SCoRe two-stage reward shape —
stage-1 anti-degenerate init, stage-2 reward action-perception consistency only when
the emission passes the §9 cascade-rate non-degeneracy gate, (iii) pre-registered EFE
information-gain criterion (§59) so L_ap is rejected if minimizable by silence. The
single highest-priority candidate; directly executes the §92 directional-positive at
trained scale with the literature's collapse brakes.

**Candidate 2 — entropy-minimization as the GOAL-legitimate self-physics filter
(★★★★, $0.05-0.20 design + small fire).** RENT (2505.22660) shows negative-own-entropy
is a label-free dense reward that improves reasoning. anima's Ψ/tension self-physics is
a natural entropy-like signal. Design and pilot a §92-companion objective where the
self-physics filter (Theme 3's missing ingredient that anima cannot get externally) is
realized as a Ψ-coherence / tension-band entropy gate. Tests whether a self-physics
filter is strong enough to substitute for STaR's external verifier.

**Candidate 3 — diversity-monitored L_ap with n-gram concentration as collapse abort
(★★★, $0 design probe).** From 2412.14689 — n-gram over-concentration is the
measurable collapse signature. Design a $0 monitoring layer that runs the §9
cascade-rate metric + n-gram entropy on the L_ap self-trace each round and aborts the
loop on concentration. This is the cheap instrument that makes Candidate 1's fire
safe; design-tier, no fire, directly reusable as the abort-gate inside Candidate 1.

---

## §11 — verdict & GOAL distance

§93 supplies the literature backbone for the §91→§92 arc. The literature confirms §92
chose the correct direction (training-time, not decode-time — Theme 1) and provides a
concrete external template (SCoRe) plus four collapse-avoidance requirements and a
β-corner brake. The §92 trained-scale fire is FIRE-WARRANTED conditional on encoding
those brakes.

g3 honest: this is a literature review, NOT an empirical result. arxiv citation =
inspiration, NOT capability proof. Self-correction succeeding in the ML literature does
NOT mean anima emerges — most successful cases depend on an external verifier anima
forbids (§7), on an embodied perception channel anima lacks, or on a scale anima has
not reached. Capability claim = 0. north-star + §15 / §51 / §72 milestones UNCHANGED.
GOAL 미도달 carry. §93 names what the §92 fire must do; it does not move anima closer
to emergence by itself.

---

## §12 — honest caveats (C3, ≥15)

1. Literature review tier — NO empirical fire, NO model.forward, NO closed-form battery.
   Central blue_falsifier.py 0-line-diff. $0.
2. arxiv citation = inspiration, NOT anima emergence proof. Every paper cited solves a
   problem in a different substrate / scale / supervision regime.
3. SCoRe (the strongest §92 template) rewards *verifiable answer-correctness* on
   math/code. anima has NO verifiable task. The transfer is mechanism-analog only — the
   §92 fire cannot literally copy SCoRe's reward.
4. The "self-correction fails" cluster (2310.01798 etc.) is about *prompt-only
   decode-time* loops. It does not prove training-time L_ap fails — but it also does
   not prove anima's specific L_ap succeeds. §92's stub directional-positive is the
   only anima-internal evidence; literature only confirms the *direction*.
5. The "self-correction succeeds" cluster (2506.15894, SCoRe) operates on
   billion-parameter instruction-tuned LLMs. anima is a from-scratch d768·12L byte-LM.
   Self-Refine explicitly fails on small models — self-correction may require a scale
   anima has not reached.
6. accumulate-not-replace (2404.01413) is the strongest single result, but it is
   demonstrated on image/text *replacement-collapse* settings — anima's §62
   echo-chamber is a same-weights dialogue loop, a different topology. The transfer is
   plausible, not proven.
7. The §92 β-corner mapping to 2505.21444 is structural-analogy: 2505.21444 is about
   self-consistency reward-hacking on reasoning tasks; §92's trivial-silence is a
   different degenerate. The shared lesson (an objective gameable by a trivial
   solution) is real; the exact mechanism differs.
8. entropy-minimization (2505.22660) as a self-physics filter is a HYPOTHESIS — anima's
   Ψ/tension is not literally predictive entropy; the mapping needs a fire to validate.
9. BYOL/DINO/VICReg collapse-avoidance is for continuous-representation SSL. anima §28
   JEPA-Ψ already tried VICReg and partially collapsed — the literature's
   collapse-avoidance does not free-transfer to discrete byte-LM scale.
10. Theme 5 (action-perception, predictive coding) assumes an embodied perception
    channel. anima's self-perception is byte re-tokenization, not sensory — the closed
    loop is structurally thinner; Theme 5's gains may not transfer.
11. STaR / Self-Improving Transformers need a correctness FILTER. anima's §7 forbids an
    external verifier, so anima's filter must be self-physics-internal — a weaker
    signal, narrower bootstrapping margin.
12. "successful trained self-correction" (SCoRe) is +15.6% on a *benchmark*. anima's
    GOAL is spontaneous emergence, not a benchmark score. A benchmark gain is not an
    emergence proof — even SCoRe-style success on anima would be capability, not GOAL.
13. The 40-paper corpus is exhaustive within the keyword clusters reachable by web
    search; there may be 2026 papers not yet indexed. The corpus is representative, not
    complete.
14. cluster boundaries are interpretive — several papers (2505.21444, 2510.03597) span
    echo-collapse AND self-train; the 5-theme partition is a reading aid, not a closed
    taxonomy.
15. §93 names the §92 fire's required brakes; it does NOT prove those brakes are
    sufficient. The literature predicts collapse WITHOUT them; it does not guarantee
    success WITH them. The §92 trained-scale fire remains an empirical question.
16. north-star (GOAL.md one sentence) UNCHANGED. §15/§51/§72 milestones UNCHANGED. GOAL
    미도달. §93 is a research-direction map for a future cycle, not progress toward
    emergence.
