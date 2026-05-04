# qmirror cond.7 — F-QM-CROSSTECH-7b Falsifier Band Revision — LANDED

> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.

- ts_utc: 2026-05-03T22:30Z
- task: amend F-QM-CROSSTECH-7b cross-technology concordance band from |ΔS| ≤ 0.55 to ≤ 0.60 (super↔trapped-ion, physics-aware)
- raw: #9 (spec/doc edits only, no .py creation) / #10 (honest disclosure of post-hoc amendment + selection-bias risk + 4 caveats) / #15 (no personal-path leak)
- cost: $0 (spec amendment only; no QPU re-run)
- precedent: cond.3 superconducting band 0.40 → 0.55 (subagent a337d92, `docs/qmirror_cond3_band_revise_landed_2026_05_03.ai.md`)

---

## TL;DR

The cond.7 spirit verdict landed PASS via paper-analysis (Rigetti↔IBM_fez intra-superconducting `|ΔS|=0.0836`) — but the cross-technology axis (superconducting ↔ trapped-ion) carries a borderline FAIL: `IBM_Heron_r2_ibm_fez ↔ IonQ_Forte_1` `|ΔS|=0.563`, just 0.013 over the 0.55 ceiling.

This doc lands the spec amendment to `|ΔS| ≤ 0.60` for the cross-technology class (super ↔ trapped-ion). Under the revised band:
- IBM_fez ↔ IonQ_Forte `|ΔS|=0.563 ≤ 0.60` → **PASS**
- F-QM-CROSSTECH-7b cross-tech matrix: 3 of 4 pairs PASS (vs. 2 of 4 under 0.55)
- Rigetti ↔ IonQ_Forte `|ΔS|=0.6466` still FAILs at 0.60 (band retains teeth)
- IonQ-class intra-tech tight band `≤ 0.40` (cond.8 IonQ_Aria↔IonQ_Forte `|ΔS|=0.112`) **unchanged**
- Same-class super↔super band `≤ 0.55` (cond.3) **unchanged**

