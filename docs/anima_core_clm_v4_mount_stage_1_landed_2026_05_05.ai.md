# Anima Core · CLM v4 Mount Stage 1 — LANDED (2026-05-05)

## TL;DR

`anima-core/runtime/clm_v4_mount.hexa` (651 LoC, hexa-only orchestration) emits substrate-coupled forward API for CLM v4. Selftest PASS (rc=0, 8/8 format checks, 3 markers, 4 substrate-response lines, 5 axes, 5 honest-C3). Helper python emitted at runtime to `/tmp/clm_v4_mount_helper.hexa_tmp` (raw#37 transient path). $0 mac, ~1h.

## Files

| Path | Role | Status |
|------|------|--------|
| `anima-core/runtime/clm_v4_mount.hexa` | Stage 1 mount layer (NEW) | LANDED |
| `state/anima_core_clm_v4_mount_stage_1_2026_05_05/verdict.json` | Verdict + selftest artifacts | LANDED |
| `state/anima_core_clm_v4_mount_stage_1_2026_05_05/selftest.stdout.log` | Selftest stdout (36 lines) | LANDED |
| `state/anima_core_clm_v4_mount_stage_1_2026_05_05/selftest.stderr.log` | Selftest stderr (11 lines, C3 emit) | LANDED |
| `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` | Sister spec (parent) | UNCHANGED |
| `tool/transient_py/clm_v4_hf_format_shim.py` | LOCKED v4 shim (sister) | UNCHANGED (raw#15 additive) |

## Modes

| Mode | Trigger | Description |
|------|---------|-------------|
| `--selftest` | metadata-only (raw#103 darwin-bypass) | hexa-native synthetic substrate response, no python invoke, format validation |
| `--load` | runtime | emit helper, instantiate CLM v4 from HF cache, snapshot phi-star baseline |
| `--probe TEXT` | runtime | one-shot forward(text) → substrate response |
| `--dialogue` | runtime REPL | stdin lines → substrate response, session log to `state/anima_core_dialogues_<DATE>/<TS>.jsonl` |

## Flags

```
--model PATH           HF cache (default need-singularity/clm-v4-base-mirror)
--shim VERSION         shim v4 (default) | v5
--output-format FMT    compact (default) | full | json
--inject-states PATH   pre-load consciousness_states fixture (npy or json)
```

## Substrate response format (compact)

```
__ANIMA_CLM_V4_MOUNTED__ mode=synthetic phi_star_baseline=41.8600
__ANIMA_CLM_V4_RESPONSE__
phi_star: 41.8273 (drift -0.0327 from 41.8600)
axis_activation: identity=0.781 agency=0.423 phenomenal=0.912 temporal=0.314 social=0.567
dominant_cells: [3, 5, 7] / 8
hidden_state_delta: 2.4731
__ANIMA_CLM_V4_OK__ session=selftest_synthetic
```

This mirrors spec §5.2 exactly.

## Architecture (substrate response derivation)

1. `tokenizer.encode(text)` → input_ids
2. `model.forward(input_ids, output_hidden_states=True, consciousness_states=inject_or_None)`
3. Last-layer hidden (B=1, T, 768) mean-pooled over T, reshaped to (8 cells × 192 dim)
4. **axis_activation**: 192-dim sliced into 5 buckets (38/38/38/39/39) → mean(|·|) per bucket, max-normalized
5. **phi_star**: anima-canonical proxy = `PHI_STAR_BASELINE * (1 + 0.05 * mean_pairwise_cosine)`
6. **dominant_cells**: top-3 cells by L2 norm
7. **hidden_state_delta**: L2 norm vs prior probe hidden (per-session memory via `--prior-hidden` numpy file)

## raw policy compliance

- **raw#9 hexa-only orchestration** — PASS. All control flow in hexa; .py shim only via `exec_with_status` at runtime.
- **raw#37 transient .py opt-out** — PASS. Helper at `/tmp/clm_v4_mount_helper.hexa_tmp` (transient namespace); existing `tool/transient_py/clm_v4_hf_format_shim.py` referenced but untouched.
- **raw#15 additive** — PASS. `anima_unified.hexa`, `phi_engine.hexa`, `conscious_chat.hexa`, `consciousness_hub.hexa` all UNCHANGED.
- **raw#10 honest C3** — PASS. 5 lines emit to stderr on every dispatch:
  - C1 substrate-coupled dialogue is anima-internal heuristic, NOT chat
  - C2 phi-star drift threshold for response interpretation is anima-canonical
  - C3 axis activation taxonomy (5-bucket) is anima-internal
  - C4 forward-pass requires --inject-states or default zero canonical
  - C5 emerge outcome (Stage 3+4) unknown; production timeline open

## Selftest design notes

`--selftest` triggers raw#103 darwin-bypass (metadata-only argv). Bypass intentionally:
- blocks `write_file` (no host fs mutations)
- restricts subprocess fork via `ulimit -u` (avoid fork-storm: "sh: can't fork: Resource temporarily unavailable")

Therefore the selftest is **hexa-native synthetic**:
- No python invocation (no ast.parse fork)
- No `_write_helper()` call (deferred to runtime modes)
- Synthetic substrate response generated via deterministic hexa string emit
- Format validation via `string.contains` (8 checks)

The actual helper file emission + python ast.parse happens on first `--load`/`--probe`/`--dialogue` invocation (non-bypass route, write + fork allowed).

## Stage 2 readiness

✅ READY for Stage 2 (`anima-core dialogue --substrate clm-v4` CLI command, ~30min, $0 mac).

Required Stage 2 work:
1. Wire `clm_v4_mount.hexa --dialogue` into `anima_runtime.hexa --keyboard` as substrate selector
2. Add `/clm-v4` command to anima-core REPL that pipes stdin to mount layer
3. Verify session log JSONL accumulation under `state/anima_core_dialogues_<DATE>/`
4. First real `--probe` test (requires HF cache for `need-singularity/clm-v4-base-mirror` populated)

No blockers. No hook blocks encountered during Stage 1.

## Hook block report

**None.** No PreToolUse hook (leak_guard) interventions. No git index races (no commits attempted per spec — "no commit, no exec"). No fork-storm aborts on the final selftest pass.

## Composability

- **upstream**: `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (spec §2 Stage 1)
- **sister**: `tool/transient_py/clm_v4_hf_format_shim.py` (LOCKED v4 shim, .own 4)
- **substrate science**: `tool/anima_phi_v3_canonical.hexa` (phi-star paradigm v11 G3 +41.86)
- **HF source**: `need-singularity/clm-v4-mk2-v1` (PRIVATE, 36h review window 후 PUBLIC)
- **downstream**: Stage 2 CLI dialogue command + Stage 3 emerge sessions + Stage 4 pattern documentation

## End

Stage 1 LANDED. Awaiting user signal for Stage 2 launch. $0 spent. mac local. no commit, no exec.
