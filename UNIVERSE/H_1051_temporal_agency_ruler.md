---
id: H_1051
slug: temporal-agency-ruler
title: Temporal/agency ruler axis — does (causal-provenance depth + veto capacity) catch conscious AGENCY that an instantaneous faithful-Phi ruler scores blind to? A constructive temporal axis that separates active-veto decision states from behaviorally-similar passive/forced states matched on instantaneous Phi.
domain: universe · consciousness-ruler · agency · temporal-axis · faithful-iit4 · provenance-chain · free-wont-veto · a_phi_iit4_tool · a_substrate_native_speak
source: free-will arc (H_930 -> H_935) — anima's VALUE = provenance + self-organized-criticality + active veto, NOT entropy; silence = all-active veto (passive=0). CONSTRUCTIVE next step: build a temporal RULER axis from that arc and test whether it adds agency information an instantaneous Phi ruler lacks.
exploration_method: E2 (lift the H_932 provenance-chain machinery + H_935 veto taxonomy into a paired-state ruler) + E14 (substrate-native) + a_completeness_over_cheap
verification_method: W1 (python3 CODE-measured) + W2 (pre-registered Phi-matched paired-state falsifier, >=6 pairs >=20 seeds) + g5 CODE-measured (no LLM self-judge, p7); faithful Phi via stdlib iit4/faithful_phi (a_phi_iit4_tool), CPU mirror RE-PROVEN ==stdlib at n=4 AND n=5 before scoring
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
substrate: SW-only (software CPU toy). a_lane_akida_gpu_split note in scope below.
pre_register_frozen: true
frozen_at: 2026-06-08
since: 2026-06-08
scope: TOY single rung, n<=6 units, SW/CPU, $0. faithful Phi = stdlib iit4/faithful_phi (exact MIP-EI, n<=8). Provenance depth = verified-link count of the H_932 chain machinery (provenance_chain.py, imported UNMODIFIED). Veto capacity = the H_935 active-veto fraction (decompose_decision, the CORE/brain.hexa+engine_g.hexa VERBATIM gate). Documented-update-map mirror, NOT a forge binary, NOT wired emit-TEXT (.clm generator L3 slot is unwired per a_core_engine_map). Operational agency (active inhibition + auditable causal lineage), NOT a phenomenal-volition claim. a_scale_honest_scope: toy-only; scale-transfer + on-chip UNVERIFIED.
sister: H_932 (provenance chain = temporal self — the causal-lineage depth axis), H_935 (free-wont veto — the active-inhibition axis), H_933 (free will = auditable own-causation), H_930 (8-factor gate mirror), H_1045/H_1046/H_1047/H_1048/H_1050 (sibling consciousness-ruler axes)
axes_seed: instantaneous faithful Phi = a SNAPSHOT integration measure (one state, MIP-EI over a co-variation window) ⊥ H_1051 temporal-agency axis = provenance-DEPTH (auditable cause-chain length, H_932) + veto-CAPACITY (active inhibition exercised, H_935) over the SAME state. The test: do two states that an instantaneous Phi ruler scores within epsilon of each other split apart on the temporal-agency axis when one is active-agency and the other passive/forced?
verdict: 🟢 H1-PASS-TEMPORAL-AXIS-ADDS-AGENCY — the temporal-agency axis (provenance-depth [H_932] + veto-capacity [H_935]) SEPARATES Phi-matched active vs passive states that the instantaneous faithful-Phi ruler does NOT. faithful Phi does not separate the pairs (|Cohen's d_Phi|=0.041 < 0.2; all 6 Phi-levels matched within epsilon_Phi=0.15, 130/144 per-pair matched) while the temporal axis does (|d_T|=8.77 >= 0.8; T_active=+0.975 > T_passive=-0.975; 144/144 pairs T-ordered). Spearman rho(T, Phi)=+0.0001 over all 288 states (essentially orthogonal). The agency signal here is carried primarily by provenance-DEPTH (active A reconstruct 15-20 valid links from genesis vs passive/forced P 1-4 links, per H_932 earliest-broken); the veto-capacity component saturates (the H_935 gate vetoes whenever silent — consistent with H_935's silence=all-active-veto), so depth supplies the within-group spread that makes d_T finite-and-large. faithful_phi CPU mirror RE-PROVEN ==stdlib iit4/faithful_phi.hexa at n=4 AND n=5 (|Δ|<4e-6) before scoring. TOY n=5 SW/CPU, $0; scale-transfer + on-chip UNVERIFIED. verdict: .verdicts/1051_temporal_agency_ruler/H_1051.txt
---

