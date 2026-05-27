# hexa-brain Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **License firewall (Sprint 1 Part A)** — `vendor/external_deps.yaml`
  (hand-curated SPDX catalog), `vendor/license_policy.yaml` (per-layer
  allow-list for `eeg/`, `eeg_core/`, `core/`, `tool/`),
  `vendor/README.ai.md`, `bin/check_licenses.sh` (bash + inline python3
  enforcer with falsifiers `F_LF_01/02/03`), `LICENSE_FIREWALL.md`
  (human-readable policy), `design/license_firewall.md` (design rationale).
  New top-level dispatcher verb `hexa-brain license-check` routes to the
  enforcer. AGPL-3.0 (BrainGenix-NES) and CC-BY-NC-4.0 (cl-sdk) are
  declared as `coupling: http`-only — tight `import` from the 4 protected
  layers is a hard fail. Marker + ledger pattern reused
  (`state/markers/license_firewall_check_<ts>.marker` +
  `state/license_firewall_checks.jsonl`). Verified: selftest 3/3 PASS,
  clean scan 198 files / 0 violations, manual injection caught.
- **Neuroglancer Precomputed export (Sprint 1 Part B-1)** —
  `eeg/export_neuroglancer.hexa`, hand-written MIT-clean writer
  (no Apache-2.0 import; mirrors `tool/module/_core/eeg_export.hexa`
  template), `--selftest` with 6 preregistered falsifiers, marker + ledger
  emission, `--verify` sub-mode (lazy-imports `neuroglancer`; gracefully
  skips on miss). CLI: `hexa-brain eeg export-neuroglancer
  --input <npy|dir|session.json> --output state/precomputed/<basename>`.
  Phase-1 `--mode=2d-time-series` only (16ch × time-samples × 1 singleton
  volume, 4 mean-pooled scales, `raw`/float32/Fortran-order encoding).
  Design doc: `design/core/neuroglancer_precomputed_export_2026_05_12.md`.
  Runbook: `eeg/doc/neuroglancer_export_runbook_2026_05_12.md`.
- **Substrate-agnostic interface (Sprint 1 Part E-1 foundation)** —
  `eeg/substrates/{substrate,synth_substrate,brainflow_substrate,replay_substrate,channel_set}.hexa`
  + `eeg/substrates/__init__.hexa` + `eeg/substrates/registry.yaml`
  + `eeg/substrates/README.ai.md` + `design/substrate_abstraction.md`.
  Declares an 11-method contract (`api_open_session`, `api_read_chunk`,
  `api_stim`, ...) with 3 active backends: deterministic synth (LCG seed=1
  mirroring `eeg/closed_loop.hexa:72-74`), brainflow shim (delegates
  lifecycle to `eeg/_session_manager.hexa`), replay (disk `.npy` playback,
  numpy optional). Plus `nes` / `cl1` declared-not-implemented entries in
  `registry.yaml` for Part C-1 / C-2. Falsifiers `F_SUB_PROTO_01..03` +
  `F_SUB_01..03` + `F_CS_01..03`. Refactor of `eeg/collect.hexa` /
  `eeg/eeg_recorder.hexa` / `eeg/dual_stream.hexa:211` to consume the
  substrate API is **deferred to a follow-up PR** — this landing is
  foundation only (contract version `v0`, semver-frozen at `v1` in the
  follow-up).
- **`eeg/protocols/README.ai.md`** — AI-native frontmatter doc for the
  protocols package (schema `hexa-brain/eeg/protocols/ai-native/1`) with a
  `substrates/` sibling section linking the new substrate package.

### Changed

- **`eeg/_session_manager.hexa`** — additively extended the emitted Python
  helper with four substrate-protocol methods (`api_read_chunk`,
  `api_get_eeg_indices`, `api_get_sample_rate`, `api_stim` — raises
  `NotImplementedError` for read-only scalp EEG). The new functions are
  inserted between `api_last_error` and `cmd_selftest`; `cmd_selftest` is
  byte-identical to v1.3.0 — `F_SM_01/02/03` PASS conditions unchanged
- **`bin/hexa-brain` dispatcher** — added top-level `license-check`
  subsystem (routes to `bin/check_licenses.sh`) and per-`eeg` verb
  `export-neuroglancer|export-ng` (routes to `eeg/export_neuroglancer.hexa`).
  Help text updated with new "TOP-LEVEL VERBS" section.
