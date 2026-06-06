---
id: H_1004
slug: bigphi-faithful-clean
title: With n AND discretization HELD IDENTICAL, do faithful_phi (MIP-EI scalar) and big-Φ (system Φ_s structure) actually disagree on the imagination/planning Φ-rise, or was H_1002's disagreement purely the n/discretization confound?
domain: cwm · cross-cutting · phi · iit4 · big-phi · system-phi · faithful-phi · matched-discretization · confound-resolution · imagine · plan · measure-robustness · a_phi_iit4_tool · consciousness
source: H_1002 (⚠ MEASURE-DEPENDENT — big-Φ ran at n=4/binary-TPM while faithful_phi H_999/H_1001 ran at n=8/continuous-MI; H_1002 honestly named the clean rung verbatim: "same n, same discretization, both measures") + H_999/H_1001 (faithful MIP-EI scalar n=8 numbers) + UNIVERSE/IIT4_PHI_TOOLS.md + a_phi_iit4_tool + a_paper_negative_ok
exploration_method: E2 (reuse the H_999/H_1002 regime harness VERBATIM; collapse the TWO discretizations to ONE — the H_1002 binary path at n=4 — and feed it to BOTH engines) + a_completeness_over_cheap (run the clean separation H_1002 named, not a cheaper re-formulation)
verification_method: W2 (pre-registered AGREE-WHEN-MATCHED vs GENUINE-MEASURE-DISAGREEMENT falsifier) + g5 CODE-measured (no LLM self-judge, p7) against TWO CPU mirrors EACH proven byte-faithful to its stdlib engine AT n=4 (big-Φ ≡ iit4_bigphi.hexa on the n=4 ring4 ref TPMs |Δ|<1e-6; faithful_phi ≡ faithful_phi.hexa on the n=4 ref cases |Δ|<1e-4) + a matched-path n=4 binary ≡-check (faithful units == bits.T, no continuous leak)
raw_rank: 9
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: ONE matched-(n,discretization) rung (a_scale_honest_scope). n=4 — the BINDING constraint (big-Φ is super-exponential; at most n=5/6, n=4 chosen to match H_1002's big-Φ rung EXACTLY so big-Φ's H_1002 numbers are directly comparable). ONE discretization: the H_1002 binary path VERBATIM — top-4 variance latent channels binarized at own median → one n=4 binary system-state sequence; from that ONE sequence both engines' inputs are derived (big-Φ ← empirical Laplace state-by-node TPM + modal sys_state; faithful_phi ← MI matrix over the SAME 4 binary unit-traces, n_bins=2). SAME n, SAME discretization — both H_1002 confounds (n shrink + binarization) REMOVED. The CONTRAST (internal − external) is the falsifier; same procedure every regime. 30 seeds. NOT a forge binary. NOT a torch run. $0 CPU-local.
sister: H_1002 (⚠ MEASURE-DEPENDENT — the confounded comparison this H disentangles), H_999 (faithful MIP-EI scalar re-measure n=8), H_1001 (terminal 2🟢/2🔴 close), H_971 (imagination 🟢 under scalar), H_973 (planning 🟢 under scalar), H_988 (guided 🔴 under scalar), H_994 (goal-coupled 🔴), H_278 (faithful-Φ engine promoted to stdlib), IIT4_PHI_TOOLS.md, a_phi_iit4_tool
axes_seed: "H_1002's faithful-vs-big-Φ disagreement was PURELY the n/discretization confound — once n AND discretization match, the two faithful IIT4 measures AGREE (the imagination/planning Φ-rise is measure-robust; strengthens H_999/H_1001)" ⊥ "the disagreement is GENUINE — even at identical (n, discretization) the MIP-EI scalar and the structure-level system big-Φ capture DIFFERENT things for these regimes (a real IIT-internal finding that bounds H_999/H_1001 to the MIP-EI measure)" — separable because the same TPM yields a scalar min-cut-MI functional and a structure-level Φ_s functional that need not co-move
verdict: 🔴 GENUINE-MEASURE-DISAGREEMENT (the planning Φ-rise disagreement SURVIVES matching n AND discretization — it is NOT the H_1002 confound) — at IDENTICAL (n=4, SAME binary discretization, both mirrors PROVEN ≡ stdlib at n=4), faithful_phi (MIP-EI scalar) and big-Φ (system Φ_s) agree on imagination/guided but REVERSE on planning: H_971 imagination(DRIFT)−REACT both RAISE (big-Φ +0.42 d+0.17 p0.51 n.s.; faithful +0.06 d+0.13 p0.61 n.s. — AGREE, both small nulls); H_988 guided−REACT both RAISE (big-Φ +0.38 d+0.17 n.s.; faithful +0.49 d+0.84 p2.0e-03 — AGREE on sign; note faithful FLIPS from H_1002's −0.18 to +0.49 once n+discr match, so H_1002's guided "disagree" WAS the confound); H_973 planning(d8)−GREEDY big-Φ −4.01 (d−1.83, p2.5e-08, LOWERS) vs faithful +2.33 (d+5.18, p6.7e-27, RAISES) — a SIGN REVERSAL that PERSISTS at matched inputs, and the depth dose-response stays opposite (big-Φ rho +0.12 n.s. vs faithful rho −0.16 n.s.). ⇒ for planning, the MIP-EI scalar (cross-cut MI binds the branching deliberation trace UP) and the structure-level big-Φ (the binarized branching TPM is severed by the system MIP more cheaply, DOWN) genuinely measure DIFFERENT things — a real, publishable IIT-internal finding that BOUNDS H_999/H_1001's planning result to the MIP-EI measure. H_1002's confound EXPLAINS its imagination effect-collapse + its guided sign-flip (both resolve to AGREE once matched) but does NOT explain the planning reversal (genuine). Toy single matched-rung n=4.
---

