---
id: H_1033
slug: split-task-property
title: Is there an identifiable TASK-STRUCTURAL property (the intervention's effect on cause-effect decomposability / modularity) that PREDICTS whether an intervention drives big-Phi DOWN — the split-enabling half that H_1023 found was NOT substrate-general?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · split-mechanism · task-structure · pre-register
source: H_1023 (🔴 SPLIT-TASK-LOCAL — on a generic TPM substrate the big-Phi-DOWN half of the split vanished: big-Phi went UP under redundancy, not DOWN; the redundancy-margin stayed general but the split is a joint property of the two Phi measures × the TASK structure) + H_1017 (redundancy explains the margin) + H_1012 (mirror equivalence proof)
exploration_method: E2 (re-run the two-engine + structural-predictor protocol over a FAMILY of frozen task substrates) + E14 (substrate-native IIT4) + a_scale_honest_scope
verification_method: W2 (pre-registered family + frozen structural predictor + frozen separation threshold · both stdlib engines via the H_1023 mirror chain · WB I_min PID cross-check · mirror equivalence-proof) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-08
since: 2026-06-08
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT
---

# H_1033 — which TASK-STRUCTURAL property predicts the big-Phi-DOWN (split-enabling) half?

## 0. motivation (the H_1023 residual)
H_1023 ruled the redundancy-driven faithful-UP / big-Phi-DOWN split **NOT substrate-general**: on a
generic TPM (coupled-copy Markov) substrate the big-Phi-DOWN half VANISHED — big-Phi went *UP* under
the redundancy intervention (RAISES, contrast +4.42), not DOWN. The Williams-Beer redundancy-margin
(Δred−Δsyn) stayed general (positive, separated from the synergy control), but the *sign of big-Phi*
did not flip the way it does on the planning-control task. So the split is a **joint property of (the
two Phi measures) × (the TASK structure)**. The OPEN question H_1023 left: **WHICH task structural
property makes the big-Phi-DOWN half appear?**

## 1. hypothesis
There is an identifiable, pre-frozen task-structural property that **predicts the sign of the big-Phi
contrast** under the intervention — specifically, the intervention's effect on the **decomposability /
modularity of the system's cause-effect structure**. When an intervention makes the system MORE
decomposable (the minimum-information-partition cut becomes cheaper — the system factors more cleanly
into near-independent parts), big-Phi (which is exactly the cost of the MIP cut, integration that is
irreducible to parts) goes **DOWN**. When the intervention makes the system LESS decomposable (more
globally integrated, the MIP cut becomes costlier), big-Phi goes **UP**. The planning task modularizes
under its redundancy intervention (sub-goal factorization) → big-Phi DOWN; the generic coupled-copy
TPM integrates (one driver floods all units, a single irreducible whole) → big-Phi UP.

## 2. pre-registered FROZEN family, predictor, and threshold (frozen 2026-06-08)

### 2a. FROZEN task-substrate family (n=4 binary, each with a matched independent-noisy-bits baseline)
A pre-frozen family of 5 generative task substrates, each with an explicit, frozen intervention vs the
SAME independent-noisy-bits baseline (the H_1023 `run_base`), so every contrast isolates the channel:

1. **modular-planning** — intervention partitions the 4 units into 2 independent sub-modules {0,1},{2,3},
   each module an internally-coupled noisy pair, the two modules causally decoupled (the modularizing
   analogue of planning sub-goal factorization). Expected: big-Phi DOWN (split-enabling).
2. **coupled-chain** — intervention couples the units in a directed ring 0→1→2→3→0 (each unit a noisy
   copy of its predecessor): integrated but NOT a single shared driver. Intermediate integration.
3. **random-TPM** — intervention = a frozen random dense stochastic channel (each next-bit a noisy
   function of a frozen random subset of current bits): generic, no clean factorization.
4. **xor-parity** — intervention = each unit's next bit is the XOR/parity of the other three (the
   H_1023 synergy control): maximally non-decomposable (pure synergy, every cut is costly).
5. **copy-channel** — intervention = the H_1023 coupled-copy channel (units 1,2,3 are noisy copies of
   a shared driver unit 0): the H_1023 case that made big-Phi go UP (one irreducible whole).

All five reuse the H_1023 `run_base` baseline, the same N_STEPS/N_SEEDS/NOISE, and the same seed schedule.

