# qmirror v2.0.0 ecosystem cross-link — LANDED 2026-05-04

- ts_utc: 2026-05-04
- agent: `qmirror_v2_announcement`
- task: additive cross-link of `qmirror v2.0.0` GitHub release across the anima ecosystem (17 prior xref docs + papers repo entry + n6-architecture README + sim-universe / hexa-bio / honesty-monitor sister READMEs + qmirror community announcement)
- mode: additive only — no v1 reference deletion, no qmirror v2.0.0 source artifact mutation, no count/measurement mutation in target docs
- gate: raw#9 STRICT (Mac → hexa only; no .py touched) · raw#10 (4 honest C3 caveats) · raw#15 (no personal-path leak in added lines)
- cost: $0 (doc-only)
- release: <https://github.com/need-singularity/qmirror/releases/tag/v2.0.0> (closure 13/13 conds met = 8 v1 + 5 v2)

---

## TL;DR

`qmirror v2.0.0` released 2026-05-04 with 5 new substrate axes (cond.9 process tomography + cond.10 GHZ-Mermin + cond.11 stabilizer + cond.12 surface-code d=3 toy + cond.13 chained-sequential CHSH) extending the v1.0 8/8 closure to **13/13 cumulative conds met** (composite verdict `qmirror_2_closure_FULL`, applied = true). This cycle propagates that achievement across the anima ecosystem in **additive-only fashion** — every v1.0 reference is preserved; every v2.0 line stacks below.

| category                                                     | files | action                                                       |
| ------------------------------------------------------------ | ----- | ------------------------------------------------------------ |
| anima docs v2 release line appended                          | 17    | additive line below pre-existing v1 GitHub URL line          |
| n6-architecture README sister-substrates section             | 1     | additive section after Sub-projects, before Community        |
| sim-universe README sister-substrates section + qmirror v2 bump | 1   | additive (in-line bump + new section)                        |
| hexa-bio README cross-links v2 bump + honesty-monitor add    | 1     | bumped existing qmirror entry to v2 release tag              |
| honesty-monitor README sister-substrates section             | 1     | additive section after License                               |
| papers repo PA-39 entry + INDEX.md Cluster 6 add             | 2     | new paper file + new index cluster                           |
| qmirror repo community announcement                          | 1     | new RELEASE_NOTES_v2.0.0_announcement.md (sibling to formal draft) |
| **total files touched**                                      | **24**| 4 created + 20 modified additive; **0 lines removed**        |

---

## Files updated (24)

### anima docs v2 xref appended (17)

All 17 docs share the additive pattern: existing v1 line `> 📦 Available at: https://github.com/need-singularity/qmirror (\`hx install qmirror\`)` preserved verbatim; new line added immediately below:

```
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/need-singularity/qmirror/releases/tag/v2.0.0
```

Inventory (same 17 docs as the v1 xref cycle `qmirror_github_xref` — sister BG `aa6c8c54e` original audit):

#### closure_related (10)

- `docs/nexus_qmirror_spec_2026_05_03.md`
- `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md`
- `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md`
- `docs/qmirror_cond3_band_revise_landed_2026_05_03.ai.md`
- `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md`
- `docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md`
- `docs/qmirror_cond8_braket_landed_2026_05_03.ai.md`
- `docs/qmirror_crosstech_band_revise_landed_2026_05_03.ai.md`
- `docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md`
- `docs/anima_nexus_qrng_dependency_wire_2026_05_03.md`

#### substrate_dependency (7)

- `docs/n_substrate_n12_quantum_pivot_2026_05_01.md`
- `docs/n_substrate_n12_ionq_penrose_hameroff_spec_2026_05_01.md`
- `docs/n_12_v3_ibm_quantum_prep_2026_05_01.md`
- `docs/n_substrate_n12_aws_prep_2026_05_01.md`
- `docs/n_substrate_n13_photonic_iit_spec_2026_05_01.md`
- `docs/ibm_cloud_experiment_list_2026_05_03.md`
- `docs/ibm_cloud_env_setup_runbook_2026_05_03.md`

### n6-architecture README (1)

