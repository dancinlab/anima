// anima-eeg-core module API spec

# anima-eeg-core — per-module API specification

This file documents the exact signature, inputs, outputs, side-effects, and
dependencies of every module in `anima-eeg-core/`. Signatures use hexa-flavoured
pseudo-syntax; actual implementations may use the runtime's `list` / `array`
types where called out in the architecture doc §2 axis A3.

## Conventions

- All paths are workspace-relative unless noted.
- All ×1000 fixed-point values use the same convention as the legacy tools
  (`*_x1000` suffix in JSON output).
- All modules export at most one public function plus their constants. The
- Every public function returns either a typed result struct (a `list` whose
  positional slots are documented) or an `int` exit code.
- Side-effects are listed under "Side-effects". Pure-data modules have none.

---

## _core/

### `_core/argv_normalize.hexa`

```
fn flags_only_argv() -> list[string]
```

Strips interpreter / script / AOT-cache prefixes (`hexa_interp`, `*.hexa`,
`/exe`) and returns the user-facing flag list. Mirrors P1.

- **Inputs:** none (reads `argv()`).
- **Outputs:** `list[string]` of the user's flags.
- **Side-effects:** none.
- **Depends on:** none.

### `_core/trailer.hexa`

```
fn emit_trailer(reason_slug: string, reason_detail: string, fix: string) -> ()
```

```
reason: <slug>: <detail>
fix: <fix>
```

- **Inputs:** three strings.
- **Outputs:** none.
- **Side-effects:** stderr write.
- **Depends on:** none.

### `_core/clock.hexa`

```
fn now_iso() -> string             # "2026-04-28T12:34:56Z"
fn now_date_utc() -> string        # "2026-04-28"
fn now_epoch_seconds() -> int      # int unix seconds
```

- **Inputs:** none.
- **Outputs:** strings or int.
- **Side-effects:** runs `date -u …` via `exec`.
- **Depends on:** none.

### `_core/manifest.hexa`

```
fn sha256_of_file(path: string) -> string         # hex; "" if path empty; "unavailable" if shasum missing
fn sha256_of_str(content: string) -> string       # hex; via shell heredoc
fn segment_id(prefix: string, ts: string) -> string  # FNV-32 short id
```

- **Inputs:** path or content.
- **Outputs:** hex string.
- **Side-effects:** runs `shasum -a 256` via `exec`.
- **Depends on:** clock.

### `_core/citations.hexa`

```
fn citation(key: string) -> string                # full citation block
fn citation_short(key: string) -> string          # one-line form
fn known_keys() -> list[string]                   # bibliography enumeration
```

Bibliography keys (initial seed):
- `kaspar_schuster_1987`, `lempel_ziv_1976`, `bandt_pompe_2002`,
  `costa_2002`, `olofsen_2008`, `hjorth_1970`, `oh_2014`, `berger_1929`,
  `welch_1967`, `schartner_2015`, `schartner_2017`, `bodizs_2024`,
  `pope_1995`, `pollock_1990`, `klimesch_1999`, `davidson_1992`,
  `pan_tompkins_1985`, `task_force_hrv_1996`, `thayer_2009`, `mccraty_2014`,
  `iber_2007_aasm`, `walker_2017`, `plews_2013`, `hjortskov_2004`,
  `berry_2015`, `salvucci_2000`, `soukupova_2016`, `stern_1994`.

- **Inputs:** lookup key.
- **Outputs:** citation string.
- **Side-effects:** none.
- **Depends on:** none.

### `_core/python_selector.hexa`

```
fn pick_python(env_aliases: list[string]) -> string
```

Resolves the Python interpreter using a fixed priority chain:
1. Each alias in `env_aliases` (e.g. `["CLM_EEG_LZ76_PYTHON", "ANIMA_EEG_VENV_PYTHON"]`).
2. Workspace-relative `.venv-eeg/bin/python`.
3. `<cwd>/.venv-eeg/bin/python` (absolute form).
4. `/opt/homebrew/bin/python3`.
5. `/usr/bin/python3`.

- **Inputs:** alias list.
- **Outputs:** path string.
- **Side-effects:** runs `test -x` probes via `exec`.
- **Depends on:** none.

### `_core/python_helper.hexa`

```
type HelperResult = list[any]   # [stdout: string, rc: int, kv_blob: string?]

fn emit_helper(helper_path: string, source: string) -> ()
fn run_helper(helper_path: string, dump_path: string, py: string,
              args: list[string]) -> HelperResult
fn parse_int_kv(blob: string, key: string) -> int        # P5 kv parser
fn parse_str_kv(blob: string, key: string) -> string
```

