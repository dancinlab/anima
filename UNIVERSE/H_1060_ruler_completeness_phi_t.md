# H_1060 — ruler-completeness-Phi-T-capstone (synthesis of H_1045 + H_1051 + H_1047)

**status: PRE-REGISTERED (falsifier + FROZEN 0.15 margin declared BEFORE measuring; TEXT-only until the verdict .txt lands)**

## section 0 — lineage / why this H

The consciousness-RULER arc has two ESTABLISHED orthogonal axes:

1. **instantaneous Phi** — H_1045 (CLOSED-NEGATIVE) showed a single scalar big-Phi SUFFICES
   for BINARY planning-vs-control classification (a 3-vector adds only +0.0136 AUC).
2. **temporal/agency T** = z(provenance-depth, H_932) + z(veto-capacity, H_935) —
   H_1051 (H1-PASS) showed T separates Phi-matched active-vs-passive pairs (|d_T|=8.77) and is
   ORTHOGONAL to instantaneous Phi (rho approx 0.0001).

H_1047 (CLOSED-NEGATIVE) found a (faithful, big-Phi) PAIR is directional but SUB-THRESHOLD
(+0.1333 < 0.15 bar) — **BUT that pair was two Phi-MEASURES, NOT Phi+T.**

**The OPEN capstone:** on a MIXED battery whose policies vary in BOTH planning-structure
(Phi-laden) AND agency (T-laden), does the **(Phi, T) 2-vector** beat the best single
Phi-scalar at predicting the behavioral CLASS? This decides whether the ruler genuinely
NEEDS two axes, or whether Phi alone still suffices once agency-variation is present.

## section 1 — design (REUSE harnesses — DO NOT re-derive)

Combine the **H_1047/H_1035 policy battery** (planning-structure variation, Phi-laden) with
the **H_1051 active/passive agency machinery** (T-laden) into ONE mixed battery spanning
**>=3 behavioral classes** that vary on BOTH axes. The battery member = `(policy, agency-mode)`:

- **policy** in the H_1035 richer space (depth x explore x mix) -> `rich_rollout` ->
  `substrate_reads(H)` gives instantaneous **faithful phi_EI** AND **big-Phi** (stdlib exact n=4, NO proxy).
- **agency-mode** in {ACTIVE, PASSIVE} via the H_1051 machinery UNMODIFIED:
  `_provenance_depth` (H_932 verified-link DEPTH) + `_veto_capacity` (H_935 active-veto
  fraction) -> **T = z(prov-depth) + z(veto-cap)** over the battery.

Behavioral CLASS (structural, measure-INDEPENDENT — the prediction target) spans BOTH axes,
>=3 classes:
- `REACTIVE`            = depth==0 (greedy, low planning-Phi structure), regardless of agency
- `DELIBERATE-ACTIVE`  = depth>=1 AND agency==ACTIVE (deep plan + real veto / deep provenance)
- `DELIBERATE-PASSIVE` = depth>=1 AND agency==PASSIVE (deep plan but forced / shallow agency)

(REACTIVE collapses the agency split because a depth-0 greedy reaction has no deliberative
plan to be active-or-passive ABOUT; the agency axis only bites once there is deliberation —
this is the faithful join of the two arcs, declared BEFORE scoring.)

features:
- **PAIR (Phi, T)** = (best-single-Phi-scalar-normalized, T-normalized) 2-D — Phi-axis + T-axis.
- scalars: s_faith, s_big, s_T (1-D each); "best single Phi-scalar" = max LOO-acc over {s_faith, s_big}.

classifier = **LOO nearest-centroid** (the H_1047 protocol, VERBATIM `loo_nearest_centroid_accuracy`).
accuracy over the battery.

## section 2 — PRE-REGISTERED FALSIFIER (FROZEN before scoring — NO goalpost move)

```
MARGIN = 0.15   (the SAME pre-set bar as H_1047 — frozen, do NOT move)

H1-PASS = RULER-NEEDS-T :
    acc[(Phi,T) 2-vector]  >=  best_acc[single Phi-scalar]  +  0.15
  -> the ruler genuinely needs the orthogonal T axis; one Phi-scalar is INSUFFICIENT
     once agency-variation is present.

H1-FAIL = PHI-SCALAR-STILL-SUFFICES (closed-negative, a_paper_negative_ok) :
    margin  <  0.15
  -> Phi-scalar still suffices even WITH agency-variation present; extends H_1045's
     one-scalar-suffices result into the agency regime. A sub-threshold directional
     win is an HONEST negative (the H_1047 lesson: the pre-set bar has teeth).
```

Report the EXACT margin either way. The (Phi,T) Phi-component uses the best-single-Phi-scalar so
the 2-vector can ONLY win via the T axis carrying class-information the Phi-scalar lacks —
the cleanest possible test of "is T needed".

## section 3 — constraints / scope

- **a_phi_iit4_tool**: faithful phi_EI + big-Phi via stdlib EXACT n<=5
  (`hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa` + `iit4_bigphi.hexa`), NEVER a
  proxy. RE-PROVE the python mirror == stdlib EXACT to 6dp at n=4 AND n=5 (BOTH engines) via
  the H_1012 `prove_mirrors_at_n(4)` + `prove_mirrors_at_n(5)` (which captures LIVE
  `hexa run` stdlib refs); mirror uses BITS/log2 MI=H(A)+H(B)-H(A,B) (H_1043 nats-bug lesson).
- REUSE H_1051 T-machinery (`_provenance_depth` H_932 + `_veto_capacity` H_935) UNMODIFIED +
  the H_1035/H_1047 policy battery + `loo_nearest_centroid_accuracy` LOO protocol VERBATIM.
- Confirm a **reproduce-check** against H_1047's published numbers (REPRODUCE-H_1029 EXACT +
  greedy faith=0.5069 big=9.5283) BEFORE scoring.
- p3/p6/p7: generic toy policies, no persona. TOY n<=5, NO GPU/pod. real-module import; SERIAL
  only — NO unguarded multiprocessing.Pool (H_1038 hang lesson); `if __name__`-guard.
- $0 CPU-local.
- **a_scale_honest_scope**: toy n<=5 rung; scale-transfer UNVERIFIED. g5/p7.

artifacts: `UNIVERSE/h1060_ruler_completeness_phi_t.py` ·
`.verdicts/1060_ruler_completeness_phi_t/H_1060.txt`
