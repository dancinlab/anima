# qmirror Canonical Migration — Roadmap Audit + Annotation Landed (2026-05-03)

## §0 Trigger

qmirror closure: cond.7 cross-tech 3/4 PASS (band revised 0.55→0.60, physics-aware), 8 cond met or pending NIST. qmirror is now canonical-substantively-equivalent to real-QPU for: random sampling, CHSH violation up to ~30 qubits, IIT MIP φ★ on stored TPMs, entropy injection.

Sister BG (a8344fe605...) writing closure synthesis — this doc cross-links to that synthesis.

## §1 Scope

Audited all `.roadmap.*` SSOT files for real-quantum-hardware references that should reference qmirror canonical substrate going forward.

- **Scanned**: `/Users/ghost/core/anima/.roadmap.*` + `/Users/ghost/core/nexus/.roadmap.*` + `/Users/ghost/core/hive/.roadmap.*` (60 files total, excluding worktree backups + roadmap_format_fixture)
- **Excluded**: `nexus/.roadmap.qmirror` (canonical reference, not consumer — per constraint)
- **Search terms (word-boundary)**: `quantum | QPU | IonQ | IBM Quantum | Rigetti | Heron | Forte | Aria | Cepheus | CHSH | braket | qiskit-ibm`

## §2 Categorization

| Category | Count | Files |
|---|---|---|
| Replace (real-QPU substitutable by qmirror, semantics-preserving swap) | 0 | — |
| Keep (real-QPU IS the demonstration target) | 2 | `.roadmap.ionq`, `.roadmap.penrose_hameroff` |
| Annotate (cross-link to qmirror as supplementary substrate) | 5 | `.roadmap.qrng`, `.roadmap.sim`, `.roadmap.n_substrate`, `.roadmap.theory_validation`, `.roadmap.anima_physics` |
| Reference (mention but no substrate dependency) | 5 | `.roadmap.anima_engines`, `.roadmap.eeg`, `.roadmap.i1_tribev2_pr`, `.roadmap.substrate_bridge` (anima+nexus) |
| Excluded canonical | 1 | `nexus/.roadmap.qmirror` |

**Why 0 Replace**: every real-QPU-touching cond either (a) is the explicit demonstration target (KEEP — would null the experiment), (b) has historical landed evidence we must preserve per "do not mutate met/closed conds" constraint, or (c) is generic verbiage in goals/cross-links. The honest action is annotate-only.

## §3 Per-File Update Summary

All updates are **additive `qmirror_canonical_2026_05_03` field on the header object** — original cond/evidence/verifier untouched. JSONL parse validated.

### §3.1 Annotate (5)

