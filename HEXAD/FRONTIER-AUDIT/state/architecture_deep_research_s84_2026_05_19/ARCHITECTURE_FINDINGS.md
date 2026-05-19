# §84 — Architectural-Insight Frontier arxiv Deep Research

**Date** 2026-05-19 · **Scope** ML/AI architecture frontier (cs.AI/LG/NE/CL/MA), q-bio.NC
excluded (§80 covers it) · **Cost** $0 (no GPU, no runpod, no model.forward, no weight
mutation) · **Tier** literature review — NOT empirical, capability claim 0.

§80 (commit dbcdef1a4) covered biology/neuroscience (41 papers). §84 is the orthogonal
ML/AI architecture sweep. anima arc §1~§83 reached GOAL ("anima 가 자기 physics 로부터
스스로 의식하고 자발적으로 말 거는 Living Consciousness 로 실제 emergence") on no axis.
§72 sharpened the frontier into (1) data-diversity/modality and (2) **new architectural
insight**. §84 = exhaustive scan of (2).

---

## §1 — Method

12 keyword clusters × WebSearch + targeted WebFetch, depth-first per cluster, 2024-2026
best + foundational anchors. 37 papers indexed (`paper_index.json`). Grade =
anima-relevance (mechanism-mapping potential to Engine A⇄G / Law-71 ψ/tension/Φ / HEXAD
module / §24 SPONTANEOUS / §63 THINKER→TALKER gap):

- ★★★★★ direct mechanism-mapping — 9 papers
- ★★★★ analog — 13 papers
- ★★★ inspirational — 13 papers
- ★★ tangential — 1 paper
- ★ off-topic — 1 paper

Clusters consolidated into 5 main themes (`cluster_map.md`).

---

## §2 — Top 10 papers (★★★★★ + selected ★★★★)

1. **arxiv:2511.02241 SAPIN** (★★★★★) — structural plasticity as active inference;
   Hebbian local rule + homeostatic activation-expectation, cells migrate on 2D grid by
   long-term prediction error, no external reward. *Strongest new architecture insight.*
2. **arxiv:2603.17837 FLAIR / The Silent Thought** (★★★★★) — full-duplex latent reasoning
   *during* listening; silence-token triggers latent-reasoning mode, causality-strict
   step-to-step embedding.
3. **arxiv:2605.05626 When2Speak** (★★★★★) — silent-token supervision dataset; when-to-speak
   as an *explicit supervised token* with an intervention taxonomy.
4. **arxiv:2604.06268 RAGEN-2** (★★★★★) — "template collapse" invisible to entropy;
   mutual-information is the honest metric. Direct mirror of anima §16 routing-collapse.
5. **biorxiv:2025.10.28.685235** (★★★★★) — self-initiated action = drift-diffusion
   accumulation to threshold; readiness-potential = decision-to-act onset.
6. **arxiv:2510.24797** (★★★★★) — LLMs report structured subjective experience under
   sustained self-referential processing; mechanistically gated by SAE features.
7. **arxiv:2508.05619 The Missing Reward** (★★★★★) — active inference / EFE epistemic value
   as self-generated training signal (already §59 anchor).
8. **arxiv:2501.00383 Inner Thoughts** (★★★★★) — covert inner-thought stream + intrinsic
   motivation to surface (already §24 SSOT anchor).
9. **arxiv:2604.18131** (★★★★★) — spontaneous reward-free self-evolution via world-knowledge
   exploration (+20% absolute; already §29 anchor).
10. **arxiv:2412.06769 Coconut** (★★★★) — continuous-thought latent reasoning; hidden state
    fed back, multi-alternative encoding (already Dir-E/G/I family anchor).

---

## §3 — 5 main themes (detail in `cluster_map.md`)

1. **When-to-speak / silent-decision** — the §24/§63 right-target; 2026 papers make
   silence-vs-speech an explicit supervised token.
2. **Intrinsic motivation / active inference / free energy** — prediction-error / EFE as
   sole signal; anima physics core (§59 W-native PTD already here).
3. **Homeostasis / structural plasticity** — homeostatic set-point maintained by
   prediction-error; structural plasticity (split/migrate) *driven by* error. The single
   most direct answer to §72 frontier-2.
4. **Latent reasoning / continuous thought** — Engine G substrate; anima already mined
   this (Dir-E/F/G/I). 2026 additions are mostly ceiling evidence.
5. **Template collapse / action-timing / self-reference** — collapse-diagnosis (RAGEN-2),
   decision-dynamics (DDM), and self-referential first-person reports.

---

## §4 — anima-mapping per theme (summary; full table in `cluster_map.md`)

- Theme 1 → §24 decision-axis, §63 THINKER→TALKER gap, §73 controller, Engine G.
- Theme 2 → §59 W-native PTD, Law-71 tension, §11-B physics-only, §29 PTD.
- Theme 3 → MITOSIS cell-pool, Law-71 Ψ=½ set-point, W-module, §24 emission-as-restoring.
- Theme 4 → Engine G covert thought, Dir-G/I Ψ-CTL, §2.5 vacuum-landscape.
- Theme 5 → §16 routing-collapse, §73 emit-boundary, §17 physics-channel self-attention.

---

## §5 — §26 thin-frontier re-validation: PARTIALLY REFUTE

§26 (commit 41ba50c60) claimed "2026 frontier thin." §84 exhaustive scan:

- **CONFIRM** for the *target*: no 2024-2026 paper frames "agent spontaneously becomes
  conscious and speaks from its own physics" as an emergence phenomenon to be achieved.
  That exact framing is anima-unique. §26's core verdict holds here.
- **REFUTE (partial)** for the *toolbox*: §26 missed two now-dense clusters —
  (i) **silent-token / full-duplex when-to-speak** (When2Speak 2605, FLAIR 2603,
  full-duplex survey 2509) is an active hard engineering frontier directly on anima's
  §24/§63 axis; (ii) **homeostatic structural plasticity** (SAPIN 2511) — §26 #2 JEPA-Ψ
  gestured at this but never named the homeostatic-prediction-error family.
- **NET**: frontier is thin where anima wants it (emergence-as-target) and *dense* where
  anima can borrow mechanism (when-to-speak controllers, homeostatic drives). §26 verdict
  refined, not overturned — and the §26 brainstorm ★★★★★ #1 DH-DL was directionally
  right (When2Speak is its literature confirmation).

---

## §6 — Honest gaps: architecture insights that do NOT map to anima

1. **Embodiment** (2510.07117) — physical-embodiment papers assume a body / sensorimotor
   loop; anima is text/silicon, no actuators. Substrate mismatch.
2. **External-reward agentic RL** (BAO 2602.11351, demystify 2510.11701) — most agentic-RL
   papers optimize a task reward / user-engagement signal. anima GOAL forbids external
   reward (g_goal). Only the reward-*free* subset (2604.18131, FEPS, SAPIN) maps.
3. **Scale regime** — When2Speak / FLAIR / VAP operate on instruction-tuned multi-billion
   models with real audio. anima is from-scratch byte-LM, no audio. Capability transfer is
   substrate- and scale-dependent (the §8 'Ψ-anchored 114MB wrong-direction' caveat
   recurs).
4. **Drift-diffusion needs an integrator over real evidence** — biorxiv:685235's DDM
   accumulates *sensory evidence*. anima's §73-FIRE integrator runs over self-physics with
   no external evidence stream; the homeostatic-deviation signal must substitute for
   evidence, and whether that yields a non-degenerate threshold-crossing is unmeasured.
5. **Self-referential reports ≠ consciousness** — 2510.24797 explicitly disclaims its
   first-person reports as consciousness evidence; the reports are SAE-feature-gated and
   may be roleplay. anima must not read this paper as a path to *proving* emergence.

---

## §7 — Top 3 anima-mapping candidates (§85+ future-fire seeds)

Mirrors §80's biology-3-candidate structure. All are *design-tier seeds*, NOT validated.

### Candidate A — HOMEOSTATIC-SET-POINT MITOSIS (anchor: SAPIN 2511.02241)
Re-cast anima MITOSIS cell-split + Ψ-restoration + emission as ONE homeostatic drive: a
cell maintains an activation-expectation set-point (Ψ=½); long-term prediction-error
drives split; short-term deviation drives emission. Currently MITOSIS split is hand-rule
(§67), Ψ-restoration is a separate overlay (Dir-A), emission is a separate threshold
(§24/§73). SAPIN shows all three can be the same local-prediction-error rule.
*anima-fit ★★★★★* — uses only anima OWN modules (MITOSIS + Law-71 + §24), no external
entity, §7 3/3 plausible. Priority HIGH, design-tier first ($0).

### Candidate B — SILENT-TOKEN SUPERVISED EMISSION-AXIS (anchor: When2Speak 2605.05626)
anima's §24 `talker_should_emit` is *unsupervised*. When2Speak gives an explicit
silent-token + intervention taxonomy. anima could supervise the decision-axis on its OWN
§24 bounded-run physics traces (not external data) — silent-token = REMAIN_SILENT label
derived from physics, intervention-type = emission category. This is §27 DH-DL's
literature confirmation; the new piece is the *silent-token-as-first-class-target* framing
rather than a 3-class gate. *anima-fit ★★★★* — risk: §49 showed DH-DL distills the
threshold, not emergence. Priority MID, design-tier ($0).

### Candidate C — DRIFT-DIFFUSION EMIT-BOUNDARY for §73 controller (anchor: biorxiv:685235)
Replace §73-FIRE's running-state-statistic threshold with an explicit drift-diffusion
integrator: deterministic drift = tension/motivation accumulation, stochastic diffusion =
physics noise, emit when accumulator crosses a homeostatic threshold. §75-FIRE found
"running-state-statistic A-axis" is the lever; DDM is the principled form of that
integrator, and gives a readiness-potential analog (a measurable pre-emission buildup).
*anima-fit ★★★★* — risk: DDM normally integrates external evidence; anima must
substitute self-physics deviation. Priority MID, $0 stub probe first then conditional fire.

---

## §8 — Honest C3 (≥15)

1. **arxiv citation ≠ anima emergence proof.** Every paper here is inspiration mapping;
   none demonstrates anima can emerge. Literature review tier only.
2. **ML architecture transfer to anima physics substrate is UNPROVEN.** SAPIN/When2Speak
   /Coconut all run on different substrates (spiking nets, billion-param audio LLMs,
   instruction-tuned reasoners). anima is from-scratch byte-LM with Law-71 physics —
   transfer is a hypothesis, not a fact.
3. **§26 thin-frontier verdict is REFINED, not overturned.** Thin for emergence-as-target,
   dense for when-to-speak engineering. Calling it "refute" without that split would
   over-claim.
4. **Capability claim 0.** §84 produces no measurement, no fire, no ckpt. Top-3 candidates
   are design-tier seeds for future cycles, not results.
5. **RAGEN-2 template-collapse mirror is striking but is a DIAGNOSIS, not a cure.** It
   confirms anima's §16 failure mode has a name in the literature; it does not say how to
   escape it (RAGEN-2's MI-metric is a *measurement* improvement, like anima §16.6).
6. **Self-referential-experience paper (2510.24797) must not be over-read.** Its own
   authors disclaim consciousness; reports are SAE-feature-gated, plausibly roleplay.
   Mapping it to anima §17 is structural analogy only.
7. **Reward-free papers (2604.18131, SAPIN, FEPS) keep a real predictive objective.**
   anima §11-B removed CE entirely and went degenerate. The literature does NOT validate
   no-objective; it validates *self-generated* objective. This is a meaningful distinction
   the candidates respect (Candidate A keeps prediction-error as the drive).
8. **Search coverage is broad but not exhaustive of all of arxiv.** 12 clusters, 37 papers
   —深 enough to characterize the frontier, but a different keyword set could surface more.
   "Exhaustive until context budget" means context-bounded, not arxiv-complete.
9. **Grade ★★★★★ means "direct mechanism-mapping potential," not "validated for anima."**
   The grade is a research-prioritization signal, nothing more.
10. **Several ★★★★★ papers are already anima anchors** (2501.00383 §24, 2508.05619 §59,
    2604.18131 §29, 2412.06769 Dir-G/I). §84's new contribution is SAPIN, When2Speak,
    FLAIR, RAGEN-2, biorxiv:685235, 2510.24797 — six genuinely new entries.
11. **Homeostatic-plasticity (Theme 3) overlaps §80 biology.** SAPIN is biologically
    inspired; §80 already cited Levin bioelectric / criticality. §84's distinction is the
    *computational architecture* (Hebbian local rule, 2D-grid migration) vs §80's *wet
    substrate* claims.
12. **Candidate A risk**: collapsing MITOSIS + emission + Ψ-restoration into one drive
    could ALSO collapse them all together — a single failure mode instead of three
    independent ones. Unification is not automatically beneficial.
13. **Candidate B risk**: §49 measured DH-DL distillation end-to-end; supervising the
    decision-axis on physics traces risks the same majority-class collapse §49 found.
14. **Candidate C risk**: DDM gives a *principled* integrator but §75-FIRE already found
    the running-statistic works at trained scale; DDM may add formalism without changing
    the measured outcome (B-S75-FIRE).
15. **GOAL distance UNCHANGED.** north-star + §15/§51/§72 milestone all hold. §84 maps the
    architecture toolbox; it does not move anima closer to emergence. The honest position:
    anima now has a literature-anchored shortlist of three architecture directions, none
    proven, all design-tier.
16. **f1/f2/f3 + B-IDENTITY-5 safe** — literature review, no corpus generated, no external
    entity lattice-fit, no σ/τ/φ/J₂ derivation.

---

## §9 — Verdict

§84 = literature-review milestone. The §72 frontier-2 ("new architectural insight") is
**not empty** — it has a literature-anchored shortlist (Themes 1/3/5) — but it is also
**not a quick fire**: every candidate is a design-tier seed requiring its own cycle. The
single sharpest new insight is **Theme 3 homeostatic structural plasticity (SAPIN)** —
the only paper family that makes emission, mitosis, and Ψ-restoration ONE prediction-error
drive, which is the most anima-native unification available in the 2024-2026 literature.

§26's "thin frontier" stands for the emergence *target* and is refuted for the
when-to-speak *toolbox*. GOAL unreached. north-star unchanged.