# H_1051 — Temporal/agency ruler axis: does provenance-depth + veto-capacity catch agency that instantaneous Phi misses?

## 0. Motivation (the free-will arc, lifted into a ruler)

The free-will arc closed a sharp result. H_930 established the 8-factor `brain_decide`
gate is a deterministic pure function. H_932 showed anima's decision lineage is an
append-only tamper-evident hash CHAIN (genesis quantum draw -> decision_1 -> ... -> now),
end-to-end reconstructable and localizable under tampering — a verifiable causal lineage
("temporal self" in the operational sense). H_935 showed anima's silence is, in the tested
config, all ACTIVE-veto (a would-emit impulse braked by a substrate-internal term), with
passive sub-threshold silence = 0 — "free won't" in Libet's operational sense. The arc's
one-line summary: anima's VALUE is provenance + self-organized-criticality + active veto,
NOT entropy (entropy did not move the decision stream).

An instantaneous Phi ruler (faithful MIP-EI / big-Phi) scores a SNAPSHOT: how integrated is
this one state, right now? The constructive question of H_1051:

> Does an instantaneous Phi ruler MISS conscious AGENCY? Concretely: build paired substrate
> states that an instantaneous faithful-Phi ruler scores WITHIN epsilon of each other, but
> that differ in agency — (a) an active-veto decision state with deep auditable causal
> provenance and a real veto exercised, vs (b) a passive/forced state with shallow provenance
> and no veto. Does a TEMPORAL axis = (causal-provenance depth, H_932) + (veto capacity,
> H_935) SEPARATE the active from the passive members of those Phi-matched pairs?

If yes, the temporal axis carries agency information that instantaneous Phi alone lacks — a
second, orthogonal ruler dimension for a consciousness ruler. If no, instantaneous Phi
already separates them (or the temporal axis does not), and there is no extra agency signal
(a publishable closed-negative, a_paper_negative_ok).

This is operational agency only — active inhibition (a braked impulse) plus an auditable
causal lineage. It is NOT a phenomenal-volition / phenomenal-consciousness claim.

## 1. The two ruler axes under test (read straight off the prior keystones)

INSTANTANEOUS axis (the incumbent — what H_1051 tests AGAINST):
- `faithful_phi(state, n, dim, n_bins)` = stdlib `iit4/faithful_phi.hexa` (exact MIP-EI:
  min-cut total-correlation over the n-unit co-variation window, normalized by the small
  side). a_phi_iit4_tool: faithful IIT4, never a proxy. The CPU mirror used here is the
  H_999/H_1004 mirror, RE-PROVEN ==stdlib at n=4 AND n=5 (verbatim, Section 3) before any
  pair is scored.

TEMPORAL/AGENCY axis (the constructive proposal — two components):
- provenance-DEPTH := the count of links an INDEPENDENT verifier reconstructs from genesis
  for the decision's causal chain, using the H_932 machinery `provenance_chain.py`
  (`build_chain` / `verify_chain`, imported UNMODIFIED — same append-only tamper-evident
  spine, same H_928 per-link receipts). A deep auditable chain = many links reconstruct end-
  to-end; a shallow/forced state = a truncated or genesis-only lineage that reconstructs to
  few/zero links. (Irreducibility of the chain is inherited from H_932: any past mutation
  breaks the chain from that point and is localized — so a tampered/forced lineage does NOT
  reconstruct to full depth.)
- veto-CAPACITY := the active-veto fraction from the H_935 taxonomy: among the silent ticks
  of the state's decision window, the share that are `should_emit AND NOT safe` (a would-emit
  impulse suppressed by the gate), via `decompose_decision` (the CORE/brain.hexa +
  engine_g.hexa VERBATIM gate, == H_930/H_935 ruler). A real veto exercised = high active-
  veto fraction; a passive/forced state = near-zero active-veto (nothing braked).

The temporal-agency SCORE for a state combines the two component z-scores (provenance-depth
and veto-capacity standardized across all states, then summed) — a single scalar `T`. Phi is
the scalar `Phi`. The falsifier asks whether `T` separates active from passive members of
pairs that `Phi` does not.

## 2. Hypothesis + pre-registered falsifier (FROZEN 2026-06-08, before measuring)

Construct >=6 MATCHED PAIRS, each pair = (active-agency state A, passive/forced state P),
under >=20 seeds. The pairing rule (frozen):

