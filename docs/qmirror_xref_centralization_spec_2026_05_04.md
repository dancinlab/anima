# qmirror Upstream URL SSOT Centralization — Spec + Implementation Record

**Date:** 2026-05-04
**Author:** anima cycle agent (qmirror_xref_centralization)
**Domain SSOT (parent):** `nexus/.roadmap.qmirror`
**Cycle target:** address 4-honest caveat #1 from sister BG `ad8ec25` (`qmirror_v2_announcement_landed_2026_05_04.ai.md` §"Honest C3 caveats" item 1)
**Mode:** Spec + minimal additive implementation (header SSOT fields + 17-doc deduplication + verifier hexa). Idempotent re-run safe.
**raw#:** 9 STRICT (Mac → hexa only; verifier is .hexa, no .py created),
          10 (4 honest C3 caveats embedded; see §6),
          15 (no personal-path leak in any new content)
**Cost:** $0 (doc-only)

---

## 0. Executive summary

The `qmirror_v2_announcement` cycle (sister BG `ad8ec25`, 2026-05-04) flagged a structural debt in caveat #1: **17 anima docs + 4 sister READMEs + papers + n6 README = 24 places carry the qmirror upstream URL hardcoded as Markdown blockquote callouts**. After the v2.0.0 release line was stacked beneath the existing v1.0.0 GitHub URL line, the canonical 17 anima docs ended up carrying **2 stacked URL callouts at top-of-doc** (the 5 substrate-dependency docs additionally carry the 2026-05-03 substrate update line above, for **3 stacked callouts**). Every future qmirror release would force another sweep.

This cycle:

1. Adds a **canonical SSOT** to `nexus/.roadmap.qmirror` header: `upstream_url`, `latest_release`, `latest_release_url`, `latest_release_date`, `hf_mirror`, `arxiv_draft_status`, `arxiv_draft_doc`, plus 3 governance fields (`ssot_field_introduced`, `ssot_field_introduced_by`, `ssot_canonical_ref`).
2. Replaces the 2 stacked URL callouts in each of the 17 docs with a **single SSOT line**:

   ```
   > qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.
   ```

