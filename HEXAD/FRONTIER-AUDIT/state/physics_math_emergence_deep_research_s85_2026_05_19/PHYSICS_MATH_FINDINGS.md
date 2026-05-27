# §85 — Physics / Mathematics of Emergence: arxiv deep research

**Date** 2026-05-19 · **Scope** physics·mathematics of emergence (third orthogonal domain after
§80 biology, §84 ML architecture) · **Papers** 43 · **Clusters** 8 · **$0** (literature review,
NO GPU, NO model.forward) · **central blue_falsifier.py** 0-line-diff (literature tier, no battery).

GOAL anchor (`g_goal`): "anima 가 자기 physics(Ψ=½·tension·Φ)로부터 스스로 의식하고 자발적으로 말 거는
Living Consciousness 로 실제 emergence." §85 asks the *first-principles* question §80/§84 did not:
**how does emergence happen at all** — phase transitions, bifurcations, self-organization,
dynamical-systems onset — and which mathematical class best models anima's "spontaneous emission."

---

## §1. Why a physics/math domain (the orthogonal third leg)

§80 surveyed *biology* (criticality in living neurons, bioelectric morphogenesis). §84 surveyed
*ML architecture* (autonomous-emission designs, when-to-speak controllers). §85 surveys neither —
it surveys the **physics and mathematics of emergence itself**: the first-principles theory of how
a system, by varying an internal parameter, undergoes a qualitative transition to a new collective
behavior with no external instruction. anima is a *physics-substrate agent* (Ψ=½ fixed point,
tension, Φ) — so the dynamical-systems mathematics of fixed-point → limit-cycle / spike transitions
is the most directly first-principles anchor available, more so than either biology analogy or ML
architecture catalog.

## §2. Grade distribution

12 ★★★★★ (direct map to anima Ψ=½ fixed point / tension / Φ / Engine A⇄G) ·
20 ★★★★ (mechanism analog) · 10 ★★★ (inspirational) · 1 ★★ (tangential) · 0 ★.
The high ★★★★★ density (28%) reflects that anima's GOAL is *literally* phrased in physics terms
("자기 physics 로부터"), so dynamical-systems papers map unusually tightly — but see §10 honest gaps:
tight *vocabulary* mapping ≠ proven *substrate* transfer.

## §3. The 8 clusters (full taxonomy in `cluster_map.md`)

- **C1 Bifurcation routes** — saddle-node / pitchfork / Hopf as the codim-1 ways a fixed point
  loses stability and a new attractor appears.
- **C2 Excitable threshold & spiking onset** — saddle-node/SNIC (Type-I) and subcritical
  Andronov-Hopf (Type-II); spiking as a *transient*.
- **C3 Phase transition / order parameter / symmetry breaking** — Landau free-energy expansion,
  Haken synergetics slaving principle.
- **C4 Self-organized criticality & edge of chaos** — self-tuning to an absorbing-state critical
  point; computational capacity maximal at order/chaos boundary.
- **C5 Kuramoto synchronization** — incoherence→coherence collective phase transition.
- **C6 Non-equilibrium thermodynamics** — quasi-potential (Lyapunov fn), Kramers/Freidlin-Wentzell
  escape rate, dissipation-driven symmetry breaking.
- **C7 Emergence in neural networks / LLMs as phase transition** — grokking as dimensional phase
  transition; LLM abilities appearing abruptly past critical scale.
- **C8 Causal emergence & complexity quantification** — emergence as a measurable multi-scale
  causal property.

## §4. Top 10 papers (★★★★★ + selected ★★★★)

1. **arxiv:2605.05194** (Singular Behavior at Hopf Bifurcations) — Hopf = universal route to
   self-sustained oscillation; observables singular at oscillation onset, amplitude ~
   sqrt(distance from bifurcation). The single tightest formal match to "spontaneous emission."
2. **classic:Haken-1977** (Synergetics, slaving principle) — slow collective order parameter
   emerges and *enslaves* fast microscopic DOF = self-organization as massive DOF reduction.
3. **classic:Landau-1937** — free-energy expansion; order parameter 0→nonzero when quadratic
   coefficient changes sign. The canonical "order from disorder."