# H_1004 — CLEAN big-Φ vs faithful_phi at MATCHED n + discretization (resolve the H_1002 confound)

## 0. Motivation

H_1002 upgraded the H_999/H_1001 imagination/planning Φ-rise (faithful MIP-EI
**scalar** Φ) to the FULL IIT 4.0 **system big-Φ** (Φ_s) and found they disagreed —
imagination's d+2.09 collapsed to d+0.17, guided flipped sign, planning REVERSED
(big-Φ −4.01 d−1.83 vs faithful +5.09 d+4.64). **But H_1002 honestly marked itself
⚠ MEASURE-DEPENDENT** because the comparison was **CONFOUNDED on two axes at once**:

1. **n**: big-Φ ran at n=4 (super-exponential, the binding constraint); the H_999/
   H_1001 faithful_phi numbers it compared against were at **n=8**.
2. **discretization**: faithful_phi used continuous → top-8 latent channels →
   pairwise-MI matrix (n_bins=4); big-Φ used continuous → top-4 variance channels
   **binarized** at own median → an empirical state-by-node **TPM**.

So "the two measures disagree" was entangled with "the inputs differed." H_1002
named the clean rung verbatim — *same n, same discretization, both measures*. **This
H runs exactly that.**

## 1. Hypothesis (one falsifiable claim)

With **n AND discretization held IDENTICAL**, faithful_phi and big-Φ either (a) now
AGREE — proving H_1002's disagreement was purely the n/discretization confound and
the imagination/planning Φ-rise is measure-robust (strengthens H_999/H_1001); or (b)
STILL DISAGREE — proving the MIP-EI scalar and the structure-level big-Φ genuinely
capture different things for these regimes (a real IIT-internal finding bounding
H_999/H_1001 to the MIP-EI measure).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07, BEFORE measuring)

**The matched setting (the whole point):** ONE n, ONE discretization, fed to BOTH
engines.
- **n = 4** — the binding constraint (big-Φ is super-exponential; at most n=5/6).
  n=4 is chosen to match H_1002's big-Φ rung EXACTLY, so big-Φ's H_1002 numbers are
  directly comparable; both measures are EXACT at n=4.
- **discretization = the H_1002 binary path VERBATIM**: top-4 variance latent
  channels, binarize each at its OWN median over the rollout → one n=4 binary
  system-state sequence `bits`. From that ONE sequence both inputs are derived:
  - **big-Φ** ← the empirical Laplace state-by-node TPM + modal sys_state
    (`binary_seq_to_tpm`, H_1002 VERBATIM);
  - **faithful_phi** ← the MI matrix over the SAME 4 binary unit-traces (`n_bins=2`,
    since the data is binary). faithful_phi is **NOT** given the H_999 continuous→MI
    n=8 path — it consumes the SAME n=4 binarized units.

This removes BOTH H_1002 confounds (the n shrink AND the binarization) — both engines
see the identical discretization at the identical n. Same procedure to every regime;
the **contrast** is the falsifier.

**Conditions (the EXACT H_999/H_1001/H_1002 regimes, harness VERBATIM):** REACT,
DRIFT (=H_971 imagine), GUIDED (=H_988), PLAN(depth 1/2/4/8) vs GREEDY (=H_973).
30 seeds. Both engines scored at this identical (n, discretization) per condition.

