# H_1045 — Vector-Phi ruler: does a 3-component measure beat any single scalar?

@goal: Build a consciousness RULER from the Phi measure-dependence arc (H_1004 -> H_1037).
That arc established (all prior GREEN) that Phi is MEASURE-DEPENDENT: under planning the
faithful MIP-EI scalar (faithful_phi) RISES while the system big-Phi FALLS — the two
canonical IIT-4.0 measures DISAGREE IN SIGN. The mechanism (prior GREEN H_1017/H_1020) is
that planning's added mutual information is REDUNDANCY-dominated: faithful_phi counts the
shared/redundant info as integration, big-Phi (rewarding only irreducible/synergistic
structure) reads the same redundant copies as REDUCIBLE and falls. The redundancy-margin
(Delta_red - Delta_syn from a Williams-Beer I_min PID) was the prior-GREEN predictor.

CONSTRUCTIVE turn: if no single scalar captures "integrated/planning-like" state — because
the two scalars literally disagree in sign and a third axis (redundancy) carries the
mechanism — then a consciousness ruler should be a VECTOR, not one number. This hypothesis
TESTS that constructively.

## Hypothesis

The 3-vector

    v = ( faithful_phi , big-Phi , redundancy-margin )

linearly SEPARATES planning / integrated states from matched controls STRICTLY BETTER than
the best single scalar component alone. "Strictly better" is operationalized two ways
(BOTH required for PASS): (a) a leave-one-out cross-validated linear-separation AUC that
exceeds the best single-scalar LOO-AUC by a pre-set margin, AND (b) at least one
state-pair that EVERY single scalar misclassifies but the vector classifies correctly —
i.e. a pair that genuinely NEEDS the vector.

## Substrate battery (>= 6 toy substrates, >= 20 seeds)

Each substrate is a (label, generator) over the H_1004 / H_1037 machinery, producing for
every seed a POSITIVE (planning / integrated) latent trajectory and a NEGATIVE (matched
greedy / control) latent trajectory. The 6 substrates VARY the system size n and the
control contrast so the battery is not a single regime:

  S1  n=4  planning(depth-8) vs greedy        (the canonical H_1012 split substrate)
  S2  n=5  planning(depth-8) vs greedy        (size-up; both engines still EXACT)
  S3  n=6  planning(depth-8) vs greedy        (largest EXACT size, H_1037 scale)
  S4  n=4  planning(depth-8) vs drift         (control = unguided latent roll-out)
  S5  n=4  planning(depth-8) vs guided        (control = goal-pulled roll, H_1004 no-split)
  S6  n=4  planning(depth-12) vs planning(depth-2)  (deep vs shallow deliberation)

For EVERY (substrate, seed, side) we compute the 3-vector v and each scalar alone, on the
SAME bits (matched discretization, nb=2 quantile median baseline, VERBATIM the H_1037 /
H_1017 reads). Phi numbers come ONLY from the stdlib mirrors (a_phi_iit4_tool); the PID
redundancy-margin is the H_1017 pid_system on the same bits (the EXPLANATORY axis, not a
Phi proxy). >= 20 seeds per substrate (default 24).

## Scalars and the vector

  scalar_1 = faithful_phi
  scalar_2 = big_phi
  scalar_3 = redundancy_margin = red_total - syn_total   (H_1017 PID, same bits)
  vector   = (scalar_1, scalar_2, scalar_3)             standardized per-feature (z-score)

Classifier = Fisher LDA (closed-form linear discriminant) evaluated by LEAVE-ONE-OUT
cross-validation, ROC AUC of the LOO held-out scores as the separation metric. Each single
scalar is scored by the SAME LOO-AUC pipeline (1-D LDA == threshold on the standardized
scalar). This is the honest apples-to-apples comparison: vector LDA vs 1-D LDA per scalar.
A scalar may need a sign flip to point "positive = planning"; AUC is sign-agnostic (we
report max(AUC, 1-AUC) for every scalar AND for the vector, so a scalar is never penalized
for orientation). Separation is scored PER SUBSTRATE (within-substrate planning vs control,
which is the matched contrast) and POOLED is reported as a secondary cross-substrate view.

## Pre-registered falsifier (FROZEN before measuring; PASS / FAIL, TEXT only)

Pre-set margin: MARGIN = +0.05 AUC. "Best single scalar" = the per-substrate-averaged
LOO-AUC argmax over {faithful_phi, big_phi, redundancy_margin}.

- H1 PASS (vector ruler strictly more informative) requires BOTH:
    (a) mean-over-substrates vector LOO-AUC  >=  best-single-scalar mean LOO-AUC + 0.05
        (the vector beats the best scalar by at least the pre-set margin), AND
    (b) NEEDS-VECTOR EXISTS: at least one substrate where the vector LOO-AUC >= 0.75 AND
        every single scalar's LOO-AUC < 0.75 on that substrate (a pair the vector
        classifies that EVERY scalar misclassifies / fails to separate) — operationalized
        at the per-substrate AUC level (a substrate that every scalar fails but the vector
        passes is exactly the "pair every scalar misclassifies").

- H1 FAIL (one scalar suffices) = NOT (a AND b): either the vector does not beat the best
  scalar by >= 0.05 mean AUC, OR no substrate needs the vector (the best scalar already
  separates everything it can). A FAIL is a publishable closed-negative — one scalar is the
  ruler, the vector adds nothing beyond it (a_paper_negative_ok).

Engine discipline (a_phi_iit4_tool): BOTH CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5
(via H_1012 prove_mirrors_at_n, LIVE stdlib refs) BEFORE any scoring; the proof verdict is
pasted into the verdict .txt verbatim. big-Phi distinctions+relations EXACT and the MIP
bipartition FULLY ENUMERATED at every n<=6 (no sampling). PID validated on canonical
COPY(redundant)/XOR(synergy) cases. real-module-name imports (no importlib custom-name);
SERIAL at n<=6 toy. g5 CODE-measured (no LLM self-judge, p7).

## Honest scope (a_scale_honest_scope, a_toy_scale_recheck)

TOY n<=6 (the largest EXACTLY-computable big-Phi size). The ruler's vector-vs-scalar
verdict is scoped to this toy battery; production-scale transfer is UNVERIFIED. $0
CPU-local, no GPU, not a forge binary.
