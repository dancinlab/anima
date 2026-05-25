# Substrate Abstraction — design rationale (E-1)

**Status:** Phase 1 dispatch landed, contract version stays `v0`. `--substrate=` flag is now wired into `eeg/collect.hexa` and `eeg/eeg_recorder.hexa`, but selftest delegation runs in **pointer mode** (verdict `DEFERRED`), not real subprocess invocation. The brainflow path is **completely untouched** — Phase 2 will move it onto `brainflow_substrate.api_open_session`. See §8 below for the 2026-05-12 follow-up record.

**Authoritative interface declaration:** `eeg/substrates/substrate.hexa`
**Reference backends:** `eeg/substrates/{synth,brainflow,replay}_substrate.hexa`
**Registry:** `eeg/substrates/registry.yaml`

---

## 1. Why "substrate" and not "board"?

Sprint 1's goal is a v3-v5 closed-loop platform where the EEG (scalp) substrate, the BrainGenix-NES virtual-brain substrate, the Cortical Labs CL1 living-neuron substrate, and a disk-replay substrate are all interchangeable. "Board" implies a piece of OpenBCI hardware; "substrate" generalizes over hardware, simulators, live cultures, and replay.

The substrate API is the **single** call-site contract for everything that emits sample-stream data with a timestamp.

---

## 2. Contract surface (v0)

All backends MUST expose 11 functions:

| Method | Purpose | Read-only? |
|---|---|---|
| `api_open_session(spec)` | construct + transition to `INIT` | — |
| `api_start_recording(s, name, fmt, max_min)` | transition `INIT → RUNNING`, allocate sink | — |
| `api_read_chunk(s, n_max)` | pull up to `n_max` samples as `(data: list-of-lists float32, ts: float)` | yes |
| `api_get_eeg_indices(s)` | return 1-indexed EEG channel ids (rows in `data` that are EEG, not aux) | yes |
| `api_get_sample_rate(s)` | return Hz | yes |
| `api_stim(s, ch_set, design)` | inject stimulus — DEFAULT `raise NotImplementedError` | — |
| `api_stop_recording(rec)` | transition `RUNNING → INIT` | — |
| `api_reinit(s)` | atomic close + open; returns new session | — |
| `api_on_shutdown_hook(s, fn)` | bind atexit + SIGTERM + SIGINT | — |
| `api_last_error(s)` | `{code, advisory_url, retry_action}` | yes |

### State machine

```
PREINIT ──open──▶ INIT ──start──▶ RUNNING ──stop──▶ INIT
                                        │
                                        └─close─▶ HALTED
INIT ──close──▶ HALTED
HALTED ──reinit──▶ INIT    (NEW session; original stays HALTED)
ANY ──SIGTERM/atexit──▶ HALTED   (best effort)
```

Mirrors the audit-derived state machine in `eeg/_session_manager.hexa:32-39`. Substrate backends inherit this state taxonomy.

### Spec dict shape

```python
{
  "backend":         "brainflow" | "synth" | "replay",
  "board_id":        int,                  # ignored by synth/replay (informational)
  "port":            str | None,           # ignored by synth/replay
  "channel_set":     CHANNEL_SET | None,   # see channel_set.hexa
  "license_posture": LICENSE_POSTURE | None,
  "path":            str | None            # required for backend=="replay"
}
```

`channel_set` shape (from `eeg/substrates/channel_set.hexa`):

```python
{
  "name":        str,                    # e.g. "cyton_daisy_16"
  "ids":         list[int],              # 1-indexed channel ids
  "sample_rate": int,                    # Hz
  "labels":      list[str] | None,       # 10-20 labels (Fp1, ...)
  "layout_2d":   list[[col, row]] | None,
}
```

`license_posture` shape (binds to Part A firewall):

```python
{
  "dep_id":   str,              # references vendor/external_deps.yaml
  "coupling": "in_process" | "http" | "subprocess" | "cli"
}
```

---

## 3. License-posture binding to firewall (Part A)

Part A (`vendor/external_deps.yaml` + `bin/check_licenses.sh`) machine-enforces the rule:

- `eeg/`, `eeg_core/`, `core/`, `tool/` may only `in_process` import code under {MIT, BSD-3, BSD-2, Apache-2.0, ISC}.
- AGPL-3.0 and CC-BY-NC-4.0 are admissible only via `coupling: http | subprocess | cli`.

The substrate `registry.yaml` is the **machine-readable mapping from backend id → dep_id → coupling**. Part A's check script can:

1. Walk `eeg/substrates/registry.yaml`, collect `(dep_id, coupling)` pairs for `status: active`.
2. Cross-reference each `dep_id` against `vendor/external_deps.yaml.<dep>.spdx`.
3. Reject any (license, coupling) pair forbidden by `vendor/license_policy.yaml`.

