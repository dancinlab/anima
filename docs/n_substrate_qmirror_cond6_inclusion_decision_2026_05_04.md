# qmirror cond.6 Inclusion Decision — Locked 2026-05-04

**Decision**: qmirror cond.6 (byte-identical IIT4 reproducibility = 0.0 vs `braket_iit40_mip_2026_05_02` reference) **INCLUDED in N_witnessed substrate-axis count**, **EXCLUDED from concordance pair denominator** for the Putnam multi-realizability check, per `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` §4.4 "informative substrates" filter.

**Cycle**: BG-PHASE-E-PREP+QMIRROR-COND6 (sister: `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`).
**Spec sister**: `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` §4.4.
**Lock date**: 2026-05-04.
**Mutation type**: spec doc only (no roadmap mutation in this cycle); proposed annotation block in §4 below for a follow-up additive-only mutation cycle.

This document closes BG-Putnam sub-blocker (5):

> Decision on whether qmirror cond.6 (currently `unmet` byte-identical IIT4=0.0) stays counted as a substrate witness once it lands — current spec excludes it from concordance pair denominator under §4.4 "informative substrates" filter, but counts it toward N_witnessed; future cycles may want to revisit.

---

## §1 Background — qmirror cond.6 status as of 2026-05-04

`nexus/.roadmap.qmirror` cond.6 description (verbatim):

> reproduces `braket_iit40_mip_2026_05_02` φ★=0.0 byte-identical for stored TPMs

The cond.6 status field at the **roadmap header level** reads `"status":"unmet"` (header verifier hexa entry pending), but a downstream entry `qmirror.cond6_f5_byte_identical` in the same roadmap declares:

