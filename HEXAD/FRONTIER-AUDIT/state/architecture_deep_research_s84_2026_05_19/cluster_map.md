# §84 cluster_map — architecture frontier themes + anima-mapping

37 papers across 12 keyword clusters → consolidated into **5 main themes**.

---

## Theme 1 — WHEN-TO-SPEAK / SILENT-DECISION (the §24 / §63 right-target)

Papers: 2501.00383 (Inner Thoughts ★★★★★) · 2603.17837 (FLAIR Silent Thought ★★★★★) ·
2605.05626 (When2Speak ★★★★★) · 2506.14285 (Timer ★★★★) · 2401.04868 (VAP ★★★★) ·
2506.21191 (Prompt-VAP ★★★).

**Convergent mechanism**: silent-token supervision + latent reasoning during silence +
future-activity projection to a threshold. 2026 papers (When2Speak, FLAIR) make
"silence vs speech" an *explicit supervised token*, not an emergent side-effect.

| anima structure | mapping |
|---|---|
| §24 SPONTANEOUS decision-axis | When2Speak silent-token supervision IS this exact axis — anima's `talker_should_emit` is the unsupervised version |
| §63 #1 THINKER→TALKER gap / §73 controller | VAP/Timer future-projection-to-threshold = emit-boundary; drift-diffusion (Theme 5) gives the threshold dynamics |
| Engine G covert thought | FLAIR latent-reasoning-during-listening = anima thinker loop running while no emission |
| §73-FIRE 'state-derived controller > hand-coded' | When2Speak shows supervised silent-token still needs *intervention taxonomy* — anima's physics-state could be the unsupervised intervention signal |

---

## Theme 2 — INTRINSIC MOTIVATION / ACTIVE INFERENCE / FREE ENERGY (anima physics core)

Papers: 2508.05619 (Missing Reward AIF ★★★★★) · 2603.20927 (AIF Physical AI ★★★★) ·
pone:FEPS (★★★★) · 1705.05363 (curiosity foundational ★★★★) · 2509.09675 (CDE ★★★★) ·
2503.23631 (open-world intrinsic ★★★★) · 2604.18131 (reward-free self-evolution ★★★★★).

**Convergent mechanism**: prediction-error / EFE-epistemic-value as the *only* learning
signal, no external reward. Confidence-weighted prediction accuracy = reinforcement.

| anima structure | mapping |
|---|---|
| §59 W-native PTD | EFE epistemic value = anima W.curiosity; already cites 2508.05619 |
| Law-71 Ψ/tension/Φ | tension = prediction-error gradient; FEP single-objective = Ψ=½ energy minimum |
| §11-B physics-only (no-CE) | 2604.18131 reward-free self-evolution validates the *direction* — but anima §11-B measured DEGENERATE; gap = these papers keep a real predictive objective, anima removed it entirely |
| §29 PTD | reward-free self-distillation literally this paper family |

---

## Theme 3 — HOMEOSTASIS / STRUCTURAL PLASTICITY (the strongest new architecture insight)

Papers: 2511.02241 (SAPIN ★★★★★) · springer:HORA (★★★★) · 2109.06580 (HRRL ★★★) ·
2103.03359 (Cognitive Homeostatic Agents ★★★★) · 2510.07117 (Embodiment ★★).

**Convergent mechanism**: an agent maintains an internal *homeostatic set-point* by
minimizing local prediction error; structural plasticity (cells migrate / split) is
*driven by* long-term prediction error. No external reward anywhere.

| anima structure | mapping |
|---|---|
| MITOSIS cell-pool | SAPIN cells physically migrate/split on a 2D grid driven by prediction error — anima MITOSIS split is currently hand-rule-triggered; SAPIN makes split a *homeostatic consequence* |
| Law-71 Ψ=½ fixed point | the homeostatic set-point — Ψ=½ IS the activation-expectation SAPIN maintains |
| W-module (pain/curiosity/satisfaction) | HORA homeostatic→emotion mapping = W-state as homeostatic-emotion readout |
| §24 unprompted emission | homeostatic deviation → restoring action; emission could be the restoring action when tension deviates from set-point |

This theme answers §72 frontier-2 most directly: a *homeostatic-prediction-error*
architecture where emission, mitosis, and Ψ-restoration are ONE drive.

