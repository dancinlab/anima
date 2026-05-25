---
date: 2026-05-05
package: hexa-brain
subsystem: eeg
status: LANDED
owner: hexa-brain repo
cycle: v1.3.0 legacy check-process scrub 2026-05-05
ssot_artifact: tag v1.3.0 @ origin/main + bin/hexa-brain + this doc
predecessor: v1.2.0 cli canonical dispatch 2026-05-05
trigger: BG-EEG-LEGACY-SCRUB — user authorization 2026-05-05 ("기존 쓸데없는 과거 체크시스템은 scrub")
raws: [R9, R10, R15, R65, R155]
---

# v1.3.0 legacy check-process scrub — hexa-brain (2026-05-05)

## TL;DR

- **What was scrubbed**: `eeg/eeg.hexa` (Phase 4b TODO-stub, 62 LOC, no real
  syscalls) → `eeg/legacy/eeg.hexa`. This file's function bodies were all
  `TODO` placeholders (no BrainFlow calls, no actual syscalls); its sole
  remaining purpose was acting as fallback for the `hexa-brain eeg router`
  verb. With v1.2.0's canonical `eeg_setup.hexa` dispatcher landed, the
  TODO-stub router has zero technical justification.
- **What was preserved (canonical, untouched)**: all 8 `eeg_setup.hexa`
  backend files (board_health_check, impedance_check,
  impedance_real_hardware_validation, headplot_helper,
  electrode_adjustment_helper, electrode_helper_rich, full_helmet_view,
  eeg_recorder), all session-stage tools (collect, calibrate, analyze,
  experiment, realtime, etc.), all session protocols
  (jaw/blink/berger/preflight_settle), the `core/` subsystem.
- **CLI deprecation strategy**: soft warning + dispatch to legacy/. The
  `hexa-brain eeg router` (and empty-verb fallback) verb still routes to
  the moved file but emits `WARN: 'router' is deprecated (v1.3.0)` to
  stderr. Help text marks it `[DEPRECATED v1.3.0]`. Future v2.0.0 may
  harden to `exit 1`.
- **Migration recipe for existing callers**:
  - `hexa run hexa-brain/eeg/eeg.hexa <verb>` → `hexa run hexa-brain/eeg/legacy/eeg.hexa <verb>` (legacy path) **or** `hexa-brain eeg <verb>` (canonical CLI) **or** `hexa run hexa-brain/eeg/eeg_setup.hexa <subcommand>` (canonical dispatcher).
  - `hexa-brain eeg router` continues to work but emits warning. Migrate to canonical verbs (see `hexa-brain eeg help`).
  - No anima-monorepo callers were affected (no anima file references `hexa-brain/eeg/eeg.hexa`).

## §1 Sequence

1. **Polled for v1.2.0 tag** — BG-EEG-LEGACY-SCRUB sequenced after
   BG-CLI-IMPROVE; waited until `v1.2.0` annotated tag landed at
   `origin/main`. Detected at iteration 22 (~11 min).
