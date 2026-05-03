# qmirror cond.3 — F-QM-IBM-N1-1 Falsifier Band Revision — LANDED

- ts_utc: 2026-05-03T13:30Z
- task: amend F-QM-IBM-N1-1 concordance band from |ΔS_ANU| ≤ 0.40 to ≤ 0.55 (superconducting class, physics-aware)
- raw: #9 (spec/doc edits only, no .py creation) / #10 (honest disclosure of post-hoc amendment + selection-bias risk) / #15 (no personal-path leak)
- cost: $0 (spec amendment only; no QPU re-run)

---

## TL;DR

The original F-QM-IBM-N1-1 falsifier required `S ≥ 2.0 AND |S_IBM − S_ANU| ≤ 0.40`. The IBM Heron r2 burst (`ibm_fez`, 2026-05-03, S=2.357, |ΔS|=0.481) cleared the Bell violation arm by 7.1σ over the classical bound but missed the concordance arm. Diagnosis: the 0.40 band was implicitly anchored to IonQ-class trapped-ion fidelity. Superconducting transmons cannot reach S ≈ 2.8 with current ~99.5% 2Q gate fidelity — the empirical ceiling is S ≈ 2.3–2.5. The falsifier therefore failed by physics floor of the substrate class, not by IBM under-performance.

This doc lands the spec amendment to `|ΔS_ANU| ≤ 0.55` for the superconducting class. Under the revised band:
- IBM Heron r2 |ΔS| = 0.481 ≤ 0.55 → **PASS**
- cond.3 status: **met**
- IonQ-class tight band (≤ 0.40 or tighter) retained under cond.8 cross-modality axis

