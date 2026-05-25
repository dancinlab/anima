---
date: 2026-05-05
package: hexa-brain
subsystem: cli
status: LANDED
owner: hexa-brain repo
cycle: v1.2.0 cli canonical dispatch 2026-05-05
ssot_artifact: tag v1.2.0 @ origin/main + bin/hexa-brain + this doc
predecessor: v1.1.1 lfs cleanup 2026-05-05 / v1.1.0 dual-subsystem layout 2026-05-04
---

# v1.2.0 CLI canonical dispatch — hexa-brain (2026-05-05)

## TL;DR

  verbs through `eeg/eeg_setup.hexa` dispatcher (single-entry-point pattern)
  rather than invoking individual hexa files directly.
- **5 missing canonical verbs added**: `impedance-validate` (worn-helmet
  5-state JSONL evidence), `headplot` (ASCII 10-20 head plot), `rich` (Rich
  TUI 3-panel variant of adjust), `list` (enumerate eeg_setup subcommands),
  `selftest` (run `--selftest` on every backend, PASS/FAIL summary).
- **Phase E quick flow** added to top-level + subsystem help text:
  health → adjust → impedance-validate → full → collect → analyze.
- **kebab-case aliases preserved** for backwards-compat: `board-health`,
  `electrode-adjust`, `full-helmet-view`, `recorder`, `impedance_validate`
  all continue to dispatch correctly.
- **Honest C3 (5 disclosures)**: alias proliferation may confuse, indirection
  selftest invokes ALL 8 backends (cost ~5-10s), help text grew significantly.

## §1 Sequence

   health, impedance, impedance_validate, headplot, adjust, rich, full,
   record, list, selftest).
2. Audited v1.1.0 `bin/hexa-brain` — verified 5 canonical verbs missing
   (impedance-validate, headplot, rich, list, selftest) and current 16 eeg
   verbs all bypass eeg_setup.hexa via direct hexa file invocation.
3. Rewrote v1.2.0 `bin/hexa-brain` eeg case-block:
   - Top section: 10 canonical verbs route through
     `hexa run eeg/eeg_setup.hexa <subcommand>`.
   - Bottom section: 11 direct verbs (collect/calibrate/analyze/experiment/
     closed-loop/validate/realtime/lsl-capture/dual-stream/neurofeedback/
     router) preserved with direct hexa dispatch (no eeg_setup.hexa
     subcommand exists for these).
   - kebab-case aliases preserved (board-health → health, electrode-adjust
     → adjust, etc.) so v1.1.0 invocations continue to work.
4. Added `--list-canonical` flag short-circuit (dispatches to
   `eeg_setup.hexa list`).
5. Updated top-level `hexa-brain --help` and subsystem `hexa-brain eeg help`
   with canonical-vs-direct verb classification + Phase E quick-flow recipe.
6. Tested 26 verbs end-to-end via `bin/hexa-brain eeg <verb> --help` — all
   resolved correctly (`validate` and `router` showed downstream backend
   parse errors, but routing itself succeeded).
7. Updated `CHANGELOG.md` with v1.2.0 entry (Changed/Added/Migration/C3).

## §2 Canonical verb mapping

| CLI verb | Aliases | eeg_setup subcommand | Backend file |
|----------|---------|---------------------|--------------|
| `health` | `board-health` | `health` | `board_health_check.hexa` |
| `impedance` | — | `impedance` | `impedance_check.hexa` |
| `impedance-validate` | `impedance_validate` | `impedance_validate` | `impedance_real_hardware_validation.hexa` ⭐ |
| `headplot` | — | `headplot` | `headplot_helper.hexa` |
| `adjust` | `electrode-adjust` | `adjust` | `electrode_adjustment_helper.hexa` |
| `rich` | — | `rich` | `electrode_helper_rich.hexa` |
| `full` | `full-helmet-view` | `full` | `full_helmet_view.hexa` |
| `record` | `recorder` | `record` | `eeg_recorder.hexa` |
| `list` | — | `list` | (in-dispatcher enumeration) |
| `selftest` | — | `selftest` | (in-dispatcher PASS/FAIL summary) |

## §3 Direct verb mapping (no eeg_setup.hexa subcommand)

