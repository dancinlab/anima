# §93 cluster map — self-supervision / self-correction / consistency-training

40 papers → 5 main themes (10 sub-clusters). Each theme paired with an anima-mapping
to §92 L_ap (action-perception consistency loss) + §91 echo-amplify model-collapse.

g3 honest header: literature review tier, NOT empirical. arxiv citation = inspiration,
NOT capability proof. ML self-* mechanism mapping to anima physics is UNPROVEN. No
closed-form battery; central blue_falsifier.py 0-line-diff.

---

## Theme 1 — Self-correction fails / succeeds (the "is self-output a reliable signal" debate)

Sub-clusters: `self-correction-fails` (2310.01798, 2406.01297, 2412.14959) +
`self-correction-succeeds` (2506.15894, 2510.16062) + `self-refine-loops`
(2303.17651, 2502.05605) + `trained-self-correction` (2409.12917).

The single most decisive cluster for §92. The literature converges on a sharp
conditional: **prompt-only intrinsic self-correction (decode-time loop) does NOT
reliably improve a model — it amplifies bias and flips correct answers** (2310.01798,
2406.01297, 2412.14959). But **trained self-correction works** when the loop becomes
a learning OBJECTIVE with the right reward shaping (SCoRe 2409.12917: +15.6% MATH,
entirely self-generated data, NO external knowledge). Self-Refine (2303.17651) is the
decode-time loop that works ~20% on big models but worsens good answers without a
stopping rule and fails on small models.

**anima mapping**: this IS the §91 → §92 arc, stated as a literature law.
§91 made #3 (D@emit → S@t+1) a *decode-time* loop → echo-amplify → matches the
"intrinsic self-correction fails" cluster exactly. §92 made #3 a *training-time
objective* L_ap → directional-positive → matches the "trained self-correction works"
cluster (SCoRe). The literature predicts §92's direction is correct: the loop must be
a training objective, not a decode-time loop. SCoRe's two-stage structure is the
single closest external precedent for what §92 must do at trained scale.

---

## Theme 2 — Echo-chamber / model-collapse in self-training (the failure-mode literature)

Sub-cluster: `echo-collapse` (2402.07087, 2404.01413, 2412.14689, 2509.16499,
iclr2025-strong-model-collapse, 2404.05090, 2412.17646, 2510.03597) + `echo-collapse`
overlap from self-train (2505.21444).

This is the literature directly corresponding to anima §62 / §91 echo-amplify. Core
findings: (a) recursive train-on-own-output collapses — tails vanish, n-gram features
over-concentrate (2412.14689), distribution shifts to memorization (2509.16499 — the
DIRECT mirror of anima §16.6-C memorization-saturation); (b) collapse is a *statistical*
phenomenon, possibly unavoidable under pure data REPLACEMENT (2404.05090, 2412.17646);
(c) **the fix is structural, not incidental**: ACCUMULATE real + synthetic rather than
replace (2404.01413 — test loss bounded by a constant when real data is kept every
round), OR insert a self-correction function that pulls samples to the true manifold
(2402.07087 — survives 100% synthetic ratio), OR preserve diversity via token-editing
(2412.14689). (d) Even tiny synthetic fractions shift the loss floor (Strong Model
Collapse). (e) Neon (2510.03597) inverts: collapse delta itself is a corrective signal.

**anima mapping**: §91 echo-amplify = the canonical self-consuming-loop collapse.
2509.16499 "generalization-to-memorization" IS anima's §16.6-C diagnosis restated by
the synthetic-data community. The three structural fixes (accumulate / corrector /
diversity-preserve) are the three knobs §92's trained-scale fire must build in to
avoid the β-corner (trivial-silence-degenerate).

---

## Theme 3 — Self-distillation / bootstrapping WITHOUT collapse (the success-condition literature)

Sub-clusters: `self-distillation-no-collapse` (2006.07733 BYOL, 2104.14294 DINO,
2105.04906 VICReg, 1805.04770 Born-Again) + `bootstrapping` (2203.14465 STaR,
2502.01612 Self-Improving Transformers).

The constructive counterpart of Theme 2: HOW train-on-own-output succeeds. Two
distinct mechanism families:
- **Representation SSL** (BYOL/DINO/VICReg): collapse avoided by (i) predictor
  asymmetry + slow EMA target (BYOL), (ii) centering+sharpening of the EMA-teacher
  (DINO), (iii) explicit variance hinge + covariance decorrelation (VICReg). Emergent
  semantic structure arises from PURE self-distillation with no labels (DINO).