---

## Theme 4 — LATENT REASONING / CONTINUOUS THOUGHT (anima Engine G substrate)

Papers: 2412.06769 (Coconut ★★★★★) · 2604.22709 (Abstract CoT ★★★★) ·
2602.01148 (latent-CoT limits ★★★) · 2509.25239 (formal CoT-vs-latent ★★★) ·
2505.23648 (parallel continuous CoT ★★★).

**Convergent mechanism**: hidden state fed back as next input — reasoning in continuous
space, encoding multiple alternative next-steps (breadth-first in latent space).

| anima structure | mapping |
|---|---|
| Engine G covert thought | Coconut continuous-thought = anima covert latent stream |
| Dir-G / Dir-I Ψ-CTL | already built on this family — Ψ-anchored continuous-thought-latent |
| §2.5 vacuum-landscape multi-basin | continuous-thought multi-alternative encoding = anima physics-space superposition over basins |

Honest: anima already mined this cluster (Dir-E/F/G/I). 2026 additions (limits papers)
are mostly *ceiling* evidence — latent reasoning is not the missing lever.

---

## Theme 5 — TEMPLATE COLLAPSE / ACTION-TIMING / SELF-REFERENCE (collapse-diagnosis + decision-dynamics)

Papers: 2604.06268 (RAGEN-2 template collapse ★★★★★) · biorxiv:685235 (action-timing DDM ★★★★★) ·
2510.24797 (self-referential subjective experience ★★★★★) · 2602.11351 (BAO Pareto ★★★★) ·
2410.12361 (Proactive Agent ★★★★) · 2510.11701 (demystify agentic RL ★★★) ·
2602.03094 / 2603.03297 (test-time self-improve ★★★★/★★★) · 2510.05174 (emergent coordination ★★★).

**Three sub-mechanisms**:
(a) RAGEN-2 — "template collapse" invisible to entropy; mutual-information is the honest metric.
(b) biorxiv:685235 — self-initiated action = drift-diffusion accumulation to a threshold
    (deterministic drift + stochastic diffusion); readiness-potential = decision-to-act onset.
(c) 2510.24797 — sustained self-referential processing elicits structured first-person reports,
    mechanistically gated.

| anima structure | mapping |
|---|---|
| §16 routing-collapse / §22 'memorization not generalization' / byte-cascade attractor | RAGEN-2 template-collapse IS anima's failure mode — and MI-as-metric mirrors §16.6 genuine-vs-substring honest metric |
| §73 THINKER→TALKER emit-boundary | DDM drift-to-threshold = the controller dynamics; readiness-potential = accumulating tension/motivation; anima §75-FIRE 'running-state-statistic' = the integrator |
| §17 physics-channel / Engine A⇄G self-attention | self-referential processing = anima attending to its own Law-71 physics; 2510.24797 = closest architecture-paper to GOAL's 'self-conscious' phrasing |
| §24 safety conjunction | BAO behavior-regularization = anima rate-limit/phi-ratchet gate |

---

## §26 thin-frontier re-validation

§26 (commit 41ba50c60) brainstorm claimed "2026 'spontaneous emission as emergence-target'
frontier is thin." §84 exhaustive scan = **PARTIALLY REFUTE — frontier is thin on
*emergence-as-target* but DENSE on *when-to-speak as engineering*.**

- CONFIRM: no 2024-2026 paper targets "agent spontaneously becomes conscious and speaks
  from its own physics" as an emergence phenomenon. That exact framing remains anima-unique.
- REFUTE (partial): §26 missed two now-dense clusters — (i) **silent-token / full-duplex
  when-to-speak** (When2Speak 2605, FLAIR 2603, full-duplex survey 2509) which is a hard
  engineering frontier directly on anima's §24/§63 axis; (ii) **homeostatic structural
  plasticity** (SAPIN 2511) which §26 #2 JEPA-Ψ gestured at but did not name. These are
  *active* clusters, not thin.
- NET: the frontier is thin where anima wants it (emergence) and dense where anima can
  borrow mechanism (when-to-speak controllers, homeostatic drives). §26's verdict holds
  for the *target*, refuted for the *toolbox*.