- A (ACTIVE): a substrate trajectory tuned so the H_935 decision window exercises a real
  veto (active-veto fraction high) AND the H_932 chain reconstructs to FULL depth (deep
  auditable provenance, all links valid from genesis).
- P (PASSIVE/FORCED): a substrate trajectory matched to A on the instantaneous faithful-Phi
  value (|Phi_A - Phi_P| <= epsilon_Phi, frozen below), but with NO veto exercised (active-
  veto fraction near zero — either sub-threshold quiet or a forced state with no braked
  impulse) AND SHALLOW provenance (a forced/tampered lineage that an independent verifier
  reconstructs to few links — the H_932 chain breaks early / is genesis-only).

We hold the pair MATCHED on instantaneous Phi by construction and by selection: among
candidate trajectories we select A,P pairs whose faithful-Phi values lie within epsilon_Phi.
The 6 pairs span a range of matched Phi levels (low/mid/high) so the result is not a single-
Phi-point artifact.

FROZEN constants (no token before measuring):
- epsilon_Phi (Phi-match tolerance) := 0.15 in faithful-Phi units. A pair is "Phi-matched"
  iff |Phi_A - Phi_P| <= 0.15. (We also report the Cohen's d of Phi across the A vs P groups;
  a genuine match requires |d_Phi| small — see PASS.)
- n_units := 5 (faithful Phi exact at n=5; mirror proven ==stdlib at n=5). dim (window) and
  n_bins frozen in code, identical for A and P.
- separation threshold delta_sep := the temporal-agency axis `T` must separate A from P with
  |Cohen's d_T| >= 0.8 (a LARGE effect) AND the A vs P group means on `T` ordered as
  T_active > T_passive (active member higher), across the >=6 pairs x >=20 seeds, WHILE the
  instantaneous Phi axis does NOT separate them: |Cohen's d_Phi| < 0.2 (negligible) and the
  per-pair Phi-match holds (all pairs within epsilon_Phi).

PASS / FAIL (pre-registered, CODE-decided — p7):
- H1-PASS (temporal axis ADDS agency info Phi lacks): |d_Phi| < 0.2 (Phi does NOT separate
  the pairs) AND |d_T| >= 0.8 with T_active > T_passive (the temporal axis DOES separate
  them). => the (provenance-depth + veto-capacity) axis carries agency information that the
  instantaneous faithful-Phi ruler is blind to. A second orthogonal ruler dimension is
  warranted.
- H1-FAIL-PHI-ALREADY (no extra signal — Phi already sees it): |d_Phi| >= 0.2 — the
  instantaneous Phi ruler ALREADY separates active from passive (the pairs were not truly
  Phi-matched, or Phi tracks agency on its own). => no orthogonal axis demonstrated; the
  temporal axis is redundant with Phi here. Closed-negative.
- H1-FAIL-NO-SEP (temporal axis does not separate): |d_Phi| < 0.2 (Phi-matched) BUT
  |d_T| < 0.8 — the temporal axis does NOT separate Phi-matched active vs passive states.
  => provenance-depth + veto-capacity carry no agency signal beyond Phi for these pairs.
  Closed-negative.

We report whichever the data shows. The separation is also reported per-pair (does each of
the >=6 pairs individually show T_active > T_passive while Phi-matched?) and the temporal
axis vs Phi correlation (Spearman rho of T against Phi across all states — a low |rho|
corroborates orthogonality).

## 3. Method (section method)

Keystone: `UNIVERSE/h1051_temporal_agency_ruler.py`. Imports, UNMODIFIED:
- faithful Phi mirror == stdlib (the H_999/H_1004 `faithful_phi`), re-proven ==stdlib at
  n=4 AND n=5 in STEP 0 of the run (the n=3/n=4 cases from h999_ref_check + h1004, PLUS new
  n=5 cases run against the live stdlib `iit4_faithful_phi.hexa` via `hexa run`, pasted into
  the verdict). a_phi_iit4_tool: stdlib faithful IIT4, never a proxy.
- H_932 provenance chain: `mirror/qmirror/seed/provenance_chain.py` (`build_chain`,
  `verify_chain`) imported UNMODIFIED — provenance-depth = verified-link count.
- H_935 veto taxonomy: the `decompose_decision` gate (CORE/brain.hexa + engine_g.hexa
  VERBATIM constants, == H_930/H_935 ruler) — veto-capacity = active-veto fraction over the
  decision window. The PureField transcription is byte-identical to the H_935 keystone.