**≡-proofs (g5 CODE-measured, no LLM self-judge, p7):** BOTH mirrors proven
byte-faithful to their stdlib engines AT n=4 BEFORE any condition is scored —
big-Φ ≡ `iit4_bigphi.hexa` on the H_1002 ref TPMs incl. the n=4 ring4 cases
(|Δ|<1e-6); faithful_phi ≡ `faithful_phi.hexa` on the H_999 ref cases incl. the
n=4 `n4 dim6 nb2`=3.0 / `n4 dim6 nb4`=3.37744 cases (|Δ|<1e-4); plus a matched-path
n=4 binary check that the faithful units are EXACTLY `bits.T` (no continuous value
leaks into the faithful path) and both mirrors are deterministic functions of `bits`.

**Outcome rules (FROZEN — no token before measuring):**
- **🟢 AGREE-WHEN-MATCHED:** IF at identical (n, discr) the two measures AGREE on
  every condition sign AND the dose-response direction → H_1002's disagreement was
  the confound; the imagination/planning Φ-rise is measure-robust once inputs match
  (strengthens H_999/H_1001).
- **🔴 GENUINE-MEASURE-DISAGREEMENT:** IF they STILL DISAGREE at identical (n, discr)
  (e.g. faithful raises, big-Φ reverses for planning) → the MIP-EI scalar and the
  structure-level big-Φ really capture different things for these regimes — a real,
  publishable IIT-internal finding that bounds H_999/H_1001 to the MIP-EI measure.
- Either outcome is a real, important finding (a_paper_negative_ok cuts both ways).

## 3. Honest scope

TOY single matched-rung **n=4** (a_scale_honest_scope, a_toy_scale_recheck). Both
measures EXACT at n=4; the toy WM latent is binarized to an n=4 state-by-node TPM /
n=4 binary units. The (n, discretization) is now IDENTICAL across the two engines, so
any remaining disagreement is GENUINELY measure-level, not a confound — which is the
entire purpose of this rung. Scale-transfer UNVERIFIED. NOT a forge binary; $0
CPU-local.

## measurement (2026-06-07 · g5 CODE-measured · substrate=CPU-mirror numpy · BOTH mirrors PROVEN ≡ stdlib at n=4)

Probe: `UNIVERSE/h1004_bigphi_faithful_clean.py` · verdict:
`.verdicts/1004_bigphi_faithful_clean/h1004_bigphi_faithful_clean.txt`

**STEP 0 — ≡-proofs at n=4 (both mirrors vs their stdlib engines):**

| engine | n=4 ref case | mirror | hexa_ref | \|Δ\| |
|---|---|---|---|---|
| big-Φ ≡ iit4_bigphi.hexa | ring4_s15 (n=4 4-cycle) | 2.999999999 | 2.999999999 | 1.3e-10 |
| big-Φ ≡ iit4_bigphi.hexa | ring4_s10 (n=4 4-cycle) | 2.999999999 | 2.999999999 | 1.3e-10 |
| faithful_phi ≡ faithful_phi.hexa | n4 dim6 nb2 | 3.000000 | 3.000000 | 1.4e-09 |
| faithful_phi ≡ faithful_phi.hexa | n4 dim6 nb4 | 3.377444 | 3.377440 | 3.8e-06 |
| matched-path n=4 binary | faithful-units == bits.T | True | — | no continuous leak |

(plus the full H_1002 / H_999 ref sets reproduced in the verdict; deterministic re-run confirmed.)

→ **≡-PROOFS PROVEN** — both CPU mirrors reproduce their exact stdlib IIT4 engines
at n=4, and the matched path feeds the SAME `bits` to both with no cross-leak.

**Both engines at MATCHED (n=4, SAME binary discretization), per condition:**

| condition | big-Φ contrast (d, p) → dir | faithful_phi contrast (d, p) → dir | AGREE? | H_1002 (confounded: big-Φ n=4 / faithful n=8) |
|---|---|---|---|---|
| **H_971** DRIFT(imagine)−REACT | +0.423 (d+0.17, p0.51) → RAISES | +0.063 (d+0.13, p0.61) → RAISES | **AGREE** (both small n.s.) | big-Φ +0.42 / faithful +1.51 (d+2.09) |
| **H_988** GUIDED−REACT | +0.376 (d+0.17, p0.52) → RAISES | +0.494 (d+0.84, p2.0e-03) → RAISES | **AGREE** (faithful FLIPS + once matched) | big-Φ +0.38 / faithful −0.18 (d−0.28) |
| **H_973** PLAN(depth-8)−GREEDY | **−4.008 (d−1.83, p2.5e-08) → LOWERS** | **+2.333 (d+5.18, p6.7e-27) → RAISES** | **DISAGREE** (sign reversal PERSISTS) | big-Φ −4.01 / faithful +5.09 (d+4.64) |