This is the structural reason every substrate must declare its `license_posture` — the firewall is **automated** at scan time, not enforced at runtime.

---

## 4. Deprecation path for inline BoardShim loops

Three files currently inline the BrainFlow lifecycle:

- `eeg/collect.hexa` — lines ~238-432 (prepare_session → start_stream → polling → release)
- `eeg/eeg_recorder.hexa` — lines ~155-348 (same pattern, recorder-flavor)
- `eeg/_session_manager.hexa` — SSOT module; **stays as-is** (the substrate wraps it)

The follow-up PR ("Part E-1 step 7") will:

1. Add `--substrate=brainflow|synth|replay` flag to collect.hexa and eeg_recorder.hexa (default `brainflow` — back-compat).
2. Add `--legacy-inline` escape hatch (one-release deprecation window).
3. Move the call-site from `BoardShim.prepare_session(...)` → `substrate.api_open_session({...})`.
4. Wire `eeg/dual_stream.hexa:211` (replay Phase 5 hole) → `replay_substrate.api_open_session(...)`.

The byte-identical regression gate after step 7 is:

```bash
# Old path — must remain green for one release
hexa run eeg/collect.hexa --selftest --legacy-inline

# New default — output must be byte-identical to old --selftest
hexa run eeg/collect.hexa --selftest --substrate=synth
```

---

## 5. API stability tier

| Version | Status | Compatible with |
|---|---|---|
| `v0` (this PR) | foundation; not exposed via CLI; subject to change with consent | reviewers + Part E-1 follow-up |
| `v1` (follow-up PR) | semver-frozen; `bin/hexa-brain` exposes `--substrate=` | external users, NES/CL1 adapters |

Promoting `v0 → v1` happens when:

1. `collect.hexa` + `eeg_recorder.hexa` refactor lands.
2. `bin/hexa-brain license-check` (Part A) verifies registry conformance.
3. Two consecutive merge windows pass without contract-breaking changes.

---

## 6. Open questions (for reviewer)

1. **Spec dict `data_rows` declaration.** Should the spec declare expected `data_rows` (32 for BrainFlow, 16 for synth/replay) so callers don't have to introspect `len(data)`? Pro: explicit. Con: redundant with `len(eeg_indices)`. Recommendation: skip — derive from `api_get_eeg_indices()` length.
2. **`channel_set` vs `electrode_montage`.** Naming. `channel_set` is the SDK-style; `electrode_montage` is the clinical neuroscience term. Picked `channel_set` for parity with BrainFlow `BoardShim.get_eeg_channels`. Open to rename if reviewer prefers.
4. **`api_stim` signature.** Currently `(sess, ch_set, design)`. Cortical Labs's `cl-sdk` uses `(channel_set, stim_design_dict)` separately. Refactor on CL1 integration if needed — `v0` allows.

---

## 7. References

- `eeg/_session_manager.hexa` lines 32-67 — state-machine semantics and falsifier triad
- `eeg/closed_loop.hexa` lines 72-74 — canonical LCG constants (synth substrate mirrors byte-identically)
- `eeg/headplot_helper.hexa` lines 111-131 — 2D ASCII coord source for `channel_set.hexa`
- `state/anima_eeg_impedance_selftest_synth.json` — canonical 10-20 channel-label order
- `Sprint 1 plan` `/home/summer/.claude/plans/hazy-kindling-wind.md` §Part E-1

---

## 8. E-1 follow-up landing record (2026-05-12)

### What landed

| File | Change |
|---|---|
| `eeg/collect.hexa` | `--substrate <brainflow\|synth\|replay>` + `--legacy-inline` flags. Default brainflow keeps 812-line inline BoardShim path byte-identical. synth/replay emit a pointer block (verdict=DEFERRED) and exit 0. |
| `eeg/eeg_recorder.hexa` | Same surgery — `--substrate` + `--legacy-inline`. Segmented recording path unchanged. |
| `eeg/dual_stream.hexa:211` | Comment updated to reference `replay_substrate` as the available wrapper-target. Functional behavior unchanged. |
| `eeg/substrates/{substrate,synth,brainflow,replay,channel_set}_substrate.hexa` | `_flags_only_argv` extended to strip `hexa_interp` argv[0] prefix (host-portability fix). |
| `eeg/collect.hexa` `_flags_only_argv` | Same `hexa_interp` strip. |

### What did NOT land (with rationale)