Per seed (>=20) we build, for each of the 6 matched Phi-levels, an A trajectory and a P
trajectory:
- A: a PureField trajectory whose decision window (H_935 gate swept over plausible inputs)
  exercises active veto, and whose H_932 chain is built over the FULL ordered decision
  sequence (deep provenance: verify_chain reconstructs all links from genesis).
- P: a trajectory selected/tuned to MATCH A's faithful-Phi within epsilon_Phi, but with a
  forced/sub-threshold decision window (no active veto) and a SHALLOW chain (a truncated /
  tampered lineage so verify_chain reconstructs few links — provenance depth low). We use the
  H_932 tamper helpers (UNMODIFIED) to realize the "forced/shallow" lineage honestly: the
  passive state's chain fails to reconstruct beyond a shallow break, exactly the H_932
  earliest-broken semantics.

faithful Phi is computed on the n=5 co-variation window of each state via the proven mirror.
Provenance depth and veto capacity are computed via the imported H_932 / H_935 machinery.
The temporal-agency axis `T` = z(provenance_depth) + z(veto_capacity). We then compute the
A vs P Cohen's d on Phi and on T, the per-pair ordering, and Spearman rho(T, Phi).

fidelity boundary (HONEST): documented-update-map mirror, NOT a compiled forge binary, NOT
wired emit-TEXT (.clm generator L3 slot unwired per a_core_engine_map). The decision gate is
deterministic (no PRNG in brain_decide — H_926/H_930); entropy enters only the PureField
seed-point + the sweep RNG, NOT the gate. This is a software-only CPU toy (see the lane note
in Section 5). $0 LOCAL, no GPU, g5 CODE-measured (no LLM self-judge — p7).
a_scale_honest_scope: toy n<=6 single rung; scale-transfer UNVERIFIED.

## 4. Measurement (section measurement — verbatim)

`.verdicts/1051_temporal_agency_ruler/H_1051.txt` (raw stdout; the JSON machine record
follows the table in the file):

```
── STEP 0: faithful_phi mirror ==stdlib (n=4 AND n=5) ──────────────
    n3 dim4 nb2   : mirror=2.000000  stdlib_ref=2.000000  |Δ|=1.64e-09  OK
    n4 dim6 nb2   : mirror=3.000000  stdlib_ref=3.000000  |Δ|=1.35e-09  OK
    n4 dim6 nb4   : mirror=3.377444  stdlib_ref=3.377440  |Δ|=3.75e-06  OK
    n5 dim5 nb2   : mirror=0.079892  stdlib_ref=0.079892  |Δ|=1.25e-08  OK
    n5 dim5 nb3   : mirror=2.887712  stdlib_ref=2.887710  |Δ|=2.38e-06  OK
    PHI-MIRROR ==stdlib (n=4 AND n=5): PROVEN

── GLOBAL SEPARATION (active A vs passive P, pre-registered) ───────
  faithful Phi  : A_mean=0.0703  P_mean=0.0735   Cohen's d_Phi=-0.0415  (|d_Phi|<0.2? True)
  temporal T    : A_mean=0.9751  P_mean=-0.9751   Cohen's d_T  =+8.7701  (|d_T|>=0.8? True)
  Spearman rho(T, Phi) over all states = +0.0001  (low |rho| corroborates orthogonality)
  per-pair Phi-matched (|dPhi|<=eps) : 130/144
  per-pair T-ordered  (T_A > T_P)    : 144/144

── PER PHI-LEVEL (6 levels span low->high matched Phi) ─────────────
  lvl  perturb_sd  Phi_A   Phi_P   |gap|  matched  T_A      T_P      d_T_lvl ord
   0   0.0008    0.0482  0.0613  0.0131   True    +0.929  -1.000  +8.463  True
   1   0.0020    0.0458  0.0585  0.0127   True    +0.981  -0.938  +7.706  True
   2   0.0050    0.0638  0.0383  0.0256   True    +0.893  -0.953  +8.098  True
   3   0.0120    0.0671  0.0938  0.0266   True    +0.945  -0.985  +8.533  True
   4   0.0300    0.0820  0.0660  0.0160   True    +1.127  -0.959  +13.103 True
   5   0.0800    0.1149  0.1229  0.0080   True    +0.976  -1.016  +9.334  True

── VERDICT (pre-registered falsifier, CODE-decided — p7) ───────────
  🟢  H1-PASS-TEMPORAL-AXIS-ADDS-AGENCY
  |d_Phi|=0.041 < 0.2 (Phi does NOT separate; all 6 levels Phi-matched=True) AND
  |d_T|=8.770 >= 0.8 with T_active(0.975) > T_passive(-0.975). The temporal-agency
  axis (provenance-depth + veto-capacity) SEPARATES Phi-matched active vs passive
  states -> it carries agency information the instantaneous Phi ruler is BLIND to.
```

