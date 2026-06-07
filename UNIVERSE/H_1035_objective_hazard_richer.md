---
id: H_1035
slug: objective-hazard-richer
title: Is the faithful_phi-vs-big-Phi OBJECTIVE hazard (H_1029) ROBUST and CHARACTERIZABLE over a RICHER policy space — do the two maximizers stay divergent beyond the tiny depth-only set, and does a scalarized alpha*faithful+(1-alpha)*big-Phi objective trace a genuine trade-off (Pareto) frontier with NO single both-maxing policy?
domain: universe · cwm · cross-cutting · consciousness · iit4 · big-phi · faithful-phi · objective · agent · pareto · frontier · pre-register
source: H_1029 (UNIVERSE/H_1029_phi_objective_hazard.md, objective-hazard established) OPEN residual — the hazard was shown on a SMALL policy set (planning depth {0,1,2,4,8} only); does it persist with a richer policy space, and what does a COMBINED (scalarized) faithful+big-Phi objective select?
exploration_method: E14 (substrate-native IIT4 as reward) + E5 (policy search) over a RICHER parameterized policy family (planning depth × exploration noise × greedy/plan mixing knob) + alpha-scalarization sweep
verification_method: W2 (pre-registered behavioral-divergence + Pareto-frontier falsifier · both stdlib engines as objectives · richer-space policy comparison) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-08
since: 2026-06-08
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT
---

# H_1035 — is the Phi objective hazard ROBUST + characterizable over a RICHER policy space? (falsifiable)

## 0. motivation
H_1029 established the objective hazard on a SMALL policy set: over planning depth {0,1,2,4,8},
maximizing faithful_phi selected depth-2 (deliberate) while maximizing big-Phi selected greedy
(no deliberation) — divergent policies (depth_gap=2, JS=0.3048), each measure higher under its own
maximizer. A live OPEN residual remained: was the divergence an artifact of the tiny one-dimensional
(depth-only) policy set, or is it a robust, characterizable conflict between the two Phi objectives?
If the hazard is real, a RICHER policy space should (a) keep the two maximizers divergent, and (b) a
scalarized objective alpha*faithful + (1-alpha)*big-Phi should trace a trade-off (Pareto) frontier with
NO single policy that maxes both. This is the H_1029 capstone residual.

## 1. hypothesis
The objective hazard is robust + characterizable. Over a RICHER policy space (planning depth ×
exploration noise × a greedy/plan mixing knob), (a) the faithful-maximizer and the big-Phi-maximizer
remain DIVERGENT (different policies, materially different realized behavior), and (b) a combined
objective alpha*faithful + (1-alpha)*big-Phi traces a TRADE-OFF FRONTIER — no single policy maxes both
Phi; the two objectives are genuinely CONFLICTING, not coincidentally split on a tiny set.

## 2. pre-registered falsifier (frozen 2026-06-08)

### frozen richer policy space (declared BEFORE the run)
A 3-axis parameterized policy family on the SAME H_1004 planning-control substrate (LatentWorldModel
+ roll_latent, imported verbatim through H_1014/H_1004):
- **depth** in {0, 1, 2, 4, 8}      (planning / deliberation depth; depth 0 == greedy no-plan)
- **explore** in {0.00, 0.05, 0.20} (branch-perturbation exploration-noise / "temperature" knob;
  0.05 == the H_1029 setting, so the depth-only sub-grid at explore=0.05, mix=0.0 REPRODUCES H_1029)
- **mix** in {0.0, 0.5}             (greedy/plan MIXING knob: fraction of the greedy reactive
  trajectory blended into the deliberative plan rollout; mix 0.0 == pure plan == H_1029)