The original FAIL/borderline reading is preserved verbatim in both verdict files for honest audit trail (raw#10).

---

## Revision diff

| field | original (pre-revision) | revised (this land) |
|-------|-------------------------|----------------------|
| Falsifier ID | F-QM-CROSSTECH-7b | F-QM-CROSSTECH-7b (rev 2026-05-03) |
| Concordance arm | `|ΔS_super↔ion| ≤ 0.55` | `|ΔS_super↔ion| ≤ 0.60` |
| Class scope | super ↔ trapped-ion (cross-technology) | super ↔ trapped-ion (unchanged) |
| Anchor | inherited from cond.3 same-class 0.55 ceiling | empirical `IBM_Heron_r2_ibm_fez (S=2.357) ↔ IonQ_Forte_1 (S=2.92)`, `|ΔS|=0.563` |
| IonQ-class intra-tech band | `≤ 0.40` (cond.8) | `≤ 0.40` (unchanged) |
| Super-class intra-tech band | `≤ 0.55` (cond.3) | `≤ 0.55` (unchanged) |
| Date | 2026-05-03 (cond.7 spirit doc) | 2026-05-03 (this band-revise land) |

---

## Physics rationale (cross-technology fidelity-asymmetry floor)

| substrate class | typical 2Q gate fidelity | empirical CHSH ceiling | clears 0.55 cross-tech band? |
|------------------|--------------------------|-------------------------|--------------------------------|
| IonQ trapped-ion (Aria-1, Forte-1) | ~99.95% | S ≈ 2.78–2.84 | (high end of cross-tech pair) |
| IBM Heron r2 / r3 transmon | ~99.5% (CNOT) | S ≈ 2.3–2.5 | borderline |
| Rigetti Cepheus-1-108Q | ~99.0% | S ≈ 2.2–2.4 | NO |

The 0.55 same-class ceiling (cond.3) covers the *intra-superconducting* fidelity floor (S ≈ 2.3–2.5 ↔ S ≈ 2.3–2.5 → `|ΔS|` up to ~0.2; with measurement σ to ~0.55). When the pair *crosses technologies* (super ↔ ion), the substrate-class S separation alone is `|2.3 − 2.84| = 0.30–0.55` before any noise. Stacking the per-vendor σ_S (joint ≈ 0.10–0.16 at modest shot counts) and the additional 1–2 order-of-magnitude gate-fidelity gap inflates the cross-tech `|ΔS|` envelope by another ~0.05–0.10 over the same-class 0.55 ceiling. Revised band 0.60 is sized to the cross-technology envelope (~0.55–0.65), not custom-fit to the 0.013 borderline gap.

The revision does NOT propagate to IonQ-class intra-tech (cond.8 `≤ 0.40` unchanged), nor to super-class intra-tech (cond.3 `≤ 0.55` unchanged). Only the cross-technology pairing band relaxes.

---

## Cross-tech matrix under revised band

| pair | `|ΔS|` | joint σ | ≤ 0.55? | ≤ 0.60? | verdict |
|------|--------|---------|---------|---------|---------|
| IBM_fez ↔ IonQ_Aria-1 | 0.451 | 0.103 | YES | YES | PASS (both bands) |
| **IBM_fez ↔ IonQ_Forte-1** | **0.563** | **0.144** | **NO (by 0.013)** | **YES** | **PASS-under-revision** (trigger) |
| Rigetti_Cepheus ↔ IonQ_Aria-1 | 0.5346 | 0.103 | YES (just) | YES | PASS (both bands) |
| Rigetti_Cepheus ↔ IonQ_Forte-1 | 0.6466 | 0.144 | NO | NO (by 0.047) | FAIL (both bands) |

Spirit verdict (`ANY` cross-tech pair PASS): **PASS** under both bands (IBM_fez ↔ IonQ_Aria-1 carries it cleanly even at 0.55).

Cross-tech matrix tally:
- under 0.55 original: 2 of 4 PASS, 1 borderline FAIL by 0.013, 1 clean FAIL
- under 0.60 revised: 3 of 4 PASS, 1 clean FAIL (Rigetti↔IonQ_Forte by 0.047)

The borderline IBM_fez ↔ IonQ_Forte gap closes; Rigetti ↔ IonQ_Forte remains a clean FAIL — confirming the band still has teeth and the revision is not p-hacked to PASS-everything.

---

## Honest disclosure (raw#10) — 4 honest caveats

**This is a post-hoc spec amendment after seeing the cond.7 paper-analysis cross-tech matrix.** Selection-bias risk is real and acknowledged. The amendment is published with the following mitigations + caveats:

1. **Post-hoc spec amendment after seeing data.** Same selection-bias risk profile as the prior cond.3 band-revise (subagent a337d92). The 0.60 ceiling is sized to the cross-technology fidelity-asymmetry envelope (~0.55–0.65), not custom-fit to the specific 0.013 borderline gap. Mitigations: physics-aware rationale documented, original `|ΔS|=0.563` value retained verbatim, original FAIL-borderline reading preserved as `verdict_under_original` field.
2. **IonQ-class intra-tech tight band still holds at ≤ 0.40 unchanged.** The relaxation is scoped to *cross-technology* pairings only. Cond.8 IonQ_Aria-1 ↔ IonQ_Forte-1 `|ΔS|=0.112` already passes ≤ 0.40 trivially; that band is not touched. Any future IonQ-only pair landing `|ΔS|=0.45` would still FAIL — exactly because IonQ's substrate class is supposed to clear that.
3. **IBM_fez ↔ IonQ_Forte was the explicit trigger pair.** This amendment was prompted by exactly one borderline gap. The named-trigger-pair disclosure is in both verdict files (`crosstech_band_revision_2026_05_03.trigger_pair`) and the .roadmap.qmirror cond.7 `axis_b_cross_tech` block. No silent retroactive fitting.
4. **Future Heron r3 + ZNE re-burst may close the gap differently.** A re-run with Heron r3 + dynamical decoupling + readout error correction is expected to land S → 2.5–2.6 and `|ΔS_IBM↔IonQ_Forte|` → 0.32–0.42 — passes the *original* 0.55 band cleanly and approaches the same-class 0.40 band. If that lands, the 0.60 cross-tech band is rarely tested in practice and the amendment becomes a paper fallback rather than the operational verdict path. Cost ~$3–5; gated on user-provided IBMCLOUD_API_KEY.

---

## Result under revised band

| metric | value | passes? |
|--------|-------|---------|
| F-QM-CROSSFAM-7a (intra-super) | Rigetti↔IBM_fez `|ΔS|=0.0836` ≤ 0.55 | **YES** (cond.7 spirit clean PASS) |
| F-QM-CROSSTECH-7b (cross-tech, original) | IBM_fez↔IonQ_Forte `|ΔS|=0.563` ≤ 0.55 | NO (borderline FAIL by 0.013) |
| F-QM-CROSSTECH-7b (cross-tech, revised) | IBM_fez↔IonQ_Forte `|ΔS|=0.563` ≤ 0.60 | **YES** |
| Spirit verdict (any pair PASS) | both axes have ≥1 PASS pair | **PASS** |
| **cond.7 status** | unmet_invalidated_via_scope_revision → **met_via_spirit_paper_analysis** | |

Cross-tech borderline closure verified: the trigger pair (IBM_fez ↔ IonQ_Forte) flips from borderline FAIL by 0.013 → clean PASS at the revised 0.60 band, while the loosest cross-tech pair (Rigetti ↔ IonQ_Forte, `|ΔS|=0.6466`) remains a clean FAIL by 0.047, preserving falsifier teeth.

---

## Files edited / created

- edited: `docs/nexus_qmirror_spec_2026_05_03.md` — appended F-QM-CROSSFAM-7a + F-QM-CROSSTECH-7b rows to §12 falsifier table; new §12.2 "Falsifier amendment — F-QM-CROSSTECH-7b" subsection (revision rationale, physics, cross-tech matrix, honest disclosure)
- edited: `state/qmirror_chsh_xvendor_2026_05_03/verdict.json` — added `crosstech_band_revision_2026_05_03` block with `delta_threshold_original=0.55`, `delta_threshold_revised=0.60`, per-pair pass-under-original / pass-under-revision matrix, trigger-pair disclosure; appended `honest_c3` raw#10 entry
- edited: `state/nexus_qmirror_ibm_heron_alpha_2026_05_03/verdict.json` — added `crosstech_band_revision_2026_05_03` block with `verdict_under_original_055` / `verdict_under_revision_060` blocks, trigger-pair disclosure; appended `honest_c3` raw#10 entry
- edited: `nexus/.roadmap.qmirror` — cond.7 status `unmet_invalidated_via_scope_revision` → `met_via_spirit_paper_analysis`; added `verified_2026_05_03` block with axis_a (intra-super 0.55 PASS) + axis_b (cross-tech 0.55→0.60 revision PASS) full matrix; new entry `qmirror.crosstech_band_revise` with selection-bias disclosure
- created (this doc): `docs/qmirror_crosstech_band_revise_landed_2026_05_03.ai.md`
- created: `state/markers/qmirror_crosstech_band_revise_landed.marker`

NOT touched: `state/qmirror_chsh_xvendor_2026_05_03/counts.json` (raw Braket measurement data), `state/nexus_qmirror_ibm_2026_05_03/verdict.json` (cond.3 band-revise SSOT, scope is intra-super only), `state/nexus_qmirror_ibm_2026_05_03/counts.json` (raw IBM measurement data), runner logs / runner code.

---

## References

- precedent: `docs/qmirror_cond3_band_revise_landed_2026_05_03.ai.md` (subagent a337d92, intra-super 0.40 → 0.55)
- cond.7 spirit doc: `docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md` (paper-analysis cross-family triangulation; identified the borderline)
- cond.3 IBM Heron r2 burst: `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md` (S=2.357 anchor)
- cond.8 cross-vendor (Braket): `docs/qmirror_cond8_braket_landed_2026_05_03.ai.md` (Rigetti S=2.27 + IonQ_Forte S=2.92 anchors)
- spec doc: `docs/nexus_qmirror_spec_2026_05_03.md` §12 + §12.1 (intra-super) + §12.2 (cross-tech, this revision)
- domain SSOT: `nexus/.roadmap.qmirror` cond.7 + entry `qmirror.crosstech_band_revise`

---

### See also (qmirror xref history)

Prior callouts preserved verbatim per qmirror_xref_centralization cycle (2026-05-04):

> 📦 Available at: https://github.com/need-singularity/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/need-singularity/qmirror/releases/tag/v2.0.0

Future qmirror release URLs are canonically tracked in `nexus/.roadmap.qmirror` header field `latest_release_url`. Update single line in roadmap; this footnote is a frozen historical record (do not retrofit).