- **`LATTICE_POLICY.md` §3.4** — registered hexa-brain's license-firewall
  verifier as the machine-enforced gate for §1.3 "per-project verify
  scripts" requirement. Pattern is project-agnostic — other dancinlab
  projects integrating copyleft/NC code may adopt the same `vendor/*.yaml`
  + `bin/check_licenses.sh` shape.
- **`AGENTS.md`** — added license-firewall obligation paragraph alongside
  the honesty obligation.
- **`README.md`** — `Sister repositories` section: prose mention of
  "blocked only by CC BY-NC 4.0 license" replaced with link to
  `LICENSE_FIREWALL.md` (single citable home for the policy). Also added a
  one-liner advertising `hexa-brain eeg export-neuroglancer` next to the
  Google Connectomics tools list.
  helpers).
- **Substrate dispatch flag (E-1 follow-up Phase 1, 2026-05-12)** —
  `eeg/collect.hexa` and `eeg/eeg_recorder.hexa` accept
  `--substrate <brainflow|synth|replay>` and `--legacy-inline` (explicit
  alias for brainflow). Default `brainflow` keeps the existing inline
  BoardShim path **byte-identical** (collect: 812 lines / `F_T1..T12` all
  PASS; recorder: 739 lines / segment lifecycle untouched). For `synth`
  and `replay`, the modules emit a **pointer block** with
  `verdict=DEFERRED` and exit 0 — pointing the operator at the dedicated
  `hexa run` subprocess delegation was attempted but the hexa-interp
  sandbox (`pwd=/tmp/resource-tcp-*` cwd-isolation) breaks relative paths;
  full delegation deferred to Phase 2 (needs either `HEXA_PROJECT_ROOT`
  env or shim-translated absolute paths). `--substrate ≠ brainflow` is
  hard-rejected in `--collect` / `--record` modes with a clear advisory.
  Also extended `_flags_only_argv` in `eeg/collect.hexa`,
  `eeg/eeg_recorder.hexa`, and all five `eeg/substrates/*.hexa` files to
  strip `hexa_interp` argv[0] prefix (host-portability fix: hexa-real
  interp on darwin emits Linux build-dir path as argv[0]).
- **`eeg/dual_stream.hexa:211`** — Phase-5 forward-look comment updated
  to point at `eeg/substrates/replay_substrate.hexa` as the available
  wrapper-target. The real `compare_streams_from_files(anima_npy, eeg_npy)`
  wrapper itself is deferred (same subprocess-delegation blocker as
  above). Functional behavior of synthetic dual-stream correlation is
- **`design/substrate_abstraction.md`** — added §8 "E-1 follow-up
  landing record (2026-05-12)" documenting the Phase 1 dispatch landing,
  what was deferred and why, and the verification matrix (12/12 default
  collect selftest, 6+7+8 substrate module selftests, 3/3 license-check
  selftest, 5 honest-deferral cases).
- **Decisions confirmed (2026-05-12 session boundary, 6 items)** — the
  six reviewer-facing open questions from the 2026-05-12 boundary are
  resolved doc-only (no code change; Phase 1 behavior already matches
  decisions 1-2 / 4-6, and decision 3 locks a Phase 2 choice).
  **B-1 (Neuroglancer)** in `design/core/neuroglancer_precomputed_export_2026_05_12.md` §12:
  (1) `--verify` w/o `neuroglancer-py` → **PASS-with-skip**;
  (2) Ledger idempotency → **append one row per `--selftest`**;
  (3) Phase 2 helmet 3D coords → **MNE `standard_1020`** (BSD-3,
  license-firewall-friendly, no FreeSurfer dep).
  **E-1 (Substrate)** in `design/substrate_abstraction.md` §9:
  (4) `EXPECTED_DATA_ROWS` → **derive via `eeg_indices` slice** (no
  explicit field in spec dict);
  (5) Synth timestamp → **sim time (`samples_emitted / sample_rate`)
  with honest disclosure**, do not mix wall-clock;
  (6) `brainflow_substrate` selftest stub-fallback → **PASS as
  "shim contract OK"** (does not claim hardware-path correctness —
  that's `eeg/_session_manager.hexa --selftest` on a host with
  `.venv-eeg`).