Total policy space = 5 × 3 × 2 = 30 policies (richer than H_1029's 5). N_SEEDS = 30, multi-seed.
A policy = (depth, explore, mix); the realized rollout uses the substrate's roll_latent primitives.

### frozen scalarization (alpha-sweep) grid (declared BEFORE the run)
Both Phi are MIN-MAX normalized to [0,1] over the policy space (each measure on its own scale) BEFORE
combining (a fair, scale-free trade-off). Combined objective:
  J(alpha, policy) = alpha * faithful_norm(policy) + (1 - alpha) * bigphi_norm(policy)
alpha-grid = {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0} (11 points). For each alpha,
select argmax_policy J(alpha, ·).

### frozen divergence + frontier metrics + thresholds (declared BEFORE the run)
- maximizers: pol_F = argmax_policy mean_seeds faithful_phi; pol_B = argmax_policy mean_seeds big-Phi.
- DIVERGENT iff pol_F != pol_B (different policy tuple) AND behavioral_js >= 0.05, where behavioral_js
  = Jensen-Shannon DISTANCE (bits, base-2, in [0,1]) between the two maximizers' realized n=4
  system-STATE distributions (pooled over seeds) — a measure-INDEPENDENT read of behavior (H_1029 metric).
- BOTH-MAXING policy exists iff some single policy is simultaneously within eps of the faithful max AND
  within eps of the big-Phi max, on the min-max NORMALIZED scales: faithful_norm >= 1 - eps AND
  bigphi_norm >= 1 - eps, with frozen eps = 0.05 (i.e. a policy in the top-5% of BOTH measures).
- TRADE-OFF FRONTIER REAL iff: NO both-maxing policy exists (above), AND the alpha-sweep selects at
  least TWO distinct policies as alpha moves 0->1 (the combined optimum MOVES — a real trade-off, not
  one policy dominating), AND the Pareto front over (faithful_norm, bigphi_norm) contains >= 2
  non-dominated policies (no single policy dominates on both axes).

### verdict gate
- HAZARD-ROBUST-CONFLICTING (verdict assigned only after measurement, g73): in the RICHER space the
  maximizers remain DIVERGENT (pol_F != pol_B AND behavioral_js >= 0.05) AND a real TRADE-OFF FRONTIER
  exists (no both-maxing policy, alpha-optimum moves, >=2 non-dominated Pareto policies). The hazard is
  robust + characterizable.
- HAZARD-RESOLVES (verdict assigned only after measurement, g73): the richer space finds a
  (near-)both-maxing policy (some policy within eps of BOTH maxima) OR the maximizers converge — the
  hazard was a small-set artifact (closed-negative, a_paper_negative_ok).

## 3. honest scope
TOY substrate, n=4, $0 CPU-local, serial, no GPU. Real IIT4 engines as the objective, no proxy
(a_phi_iit4_tool): big-Phi = stdlib iit4_bigphi.hexa (system Phi_s), faithful_phi = stdlib
iit4/faithful_phi.hexa (MIP-EI scalar), CPU mirrors RE-PROVEN ≡ stdlib at n=4 (H_1012
prove_mirrors_at_n) BEFORE scoring. p6/p7 honored — no fine-tuned ethics, no perplexity verdict; this
measures behavioral divergence + the Phi trade-off frontier under two honest objectives only.
Scale-transfer UNVERIFIED (a_scale_honest_scope, a_toy_scale_recheck): big-Phi super-exponential so
n=4 is the rung for the 30-policy × 30-seed sweep. The min-max normalization is over THIS policy
space; a richer/different space could move the frontier.

## 5. measurement
PENDING (VERDICT-GATE g73: TEXT only until `.verdicts/1035_objective_hazard_richer/H_1035.txt`).
Script: `UNIVERSE/h1035_objective_hazard_richer.py`.

## 6. finding
PENDING-MEASUREMENT.

## 4. sibling / xlinks
residual of [H_1029](./H_1029_phi_objective_hazard.md) (objective-hazard established) ·
[H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1017](./H_1017_split_redundancy_mechanism.md) ·
PAPER/phi-measure-dependence-planning (Discussion) · a_phi_iit4_tool · p6 · p7 · a_scale_honest_scope