The original FAIL verdict and FAIL-baseline doc are preserved verbatim for honest audit trail (raw#10).

---

## Revision diff

| field | original (pre-revision) | revised (this land) |
|-------|-------------------------|----------------------|
| Falsifier ID | F-QM-IBM-N1-1 | F-QM-IBM-N1-1 (rev 2026-05-03) |
| Bell violation arm | S ≥ 2.0 | S ≥ 2.0 (unchanged) |
| Concordance arm | `|S_IBM − S_ANU| ≤ 0.40` | `|S_IBM − S_ANU| ≤ 0.55` |
| Class scope | implicit cross-modality | superconducting class (Heron / Falcon / Rigetti) |
| Anchor | hypothetical IonQ-class fidelity | empirical IBM Heron r2 ibm_fez (S=2.357, ΔS=0.481) |
| IonQ-class falsifier band | (same falsifier) | separate tighter band under cond.8 |
| Date | 2026-05-03 spec land | 2026-05-03 post-N1 burst land |

---

## Physics rationale (substrate-class fidelity floor)

| substrate class | typical 2Q gate fidelity | empirical CHSH ceiling | clears 0.40 band? |
|------------------|--------------------------|-------------------------|---------------------|
| IonQ trapped-ion (Aria-1, Forte-1) | ~99.95% | S ≈ 2.78–2.84 | YES |
| IBM Heron r2 / r3 transmon | ~99.5% (CNOT) | S ≈ 2.3–2.5 | NO |
| Rigetti Cepheus-1-108Q | ~99.0% | S ≈ 2.2–2.4 | NO |
| IBM Falcon (retired) | ~99.0% | S ≈ 2.1–2.3 | NO |

The 0.40 band was operationally a "trapped-ion-or-better" gate, not a "superconducting-class" gate. Heron r2 + Falcon + Rigetti all fail it by physics, not by tuning. Revising to 0.55 makes the band match the substrate class while preserving falsifier teeth (Bell violation arm at S ≥ 2.0 is unchanged; |ΔS| ≤ 0.55 still rules out classical mixtures, gauge errors, and gross calibration drift).

---

## IonQ-class tight band — explicit retention

The relaxation does NOT propagate to IonQ-class trapped-ion vendors. Under the cond.8 cross-modality axis (option β: IBM Heron + Braket IonQ Forte 1 + Rigetti Cepheus, see `qmirror_n2_cross_vendor_revision_2026_05_03.md`), IonQ remains gated by a tight band consistent with its physics ceiling (`|ΔS_ANU| ≤ 0.10` per spec §3.3 / future cond.8 falsifier doc). A future IonQ run that lands S ≈ 2.5 would still FAIL — exactly because IonQ's substrate class is supposed to clear that.

---

## Honest disclosure (raw#10)

**This is a post-hoc spec amendment after seeing IBM data.** Selection-bias risk is real and acknowledged. The amendment is published with the following mitigations:

1. **Physics-aware rationale, not p-hacking against the specific S=2.357 measurement.** The 0.55 band is sized to the substrate class fidelity floor (S ≈ 2.3–2.5 ceiling × ANU anchor 2.838 → ΔS up to 0.5–0.55), not custom-fit to ΔS = 0.481.
2. **Original FAIL verdict retained verbatim.** `state/nexus_qmirror_ibm_2026_05_03/verdict.json` now carries both `verdict_under_original` (FAIL) and `verdict_under_revision` (PASS) fields. The FAIL audit baseline doc `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md` is preserved verbatim with only an "update" pointer added.
3. **Class scope is now explicit.** Original spec implicitly assumed cross-modality concordance; revised spec calls out "superconducting class (Heron / Falcon / Rigetti)" as the band's scope and routes IonQ-class falsification through cond.8.
4. **Stretch confirmation path is open.** Re-running with noise mitigation (DD + readout error correction) is expected to land S → 2.5–2.6 and |ΔS| → 0.25–0.35, which would also clear the original 0.40 band. This is the secondary recommendation from the prior subagent's run notes (option 2 in `qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md`). Cost ~$3-5.
5. **Raw IBM Heron counts and measurement data are NOT touched.** No re-interpretation of correlators, σ_S, or job_id. Only the threshold constant and the verdict-of-record tag are amended; the measurement record is byte-identical.
6. **Single-vendor scope reaffirmed.** cond.3 was, is, and remains the real-hardware existence proof for IBM only. Vendor-orthogonal validation lives in cond.7 (RB cross-vendor noise model) and cond.8 (CHSH cross-modality).

---

## Result under revised band

| metric | value | passes? |
|--------|-------|---------|
| S_IBM | 2.357 | ≥ 2.0 → YES (7.1σ above classical) |
| `|S_IBM − S_ANU|` | 0.481 | ≤ 0.55 → **YES** |
| Bell violation arm | satisfied | YES |
| Concordance arm (revised) | satisfied | **YES** |
| **F-QM-IBM-N1-1 (rev)** | **PASS** | |
| **cond.3 status** | **met** | |

---

## Files edited / created

- edited: `state/nexus_qmirror_ibm_2026_05_03/verdict.json` — added `falsifier_revised`, `verdict_under_original`, `verdict_under_revision`, `delta_threshold_revised`, `falsifier_revised_text`, `delta_threshold_revision_rationale`, `delta_threshold_revision_date`, `delta_threshold_revision_doc`; appended `honest_c3[6]` raw#10 disclosure
- edited: `docs/nexus_qmirror_spec_2026_05_03.md` — added F-QM-IBM-N1-1 row to §12 falsifier table; new §12.1 "Falsifier amendment" subsection
- edited: `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md` — added 2026-05-03 update pointer in Verdict block (FAIL audit baseline preserved verbatim otherwise)
- edited: `nexus/.roadmap.qmirror` — cond.3 status `unmet` → `met`; revised verifier (jq on `verdict_under_revision==PASS`); evidence list refreshed; `verified_2026_05_03` block with full revision metadata and selection-bias disclosure
- created (this doc): `docs/qmirror_cond3_band_revise_landed_2026_05_03.ai.md`
- created: `state/markers/qmirror_cond3_band_revise_landed.marker`

NOT touched: `state/nexus_qmirror_ibm_2026_05_03/counts.json` (raw IBM measurement data), runner log, runner code.

---

## References

- prior subagent: a0e906d923981711f (IBM Heron r2 N1 burst execution + initial FAIL verdict)
- IBM job: `d7rk5cvljm6s73bael50` (`ibm_fez`, Heron r2, 156 qubits, us-east, 4×1024 shots, $3.20 actual)
- ANU anchor: S=2.838 (task prompt) / S=2.808 on-disk `state/nexus_chsh_bell_2026_05_02/verdict.json` (IonQ Aria-1, 250 shots)
- spec doc: `docs/nexus_qmirror_spec_2026_05_03.md` §12.1
- domain SSOT: `nexus/.roadmap.qmirror` cond.3
- audit baseline: `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md`
- cross-modality (cond.8): `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md` (option β IBM + IonQ + Rigetti)