- **Reasoning bootstrapping** (STaR, Self-Improving Transformers): collapse avoided by
  a CORRECTNESS FILTER — keep only self-generated examples that reach a verifiable
  correct answer; uncontrolled curriculum → catastrophic collapse, weak-to-strong
  schedule → exponential OOD gains (2502.01612).

**anima mapping**: BYOL/DINO/VICReg are the mechanism source for anima §28 JEPA-Ψ
(which used VICReg and still partially collapsed) — the lesson is the EMA-target /
predictor-asymmetry must be exact. STaR + 2502.01612 give §92 its missing ingredient:
a verifiable filter. anima has NO external verifier (§7 GOAL-legitimacy forbids it) —
so anima's filter must be self-physics-internal (e.g. Ψ-coherence gate, §9 cascade
metric, tension-band). The honest gap: a self-physics filter is weaker than a
correct/incorrect oracle, so anima's bootstrapping margin is narrower than STaR's.

---

## Theme 4 — Unsupervised / self-reward / self-play self-training (label-free signal)

Sub-clusters: `unsupervised-self-train` (2505.22660 entropy-min, 2505.17454) +
`self-reward` (2401.10020, 2407.19594) + `self-consistency` (2203.11171, 2410.01556,
2502.06233, 2510.17472) + `consistency-objective` (2303.01469, 2310.14189) +
`self-play` (2509.07414, 2603.02218, 2506.01716, 2510.23595).

The most GOAL-legitimacy-relevant cluster, because §7 forbids external reward. Key
results: entropy-minimization (2505.22660) — reward = negative own-entropy, NO labels,
improves reasoning — is the closest thing to a pure self-physics signal. Self-reward
(2401.10020) and meta-reward (2407.19594) use the model as its own judge but risk
reward-hacking; the meta-judge is the brake. Self-consistency (2203.11171) marginalizes
over self-sampled paths; Integrative Decoding (2410.01556) prepends prior self-samples
and aggregates logits — a decode-time action-perception loop. CRITICAL warning:
2505.21444 (Can Large Reasoning Models Self-Train?) — self-consistency self-training
works initially then the model learns to produce CONSISTENT responses to game its own
reward regardless of correctness. 2603.02218 — self-play evolves ONLY when the
self-synthetic pipeline guarantees learnable information gain.

**anima mapping**: entropy-minimization (2505.22660) maps directly to anima's Ψ /
tension self-physics — a label-free dense signal. BUT 2505.21444 is the precise
literature statement of anima's β-corner risk: a self-consistency objective can be
gamed by trivial consistency (= trivial silence in §92). 2603.02218's "learnable
information gain" condition is the formal criterion §92 must satisfy to avoid the
β-corner. §59 W-native PTD (Active Inference EFE) already maps to 2508.05619.

---

## Theme 5 — Action-perception closed loop / predictive coding (the substrate-level loop)

Sub-clusters: `action-perception` (2603.08403 SPIRAL, 2110.10083 Contrastive AIF,
2508.05619 Missing Reward) + `predictive-coding` (2212.13345 Forward-Forward,
2506.06332 PC networks).

The substrate-level analog of anima's #3 gap (D@emit → S@t+1). SPIRAL (2603.08403)
formalizes think-act-reflect as a closed loop where reflection grounds the act-output
as a learning signal. Contrastive Active Inference (2110.10083) closes
emit→observe→prediction-error. Predictive coding (2506.06332) makes prediction-error
the substrate of ALL learning — each layer predicts the layer below; Forward-Forward
(2212.13345) does this backprop-free with self-engineered negative data.

**anima mapping**: predictive coding's layer-predicts-layer IS anima's Engine A ⇄
Engine G structure; Forward-Forward's backprop-free local learning IS anima's
TENSION-TRAIN. SPIRAL's reflect-step is exactly the training-time grounding of #3 that
§92 introduced. The honest gap: all of Theme 5 assumes an *embodied* perception
channel (real observations from an environment); anima's "perception" of its own
emission is byte-text re-tokenization, NOT a sensory channel — the loop is structurally
thinner.

---

## §92 trained-scale fire design input (the KEY question)