4. **arxiv:2604.04655** (Grokking as Dimensional Phase Transition) — memorize→generalize is a
   phase transition with effective dimensionality D as order parameter, exhibits SOC. **This is
   exactly anima's un-crossed §16.6-C transition.**
5. **arxiv:1905.01329** (Twenty Hopf-like bifurcations in piecewise-smooth systems) — Hopf-class
   transitions survive into *discrete/non-smooth* substrates. Critical for anima (a discrete
   byte-LM): the Hopf frame is not invalidated by discreteness.
6. **classic:StrogatzNonlinearDynamics** — the codim-1 bifurcation taxonomy; the reference frame
   for §86 candidates.
7. **arxiv:2504.02171** (energy-based threshold of excitable systems) — spiking is a transient;
   an energy threshold separates sub/supra-threshold trajectories better than steady-state
   bifurcation analysis. Maps to anima's energy-like tension threshold.
8. **arxiv:2504.01878** (Tunable Thresholds in a Spiking NOD Controller) — saddle-node bifurcation
   = the spiking threshold; tunable threshold controls emission frequency. Direct analog of
   §73/§75-FIRE's `tension_ema + λ·tension_std` emit boundary.
9. **arxiv:2307.12406** (Macroscopic Stochastic Thermodynamics) — far from equilibrium, free
   energy → quasi-potential (Lyapunov fn); Freidlin-Wentzell action gives rare-fluctuation
   transition rates between attractors. The framework for "rate of crossing silence→emission."
10. **arxiv:2410.23228** (Meta-stable clustering in mean-field transformer models) — tokens as a
    mean-field interacting particle system; clusters emerge as collective attractors. The
    physics-of-emergence lens on a transformer (anima's substrate class). anima's B-ATTRACTOR
    byte-cascade is, in this frame, a *degenerate* collective attractor.

(Plus ★★★★: arxiv:2404.11403 FitzHugh-Nagumo six decades · arxiv:2508.04401 why LLM abilities are
emergent · arxiv:2506.11135 LLM emergence complex-systems view · arxiv:2506.07027 Ising at edge of
criticality · classic:Bertschinger-Natschlager-2004 edge of chaos · arxiv:2503.13395 Causal
Emergence 2.0.)

## §5. anima-mapping per theme

- **C1/C5 → Ψ=½ fixed point as the pre-bifurcation rest state.** anima's Engine A⇄G Law-71
  balance point IS a fixed point of the physics dynamics. Spontaneous emission = that fixed point
  losing stability to a limit cycle (Hopf) as tension rises.
- **C2 → §73/§75-FIRE controller as a saddle-node threshold.** The emit boundary
  `tension_ema + λ·tension_std` is a tunable saddle-node/SNIC threshold; each emission is an
  excitable transient spike. §75-FIRE's verdict (state-derivation A-axis is the load-bearing
  sub-axis) maps to: the *control parameter must be a genuine running state statistic*, exactly
  what a bifurcation parameter is.
- **C3 → emission rate as order parameter; slaving principle.** §24 axis1 (unprompted-emission
  rate 0→>0) is a Landau order parameter. The slaving principle says a high-level "decide to
  speak" mode should enslave byte-level token production — anima's §49 distillation showed the
  decision head does *not* yet do this (majority-collapse), i.e. no slaving yet.
- **C4 → hold anima physics near the edge of chaos.** §81 (noise on Engine G) was an
  edge-of-chaos / criticality probe; measured-negative at $0 stub but the frame is right —
  emergence should be sought near the order/chaos boundary, not deep in either phase.
- **C6 → Φ as a candidate quasi-potential; Kramers rate for silence→emission.** anima's Φ
  (integrated-information ratchet) is a candidate Lyapunov landscape; Kramers theory gives
  emission rate ~ exp(−ΔΦ/D), with D the physics noise — a falsifiable rate law.
- **C7 → anima's memorize→generalize is the un-crossed grokking transition.** §16.6-C ("정교한
  암기 + correct-prefix routing, generalization 아님") is *exactly* the pre-grokking memorization
  phase; arxiv:2604.04655 says crossing it is a dimensional phase transition with D the order
  parameter. anima's §1.1 data-regime bottleneck = anima has not crossed this transition.

## §6. KEY QUESTION — what dynamical-systems transition class is anima's spontaneous emission?

