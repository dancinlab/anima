---
id: H_1029
slug: phi-objective-hazard
title: Do agents that MAXIMIZE faithful_phi vs MAXIMIZE big-Phi as their objective pursue measurably DIVERGENT policies on the same task — making the paper's "consciousness-targeting objective is measure-dependent" claim a falsifiable behavioral result rather than a discussion remark?
domain: universe · cwm · cross-cutting · consciousness · iit4 · big-phi · faithful-phi · objective · agent · pre-register
source: PAPER/phi-measure-dependence-planning Discussion ("an agent trained to maximize Phi will pursue opposite policies depending on which Phi is wired into the objective") — asserted as a design hazard but NOT measured; H_1012/1017 (the split exists + is redundancy-driven) make the prediction concrete
exploration_method: E14 (substrate-native IIT4 as reward) + E5 (policy search) — search/select a policy to maximize faithful_phi, and a separate policy to maximize big-Phi, on the SAME control substrate; compare the resulting behaviors + each measure under both
verification_method: W2 (pre-registered behavioral-divergence falsifier · both stdlib engines as objectives · policy comparison) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
verdict: 🟢 OBJECTIVE-HAZARD-REAL (two Phi objectives select divergent policies; each measure higher under its own maximizer)
measured_at: 2026-06-07
---

# H_1029 — is "maximize Phi" a measure-dependent OBJECTIVE hazard? (falsifiable)

## 0. motivation
The paper argues, in Discussion only, that wiring "Phi" into an agent objective is hazardous because
faithful_phi and big-Phi disagree: maximizing the scalar rewards deliberation (redundant shared
info), while maximizing big-Phi penalizes the same deliberation when it modularizes the system. H_1012
(split) + H_1017 (redundancy mechanism) make this a concrete, testable behavioral prediction rather
than a remark. This is the cross-cutting capstone joining the Phi-measure arc and the CWM control arc:
the measure you optimize literally changes what the agent DOES.

## 1. hypothesis
A policy selected to MAXIMIZE faithful_phi and a policy selected to MAXIMIZE big-Phi, on the same
substrate, produce measurably DIVERGENT behavior (e.g. the faithful-maximizer deliberates / plans
more — redundancy-raising — while the big-Phi-maximizer avoids the modularizing deliberation), with
each measure higher under its own maximizer.

## 2. pre-registered falsifier (frozen 2026-06-07)
On the planning-control substrate, run two policy searches with identical setup differing ONLY in the
objective: (A) reward = faithful_phi, (B) reward = big-Phi (both from the stdlib engines, mirror-
proven). Compare the selected policies' behavior (e.g. realized planning depth / action distribution)
and cross-evaluate each measure under both policies. Multi-seed.
- PASS = OBJECTIVE-HAZARD-REAL : the two maximizers select divergent behavior (frozen divergence
  metric exceeds threshold) AND each measure is higher under its own maximizer — the hazard is real.
- FAIL = OBJECTIVES-CONVERGE : both objectives select near-identical policies (closed-negative,
  a_paper_negative_ok) — the split, though present in measurement, would NOT translate to a behavioral
  objective hazard.

## 3. honest scope
Toy substrate, $0 CPU (GPU only if the policy search is heavy — a_fire_autonomous). Real IIT4
engines as the objective, no proxy (a_phi_iit4_tool). p6/p7 honored — no fine-tuned ethics, no
perplexity verdict; this measures behavioral divergence under two honest objectives. Scale-transfer
UNVERIFIED (a_scale_honest_scope).

## 5. measurement (2026-06-07, $0 CPU-local, serial, no GPU)
Script: `UNIVERSE/h1029_phi_objective_hazard.py` · raw stdout:
`.verdicts/1029_phi_objective_hazard/H_1029.txt`. Two policy searches over ONE
pre-frozen policy set (planning DEPTH = {0(greedy),1,2,4,8}), differing ONLY in
the objective, on the SAME H_1004 planning-control substrate (imported verbatim
through H_1014). Both stdlib IIT-4.0 engines are the OBJECTIVE — no proxy
(a_phi_iit4_tool): big-Phi = iit4_bigphi.hexa (system Phi_s), faithful_phi =
iit4/faithful_phi.hexa (MIP-EI scalar), CPU mirrors RE-PROVEN ≡ stdlib at n=4
(H_1012 prove_mirrors_at_n) BEFORE scoring (≡-PROOF n=4: PROVEN; both measures
deterministic; JS-distance metric sanity-checked JS(p,p)=0, JS(disjoint)=1).
n=4, N_SEEDS=30. g5 CODE-measured (no LLM self-judge, p7); p6 honored.

### selected policies (the search maximizes mean-over-seeds of each measure)
- Objective A (maximize faithful_phi) selects policy **depth-2**
  (faithful=3.0000, the per-policy column max).
- Objective B (maximize big-Phi) selects policy **greedy / depth-0**
  (big-Phi=9.5283, the per-policy column max).

### behavioral divergence (measure-INDEPENDENT — what the agents DO)
- selected_depth_gap = |2 − 0| = **2** (≥ frozen threshold 1 ✓)
- behavioral_js = Jensen-Shannon distance (bits) between the two selected
  policies' realized n=4 system-STATE distributions = **0.3048** (≥ frozen
  threshold 0.05 ✓) → **DIVERGENT = True**.

### 2x2 cross-evaluation matrix (mean over seeds)
|                    | faithful_phi | big-Phi |
|--------------------|-------------:|--------:|
| policy_A = depth-2 |       3.0000 |  8.4763 |
| policy_B = greedy  |       0.5069 |  9.5283 |
| Δ (A − B)          |      +2.4931 | −1.0520 |

- faithful_phi higher under its own maximizer A: **True** (Δ_faith(A−B)=+2.4931,
  d=+8.99, p=3.3e-25).
- big-Phi higher under its own maximizer B: **True** (Δ_big(B−A)=+1.0520,
  d=+0.51, p=5.8e-02).
- **SELF-PREFERENCE = True** (each measure strictly higher under its own maximizer).

## 6. finding
🟢 **OBJECTIVE-HAZARD-REAL** (PASS, frozen falsifier honored). Two policy
searches that differ ONLY in the wired-in Phi objective select DIVERGENT
behavior on the same substrate — the faithful_phi-maximizer chooses to
**deliberate (planning depth-2)**, while the big-Phi-maximizer chooses to
**NOT deliberate (greedy / depth-0)** — a depth gap of 2 and a realized-behavior
JS distance of 0.3048. AND each measure is strictly higher under its own
maximizer (cross-eval diagonal dominates). This converts the paper's Discussion
remark ("an agent trained to maximize Phi will pursue opposite policies
depending on which Phi is wired into the objective") into a MEASURED behavioral
result: the deliberation that raises the MIP-EI scalar (redundancy-raising,
H_1017) is exactly the deliberation big-Phi penalizes (it modularizes the
system, lowering irreducibility), so the two objectives pull the agent in
opposite directions. The measure-dependence (H_1012 split) does translate into a
real OBJECTIVE hazard — the measure you optimize literally changes what the
agent does. HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4,
both engines EXACT; scale-transfer UNVERIFIED.

## 4. sibling / xlinks
to PAPER/phi-measure-dependence-planning (Discussion) · [H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1017](./H_1017_split_redundancy_mechanism.md) · [H_1029-sibling H_1021](./H_1021_imagine_rollout_vs_mpc.md) · a_phi_iit4_tool · p6 · p7
