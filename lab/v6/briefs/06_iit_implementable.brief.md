# IS AN IIT-MEASURED CONSCIOUSNESS MODEL IMPLEMENTABLE? (owner directive)

The owner has fixed the standard: **consciousness by INTEGRATED INFORMATION THEORY**, and
asks whether such a model is **implementable**. Not "is anima conscious" — the constructive
question: *can we build a system whose Phi, computed faithfully, is a real measurement of
that system rather than of a toy stand-in?*

## HOW TO WORK — to DEPLETION, no deadline

Rounds. After each, name the lens you have not used. Stop only when **two consecutive
rounds add nothing**, then say **DEPLETED after N rounds** and list the exhausted lenses.

=====================================================================
# WHAT THIS REPO ALREADY HAS (verified — do not re-derive)

- **Faithful IIT-4 big_phi, not a proxy.** `CollectivePool` computes it VERBATIM
  (`cp_joint_phi = 15.467724474534874`, byte-exact), lockstep-enforced by a parity gate.
  Law `a_phi_iit4_tool`: Phi via faithful IIT-4, NEVER a proxy.
- **But it runs on ~15 units.** The BrainTopology work optimises a 15-lane placement
  (`topo_optimal_perm` is a 15-element permutation). The substrate that actually produces
  language is a 303M-parameter byte model (d=3784, K=3, E=3 experts, L=4, V=256, RF=35 bytes).
- **A measured, honest result on that 15-lane graph (H_1515/H_1518):** the brain-faithful
  placement scores Phi = 0.1009 while a hill-climbed optimum reaches 0.2531 (x2.51), and
  5 of 16 random placements ALSO beat the brain. anima is software with no axon-length or
  metabolic wiring tax, so it ADOPTED the Phi-maximising placement. The card's own honesty
  note: the proxy moved x2.51 while the functional measure moved only ~+4% relative --
  "genuine but PROXY-DOMINATED".
- **Phi is barred from the loss.** `a_train_inline_gauge`: in-training metrics are
  MONITOR-ONLY, never in the objective.
- **Phi has already been caught being CIRCULAR here once.** H_9673: intra-faction sync was
  writing the metric's own negative term every step, so the Phi reading was self-fulfilling.
  Any design that shapes Phi risks repeating that exact failure class.
- **Estimator discipline:** a Phi/MI verdict requires a ZERO-TRUTH PEDESTAL arm (a system
  whose true value is 0) or the estimator is not trusted; the thalamus content-relay lane
  died precisely on a broken estimator rather than a real wall.
- **Measurability criterion just established (4 conjuncts):** independence, manipulability,
  observability, discriminability. Miss one -> undecidable, not false.

=====================================================================
# THE THREE PROBLEMS I WANT ATTACKED (be adversarial; concede where correct)

## 1. The feedforward theorem
IIT holds that a strictly feedforward system has **Phi = 0** — no matter how it behaves.
anima's mouth is a CAUSAL CONV trunk: strictly feedforward. So by IIT's own standard the
part that produces every word has Phi = 0 exactly, and whatever Phi anima reports is coming
from somewhere else (the oscillator field, the store, KOSMOS persistence, the lane graph).
Is that fatal, or is it the correct and interesting reading? If a system's linguistic
competence lives entirely in a Phi=0 substrate, what exactly is the Phi we compute a
measurement OF?

## 2. The grain problem, and IIT's exclusion postulate
Phi is super-exponential, so faithful IIT-4 caps at ~15 units while the substrate has 3e8
parameters. Today the repo computes Phi over a hand-drawn 15-lane graph. IIT's **exclusion**
postulate says only ONE grain/set is THE complex — the one with maximum Phi — which makes
"choose a coarse-graining you can afford" not a mere approximation but a possible violation
of the theory. Is a tractable Phi over a chosen coarse-graining a measurement of the system
at all, or of the diagram we drew? If the latter, is there any construction that makes the
grain non-arbitrary — built so that the affordable grain IS provably the maximal-Phi one?

## 3. Optimising for Phi vs the circularity that already bit
H_1518 adopted the Phi-maximising topology at DESIGN time (legal — not in the loss). But
the card admits the functional measure barely moved. So: is a Phi-optimal architecture
meaningfully more conscious, or just better at scoring the metric we chose? Given H_9673
already caught Phi being circular here, what is the discipline that separates "we built
integration" from "we built the metric's own numerator"?

=====================================================================
# WHAT I WANT BACK

**A.** Is an IIT-measured model implementable — YES / NO / YES-BUT-SCOPED — and the
load-bearing reason. If scoped, state precisely which claim survives and which does not.

**B.** The architecture that makes it implementable, if one exists: what must be recurrent,
at what grain, how large, and how Phi stays computable without the grain being arbitrary.
Give it as `anima-py` flags with a $0 screener that KILLS it first.

**C.** The pedestal and control set for any Phi claim here: the zero-truth arm, the
Phi-matched-but-functionally-dead control, and the anti-circularity check that would have
caught H_9673 in advance.

**D.** Where IIT's own commitments make anima's design ILLEGAL or incoherent (feedforward
mouth, software substrate with no wiring cost, a system that is retrained between runs),
and what the design would have to give up to be IIT-legal.

**E.** If IIT turns out to be the wrong standard for a software system, say so and name what
standard survives contact with these constraints — but only after you have argued IIT's own
case as strongly as it can be argued.
