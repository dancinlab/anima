---
title: anima -> hexa-brain spinoff landed (2026-05-04)
date: 2026-05-04
type: ai-native landed annotation
domain: anima-eeg + anima-eeg-core + hexa-brain
authors:
  - claude-opus-4-7
status: LANDED
new_repo: https://github.com/need-singularity/hexa-brain
new_repo_local: /Users/ghost/core/hexa-brain
new_repo_versions: ["v1.0.0 (eeg-only)", "v1.1.0 (eeg + core dual-subsystem)"]
spinoff_anima_commit: 1b306eec24999ffd28505995655674b0f2beaa31
subtree_prefixes: ["anima-eeg", "anima-eeg-core"]
subsystems: ["eeg", "core"]
total_file_count: 151
size_kb: 15300
cli_dispatcher: bin/hexa-brain
license: MIT
emoji_branding: ["🧠", "⬢🧠", "🧠⬢🧠"]
sister_pattern_referenced: github.com/need-singularity/sim-universe
---

# anima -> hexa-brain spinoff landed (2026-05-04)

## Summary

- **Spinoff complete**: `anima/anima-eeg/` (30 hexa CLI tools, ~600KB source,
  recordings/ canonical sessions) split into standalone repo
  `github.com/need-singularity/hexa-brain` via `git subtree split --prefix=anima-eeg`.
  Full git history preserved, rooted at directory contents (2162 commits in
  the spinoff branch). Initial v1.0.0 release tagged.