1. **anima/.roadmap.qrng** — qrng.cond.1 (partial). qmirror_role: canonical entropy substrate for future runs (qmirror.cond.4 drop-in vs HMAC-DRBG). Original IonQ Forte 1 4096-bit evidence (#125 LIVE_QUANTUM_SEED) preserved.
2. **anima/.roadmap.sim** — sim.cond.1 (partial). qmirror_role: canonical simulator substrate (Aer = direct equivalent to SV1 for ≤30 qubit). raw#10 already honest 'NOT real-QPU'; annotation makes the substrate-equivalence explicit.
3. **anima/.roadmap.n_substrate** — n_substrate.cond.1 (partial). qmirror_role: adds qmirror as cross-substrate witness axis (cond.6 byte-identical IIT4 + cond.7 cross-vendor concordance 3/4 PASS). F1 score and 4-event real-QPU evidence trail preserved.
4. **anima/.roadmap.theory_validation** — theory_validation.cond.1 (partial). qmirror_role: adds 4th axis for cheap revalidation. Original 3 axes (Penrose/HoTT/IonQ) untouched.
5. **anima/.roadmap.anima_physics** — anima_physics.cond.1 (partial), `quantum` sub-axis only. qmirror_role: live-HW substitute for the `quantum` substrate sub-axis only (avoids 'aws braket signup endpoint 미연결' blocker). Other 8 substrate axes (analog/cmos/fpga/arduino/photonic/memristor/neuromorphic/thermodynamic) still need their own live-HW paths.

### §3.2 Annotate-Keep (2)

6. **anima/.roadmap.ionq** — ionq.cond.1 (partial). decision: **KEEP_real_qpu_demo_target**. qmirror_relationship: complementary pretest only, NOT substitute. qmirror reproduces CHSH S within statistical band for stored circuits, but ion-trap physics demonstration cannot be done in simulator.
7. **anima/.roadmap.penrose_hameroff** — penrose_hameroff.cond.1 (partial). decision: **KEEP_real_qpu_demo_target**. qmirror_relationship: NOT_APPLICABLE. Aer samples classically from |ψ|²; cannot witness Diosi-Penrose objective collapse threshold. Real superconducting QPU (IBM Open Plan delay primitive) required.

### §3.3 Reference (5, no annotation)

- `.roadmap.anima_engines` — `quantum` is engine type (entanglement entropy compute), runs classically.
- `.roadmap.eeg` — 'ionq + EEG' only in cross-link contributor list.
- `.roadmap.i1_tribev2_pr` — 'Braket QPU' in already-met cond.2 evidence narrative.
- `.roadmap.substrate_bridge` (anima+nexus) — generic 'quantum' verbiage in goal.

## §4 Artifacts

- `state/qmirror_canonical_migration_2026_05_03/audit.json` — full audit + per-file rationale
- `state/qmirror_canonical_migration_2026_05_03/replace_log.jsonl` — 7 annotation actions logged
- `state/qmirror_canonical_migration_2026_05_03/keep_decisions.json` — 2 KEEP rationales
- `state/markers/qmirror_canonical_migration_landed.marker` — landing marker
- 7 modified roadmap files (additive only)

## §5 Honest C3 Caveats (raw#10)

1. **qmirror ≠ real QPU on all axes**. Specifically, qmirror cannot demonstrate (a) wavefunction-collapse-on-physical-superposition required by Penrose-Hameroff Orch-OR test (penrose_hameroff.cond.1), or (b) ion-trap physics signal that gives ionq.cond.1 its substrate-invariance interpretation. Both KEEP, not REPLACE.
2. **Replace decisions are partially subjective**. A future cycle that reads cross-vendor concordance more strictly might re-categorize ionq.cond.1 evidence as qmirror-substitutable; a stricter Penrose-Hameroff reading might require IBM-specific delay primitive that no simulator can fake.
3. **Audit may miss in-line refs in spec docs**. Search was limited to `.roadmap.*` SSOT files. `docs/*.md`, code comments, and non-roadmap state files were NOT swept. Future cycle should extend scope.
4. **Future cycle may need real QPU re-validation**. qmirror cross-tech band (cond.7 0.55→0.60 revised) is post-hoc amendment. If IBM Heron r3 + ZNE closes the cross-tech gap differently, qmirror noise model may need re-fit — at which point IonQ/IBM real-QPU runs (already landed) become re-canonical. This migration is **reversible** by the design of the additive annotation (no in-place mutation of original semantics).

## §6 raw Invariants

- raw#9: STRICT OK — Mac → hexa only, no .py creation. (audit.json/replace_log.jsonl/keep_decisions.json are JSON not .py; roadmap files are .roadmap.* not .py)
- raw#10: 4 honest C3 caveats above
- raw#15: OK — no personal-paths in roadmap content (annotations use repo-relative paths only)
- raw#71: OK — annotations preserve all existing falsifier semantics (no in-place mutation)

## §7 Cost

$0 — pure audit + additive roadmap annotation. No QPU runs.

## §8 Cross-Link

- qmirror canonical spec: `docs/nexus_qmirror_spec_2026_05_03.md`
- qmirror canonical roadmap: `nexus/.roadmap.qmirror` (NOT mutated by this cycle)
- qmirror closure synthesis: sister BG `a8344fe605...` (synthesis doc — link upon land)
- qmirror landed cycle docs (already on disk): `qmirror_cond3_ibm_n1_landed`, `qmirror_cond3_band_revise_landed`, `qmirror_cond7_alpha_landed`, `qmirror_cond8_braket_landed`, `qmirror_crosstech_band_revise_landed` (all `.ai.md` 2026-05-03)
