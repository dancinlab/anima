# electrode_adjustment_helper — 16ch concurrent touch detector upgrade

date: 2026-04-29
file: `anima-eeg/electrode_adjustment_helper.hexa` (1310 → 1542 LoC, +232)
context: BrainFlow cyton_daisy 16ch headset realtime electrode-touch helper

## rationale

prior version supported multi-channel concurrent touch in `--live` mode
(`active_indices` array, all-touched-positions highlighted), but the
`--selftest` mode only emitted hardcoded kv stub values (`active_indices=[2,5,11]`)
without actually exercising the detector pipeline. that meant the
"can the helper detect 2 simultaneous touches?" assertion could pass on
selftest while the live pipeline was silently broken.

this upgrade:

1. replaces the kv-stub `--selftest` with a real synthetic-data pipeline test:
   - synthesize 16ch noise (gaussian, rms ≈ 6000µV, 4s @125Hz)
   - inject upward spikes on **ch3 + ch7** simultaneously starting at t=2s
     (×3.5 amplitude → rms boost exceeds 3-AND threshold)
   - run the full detector loop (3-AND threshold, frozen baseline, uni-directional
     UP-only) tick-by-tick at 60Hz simulation
   - assert BOTH ch3 AND ch7 appear in `active_indices` in the same tick
2. exposes per-channel state struct fields (`baseline_mean`, `baseline_std`,
   `touched`, `last_touch_ms`) — vectorized numpy arrays of shape `(16,)`
   shared across the live loop, replacing scalar derived values
3. adds `TICK_HZ` as a single-constant toggle (60 default, 120 supported via
   `--fps`); derives `TICK_INTERVAL_MS` and uses adaptive sleep with `MIN_SLEEP_MS = 1.0`
   floor (raw#12 — never busy-loop)
4. adds GRAY ANSI (`chr(27)+'[90m'`) for idle electrodes alongside existing
   GREEN (`chr(27)+'[32;1m'`) for touched — multi-color headplot
5. adds frame-budget measurement (`work_ms` per tick) emitted to JSONL row
   and rendered in the live display panel
6. ANSI escape sequences use `chr(27)` per RFC-003 string-escape workaround;
   verified compatible with macOS Terminal.app + ghostty (both render
   `\x1b[90m` as bright-black/gray; both honor cursor-home + clear-to-end)

## per-channel state struct (vectorized numpy form)

```
buffer[ch, :ROLLING_SIZE]   # rms_window — raw sample rolling buffer (≈100ms @125Hz)
baseline_mean[ch]: f64      # median of recent rms snapshots
baseline_std[ch]:  f64      # std of recent rms snapshots
touched[ch]:       bool     # active touch state
last_touch_ms[ch]: i64      # epoch ms of last positive detection
```

stored as numpy arrays of shape `(n_ch,)` for vectorized 16ch parallel updates.
single-touch detection becomes `touched.any()`; multi-touch becomes
`active_indices = np.where(touch_active)[0]`.

## 3-AND threshold (preserved from session 2026-04-28 calibration)

```
deviation > 1.4σ  AND  abs_change > 3000µV  AND  rel_change > 0.20
```

uni-directional UP-only (touched = positive RMS spike). frozen baseline
per-tick: when `touch_active.any()` is true, the rms snapshot is NOT
appended to history, preventing baseline poisoning during sustained touch.

## selftest evidence (run 2026-04-29)

```
SELFTEST PIPELINE: concurrent_pass=Y (spikes=[3,7] first_tick=127
                   first_chs=[3,7] max_active=3)
FRAME BUDGET (synth): mean=0.062ms p95=0.049ms max=7.295ms
                      | target 60fps=16.667ms 120fps=8.333ms
```

- BOTH ch3 (C4) and ch7 (O2) detected concurrently — verdict ALL_OK
- frame work mean 0.062ms — 269x under 60fps budget, 134x under 120fps budget
- max 7.295ms first-tick cold start (numpy import); steady-state sub-ms

ANSI probe verification:
- `ansi_green_probe = chr(27)+'[32;1m●'+chr(27)+'[0m'` ✓
- `ansi_gray_probe  = chr(27)+'[90m·'+chr(27)+'[0m'` ✓

## modes

```
--selftest    synthetic 16ch noise + dual-spike pipeline test (no hardware)
--check       one-shot real check (single BrainFlow session)
--watch       periodic loop (5s tick)
--live        REAL-TIME 16ch concurrent touch detector
              (default 60fps, --fps 120 supported, clamp 10-240)
```

## terminal compatibility (RFC-003 chr(27) workaround)

| terminal       | cursor-home `\x1b[H` | clear-to-end `\x1b[J` | gray `\x1b[90m` | green `\x1b[32;1m` |
|----------------|----------------------|------------------------|-----------------|---------------------|
| Terminal.app   | OK                   | OK                     | OK              | OK                  |
| ghostty        | OK                   | OK                     | OK              | OK                  |

no observed differences between Terminal.app and ghostty for the escape
sequences used. both render the in-place fast_render() pattern without
scroll accumulation.

## constraints honored

- raw#9 hexa-only (Python helper materialized via `_write_helper()` to /tmp)
- raw#10 honest (selftest now actually runs the detector pipeline)
- raw#12 silent-error-ban (adaptive sleep has 1ms floor; no busy-loop)
- raw#37 transient-helper-in-/tmp (`/tmp/anima_eeg_electrode_adjustment_helper.py`)
- raw#65 idempotent (selftest JSONL truncates+rewrites)
- raw#82 darwin-native (BrainFlow USB only on macOS host)
- raw#91 honesty-triad (synthetic mode does NOT replace real-hardware verification —
  documented in selftest docstring)
- raw#101 minimal (single file, no new tool surface)
- own#5 completeness-first (selftest covers the full 16ch concurrent path)