`emit_helper` writes `source` to `helper_path` (workspace-state preferred for
sandboxed callers). `run_helper` invokes
`<py> <helper_path> <args...>` with `exec_with_status` and reads the kv
output from `dump_path`. Mirrors P5 across lz76 / pe / hjorth / berger.

- **Inputs:** paths + source + py interpreter + arg list.
- **Outputs:** `HelperResult` = [stdout, rc, kv_blob].
- **Side-effects:** writes helper, executes shell, reads dump.
- **Depends on:** python_selector + trailer.

### `_core/npy_loader.hexa`

```
type NpyData = list[any]   # [n_ch: int, n_samp: int, samples: list[int]]

fn load_npy(npy_path: string, py: string) -> NpyData
```

Wraps a transient helper that reads a 16ch × N (or BrainFlow 32-row) .npy,
scales floats by 1e6, returns flat channel-major ints. Mirrors P6.

- **Inputs:** .npy path, python interpreter.
- **Outputs:** NpyData.
- **Side-effects:** writes helper, reads dump.
- **Depends on:** python_helper.

### `_core/json_eeg_parser.hexa`

```
fn parse_raw_arrays(blob: string) -> list[any]    # [n_ch, n_samp, samples...]
```

Pure-hexa parser for the `an11_b_eeg_ingest` schema (`anima/eeg_recording/1`).
Mirrors P7. Same sentinel layout as `npy_loader.NpyData`.

- **Inputs:** JSON blob string.
- **Outputs:** flat sentinel list.
- **Side-effects:** none.
- **Depends on:** none.

### `_core/jsonl_audit.hexa`

```
fn append_jsonl(path: string, line: string) -> ()
fn read_jsonl(path: string) -> list[string]
fn ensure_dir(path: string) -> ()                # mkdir -p $(dirname path)
```

file + `cat >>` to bypass hexa's /tmp sandbox.

- **Inputs:** path + line.
- **Outputs:** none / list[string].
- **Side-effects:** writes scratch, appends to path.
- **Depends on:** clock.

### `_core/falsifier_runner.hexa`

```
type Verdict = list[any]   # [tier: string, c1_pass: int, c2_pass: int, ...,
                           #  classification: string, abs_delta_x1000: int]

fn evaluate_criteria(values: list[int], thresholds: list[int],
                     rules: list[string]) -> Verdict
```

Generic 3-tier (PASS / PARTIAL / FAIL) verdict computation from frozen
criteria. Refuses to emit a verdict if `len(rules) < 3` or if any `value` is
sentinel `-2147483647`. Mirrors P11.

- **Inputs:** measured values, threshold ints, rule strings.
- **Outputs:** Verdict.
- **Side-effects:** none.
- **Depends on:** citations.

### `_core/cert_emitter.hexa`

```
type CertSpec = list[any]   # [tool, version, raw_rank, hypothesis,
                            #  criteria, mode, run_block, classification, ...]

fn emit_cert(out_path: string, spec: CertSpec) -> ()
fn emit_jsonl_row(audit_path: string, spec: CertSpec) -> ()
```

guard: refuses to set `classification == "REAL_HW_PASS"` unless
`spec.mode == "real" && spec.input_sha256 != ""`. Mirrors P12.

- **Inputs:** output path + cert spec.
- **Outputs:** none.
- **Side-effects:** writes JSON cert + appends JSONL.
- **Depends on:** clock + manifest + jsonl_audit + falsifier_runner.

### `_core/chflags_lock.hexa`

```
fn unlock(path: string) -> int     # nouchg + return prior state
fn lock(path: string) -> int       # uchg
fn locked_write(path: string, content: string) -> int   # nouchg → write → uchg
```

that emit ledger files marked immutable after rotation.

- **Inputs:** path (+ content for locked_write).
- **Outputs:** rc int.
- **Side-effects:** runs `chflags`; writes file.
- **Depends on:** trailer.

### `_core/board_config.hexa`

```
type BoardSpec = list[any]   # [name, board_id, expected_channel_count,
                             #  expected_data_rows, sample_rate_hz]

fn default_board() -> BoardSpec
fn resolve_board(name: string) -> BoardSpec
fn last_board_used() -> BoardSpec  # reads recordings/sessions/last_board.json
```

SSOT for board defaults (axis A7).

- **Inputs:** optional board name.
- **Outputs:** BoardSpec.
- **Side-effects:** reads ledger.
- **Depends on:** none.

### `_core/cli_parser.hexa`

```
type ParsedCli = list[any]   # [input_path: string, out_path: string,
                             #  audit_path: string, selftest: int,
                             #  selftest_mode: string, want_help: int, extra: list]

fn parse_cli(av: list[string], schema: string) -> ParsedCli
```