2. **Surveyed Tier 1/2 candidates** per spec:
   - `*_legacy*.hexa`, `*_old.hexa`, `*_v1.hexa`: NONE found in `eeg/`.
   - Files with `STATUS: deprecated` / `SUPERSEDED BY` headers: NONE
     (only `eeg_ftdi_latency_fix.hexa` mentions a `LEGACY` kext path
     constant — unrelated to file deprecation).
   - `eeg/eeg.hexa`: confirmed as Phase 4b stub with all-TODO bodies,
     superseded by `eeg_setup.hexa` (canonical) + `bin/hexa-brain`
     (kebab-case CLI). VALID scrub target.
   - `eeg/impedance_check.hexa`: spec listed as Tier 1 ("superseded by
     impedance_real_hardware_validation.hexa per its header"), but
     audit of canonical neighbor's actual header revealed *distinct
     roles*: "impedance_check is the one-shot diagnostic; this runner
     is the canonical evidence producer for 헬멧 착용 후 실측 sessions."
     PLUS active dependencies in 4 session protocols
     (`jaw_session_audio.hexa`, `blink_session_audio.hexa`,
     `berger_session_audio_v3_8ch.hexa`, `preflight_settle.hexa`).
     **Scrub blocked by active dependency** → preserved.
3. **Executed scrub**:
   - `mkdir -p eeg/legacy/`
   - Added `STATUS: SCRUBBED 2026-05-05 (v1.3.0)` header marker in moved file.
4. **Updated `bin/hexa-brain`**:
   - `router|""` verb: emit `WARN: 'router' is deprecated...` then
     `exec` to `eeg/legacy/eeg.hexa`.
   - Help text: `router` line in two places marked `[DEPRECATED v1.3.0]`.
5. **Updated `.roadmap.hexa_brain`** header version `1.1.0` → `1.3.0`,
   added `legacy_scrub_2026_05_05` field documenting the scrub manifest
   (scrubbed list, blocked-by-dependency list, deprecation strategy,
6. **Updated `eeg/README.ai.md`** + `eeg/module/README.ai.md` to mark
   `eeg.hexa` as `[SCRUBBED v1.3.0 → eeg/legacy/eeg.hexa]`.
7. **Wrote CHANGELOG.md v1.3.0 entry** (Removed / Changed / Not scrubbed
   / Migration / 6 honest C3 disclosures).
8. **Wrote this doc** (`docs/ai-native/v1_3_0_legacy_scrub_2026_05_05.ai.md`).
9. **Commit + push + tag v1.3.0** to `origin/main`.

## §2 Scrub manifest

| File | Before | After | Rationale |
|------|--------|-------|-----------|
| `eeg/eeg.hexa` | active in `bin/hexa-brain router` verb | `eeg/legacy/eeg.hexa` (deprecation header) | Phase 4b TODO-stub, all bodies `TODO`, superseded by `eeg_setup.hexa` + `bin/hexa-brain`. |

| File | Spec class | Verdict | Reason |
|------|-----------|---------|--------|
| `eeg/impedance_check.hexa` | Tier 1 (per spec) | **NOT SCRUBBED** | Distinct role per canonical neighbor's header (one-shot diagnostic, not superseded). 4 active session-protocol consumers. |


Before v1.3.0:
- `eeg_setup.hexa` was the canonical 10-subcommand dispatcher.
- `eeg.hexa` (TODO-stub) was a duplicate router with no real bodies but
  occupied the `eeg/eeg.hexa` filename in active code.

After v1.3.0:
- `eeg_setup.hexa` is the **single** canonical dispatcher in active
  `eeg/`. Any future references to "the eeg dispatcher" unambiguously
  resolve there.
- `eeg/legacy/eeg.hexa` exists for backwards-compat reads only; the
  deprecation warning in `bin/hexa-brain` actively steers consumers
  away from it.


1. **Scrub is reversible**. `git mv` preserves blob history; restoring
   the prior state is a single `git revert <v1.3.0-commit>` or a manual
   `git mv eeg/legacy/eeg.hexa eeg/eeg.hexa` plus rolling back
   `bin/hexa-brain`'s `router` verb routing change. No data loss.
2. **`legacy/` subdirectory adds clutter**. `ls eeg/` now shows a
   subdirectory that didn't exist in v1.2.0. Tab-completion may surface
   `eeg/legacy/...` paths to unfamiliar users; future agents reading
   `eeg/` may waste time investigating the legacy file before realizing
   it's deprecated.
3. **Existing CI / scripts may break**. Any external script using
   `hexa run anima-eeg/eeg.hexa` (legacy anima monorepo path) or
   `hexa run hexa-brain/eeg/eeg.hexa` (post-v1.0.0 path) will now miss
   the file. The migration path is documented in CHANGELOG and this
   handoff, but adoption is not enforced. A future grep across
   downstream repos may surface stale references.
4. **Deprecation warning vs hard removal**. Chose soft deprecation
   (warning + dispatch) over hard removal (exit 1) to honor the
   spec's "additive" mandate. This means the `router` verb still
   "works" for v1.3.0 consumers but with stderr noise. A future
   v2.0.0 release should harden the contract; this v1.3.0 release
   intentionally accepts the warning-only posture.
   router from active eeg/ tightens the canonical entry surface to
   `eeg_setup.hexa` only. This is good for clarity but raises the bar
   for downstream consumers expecting any other eeg-rooted dispatcher
   — they must adopt eeg_setup.hexa or bin/hexa-brain.
6. **`impedance_check.hexa` scrub blocked**. The spec author's intent
   was to retire it as Tier 1. Distinct-role analysis (one-shot
   diagnostic vs worn-helmet evidence) plus 4 active protocol
   dependencies argued against scrub. Honest verdict: spec was based
   on a misread of the canonical neighbor's header — that header
   describes them as *complementary* tools, not as one superseding
   the other. Future v1.4.0 may revisit if protocol dependencies
   migrate to `impedance_validate`.
7. **Deprecation warning fires unconditionally on `router`**. Even
   intentional usage (e.g., test harnesses verifying the legacy path
   resolves) now emits `WARN: 'router' is deprecated...` to stderr.
   No way to suppress without flag-plumbing change. Acceptable for
   v1.3.0 (warning is the point); revisit if it pollutes CI logs.

## §5 Verification

- `git log eeg/legacy/eeg.hexa` shows full history preserved
  (rename detected by git's similarity heuristic).
- `bin/hexa-brain eeg router --help` (or empty verb) emits warning
  to stderr, dispatches to `eeg/legacy/eeg.hexa` (which itself is a
  TODO-stub so will not produce useful output, but routing succeeds).
- `bin/hexa-brain eeg health|impedance|impedance-validate|adjust|...`
  all unaffected — they still route through `eeg_setup.hexa`.
- `hexa run eeg/eeg_setup.hexa list` enumerates 8 backends — all
  pre-v1.3.0 backends still present, none accidentally moved.
- Session protocols (jaw/blink/berger/preflight_settle) still
  reference `impedance_check.hexa` via direct `hexa run anima-eeg/...`
  paths — those paths are anima-monorepo paths (legacy reference
  string in protocol files), not hexa-brain working-tree paths.

## §6 Files touched

- `eeg/eeg.hexa` → `eeg/legacy/eeg.hexa` (rename + header marker)
- `bin/hexa-brain` (router verb deprecation + help text)
- `CHANGELOG.md` (v1.3.0 entry)
- `.roadmap.hexa_brain` (header version + legacy_scrub_2026_05_05 field)
- `eeg/README.ai.md` (eeg.hexa line in tree diagram)
- `eeg/module/README.ai.md` (caveat 2 updated)
- `docs/ai-native/v1_3_0_legacy_scrub_2026_05_05.ai.md` (this file)

## §7 Provenance

- **Spec**: BG-EEG-LEGACY-SCRUB inline (this conversation, 2026-05-05)
- **User authorization**: 2026-05-05 ("기존 쓸데없는 과거 체크시스템은 scrub")
- **Predecessor commit**: `82254bb0` (v1.2.0 cli canonical dispatch)
- **Tag**: `v1.3.0` annotated, pushed to `origin/main`
- **Anima monorepo**: NOT touched (no anima commits per spec CRITICAL section)