- **`api_stim` signature widening (E-1 v0, 2026-05-12, supersedes
  Decision 4 same session)** — `api_stim(sess, ch_set, design) →
  unspecified` widened to `api_stim(sess, stim_spec) → StimResult`
  (CL1-SDK compatible dict signature + explicit result envelope).
  Caller count was 0 (all 3 active backends + `_session_manager`
  raise `NotImplementedError`); migration cost zero. Five completeness
  deltas: (1) 3-arg triple → 2-arg dict for `api_open_session(spec)`
  parity + CL1 HTTP body 1:1; (2) explicit `StimResult` envelope
  reusing `api_last_error` shape; (3) `wall_time_ns` field —
  required for closed-loop latency math under Decision 5 (synth ts =
  sim time); (4) `schema = "hexa-brain/substrate/stim/1"` for v2
  forward-compat dispatch; (5) `license_posture` + `stim_id` for
  Part A firewall check + marker/.jsonl ledger correlation.
  Touched: `eeg/substrates/substrate.hexa` (APPENDIX A + new
  `validate_stim_spec` helper + new `F_SUB_PROTO_04` falsifier + T7
  assertion + `STIM_SPEC_SCHEMA`/`ALLOWED_WAVEFORMS` exposed in
  `--inspect`), `eeg/substrates/{synth,brainflow,replay}_substrate.hexa`
  (signature + falsifier call-args), `eeg/_session_manager.hexa:480`
  (signature only; `cmd_selftest` byte-identical gate unaffected —
  `F_SM_01/02/03` PASS conditions stand). Authoritative spec:
  `eeg/substrates/substrate.hexa` APPENDIX A. Design rationale:
  `design/substrate_abstraction.md` §10. Verification on this Mac box
  **deferred** — `127.0.0.1:5555` TCP compute backend not running this
  is unverifiable until CL1 substrate (Part C-2) actually implements
  `api_stim`; current falsifier coverage is shape-only.