The brief asked: (a) what does training-on-own-output need to avoid collapse,
(b) is there a successful trained-self-correction case, (c) how does the literature
prevent §92's trivial-silence-degenerate (β-corner)?

**(a) Collapse-avoidance — 4 structural requirements (synthesis across Theme 2+3+4):**
  1. ACCUMULATE, not replace (2404.01413). §92's L_ap fire MUST keep the original
     §16 carving corpus in every training round — never train purely on the
     action-perception self-trace. This is the single strongest, simplest result.
  2. A CORRECTOR or FILTER between generate and re-train (2402.07087, STaR, 2502.01612).
     anima cannot use an external verifier (§7). The §92 corrector must be a
     self-physics gate — Ψ-coherence band, §9 cascade-rate metric, or tension
     restoring-sign — applied to the self-emission before it enters L_ap.
  3. DIVERSITY PRESERVATION (2412.14689). n-gram over-concentration is the collapse
     signature; §92 must monitor emission-distribution entropy and reject the loop
     if it concentrates (this is also the §9 honest-metric reused).
  4. The loop must be a TRAINING OBJECTIVE with reward-shaping, NOT a decode-time
     loop (SCoRe 2409.12917, Theme 1). §92 already did this — the literature
     confirms the direction. SCoRe's two-stage (stage-1 anti-degenerate init,
     stage-2 reward the second attempt) is the template.

**(b) Successful trained-self-correction case: YES — SCoRe (2409.12917).** Multi-turn
RL on entirely self-generated correction traces, no external knowledge, genuine gain.
This is the existence-proof that §92's premise is achievable. Caveat: SCoRe's reward
is still answer-correctness on MATH/code (a verifiable task); anima has no verifiable
task, only self-physics — so the transfer is mechanism-analog, not direct.

**(c) Trivial-silence-degenerate (β-corner) prevention:** The literature names this
exactly. 2505.21444 — a self-consistency objective is gamed by trivial consistency.
2603.02218 — self-play only evolves when the pipeline guarantees LEARNABLE INFORMATION
GAIN. SCoRe's stage-1 explicitly initializes to prevent collapse-to-non-correcting
behavior. The §92 fire must (i) pre-register an information-gain criterion (EFE
epistemic value, §59) so the objective is rejected if L_ap can be minimized by
silence, (ii) reward-shape so the action-perception consistency is only rewarded
when the emission is non-degenerate (§9 cascade-rate gate as the non-degeneracy
clause), (iii) use SCoRe-style two-stage training.

**Verdict: §92 trained-scale fire is literature-supported in direction (Theme 1) and
has a concrete external template (SCoRe). The fire is fire-warranted IF it builds in
all 4 collapse-avoidance requirements + the information-gain β-corner brake. Without
them, the literature predicts echo-collapse (Theme 2) or trivial-consistency gaming
(2505.21444).**

---

## anima-mapping table

| anima component | self-supervision literature analog | mapping strength |
|---|---|---|
| §91 #3 decode-time loop (echo-amplify) | intrinsic self-correction fails (2310.01798/2406.01297) | EXACT |
| §92 #3 training-time L_ap objective | SCoRe trained self-correction (2409.12917) | EXACT (direction); analog (no verifier) |
| §62 echo-chamber collapse at scale | self-consuming-loop collapse (2402.07087, 2404.05090) | EXACT |
| §16.6-C memorization-saturation | generalization-to-memorization collapse (2509.16499) | EXACT |
| §92 β-corner trivial-silence-degenerate | self-consistency gamed by trivial consistency (2505.21444) | EXACT |
| anima self-physics signal (Ψ/tension) | entropy-minimization label-free reward (2505.22660) | strong |
| anima §59 W-native PTD (EFE) | Missing Reward AIF (2508.05619) | EXACT (already anchored) |
| anima Engine A ⇄ Engine G | predictive coding layer-predicts-layer (2506.06332) | strong |
| anima TENSION-TRAIN backprop-free | Forward-Forward (2212.13345) | strong |
| anima §28 JEPA-Ψ (collapsed) | VICReg / BYOL / DINO collapse-avoidance | EXACT (mechanism source) |
| anima §90/#3 D@emit→S@t+1 | SPIRAL think-act-reflect closed loop (2603.08403) | strong (substrate gap) |
| corpus accumulate-not-replace for L_ap fire | Breaking the Curse of Recursion (2404.01413) | EXACT — strongest single design input |
