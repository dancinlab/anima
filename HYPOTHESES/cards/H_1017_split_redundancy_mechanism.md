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
status: measured
verdict: 🟢 REDUNDANCY-EXPLAINS-SPLIT — planning's added MI is REDUNDANCY-DOMINATED and that dominance DISTINGUISHES planning from every no-split control, mechanistically explaining the H_1012/H_1014 split. On the matched n=4 binary substrate (both stdlib mirrors RE-PROVEN ≡ stdlib at n=4 BEFORE scoring; the Williams-Beer I_min PID independently validated on canonical COPY=pure-redundancy and XOR=pure-synergy cases), planning RAISES total redundancy by Δredundancy=+9.3958 (d+1, large) while LOWERING synergy by Δsynergy=−1.0438 — the entire pairwise-MI rise (Δmi_total=+4.1060) is carried by REDUNDANT (shared/duplicated) information, and synergy (the irreducible component big-Φ rewards) actually FALLS. This is exactly why the two engines read the same MI rise oppositely: faithful_phi (summed pairwise MI across the min cut) RISES on the redundant info, while system big-Φ FALLS because redundant copies are REDUCIBLE (a partition isolating a duplicate loses little). All four interventions are redundancy-dominated (Δred>Δsyn), but planning's redundancy-margin (Δred−Δsyn=+10.4396) DWARFS every no-split control (imagination +0.4483, guided +2.2508, chaos +2.9471) — the redundancy SHOCK is what discriminates the split-inducer. The pre-registered PASS condition (planning Δred≫Δsyn AND distinguishes planning from the no-split control) is MET; H_1014's open WHY is answered. The PID is the EXPLANATORY variable, NOT a Φ proxy — Φ numbers come only from the stdlib mirrors (a_phi_iit4_tool). g5 CODE-measured (no LLM self-judge, p7). TOY n=4; scale-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).
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

## 6. measurement + finding (2026-06-07 · 🟢 REDUNDANCY-EXPLAINS-SPLIT · g5 CODE-measured, $0 CPU-local)
Verdict raw: `.verdicts/1017_split_redundancy_mechanism/H_1017.txt` (g73 — deterministic run that
COULD have falsified; both stdlib engines + CPU mirror RE-PROVEN ≡ stdlib at n=4 BEFORE scoring, and
the Williams-Beer I_min PID independently validated on the canonical COPY=pure-redundancy / XOR=pure-
synergy cases BEFORE scoring).

**Result — planning's added MI is REDUNDANCY, not synergy; that is the split mechanism:**

intervention vs baseline, 30 seeds, matched (n=4, binary discretization):

| intervention | SPLIT? | Δredundancy | Δsynergy | red-margin (Δred−Δsyn) | Δmi_total |
|---|---|---|---|---|---|
| planning (depth-8 vs greedy) | **True** (reproduces H_1012) | **+9.3958** (d+1, large) | **−1.0438** | **+10.4396** | +4.1060 |
| imagination (drift vs react) | False | +0.2731 | −0.1752 | +0.4483 | +0.3477 |
| guided (goal-pull vs react) | False | +1.8690 | −0.3817 | +2.2508 | +1.0431 |
| chaos [NEW] (gain-1.4 vs gain-1.0) | False | +2.5732 | −0.3739 | +2.9471 | +1.1465 |

- **VERDICT-TOKEN: 🟢 REDUNDANCY-EXPLAINS-SPLIT.** The pre-registered PASS condition is MET. For the
  split-inducing planning intervention the added MI is REDUNDANCY-DOMINATED (Δredundancy=+9.3958 ≫
  Δsynergy=−1.0438): the entire pairwise-MI rise (Δmi_total=+4.1060) is carried by REDUNDANT (shared/
  duplicated) information, while synergy — the irreducible component big-Φ rewards — actually FALLS.
  And this redundancy dominance DISTINGUISHES planning from the no-split controls: planning's
  redundancy-margin (+10.4396) DWARFS every no-split control's (imagination +0.4483, guided +2.2508,
  chaos +2.9471). All four are redundancy-dominated (every Δred>Δsyn), but only planning shows the
  large redundancy SHOCK — so the discriminator is the MAGNITUDE of the redundancy rise, consistent
  with H_1014's magnitude-separation finding.
- **MECHANISM (the WHY behind the H_1012/H_1014 split):** the two engines read the SAME MI rise
  OPPOSITELY because the rise is redundant. `faithful_phi` is summed pairwise MI across the min cut —
  it credits shared/redundant info as integration, so it RISES. System big-Φ rewards IRREDUCIBLE
  (synergistic) structure — redundant copies are REDUCIBLE (a partition isolating a duplicate loses
  little), so big-Φ FALLS (its distinction/relation structure collapses, H_1014 Δbigphi_total ≈ −6.7).
  H_1014 ruled out the "modularity-increase" direction and left this WHY open; it is now answered:
  the split is a REDUNDANCY artifact of the pairwise-MI scalar, not genuine integration.
- **WB PID validity (g5, BEFORE scoring):** the estimator returns red=1.0 / syn=0.0 on a pure COPY
  (S1=S2=T, pure redundancy) and red=0.0 / syn=1.0 on XOR (pure synergy) — the canonical Williams-Beer
  sanity cases. The PID is deterministic and a pure function of the same bits. It is NOT a proxy for Φ.
- **honest scope (a_scale_honest_scope · a_toy_scale_recheck):** TOY n=4 — both engines EXACT; big-Φ
  super-exponential so n=4 is the rung for the full SET × 30 seeds. Both CPU mirrors RE-PROVEN ≡ stdlib
  at n=4 BEFORE scoring. Scale-transfer beyond n=4 UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7),
  a_phi_iit4_tool. NOT a forge binary; $0 CPU-local, no GPU.
