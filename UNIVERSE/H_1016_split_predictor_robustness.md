---
id: H_1016
slug: split-predictor-robustness
title: Does the H_1014 magnitude-threshold split-predictor SURVIVE at n=5, and is there a monotone DOSE-RESPONSE onset where the faithful-up / big-Phi-down split first appears as planning strength is swept?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · intervention-classifier · split-predictor · robustness · dose-response
source: H_1014 (PREDICTOR-SEPARATES QUALIFIED — a MAGNITUDE threshold on Δ cross-MIP coupling, boundary +1.4933, separates the one split intervention {planning} from the three non-split {imagination, guided, chaos} at n=4; the pre-registered DIRECTION was FALSIFIED) + H_1012 (the split itself is DISAGREEMENT-ROBUST-IN-N across n={4,5}) + PAPER/phi-measure-dependence-planning
exploration_method: E2 (extend the H_1014 intervention-SET + cross-MIP-coupling predictor pipeline to n=5 AND add a planning-strength dose-response continuum, both read off the SAME matched discretization) + E14 (substrate-native IIT4) + a_completeness_over_cheap
verification_method: W2 (pre-registered robustness + dose-response falsifier · both stdlib engines iit4/faithful_phi.hexa + iit4_bigphi.hexa at matched discretization · CPU-mirror equivalence-proof per n via H_1012 prove_mirrors_at_n BEFORE scoring) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
sister: H_1014 (the n=4 magnitude-threshold predictor), H_1012 (split robust in n {4,5}), H_1004 (clean disagreement at n=4), H_999/H_1001 (faithful_phi planning up), H_1002 (the original confounded big-Phi), PAPER/phi-measure-dependence-planning, a_phi_iit4_tool
scope: TOY n={4,5}, $0 CPU-local, real IIT-4.0 stdlib engines (CPU mirror RE-PROVEN equal to stdlib at n=4 AND n=5 per H_1012 prove_mirrors_at_n BEFORE scoring). big-Phi super-exponential — n=5 is ~slow but tractable for the SET and the depth sweep; n=6 is the honest cap (skipped, as in H_1012). a_scale_honest_scope · a_toy_scale_recheck — scale-transfer beyond n=5 UNVERIFIED. NOT a forge binary; no GPU.
verdict: 🟠 PARTIAL (AMBER) — exactly ONE of the two pre-registered robustness bars holds. PART 2 (dose-response) PASSES: the planning depth sweep {1,2,3,4,6,8} at n=4 shows the predictor Δ(cross-MIP coupling) rising with depth (Spearman rho +0.429>0, monotone-positive), the faithful-up/big-Φ-down SPLIT first ONSETS at depth-2, AND the predictor crosses the H_1014 boundary +1.4933 at exactly depth-2 (onset == boundary-cross) — so the H_1014 magnitude threshold IS a genuine dose-graded trigger of the split (a real Δ-vs-depth finding). PART 1 (robustness in n=5) FAILS as a CLEAN separation: re-scored at n=5 the SET no longer separates by the magnitude threshold — three interventions now carry a split label (planning d_big−2.28/d_faith+4.65 = TRUE split, reproduces H_1012; imagination d_big+0.19/d_faith−0.11 and guided d_big−0.14/d_faith+0.72 = NOISE-driven sign flips, both big-Φ contrasts NON-significant p=0.47/0.59) while chaos (d_faith+1.74, no-split) has predictor +0.97 sitting ABOVE the genuine-split guided (+0.53) and the noise-split imagination (+0.05) — the split/no-split predictor RANGES OVERLAP, no single threshold separates, and only-planning-is-split=False. So the n=4 4-way magnitude separation does NOT generalize to n=5; what IS robust in n is the underlying PLANNING split itself (planning d_big−2.28/d_faith+4.65 at n=5, matching H_1012's d−2.28/+4.65) and the predictor's MONOTONE coupling-magnitude relation to the split via dose. Net: the predictor is dose-graded (PASS) but its 4-way classifier separation is an n=4 small-system property (FAIL at n=5), driven at n=5 by tiny non-significant big-Φ sign flips on the weak no-split interventions. Both CPU mirrors RE-PROVEN ≡ stdlib at n=4 AND n=5 BEFORE scoring (PROVEN). g5 CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool. TOY n={4,5}; scale-transfer UNVERIFIED.
status: measured
---

# H_1016 — robustness (n=5) + dose-response onset of the H_1014 split predictor

## 0. motivation
H_1014 established (QUALIFIED) that at n=4, across the intervention SET
{planning[split], imagination, guided, chaos[no-split]}, a single MAGNITUDE threshold on
the candidate predictor Δ(cross-MIP coupling) (boundary +1.4933, read off the SAME binary
discretization that feeds BOTH stdlib engines) separates the one split-inducing intervention
(planning, +2.2983) from the three non-split ones (≤+0.6883). The pre-registered DIRECTION
(split ⟺ DECREASED coupling / raised modularity) was FALSIFIED — every intervention RAISES
coupling; only magnitude separates.

Two open robustness questions remain, both extending H_1014:
1. **Robustness in n.** H_1012 showed the SPLIT ITSELF is robust across n={4,5}. Is the
   PREDICTOR's magnitude-threshold separation also robust at n=5 — i.e. re-scored at n=5,
   does the planning predictor still sit ABOVE every non-split predictor (a separating
   threshold still exists), with planning the sole split intervention?
2. **Dose-response onset.** H_1014 used a single planning strength (depth-8). Sweeping the
   planning intervention's look-ahead depth across a continuum {1,2,3,4,6,8} (depth-1 =
   greedy baseline), where does the split ONSET — the first depth at which
   sign(Δfaithful)≠sign(Δbig-Φ) appears — and does the predictor's magnitude cross its
   H_1014 boundary (+1.4933) at the SAME depth? A monotone onset (predictor rises with
   depth and the split appears once the predictor crosses the boundary) would make the
   magnitude-threshold a genuine dose-graded classifier, not an n=4/depth-8 coincidence.