2. **Full BoardShim → brainflow_substrate delegation in `collect.hexa` / `eeg_recorder.hexa`** — the inline BoardShim loops (`collect.hexa:238-432`, `eeg_recorder.hexa:155-348`) carry hardware-tuned logic (FTDI IOSSDATALAT 1ms ioctl, ring-buffer 450k-sample sizing, chunked `get_current_board_data` polling, drop_ratio detection, retry-on-leak codes). Moving this to `brainflow_substrate` requires a real-hardware regression sweep, which we don't have access to in this session. Phase 2 needs OpenBCI Cyton+Daisy on a Mac with .venv-eeg.

3. **Contract `v0 → v1` promotion** — gated by the two items above. Stays at `v0`.

4. **`eeg/dual_stream.hexa` real `.npy` file-loading wrapper** — replay_substrate now exists as the call-target, but the wrapper (`compare_streams_from_files(anima_npy, eeg_npy)`) needs the same subprocess-delegation primitive that item 1 blocks. Updated the comment to reference replay_substrate; wrapper itself deferred.

### Verification matrix (this PR)

| Case | Result | Notes |
|---|---|---|
| `eeg/collect.hexa --selftest` (default brainflow) | 12/12 PASS | Byte-identical to pre-PR (`hexa_interp` argv fix is additive) |
| `eeg/collect.hexa --selftest --legacy-inline` | 12/12 PASS | Same as default |
| `eeg/collect.hexa --selftest --substrate synth` | exit 0, `verdict=DEFERRED` | Pointer mode — points at `eeg/substrates/synth_substrate.hexa --selftest` |
| `eeg/collect.hexa --selftest --substrate replay` | exit 0, `verdict=DEFERRED` | Pointer mode — points at `eeg/substrates/replay_substrate.hexa --selftest` |
| `eeg/collect.hexa --selftest --substrate bogus` | exit 2, `reason=substrate-invalid` | Argument validation |
| `eeg/collect.hexa --collect --substrate synth ...` | exit 2, `reason=substrate-not-implemented-for-collect` | Phase 2 guard |
| `eeg/substrates/substrate.hexa --selftest` | 6/6 PASS | `F_SUB_PROTO_01..03` |
| `eeg/substrates/synth_substrate.hexa --selftest` | 7/7 PASS | `F_SUB_01_*` |
| `eeg/substrates/replay_substrate.hexa --selftest` | 8/8 PASS | `F_SUB_03_*` |
| `eeg/eeg_recorder.hexa --selftest` (default) | FAIL on this Mac box | **Pre-existing** failure — `.venv-eeg/bin/python` missing in our test environment; unrelated to this PR. The bg-agent verification on ubu-2 (Sprint 1 commit `77484267`) passed because that host had .venv-eeg. |
| `eeg/eeg_recorder.hexa --selftest --substrate synth` | exit 0, `verdict=DEFERRED` | Substrate dispatch actually **adds a working path** here, since pointer mode doesn't need .venv-eeg |
| `bin/hexa-brain license-check --selftest` | 3/3 PASS | Part A firewall regression OK |

---

## 9. Resolved open questions (2026-05-12)

The §6 reviewer-facing open questions are resolved as follows. These decisions
are stamped at contract `v0`; if `v0 → v1` promotion (§5) introduces a
contract-breaking change, the resolution may be revisited.

| # | Question (cf. §6) | Decision | Rationale |
|---|---|---|---|
| 1 | Spec dict `data_rows` declaration — declare expected row count (32 for BrainFlow, 16 for synth/replay) or derive from `api_get_eeg_indices()`? | **(a) eeg_indices slice** — derive `data_rows` from `len(api_get_eeg_indices(sess))`. No explicit `data_rows` field in `spec`. | Avoids redundancy with `eeg_indices`. The 32-row BrainFlow shape is a backend implementation detail and should not leak into the substrate contract; callers slice the data matrix by `eeg_indices`. |
| 2 | `channel_set` vs `electrode_montage` naming | **Keep `channel_set`** | Parity with `BoardShim.get_eeg_channels`. Renaming on `v1` promotion only if a clinical-neuroscience reviewer pushes back. |
| 4 | `api_stim(sess, ch_set, design)` signature vs CL1-style `(channel_set, stim_design_dict)` | **SUPERSEDED 2026-05-12** — widened in same session to `api_stim(sess, stim_spec) → StimResult`. See §10 below. | Initial v0 stamp was "keep triple, refactor on C-2". Re-decided same session: caller count is 0, v0→v1 promotion is gated by Phase 2 BoardShim work anyway, and deferring CL1-shaped signature creates a second breaking change later. Pre-commit the dict shape now while the cost is zero. |
| 5 | (added) `brainflow_substrate` selftest stub-fallback verdict | **PASS as "shim contract OK"** | When the test env lacks `.venv-eeg`/brainflow, `brainflow_substrate --selftest` exercises the substrate-protocol shim layer (method presence, state-machine transitions, last-error shape) without the BrainFlow dep. PASS here means "the shim conforms to the contract"; it does **not** claim hardware-path correctness — that's tested by `eeg/_session_manager.hexa --selftest` on a host with `.venv-eeg`. |

