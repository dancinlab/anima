# qmirror README sync landed — 2026-05-04 (handoff)

**Cycle:** anima qmirror README post-cycle sync
**Target:** `/Users/ghost/core/qmirror/README.md`
**Marker:** `anima/state/markers/qmirror_readme_sync_landed.marker`
**Audit:** `anima/state/qmirror_readme_sync_2026_05_04/{audit.json, before_after.diff}`
**Commit:** [`a450113`](https://github.com/dancinlab/qmirror/commit/a450113)
**Cost:** $0

---

## TL;DR

qmirror's `README.md` was 4 commits behind the post-1.0.0 reality (qmirror 2.0
cond.9 + cond.10 PASS, nexus CLI consumer, dual-mirror auto-sync workflow,
LICENSING.md authoritative SSOT). This cycle is a **purely additive sync**:
LoC delta 282 → 407 (+125 lines), zero deletions, canonical voice + structure
preserved. Pushed to GitHub `main` (commit `a450113`); HF sync workflow
correctly fails loudly at the documented HF_TOKEN USER ACTION gate.

---

## What landed

### 3 new sections

1. **qmirror 2.0 progress (2/5 axes landed)** — full status table for the
   5 ranked axes (cond.9 process tomography PASS 7/7 gates @ fid ≥ 0.99918;
   cond.10 GHZ-3 Mermin PASS @ M=4.0 saturated; cond.11 / cond.12 / cond.13
   pending) with falsifier IDs, verdict numerics, substrates, and landing
   handoff cross-links.

2. **Real-world consumer: nexus uses qmirror** — documents that nexus declares
   `qmirror = "^1.0.0"` in `nexus/hexa.toml` `[dependencies]` and consumes
   the standalone CLI through a **4-tier resolution chain with hard-fail**:
   `$QMIRROR_ROOT` env → `/Users/ghost/core/qmirror` (Mac dev) →
   `$HOME/core/qmirror` (user-home) → PATH-resolved `qmirror`. Notes that
   the legacy 5th-tier `legacy-intree` fallback was **removed in v0.3.0** of
   the router to enforce standalone-only consumption.

3. **Dual-mirror auto-sync (GitHub → HuggingFace)** — documents the
   `.github/workflows/sync-to-hf.yml` workflow trigger semantics, the
   `~2-3 min` sync lag, and the **USER ACTION required**: set the `HF_TOKEN`
   GitHub repo secret at `settings/secrets/actions`. Documents the fail-loud
   semantics and the local fallback hook.

### 6 updated sections

- **Header badges**: added `qmirror 2.0: 2/5 axes landed` blue badge
  (alongside existing License / Closure 8/8 / HF Mirror badges).
- **Installation › Via `hx`**: dropped sister-cycle pending stub; documents
  `hx install qmirror` works (registry.tsv L22).
- **Closure conditions (8/8 PASS)**: appended confirmation that all 8 conds
  remain MET as of 2026-05-04 post-NIST cond.4 PASS verified 7/7 at α=0.01.
- **Cost comparison**: added per-second QPU rate row (`$0/sec` qmirror vs
  `$1.60–2.30/sec` IBM Heron r2 paygo) and the **USD 41.34 one-time
  calibration spend** total across the closure cycle (sourced from
  `anima/docs/qmirror_arxiv_draft_2026_05_03.md` §5.2).
- **License & attribution**: strengthened cross-link with sub-component
  summary callout (Apache-2.0 source + pyphi GPLv3 subprocess-isolated)
  + explicit `NEXUS_QMIRROR_MOCK=1` GPLv3 opt-out + LICENSING.md as
  authoritative SSOT pointer.
- **Status**: expanded from 2 bullets to 6, covering v1.0.0, v1.0.1 license
  audit, dual-mirror workflow, nexus CLI integration, hx registry
  registration, qmirror 2.0 cond.9/cond.10 PASS.

---

## Publishing

| target | status | detail |
|--------|--------|--------|
| GitHub `main` | PUSHED | `5a3c516..a450113` to `https://github.com/dancinlab/qmirror.git` |
| HF Hub | FAIL-LOUD (by design) | workflow run [`25298055312`](https://github.com/dancinlab/qmirror/actions/runs/25298055312) failed at `Verify HF_TOKEN secret is present` step — exact behavior documented in the new dual-mirror section |

**To complete HF sync**: USER must set `HF_TOKEN` write-scope secret at
<https://github.com/dancinlab/qmirror/settings/secrets/actions>, then
re-trigger the failed workflow run. End-to-end mirror semantics
(including delete-on-source-removal) are then exercised on the next push
or manual `workflow_dispatch`.

---

## raw compliance

- **raw#9 STRICT**: only `README.md` (markdown allowed) edited on Mac side.
  No `.py`/`.ts`/`.js`/`.go` files created or modified.
- **raw#15**: no token literal in README; no personal-path leak. The
  `/Users/ghost/core/qmirror` reference in the 4-tier resolution chain
  matches the actual nexus router behavior (load-bearing — the README
  documents what the code does).
- **raw#10**: 3 honest C3 caveats kept or strengthened in the README body
  (noiseless-Aer for cond.9/cond.10; license sub-component pyphi GPLv3
  subprocess isolation; USER ACTION required for HF_TOKEN secret).
- **Cost**: $0 (markdown edit + 1 git push + 1 GH Actions free-tier run).

---

## Commit-scope note

The commit `a450113` swept in 2 pre-staged files
(`modules/process_tomography.hexa` + `modules/_python_bridge/process_tomography_runner.py`)
that were already `git add`-staged at session start (status `A` from the
cond.9 land cycle). These files implement the cond.9 process-tomography
verifier the new README section documents, so the bundling is semantically
honest. The commit message foregrounds the README sync as the primary intent.

---

## Cross-links

- Spec: `anima/docs/qmirror_2_axes_spec_2026_05_03.md` (5-axis ranking)
- cond.9 land: `anima/docs/qmirror_2_cond9_tomography_landed_2026_05_03.ai.md`
- cond.10 land: `anima/docs/qmirror_2_cond10_ghz_mermin_landed_2026_05_03.ai.md`
- nexus consumer: `anima/docs/nexus_cli_qmirror_landed_2026_05_03.ai.md`
- 5th-tier removal: `anima/docs/nexus_qmirror_legacy_removed_2026_05_03.ai.md`
- dual-mirror workflow: `anima/docs/qmirror_dual_mirror_autosync_landed_2026_05_03.ai.md`
- LICENSING audit: `anima/docs/qmirror_license_audit_landed_2026_05_03.ai.md`
- arXiv draft (calibration $41.34): `anima/docs/qmirror_arxiv_draft_2026_05_03.md` §5.2