- **`eeg/substrates/_brainflow_helper.py` (E-1 Phase 2b, 2026-05-12)** —
  hand-maintained Python superseding the `parts.push("...")` Python
  heredoc that `eeg/substrates/brainflow_substrate.hexa` carried. Retires
  the RFC-016 §1.4 anti-pattern (".hexa carrying a Python body in a
  string heredoc, stringified + subprocess-executed") — the same pattern
  hexa-bio `_python_bridge/module/*.py`, the anima staging copy, and
  `stdlib/anima_audio_worker.hexa` also use. Two call surfaces: (1)
  embedded-CPython json-in/out wrappers (`open_session`, `read_chunk`,
  … — session objects live in a module `_SESSIONS` registry keyed by
  opaque `bf-<hex12>` strings, since they can't cross
  `py_call(module,fn,str)→str`) for the post-Phase-2c `import py` path;
  (2) standalone CLI (`python3 eeg/substrates/_brainflow_helper.py
  selftest`) so `hexa run brainflow_substrate.hexa --selftest` keeps
  working during migration. Verified on this Mac box: `selftest` 4/4 PASS
  (`F_SUB_02_shape/stim_raises/idempotent/json_surface`) + `inspect` OK
  (pure stdlib Python — no TCP/hardware). `eeg/substrates/brainflow_substrate.hexa`
  is **unchanged** in this PR — Phase 2c (rewrite the .hexa to delegate
  via `use "stdlib/python_ffi"` + `py_call`) is deferred pending TCP
  backend + `libhxpyembed.dylib` + real-hardware verification. Full staged
  plan (2b/2b-2/2c/2d/2e/2f) + `_brainflow_helper.py` interface table in
  are returned as nested lists in json (V1 string-only); a V2 zero-copy
  path via `stdlib/python_ffi.py_buffer_to_hexa` is deferred.
- **`eeg/_session_manager_helper.py` (E-1 Phase 2b-2, 2026-05-13)** —
  hand-maintained Python superseding the `parts.push("...")` heredoc that
  `eeg/_session_manager.hexa` emitted at
  `/tmp/anima_eeg_session_manager_helper.py`. **Byte-identical-preserving**:
  `cmd_selftest()` output is character-for-character identical, so the
  `F_SM_01/02/03` + `T_REC_01` + `T_ERR_01` PASS conditions in the .hexa's
  in-hexa assertions stand; the legacy `anima-eeg/` schema string,
  verbatim (identity-rename is a separate PR). `eeg/substrates/_brainflow_helper.py`'s
  `_try_load_session_manager()` now resolves `eeg/_session_manager_helper.py`
  via `__file__` (works regardless of cwd — the resource/tcp sandbox runs
  with `cwd=/tmp/resource-tcp-*`; never rely on cwd, see §11.1) ahead of
  the legacy `/tmp/` emit-copy. Verified on this Mac box (pure stdlib
  python): `python3 eeg/_session_manager_helper.py selftest` → all PASS +
  `inspect` OK; `_brainflow_helper.py selftest` →
  `session_manager_helper_present=True`, 4/4 PASS; cwd-from-`/tmp` test
  confirms `__file__`-based resolution. `eeg/_session_manager.hexa` is
  **unchanged** — rewriting it to ship the `.py` instead of emitting it
  needs `hexa run` (≡ TCP backend) to byte-diff; deferred. Plan:
  `design/substrate_abstraction.md` §11.
- **`eeg/_session_manager.hexa` `_flags_only_argv()` — `hexa_interp` strip
  (E-1 verification-infra completion, 2026-05-13)** — added `a.ends_with("hexa_interp")`
  case that was already in `collect.hexa` / `eeg_recorder.hexa` + the 5
  substrate files (commit `76494ad3`). Header-only change; `cmd_selftest`
  emit byte-identical → `F_SM_01/02/03` PASS conditions unchanged. Paired
  with the upstream `resource/tcp/exec_workers.py` fix (separate repo —
  see §11.7), this unblocks the **full `hexa run` verification surface**:
  `substrate.hexa` 7/7 (`F_SUB_PROTO_01..04`), `synth_substrate.hexa` 7/7,
  `brainflow_substrate.hexa` 6/6, `replay_substrate.hexa` 8/8,
  `_session_manager.hexa` 9/9 (incl. sentinel), `collect.hexa` 12/12
  (byte-identical gate intact — api_stim widening at
  `_session_manager.hexa:480` did not perturb `cmd_selftest`). All PASS
  on this Mac box, recursion-free (0 procs after each run). The earlier
  hexa-run blocker (§11.6) is resolved; 2b-3 onward are now unblocked
  except for `libhxpyembed.dylib` (2c) and real OpenBCI (2c/2d) gates.
  (not hexa-brain) — `_resolve_hexa_interp_argv0()` resolves
  `~/.hx/packages/hexa/build/hexa_interp.real` and exposes it via a
  `$TMPDIR/hexa_interp` symlink (so argv[0] ends in `hexa_interp`, matching
  the .hexa strip pattern); `hexa_script_worker` now calls
  `argv_prefix=[<symlink>]` + `RESOURCE_LOCAL_HEXA=1` instead of
  `[hexa, "run"]`, ending the self-referential TCP recursion.
- **`libhxpyembed.dylib` build cleared (E-1 Phase 2c dep, 2026-05-13)** —
  `cmake -S lib/hxpyembed -B lib/hxpyembed/build && cmake --build` from
  `~/core/hexa-lang/`: 35584-byte Mach-O dylib at
  `~/core/hexa-lang/lib/hxpyembed/build/libhxpyembed.dylib`, linked against
  Python 3.14 (Homebrew `python@3.14`, AppleClang 21). PoC integration:
  `hexa run ~/core/hexa-lang/bench/import_py_e2e.hexa` → `py-repr ` output,
  exit 0, recursion-free. Confirms the full chain — hexa source → `py_call`
  → `hxpy_call_str` → embedded CPython → string round-trip — works on this
  Mac box. Phase 2c (`brainflow_substrate.hexa` v2 with `use
  "stdlib/python_ffi"` + `py_call("_brainflow_helper", ...)`) remaining
  blocker narrows to *only* the numpy data-path regression on real OpenBCI
  Cyton+Daisy. Full record: `design/substrate_abstraction.md` §11.8.
  need its own native build (no shared dylib).
- **`eeg/_neuroglancer_helmet_helper.py` (B-1 Phase 2 V1, 2026-05-13)** —
  hand-maintained Python (RFC-016 §1.4 avoided per Phase 2b precedent)
  emitting the **coordinate inventory** layer for `--mode=helmet-annotation`.
  Uses MNE `standard_1020` (decision 3) via lazy import; falls back to a
  hand-curated 10-20 fixture if MNE absent (selftest still passes,
  `coord_source=fixture` honest disclosure). 16-channel CYTON_DAISY order
  (`Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7, F8, F3, F4, T7, T8, P3, P4`)
  matches `eeg/substrates/channel_set.hexa`. Sidecar `meta.json` shape:
  `{schema, coord_source, coord_units:"meters", coord_frame, channels:[{name,xyz},…]}`.
  Falsifiers `F_NG_HA_01..03` (channel count + 3-tuple xyz / label order /
  write→read round-trip). Verified on this Mac (no MNE installed):
  `python3 eeg/_neuroglancer_helmet_helper.py selftest` → 3/3 PASS,
  exit 0. Phase 2.1 (Neuroglancer viewer URL composition + wire-up in
  `export_neuroglancer.hexa --mode=helmet-annotation`) deferred — the
  helper.py is the coordinate-source dependency; the hexa-side integration
  Full record: `design/core/neuroglancer_precomputed_export_2026_05_12.md` §13.
- **`reference/BrainGenix-NES/` cloned (C-1 NES adapter prep, 2026-05-13)** —
  `git clone --depth=1 https://gitlab.braingenix.org/carboncopies/BrainGenix-NES.git
  /Users/ghost/core/reference/BrainGenix-NES`. Upstream contains `Docs/API.md`
  (REST API spec — endpoint inventory pending a follow-up walk-through),
  `Source/Core/` + `Source/Renderer/` (C++ principal components +
  GPU-accelerated 3D rendering for VSDA EM/CA), `Tools/Setup.sh + Build.sh`
  C3: clone is in the dancinlab-monorepo `reference/` (not hexa-brain repo
  — no source absorption). C-1 adapter (`eeg/substrates/sim_nes.hexa` +
  Docker `127.0.0.1:8410` loopback) still needs the user's docker probe +
  curl REST capture, but the clone gives us local `Docs/API.md` to scan for
  the endpoint inventory without first booting the container.

## [1.3.0] — 2026-05-05

### Removed (scrubbed to `eeg/legacy/`)

- **`eeg/eeg.hexa`** → `eeg/legacy/eeg.hexa` — Phase 4b stub with all-TODO
  function bodies (62 LOC, no real syscalls / BrainFlow integration).
  dispatcher) + `bin/hexa-brain` (top-level kebab-case CLI). The file is
  preserved at `eeg/legacy/eeg.hexa` for backwards-compat with the
  `hexa-brain eeg router` verb (which still routes there but now emits
  a deprecation warning).

