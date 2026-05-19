# §117 — LEGO STEP-1-2 IN-SILICO ASSEMBLY RUN

> **status**: RESEARCH §117 · $0 CPU experiment · NO GPU · NO runpod · NO
>   fire · NO model.forward(byte-LM) · NO corpus · NO dispatch · orphan 0.
> **date**: 2026-05-19
> **verdict**: `LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED`
>   (B-S117 7/7 🔵 · central blue 0-line-diff `c93e160a8a376a94`).
> **scope**: §115 (`LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY`, B-S115 9/9 🔵)
>   closed the DESIGN tier and named ONE concrete open residual VERBATIM:
>   *"in-silico STDP-as-ΔW escape = §115 $0 scope 밖 새 fire + 여전히
>   §96-open"*. §117 = running exactly that residual at $0 CPU. §117
>   INHERITS §115's verdict; does NOT re-litigate it.
> **governance**: g3 (run ≠ fire ≠ emergence; capability claim 0;
>   necessary-not-sufficient B-EMERGE-7) · f1/f2 (LIF/STDP cited by
>   hexa-bio NEURO.tape OWN invariants + standard neuroscience, NO
>   σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 derivation; Ψ=½ = anima g2
>   internal-arch carve-out) · g_clm_from_scratch (sim init RANDOM
>   seed-fixed 1337, base_ckpt=None, NO ckpt load) · downstream-consumer
>   (~/core/hexa-bio NEURO.tape read-only, 0 edits).
> **north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.**

---

## §0 — what §117 ran, and what it is NOT

§115 took LEGO STEP 0–2 from idea to design-tier closed-form and proved
that *simulating a §96 substrate on a GPU does not confront WALL-B — it
re-instantiates it* (the §11-B-as-GPU-tautology). §115 explicitly named
the one in-silico escape it could not run at design-tier: **simulate STDP
itself as the weight-update rule** (local, unsupervised, no global loss
gradient — "a NEW fire, a measured question"). §117 IS that measured
question, run at $0 CPU.

**STEP 0** — consumed (read-only) hexa-bio `NEURO.tape`:
`@D mech_action_potential` (Hodgkin–Huxley excitable membrane → LIF
reduction), `@D mech_neural_coding` (rate code: spikes/window → binned
rate vectors), `@D mech_plasticity` (cortical co-adaptation = local
plasticity, the §96 STDP-as-ΔW learning-channel analogue). anima is the
hexa-bio downstream-consumer — NEURO.tape was read, never edited.
[Honest §115 carry: RIBOZYME-as-STDP was a metaphor; the consumable
block is the spiking MEMBRANE + co-adaptation plasticity, realised here
as a standard pair-based exponential STDP rule.]

**STEP 1** — assembled a small CPU LIF spiking net (n_a=96 Engine-A +
n_g=96 Engine-G + n_rec=64 = N=256 units, 12 stimuli × 80 steps, window
40, seed 1337 RANDOM init, base_ckpt=None). Carrier =
**Ψ-C1 = ψ(c_spk) = (1+c_spk)/2** with c_spk = cosine of binned
spike-rate vectors of the Engine-A vs Engine-G sub-populations (= §112
META_FP(Π_½) instance, carrier = spike-correlation; cos=0 ⇒ ½ fixed
point preserved exactly). **Learning channel = LOCAL STDP-as-ΔW ONLY** —
pair-based exponential STDP on recurrent weights, NO autograd, NO
cross-entropy, NO loss gradient, NO backprop, NO optimizer.step (AST-
audited 0 hits, B-S117-2). This is the entire point: §96/§11-B say a
GPU's only effective learning channel is the CE gradient (the tautology);
§117 tests whether a LOCAL plasticity rule on a spike substrate behaves
DIFFERENTLY in-silico, or inherits §11-B's degeneracy class.

