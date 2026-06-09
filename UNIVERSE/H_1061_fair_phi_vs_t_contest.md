# H_1061 — fair-Phi-vs-T-contest (closes the H_1060 QUALIFIED / DEGENERATE residual)

**status: PRE-REGISTERED (falsifier + FROZEN 0.15 margin + non-degeneracy guard declared BEFORE measuring; TEXT-only until the verdict .txt lands)**

## section 0 — lineage / why this H (the residual H_1060 SELF-FLAGGED verbatim)

H_1060 (RULER-NEEDS-T, GREEN-tier) was **QUALIFIED / DEGENERATE**. Its big PASS margin (+0.60)
was partly **BUILT-IN**: by construction the DELIBERATE-ACTIVE vs DELIBERATE-PASSIVE classes
were **Phi-IDENTICAL pair-for-pair (24/24)** — agency-mode moved ONLY T, never Phi — so a
Phi-scalar was *structurally* unable to separate them. H_1060 flagged the open follow-up
VERBATIM:

> "does NOT demonstrate a fair head-to-head Phi-vs-T contest (that would need agency to ALSO move
> Phi-relevant behavior — UNVERIFIED, a follow-up rung)."

**THIS hypothesis closes that residual.** Build a **FAIR** battery where agency-mode ALSO
co-varies Phi-relevant behavioral structure (the active/passive classes are NO LONGER
Phi-matched) so NEITHER axis is structurally privileged, then re-run the head-to-head: **does T
STILL add discriminative power over the best single Phi-scalar once Phi is genuinely allowed to
move with agency?**

## section 1 — design (REUSE harnesses; fix the degeneracy)

Take the H_1060 mixed battery but **REMOVE the Phi-identity constraint** — let agency-mode
couple to the rollout parameters that DRIVE Phi. Concretely, in the H_1035 `rich_rollout(seed,
depth, explore, mix)` substrate, the realized n=4 state distribution (hence faithful phi_EI and
big-Phi via `substrate_reads`) is a deterministic function of `(depth, explore, mix)`. So we
make agency co-vary `(explore, mix)`:

- A base policy has a nominal `(depth, explore_base, mix_base)`.
- **ACTIVE** agency = a COMMITTED deliberate plan -> low explore / low mix (`explore_base`,
  `mix_base`) AND the H_1051 machinery run with `active=True` (deep provenance + real veto).
- **PASSIVE** agency = a FORCED / drifting plan -> higher explore + more greedy-mixing
  (`explore_base + de`, `min(mix_base + dm, 0.5)`) AND the H_1051 machinery `active=False`
  (shallow provenance + saturated veto).

Because `(explore, mix)` provably move Phi at fixed depth (pre-probe: d=2 faith 3.000->0.541,
big 8.476->3.343 as e/mix rise), the SAME base policy under ACTIVE vs PASSIVE now yields a
**DIFFERENT Phi AND a DIFFERENT T** — Phi is NO LONGER blind by construction. This is the
precise fix for the H_1060 degeneracy.

Everything else is REUSED VERBATIM:
- `rich_rollout` + `substrate_reads` (BOTH stdlib IIT-4.0 engines, n=4 exact, NO proxy) +
  `policies` + `loo_nearest_centroid_accuracy` — via the H_1047 module exec'd with its
  `__main__` guard stripped (inherits H_1035/H_1014/H_1004 + the H_1012 mirror proof).
- H_1051 `_provenance_depth` (H_932 verified-link DEPTH) + `_veto_capacity` (H_935 active-veto
  fraction) UNMODIFIED -> **T = z(prov-depth) + z(veto-cap)** over the battery.
- Phi per member = the H_1047/H_1035 SEED-MEAN path (`for s in range(N_SEEDS)`), so the
  REPRODUCE-H_1047 greedy anchor (faith=0.50693 / big=9.52829) holds.

Behavioral CLASS (structural, measure-INDEPENDENT — the prediction target), >=3 classes:
- `REACTIVE`            = depth==0 (greedy), regardless of agency
- `DELIBERATE-ACTIVE`  = depth>=1 AND agency==ACTIVE (committed plan: distinct Phi + deep T)
- `DELIBERATE-PASSIVE` = depth>=1 AND agency==PASSIVE (drifting plan: distinct Phi + shallow T)

features:
- **PAIR (Phi, T)** = (best-single-Phi-scalar-normalized, T-normalized) 2-D.
- scalars: s_faith, s_big, s_T (1-D each); "best single Phi-scalar" = max LOO-acc over
  {s_faith, s_big}.

classifier = **LOO nearest-centroid** (H_1047/H_1060 protocol, VERBATIM
`loo_nearest_centroid_accuracy`).