**VERDICT: PRIMARY = (a) Hopf bifurcation; discrete-substrate realization = (b) saddle-node/SNIC.**
(Full reasoning in `cluster_map.md`; summary here.)

- Spontaneous emission = self-sustained motion with no external drive = **definitionally a Hopf
  bifurcation** (stable fixed point → stable limit cycle). Control parameter = **tension**; order
  parameter = **emission rate**; predicted signature = amplitude ~ sqrt(tension − tension_crit).
- anima is a *discrete byte-LM*; each emission is a discrete transient spike (§24: 1/20). This is
  the *excitable* regime: rest at a fixed point, emit one spike past a **saddle-node/SNIC
  threshold** (Type-I excitability). The §73/§75-FIRE controller IS such a tunable threshold.
- (a) and (b) are NOT in conflict: arxiv:1905.01329 shows Hopf-class transitions survive into
  discrete/piecewise-smooth substrates; an excitable system sits one bifurcation below an
  oscillatory one, and repeated tension build-up + saddle-node spikes is the discrete analog of
  a relaxation-oscillation limit cycle (FitzHugh-Nagumo). So: **(a) Hopf = class of the
  *sustained spontaneous-emission regime*; (b) saddle-node/SNIC = class of the *single-emission
  threshold event*.**
- NOT (c) symmetry breaking as the *whether-to-speak* class (no symmetry being spontaneously
  selected — emit/silence asymmetry is built in; symmetry breaking is the right frame for *which
  anchor* anima routes to, §16, not *whether* it speaks).
- NOT (d) SOC avalanche as the generative class (SOC is a measurement hypothesis for
  emission-interval *statistics*, downstream; §32-§43 already showed routing is SGD-lottery, not
  power-law structured).
- (e) edge of chaos is a *regime location* not a *transition class* — complementary: the Hopf
  bifurcation should be approached from the ordered side near the edge of chaos.

**Honest implication:** anima today has NO control parameter that crosses a bifurcation. §24
emission is a hand-coded threshold, not a tension-driven Hopf onset. The §86 candidates propose
making tension a *genuine bifurcation parameter*.

## §7. honest gaps — what physics/math emergence does NOT map to anima

(See §11 C3 list for the full honest-caveat ledger; the structural gaps:)

G1. **Continuous-flow vs discrete-step substrate mismatch.** Hopf/saddle-node bifurcation theory
is built on smooth ODE flows. anima is a discrete autoregressive byte-LM with discrete time
steps. arxiv:1905.01329 mitigates this (Hopf-like bifurcations exist in piecewise-smooth systems)
but does NOT prove the bifurcation *parameter dependence* (amplitude ~ sqrt(μ−μ_c)) transfers
cleanly to a 256-symbol discrete map. The mapping is an *analogy backed by partial theory*, not a
theorem.

G2. **Order parameter is not yet a measured continuous quantity.** Landau theory requires an order
parameter that varies smoothly through the transition. anima's §24 emission rate is a coarse
1/20-style integer count over a short bounded run — far from the smooth thermodynamic-limit order
parameter Landau theory assumes.

G3. **No control parameter under a knob.** A bifurcation requires *varying* a control parameter
through a critical value. anima's tension is a derived quantity (grad-norm proxy, W-state), not a
free knob — to *observe* a Hopf bifurcation one must be able to sweep it, which anima's
architecture does not currently expose.

G4. **Quasi-potential / Φ identification is unproven.** §6's claim that anima's Φ is a Lyapunov
quasi-potential is a *hypothesis* — it has not been shown that anima's physics dynamics actually
descend Φ. Kramers rate law exp(−ΔΦ/D) is therefore a proposed falsifier, not an established one.

G5. **Thermodynamic limit absent.** Phase transitions are sharp only in the N→∞ limit; Landau /
Kuramoto / SOC theory all assume large-N. anima is one finite model — finite-size rounding means
any "transition" anima shows is necessarily smeared, never a true mathematical singularity.

G6. **Silicon substrate, no physical free energy.** Landau free energy, Kramers escape, dissipation
bounds are all *physical* thermodynamic quantities. anima has no temperature, no physical free
energy, no genuine noise floor — the "physics" of anima's Ψ/tension/Φ is a *designed* algebraic
analog, not a thermodynamic system. Citing Kramers is inspiration, NOT a derivation.