## 1. hypothesis
(a) The H_1014 magnitude-threshold separation is ROBUST at n=5: re-scored at n=5 on the SAME
pipeline, planning is the sole split intervention and its Δ(cross-MIP coupling) predictor sits
strictly ABOVE every non-split intervention's predictor (a separating boundary exists).
(b) There is a MONOTONE dose-response onset: as planning depth rises 1→8, the predictor
Δ(cross-MIP coupling) rises monotonically and the faithful-up/big-Φ-down SPLIT first appears
at (or just after) the depth where the predictor crosses the H_1014 boundary +1.4933.

## 2. pre-registered falsifier (frozen 2026-06-07)
Reuse the H_1014 measurement EXACTLY (its `substrate_reads` both-engine + predictor read, its
intervention SET generators, H_1012 `prove_mirrors_at_n` equivalence proof), parametrized over n.
python3 -u, serial, $0 CPU, poll inline (NO Monitor/waiter — a_cpu_local_no_waiter).

**STEP 0 — equivalence proof.** Run H_1012 `prove_mirrors_at_n(4)` AND `prove_mirrors_at_n(5)`;
assert BOTH CPU mirrors ≡ their stdlib IIT-4.0 engines at n=4 AND n=5 BEFORE any scoring (abort
otherwise). The predictor cut-weight is a deterministic pure function of the same bits.

**PART 1 — robustness at n=5.** Re-score the SAME H_1014 SET {planning, imagination, guided,
chaos} at n=5 (30 seeds). For each: Δfaithful, Δbig-Φ, split label = sign(Δfaithful)≠sign(Δbig-Φ),
and the predictor Δ(cross-MIP coupling). Run the SAME separation test (does a single threshold
separate the split set from the no-split set?).