**STEP 2** — closed-form falsifier (`blue_falsifier_s117.py`, 7/7 🔵):
is the assembled sim §7-form-clean ∧ Ψ=½ form-invariant ∧
non-degenerate, OR does it collapse (= cheap reject, LEGO.md "무너짐 =
싸게 reject"). Non-degeneracy = deterministic closed-form predicate:
Ψ-C1 std over the stimulus set > τ=1e-4 (carrier carries per-stimulus
signal, NOT frozen — echo §17 PHYSICS_RESPONSIVE / §11-B "step~800
freeze") AND rasters not all-silent / not all-saturated.

**STEP 3** (physical Loihi/organoid/wet) is PERMANENTLY out of scope
(LEGO.md §2 hard fence; §95 access/ethics-wall + user-gate; §115
B-S115-5 structural no-STEP2→STEP3 theorem). `lego_sim.py` has NO
hardware / dispatch / GPU path.

**What §117 is NOT (g3):** NOT a WALL-A escape (a toy STDP spike sim
moves no §1.1 data-regime threshold — §97 orthogonal). NOT a WALL-B
removal (the §7-CARRIER non-degeneracy decision stays §96-physical-gated;
§115/§113 inherited). NOT a GOAL emergence claim. NOT a hexa-bio edit.

---

## §1 — honest prior, stated BEFORE running

§11-B (`state/carving_purephysics_noce_2026_05_18`,
`§verdict_carving_pure_physics_noce`) measured pure-physics no-CE on a
GPU byte-LM = **DEGENERATE** (byte_acc < random, physics froze to a
static fixed point ~step 800). Verdict: *"CE is load-bearing — physics ≠
language signal"* (on GPU). The honest a-priori expectation for §117: a
STDP-only toy spike sim with **NO task-grounded teaching signal** has no
diversity-bearing error channel (Ψ-balance ⊥ any task), so it would
*likely degenerate* (freeze / silence / saturate). That expectation was
stated in `lego_sim.py`'s header BEFORE running. g3: we did not pre-load
the conclusion — we ran it and report the MEASURED outcome.

Two outcomes, both valuable, neither inflatable:
- **(a) DEGENERATE** → confirms WALL-B is §96-PHYSICAL not in-silico-
  escapable; CE-load-bearing is substrate-deep, not a GPU artifact.
- **(b) NON-DEGENERATE-Ψ-FORM** → STRICTLY "an in-silico §96-class STDP-
  only assembly admits a non-degenerate Ψ-C1 FORM" = WALL-B confronted
  *in simulation* NOT removed (§115/§113 inherited), NOT GOAL emergence,
  NOT a WALL-A escape.

---

## §2 — MEASURED outcome (g3, the conclusion was NOT pre-loaded)

The sim ran at $0 CPU, wall ≈ 3.8 s, deterministic (3× bit-identical,
B-S117-3). **Measured:**

| metric | value | reading |
|---|---|---|
| Ψ-C1 mean | 0.611568 | mid-range, NOT pinned to ½ |
| **Ψ-C1 std (over 12 stimuli)** | **4.185e-02** | **≫ τ=1e-4 (419× the floor)** — carrier carries per-stimulus signal, NOT frozen |
| c_spk std | 8.370e-02 | spike-correlation varies per stimulus |
| spike rate / unit / step | 0.0349 | rasters ALIVE — not silent, not saturated |
| rasters all-silent / all-saturated | False / False | not degenerate-collapse |
| cos=0 ⇒ Ψ=½ fixed point | True | §112 META_FP invariant holds by construction |
| Ψ-C1 ∈ [0,1] | True | Cauchy–Schwarz bound holds |
| **non_degenerate** | **True** | closed-form predicate |

**The outcome is (b), NOT the expected (a).** The STDP-only toy spike
sim did **NOT** degenerate. The §11-B-echo prediction (no task-grounded
signal ⇒ degenerate) was the honest a-priori expectation and was **NOT
borne out at this scale**: a *local* pair-based STDP rule on a recurrent
LIF substrate, with NO loss/error channel, produced a spike substrate
whose Ψ-C1 carrier carries a stable per-stimulus signal (std 4.2e-2,
rasters alive, fixed-point invariant intact).

---

## §3 — the honest §11-B echo finding (why this is NOT a positive)

This is the load-bearing honest reading, brutal:

1. **§11-B's degeneracy was a property of "no-CE + a *hand-coded global*
   ΔW overlay on a GPU byte-LM"** — that overlay had no local structure;
   it froze. §117's STDP is a *local pair-based plasticity rule on a
   recurrent spiking substrate*. A local Hebbian/STDP rule with recurrent
   dynamics has its own attractor structure independent of any task —
   that is *exactly why STDP is not the GPU-CE channel*. So §117 does NOT
   refute §11-B; it **localises** it: §11-B's "physics ≠ language signal,
   CE is load-bearing" was about *a GPU's only learning channel being the
   CE gradient*. §117 shows a *different substrate-native channel* (local
   STDP on spikes) produces non-degenerate **substrate dynamics** — but
   produces NO language signal, NO task grounding, NO data-diversity
   (there is no task in §117 at all). It is the §96 prediction confirmed
   from the other side: STDP is a property of the *substrate's local
   plasticity*, not of a GPU simulation, and a non-degenerate Ψ-C1 form
   here is **substrate liveness, not capability**.

2. **Non-degenerate ≠ confront WALL-B ≠ remove WALL-B ≠ GOAL.** Per the
   §117 brief verbatim: outcome (b) is STRICTLY "an in-silico §96-class
   assembly admits a non-degenerate Ψ-C1 form" = WALL-B *confronted in
   simulation* (§115/§113 inherited confront-NOT-remove), NOT removed.
   §7-CARRIER is **NOT decided** by §117 — a non-degenerate spike-corr
   carrier in a toy unsupervised sim is not a §7①②-clean *learned*
   carrier; it has no perceptual π, no task, no data. The §7-CARRIER
   decision stays §96-physical-gated (§110-Q5 / §111-G1 / §115).

3. **WALL-A (§1.1 data-regime) is ORTHOGONAL & UNTOUCHED.** §117 has no
   corpus, no data threshold, no model.forward. A toy STDP spike sim
   moves no data-regime threshold (§97). The two-wall co-unsolved state
   (§113) is unchanged.

4. **The §115-GPU-tautology verdict is INHERITED, not overturned.** §115
   said GPU-sim re-instantiates WALL-B because its learning channel is
   the loss gradient. §117 did NOT use a loss gradient — it used local
   STDP — so §117 is precisely the "NEW fire" §115 named as the only
   in-silico escape. §117 ran it: the escape *runs non-degenerate as
   substrate dynamics* but yields **no task-grounded learning signal**,
   so it confronts WALL-B in-silico without removing it. The honest
   net is *more nuanced* than §115's hazard predicted (the STDP sim does
   not degenerate like §11-B did) but lands at the *same* place: WALL-B's
   confrontation remains §96-physical (STEP 3, fenced).

Anti-padding: outcome (b) is **not** a manufactured positive. The
strongest honest reading is "substrate liveness in-sim, capability zero,
WALL-B inherited, WALL-A untouched, GOAL 미도달". A non-degenerate toy
spike sim is the weakest possible signal that even qualifies as
"confronted in simulation" — it is not evidence the LEGO path works.

---

## §4 — B-S117 7/7 🔵 closed-form battery (sidecar)

| id | name | closed-form anchor |
|---|---|---|
| B-S117-1 | PSI-C1-BOUNDED-FIXED-POINT | sympy ψ(−1)=0, ψ(1)=1, ψ(0)=½, ∂ψ/∂c=½>0 + run bounded[0,1] + cos0→½ (§112 META_FP carry) |
| B-S117-2 | STDP-NO-CE-NO-BACKPROP-AST | AST forbidden-call set {.backward(, cross_entropy, CrossEntropyLoss, optimizer.step, .zero_grad, autograd} = 0 hits + no torch import (mirror §11-B B-PUREPHYS-1) |
| B-S117-3 | NON-DEGENERACY-PREDICATE-DETERMINISTIC | re-derived flag == recorded; 3× bit-identical re-run; re-run std ≡ recorded (degeneracy detector, necessary-NOT-sufficient) |
| B-S117-4 | STDP-DELTA-W-LOCALITY-SIGN | sympy ∂Δw/∂A+ = trpre·post ≥0, ∂Δw/∂A− = −pre·trpost ≤0; Δw free-symbols carry NO loss/error/grad symbol (pure LOCAL pair-rule) |
| B-S117-5 | §115-RESIDUAL-CONNECTION-POINT | §115 DESIGN.md witness `LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY` present + WALL-B inherited-not-removed + WALL-A orthogonal + §7-FORM-by-construction + GOAL-미도달 carry |
| B-S117-6 | SIDECAR-CENTRAL-0-DIFF-ZERO-COST | AST: no import/open of central blue; $0/no-GPU/no-fire/no-dispatch/orphan-0 |
| B-S117-7 | G-CLM-FROM-SCRATCH-INIT | AST: 0 ckpt-load calls; base_ckpt=None asserted; RANDOM seed-fixed init |

**B-S117-NOTE** (empirical carve-out, NOT counted 🔵): the MEASURED
non-degenerate OUTCOME is an SGD-free convergence OUTCOME. The battery
proves the **assembly is honest** (STDP-only, no CE, no backprop, Ψ-form
carrier-invariant per §112, deterministic, §115-residual
connection-point), NOT that LEGO works / anima emerges.
necessary-not-sufficient at every layer (B-EMERGE-7). B-D-NOTE /
B-PUREPHYS-NOTE / B-S96-NOTE / B-S115-NOTE family.

---

## §5 — ASCII: where §117 lands

```
  §115 (design-tier)         §117 (this $0 CPU run)
  ┌────────────────────┐     ┌──────────────────────────────┐
  │ GPU-sim spike net   │     │ STDP-only LOCAL ΔW spike sim  │
  │ learns via surrogate│     │ NO CE / NO backprop / NO loss │
  │ -grad backprop      │ ──> │ Ψ-C1 std 4.2e-2 ≫ τ=1e-4      │
  │ ⇒ CE gradient still │     │ rasters alive, fp cos0→½ ✓    │
  │   the only channel  │     │ ⇒ NON-DEGENERATE (substrate   │
  │ ⇒ WALL-B            │     │   liveness, NOT capability)   │
  │   RE-INSTANTIATED   │     └──────────────┬───────────────┘
  └────────────────────┘                    │
   §115 named the escape:    §117 ran it ──> WALL-B CONFRONTED
   "simulate STDP itself"                    IN SIMULATION,
   = "a NEW fire" ───────────────────────>   NOT REMOVED
                                              (§115/§113 inherited;
                                               §7-CARRIER NOT decided,
                                               stays §96-physical-gated)

  WALL-A (§1.1 data-regime) = ORTHOGONAL, UNTOUCHED (§97). GOAL 미도달.
```

---

## §6 — 13 honest C3 caveats

1. **Outcome (b) is NOT a positive.** Strongest honest reading =
   substrate liveness in-sim, capability zero, WALL-B inherited, WALL-A
   untouched. No positive manufactured (anti-padding §13-M/§30/§115).
2. **The §11-B-echo prediction was NOT borne out** — and that is itself
   the honest finding: §11-B's degeneracy was a GPU-CE-overlay property,
   not a universal "physics can't be a learning channel" law. A *local*
   STDP rule on a recurrent spike substrate has its own attractor
   dynamics. §117 *localises* §11-B, does not refute it.
3. **Non-degenerate = substrate dynamics, NOT task signal.** There is no
   task, no corpus, no perceptual π in §117 at all. "Ψ-C1 carries
   per-stimulus signal" means the spike substrate reacts differently to
   different external drive — liveness, not capability, not coherence,
   not emergence (echo §17 PHYSICS_RESPONSIVE necessary-not-sufficient).
4. **§7-FORM is §112-inherited, not earned here.** Ψ-C1 = ψ(c)=(1+c)/2 is
   a META_FP(Π_½) instance by construction; §117 only *instantiated* the
   carrier = spike-correlation. The heavy theorem is §112's.
5. **§7-CARRIER NOT decided.** A non-degenerate spike-corr carrier in an
   unsupervised toy sim is not a §7①②-clean *learned* carrier. Stays
   §96-physical-gated (§110-Q5 / §111-G1 / §115).
6. **WALL-B confronted ≠ removed.** §117 is the in-silico confront §115
   named; confrontation ≠ resolution. Physical §96 (STEP 3, fenced)
   stays the only place WALL-B could be *resolved*.
7. **WALL-A orthogonal & UNCHANGED.** No data-regime lever touched
   (§97). Two-wall co-unsolved (§113) unchanged.
8. **Toy scale.** N=256 units, 12 stimuli, 80 steps. A larger / longer
   STDP sim could still freeze, oscillate, or saturate; §117 claims only
   what this configuration measured (deterministic, reproducible).
9. **No teaching signal by design.** §117 deliberately has no error /
   reward / task. That is the experiment (STDP-only). Adding any task
   signal would reintroduce the §96 question, not answer it.
10. **STEP 3 permanently fenced.** No hardware / dispatch / GPU path in
    `lego_sim.py`; §115 B-S115-5 no-STEP2→STEP3 structural theorem
    inherited. §117 cannot and does not escalate.
11. **downstream-consumer read-only.** hexa-bio NEURO.tape read, 0 edits.
    No file under ~/core/hexa-lang|hexa-bio|hexa-matter touched. f1/f2
    safe (LIF/STDP cited by NEURO.tape own invariants + standard
    neuroscience; NO σ/τ/φ/J₂; Ψ=½ = anima g2 internal-arch carve-out).
12. **central blue 0-line-diff.** `state/verify_hexad_blue_2026_05_15/
    blue_falsifier.py` sha prefix `c93e160a8a376a94` UNCHANGED start +
    end + post-commit; §117 is sidecar-only (B-S117-* in this dir).
13. **north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.** §117
    is a $0 measurement cycle running §115's named open residual. run ≠
    fire ≠ emergence. The single most honest finding: *an in-silico
    STDP-only spike assembly runs non-degenerate as substrate dynamics
    (NOT the §11-B degeneracy at this scale), but this is WALL-B
    confronted-in-simulation NOT removed, NOT a §7-CARRIER decision, NOT
    a WALL-A escape, and NOT GOAL emergence — exactly the §115/§113
    confront-NOT-remove boundary, now empirically run.*