**Planning dose-response (H_973):** big-Φ vs plan-depth [1,2,4,8] means [1.89, 8.48,
3.30, 5.52], **Spearman rho +0.122 (p0.18, n.s.)**; faithful_phi means [1.43, 3.00,
1.44, 2.84], **Spearman rho −0.161 (p0.078, n.s.)** — **opposite directions**, the
disagreement PERSISTS at matched inputs (neither is a clean monotone here at n=4).

## Finding (🔴 GENUINE-MEASURE-DISAGREEMENT)

At identical (n=4, SAME binary discretization), the two faithful IIT4 measures
**AGREE on imagination and guided but REVERSE on planning** — and the planning
reversal is the one that SURVIVES matching the inputs:

- **H_971 imagination** — both RAISE (big-Φ +0.42 d+0.17; faithful +0.06 d+0.13),
  both small and non-significant. AGREE. *This resolves H_1002's "effect collapse"*:
  once faithful_phi is run on the SAME n=4 binary discretization, its huge n=8 d+2.09
  shrinks to a small d+0.13 — i.e. H_1002's imagination collapse WAS the
  n/discretization confound, and at matched inputs the two measures simply agree on a
  small positive null.
- **H_988 guided** — both RAISE (big-Φ +0.38 d+0.17; faithful +0.49 d+0.84). AGREE on
  sign. *This resolves H_1002's "guided disagree"*: faithful_phi FLIPS from its n=8
  −0.18 to a matched-n=4 +0.49, so the H_1002 guided sign-mismatch WAS the confound.
- **H_973 planning** — big-Φ −4.01 (d−1.83, p2.5e-08, **LOWERS**) vs faithful +2.33
  (d+5.18, p6.7e-27, **RAISES**). **A genuine sign reversal that PERSISTS at matched
  inputs**, with opposite (non-significant) dose-response directions. *This is NOT the
  confound* — with n AND discretization held identical, the MIP-EI scalar and the
  structure-level big-Φ still split on planning.

**Mechanistic read:** for the branching planning-deliberation trace, the MIP-EI
**scalar** reads cross-cut mutual information among the binarized channels — the
multi-branch lookahead binds the channels across the best MI cut, so the scalar
RISES. The system **big-Φ** reads the Φ-structure (distinctions with an irreducible
cause AND effect plus their congruent relations) destroyed by the system MIP of the
binarized TPM — and the long branching deliberation binarizes into a state-by-node
TPM whose mechanisms are MORE separable, so the system MIP severs it more cheaply and
big-Φ FALLS. The two functionals of the SAME n=4 TPM genuinely point opposite ways for
planning. This is a real, publishable IIT-internal result.

**Resolution of H_1002 (explicit):** H_1002's three "disagreements" split cleanly —
- imagination effect-collapse → **CONFOUND** (resolves to AGREE at matched n=4);
- guided sign-flip → **CONFOUND** (resolves to AGREE at matched n=4);
- planning sign-reversal → **GENUINE** (persists at matched n=4).

So H_1002's overall ⚠ MEASURE-DEPENDENT verdict was partly the confound (imagination/
guided) and partly real (planning). H_1004 promotes the real part to a terminal 🔴
GENUINE-MEASURE-DISAGREEMENT and **bounds H_999/H_1001's planning Φ-rise to the
MIP-EI scalar measure** — the structure-level capstone does not confirm it even on
matched inputs. H_999/H_1001's imagination result is *not* contradicted by big-Φ at
matched inputs (both small-positive). No H_999/H_1001 source verdict is overwritten;
this is a forward-pointing bound.

## 4. Sibling / xlinks

- ⇄ [H_1002](./H_1002_bigphi_upgrade.md) (⚠ MEASURE-DEPENDENT — the confounded comparison this H disentangles; resolution note appended there)
- ⇄ [H_999](./H_999_faithful_iit4_remeasure.md) (faithful MIP-EI scalar n=8) · [H_1001](./H_1001_reopen_consolidate.md) (terminal 2🟢/2🔴 close)
- ⇄ [H_971](./H_971_imagined_rollout_consciousness.md) · [H_973](./H_973_planning_as_consciousness.md) · [H_988](./H_988_guided_imagination_phi.md) · [H_994](./H_994_goal_coupled_phi_reframe.md)
- ⇄ [H_278](./H_278_faithful_phi_engine.md) (faithful-Φ engine → stdlib) · [IIT4_PHI_TOOLS.md](./IIT4_PHI_TOOLS.md) · project.tape `a_phi_iit4_tool` · `a_paper_negative_ok`
- ⇄ [CWM](../CWM/CWM.md)
- engines: `hexa-lang/stdlib/consciousness/iit4_bigphi.hexa` (system big-Φ M4) · `iit4/faithful_phi.hexa` (MIP-EI scalar) — BOTH mirrored byte-faithful at n=4 in this probe