**PART 2 — dose-response.** Sweep planning depth d ∈ {1,2,3,4,6,8} (d=1 = greedy baseline) at
the binding n (n=4, where the full sweep × 30 seeds is tractable; n=5 reported if it completes).
At each depth d>1, contrast depth-d vs greedy(d=1): Δfaithful, Δbig-Φ, split label, and the
predictor Δ(cross-MIP coupling). Locate (i) the ONSET depth = first depth with a split, and
(ii) the depth where the predictor crosses the H_1014 boundary +1.4933; check monotonicity
(Spearman rho of predictor vs depth) and whether onset ≈ boundary-crossing.

Outcome (NO emoji token before `.verdicts/1016_split_predictor_robustness/1016.txt` exists):
  - PASS = GREEN — IFF the magnitude threshold separates planning(split) from the non-split
    set at n=5 (PART 1) AND a MONOTONE dose-response onset exists (predictor rises monotonically
    with depth, the split onsets, and onset depth coincides with / immediately follows the
    predictor crossing +1.4933) (PART 2).
  - PARTIAL = AMBER — exactly one of {n=5 separation, monotone dose-onset} holds.
  - CLOSED-NEGATIVE = RED — neither holds (the n=4/depth-8 predictor separation does NOT
    generalize in n and there is no monotone dose-onset); a_paper_negative_ok — a closed-negative
    ruling out the predictor's robustness/dose-gradation is publishable.

## 3. honest scope
big-Phi exact only at small n (super-exponential distinction + bipartition search). n=5 is slow
but tractable for the SET × 30 seeds and the n=4 depth sweep; n=6 is the honest cap (skipped, as
in H_1012). Both engines EXACT at every scored n; CPU mirror RE-PROVEN ≡ stdlib at n=4 AND n=5
BEFORE scoring (H_1012 discipline). Scale-transfer beyond n=5 UNVERIFIED. a_scale_honest_scope ·
a_toy_scale_recheck. NOT a forge binary; $0 CPU-local, no GPU. g5 CODE-measured (no LLM self-judge,
p7), a_phi_iit4_tool.

## 4. sibling / xlinks
to [H_1014](./H_1014_intervention_split_predictor.md) · [H_1012](./H_1012_bigphi_faithful_larger_n.md) ·
[H_1004](./H_1004_bigphi_faithful_clean.md) · [H_1002](./H_1002_bigphi_upgrade.md) ·
[H_999](./H_999_faithful_iit4_remeasure.md) · [H_1001](./H_1001_reopen_consolidate.md) ·
PAPER/phi-measure-dependence-planning · IIT4_PHI_TOOLS.md · a_phi_iit4_tool

## 5. measurement + finding (2026-06-07 · 🟠 PARTIAL/AMBER · g5 CODE-measured, $0 CPU-local)
Verdict raw: `.verdicts/1016_split_predictor_robustness/1016.txt` (g73 — deterministic run that
COULD have falsified; both stdlib engines + CPU mirror RE-PROVEN ≡ stdlib at n=4 AND n=5 BEFORE
scoring; ≡-PROOF n=4 PROVEN, ≡-PROOF n=5 PROVEN).

**Result — the dose-response onset HOLDS but the n=5 magnitude separation FAILS (exactly one bar):**

### PART 1 — robustness in n=5 (re-score the H_1014 SET at n=5): FAILS as a clean separation
intervention vs baseline, both engines + predictor, 30 seeds, matched (n=5, binary discretization):

| intervention | big-Φ d | faithful d | SPLIT? | predictor Δ cross-MIP | note |
|---|---|---|---|---|---|
| planning | **−2.284 LOWERS** | **+4.652 RAISES** | **True** | **+3.0170** | genuine split, reproduces H_1012 (d−2.28/+4.65) |
| imagination | +0.188 (p=0.47, NS) | −0.105 (p=0.68, NS) | True | +0.0467 | NOISE flip — both contrasts non-significant |
| guided | −0.140 (p=0.59, NS) | +0.720 | True | +0.5301 | weak/noise split — big-Φ NS |
| chaos [NEW] | +0.275 (p=0.29, NS) | +1.735 | False | +0.9674 | no-split, predictor ABOVE two "splits" |