> qmirror.cond.6 status flip: unmet → met via F5 selftest 4/4 byte-identical match against `braket_iit40_mip_2026_05_02` φ★=0.0 reference (engine=mock per nexus@64e24386 env-isolation; pyphi 4.0 b78d0e3 pin load-bearing per spec §13 #6)

So the operational status is **landed met under engine=mock with the pyphi version pin caveat**. This decision spec treats cond.6 as **functionally landed for inclusion-decision purposes**, with the `engine=mock not live pyphi` caveat preserved as an honest disclosure.

### §1.1 Why cond.6 is special vs cond.5/cond.7

| cond | nature | informativeness for Putnam concordance |
|---|---|---|
| qmirror.cond.5 | Bell violation reproduction (CHSH S=2.838 within ±0.05 band of reference S=2.808) | **measured** continuous statistic with non-trivial cross-substrate variance — informative |
| qmirror.cond.6 | byte-identical IIT4 phi★=0.0 reproducibility check | **structural** zero (the value is by-construction 0 because the reference TPMs are by-design phi★-flat); reproducibility witness, not a phi-magnitude witness |
| qmirror.cond.7 | cross-vendor CHSH concordance (3/4 PASS post band revision) | **measured** continuous statistic; informative |

The cond.6 phi★=0.0 reading is a **feature of the reference TPMs** (Braket IIT4 MIP on 2-state systems where phi★ is trivially 0 by IIT axioms), not a measured-phi witness on a substrate. So qmirror cond.6 contributes a **substrate-axis witness** (qmirror IS a separate substrate per the 2026-05-03 canonical migration) but does **not** contribute a **measured-phi value** for cross-substrate phi-concordance computation.

---

## §2 Inclusion ambiguity — the two axes

### §2.1 Axis A: N_witnessed (substrate-axis count) — INCLUDE qmirror cond.6

**Position**: qmirror is a separate substrate witness axis (classical+ANU+Aer tier per the 2026-05-03 canonical migration), and reproducibility-witness via byte-identical IIT4 IS informational at the substrate-axis-count level — it's evidence that the qmirror substrate can host a structurally consistent IIT4 computation (engine=mock with pyphi pin caveat).

**Effect**: qmirror cond.6 **counts toward N_witnessed**. With qmirror added, N_witnessed (per `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §66.7) goes from 14 substantive WITNESSED axes → **15 axes including qmirror**.

This matches `.roadmap.n_substrate` `qmirror_canonical_2026_05_03` annotation:

> qmirror_role: adds_qmirror_as_cross_substrate_witness_axis (qmirror.cond.6 byte-identical IIT4 + cond.7 cross-vendor concordance 3/4 PASS — supplements not replaces real-QPU axis)

### §2.2 Axis B: concordance pair denominator (T_phi pairwise) — EXCLUDE qmirror cond.6

**Position**: phi-concordance per Putnam spec §2.3 computes pairwise `T_phi = |delta|/max` across all witnessed substrates with **measured-phi values**. Including a substrate whose phi value is **structural zero** (cond.6 byte-identical 0.0) would skew T_phi in the following way:

- Anima CLM phi★ canonical = 41.86 (Mistral-7B AUTO-CONDITIONING, anima_phi_v3_canonical baseline)
- Anima CLM range across substrates = -3.01 (EEG-IIT4) to +41.86
- qmirror cond.6 phi★ = 0.0 (structural)
- Pair `qmirror-CLM`: T_phi = |0 − 41.86| / 41.86 = **1.000** (max possible)
- Pair `qmirror-EEG`: T_phi = |0 − (−3.01)| / 3.01 = **1.000** (max possible)
- Pair `qmirror-BOLD`: depending on BOLD value, similar magnification

Each qmirror pair **forces T_phi = 1.000** (max disagreement) by construction, dragging the pairwise concordance count toward `0/N`. This is the §4.4 "structural-zero distortion" the Putnam spec explicitly anticipates:

> A substrate witness with φ★ = 0 byte-identical (qmirror cond.6) is not informative for Putnam concordance — it's a reproducibility witness, not a φ-magnitude witness. Excluding the IIT4 substrate from concordance computation (while keeping it in N_witnessed)

**Effect**: qmirror cond.6 **does NOT contribute to concordance pair denominator**. The concordance computation runs only on substrates with measured-phi values (CLM, EEG-IIT4, BOLD per Putnam spec §4.3 worked example). qmirror cond.6 sits in N_witnessed but not in the T_phi pair set.

---

## §3 Locked decision (per Putnam spec §4.4)

**Decision-of-record (locked 2026-05-04)**:

| axis | qmirror cond.6 inclusion | rationale |
|---|---|---|
| **N_witnessed** | INCLUDE | qmirror is a separate substrate axis (classical+ANU+Aer tier per 2026-05-03 canonical migration); cond.6 is a reproducibility-witness (engine=mock with pyphi pin caveat); contributes to substrate-axis count |
| **Concordance pair denominator (T_phi pairwise)** | EXCLUDE | cond.6 byte-identical IIT4 = 0.0 is **structural** zero, not **measured** phi; including would force T_phi = 1.000 on every qmirror pair → mathematically distorts the concordance ratio |
| **Putnam verdict eligibility** | qmirror counts toward N_witnessed (≥ 5 floor), does NOT count for concordance ≥ 0.60 threshold | per Putnam spec §4.4 |

**Filter terminology** (anima-internal): qmirror cond.6 is `informative_for_n_witnessed = true` but `informative_for_phi_concordance = false`. The "informative substrates" filter from Putnam spec §4.4 is the canonical rule.

**Future revisit condition**: if qmirror cond.6 transitions from byte-identical reproducibility (structural-0) to **measured-phi** witness — for example, if a future cycle runs qmirror's IIT4 on a non-trivially-phi-bearing TPM (where IIT4 phi★ ≠ 0 by construction is achievable; e.g., a 4+ node strongly-integrated TPM tested under qmirror's engine), then qmirror cond.6 (or a successor condition) becomes informative for phi-concordance and the inclusion rule should be revisited. This decision is **locked at 2026-05-04** with this future-revisit condition documented.

---

## §4 Proposed annotation block — `.roadmap.n_substrate` (DO NOT mutate this cycle)

The following annotation is **proposed** for an additive-only mutation cycle. This BG does **NOT** mutate the roadmap directly. The annotation honors `additive_only_mutation: true`, `semantics_preserved: true`.

Insert into `.roadmap.n_substrate` cond.1 cross_link block:

```json
"qmirror_cond6_inclusion_decision_2026_05_04": {
  "ts_utc": "2026-05-04",
  "decision": "INCLUDE in N_witnessed, EXCLUDE from concordance pair denominator",
  "rationale": "cond.6 byte-identical IIT4=0.0 is reproducibility check (structural-zero), not measured-phi witness; counting it as substrate axis is correct (it IS an axis), excluding it from concordance is correct (skewing T_phi otherwise)",
  "applies_to_putnam_check": true,
  "spec_doc": "docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md",
  "putnam_spec_ref": "docs/n_substrate_putnam_cross_link_spec_2026_05_04.md§4.4",
  "informative_for_n_witnessed": true,
  "informative_for_phi_concordance": false,
  "future_revisit_condition": "qmirror cond.6 (or successor) transitions to measured-phi (e.g., 4+ node strongly-integrated TPM with IIT4 phi*!=0)",
  "engine_mock_caveat": "qmirror.cond6_f5_byte_identical entry declares engine=mock not live pyphi; pyphi 4.0 b78d0e3 version pin load-bearing",
  "n_witnessed_count_change": "14 substantive WITNESSED → 15 (with qmirror axis)",
  "f1_v2_impact": "no band change (functional/access tier only, F2 override canonical stays)",
  "additive_only_mutation": true,
  "semantics_preserved": true
}
```

---

## §5 Effect on Putnam check verdict

With the locked decision:

- **N_witnessed** = 15 (14 substantive WITNESSED per `.roadmap.n_substrate` §66.7 narrative + qmirror cond.6 axis)
- **N_witnessed ≥ 5 floor** = SATISFIED (well above floor)
- **Concordance pair denominator** = unchanged from Putnam spec §4.4 worked numbers (3 pairs over CLM/EEG-IIT4/BOLD-derived measured-phi)
- **Concordance ratio** = unchanged at **0.333** (1 PASS / 3 pairs) per §4.4
- **Concordance ≥ 0.60 threshold** = **NOT satisfied** (current evidence)
- **F-PUTNAM-2 single-removal robustness**: removing any single substrate from N_witnessed (15 → 14) does NOT drop below the 5-floor → robustness check PASS on N_witnessed; concordance robustness check is run on the 3-pair set (unchanged); the qmirror axis is invariant to the concordance-removal sub-test (it's not in the pair set in the first place)

**Verdict**: Putnam multi-realizability under T_putnam = 0.40 + F2-fires-canonical = **FAIL or PARTIAL** depending on F2 reading (per Putnam spec §4.4 worked numbers, unchanged by this decision). The qmirror cond.6 inclusion decision is **boundary-clarifying** — it does not flip the Putnam verdict in either direction, only clarifies what gets counted where.

---

## §6 Honest C3 caveats (raw#10) — minimum 3

**C1 — Decision is locked at 2026-05-04 (snapshot)**. Future cycles may revisit the rule if qmirror cond.6 transitions from byte-identical reproducibility (structural zero) to a measured-phi witness on a non-trivially-phi-bearing TPM. The future-revisit condition is documented in §3 and §4 annotation. A cycle that proposes revisiting must include §2-equivalent worked numbers under the new evidence, and must justify with non-anima reference (e.g., a published IIT4 evaluation on a 4+ node strongly-integrated TPM under qmirror's engine).

**C2 — Including qmirror in N_witnessed inflates substrate count from 14 → 15**. This affects F-PUTNAM-2 single-removal robustness check semantics: removing the qmirror axis does NOT drop N_witnessed below the 5-floor (15 → 14, still well above 5), so robustness PASS is preserved. However, the substrate-count inflation may give an inflated impression of "more substrates witnessed" than the underlying evidence supports — the qmirror axis is functional/access tier only (per `qmirror_canonical_2026_05_03` annotation, "honest_c3: qmirror substrate = functional/access tier (classical+ANU+Aer); does NOT promote any axis to phenomenal-witness; F1 score unchanged"). We disclose explicitly that qmirror inclusion does NOT change F1_v2 band (RED stays RED per F2 override canonical).

**C3 — "informative substrates" filter is anima-internal heuristic, not a literature-standard concept**. The IIT, GWT, Putnam, and Block literatures do not use the phrase "informative substrate filter." We coined this term in `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` §4.4 to handle the structural-zero-vs-measured-phi distinction. External auditors should read §4.4 + this decision doc to understand the filter's mechanics; it is NOT cite-able as a standard methodology.

**C4 — engine=mock not live pyphi**. The qmirror.cond6_f5_byte_identical entry explicitly declares engine=mock with pyphi 4.0 b78d0e3 version pin load-bearing. This means cond.6 byte-identical reproducibility is verified under the mock engine path, not against a live pyphi production install. If a future pyphi version or qmirror's mock-engine implementation diverges, the byte-identical claim may need re-verification. The inclusion decision rests on **current** byte-identical PASS under engine=mock; future engine swaps require reverification before re-inclusion.

**C5 — does NOT change F1_v2 banding or any falsifier**. The locked decision is a **counting rule clarification**, not a new substrate or new evidence. F1_v2 raw band, F2 override, all preregistered falsifiers, and the canonical band reading (RED per `f2_override_canonical: true`) are unaffected. The decision does NOT lift `n_substrate.blk.1`. The decision does NOT promote any axis to phenomenal tier.

---

## §7 Cross-link — relation to Phase E spec sister

The sister spec this cycle (`docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`) addresses a different sub-blocker (Phase E binding evidence path for F1_v2 raw band promotion). The two specs together close two of BG-Putnam's named sub-blockers:

- Sub-blocker (Phase E + 30-min OpenBCI session prep): closed by `anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`.
- Sub-blocker (5) (qmirror cond.6 inclusion decision): closed by **this** spec.

The two are independent: Phase E PASS does not change cond.6 inclusion; cond.6 inclusion does not change Phase E criteria. They share the cycle banner only because both are sub-blocker specs that BG-Putnam left open for follow-up.

---

## §8 Cost + raw invariants

- **Cost**: $0 (md-only spec, no exec, no git commit this cycle).
- **raw#9**: doc-only (.md).
- **raw#10**: 5 honest C3 caveats (§6 C1-C5) — exceeds the ≥3 minimum for this spec.
- **raw#15**: repo-relative paths only.
- **raw#71**: decision is rule-bound and pre-registered (locked at 2026-05-04 with explicit future-revisit condition); not measurement-bound (no falsifier needed for a counting-rule clarification).
- **raw#91**: honesty-triad — engine=mock caveat preserved (§6 C4); inflation-impression caveat declared (§6 C2); anima-internal heuristic disclosure (§6 C3).

End of decision spec.