### Changed

- **`bin/hexa-brain` CLI** — `router` verb (and empty-verb fallback) now
  emits `WARN: 'router' is deprecated (v1.3.0)` to stderr before
  dispatching to `eeg/legacy/eeg.hexa`. Help text marks `router` as
  `[DEPRECATED v1.3.0]`. Migrate to canonical verbs
  (`hexa-brain eeg <verb>` per `hexa-brain eeg help`) or
  `hexa run eeg/eeg_setup.hexa <subcommand>`.
- **`.roadmap.hexa_brain`** — added `legacy_scrub_2026_05_05` field on
  `hexa_brain.cond.1` documenting the scrub manifest.

### Not scrubbed (active dependencies — preserved as canonical)

- **`eeg/impedance_check.hexa`** — although the BG-EEG-LEGACY-SCRUB spec
  listed this as a Tier 1 scrub candidate ("superseded by
  impedance_real_hardware_validation.hexa per its header"), audit showed
  the canonical neighbor's header actually states a *distinct* role:
  "impedance_check is the one-shot diagnostic; this runner is the
  canonical evidence producer for 헬멧 착용 후 실측 sessions." The two
  files have non-overlapping roles. Additionally, `impedance_check.hexa`
  has 4 active session-protocol consumers (jaw / blink / berger /
  preflight_settle). Scrub blocked by active dependency; preserve.

### Migration notes

- Existing scripts using `hexa-brain eeg router` continue to work
  (legacy file still exists, dispatch still succeeds), but they will
  see a stderr deprecation warning. Migrate to canonical verbs.
- Direct `hexa run eeg/eeg.hexa` paths must update to
  `hexa run eeg/legacy/eeg.hexa` (or migrate to `eeg_setup.hexa`).
- No anima-monorepo-side changes — anima callers are unaffected.


1. **Scrub is reversible** — `git mv` preserves history; `git revert
   <v1.3.0-commit>` (or `git mv eeg/legacy/eeg.hexa eeg/eeg.hexa` plus
   bin/hexa-brain rollback) restores the prior state.
2. **`legacy/` subdirectory adds clutter** — ls in `eeg/` now shows a
   subdir that didn't exist in v1.2.0. Tab-completion may surface
   `eeg/legacy/...` paths to unfamiliar users.
3. **Existing CI / scripts may break** — any external script using
   `hexa run anima-eeg/eeg.hexa` (legacy anima path) or
   `hexa run hexa-brain/eeg/eeg.hexa` (post-v1.0.0 path) will now miss
   the file. Migration path: update to legacy/ or canonical verbs.
4. **Deprecation warning vs hard removal** — chose soft deprecation
   (warning + dispatch) over hard removal (exit 1) to honor the
   "additive" spec mandate. A future major version (v2.0.0) may
   harden this to an error.
   from active eeg/ tightens the canonical entry surface to
   `eeg_setup.hexa` only. Downstream consumers expecting any other
   eeg-rooted dispatcher must adopt eeg_setup.hexa or bin/hexa-brain.
6. **`impedance_check.hexa` scrub blocked** — spec author intent was
   to retire it, but distinct-role analysis (one-shot diagnostic vs
   worn-helmet evidence) plus 4 active protocol dependencies argue
   against. Honest verdict: spec was based on misread of canonical
   header. Future v1.4.0 may revisit if protocol dependencies migrate
   to `impedance_validate`.

## [1.2.0] — 2026-05-05

### Changed

- **`bin/hexa-brain` CLI eeg subsystem** — route 10 canonical verbs through
  Previously the v1.1.0 dispatcher invoked individual hexa files directly
  (e.g., `eeg impedance` → `impedance_check.hexa`), bypassing the canonical
  single-entry-point.
- **Help text** — added explicit canonical-vs-direct verb distinction at both
  top-level (`hexa-brain --help`) and subsystem-level (`hexa-brain eeg help`).
  Phase E worn-helmet quick-flow recipe added (health → adjust →
  impedance-validate → full → collect → analyze).

### Added

- **5 missing canonical verbs** (previously absent from v1.1.0 CLI):
  - `impedance-validate` ⭐ canonical worn-helmet 5-state JSONL evidence
    (routes to `impedance_real_hardware_validation.hexa` via eeg_setup).
  - `headplot` (ASCII 10-20 head plot via `headplot_helper.hexa`).
  - `rich` (Rich TUI variant of adjust, 3-panel layout via
    `electrode_helper_rich.hexa`).
  - `list` (enumerate eeg_setup.hexa subcommands + their backend files).
  - `selftest` (run `--selftest` on every backend, PASS/FAIL summary).
- **`--list-canonical` flag** — `hexa-brain eeg --list-canonical` dispatches
  to `eeg_setup.hexa list` for live enumeration of canonical subcommands.

### Migration notes

- Existing CLI invocations (e.g., `hexa-brain eeg board-health`,
  `hexa-brain eeg electrode-adjust`, `hexa-brain eeg full-helmet-view`)
  continue to work — kebab-case aliases preserved for backwards-compat.
- Direct hexa verbs (`collect`, `calibrate`, `analyze`, `experiment`,
  `closed-loop`, `validate`, `realtime`, `lsl-capture`, `dual-stream`,
  `neurofeedback`, `router`) unchanged — eeg_setup.hexa has no subcommand
  for these, so direct dispatch is preserved.


1. **Alias proliferation may confuse**: each canonical verb now has 2-3
   spellings (e.g., `health` + `board-health`, `adjust` + `electrode-adjust`,
   `record` + `recorder`, `full` + `full-helmet-view`,
   `impedance-validate` + `impedance_validate`). Discoverability via
   `--help` is OK but `compgen` / shell-completion may show duplicates.
2. **Indirection layer added**: canonical verbs invoke
   `hexa run eeg_setup.hexa <subcommand> ...` which then internally invokes
   `hexa run <backend>.hexa ...`. Adds ~50ms cold-start latency vs direct
   v1.1.0 dispatch and one extra process in `pstree`.
   anima-internal pattern, not a hexa-lang-wide standard. hexa-brain
   adopts it for eeg subsystem consistency with anima/anima-eeg/, but
   non-anima downstream consumers may find the indirection unnecessary.
4. **`list` and `selftest` invoke ALL backends**: `selftest` opens 8
   subprocess invocations (one per canonical backend); cost is
   non-trivial on cold cache (~5-10s end-to-end) and may surface
   transient hardware errors that are not session-relevant.
5. **Help text grew significantly**: `hexa-brain --help` body grew from
   ~50 lines (v1.1.0) to ~75 lines (v1.2.0); top-level help now needs
   pagination on smaller terminals (`less` recommended). The eeg
   subsystem help also grew to differentiate canonical-vs-direct verb
   classes.

## [1.1.0] — 2026-05-04

### Added

- **`core/` subsystem** — anima-eeg-core/ migrated as second subsystem.
  - **5 paradigms** (`tool/module/_paradigms/`): `resting_baseline`,
    `daily_life`, `visual_p300`, `auditory_p300`, `_integration_test`.
  - **20 metrics** (`tool/module/_metrics/`) including pure-native ports:
    `hjorth_native`, `lz76_native`, `pe_native`, `phi_proxy_native`,
    `gamma_theta_native`, plus alpha/PLV/spectral entropy/coherence variants.
  - **5 gates** (`tool/module/_gates/`): `hjorth_band`, `rms_band`,
    `composite_gate`, `pe_saturation`, `berger_alpha`.
  - **11 artifact detectors** (`tool/module/_artifact/`): EMG, electrode
    aging, reference drift, rail flat, AI cleaning pipeline, ECG/heart, eye
    blink, motion, EMI, HPF DC drift, meta classifier.
  - **9 integrations** (`tool/module/_integrations/`): clm_eeg p1/p2/p3,
    rsn/berger validators, multi-subject aggregate, synthetic fixture, etc.
  - **6 hardware modules** (`tool/module/_hw/`): `recorder`, `headplot`,
    `board_health`, `impedance`, `adjustment`, `_integration_test`.
  - **9 core utilities** (`tool/module/_core/`): `eeg_export`,
    `jsonl_audit`, `_adapter`, `filter_pipeline`, `pipeline_suggester`,
    `falsifier_runner`, `chflags_lock`, `npy_loader`, `_integration_test`.
  - **2 PRNG modules** (`tool/module/_prng/`): `pcg32_native`,
    `splitmix64_native`.
  - Top-level entry: `tool/core/eeg_core.hexa`.
  - Source: `anima/anima-eeg-core/` subtree split @ anima HEAD `1b306eec24`,
    44 commits preserved.
  - On-disk: 1.3MB, 68 hexa files.
- **CLI dispatcher** at `bin/hexa-brain`:
  - Routes `hexa-brain eeg <verb>` to `eeg/*.hexa` files.
  - Routes `hexa-brain core <verb>` to `tool/module/.../*.hexa` files.
  - `hexa-brain --help` shows both subsystems' verbs.
  - `hexa-brain --version` reads version from this CHANGELOG.
  - 16 eeg verbs, 14 core verbs, plus fall-through to subsystem routers.

### Changed

- **Repo layout reorganized** — eeg subsystem moved from repo-root to `eeg/`
  subdirectory to make room for `core/`. All paths now use `eeg/<file>.hexa`
  format. Existing `bin/hexa-brain` shim updated to dual-subsystem dispatcher.
  Pre-v1.1.0 paths in commit history reference repo-root; working-tree paths
  are `eeg/...` going forward (pure rename, no content change).
- **`.roadmap.hexa_brain` v1.1.0** — adds `cond.1b` for the core subsystem
  alongside existing `cond.1` (scalp EEG). Both substrate-v1 conditions are
  now COMPLETE; v2-v5 ladder unchanged.
- **README.md** — documents both subsystems, dispatcher usage, dual quickstart.


1. **Core subsystem maturity asymmetry**: eeg/ has 7 production cycles of real
   hardware evidence; core/ paradigms + metrics are mostly spec/synthetic-fixture
   tested, with selected real-data integration via `clm_eeg_p[1-3]` consumers
   in anima. Treat core/ as research-stage rather than production-ready.
2. **Cross-subsystem integration not stabilized**: `tool/module/_hw/` has
   overlapping concerns with `eeg/` hardware drivers; consolidation deferred.
   No formal interface contract between eeg/ and core/ yet.
3. **CLI dispatcher is bash-only**: `bin/hexa-brain` is a bash shim, not a
   hexa-native binary. Linux/macOS only; Windows users need WSL or hexa-native
   wrapper port.
4. **Test coverage uneven**: most `_integration_test.hexa` modules in core/ are
   synthetic-fixture only; real-hardware integration tests live in eeg/ but
   gate only the v1 substrate. v2-v5 substrates have no test scaffolding yet.
5. **44-commit core/ history**: history is from anima-eeg-core/ subtree split,
   so commit messages reference `anima-eeg-core/`-rooted paths that no longer
   exist (now under `core/`). No functional break; rebase intentionally avoided
   to preserve attribution.

### Provenance

- **Spinoff source**: <https://github.com/dancinlab/anima>
- **Spinoff commit (anima HEAD)**: `1b306eec24999ffd28505995655674b0f2beaa31`
- **eeg subtree prefix**: `anima-eeg/` (83 hexa files, 14MB inc. recordings)
- **core subtree prefix**: `anima-eeg-core/` (68 hexa files, 1.3MB)
- **Combined**: 151 hexa files, ~15MB on disk (recordings dominate eeg/).

---

## [1.0.0] — 2026-05-04

### Added

- **Initial standalone release** — spun off from `anima/anima-eeg/` after
  7 production cycles on real OpenBCI Cyton+Daisy 16ch hardware.
- **30 hexa CLI tools** at repo root, organized into 6 functional tiers:
  - **Hardware drivers** (`board_health_check.hexa`, `_port_lock_detector.hexa`,
    `_session_manager.hexa`, `eeg_ftdi_latency_fix.hexa`, `ads1299_settings.hexa`).
  - **Calibration** (`calibrate.hexa`, `electrode_adjustment_helper.hexa`,
    `electrode_helper_rich.hexa`, `headplot_helper.hexa`, `impedance_check.hexa`,
    `impedance_real_hardware_validation.hexa`).
  - **Acquisition** (`collect.hexa`, `lsl_capture.hexa`, `dual_stream.hexa`,
    `eeg_recorder.hexa`, `eeg_brainflow_sanity.hexa`, `eeg_setup.hexa`).
  - **Analysis** (`analyze.hexa`, `eeg_filter.hexa`, `validate_consciousness.hexa`,
    `full_helmet_view.hexa`, `transplant_eeg_verify.hexa`).
  - **Protocols** (`closed_loop.hexa`, `experiment.hexa`, `realtime.hexa`,
    `neurofeedback.hexa`, `rp_adaptive_response.hexa`,
    `board_health_check_lsl.hexa`, plus `protocols/{bci_control,emotion_sync,multi_eeg,sleep_protocol}.hexa`).
  - **Entry surface** (`eeg.hexa` — top-level CLI router).
- **Canonical session recordings** in `recordings/sessions/` (Berger eyes-open/closed,
  jaw artifact, blink artifact, alpha-blocking) — real-hardware evidence for v1.
- **`.roadmap.hexa_brain`** — mk2 SSOT JSONL with v1-v5 substrate ladder
  (scalp EEG -> intracranial -> high-density arrays -> closed-loop BMI -> chronic implant).
- **GitHub-only distribution.** Canonical at <https://github.com/dancinlab/hexa-brain>.
- **Branding**: 🧠 (primary) / ⬢🧠 (compound, hexa-lang sister marker).

### Provenance

- **Spinoff source**: <https://github.com/dancinlab/anima>
- **Spinoff commit (anima HEAD)**: `1b306eec24999ffd28505995655674b0f2beaa31`
- **Subtree prefix**: `anima-eeg/`
- **Subtree split**: full git history preserved, rooted at directory contents.
- **Upstream parent**: `anima/anima-eeg/` retained during stabilization period
  (deletion deferred to next cycle pending cross-repo dependency interface
  stabilization).


1. v1 only is production-ready; v2-v5 are spec-phase research direction declarations.
2. Hardware-specific (OpenBCI BrainFlow + ADS1299); other vendors not yet ported.
3. macOS primary; Linux less-tested; Windows untested.
4. Subtree split may have orphan blob references in old commit messages
   (cross-references to other anima subdirectories) — no functional break in
   working tree paths.
5. Sister-repo coupling with anima consciousness runtime via WebSocket events
   is not yet a frozen versioned API contract.