- `n6-architecture/README.md` — added new `## Sister substrates` section between Sub-projects and Community sections; entries: qmirror v2.0.0 (closure 13/13, Aer integration for n=6 / J₂=24 invariant verification across `n6-quantum-computing-paper.md` + `n6-quantum-error-correction-paper.md` + `n6-quantum-machine-learning-paper.md`), sim-universe v1.0.0, hexa-bio v1.0.0, honesty-monitor v1.0.0.

### sim-universe README (1)

- `sim-universe/README.md` — bumped existing in-line qmirror reference (Cost-comparison-table sister-substrate paragraph) to v2.0.0 release tag with closure 13/13 framing; added new `## Sister substrates` section (qmirror v2.0.0 + hexa-bio v1.0.0 + honesty-monitor v1.0.0).

### hexa-bio README (1)

- `hexa-bio/README.md` — bumped Cross-links section qmirror entry to v2.0.0 release tag with closure 13/13 framing; added honesty-monitor v1.0.0 sister standalone entry. Pre-existing Provenance section already references "qmirror v2.0.0 (registry L22)" — preserved verbatim.

### honesty-monitor README (1)

- `honesty-monitor/README.md` — added new `## Sister substrates` section between License & attribution and Changelog sections; entries: qmirror v2.0.0 + sim-universe v1.0.0 + hexa-bio v1.0.0.

### papers repo (2)

- `papers/anima/PA-39-qmirror-v2-closure.md` — NEW. Full closure summary + 13/13 verdict matrix + per-axis verdict JSON pointers + upstream artifacts + sister-substrate consumer pattern + 4 honest C3 paper-scope caveats + next-steps publication path (refresh draft / peer review / LaTeX / figure prep / counsel sign-off / arXiv submission) + BibTeX citation.
- `papers/anima/INDEX.md` — added new `## Cluster 6: Substrate Achievements` section pointing to PA-39 (category `quant-ph,cs.ET`, status `arXiv draft v0.1 (peer review pending); upstream release LIVE 2026-05-04`).

### qmirror repo (1)

- `qmirror/RELEASE_NOTES_v2.0.0_announcement.md` — NEW community-friendly companion to the formal `RELEASE_NOTES_v2.0.0.md.draft`. Covers: 5 v2 axes summary + why-it-matters + strict additive backward-compat statement + how-to-consume CLI examples + sister substrate ecosystem (4 standalone repos + nexus + anima consumer pattern) + 4 honest C3 community-facing caveats + provenance + BibTeX citation. **Additive only** — formal draft NOT mutated (constraint: DO NOT mutate qmirror v2.0.0 source artifacts).

---

## Honest C3 caveats (raw#10)

1. **Cross-link burden grows per release.** Each qmirror version cycle (v1.0.0 → v1.0.1 → v2.0.0) adds another row of xref maintenance across 17+ anima docs + 4 sister repos + papers + n6-architecture README. Without a centralized symbol (e.g. `nexus.qmirror.upstream_url` in `nexus/.roadmap.qmirror`), future renames or version bumps require a fan-out sweep. Mitigation deferred to a future consolidation cycle. Concrete signal: the 17 anima docs now carry **3 stacked qmirror callout blockquotes at top** (sister `aa6c8c54e` substrate update line + v1 GitHub URL line + v2 release line). Bounded growth (each cycle adds ≤1 line), but compounding visual noise.

2. **Papers repo needs separate workflow.** The `papers/` repo carries CC BY 4.0 while qmirror code is Apache-2.0; the new PA-39 entry under `papers/anima/` is a **status pointer + closure summary**, not the upstream draft. The arXiv draft refresh + arXiv submission live under the anima cycle (separate workflow from the papers cycle). Until refresh lands, `papers/anima/PA-39` is the canonical pointer for closure status; `anima/docs/qmirror_arxiv_draft_2026_05_03.md` (v0.1, v1-scope) remains the canonical pre-print body but does **not** yet incorporate the 5 v2.0 axes.