### Cross-reference

These resolutions match the six user-decision items raised at the 2026-05-12
session boundary. Items 4 (eeg_indices slice), 5 (sim time), and 6 (stub
fallback) are E-1; items 1, 2, 3 are B-1 (see `design/core/neuroglancer_precomputed_export_2026_05_12.md` §12).

---

## 10. `api_stim` signature widening (2026-05-12, supersedes §9 row 4)

§9 row 4 initially deferred the CL1-shaped signature to Part C-2. Same-session
re-decision: widen now while caller count is 0. Authoritative shape lives in
`eeg/substrates/substrate.hexa` APPENDIX A; this section is the design rationale.

### 10.1 Effective signature

```python
api_stim(sess, stim_spec) -> StimResult
```

| Surface | Pre-2026-05-12 v0 | Effective 2026-05-12 v0 |
|---|---|---|
| Arity | 3 (`sess, ch_set, design`) | 2 (`sess, stim_spec`) |
| Request shape | unspecified | dict (`stim_spec`) |
| Response shape | unspecified | dict (`StimResult`) |
| Validation helper | none | `validate_stim_spec(spec) → (ok, reason)` |

### 10.2 `stim_spec` (request)

```python
{
  "schema":                 "hexa-brain/substrate/stim/1",
  "channels":               list[int],      # 1-indexed channel_set ids
  "waveform":               "biphasic" | "monophasic" | "sine"
                            | "custom_array",
  "amplitude_uA":           float,
  "frequency_hz":           float,
  "duration_ms":            float,
  "phase_duration_us":      float | None,   # required iff waveform=="biphasic"
  "interpulse_interval_ms": float | None,
  "custom_array":           list[float] | None,  # required iff waveform=="custom_array"
  "license_posture":        LICENSE_POSTURE | None  # same shape as spec.license_posture
}
```

### 10.3 `StimResult` (response)

```python
{
  "ok":              bool,
  "stim_id":         str,             # caller-opaque; uniqueness within session only
  "wall_time_ns":    int,             # wall clock at injection — REQUIRED
  "frames_injected": int,
  "last_err":        {                # shape-identical to api_last_error
    "code":          str,
    "advisory_url":  str | None,
    "retry_action":  str | None
  } | None
}
```

### 10.4 Five completeness deltas vs pre-widening v0

| # | Delta | Why |
|---|---|---|
| 1 | 3-arg triple → 2-arg dict | Pattern-match `api_open_session(spec)`. CL1 SDK HTTP POST body 1:1. |
| 2 | Unspecified result → `StimResult` envelope | Re-uses `api_last_error` shape; gives callers an `if ok:` pattern. |
| 3 | `wall_time_ns` field added | Decision 5 (synth ts = sim time) leaves no wall-clock channel for stim-latency math. `wall_time_ns` is the dedicated channel. Backends MUST capture `time.time_ns()` at injection. |
| 4 | `schema` field added | Enables dispatch when stim/v2 lands later. Forward-compat: schema=None tolerated. |
| 5 | `license_posture` + `stim_id` | AGPL NES backend can be firewall-checked at stim-call time. `stim_id` enables marker/.jsonl ledger correlation (same pattern as `state/license_firewall_checks.jsonl`). |


1. **Breaking change at v0** — Pre-2026-05-12 `api_stim(sess, ch_set, design)` callers would break. Caller count was 0 (all 3 active backends raise `NotImplementedError`; `eeg/_session_manager.hexa:480` also raises). Migration cost: zero.
2. **`wall_time_ns` is unverifiable until C-2** — Until CL1 substrate actually implements `api_stim`, the field exists in the spec but is never written. Falsifier coverage is shape-only (`validate_stim_spec`) until C-2.
3. **`F_SUB_PROTO_04` is the only validation gate** — Shape-only (4 junk shapes rejected, 1 canonical accepted). Semantic validation (e.g., physiologically plausible amplitude ranges, channel-set membership) is deferred to per-backend.
4. **Three-backend ripple** — `synth_substrate.hexa`, `brainflow_substrate.hexa`, `replay_substrate.hexa`, plus `_session_manager.hexa:480`, all updated to `(sess, stim_spec)`. Body is unchanged (`raise NotImplementedError`); no behavior change. `cmd_selftest` byte-identical gate in `_session_manager` is unaffected — `F_SM_01/02/03` PASS conditions stand.

### 10.6 Verification matrix