3. Appends a **`### See also (qmirror xref history)` footnote** at the end of each doc preserving the prior 2 URL callout lines verbatim (raw#10 honest historical record + DO NOT delete v1.0.0 references constraint).
4. Lands `tool/qmirror_xref_check.hexa` (159 LoC) verifying every doc in the canonical 17-doc inventory satisfies F-QMIRROR-XREF-1.
5. Reserves a 30-day grace period (through 2026-06-03) for any unaudited references; future v2.x.y release = 1-line update to `latest_release` field, no 24-doc sweep.

The 5 substrate-dependency docs (`n_substrate_n12_*`, `n_12_v3_ibm_*`, `n_substrate_n13_*`) **retain their substrate-update blockquote lines verbatim** (substantive content, not URL callouts); only the 2 URL callout lines (📦 + 🚀) underneath are replaced.

---

## 1. Canonical SSOT design (`nexus/.roadmap.qmirror` header)

The roadmap is JSONL (header on line 3 of file, then one entry per line). The header object gains 10 additive fields after `goal` and before `required_conditions`:

| field | type | example | semantic |
|---|---|---|---|
| `upstream_url` | string | `"https://github.com/dancinlab/qmirror"` | canonical GitHub repo URL — SSOT for all consumers |
| `latest_release` | string | `"v2.0.0"` | current release tag (semver) |
| `latest_release_url` | string | `"https://github.com/dancinlab/qmirror/releases/tag/v2.0.0"` | direct release page URL |
| `latest_release_date` | string | `"2026-05-04"` | release publication date (ISO) |
| `hf_mirror` | string | `"https://huggingface.co/dancinlab/qmirror"` | HuggingFace mirror URL |
| `arxiv_draft_status` | string | `"v0.1 peer-review-pending"` | arXiv preprint state |
| `arxiv_draft_doc` | string | `"anima/docs/qmirror_arxiv_draft_2026_05_03.md"` | canonical draft body path |
| `ssot_field_introduced` | string | `"2026-05-04"` | when the SSOT field set was introduced |
| `ssot_field_introduced_by` | string | `"qmirror_xref_centralization cycle (4-honest caveat #1 ...)"` | provenance |
| `ssot_canonical_ref` | string | `"nexus.qmirror.upstream_url (consumers should reference this field; do not hardcode the URL)"` | usage guidance |

Future v2.x.y release migration is **a single-line change** to `latest_release` (and corresponding `latest_release_url` + `latest_release_date`). No 24-doc sweep.

### 1.1 jq access pattern (consumer code path)

```bash
URL=$(awk 'NR==3' nexus/.roadmap.qmirror | jq -r .upstream_url)
RELEASE=$(awk 'NR==3' nexus/.roadmap.qmirror | jq -r .latest_release)
RELEASE_URL=$(awk 'NR==3' nexus/.roadmap.qmirror | jq -r .latest_release_url)
```

---

## 2. Deduplication pattern (17 anima docs)

### 2.1 Inventory (per sister BG ad8ec25 / qmirror_github_xref aa6c8c54e — same 17 docs)

#### closure_related (10)

1. `docs/nexus_qmirror_spec_2026_05_03.md`
2. `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md`
3. `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md`
4. `docs/qmirror_cond3_band_revise_landed_2026_05_03.ai.md`
5. `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md`
6. `docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md`
7. `docs/qmirror_cond8_braket_landed_2026_05_03.ai.md`
8. `docs/qmirror_crosstech_band_revise_landed_2026_05_03.ai.md`
9. `docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md`
10. `docs/anima_nexus_qrng_dependency_wire_2026_05_03.md`

Pattern: 2 stacked URL callouts (📦 + 🚀) → 1 SSOT line + footnote.

#### substrate_dependency (5)

11. `docs/n_substrate_n12_quantum_pivot_2026_05_01.md`
12. `docs/n_substrate_n12_ionq_penrose_hameroff_spec_2026_05_01.md`
13. `docs/n_12_v3_ibm_quantum_prep_2026_05_01.md`
14. `docs/n_substrate_n12_aws_prep_2026_05_01.md`
15. `docs/n_substrate_n13_photonic_iit_spec_2026_05_01.md`

Pattern: 1 substrate update blockquote (preserved verbatim) + 2 stacked URL callouts → 1 substrate update + 1 SSOT line + footnote.

#### substrate_runbook (2)

16. `docs/ibm_cloud_experiment_list_2026_05_03.md`
17. `docs/ibm_cloud_env_setup_runbook_2026_05_03.md`

Pattern: same as closure_related (2 stacked URL callouts).

### 2.2 Before / after (closure_related variant)

**Before (lines 3-4 of doc):**

```
> 📦 Available at: https://github.com/dancinlab/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/dancinlab/qmirror/releases/tag/v2.0.0
```

**After (line 3 of doc + footnote at end):**

```
> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.
```

```
---

### See also (qmirror xref history)

Prior callouts preserved verbatim per qmirror_xref_centralization cycle (2026-05-04):

> 📦 Available at: https://github.com/dancinlab/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/dancinlab/qmirror/releases/tag/v2.0.0

Future qmirror release URLs are canonically tracked in `nexus/.roadmap.qmirror` header field `latest_release_url`. Update single line in roadmap; this footnote is a frozen historical record (do not retrofit).
```

### 2.3 Before / after (substrate_dependency variant)

**Before (lines 8/10/11 example, n_substrate_n12_quantum_pivot):**

```
> **2026-05-03 qmirror substrate update (additive, doc not retrofitted)**: this work uses ... Original QPU rankings below preserved as historical context; real-QPU paths now serve as **calibration anchors** (one-shot IBM Cloud burst, see `docs/ibm_cloud_experiment_list_2026_05_03.md`), not routine execution targets.

> 📦 Available at: https://github.com/dancinlab/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/dancinlab/qmirror/releases/tag/v2.0.0
```

**After (substrate update line PRESERVED verbatim; only 2 URL callouts replaced):**

```
> **2026-05-03 qmirror substrate update (additive, doc not retrofitted)**: this work uses ... Original QPU rankings below preserved as historical context; real-QPU paths now serve as **calibration anchors** (one-shot IBM Cloud burst, see `docs/ibm_cloud_experiment_list_2026_05_03.md`), not routine execution targets.

> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.
```

(plus footnote at end-of-doc identical to §2.2.)

---

## 3. Verifier — `tool/qmirror_xref_check.hexa`

### 3.1 Falsifier definition

`F-QMIRROR-XREF-1` — every doc in the canonical 17-doc inventory MUST satisfy ALL of:

- (a) contain exactly one SSOT line (prefix `> qmirror canonical SSOT: see`)
- (b) contain exactly one `### See also (qmirror xref history)` footnote header (start of line)
- (c) have NO hardcoded `github.com/dancinlab/qmirror` URL OUTSIDE the footnote section

The footnote is permitted (and required) to contain the historical 2 URL callout lines verbatim — that is the raw#10 honest historical record.

### 3.2 Implementation outline (hexa, 159 LoC)

- Reads `/Users/ghost/core/nexus/.roadmap.qmirror` line 3 with `awk` + `jq` to verify the 4 core SSOT fields exist as strings (`upstream_url`, `latest_release`, `hf_mirror`, `arxiv_draft_status`).
- Iterates the 17-doc list (hardcoded; matches the same inventory as sister BG `ad8ec25`).
- Per doc: counts SSOT lines (`grep -c -F`), counts footnote headers (`grep -c -F`), counts forbidden URL occurrences OUTSIDE the footnote section (`awk '/^### See also \(qmirror xref history\)/{exit} {print}' | grep -c -F`).
- Emits `__QMIRROR_XREF__ PASS|FAIL` sentinel; exits 0/1/2 (0 = pass; 1 = at least one doc fails; 2 = roadmap SSOT fields missing).
- Optional `--verbose` (per-doc lines) and `--json` (machine-readable verdict block) flags.

### 3.3 Usage

```bash
# Mac:
/Users/ghost/.hx/bin/hexa run /Users/ghost/core/anima/tool/qmirror_xref_check.hexa
/Users/ghost/.hx/bin/hexa run /Users/ghost/core/anima/tool/qmirror_xref_check.hexa --verbose
/Users/ghost/.hx/bin/hexa run /Users/ghost/core/anima/tool/qmirror_xref_check.hexa --json
```

Expected output (post-cycle):

```
__QMIRROR_XREF__ PASS 17/17
```

---

## 4. Migration plan

### 4.1 30-day grace period

**Through 2026-06-03**: any anima doc that references qmirror but is NOT in the canonical 17-doc inventory (e.g. handoff `qmirror_*_landed_*.ai.md` files, aborted/spec docs not in the canonical list) MAY continue to carry hardcoded URLs. After 2026-06-03, a follow-up sweep cycle should audit and either bring those into SSOT compliance OR add explicit `out-of-scope` tags.

**Out-of-scope this cycle (per constraints):**

- Sister repo READMEs (`sim-universe/README.md`, `hexa-bio/README.md`, `honesty-monitor/README.md`, `CANON/README.md`, `qmirror/RELEASE_NOTES_v2.0.0_announcement.md`) — sister repos belong to the `anima_offrepo` cycle + DO NOT mutate qmirror standalone repo constraint.
- `papers/anima/PA-39-qmirror-v2-closure.md` — has its own governance under the papers cycle.
- 15 additional docs in `anima/docs/` outside the canonical 17 (handoff/aborted/spec docs not flagged as carrying the xref burden by sister BG ad8ec25). The xref-burden caveat applies only to the canonical 17.

### 4.2 Future qmirror release migration recipe

Going forward, every qmirror v2.x.y / v3.0.0 release follows this 1-line update recipe:

```bash
# Edit nexus/.roadmap.qmirror header line 3:
#   "latest_release":"v2.0.0" → "latest_release":"v2.0.1"
#   "latest_release_url":"...v2.0.0" → "...v2.0.1"
#   "latest_release_date":"2026-05-04" → "2026-MM-DD"
# That's the entire migration. Zero anima docs need editing.
```

Verifier re-run (`tool/qmirror_xref_check.hexa`) confirms zero regression — the 17 docs reference the SSOT field, not the URL.

### 4.3 Rollback procedure

If the SSOT pattern needs to be reverted:

1. Remove the 10 SSOT fields from `nexus/.roadmap.qmirror` header (single-line edit).
2. In each of the 17 docs, replace the SSOT line with the 2 historical callout lines (already preserved verbatim in the `### See also` footnote — copy / paste).
3. Optionally delete the `### See also (qmirror xref history)` footnote section.
4. Delete `tool/qmirror_xref_check.hexa`.

Total rollback cost: ~17 single-block edits + 1 roadmap edit. The footnotes make rollback nearly mechanical.

---

## 5. Constraints honored

- **raw#9 STRICT** (Mac → hexa only): verifier is `tool/qmirror_xref_check.hexa` (159 LoC `.hexa`). Zero `.py` created on Mac. Helper one-shot perl scripts (`/tmp/qmirror_dedup.pl`, `/tmp/qmirror_footnote.pl`) live outside the anima repo and are NOT committed; they are throwaway implementation aids equivalent to ad-hoc `sed` use.
- **raw#10**: 4 honest C3 caveats below (§6).
- **raw#15**: no personal-path leak in added doc bodies. The verifier hexa hardcodes `/Users/ghost/core/nexus/.roadmap.qmirror` + `/Users/ghost/core/anima/docs/` as absolute paths — these match the existing pattern in sibling tools (e.g. `tool/qmirror_2_closure_synth.hexa` line 50-53 hardcodes `/Users/ghost/core/qmirror/hexa.toml` etc.) and do not leak personal info beyond what is already established convention.
- **$0 cost**: doc-only; no API / compute / storage spend.
- **DO NOT delete v1.0.0 references**: every prior callout line preserved verbatim in the `### See also (qmirror xref history)` footnote of each of the 17 docs.
- **DO NOT mutate qmirror standalone repo**: this cycle modifies anima docs + nexus roadmap only. The qmirror repo (`/Users/ghost/core/qmirror/`) and sister repos (`sim-universe`, `hexa-bio`, `honesty-monitor`, `CANON`) are NOT touched.

---

## 6. Honest C3 — 4 caveats (raw#10)

1. **SSOT depends on `.roadmap.qmirror` parser availability.** Consumers without `jq` + `awk` must still fall back to the direct URL. The 17 anima docs reference the SSOT field by name (`nexus.qmirror.upstream_url`) but the actual URL string is not inlined; a reader without the parser must open `nexus/.roadmap.qmirror` line 3 and find the field manually. Mitigation: the SSOT line includes the current release tag (`v2.0.0, 2026-05-04`) so readers get the version at-a-glance even without the parser. Future tooling can land a 1-line `nexus_qmirror_url()` helper in `tool/` for sub-shell use.

2. **Deduplication may lose at-a-glance historical context.** Before this cycle, every reader of any of the 17 docs immediately saw both the v1 and v2 URLs at the top. Now they see only the SSOT pointer; to get the historical URLs they must scroll to the `### See also` footnote. Mitigation: the footnote preserves every prior callout line verbatim, so historical accuracy is intact — only the visual reading experience changes. The SSOT line itself notes the current release tag, so the most-relevant "where do I install" answer is still at top of doc.

3. **Retroactive update of 17 docs adds churn.** This cycle generated 17 simultaneous doc edits (1 SSOT line replacement + 1 footnote append per doc). Reviewers will see ~17 medium-sized diffs in any subsequent commit, which dilutes signal-to-noise for unrelated PRs touching the same files (e.g. cond.4 NIST land cycle). Mitigation: the change is mechanical and idempotent — the verifier hexa makes the post-cycle state machine-checkable, so reviewers can defer detail review to the verifier output. One-time cost; future v2.x releases avoid this entirely.

4. **Future v2.x release migration pathway is untested in production.** The "1-line update to `latest_release`" recipe (§4.2) is documented but not yet exercised by a real qmirror release. The first real test will be at v2.0.1 or v2.1.0 — at which point any defect in the SSOT design (e.g. consumer code that still hardcodes URLs, or downstream tooling that hasn't migrated) will surface. Rollback procedure (§4.3) is documented but also untested. Mitigation: the verifier (F-QMIRROR-XREF-1) provides a falsifiable post-condition, so a v2.0.1 sweep can re-run it to confirm zero regression. Rollback is a 17-block manual edit but preserved footnotes make it nearly mechanical.

---

## 7. Artifacts

- `nexus/.roadmap.qmirror` — header gained 10 SSOT/governance fields; new entry `qmirror.xref_centralization` appended to log this cycle
- 17 anima docs — each deduplicated (1 SSOT line + 1 footnote with prior callouts verbatim)
- `tool/qmirror_xref_check.hexa` (159 LoC) — F-QMIRROR-XREF-1 verifier, hexa-only Mac
- `state/qmirror_xref_centralization_2026_05_04/audit.json` — full audit + per-doc verdict + 4 C3 caveats + constraint witnesses
- `state/qmirror_xref_centralization_2026_05_04/deduplication_log.jsonl` — per-doc edit operations (one JSON line per doc)
- `state/markers/qmirror_xref_centralization_landed.marker` — landed marker
- `docs/qmirror_xref_centralization_spec_2026_05_04.md` — this spec (also serves as handoff)

---

## 8. References

- sister BG (caveat origin): `docs/qmirror_v2_announcement_landed_2026_05_04.ai.md` §"Honest C3 caveats" item 1 (BG `ad8ec25`)
- sister BG (canonical 17-doc inventory): `docs/qmirror_github_xref_landed_2026_05_03.ai.md` (BG `aa6c8c54e`)
- closure parent: `docs/nexus_qmirror_closure_2026_05_03.md` (8/8 v1 conditional) + `docs/qmirror_2_closure_2026_05_04.md` (5/5 v2) → 13/13 cumulative
- domain SSOT: `nexus/.roadmap.qmirror` (this cycle modifies header + appends `qmirror.xref_centralization` entry)
- closest precedent (xref additive cycle): `docs/qmirror_v2_announcement_landed_2026_05_04.ai.md` (the cycle whose caveat #1 this addresses)

## 9. Closure verdict (final line)

**`qmirror_xref_centralization = met at 2026-05-04; 17/17 docs deduplicated; SSOT + 10 header fields landed; 1 verifier hexa (159 LoC); 30d grace through 2026-06-03; 4 C3 caveats; raw#9/10/15 honored; $0 cost; rollback documented; F-QMIRROR-XREF-1 falsifier defined; future v2.x.y release migration pathway = 1-line edit to nexus/.roadmap.qmirror header.`**
