# qmirror Spec Doc Cross-Reference Update — LANDED (2026-05-03)

- ts_utc: 2026-05-03
- agent: `qmirror_spec_xref_update`
- mode: doc-only annotation pass (additive paragraphs + References sections)
- budget: $0
- constraints: raw#9 hexa-only · raw#10 honest C3 · raw#15 no-personal-paths
- companion: roadmap migration BG (parallel cycle)

---

## Mission

After `nexus.qmirror` was validated as substantively equivalent for our use cases (closure series 2026-05-03), audit anima's `docs/*.md` for spec docs that reference real quantum hardware as an execution dependency, and annotate them with cross-links to the qmirror canonical substrate.

**Key principle**: additive only. No deletion of historical QPU mentions, no semantic mutation, no measurement data touched.

---

## Audit summary

| Metric | Value |
|---|---|
| `docs/*.md` total | 1,369 |
| Pattern-matched docs (`quantum\|QPU\|IBM Quantum\|IonQ\|Rigetti\|Heron\|Aer\|Bell test\|CHSH\|qiskit\|braket`) | 103 |
| Substrate-dependency (UPDATED) | 7 |
| Closure-related (skipped — self-reference) | 10 |
| Closed-historical (preserved unchanged) | 21 |
| Methodology-reference (no change — concept, not substrate) | 65 |

Full categorization: `state/qmirror_spec_xref_update_2026_05_03/audit.json`.

---

## Per-category action

### Substrate dependency (7 docs UPDATED)

Each got an additive `> **2026-05-03 qmirror substrate update (additive)**: ...` paragraph after the header / status block, plus a `## References (qmirror substrate xref, added 2026-05-03)` section appended to the bottom with cross-links to relevant qmirror anchors.

| Doc | Reframing |
|---|---|
| `n_substrate_n12_quantum_pivot_2026_05_01.md` | IBM/IonQ/Rigetti rankings → calibration anchors only |
| `n_substrate_n12_ionq_penrose_hameroff_spec_2026_05_01.md` | IonQ Forte 1 path → historical methodology |
| `n_12_v3_ibm_quantum_prep_2026_05_01.md` | IBM Heron r2 prep → calibration anchor only |
| `n_substrate_n12_aws_prep_2026_05_01.md` | Braket launch artifacts → optional anchor |
| `n_substrate_n13_photonic_iit_spec_2026_05_01.md` | photonic-quantum vendor overlap → covered by qmirror |
| `ibm_cloud_experiment_list_2026_05_03.md` | already qmirror-anchored R3+; added References section + framing note |
| `ibm_cloud_env_setup_runbook_2026_05_03.md` | already qmirror-aligned; added References section + framing note |

### Closure-related (10 docs SKIPPED)

These ARE the canonical xref target. Adding "see qmirror" inside qmirror docs is circular.

### Closed historical (21 docs PRESERVED)

Landed cycle reports documenting actual real-QPU runs (n12 IonQ Forte 1 PASS WITNESSED $16.60, IIT 4.0 MIP, etc.). These are the substantive-equivalence evidence base for qmirror itself — modifying them would corrupt the historical record.

### Methodology reference (65 docs NO CHANGE)

Docs that use `quantum` / `CHSH` / `Bell` / `qiskit` as concept references (post-quantum crypto threat models, abstraction ladders, paper outlines, RNG abstractions). No real-QPU execution dependency.

---

## Honest C3 caveats (raw#10)

1. **Categorization is subjective**. The boundary between "substrate dependency" and "methodology reference" is judgment-based — a few docs (e.g. `n_substrate_n13_photonic_iit_spec` for the photonic-classical analog axis) sit on the line. Inclusion in the "substrate dependency" bucket reflects axis-overlap risk with quantum-photonic vendors covered by qmirror, even though N-13's primary scope is classical optical compute.

2. **Audit may miss inline references**. The grep pattern (`quantum|QPU|IBM Quantum|IonQ|Rigetti|Heron|Aer|Bell test|CHSH|qiskit|braket`) is a finite keyword list. Docs that reference quantum hardware via paraphrase (e.g. "trapped-ion vendors", "the 156q chip"), via inline state file paths only, or via vendor-internal jargon may have been missed. Categorization rests on header-only inspection for most docs in the methodology bucket.

3. **Additive paragraphs grow doc size**. Each updated doc gained ~80–200 words of additive content (top-of-doc paragraph + bottom References section). For the 7 updated docs the cumulative addition is non-trivial; over many xref passes this can accumulate. Mitigation: kept additions concise and localized to top header + bottom References to avoid mid-doc interruption.

---

## Deliverables

| Artifact | Path |
|---|---|
| Audit JSON (full categorization) | `state/qmirror_spec_xref_update_2026_05_03/audit.json` |
| Update log (per-doc actions) | `state/qmirror_spec_xref_update_2026_05_03/update_log.jsonl` |
| Kept decisions (closed historical / closure-related rationale) | `state/qmirror_spec_xref_update_2026_05_03/kept_decisions.json` |
| Marker | `state/markers/qmirror_spec_xref_update_landed.marker` |
| This handoff | `docs/qmirror_spec_xref_update_landed_2026_05_03.ai.md` |

---

## Cross-links

- `docs/nexus_qmirror_spec_2026_05_03.md` — qmirror canonical substrate spec
- `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` — Phase 3 calibration runbook
- `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md` — N2 cross-vendor revision
- `docs/qmirror_cond3_band_revise_landed_2026_05_03.ai.md` — band revise closure
- `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md` — IBM N1 calibration closure
- `docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md` — alpha-axis closure
- `docs/qmirror_cond8_braket_landed_2026_05_03.ai.md` — Braket cross-vendor closure
- `docs/qmirror_crosstech_band_revise_landed_2026_05_03.ai.md` — cross-tech band revise

**status**: LANDED
**verdict_key**: SPEC_XREF_PASS_COMPLETE · 7_DOCS_ANNOTATED · 21_HISTORICAL_PRESERVED · ZERO_DATA_MUTATION