3. **arXiv submission still pending peer review.** PA-39 declares `arXiv draft v0.1 (peer review pending)` for status transparency. Concrete sequential blockers:
   - (a) refresh `anima/docs/qmirror_arxiv_draft_2026_05_03.md` to incorporate cond.9–cond.13
   - (b) internal peer review by need-singularity stack contributors
   - (c) LaTeX migration (Markdown → arXiv-ready `.tex`)
   - (d) figure prep (per-axis verdict matrix + cost comparison + sister substrate diagram)
   - (e) counsel sign-off (license/IP review for cross-vendor IBM/AWS Braket data + ANU QRNG ToS attribution + pyphi GPLv3 sub-component disclosure)

   No parallel acceleration available without external contributor sign-up.

4. **v2.0.0 deletion would invalidate links.** The v2.0.0 release tag is technically deletable via `gh release delete v2.0.0 --yes`, but the tag retains its OID in any clone that fetched it; downstream consumers — PA-39 paper entry + 17 anima xref docs + 4 sister repo READMEs (sim-universe, hexa-bio, honesty-monitor, qmirror itself) + n6-architecture README — all carry phantom references. If a critical bug requires retraction, prefer a v2.0.1 patch release over deletion. Treat each release tag as effectively immutable.

---

## Constraints honored

- **raw#9 STRICT** (Mac → hexa only): no .py created or touched on Mac repo. All edits are .md doc-only.
- **raw#15** (no personal-path leak): added lines contain no `/Users/...` or other personal filesystem paths. Pre-existing personal-path leaks in target docs (e.g. `n_12_v3_ibm_quantum_prep_2026_05_01.md` line 5: `/Users/ghost/n12_v3_ibm/`) are NOT mutated per user constraint.
- **raw#10**: 4 honest C3 caveats above (bumped from prior cycle's 3 — added "papers repo separate workflow" + "v2.0.0 deletion invalidates links" per user request).
- **$0** cost (doc-only, no API / compute / storage spend).
- **No qmirror v2.0.0 source artifact mutation**: the formal `RELEASE_NOTES_v2.0.0.md.draft` + `CHANGELOG.md` v2.0.0 entry + `README_hf_v2_draft.md` + `registry_v2_entry.tsv.draft` + `CHANGELOG_v2_entry.md.draft` are NOT mutated. The new `RELEASE_NOTES_v2.0.0_announcement.md` is a sibling additive file.
- **No v1 reference deletion**: every existing v1.0.0 GitHub URL line in the 17 anima docs is preserved verbatim; v2 line stacks below.

## Out-of-scope (preserved)

- 21 closed historical docs (audit trail integrity, same as prior v1 xref cycle)
- 65 methodology reference docs (concept abstraction, not substrate execution)
- 1369+ total docs in `docs/` (only the 17 substrate-anchored qmirror docs + this handoff are in scope)
- arXiv draft body refresh (separate cycle; PA-39 declares the dependency)
- Formal `gh release create v2.0.0` publication (already LIVE per user context)

## Artifacts

- `state/qmirror_v2_announcement_2026_05_04/audit.json` — full audit + 4 C3 caveats + constraint witnesses
- `state/qmirror_v2_announcement_2026_05_04/updated_docs.json` — 24-file inventory + per-category split + per-file action breakdown
- `state/markers/qmirror_v2_announcement_landed.marker` — landed marker
- `docs/qmirror_v2_announcement_landed_2026_05_04.ai.md` — this handoff
- `papers/anima/PA-39-qmirror-v2-closure.md` — papers repo entry (qmirror v2.0.0 closure summary + arXiv draft pointer)
- `papers/anima/INDEX.md` — Cluster 6 added
- `qmirror/RELEASE_NOTES_v2.0.0_announcement.md` — community-friendly announcement

## Sister dependency

- `aa6c8c54e` (sister BG: substrate-dependency xref audit + first v1 pass) + the original `qmirror_github_xref` cycle (handoff `docs/qmirror_github_xref_landed_2026_05_03.ai.md`) — this cycle reuses the same 17-doc inventory.
- qmirror v2.0.0 closure synth cycle: `docs/qmirror_2_closure_spec_landed_2026_05_04.ai.md` + `docs/qmirror_2_closure_2026_05_04.md` (closure verdict source).
- 4 standalone sister repo extractions: qmirror (v1+v2), sim-universe (v1.0.0), hexa-bio (v1.0.0), honesty-monitor (v1.0.0) — all under the `anima_offrepo` 2026-05-04 cycle.
