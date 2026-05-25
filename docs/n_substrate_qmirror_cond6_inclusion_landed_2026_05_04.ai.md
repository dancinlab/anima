# qmirror cond.6 Inclusion Decision — landed 2026-05-04 (1-page handoff)

**Spec**: `docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md`
**Cycle**: BG-PHASE-E-PREP+QMIRROR-COND6 (sister: Phase E EEG live session prep).
**Status**: LOCKED 2026-05-04.
**Sub-blocker addressed**: BG-Putnam sub-blocker (5) — qmirror cond.6 inclusion ambiguity.

## What landed (decision-of-record)

| axis | qmirror cond.6 | rationale |
|---|---|---|
| **N_witnessed (substrate-axis count)** | **INCLUDE** | qmirror is a separate substrate axis (classical+ANU+Aer per 2026-05-03 canonical migration); cond.6 is a reproducibility-witness with engine=mock + pyphi 4.0 b78d0e3 pin caveat |
| **Concordance pair denominator (T_phi pairwise)** | **EXCLUDE** | cond.6 byte-identical IIT4 = 0.0 is **structural** zero, not **measured** phi; including would force T_phi = 1.000 on every qmirror pair, mathematically distorting the concordance ratio |

**Filter terminology** (anima-internal): qmirror cond.6 is `informative_for_n_witnessed = true`, `informative_for_phi_concordance = false`. Per `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` §4.4 "informative substrates" filter.

## Effect on Putnam verdict

- N_witnessed: 14 substantive WITNESSED → **15** (with qmirror axis); ≥ 5 floor satisfied with margin.
- Concordance ratio: **0.333 (1/3 pairs PASS)** unchanged from Putnam spec §4.4 worked numbers — qmirror not in pair set.
- Concordance ≥ 0.60 threshold: **NOT satisfied** (current evidence).
- F-PUTNAM-2 single-removal robustness: PASS on N_witnessed (15 → 14 still well above 5-floor); concordance robustness on 3-pair set unchanged.
- **Putnam verdict**: FAIL or PARTIAL depending on F2 reading; this decision is **boundary-clarifying**, not verdict-flipping.

## Future-revisit condition

If qmirror cond.6 (or successor) transitions from byte-identical reproducibility (structural zero) to **measured-phi** witness on a non-trivially-phi-bearing TPM (e.g., 4+ node strongly-integrated TPM with IIT4 phi★ ≠ 0), the inclusion rule should be revisited. A revisiting cycle must include §2-equivalent worked numbers under new evidence + non-anima reference justification.

## Proposed annotation block (DO NOT mutate this cycle)

For an additive-only mutation cycle, insert into `.roadmap.n_substrate` cond.1 cross_link block:

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

## Honest C3 (5 caveats)

C1 decision is locked-snapshot at 2026-05-04 with explicit future-revisit condition. C2 substrate-count inflation 14 → 15 may give inflated-impression vs evidence (qmirror is functional/access tier only; F1_v2 RED stays RED). C3 "informative substrates" filter is anima-internal heuristic, not standard literature concept. C4 engine=mock + pyphi 4.0 b78d0e3 pin load-bearing — future engine swaps require reverification. C5 decision does NOT change F1_v2 band, any falsifier, or any phenomenal-tier reservation; it is a counting-rule clarification only.

## Cross-link — sister Phase E spec

Phase E EEG live session prep spec (`docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`) addresses a different sub-blocker (F1_v2 raw band promotion path). The two specs together close two of BG-Putnam's named sub-blockers; they are independent (Phase E PASS does not change cond.6 inclusion; cond.6 inclusion does not change Phase E criteria).

## Raw invariant compliance

raw#9 (md only, no roadmap mutation, no exec). raw#10 (5 caveats). raw#15 (repo-relative paths). raw#71 (rule-bound + pre-registered with future-revisit condition). raw#91 (honesty-triad: engine=mock, inflation-impression, anima-internal-heuristic disclosures all explicit).