## section 1b — THE KEY NEW PIECE: anti-tautology NON-DEGENERACY guard

This is what makes H_1061 a genuine NEW measurement, not a re-run. It is the **converse** of
H_1060's fairness guard. BEFORE scoring we MEASURE and ASSERT that the agency classes are
**NOT Phi-identical**:

```
for each deliberate (depth>=1) base policy with an ACTIVE member A and PASSIVE member Q:
    dphi_faith = |A.faith - Q.faith|   ;   dphi_big = |A.big - Q.big|
non-degeneracy PASS  iff  every deliberate active/passive pair has  (dphi_faith > FLOOR  OR
                                                                     dphi_big   > FLOOR)
FLOOR = 1e-3   (FROZEN; far above the 1e-9 Phi-identity test H_1060 used)
report the FULL distribution of per-pair |dphi_faith| and |dphi_big| (min / median / max).
```

If non-degeneracy FAILS (classes still Phi-identical), the contest is NOT fair and the verdict
is VOID/QUALIFIED — same trap H_1060 fell into. We assert it explicitly so the head-to-head is
honest.

## section 2 — PRE-REGISTERED FALSIFIER (FROZEN before scoring — NO goalpost move)

```
MARGIN = 0.15   (the SAME pre-set bar as H_1047 / H_1060 — frozen, do NOT move)

H1-PASS = RULER-GENUINELY-NEEDS-BOTH :
    (non-degeneracy PASS)  AND
    acc[(Phi,T) 2-vector]  >=  best_acc[single Phi-scalar]  +  0.15   AND
    s_T-alone does NOT already saturate (i.e. acc[(Phi,T)] > acc[s_T] + eps,
        so Phi also contributes)  -> ruler needs BOTH axes, NON-degenerately.

FAIL modes — BOTH publishable (a_paper_negative_ok):
  (a) PHI-ABSORBS-AGENCY : non-degeneracy PASS but margin < 0.15
      -> once Phi can move with agency, a Phi-scalar absorbs the agency signal and T is
         redundant (Phi-suffices; strengthens H_1045).
  (b) NON-DEGENERATE-T-DOMINANT : non-degeneracy PASS and margin >= 0.15 but
      s_T-alone == (Phi,T) 2-vector (Phi adds ~0, Phi-alone low)
      -> still T-dominant, but now NON-degenerately (genuine separable-Phi battery,
         T still carries the class signal Phi cannot).
```

Report the EXACT margin + the non-degeneracy |dphi| distribution EITHER WAY. NO goalpost-moving
(the H_1047 lesson: the pre-set bar has teeth). eps for the s_T-saturation sub-clause = 1e-9
(strict-greater, deterministic LOO so accuracies are exact rationals).

## section 3 — constraints / scope

- **a_phi_iit4_tool**: faithful phi_EI + big-Phi via stdlib EXACT n<=5
  (`hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa` + `iit4_bigphi.hexa`), NEVER a proxy.
  RE-PROVE the python mirror == stdlib EXACT to 6dp at n=4 AND n=5 (BOTH engines) via the
  H_1012 `prove_mirrors_at_n(4)` + `prove_mirrors_at_n(5)`; mirror uses BITS/log2
  MI=H(A)+H(B)-H(A,B) (H_1043 nats-bug lesson).
- REUSE H_1051 T-machinery (`_provenance_depth` H_932 + `_veto_capacity` H_935) UNMODIFIED +
  the H_1035/H_1047 policy battery + `loo_nearest_centroid_accuracy` LOO protocol VERBATIM +
  the H_1012 mirror-prover.
- Confirm a **reproduce-check**: REPRODUCE-H_1029 EXACT + REPRODUCE-H_1047 greedy seed-mean
  anchor (faith=0.50693 / big=9.52829) BEFORE scoring.
- p3/p6/p7: generic toy policies, no persona. TOY n<=5, NO GPU/pod. real-module import; SERIAL
  only — NO unguarded multiprocessing.Pool (H_1038 hang lesson); `if __name__`-guard.
- $0 CPU-local.
- **a_scale_honest_scope**: toy n<=5 rung; scale-transfer UNVERIFIED. g5/p7.

artifacts: `UNIVERSE/h1061_fair_phi_vs_t_contest.py` ·
`.verdicts/1061_fair_phi_vs_t_contest/H_1061.txt`

## section 4 — VERDICT (g73 .txt backed; emoji tier AFTER the .txt landed)

_(pending measurement — TEXT-only until `.verdicts/1061_fair_phi_vs_t_contest/H_1061.txt` lands)_