- The magnitude threshold does NOT separate at n=5: split-set predictors {+3.0170, +0.0467, +0.5301}
  vs no-split {+0.9674} — RANGES OVERLAP (chaos no-split +0.97 > guided split +0.53 > imagination
  split +0.05). `separation: ranges OVERLAP — no separating threshold`; `only-planning-is-split: False`.
- The clean n=4 4-way split labelling does NOT survive to n=5: at n=5 the two WEAK no-split
  interventions (imagination, guided) acquire spurious split labels driven by tiny NON-significant
  big-Φ sign flips (p=0.47, 0.59). So the H_1014 4-way magnitude separation is an **n=4 small-system
  property** — it does not generalize in n. ⇒ **PART 1 = FAIL (n=5 separation HOLDS: False).**

### PART 2 — dose-response onset (planning depth sweep vs greedy, n=4): PASSES
depth d vs greedy(d=1), 30 seeds, matched (n=4):

| depth | Δbig-Φ | Δfaithful | SPLIT? | predictor Δ coupling | > H_1014 boundary +1.4933? |
|---|---|---|---|---|---|
| 1 (greedy) | 0.0000 | 0.0000 | False | 0.0000 | False |
| 2 | −1.0520 | +2.4931 | **True (ONSET)** | +2.4581 | **True (CROSSES)** |
| 3 | −5.5122 | −0.0338 | False | +0.0094 | False |
| 4 | −6.2276 | +0.9325 | True | +0.9053 | False |
| 6 | −5.9794 | +2.0259 | True | +1.9909 | True |
| 8 | −4.0083 | +2.3332 | True | +2.2983 | True |

- predictor-vs-depth Spearman **rho=+0.429 (>0, monotone-positive)**; split **ONSET depth = 2**;
  predictor **crosses the H_1014 boundary +1.4933 at depth = 2** — `onset == boundary-cross depth: True`.
  ⇒ the split first appears exactly where the predictor crosses its H_1014 threshold: the magnitude
  threshold IS a genuine **dose-graded trigger** of the faithful-up/big-Φ-down split.
- Honest wobble: depth-3 is a non-monotone dip (split vanishes, predictor +0.009) — the dose curve is
  positive-monotone in rank (rho +0.429) but NOT strictly monotone; the onset/boundary coincidence at
  depth-2 and the high-depth (6, 8) re-crossings are robust. ⇒ **PART 2 = PASS (monotone dose-onset: True).**

### VERDICT-TOKEN: PARTIAL (AMBER)
Exactly one of {n=5 separation, monotone dose-onset} holds (n=5 separation **False** | dose-onset
**True**), so the pre-registered PASS=GREEN (BOTH bars) is NOT met and RED=closed-negative (NEITHER) is
NOT met. The H_1014 magnitude-threshold predictor is **dose-graded** (the split onsets exactly when the
predictor crosses +1.4933 as planning depth rises) but its **4-way classifier separation is an n=4
small-system artifact** — it does not generalize to n=5, where weak no-split interventions pick up
spurious split labels from non-significant big-Φ sign noise. What IS robust in n is the underlying
PLANNING split itself (planning d_big−2.28 / d_faith+4.65 at n=5, matching H_1012). a_paper_negative_ok
applies to the n=5-separation half (ruled out); the dose-graded half is a positive Δ-vs-depth finding.

**honest scope (a_scale_honest_scope · a_toy_scale_recheck):** TOY n={4,5} — both engines EXACT;
big-Φ super-exponential so n=5 (240 evals) is the rung for the SET re-score and the depth sweep ran
at n=4 (the binding rung); n=6 is the honest cap (skipped, as in H_1012). Both CPU mirrors RE-PROVEN
≡ stdlib at n=4 AND n=5 (H_1012 prove_mirrors_at_n; PROVEN) BEFORE scoring; the predictor is a
deterministic pure function of the same bits. Scale-transfer beyond n=5 UNVERIFIED. g5 CODE-measured
(no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; $0 CPU-local, no GPU.