### 2b. FROZEN structural predictor — Δ-decomposability (DEC)
For an arm (baseline or intervention) compute, from its mirror-built MI matrix `mi` (the H_1004
`build_mi_matrix` reused via the H_1023 chain), the **best-balanced-bipartition normalized cut**:
over all 3 balanced 2|2 bipartitions of the 4 units, the cut weight = sum of cross-partition MI; the
within weight = sum of within-partition MI; **DEC = (within − cross_min) / (within + cross_min + ε)**
where `cross_min` is the cut weight of the cheapest (most-separable) balanced bipartition. DEC is HIGH
when the system factors cleanly (within-MI dominates, the cheapest cut is cheap → decomposable) and LOW
when integration spans the cut. The predictor is **Δ_DEC = DEC(intervention) − DEC(baseline)**: a
POSITIVE Δ_DEC means the intervention made the system MORE decomposable. This is a structural measure
of the cause-effect MI geometry; it is NOT a Phi proxy (Phi numbers come ONLY from the stdlib engine
mirrors, a_phi_iit4_tool). The PID redundancy/synergy totals are also recorded as a secondary cross-check.

### 2c. FROZEN separation rule + threshold
- Label each task **bigΦ-DOWN** iff its big-Phi contrast < −eps (eps=1e-3), else **bigΦ-NOT-DOWN**.
- The predictor SEPARATES the family iff there exists a threshold τ on Δ_DEC such that **every**
  bigΦ-DOWN task has Δ_DEC ≥ τ AND **every** bigΦ-NOT-DOWN task has Δ_DEC < τ (a clean monotone split:
  big-Phi goes DOWN exactly when the intervention raises decomposability past τ). Equivalently the
  rank-separation is PERFECT: min(Δ_DEC over bigΦ-DOWN) > max(Δ_DEC over bigΦ-NOT-DOWN).
- Require at least one task in EACH class (else the family is degenerate and the test is INCONCLUSIVE,
  reported honestly, not scored PASS).

## 3. PASS / FAIL (frozen)
- **PASS = TASK-PROPERTY-PREDICTS-SPLIT** : Δ_DEC perfectly rank-separates the bigΦ-DOWN tasks from the
  bigΦ-NOT-DOWN tasks across the frozen family (a real structural predictor of which task structures
  induce the split-enabling big-Phi-DOWN half). Direction must match the hypothesis (bigΦ-DOWN tasks are
  the MORE-decomposable, higher-Δ_DEC ones).
- **FAIL = NO-TASK-PREDICTOR** : no threshold on Δ_DEC cleanly separates the two classes (the bigΦ-DOWN
  and bigΦ-NOT-DOWN tasks interleave in Δ_DEC), i.e. decomposability does NOT predict the split half
  (closed-negative, a_paper_negative_ok) — the split-enabling property stays unpredictable by this
  pre-registered structural measure.

## 4. method (reuse, no reinvention)
Reuse VERBATIM through the H_1023 import chain: the two stdlib IIT-4.0 engine CPU mirrors (`big_phi` +
`faithful_phi`), the matched binary discretization reads (`binary_seq_to_tpm`, `modal_state`,
`build_mi_matrix`, `faithful_phi_from_mi`, `binary_seq_to_faithful_state`), the H_1012
`prove_mirrors_at_n` equivalence proof (re-proven == stdlib at n=4 AND n=5 BEFORE scoring), the
Williams-Beer (2010) I_min PID (`pid_system`, validated on canonical COPY/XOR), and `run_base`. New code
in this H: only the 4 additional frozen task-channel generators + the frozen Δ_DEC predictor + the
separation test. n=4 toy, 30 seeds per arm, matched baseline.

## 5. honest scope (a_scale_honest_scope, a_toy_scale_recheck)
TOY n=4 — both engines EXACT; big-Phi super-exponential so n=4 is the rung for the full family × 30
seeds. The structural predictor Δ_DEC is exact + deterministic on the mirror-built MI matrix. Both CPU
mirrors RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring. Scale-transfer UNVERIFIED. NOT a forge
binary; $0 CPU-local, no GPU. g5 CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool (REAL stdlib
engines, no proxy).

## 6. measurement
PENDING — see `.verdicts/1033_split_task_property/H_1033.txt` (VERDICT-GATE g73: this section filled
only after the verdict .txt is committed).