| Falsifier | Status | Notes |
|---|---|---|
| `F_SUB_PROTO_02` | call-arg updated `(None, None)` | shape: arity-2 raise |
| `F_SUB_PROTO_04` | **new** | `validate_stim_spec` accept canonical + reject 4 junk shapes |
| `F_SUB_01_stim_raises` (synth) | call-arg updated `(s4, None)` | unchanged semantic |
| `F_SUB_02_stim_raises` (brainflow) | call-arg updated `(s1, None)` | unchanged semantic |
| `F_SUB_03_close_stim` (replay) | call-arg updated `(sess, None)` | unchanged semantic |
| `F_SM_01/02/03` (_session_manager) | **unaffected** | `cmd_selftest` byte-identical, `api_stim` def is outside |

Execution on this Mac box deferred — TCP compute backend (`127.0.0.1:5555`) is not running in this session. User-side runbook:

```bash
# Start TCP server (ubu host or local), then on Mac:
hexa run eeg/substrates/substrate.hexa --selftest          # F_SUB_PROTO_01..04 PASS
hexa run eeg/substrates/synth_substrate.hexa --selftest    # F_SUB_01_* PASS
hexa run eeg/substrates/brainflow_substrate.hexa --selftest # F_SUB_02_* PASS (shim contract)
hexa run eeg/substrates/replay_substrate.hexa --selftest   # F_SUB_03_* PASS
```

---

## 11. `import py` migration — retiring the heredoc anti-pattern (Phase 2 root fix)

### 11.1 The actual problem (resource/tcp layer, NOT hexa-lang)

`resource/tcp/exec_workers.py:_run_ephemeral` writes the job payload to
`tempfile.TemporaryDirectory(prefix="resource-tcp-")` and runs the subprocess
with `cwd=tmpdir`. So `hexa run job.hexa` executes with cwd `/tmp/resource-tcp-XXXX`;
a nested `hexa run eeg/substrates/X.hexa` then resolves the relative path against
`/tmp/resource-tcp-XXXX/eeg/...` — which doesn't exist → empty stdout. This is
the §10.5 / SESSION_LOG §10.4 deferral root cause for Phase 2 BoardShim delegation.

hexa-lang already has the "cut cwd dependence, resolve via env" pattern landed:
`hexa cc` resolves SSOT modules via `$HEXA_LANG > install_dir > ./self` **(not cwd)**
(SPEC.md line 789), and RFC-016 P2 added `$HEXA_PATH` module search. The fix uses
those, not a new mechanism.

### 11.2 Three fixes (shallow → deep)

| Fix | Layer | Effort | Effect |
|---|---|---|---|
| A — `HEXA_PROJECT_ROOT` env export | `resource/tcp/exec_workers.py` (`hexa_script_worker` already injects `HEXA_RESOLVER_NO_REROUTE` etc. — add one more) | ~1 line | Immediate Phase 2 unblock; nested-run still happens but resolves correctly. |
| B — `import <hexa>` flattening | hexa-lang (RFC-016 P1/P2, **already landed**) | leverage only | `collect.hexa` does `import eeg/substrates/brainflow_substrate as bf` — `module_loader` flattens at **compile time**; no subprocess at runtime. `HEXA_PATH` needs the project root. |
| C — `import py` (embedded CPython) | hexa-lang (RFC-016 P4 `import py` + `stdlib/python_ffi.hexa`, **already landed**) | substrate-backend rewrite | substrate backends call BoardShim **in-process** via `py_call(...)` — no `/tmp/*.py` heredoc, no subprocess, no nested run. |