Parses the canonical `--selftest / --input / --out / --audit-jsonl / --help /
--selftest-mode <kind>` flag set, plus a free-form `extra` list for
module-specific flags. Mirrors P2.

- **Inputs:** flag list + schema string (for error messages).
- **Outputs:** ParsedCli.
- **Side-effects:** stderr trailer on parse error.
- **Depends on:** argv_normalize + trailer.

---

## _gates/

Every gate has the same shape:

```
type GateResult = list[any]   # [pass: int, classification: string,
                              #  measured_value: int, threshold: int]

fn run_gate(input_path: string, audit_path: string, out_path: string) -> int
fn evaluate_gate(samples: list[int], n_ch: int, n_samp: int) -> GateResult
```

`run_gate` is the verb-callable form (used by `eeg_core gate <name>`).
`evaluate_gate` is the reusable kernel (called by pipeline recipes).

- **Depends on:** _core/* (npy_loader, falsifier_runner, cert_emitter).

| Gate | Threshold | Reference |
|------|-----------|-----------|
| `berger_alpha` | alpha > beta on O1∧O2; peak ∈ [7,14] Hz | berger_1929, welch_1967 |
| `rms_band` | rms ∈ [2 µV, 200 µV] on ≥14 of 16 ch | board health proxy |
| `pe_saturation` | PE_scale1 ≤ 0.95 | bandt_pompe_2002 |
| `hjorth_band` | Complexity ∈ [1.0, 2.0] | hjorth_1970 |

---

## _metrics/

Every metric has the same shape:

```
type MetricResult = list[any]   # [primary_value_x1000: int, ...,
                                #  per_channel_x1000: list[int]]

fn compute_metric(samples: list[int], n_ch: int, n_samp: int,
                  fs_hz: int) -> MetricResult
fn run_metric(input_path: string, audit_path: string, out_path: string) -> int
```

`run_metric` is the verb-callable form (used by `eeg_core metric <name>`).
`compute_metric` is the closed-form kernel (called by pipelines and gates).

- **Depends on:** _core/* (npy_loader, falsifier_runner, cert_emitter,
  python_helper for Welch-PSD-based metrics).

| Metric | Inputs | Output | Reference |
|--------|--------|--------|-----------|
| `lz76` | samples, n_ch, n_samp | b(n)_x1000, c_n | kaspar_schuster_1987 |
| `permutation_entropy` | samples, n_ch, n_samp | PE_mean_x1000, per-scale | bandt_pompe_2002, costa_2002 |
| `hjorth` | samples, n_ch, n_samp | Activity/Mobility/Complexity_x1000 | hjorth_1970 |
| `gamma_theta` | samples, n_ch, n_samp, fs_hz | ratio_x1000 (own 3 σ/τ=3) | welch_1967 |
| `alpha_coherence` | samples, n_ch, n_samp, fs_hz, ch_pairs | coh_x1000 per pair | welch_1967 |
| `alpha_phase_plv` | samples, n_ch, n_samp, fs_hz, ch_pairs | PLV_x1000 per pair | NEW |
| `dmn_coherence` | samples, n_ch, n_samp, fs_hz | dmn_coh_x1000 | NEW (RSN split) |
| `frontal_asymmetry` | samples, n_ch, n_samp, fs_hz | fa_x1000 (signed) | davidson_1992 |
| `spectral_entropy` | samples, n_ch, n_samp, fs_hz | sh_entropy_x1000 | welch_1967 |
| `change_points` | b_n_series: list[int] | cp_indices: list[int] | PELT |

---

## _paradigms/

```
type RecordingSpec = list[any]   # [task: string, duration_sec: int,
                                 #  segment_sec: int, board: BoardSpec,
                                 #  output_dir: string]

fn record_paradigm(spec: RecordingSpec) -> int
```

- **Depends on:** _core/* + _hw/calibrate (impedance pre-flight).

| Paradigm | Default duration | Output |
|----------|------------------|--------|
| `resting` | 300 s | `recordings/sessions/resting_<ts>_<seg>.npy` |
| `daily_life` | rolling | `recordings/daily/<date>_axes.jsonl` |
| `visual_p300` | 600 s | `recordings/p300/<ts>_visual.npy` + stim ledger |
| `auditory_p300` | 600 s | `recordings/p300/<ts>_audio.npy` + stim ledger |
| `pre_post` | 2× 300 s | `recordings/pre_post/<ts>_{pre,post}.npy` |
| `longitudinal` | scheduled | `recordings/longitudinal/<date>_<task>.npy` |
| `long_duration` | 3600-7200 s | `recordings/long/<ts>_<dur>min.npy` |
| `sleep` | 28800 s | `recordings/sleep/<date>_overnight.npy` |

---

## _hw/

```
fn run_hw_action(action: string, board: BoardSpec, port: string) -> int
```

| Action | Reads from | Effects |
|--------|-----------|---------|
| `board_health` | BrainFlow stream 3-5 s | exit 0 = HEALTHY |
| `calibrate` | BrainFlow stream 5 s + impedance | exit 0 = ALL_PASS |
| `impedance` | BrainFlow get_imp | per-ch 5-state ASCII view |
| `impedance_validate` | impedance + worn-helmet ledger | JSONL evidence row |
| `electrode_adjust` | BrainFlow live | TUI event loop |

- **Depends on:** _core/python_selector + _core/python_helper +
  _core/board_config.

---

## _integrations/

```
type IntegrationSpec = list[any]   # [source: string, in_path: string,
                                   #  out_path: string, mode: string]

fn run_integration(spec: IntegrationSpec) -> int
```

| Source | Hypothesis | Output |
|--------|-----------|--------|
| `claude_cli` | r ≥ 0.30 between EEG axes and CLI msg pairs | `state/eeg_claude_cli_audit/<date>_session.jsonl` |
| `claude_cli_long` | longitudinal r ≥ 0.20 across N≥10 sessions | `state/eeg_claude_cli_long_audit/<date>_long.jsonl` |
| `behavioral` | r ≥ 0.30 EEG ↔ self-reported labels | `state/behavioral_eeg_audit/<date>_behav.jsonl` |
| `webcam` | I1-I7 privacy + 5 metrics @ 30 Hz → 1-min rows | `state/eye_tracker_audit/<date>_gaze.jsonl` |
| `wearable` | apple/oura/whoop ↔ EEG axes | `state/wearable_eeg_audit/<date>_wearable.jsonl` |
| `cardiac` | HRV ↔ alpha attenuation r ≥ 0.20 | `state/cardiac_eeg_audit/<date>_cardiac.jsonl` |
| `mobile` | mobile-EEG↔stationary-EEG concordance | `state/mobile_eeg_audit/<date>_mobile.jsonl` |

- **Depends on:** _core/* + select _metrics/ (e.g. cardiac uses gamma_theta,
  webcam uses alpha_phase_plv).

---

## _ml/

```
fn run_ml(model: string, mode: string, input_path: string,
          model_path: string, audit_path: string) -> int
```

| Model | mode | Effect |
|-------|------|--------|
| `anomaly_autoencoder` | `train` | learn 80→8→80 AE, save weights |
| `anomaly_autoencoder` | `infer` | per-segment z-score |
| `token_cyborg`         | `encode` | 200-char hex from 16-ch .npy |

- **Depends on:** _core/python_helper (numpy autoencoder) +
  _metrics/spectral_entropy (feature extraction).

---

## _ui/

```
fn render_ui(view: string, input_path: string) -> int
```

| View | Source | Output |
|------|--------|--------|
| `headplot` | impedance JSON | ASCII 10-20 head plot |
| `full_helmet` | live BrainFlow | 16ch concurrent 5-state grid |

- **Depends on:** _core/* + _hw/impedance.

---

## eeg_core.hexa (root dispatcher)

```
fn main() {
    let av = _core/argv_normalize.flags_only_argv()
    let verb = av[0]
    let noun = av[1]
    let rest = av[2..]
    match (verb) {
        "gate"      -> dispatch_gate(noun, rest)
        "metric"    -> dispatch_metric(noun, rest)
        "pipeline"  -> dispatch_pipeline(noun, rest)
        "record"    -> dispatch_paradigm(noun, rest)
        "hardware"  -> dispatch_hw(noun, rest)
        "integrate" -> dispatch_integration(noun, rest)
        "ml"        -> dispatch_ml(noun, rest)
        "ui"        -> dispatch_ui(noun, rest)
        "list"      -> print_inventory(rest)
        "selftest"  -> run_all_selftest(rest)
        "help"      -> print_usage()
        _           -> { _core/trailer.emit_trailer("unknown-verb", verb,
                         "1) eeg_core help  2) eeg_core list"); exit(2) }
    }
}
```

The 8 dispatch functions each:
1. Validate `noun` against the static module table for that category.
2. Resolve the module path (e.g. `_metrics/lz76.hexa`).
3. Forward `rest` to the module's main entry point.
4. Map the module's typed verdict to an exit code per A5 mitigation.

— end module API spec.