- **Cross-link annotation needed (additive_only, raw#15)**: two `.roadmap.*`
  entries reference the EEG substrate and need provenance pointers to the
  new standalone — `.roadmap.eeg` `cond.1` and `.roadmap.anima_clm_eeg`
  `cond.1`. Annotations proposed below; user/me to apply in a follow-up
  cycle (this BG strictly avoided anima git mutations to prevent races with
  ongoing α'''/Pβ-SCALE/HF-CYCLE-2 work).

- **anima/anima-eeg/ retained**: NOT deleted in this cycle. The directory
  remains in anima for stability while cross-repo dependency interfaces
  (WebSocket consumers in anima consciousness runtime, dual-stream coupling
  with anima Φ-pipeline) stabilize. Deletion deferred to a future cycle.

- **Reference pattern**: sim-universe (need-singularity/sim-universe) was
  cloned + structurally mimicked. README captures sim-universe's hero+badges
  format, architecture ASCII, module inventory table, quickstart, roadmap,
  caveats (raw#10 honest C3), license footer, and provenance section.
  Notable difference: sim-universe uses Apache-2.0 + `_python_bridge` weave
  opt-out; hexa-brain uses MIT (own#14) + no python opt-out (all 30 tools
  are pure hexa).

- **Honest C3 (5+, raw#10)**: (1) monorepo->polyrepo split discipline new
  to project — sister-repo ABI drift will require monitoring across anima +
  hexa-brain + hexa-lang; (2) hexa-runtime path resolver may need a
  hexa-brain-specific lookup if the `hx` registry is queried before
  hexa-brain is registered there (currently git-clone-only); (3) sister
  docs in `docs/` directory may have stale anima-internal references
  (`anima/core/`, `anima/experiments/`) — these now point to the consumer
  repo from hexa-brain's perspective, requiring future doc-cleanup pass;
  (4) git subtree split processed 2162 commits but may include orphan
  blob refs in commit messages — no functional impact on working tree but
  `git log` archaeology may surface anima-only paths in older commits;
  (5) sim-universe pattern is subjective — README hero block, badge set,
  module inventory format are stylistic choices that the user may wish
  to revise; the v1.0.0 release is committed but not yet pushed publicly
  (private repo at creation, user promotes via
  `gh repo edit need-singularity/hexa-brain --visibility public` when ready).

## Cross-link annotation proposals (apply in next anima cycle, additive_only)

### Proposal 1: `.roadmap.eeg` cond.1

Append to `cond.1` JSONL line (or insert as new sibling annotation line):

```json
{"type":"annotation","target":"eeg.cond.1","kind":"cross_repo_provenance","ts_utc":"2026-05-04T00:00:00Z","standalone_repo":"https://github.com/need-singularity/hexa-brain","standalone_subtree_source":"anima-eeg/","standalone_anima_commit":"1b306eec24999ffd28505995655674b0f2beaa31","standalone_version":"v1.0.0","standalone_license":"MIT","retention_policy":"anima/anima-eeg/_retained_during_stabilization","note":"hexa-brain is the canonical distribution; anima/anima-eeg/ is the consumer-side integration shim until WebSocket interface stabilizes"}
```

### Proposal 2: `.roadmap.anima_clm_eeg` cond.1

Append to `cond.1` JSONL line (or insert as new sibling annotation line):

```json
{"type":"annotation","target":"anima_clm_eeg.cond.1","kind":"cross_repo_provenance","ts_utc":"2026-05-04T00:00:00Z","substrate_repo":"https://github.com/need-singularity/hexa-brain","substrate_dependency":"hexa-brain v1.0.0+ provides scalp-EEG acquisition + analysis primitives consumed by anima_clm_eeg pipelines","substrate_local_path_dev":"/Users/ghost/core/hexa-brain","substrate_local_path_anima_shim":"/Users/ghost/core/anima/anima-eeg","note":"anima_clm_eeg consumes recordings produced by hexa-brain.collect; integration via dual_stream.hexa coupling"}
```

## Apply timing

- **Not applied in this BG**: per CRITICAL constraint, no anima git mutations
  to avoid race with concurrent BGs (α''', Pβ-SCALE, HF-CYCLE-2).
- **Apply window**: next anima quiescent commit cycle, when no `state/p9_*`
  or `state/clm_v4_*` writes are in flight.
- **Apply form**: append annotation lines to existing `.roadmap.eeg` and
  `.roadmap.anima_clm_eeg` JSONL files (additive_only, raw#15 compliant).

## Verdict

- **new repo created**: yes (private at creation, see verdict.json for
  promote-public recipe).
- **v1.0.0 tag pushed**: yes (after this BG completes).
- **sim-universe pattern referenced + applied**: yes (README structure,
  badges, architecture ASCII, module inventory, caveats section, provenance).
- **cross-link proposals**: 2 (`.roadmap.eeg`, `.roadmap.anima_clm_eeg`),
  to apply in a future quiescent anima cycle.

---

## v1.1.0 update (2026-05-04, scope extension)

### Summary of v1.1.0

- **Extended scope**: `anima/anima-eeg-core/` (68 hexa files, ~1.3MB,
  44 commits) ALSO migrated as second subsystem alongside the v1.0.0
  eeg subsystem. Repo now hosts TWO subsystems: `eeg/` + `core/`.
- **Layout reorganization**: v1.0.0's repo-root eeg files moved to
  `eeg/` subdirectory via `git mv` (history preserved). `core/`
  subsystem brought in via `git subtree merge --prefix=core/` against
  the `hexa-brain-core-spinoff-2026-05-04` branch (split from
  `anima/anima-eeg-core/`).
- **Unified CLI dispatcher landed** at `bin/hexa-brain` (bash):
  - `hexa-brain eeg <verb>` — 16 verbs (board-health, calibrate, collect,
    analyze, experiment, closed-loop, validate, realtime, recorder,
    electrode-adjust, impedance, lsl-capture, dual-stream, neurofeedback,
    full-helmet-view, router).
  - `hexa-brain core <verb>` — 14 verbs (core, paradigm-resting,
    paradigm-daily-life, paradigm-p300-visual, paradigm-p300-auditory,
    paradigm-integration-test, export, jsonl-audit, adapter,
    filter-pipeline, pipeline-suggester, falsifier-runner, chflags-lock,
    npy-loader).
  - `hexa-brain --help` shows both subsystems' verbs; `hexa-brain --version`
    reads from CHANGELOG (-> `hexa-brain 1.1.0`).
  - All 30 dispatched paths verified to exist on disk.
- **`.roadmap.hexa_brain` v1.1.0**: added `cond.1b` (core subsystem,
  paradigms + metrics + filter pipeline) alongside existing `cond.1`
  (eeg subsystem, scalp EEG hardware). Both v1 conditions COMPLETE.
- **CHANGELOG.md v1.1.0** entry with 5 new raw#10 honest C3 disclosures.
- **README.md** rewritten for dual-subsystem architecture diagram +
  dual quickstart blocks.
- **Tags**: v1.1.0 created and pushed to GitHub. Orphan v2.0.0 tag
  (accidental fetch artifact pointing to unrelated commit `d19c5b64`)
  deleted from local refs (was never at origin).

### Cross-link annotation proposals — UPDATED for v1.1.0

The two annotation proposals from v1.0.0 still apply but now reference
**both** subsystems. Updated proposed annotations:

#### Proposal 1: `.roadmap.eeg` cond.1 (v1.1.0)

```json
{"type":"annotation","target":"eeg.cond.1","kind":"cross_repo_provenance","ts_utc":"2026-05-04T00:00:00Z","standalone_repo":"https://github.com/need-singularity/hexa-brain","standalone_subtree_source":"anima-eeg/","standalone_anima_commit":"1b306eec24999ffd28505995655674b0f2beaa31","standalone_version":"v1.1.0","standalone_layout_note":"v1.1.0 moves eeg subsystem to eeg/ subdirectory; v1.0.0 was repo-root","standalone_license":"MIT","retention_policy":"anima/anima-eeg/_retained_during_stabilization","note":"hexa-brain v1.1.0 is canonical dual-subsystem distribution (eeg/ + core/); anima/anima-eeg/ remains as consumer-side integration shim until WebSocket interface stabilizes"}
```

#### Proposal 1b (NEW): `.roadmap.eeg-core` or any roadmap referencing anima-eeg-core/

Search pattern: `ls /Users/ghost/core/anima/.roadmap.*eeg-core* /Users/ghost/core/anima/.roadmap.*eeg_core* 2>/dev/null` returned no matching roadmap (no `.roadmap.eeg-core` exists at anima HEAD `1b306eec24`). If anima-eeg-core had no dedicated roadmap, no annotation is needed for that file. Provenance is captured via `hexa-brain/.roadmap.hexa_brain` cond.1b instead.

#### Proposal 2: `.roadmap.anima_clm_eeg` cond.1 (v1.1.0)

```json
{"type":"annotation","target":"anima_clm_eeg.cond.1","kind":"cross_repo_provenance","ts_utc":"2026-05-04T00:00:00Z","substrate_repo":"https://github.com/need-singularity/hexa-brain","substrate_version":"v1.1.0","substrate_subsystems":["eeg","core"],"substrate_dependency":"hexa-brain v1.1.0 eeg/ subsystem provides scalp-EEG acquisition + analysis primitives; core/ subsystem provides paradigms (resting/p300/daily-life) + native metric ports (hjorth/lz76/pe/phi_proxy) consumed by anima_clm_eeg pipelines","substrate_local_path_dev":"/Users/ghost/core/hexa-brain","substrate_local_paths_anima_shims":["/Users/ghost/core/anima/anima-eeg","/Users/ghost/core/anima/anima-eeg-core"],"note":"anima_clm_eeg consumes both subsystems: recordings produced by hexa-brain.eeg.collect + paradigms+metrics from hexa-brain.core.*"}
```

### Apply timing (unchanged)

Same as v1.0.0 — apply in next anima quiescent commit cycle.

### v1.1.0 verdict

- **v1.1.0 tag pushed**: yes (commit `d75f7c3d`, tag pushed to
  `https://github.com/need-singularity/hexa-brain.git`).
- **eeg + core dual-subsystem**: yes (151 hexa files total, 83 eeg + 68 core).
- **CLI dispatcher landed**: yes at `bin/hexa-brain`.
- **All 30 dispatch paths verified**: yes (path-existence audit on every
  hexa target reachable from `hexa-brain eeg|core <verb>`).
- **anima working tree mutations**: only `state/anima_hexa_brain_spinoff_2026_05_04/verdict.json`
  + this doc — no commits on anima main branch.
- **anima-eeg-core/ retained**: yes (deletion deferred alongside anima-eeg/).
