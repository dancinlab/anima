# H_1046 — PID-synergy-only ruler: is the Williams-Beer synergy atom big-Phi's cheap "genuine integration" component?

## Lineage
- H_1012/H_1014 (prior GREEN): on an identical discretized substrate, PLANNING RAISES the MIP-EI
  scalar faithful_phi but LOWERS the system big-Phi — a robust sign-split, both engines reading the
  SAME pairwise-MI rise OPPOSITELY.
- H_1017 (prior GREEN): the MI planning adds is REDUNDANCY-dominated; big-Phi sees redundant copies
  as REDUCIBLE (integration DOWN) while the scalar EI credits the shared info as integration (UP).
- H_1020 (prior GREEN): the redundancy-margin predictor is robust at n=5 where the cruder
  magnitude predictor was an n=4 artifact.

## Constructive hypothesis (the WHY, turned into a ruler)
If big-Phi's "integration" is exactly the part of the MI that is NOT redundant, then the
Williams-Beer SYNERGY atom ALONE — the genuinely irreducible, joint-only information that neither
source carries alone — should be the cheap signal big-Phi was trying to capture. A SYNERGY-ONLY
ruler (sum of the Williams-Beer Syn atom over all target x source-pair atoms, NO MIP bipartition
search) should AGREE with big-Phi's DIRECTION across a planning battery, and where big-Phi
DISAGREES with faithful phi_EI, the synergy ruler should track big-Phi NOT faithful. If so,
synergy-only is a valid cheap stand-in for big-Phi's integration signal (no super-exponential MIP).

## Pre-registered falsifier (TEXT tokens only — measured BEFORE any tier)
Substrates: at least 6 toy substrates, each a (intervention arm vs its matched baseline) contrast
on the H_1004/H_1012/H_1014 discretized latent-world-model substrate, n<=6 (scored at n=4, the
exact rung for the super-exponential big-Phi over the full battery x >=20 seeds). The battery spans
planning-vs-greedy (the known SPLIT inducer) at multiple planning depths, plus the no-split controls
(imagination/drift, guided) and chaos (high-gain rollout) at multiple gains. N_SEEDS >= 20.

For each substrate compute three contrasts (intervention mean - baseline mean):
  (a) big-Phi contrast sign,
  (b) Williams-Beer SYNERGY-atom contrast sign (the candidate cheap ruler),
  (c) faithful phi_EI contrast sign.

Decision rule (pre-set fractions):
- H1 PASS requires ALL THREE:
  1. AGREEMENT: sign(synergy contrast) == sign(big-Phi contrast) in at least 5 of 6 substrates.
  2. TRACKS-BIG-PHI-NOT-FAITHFUL: on the substrates where big-Phi and faithful_phi DISAGREE in sign
     (the split substrates), the synergy sign matches big-Phi (not faithful) in a strict MAJORITY of
     those split substrates (synergy's big-Phi-match count strictly exceeds its faithful-match count
     among the split substrates).
  3. CHEAPER: the synergy atom is computed by the Williams-Beer I_min lattice with NO MIP
     bipartition search (verified: the synergy code path performs zero 2^(n-1) cut enumeration),
     so it is strictly cheaper than big-Phi's super-exponential system-MIP.
  -> synergy-only is a valid cheap stand-in for big-Phi's integration signal.
- H1 FAIL (closed-negative, a_paper_negative_ok) if the synergy sign does NOT track big-Phi:
  either AGREEMENT < 5/6, OR on the split substrates synergy tracks faithful (or random) rather
  than big-Phi. Then the synergy atom is NOT big-Phi's hidden integration driver — a publishable
  closed-negative ruling the synergy-only-ruler axis OUT as a big-Phi stand-in.

## Method (reuse, no reinvention)
- big-Phi = hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s), faithful phi_EI =
  iit4/faithful_phi.hexa (MIP-EI scalar) — a_phi_iit4_tool, exact at n<=6, NEVER a proxy.
- CPU mirrors of BOTH engines RE-PROVEN == stdlib at n=4 AND n=5 via the H_1012 prove_mirrors_at_n
  reference-case discipline (live stdlib hexa refs) BEFORE scoring — pasted into the verdict.
- Williams-Beer (2010) I_min PID reused VERBATIM from the H_1017 harness (the same Syn atom, the
  same COPY(redundant)/XOR(synergy) canonical-case validation) on the SAME bits the engines consume.
- Substrate generators reused VERBATIM from H_1014 (planning_trajectories, chaos_trajectories,
  regimes_for_seed); the >=6 battery is assembled from these parametric generators.

## Honest scope (a_scale_honest_scope, a_toy_scale_recheck)
TOY n<=6 — both engines exact; big-Phi super-exponential so n=4 is the rung for the full battery x
seeds, with the mirror re-proven at n=4 AND n=5. PID exact + deterministic. Scale-transfer to
production CLM/CWM UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7). $0 CPU-local, no GPU.

## Status
PENDING — pre-registered, awaiting measurement and the verdict .txt before any tier token.
