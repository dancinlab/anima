# qmirror GitHub URL cross-reference — LANDED 2026-05-03

- ts_utc: 2026-05-03
- agent: `qmirror_github_xref`
- task: additive cross-link to `https://github.com/dancinlab/qmirror` in qmirror-anchored anima docs
- mode: additive single-line blockquote per file (no mutation of existing path references / counts / measurements)
- gate: raw#9 strict (Mac → hexa only; no .py touched) · raw#10 (3 honest C3 caveats) · raw#15 (no personal-path leak in added line)
- cost: $0 (doc-only)
- sister_dependency: `aa6c8c54e` (substrate-dependency xref audit + first pass) + sister BG push to GitHub (URL goes live when sister lands)

---

## TL;DR

Added a single blockquote line — `> 📦 Available at: https://github.com/dancinlab/qmirror (`hx install qmirror`)` — to **17 qmirror-anchored anima docs** so future readers can also locate the standalone qmirror repo for installation, in addition to the in-tree canonical paths (`docs/nexus_qmirror_spec_2026_05_03.md`, `nexus/modules/qmirror/...`).

| category | docs | action |
| --- | --- | --- |
| closure_related | 10 | additive line after H1 / front-matter |
| substrate_dependency | 7 | additive line after sister's pre-existing 2026-05-03 qmirror substrate update callout |
| closed_historical | 21 | preserved (audit-trail integrity per user constraint) |
| methodology_reference | 65 | preserved (concept references, not substrate-execution dependency) |

Total mutation: **0 lines removed, 34 lines added** (2 lines × 17 files: blockquote + blank separator).

---

## Files updated

### closure_related (10)

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

### substrate_dependency (7)

- `docs/n_substrate_n12_quantum_pivot_2026_05_01.md`
- `docs/n_substrate_n12_ionq_penrose_hameroff_spec_2026_05_01.md`
- `docs/n_12_v3_ibm_quantum_prep_2026_05_01.md`
- `docs/n_substrate_n12_aws_prep_2026_05_01.md`
- `docs/n_substrate_n13_photonic_iit_spec_2026_05_01.md`
- `docs/ibm_cloud_experiment_list_2026_05_03.md`
- `docs/ibm_cloud_env_setup_runbook_2026_05_03.md`

---

## Honest C3 caveats (raw#10)

1. **URL not verified live** — sister BG handles the actual GitHub push to `dancinlab/qmirror`. Until that BG completes, the URL added here is forward-declarative and may return 404 for early readers. Sister marker (TBD) will close the loop; until then, the in-tree path `docs/nexus_qmirror_spec_2026_05_03.md` remains the only verified canonical.

2. **Doc-top growth** — the additive line stacks with sister `aa6c8c54e`'s pre-existing 2026-05-03 qmirror substrate update callouts on the 7 substrate-dependency docs. Those docs now carry **2 stacked qmirror blockquotes at top** before the content begins. The growth is bounded (each cycle adds ≤1 line) but future cycles may want consolidation into a single header summary block.

3. **Future rename sweep required** — there is no central registry binding the GitHub URL across these 17 docs. If the repo is later renamed (e.g. `dancinlab/qmirror` → `singularity/qmirror`, or moved to a different org), all 17 files need a sweep. Mitigation idea (out-of-scope this cycle): add a `nexus.qmirror.upstream_url` symbol in `nexus/.roadmap.qmirror` so future doc references can cite the symbol rather than the literal URL.

---

## Constraints honored

- **raw#9 strict** (Mac → hexa only): no .py created or touched on Mac repo. All edits are `.md` doc-only.
- **raw#15** (no personal-path leak): added line contains no `/Users/...` or other personal filesystem paths. Pre-existing personal-path leaks in target docs (e.g. `n_12_v3_ibm_quantum_prep_2026_05_01.md` line 5: `/Users/ghost/n12_v3_ibm/`) are **not** mutated per user's "DO NOT mutate ... pre-existing path references" constraint.
- **raw#10**: 3 honest C3 caveats above.
- **$0** cost (doc-only, no API / compute / storage spend).

## Out-of-scope (preserved)

- 21 closed historical docs (audit trail integrity)
- 65 methodology reference docs (concept abstraction, not substrate execution)
- 1369 total docs in `docs/` (only the 17 substrate-anchored qmirror docs are in scope)

## Artifacts

- `state/qmirror_github_xref_2026_05_03/updated_files.json` — 17-file inventory + category split + constraint witnesses
- `state/qmirror_github_xref_2026_05_03/diff.json` — per-file insertion anchor + +2/-0 line accounting
- `state/markers/qmirror_github_xref_landed.marker` — landed marker
- `docs/qmirror_github_xref_landed_2026_05_03.ai.md` — this handoff