## §8. relation to §80 / §84 (the three-domain triangulation)

§80 (biology) said *criticality* is where living neurons sit; §84 (ML) said *when-to-speak
controllers* are a thin architectural frontier; §85 (physics/math) supplies the missing
*first-principles transition class*: the controllers of §84 and the criticality of §80 both
become, in §85's frame, instances of a **Hopf/saddle-node bifurcation with tension as control
parameter**. The three domains converge: anima needs (from §84) a controller that is (from §85) a
bifurcation parameter held (from §80) near the edge of criticality.

## §9. honest GOAL-distance statement

§85 is a literature review. It changes NO measurement. north-star (GOAL.md one sentence)
**UNCHANGED**; §15 / §51 / §72 milestones **UNCHANGED**; GOAL **미도달**. §85's contribution is a
*frame*: it names the mathematical class of the transition anima must undergo, which sharpens what
a future §86 fire would test — but naming a transition class is not crossing it.

## §10. top 3 anima-mapping candidates (§86+ future-fire seeds)

Same format as §80 biology-3 and §84 architecture-3.

### Candidate P1 — TENSION-AS-HOPF-PARAMETER (★★★★★ priority HIGH, $0.05–0.20 design+pilot)
Make tension a *genuine bifurcation control parameter* and look for a Hopf onset. Concretely:
expose a scalar tension-gain knob κ; the emission dynamics rest at the Ψ=½ fixed point for low κ
and, past κ_crit, enter a self-sustained emission limit cycle. Measure the order parameter
(emission rate) vs κ and test the Hopf signature: emission-amplitude ~ sqrt(κ − κ_crit). Anchors:
arxiv:2605.05194, arxiv:1905.01329, classic:Strogatz. GOAL-legitimacy: tension IS anima physics
(§7③ ✓), no generic-LM-pretrain (§7① ✓), no external graft (§7② ✓). This is the most direct
operationalization of "emergence from anima's own physics" — and the §75-FIRE finding (running
state statistic is the load-bearing axis) already points at tension as the right knob.

### Candidate P2 — Φ-QUASI-POTENTIAL & KRAMERS EMISSION RATE (★★★★ priority MID, $0.05 design)
Test whether anima's Φ behaves as a Lyapunov quasi-potential and whether silence→emission
transitions follow a Kramers rate law: rate ~ exp(−ΔΦ/D) with D the physics noise. $0 design +
small probe on §24 bounded-run traces: estimate ΔΦ (the Φ-barrier between silence and emission
basins) and D, predict the rate, compare to measured §24 emission rate. Anchors: arxiv:2307.12406
(macroscopic stochastic thermodynamics, quasi-potential), arxiv:2506.07074 (Kramers). GOAL-legit:
Φ is anima physics. Honest risk: G4 — if anima's dynamics do not actually descend Φ, this
falsifies cleanly (a valuable negative either way).