**Chosen direction: B + C** — the deep fix. When B+C land, the §10.5 deferral
reasons (subprocess sandbox) are *eliminated at the source*, not worked around.
This also retires the RFC-016 §1.4 anti-pattern (".hexa file carrying a Python
heredoc, stringified + subprocess-executed") that hexa-brain shares with
hexa-bio `_python_bridge/module/*.py`, the anima staging copy, and
`stdlib/anima_audio_worker.hexa`.

### 11.3 Staged plan

| Phase | Scope | Status | Verification |
|---|---|---|---|
| **2b** | `eeg/substrates/_brainflow_helper.py` — hand-maintained Python superseding the `parts.push("...")` heredoc in `brainflow_substrate.hexa`. Two surfaces: (1) embedded-CPython json-in/out wrappers (`open_session`, `read_chunk`, … — session objects live in a module `_SESSIONS` registry keyed by opaque `bf-<hex12>` strings, since they can't cross `py_call(module,fn,str)→str`); (2) standalone CLI (`python3 _brainflow_helper.py selftest`). | **DONE 2026-05-12** | `python3 eeg/substrates/_brainflow_helper.py selftest` → 4/4 PASS (`F_SUB_02_shape/stim_raises/idempotent/json_surface`) + `inspect` OK. Verified on this Mac box (pure stdlib python, no TCP/hardware needed). |
| **2b-2** | `eeg/_session_manager_helper.py` — hand-maintained Python superseding the `parts.push("...")` heredoc in `eeg/_session_manager.hexa`, **byte-identical-preserving** (`cmd_selftest` output character-for-character identical, legacy `anima-eeg/` schema + advisory URLs + `__EEG_SESSION_MGR__` sentinel kept verbatim). `_brainflow_helper.py`'s `_try_load_session_manager()` now resolves `eeg/_session_manager_helper.py` via `__file__` (cwd-independent — sandbox-safe) ahead of the legacy `/tmp/anima_eeg_session_manager_helper.py`. | **DONE 2026-05-13** | `python3 eeg/_session_manager_helper.py selftest` → all PASS (`F_SM_01/02/03` + `T_REC_01` + `T_ERR_01`, `verdict=PASS`, sentinel emitted) + `inspect` OK. `_brainflow_helper.py selftest` re-run → `session_manager_helper_present=True`, 4/4 PASS. cwd-from-`/tmp` test confirms `__file__`-based resolution. **Still TODO**: rewrite `eeg/_session_manager.hexa` itself to ship the `.py` instead of emitting it (needs `hexa run` ≡ TCP backend to byte-diff). |
| **2c** | `eeg/substrates/brainflow_substrate.hexa` v2 — delete the heredoc; `use "stdlib/python_ffi"`; each `api_*` hexa fn delegates: `py_init()` once; `py_eval("import sys; sys.path.insert(0, <eeg/substrates dir>)")`; `py_eval("import _brainflow_helper")`; `api_open_session(spec) → string` returns `py_call("_brainflow_helper", "open_session", json_encode(spec))` (the json `{session_id,…}`); `api_read_chunk` etc. take the `session_id` string and call the matching wrapper. The `<eeg/substrates dir>` is the open question — resolve via `HEXA_PATH` (B) or a `__file__`-equivalent; do NOT use cwd. | ⏸ Real OpenBCI Cyton+Daisy only (numpy data-path regression); `libhxpyembed.dylib` build cleared 2026-05-13 (§11.8). | `hexa run eeg/substrates/brainflow_substrate.hexa --selftest` ≡ 2b CLI output. |
| **2d** | `eeg/collect.hexa` / `eeg/eeg_recorder.hexa` — replace the inline BoardShim loop AND the `--substrate` pointer-mode `hexa run eeg/substrates/X.hexa` with `import eeg/substrates/brainflow_substrate as bf` + `bf.api_open_session(spec)`. `module_loader` flattens at compile time → no nested run → sandbox-irrelevant. `--legacy-inline` keeps the old path for one release. | TODO | byte-identical regression gate: `collect --selftest --legacy-inline` ≡ pre-2d `collect --selftest`. Real OpenBCI Cyton+Daisy regression for the data path. |
| **2e** | `synth_substrate.hexa` / `replay_substrate.hexa` — already hexa-native (no Python); just adopt the `import <hexa>` consumer side from `collect`/`recorder`. Minimal change. | TODO | existing `F_SUB_01_*` / `F_SUB_03_*` selftests unchanged. |
| **2f** | Contract `v0 → v1` promotion — gated on 2b-2 + 2c + 2d landing + the real-hardware regression sweep. `bin/hexa-brain license-check` re-verifies `registry.yaml` conformance. | TODO | `F_SM` + `F_SUB_*` + license-check all green on a host with `.venv-eeg` + OpenBCI. |

### 11.4 `_brainflow_helper.py` interface (2b — landed)

embedded-CPython surface (each `<json>` is a string; return is a json string):

| `py_call` target | arg json | return json |
|---|---|---|
| `open_session` | `{backend, board_id, port, synthetic, channel_set:{...}}` | `{session_id:"bf-…", state, board_id, synthetic}` |
| `close_session` | `{session_id}` | `{session_id, has_halted:true}` |
| `reinit` | `{session_id}` | `{old_session_id, session_id, state}` |
| `start_recording` | `{session_id, name, fmt, max_min}` | `{recording_id:"rec-…", state}` |
| `stop_recording` | `{recording_id}` | `{recording_id, is_open:false}` |
| `read_chunk` | `{session_id, n_max}` | `{data:[[…],…], ts}` |
| `get_eeg_indices` | `{session_id}` | `[1,2,…]` |
| `get_sample_rate` | `{session_id}` | `125` |
| `stim` | `{session_id, …stim_spec}` | `{ok:false, stim_id:"", wall_time_ns, frames_injected:0, last_err:{code:"stim-not-implemented",…}}` (always — scalp EEG read-only) |
| `last_error` | `{session_id}` | `{code, advisory_url, retry_action}` |

1. **numpy → nested list** — `read_chunk` returns the BoardShim ndarray as nested Python lists in json (V1 string-only). A V2 zero-copy path via `stdlib/python_ffi.py_buffer_to_hexa` (PEP 3118 buffer protocol) is deferred; for now the json round-trip is the cost of the simple contract.
2. **`_session_manager` loaded via `__file__`-resolved path (Phase 2b-2)** — `_brainflow_helper.py` now resolves `eeg/_session_manager_helper.py` via `os.path.dirname(__file__)`, falling back to the legacy `/tmp/anima_eeg_session_manager_helper.py` emit-copy. The Python-side `<eeg dir>` question is answered: `__file__`.
3. **`<eeg/substrates dir>` resolution in 2c — Python side solved, hexa side open** — Python's `__file__` (used in 2b-2) is the answer for `_brainflow_helper.py`. The hexa side still needs to know its own directory to do `py_eval("sys.path.insert(0, <dir>)")`; `argv[0]` is the candidate but under the resource/tcp sandbox it's `/tmp/resource-tcp-*/job.hexa` (a copy), so it must come from `HEXA_PATH` / `HEXA_PROJECT_ROOT` env (Fix A) or hexa-lang growing a `__file__`-equivalent.

### 11.6 Verification-infrastructure blocker (2026-05-13)

`hexa run X.hexa` cannot execute on this Mac box:
- `hexa.real` unconditionally re-routes to `resource/tcp/run_remote.py hexa X.hexa` → TCP `127.0.0.1:5555`. The reroute-disabling envs (`HEXA_RESOLVER_NO_REROUTE`, `HEXA_SHIM_NO_DARWIN_LANDING`, `HEXA_NO_REMOTE`) do **not** take effect — `hexa.real` ignores them.
- With the TCP server up: `hexa_script_worker` writes the payload to `/tmp/resource-tcp-*/job.hexa` and runs `hexa run /tmp/.../job.hexa` — which re-routes to `run_remote.py` → TCP again → another `hexa_script_worker` → another `hexa run` → **infinite recursion** (queue depth grows; processes pile up).
- With the TCP server down: `ConnectionRefused`.

So `hexa run` selftests (`F_SUB_PROTO_*`, `F_SUB_0{1,2,3}_*`, `F_SM_*`, the `api_stim` widening, the B-1/E-1 decision checks) and Phases **2b-3 / 2c / 2d / 2e / 2f** are all blocked here.

**ubu-2 was tried (2026-05-13) and is also blocked**: ubu-2's `~/.hx/bin/hexa.real` is a symlink to `/Users/ghost/core/hexa-lang/hexa.real` (the Mac arm64 binary, reachable via the `mac_home` mount). On Linux ubu-2 that binary fails with `Exec format error` — there is no native Linux hexa build on ubu-2 (no `~/core/hexa-lang` clone; `~/.hx/` is itself the Mac mount). So `hexa run` is unavailable there too.

Remaining paths to a `hexa run` verification surface:
- **a fix in hexa-lang's `hexa.real` shim / `resource/tcp/exec_workers.py`** so the nested `hexa run` inside `hexa_script_worker` does not re-route into the TCP recursion (i.e. `HEXA_RESOLVER_NO_REROUTE=1` actually suppresses the `run_remote.py` hop). Same family as §11.2 Fix A. This is the only path that fixes it on the Mac box. **OR**
- **install a native Linux hexa build on ubu-2** (build `hexa-lang/compiler/` ground-up-native on Linux, or fetch a Linux release binary) — then ubu-2 can run the selftest matrix directly without the Mac-binary mount.

Phases 2b + 2b-2 sidestep this entirely — `_brainflow_helper.py` and `_session_manager_helper.py` are pure-stdlib Python, runnable directly with `python3` (no `hexa run`, no TCP). **Cross-platform verified 2026-05-13**: both `selftest`s pass on macOS arm64 (this box) AND on Linux ubu-2 (`python3 eeg/substrates/_brainflow_helper.py selftest` → 4/4 PASS; `python3 eeg/_session_manager_helper.py selftest` → all PASS + sentinel).

### 11.7 Upstream fix landed (2026-05-13) — `hexa run` verification surface restored

**Fix shape** (in `~/core/resource/tcp/exec_workers.py`, separate repo — not hexa-brain):
- New `_resolve_hexa_interp_argv0()`: resolves `~/.hx/packages/hexa/build/hexa_interp.real`, exposes it via a `$TMPDIR/hexa_interp` symlink (no `.real` suffix). Reason: `.hexa` scripts' `_flags_only_argv()` strips argv[0] when it ends in `.hexa`, `/exe`, or `hexa_interp` — calling the real binary directly produced argv[0] ending in `hexa_interp.real`, so the script saw it as a positional arg → `unknown-arg`. The symlink fixes argv[0] without touching the .hexa scripts.
- `hexa_script_worker` now uses `argv_prefix=[<symlink>]` (direct interp call) + `env_extra` adds `RESOURCE_LOCAL_HEXA=1` (defangs the `hexa-lang/build/hexa_interp` shim's `RESOURCE_R ubu-1 run …` offload, should anything still reach it). The old `[hexa, "run"]` path was the recursion source: `hexa run` → `hexa.real run` → `run_remote.py` → TCP → server's `hexa_script_worker` → another `hexa run` → ∞.

**Companion fix (hexa-brain side)**: `eeg/_session_manager.hexa` `_flags_only_argv()` extended with the `hexa_interp` strip pattern that was already in collect/recorder + 5 substrate files (commit `76494ad3`). Without this `_session_manager.hexa --selftest` errored with the symlink-path as an unknown arg; the strip pattern itself is what the upstream symlink choice targets, so this is a one-line completion (no `cmd_selftest` change → `F_SM_01/02/03` byte-identical gate intact).

**Verification matrix (2026-05-13, all `hexa run` via patched worker, on this Mac box, no hardware)**:

| Target | Result |
|---|---|
| `hexa run eeg/substrates/substrate.hexa --selftest` | 7/7 PASS (`F_SUB_PROTO_01..04`) |
| `hexa run eeg/substrates/synth_substrate.hexa --selftest` | 7/7 PASS (`F_SUB_01_shape/deterministic/idempotent/stim_raises`) |
| `hexa run eeg/substrates/brainflow_substrate.hexa --selftest` | 6/6 PASS (`F_SUB_02_shape/stim_raises/idempotent`) |
| `hexa run eeg/substrates/replay_substrate.hexa --selftest` | 8/8 PASS (`F_SUB_03_shape/roundtrip/eof/close_stim/missing_path`) |
| `hexa run eeg/_session_manager.hexa --selftest` | 9/9 PASS (`F_SM_01/02/03 + T_REC_01 + T_ERR_01`, sentinel `__EEG_SESSION_MGR__ PASS HALTED` emitted) |
| `hexa run eeg/collect.hexa --selftest` | 12/12 PASS — **byte-identical gate intact** (api_stim widening at `_session_manager.hexa:480` did not perturb `cmd_selftest` output) |
| recursion check (`run_remote` / `hexa.real run` / `hexa_interp` procs) | 0 after each run |

So the §10 `api_stim` widening (`(sess, stim_spec) → StimResult`), Phase 2b/2b-2 (`_brainflow_helper.py`, `_session_manager_helper.py`), and the six §9 + §12 decisions are now **all hexa-run-verified** in addition to their earlier pure-python verification. Phases 2b-3 / 2c / 2d / 2e / 2f remaining blockers narrow to:
- 2c: ~~`libhxpyembed.dylib`~~ ✅ cleared 2026-05-13 (§11.8) + real OpenBCI for the numpy data path
- 2d: real OpenBCI for the BoardShim regression sweep
- 2b-3: nothing new — `hexa run` byte-diff is now available; ready to proceed

### 11.8 `libhxpyembed.dylib` build cleared (2026-05-13)

`cmake -S lib/hxpyembed -B lib/hxpyembed/build && cmake --build lib/hxpyembed/build` from `/Users/ghost/core/hexa-lang/`:

```
[ 25%] Building C object CMakeFiles/hxpyembed.dir/hxpyembed.c.o
[ 50%] Linking C shared library libhxpyembed.dylib
[ 50%] Built target hxpyembed
[ 75%] Building C object CMakeFiles/hxpyembed_smoke.dir/smoke.c.o
[100%] Linking C executable hxpyembed_smoke
```

Result: `/Users/ghost/core/hexa-lang/lib/hxpyembed/build/libhxpyembed.dylib` 35584 bytes, linked against Python 3.14 (Homebrew `python@3.14`, framework lib `-lpython3.14 -ldl -framework CoreFoundation`), AppleClang 21.

**PoC `import py` integration**: `hexa run /Users/ghost/core/hexa-lang/bench/import_py_e2e.hexa` →
```
py-repr
exit=0
```
The bench uses `use "stdlib/python_ffi"` + `import py "builtins" as bi; let r = bi.repr("hello"); println("py-repr " + r)`. exit 0 + recursion-free (procs 0 after cleanup) confirms the full chain works: hexa source → `py_call("builtins", "repr", "hello")` → `hxpy_call_str` (in `libhxpyembed.dylib`) → embedded CPython interp → string round-trip back to hexa.


