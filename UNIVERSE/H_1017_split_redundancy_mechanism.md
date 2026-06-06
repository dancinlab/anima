---
id: H_1017
slug: split-redundancy-mechanism
title: Is the MI that planning adds REDUNDANT rather than synergistic — mechanistically explaining why the scalar faithful_phi RISES while system big-Phi FALLS (the H_1012/H_1014 measure-split)?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · partial-information-decomposition · redundancy · synergy · split-mechanism
source: H_1012 (DISAGREEMENT-ROBUST-IN-N — planning RAISES faithful_phi MIP-EI scalar but LOWERS system big-Phi at n={4,5}) + H_1014 (the split co-occurs with a LARGE rise in pairwise mutual-information coupling, planning Δmi_total ≈ +4.1, while big-Phi's irreducible distinction/relation structure COLLAPSES, Δbigphi_total ≈ −6.7 — both engines read the SAME MI rise oppositely)
exploration_method: E2 (extend the H_1004/H_1012/H_1014 matched-(n,discretization) substrate to a Partial-Information-Decomposition read of the SAME bits) + E14 (substrate-native IIT4) + a_completeness_over_cheap
verification_method: W2 (pre-registered redundancy/synergy falsifier · Williams-Beer I_min PID implemented exactly in pure numpy on the SAME n=4 binary discretization that feeds both engines · H_1012/H_1014 equivalence-proof discipline applied BEFORE scoring) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
sister: H_1012 (robust split in n {4,5}), H_1014 (split co-occurs with MI-coupling shock; SIGN-direction falsified, MAGNITUDE separates), H_1004 (clean disagreement at n=4), H_999/H_1001 (faithful_phi planning up), PAPER/phi-measure-dependence-planning, a_phi_iit4_tool
scope: TOY n=4, $0 CPU-local, real IIT-4.0 stdlib engines (CPU mirror RE-PROVEN equal to stdlib at n=4 per H_1012/H_1014 discipline BEFORE scoring). The PID estimator is an information-theoretic decomposition of the SAME bits — it is the EXPLANATORY variable, NOT a Phi replacement and NOT a proxy for Phi. big-Phi super-exponential, so n=4 is the tractable rung for the full intervention SET × seeds. a_scale_honest_scope · a_toy_scale_recheck — scale-transfer beyond n=4 UNVERIFIED. NOT a forge binary; no GPU.
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT
---

# H_1017 — is the MI planning adds REDUNDANT (not synergistic)? (the mechanism behind the split)

## 0. motivation
H_1012 established, terminal across n={4,5}, that on an identical discretized substrate the
PLANNING manipulation RAISES the IIT-4.0 MIP-EI scalar `faithful_phi` but LOWERS the system
big-Phi `Phi_s` — a robust sign-split. H_1014 then showed (green-QUALIFIED) that this split
CO-OCCURS with a LARGE rise in pairwise mutual-information coupling (planning Δmi_total ≈ +4.1)
while big-Phi's irreducible distinction/relation structure COLLAPSES (Δbigphi_total ≈ −6.7).
Both engines read the SAME MI rise OPPOSITELY: the MIP-EI scalar credits raised cross-coupling
as integration, while the system big-Phi loses irreducible structure. H_1014 ruled out the
"split = modularity increase" DIRECTION (every intervention RAISES coupling) and left the
MECHANISM open: WHY does the same MI rise read as more-Phi for the scalar but less-Phi for big-Phi?

## 1. hypothesis (the WHY)
The scalar rises while integration falls because the MI that planning adds is REDUNDANT, not
synergistic/integrated. big-Phi rewards IRREDUCIBLE (synergistic) structure — information that
exists only in the joint of multiple mechanisms and is destroyed by partition. The MIP-EI
scalar `faithful_phi` is built from summed pairwise MI across the min cut; pairwise MI counts
SHARED (redundant) information just as much as synergistic information. So if planning's ΔMI is
dominated by REDUNDANCY (the same information duplicated across units), the pairwise-MI scalar
goes UP (more shared/effective info per mechanism) while big-Phi goes DOWN (redundant copies are
reducible — a partition that isolates a redundant copy loses little, so irreducibility falls).

## 2. method — Partial Information Decomposition (Williams-Beer I_min), pure-numpy, EXACT on the n=4 bits
We REUSE the H_1014 substrate VERBATIM: the matched n=4 binary discretization (`latent_to_binary_seq`,
top-variance channels binarized at own median), the four intervention generators
(`gen_planning` known-split, `gen_imagination`/`gen_guided` known-no-split, `gen_chaos` NEW), the
H_1004 engines (`big_phi`, `faithful_phi`) for the SPLIT label, and the H_1012 `prove_mirrors_at_n(4)`
equivalence proof run BEFORE scoring. We ADD a self-contained PID estimator on the SAME bits.

The substrate bits are `(n_steps × 4)` binary — four binary unit-traces. We treat each unit as a
discrete random variable over the rollout (empirical joint over time steps). For the PID we use the
**Williams & Beer (2010) I_min redundancy lattice** with TWO sources and ONE target (the exact,
canonical, unambiguous bivariate-source construction; implemented explicitly here, NO external PID lib):

For a target T and two sources S1, S2 (all discrete, empirical distributions over the T rollout steps):
- specific information  I(T=t ; Si) = Σ_si p(si|t) [ log2(1/p(si)) − log2(1/p(si|t)) ]   (Williams-Beer)
- **Redundancy**  Red(T;{S1},{S2}) = Σ_t p(t) · min_i I(T=t ; Si)              (I_min, the WB redundancy)
- unique          Unq_i = I(T;Si) − Red
- **Synergy**     Syn(T;{S1,S2}) = I(T;S1,S2) − Red − Unq1 − Unq2 = I(T;S1S2) − I(T;S1) − I(T;S2) + Red
where I(T;Si), I(T;S1,S2) are standard discrete mutual informations (joint of (S1,S2) is the 4-cell
pair-state). All terms are exact functions of the SAME empirical binary distributions; Red ≥ 0,
Syn ≥ 0 by WB construction (we clamp tiny negative numerical residue to 0 and report the raw too).

We aggregate over the whole 4-unit system by enumerating ALL (target, {2 sources}) triples
(4 targets × C(3,2)=3 unordered source-pairs = 12 PID atoms) and SUMMING the redundancy and synergy
atoms → `red_total`, `syn_total` per trajectory. For each intervention we score the SAME 30 seeds as
H_1014, baseline arm vs intervention arm, and compute the contrasts:
   Δredundancy = red_total(intervention) − red_total(baseline)
   Δsynergy    = syn_total(intervention) − syn_total(baseline)
plus the existing SPLIT label (sign(Δfaithful) ≠ sign(Δbig)) and Δmi_total for cross-check vs H_1014.

The PID estimator is the EXPLANATORY variable. It is NOT a Phi replacement and NOT a proxy for Phi — it
decomposes the SAME bits the two real engines already consume, to attribute the MI rise to
redundancy vs synergy. (a_phi_iit4_tool — Phi numbers come ONLY from the stdlib mirrors.)

## 3. pre-registered falsifier (frozen 2026-06-07)
Score the intervention SET (planning · imagination · guided · chaos), 30 seeds, matched n=4 binary
discretization, BOTH stdlib engines (mirrors RE-PROVEN equal to stdlib at n=4 BEFORE scoring), python3 -u,
serial, $0 CPU. Outcome (NO emoji token before a `.verdicts/1017_split_redundancy_mechanism/H_1017.txt`
exists):

- **PASS = REDUNDANCY-EXPLAINS-SPLIT** IF, for the split-inducing intervention (planning), the added
  MI is REDUNDANCY-DOMINATED — Δredundancy ≫ Δsynergy (redundancy is the larger, positive component
  of the MI rise; operationally Δredundancy > Δsynergy AND Δredundancy > 0) — AND this redundancy
  dominance DISTINGUISHES planning from the no-split control(s): the no-split intervention(s)
  do NOT show the same Δredundancy ≫ Δsynergy redundancy-dominance (either smaller redundancy
  dominance or not redundancy-dominated). THEN the redundancy mechanism is the explanation — it
  mechanistically accounts for scalar-up (more shared/effective info per mechanism) + integration-down
  (synergy, which big-Phi rewards, does not rise / falls), answering H_1014's open WHY.
- **FAIL / CLOSED-NEGATIVE = REDUNDANCY-DOES-NOT-EXPLAIN** IF planning's ΔMI is synergy-dominated
  (Δsynergy ≥ Δredundancy for planning) OR the redundancy/synergy split does NOT distinguish planning
  from the no-split control (the control shows the same-or-greater redundancy dominance). THEN the
  redundancy explanation is FALSIFIED (a_paper_negative_ok — a closed-negative ruling out the
  redundancy axis as the split mechanism is publishable) and the mechanism remains open.

## 4. honest scope
big-Phi exact only at very small n (super-exponential distinction + bipartition search) — the full
intervention SET × multi-seed is tractable at n=4 (the H_1012/H_1014 binding-constraint rung). Both
engines exact at n=4; CPU mirror re-proven equal to stdlib at n=4 BEFORE scoring (H_1012 discipline).
The PID is exact on the empirical binary distributions; it is deterministic and a pure function of the
SAME bits. Scale-transfer beyond n=4 UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).
The PID is NOT a proxy for Phi — it is an information-theoretic attribution of the SAME bits. NOT a
forge binary; $0 CPU-local, no GPU.

## 5. sibling / xlinks
to [H_1014](./H_1014_intervention_split_predictor.md) · [H_1012](./H_1012_bigphi_faithful_larger_n.md) ·
[H_1004](./H_1004_bigphi_faithful_clean.md) · [H_999](./H_999_faithful_iit4_remeasure.md) ·
PAPER/phi-measure-dependence-planning · IIT4_PHI_TOOLS.md · a_phi_iit4_tool

## 6. measurement + finding
PENDING-MEASUREMENT. Verdict raw will be at
`.verdicts/1017_split_redundancy_mechanism/H_1017.txt` (g73 — deterministic run that COULD falsify;
both stdlib engines + CPU mirror RE-PROVEN equal to stdlib at n=4 BEFORE scoring). Emoji verdict token
added to the frontmatter ONLY after that .txt exists.