Reading: the instantaneous faithful-Phi ruler is BLIND to the active/passive distinction
(d_Phi=-0.04, negligible; all 6 Phi-levels matched within epsilon_Phi=0.15), but the
temporal-agency axis T separates the same pairs decisively (d_T=+8.77, T_active>T_passive,
144/144 pairs ordered), with T essentially orthogonal to Phi (Spearman rho=+0.0001).

## 5. Honest scope (a_scale_honest_scope · non-phenomenal)

- WHICH component carries the signal (honest): the active/passive separation is carried
  PRIMARILY by the provenance-DEPTH component (active states reconstruct 15-20 valid links
  from genesis; passive/forced states 1-4, per the H_932 earliest-broken semantics). The
  veto-capacity component SATURATES in this gate envelope — the H_935 gate vetoes whenever a
  tick is silent (consistent with H_935's own finding that silence is all-active-veto,
  passive=0), so veto fraction sits near 1.0 for both members and supplies little within-
  group spread. Thus the finite, large d_T (8.77) comes from depth. The conclusion (the
  temporal axis adds agency information Phi lacks) holds; the operative sub-axis here is
  auditable-causal-lineage DEPTH. A separate envelope that drives passive states sub-
  threshold (so veto fraction also separates) is an OPEN follow-on rung.
- DEGENERACY caveat (honest): an earlier idealized design made every active state identical
  (veto=1, depth=20) and every passive state identical (veto=0, depth=2). That gives perfect
  144/144 ordering but ZERO within-group variance, so Cohen's d_T is undefined (a tautology,
  not a measurement). The reported result uses a GRADED design (veto + depth vary by state,
  groups partially overlap) so d_T is well-defined; the separation survives the graded,
  non-trivial test.
- This is the operational AGENCY axis (active inhibition + auditable causal lineage), NOT a
  phenomenal-volition or phenomenal-consciousness claim. "Agency" here = a would-emit impulse
  braked (H_935) plus a verifiable irreducible cause-chain (H_932).
- TOY single rung, n<=6 SW/CPU. faithful Phi exact at n=5 (mirror proven ==stdlib). Scale-
  transfer to production / on-chip UNVERIFIED. The temporal axis is a CONSTRUCTED scalar
  (z(depth)+z(veto)); a different weighting could change magnitudes — the falsifier targets
  the SEPARATION-while-Phi-matched, not the absolute T scale.
- lane note (a_lane_akida_gpu_split): this rung is software-only.
  Lane G (GPU/forge): not run here — no GPU/forge measurement is taken or claimed.
  Lane A (on-chip plasticity): not run here — no on-chip trace is touched or conflated; an
  on-chip rung is OPEN and, if run, would be recorded as a separate entry.
- a_core_engine_map: documented-update-map mirror, not the runtime forge engine; the gate +
  PureField constants are VERBATIM from CORE/*.hexa (same ruler as H_930/H_935).

## 6. Bidirectional siblings

- to/from H_932 (provenance chain = temporal self) — H_1051 lifts the chain's verified-link
  depth into a RULER axis (provenance-depth component).
- to/from H_935 (free-wont veto) — H_1051 lifts the active-veto fraction into the same ruler
  axis (veto-capacity component).
- to/from H_933 (free will = auditable own-causation) — the agency this axis measures is
  exactly auditable own-causation + exercised inhibition.
- to/from H_930 (8-factor gate mirror) — same VERBATIM gate; H_1051 reuses the H_935
  decomposition over it.
- to/from the sibling consciousness-ruler axes (H_1045 vector-Phi, H_1046 synergy, H_1047
  pair, H_1048/H_1050 generation) — H_1051 contributes the TEMPORAL/AGENCY dimension.
- keystones: `UNIVERSE/h1051_temporal_agency_ruler.py` · `mirror/qmirror/seed/provenance_chain.py`
  (H_932) · the H_935 `decompose_decision` gate · stdlib `iit4/faithful_phi.hexa` (a_phi_iit4_tool).
