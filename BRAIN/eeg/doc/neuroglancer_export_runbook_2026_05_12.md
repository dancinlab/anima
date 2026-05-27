# Neuroglancer Export — Operator Runbook (2026-05-12)

**Module:** `eeg/export_neuroglancer.hexa`
**Design doc:** `design/core/neuroglancer_precomputed_export_2026_05_12.md`
**Mode (Phase 1):** `--mode=2d-time-series` (16 channels × time samples × 1 singleton-Z)

This runbook gets you from a captured EEG session to a Neuroglancer URL
shareable with collaborators in under 60 seconds.

---

## 1. Pre-flight

```bash
# Where are you?
cd $HOME/.hexa-brain   # or wherever your hexa-brain clone lives

# Sanity check
hexa-brain --version
hexa-brain eeg help | grep export-neuroglancer
```

Expected: `export-neuroglancer  Neuroglancer Precomputed export (2D time-series)`.

## 2. Self-test (no recording required)

```bash
hexa-brain eeg export-neuroglancer --selftest
```

Expected end-of-output:

```
  PASS: F_NG_01 info required keys
  PASS: F_NG_02 scale0 size == [12500,16,1]
  PASS: F_NG_03 n_scales == 4
  PASS: F_NG_04 chunks-per-scale > 0
  PASS: F_NG_05 first chunk bytes == 65536
  PASS: F_NG_06 round-trip bit-compare

Results: 6 PASS / 0 FAIL
    marker: state/markers/export_neuroglancer_selftest_synth_PASS.marker
schema=hexa-brain/eeg/export_neuroglancer/1
selftest: OK
```

Artifacts created:

```
state/precomputed/synth_selftest/        # the precomputed volume
├── info                                 # spec JSON
├── meta.json                            # hexa-brain sidecar (axis disclosure)
├── _selftest_synth.npy                  # source synth (16, 12500) float32
├── _selftest_synth.npy.meta.json
├── 4000000_1000000_1000000/             # scale 0 (250 Hz native)
│   ├── 0-1024_0-16_0-1
│   ├── 1024-2048_0-16_0-1
│   └── ... (13 chunks total)
├── 8000000_1000000_1000000/             # scale 1 (125 Hz mean-pooled)
├── 16000000_1000000_1000000/            # scale 2 (62.5 Hz)
└── 32000000_1000000_1000000/            # scale 3 (31.25 Hz)

state/markers/export_neuroglancer_selftest_synth_PASS.marker
state/export_neuroglancer_ledger.jsonl   # appended
```

## 3. Real-session export

After capturing a session via `hexa-brain eeg record`, you'll have
`recordings/sessions/session_<ts>.json` + a tree of `<task>_<ts>_segNNN.npy`
files. Point the exporter at the session ledger:

```bash
hexa-brain eeg export-neuroglancer \
    --input recordings/sessions/session_<ts>.json \
    --output state/precomputed/session_<ts>
```

Or at a single `.npy`:

```bash
hexa-brain eeg export-neuroglancer \
    --input recordings/sessions/resting_eyes_open_20260512T100000Z_seg000.npy \
    --output state/precomputed/resting_eyes_open_seg000
```

Or at a directory (finds the newest `session_*.json` inside, falls back to
sorted `*.npy`):

```bash
hexa-brain eeg export-neuroglancer \
    --input recordings/sessions/ \
    --output state/precomputed/all_sessions
```

CLI knobs (rarely needed — defaults are tuned):

```
--mode 2d-time-series   default; --mode helmet-annotation is the Phase 2 stub
--chunk-time 1024       scale-0 chunk x size; smaller = more files, finer streaming
--scales 4              number of pyramid levels (mean-pool factor 1×/2×/4×/8×)
--encoding raw          only raw supported in Phase 1
```

Expected output tail:

```
verdict=PASS
schema=hexa-brain/eeg/export_neuroglancer/1
export: OK
```