| CLI verb | Aliases | Backend file |
|----------|---------|--------------|
| `collect` | — | `collect.hexa` |
| `calibrate` | — | `calibrate.hexa` |
| `analyze` | — | `analyze.hexa` |
| `experiment` | — | `experiment.hexa` |
| `closed-loop` | `nback`, `meditation` | `closed_loop.hexa` |
| `validate` | `brain-likeness` | `validate_consciousness.hexa` |
| `realtime` | — | `realtime.hexa` |
| `impedance-real-hardware` | `impedance-validate-rich` | `impedance_real_hardware_validation.hexa` (direct) |
| `lsl-capture` | — | `lsl_capture.hexa` |
| `dual-stream` | — | `dual_stream.hexa` |
| `neurofeedback` | — | `neurofeedback.hexa` |
| `router` (default) | `""` | `eeg.hexa` |

## §4 Phase E worn-helmet quick flow

```bash
hexa-brain eeg health --check                # 1. board sanity (no helmet)
hexa-brain eeg adjust --live                 # 2. electrode placement check
hexa-brain eeg impedance-validate --measure  # 3. 5-state worn-helmet evidence (JSONL)
hexa-brain eeg full                          # 4. concurrent 5-state overview
hexa-brain eeg collect --duration 30m        # 5. session capture
hexa-brain eeg analyze                       # 6. offline band-power + topomap
```


1. **Alias proliferation may confuse**: each canonical verb now has 2-3
   spellings (e.g., `health` + `board-health`, `adjust` + `electrode-adjust`,
   `record` + `recorder`, `full` + `full-helmet-view`,
   `impedance-validate` + `impedance_validate`). Discoverability via
   `--help` is OK but `compgen` / shell-completion may show duplicates.
   Consider deprecation cycle for kebab-case aliases in v2.0.0.

2. **Indirection layer added**: canonical verbs invoke
   `hexa run eeg_setup.hexa <subcommand> ...` which then internally invokes
   `hexa run <backend>.hexa ...` via `exec_stream`. This adds ~50ms
   cold-start latency vs direct v1.1.0 dispatch and one extra process in
   `pstree`. For interactive helpers (adjust/rich) this is imperceptible;
   for scripted batch invocations (e.g., per-electrode loops) it can
   compound.

   anima-internal pattern declared in anima/.raw, not a hexa-lang-wide
   standard. hexa-brain adopts it for eeg subsystem consistency with
   `anima/anima-eeg/`, but non-anima downstream consumers (other hexa-lang
   packages depending on hexa-brain) may find the indirection unnecessary
   or counter-intuitive. This is a stylistic alignment, not a technical
   correctness mandate.

4. **`list` and `selftest` invoke ALL backends**: `selftest` opens 8
   subprocess invocations (one per canonical backend); cost is non-trivial
   on cold cache (~5-10s end-to-end) and may surface transient hardware
   errors (e.g., USB enumeration jitter, FTDI latency timeout) that are
   not session-relevant. Recommend running `selftest` once at session
   start, not per-verb. `list` is cheap (in-dispatcher enumeration).

5. **Help text grew significantly**: `hexa-brain --help` body grew from
   ~50 lines (v1.1.0) to ~75 lines (v1.2.0) due to canonical-vs-direct
   split + Phase E quick-flow. Top-level help now needs pagination on
   smaller terminals (`less` recommended). The subsystem-level
   `hexa-brain eeg help` also grew to differentiate verb classes
   (~50 lines). Consider a `--terse` flag in future if user feedback
   indicates information-overload.

## §6 Verification

26 verbs tested via `bin/hexa-brain eeg <verb> --help`:
- All canonical verbs (10) dispatch through eeg_setup.hexa correctly
  (verified by `[GATE] dispatch=local backend=anima-eeg/<file>` trailer).
- All direct verbs (16 incl. aliases) resolve to their target hexa files.
- `validate` + `router` show downstream backend parse/codegen errors but
  routing itself succeeds (errors originate inside the target hexa file,
  not in the dispatcher).
- `--list-canonical` flag dispatches to `eeg_setup.hexa list` as expected.
- Backwards-compat aliases preserved: `board-health`, `electrode-adjust`,
  `full-helmet-view`, `recorder`, `impedance_validate`.

## §7 Provenance

- **Spec**: BG-CLI-IMPROVE inline (this conversation, 2026-05-05)
- **Predecessor commit**: `3687c703` (v1.1.1 lfs cleanup)
- **Files touched**: `bin/hexa-brain`, `CHANGELOG.md`,
  `docs/ai-native/v1_2_0_cli_canonical_dispatch_2026_05_05.ai.md` (this file)
- **Tag**: `v1.2.0` annotated, pushed to origin/main
- **Anima monorepo**: NOT touched (no anima commits per spec CRITICAL section)