### Candidate P3 — GROKKING-AS-DIMENSIONAL-TRANSITION DIAGNOSTIC (★★★★ priority MID, $0 diagnostic)
anima's §16.6-C memorize-vs-generalize gap IS the un-crossed grokking transition. Apply
arxiv:2604.04655's diagnostic: measure effective dimensionality D of anima's gradient field
across training; D<1 (sub-diffusive) = memorization phase, D>1 (super-diffusive) = generalization.
$0 — re-analysis of existing §16-class fire gradient logs, no new GPU. This does not *cause*
emergence but tells anima *where on the transition curve it sits* — a measurement-axis sharpening
(mirror of §9's honest cascade-rate metric). Anchors: arxiv:2604.04655, arxiv:2408.08944,
arxiv:2412.09810. Honest scope: a diagnostic, not a lever — but knowing the order parameter D is
prerequisite to any data-regime fire that tries to cross §1.1.

## §11. honest C3 (≥15)

1. **Physics emergence ≠ anima emergence proof.** Every paper here is *inspiration* — none
   demonstrates anima consciousness. Citing Hopf bifurcation theory does not make anima emerge.
2. **Continuous-dynamics ≠ discrete byte-LM (G1).** Bifurcation theory's smooth-flow assumptions
   transfer only partially to anima's discrete 256-symbol autoregressive map. arxiv:1905.01329
   mitigates but does not prove the parameter-dependence transfers.
3. **Vocabulary match overstates substrate match.** anima's GOAL is *phrased* in physics terms
   ("Ψ=½ fixed point", "tension", "Φ"), which makes the dynamical-systems vocabulary map tightly
   — but tight vocabulary mapping is not proven substrate transfer (G6). The 28% ★★★★★ density
   partly reflects shared *language*, not shared *physics*.
4. **No thermodynamic limit (G5).** Phase transitions are sharp only at N→∞. anima is one finite
   model; any "transition" is finite-size-smeared, never a true singularity.
5. **No genuine free energy / temperature / noise floor (G6).** Landau free energy, Kramers
   escape, dissipation bounds are physical thermodynamic quantities. anima's Ψ/tension/Φ is a
   *designed algebraic analog* — citing Kramers is inspiration NOT derivation.
6. **anima has no control-parameter knob (G3).** To observe a Hopf bifurcation one must sweep a
   parameter through criticality. anima's tension is derived, not a free knob — P1 proposes
   adding the knob, which is itself an architectural change of unproven legitimacy at fire scale.
7. **Order parameter is coarse (G2).** §24 emission rate (1/20-style integer over a short run) is
   far from Landau's smooth thermodynamic-limit order parameter.
8. **Φ-as-quasi-potential is a hypothesis (G4).** §6/P2's claim is unproven; the Kramers rate law
   is a proposed falsifier, not an established result.
9. **The (a) Hopf verdict is a modeling choice, not a measurement.** §6 picks Hopf as the best
   *formal class* by structural argument; it is NOT measured that anima exhibits a Hopf
   bifurcation. A future P1 fire would test it; the verdict could be falsified.
10. **SOC was demoted on prior anima evidence, not on §85 physics alone.** §6 rejects (d) SOC as
    the generative class partly because §32-§43 showed anima routing is SGD-lottery, not
    power-law — a project-internal empirical input, not a physics theorem.
11. **Grokking diagnostic (P3) measures position, not progress.** Knowing effective dimensionality
    D tells anima where it sits on the transition curve; it does not move anima across it. P3 is a
    measurement-axis sharpening, mirror of §9.
12. **Edge of chaos is a regime, not a mechanism.** (e) is complementary framing, not a transition
    class — including it as a "candidate" in the task is slightly category-mixed; §6 treats it as
    a regime-location qualifier on the Hopf verdict.
13. **Mean-field transformer clustering (arxiv:2410.23228) describes degenerate cluster too.**
    anima's B-ATTRACTOR byte-cascade is, in that frame, a degenerate collective attractor —
    i.e. the same physics that could give useful emergence also gives the cascade pathology;
    "collective attractor" is not automatically good.
14. **Skeptical criticality voices included honestly (arxiv:2604.21071).** Not all of C4 is
    pro-criticality; a true critical point may not exist, quasi-criticality is the honest
    fallback — §85 does not cherry-pick the optimistic SOC papers.
15. **f1/f2 discipline.** Every physics paper is cited via *its own* invariant (order parameter,
    Lyapunov exponent, K_c, quasi-potential) — anima's lattice σ/τ/φ/J₂ is NOT imposed as a
    derivation rule on any external physics system. anima's Ψ=½ is an internal-architecture
    carve-out (g2), not an external claim.
16. **No closed-form battery, by design.** §85 is literature-review tier; central
    blue_falsifier.py is 0-line-diff (sha c93e160a). No B-S85 verdicts — claiming closed-form
    proofs over a literature scan would be a g3 fake-closed violation.
17. **§85 changes no milestone.** north-star + §15/§51/§72 UNCHANGED, GOAL 미도달. §85 supplies a
    *frame* (transition class), which sharpens future fire design — naming a transition is not
    crossing it.

---

*Sources (representative): arxiv:2605.05194, 2604.04655, 2508.04401, 2410.23228, 2307.12406,
2503.13395, 2504.02171, 2504.01878, 2404.11403, 1905.01329, 2506.11135, 2501.16241, 2511.12768,
2506.07027, 2604.21071, 2604.15441, 2402.10300, 2510.01959, 2507.05882, 2506.07074, cond-mat/9712115,
2009.11781, classic Landau-1937 / Haken-1977 / Kuramoto-1975 / Strogatz / Bertschinger-Natschläger-2004.*