If `verdict=FAIL`, the `reason` token in the kv-block tells you why (e.g.
`reason=input-missing:<path>`, `reason=phase-2-not-implemented`).

## 4. Serve the precomputed dir over HTTP

Neuroglancer needs an HTTP source. Any static file server works.
The stdlib one-liner:

```bash
cd state/precomputed/session_<ts>
python3 -m http.server 9000
```

Verify:

```bash
curl -s http://localhost:9000/info | python3 -m json.tool | head
# Expected: { "@type": "neuroglancer_multiscale_volume", "type": "image", ... }
```

## 5. Load in the public demo viewer

Open this URL in any browser (replace `9000` with your port):

```
https://neuroglancer-demo.appspot.com/#!{"layers":[{"type":"image","source":"precomputed://http://localhost:9000"}]}
```

What you should see:
- Three-pane orthogonal view (XY / XZ / YZ).
- The XY pane shows a horizontal band of 16 channel rows (Y axis) × time
  samples (X axis). Scroll horizontally to scrub time.
- The pyramid zoom (mouse wheel) hops between the 4 mean-pooled scales.
- The intensity is direct float32 µV (no scaling) — set the "shader" range
  to your expected µV span (e.g. -100 to +100 for resting state) for legible
  contrast.

For permanent / non-localhost sharing: host the dir on Google Cloud Storage
or any CDN (the spec is byte-identical), then change the URL's
`http://localhost:9000` to the public origin.

## 6. Verify a pre-existing precomputed dir

```bash
hexa-brain eeg export-neuroglancer --verify state/precomputed/session_<ts>
```

The verify sub-mode:
- Parses `info` JSON, asserts `type=image, data_type=float32`.
- Walks each scale's chunk dir, asserts ≥1 chunk per scale.
- Reports first-chunk byte size vs the full-chunk expected size.
- *Optionally* imports the `neuroglancer` Python client; on `ImportError`
  emits `verify_skipped=neuroglancer-not-installed` and continues (exit 0
  if the structural checks pass).

To enable the client-side round-trip check:

```bash
.venv-eeg/bin/pip install neuroglancer    # Apache-2.0; not auto-installed
hexa-brain eeg export-neuroglancer --verify state/precomputed/session_<ts>
# Expected: `neuroglancer_import=ok` instead of `verify_skipped=...`.
```

## 7. Channel ordering reminder

The 16 Y rows correspond to the **Cyton (1-8) + Daisy (9-16)** physical
channel order, with 10-20 labels embedded in the sidecar `meta.json`:

```
Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7, F8, F3, F4, T7, T8, P3, P4
```

Row 0 = Fp1 (top of the Y axis in the XY pane).

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `verdict=FAIL reason=input-missing:<path>` | `--input` doesn't point at an existing file/dir. | Double-check path; `ls -la` the target. |
| `verdict=FAIL reason=phase-2-not-implemented` | You ran `--mode=helmet-annotation`. | Switch to `--mode=2d-time-series` (Phase 1 only). |
| Neuroglancer viewer says "Failed to fetch info" | HTTP server not running OR CORS blocked OR port mismatch. | `curl http://localhost:9000/info` to confirm. Use `python3 -m http.server` (sends permissive CORS by default for `precomputed://`). |
| Image is all-zeros / featureless | Source `.npy` was zero / `eeg_indices` mismatched. | Inspect `state/precomputed/<session>/_*.npy` directly with numpy. |
| Selftest fails F_NG_06 (round-trip) | numpy installed but byte-order differs (very rare, big-endian host). | Open an issue — current writer uses `'<f4'` little-endian explicitly. |

## 9. Cross-references

- Design doc: `design/core/neuroglancer_precomputed_export_2026_05_12.md`
- Module: `eeg/export_neuroglancer.hexa`
- Template: `tool/module/_core/eeg_export.hexa` (parts-push emitter shape mirror)
- Session capture: `eeg/eeg_recorder.hexa` + `hexa-brain eeg record`
- Public demo viewer (read-only mirror): https://neuroglancer-demo.appspot.com/
