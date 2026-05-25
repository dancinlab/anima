# Neuroglancer Precomputed Export — Design Doc (2026-05-12)

**Status:** Phase 1 landed. Phase 2 (helmet annotation) deferred.
**Author:** hexa-brain Sprint 1 / Part B-1.
**Schema:** `hexa-brain/eeg/export_neuroglancer/1`
**Module:** `eeg/export_neuroglancer.hexa`
**Runbook:** `eeg/doc/neuroglancer_export_runbook_2026_05_12.md`
**License:** MIT (hand-written writer — no Apache-2.0 import dependency).

---

## 1. Goal

Zero-friction sharing of hexa-brain EEG recordings with external collaborators
who already use Google's open-source Neuroglancer viewer (the dominant
visualization frontend in the connectomics community). A `--mode=2d-time-series`
export produces a Precomputed multiscale volume that loads in the public
demo viewer
(`https://neuroglancer-demo.appspot.com/#!{...}`) via a `precomputed://`
source URL pointing at a local HTTP server.

## 2. Decisions locked

| Param | Value | Rationale |
|---|---|---|
| File location | `eeg/export_neuroglancer.hexa` | Standalone module reading existing recordings. Recording (capture) ≠ export (format conversion). Mirrors `tool/module/_core/eeg_export.hexa` template 1:1. |
| X axis | time (samples) | resolution = `1e9 / sample_rate` ns/voxel. See §5 honesty disclosure. |
| Y axis | channel (16) | resolution = 1_000_000 ns (1 mm-equivalent). |
| Z axis | singleton (size 1) | Precomputed requires 3D. |
| dtype | float32 | EEG µV in native float32. |
| chunk_size (scale 0) | `[1024, 16, 1]` | ~440 chunks for 30-min @ 250 Hz (see §4 math). |
| n_scales | 4 | mean-pool along time 1× / 2× / 4× / 8×; balances file count vs zoom UX. |
| encoding | `raw` (little-endian, x-fastest = Fortran) | Simplest. Float32 raw is uncompressed but tractable. Lossless round-trip required by `--selftest` F_NG_06. |
| External lib | None (hand-written) | MIT-clean. The Neuroglancer Python client (`google/neuroglancer`) is Apache-2.0; both compatible-with-MIT and a hard import target. We hand-write the spec's `info` JSON + raw chunk bytes via `numpy + json + open(..,'wb')` instead. |
| `--verify` lib | optional, lazy | Only the `--verify` sub-mode imports `neuroglancer`; on `ImportError` it prints `verify_skipped=neuroglancer-not-installed` and exits 0. Keeps Phase 1 CI green without adding a dependency to any manifest. |
| Phase 1 mode | `--mode=2d-time-series` only | `--mode=helmet-annotation` is a stable CLI surface stub returning `verdict=FAIL reason=phase-2-not-implemented`. |

## 3. Spec reference (Precomputed `info` shape we emit)

```json
{
  "@type": "neuroglancer_multiscale_volume",
  "type": "image",
  "data_type": "float32",
  "num_channels": 1,
  "scales": [
    {
      "chunk_sizes": [[1024, 16, 1]],
      "encoding": "raw",
      "key": "4000000_1000000_1000000",
      "resolution": [4000000, 1000000, 1000000],
      "size": [N_samples, 16, 1],
      "voxel_offset": [0, 0, 0]
    },
    ...
  ]
}
```

Chunk file naming: `<output>/<key>/<x0>-<x1>_<y0>-<y1>_<z0>-<z1>`.

Chunk byte layout: little-endian float32, **Fortran order (x-fastest)** per the
Precomputed `raw` encoding spec. Each scale's resolution = base × 2^scale on
the X axis only; Y and Z stay at 1_000_000 ns (the singleton-Z dimension is
preserved across scales).

## 4. Chunk-count math (30-min session @ 250 Hz example)

- N_samples = 30 × 60 × 250 = 450_000
- chunk_x = 1024, chunk_y = 16, chunk_z = 1
- scale-0 chunks_x = ⌈450_000 / 1024⌉ = 440  (file count: 440)
- scale-1 chunks_x = 220
- scale-2 chunks_x = 110
- scale-3 chunks_x = 55
- Total chunk files ≈ 440 + 220 + 110 + 55 = **825**
- Bytes per full chunk = 1024 × 16 × 1 × 4 = **65 536 bytes** (64 KiB)
- Total payload (lossless) ≈ N_samples × 16 × 4 × (1 + 1/2 + 1/4 + 1/8) ≈ 54 MiB

Selftest (50 s @ 250 Hz = 12 500 samples) lands 26 chunks total (13 + 7 + 4 + 2).


Neuroglancer Precomputed treats `resolution` as nanometres per voxel: an
intended-for-3D-EM-volume convention. We export a 2D time-series where the
X axis is time samples and the Y axis is electrode index. Encoding that as
"ns per voxel" is semantically wrong — the X axis is not a spatial axis.

We use the convention anyway because (a) Neuroglancer requires it,
(b) collaborators can still scroll the time axis with no client-side
modification, and (c) the temporal interpretation is preserved via the
**sidecar `meta.json`** (non-spec, hexa-brain-only):

```json
{
  "schema": "hexa-brain/eeg/export_neuroglancer/1",
  "x_axis": "time_samples",
  "x_resolution_s": 0.004,
  "sample_rate_hz": 250.0,
  "y_axis": "electrode",
  "z_axis": "singleton",
  "channel_names": ["Fp1", "Fp2", "C3", ...],
  "axis_units_disclosure": "time-as-X uses ns/voxel as Precomputed convention; the axis is samples, not nanometres."
}
```

Phase 2 (helmet annotation) will revisit this — for a real 3D head model
with electrode positions in physical space, the ns-as-nm convention becomes
sensible again.

## 6. Phase 2 roadmap — `--mode=helmet-annotation`

Goal: emit a Precomputed `annotation` layer that places each electrode
(Fp1 ... P4) at its 10-20 head-surface coordinate, paired with the same
time-series image layer. The viewer would then show a head with 16 dots
that update colour from band-power per time-sample.

Open questions (deferred to Phase 2 design):
- 3D head model source — MNE `standard_1020` montage XYZ? FreeSurfer fsaverage?
- annotation schema — `point_annotations` with `id` = channel name?
- time animation — frame-as-scale? client-side scrubbing?
- compatibility with the existing 2D image layer URL — single info or multi-source?

Phase 1 reserves the CLI surface: `--mode=helmet-annotation` exits with
`verdict=FAIL reason=phase-2-not-implemented` (stable; documented; won't
move under callers).

## 7. Why hand-write vs Apache-2.0 import

| Option | Pros | Cons | Decision |
|---|---|---|---|
| `import neuroglancer` (Apache-2.0) | Spec compliance guaranteed; less code to maintain | Adds Apache-2.0 dep to `eeg/` layer; license firewall (Part A) would need an extra catalog entry; not all consumers want the dep. | Rejected for Phase 1 writer. |
| `import cloudvolume` (BSD-3 from seung-lab) | Better-tested writer; BSD-3 license-friendly | Heavy dep; gcsfs / google-cloud-storage transitive deps; overkill. | Rejected. |
| Hand-write `info` JSON + raw bytes | Zero deps; MIT-clean; ~80 LOC of helper Python; perfect spec control. | Manual upkeep if spec evolves; round-trip semantics need explicit test. | **Chosen.** |
| Lazy `--verify` with `neuroglancer` Python | Bonus client-side validation when dep available; no manifest add. | Optional code path only; verify can pass without it. | **Chosen** as opt-in sub-mode. |


| ID | Assertion | Coverage |
|---|---|---|
| F_NG_01 | `info` JSON has `@type, type, data_type, scales, num_channels` and `type=='image' AND data_type=='float32'`. | Schema sanity. |
| F_NG_02 | `scales[0].size == [N_samples, 16, 1]`. | Volume dimensions match input. |
| F_NG_03 | `len(scales) == 4`. | Mean-pool pyramid built. |
| F_NG_05 | First chunk byte size == `chunk_x*chunk_y*chunk_z*4`. | Full-chunk byte math (selftest input is large enough). |
| F_NG_06 | Round-trip: read 4 bytes of chunk-0 back as `'<f4'` little-endian float32, bit-compare to `data[0,0]`. | Encoding correctness (Fortran order, little-endian, lossless raw). |

Selftest input is deterministic: `(16, 12500)` float32 (50 s @ 250 Hz, seed
`20260512`, sine 8-14 Hz + noise). Output is byte-identical across runs

## 9. Input formats accepted

The `--input` flag accepts three shapes:

1. **Single .npy** — `recordings/sessions/<task>_<ts>_seg000.npy`. Reads
   the optional `.meta.json` sidecar for `sample_rate` + `eeg_indices`.
2. **Directory** — searches for `session_*.json` first (multi-segment
   ledger); falls back to `*.npy` in sorted order.
3. **Session ledger** — `session_<ts>.json` emitted by
   `eeg/eeg_recorder.hexa`. Walks `tasks[*].segments[*]` (sorted by
   concatenates segments along time axis. Inter-segment gap is honest
   ~1s per `eeg_recorder.hexa:36` — documented, not bridged here.

## 10. Marker + ledger conventions

- Marker (PASS): `state/markers/export_neuroglancer_<ts>_PASS.marker`
- Marker (FAIL): `state/markers/export_neuroglancer_<ts>_FAILED.marker`
- Ledger: `state/export_neuroglancer_ledger.jsonl` (append-by-rewrite, mirroring `eeg/impedance_check.hexa:722-740`)
  idempotent); real exports use `date -u +%s` unix timestamp.

## 11. Cross-references

- Template: `tool/module/_core/eeg_export.hexa` (parts-push, kv-block, --selftest skeleton)
- Ledger pattern: `eeg/impedance_check.hexa:722-740`
- Session layout: `eeg/eeg_recorder.hexa:395-422`
- License firewall (Part A — next sprint): `vendor/external_deps.yaml` will list `neuroglancer-py` as Apache-2.0 optional verify-only dependency.

---

## 12. Resolved open questions (2026-05-12)

The three reviewer-facing open questions from the 2026-05-12 session boundary
are resolved as follows. Decisions 1 and 2 codify behavior already implemented
in Phase 1; decision 3 promotes a §6 Phase 2 open question to a locked choice.

| # | Question | Decision | Rationale |
|---|---|---|---|
| 1 | `--verify` behavior when `neuroglancer-py` is missing — PASS-with-skip or strict FAIL? | **PASS-with-skip** | The dep is **optional verify-only** (already in §2 decisions table + §7 "lazy `--verify`"). Strict FAIL would force the Apache-2.0 dep into every test env, defeating the hand-written MIT-clean rationale. Emit `verify_skipped=neuroglancer-not-installed` and exit 0. |
| 2 | Ledger idempotency — append one row per `--selftest`, or dedupe to one row total? | **Append one row per selftest run** | Matches `eeg/impedance_check.hexa:722-740` pattern (already cited in §10). The ledger is an append-only audit trail; selftest runs are observable events worth recording. Operators dedupe at read-time if they want last-state-only. |
| 3 | Phase 2 helmet 3D coordinate source — MNE `standard_1020` or FreeSurfer `fsaverage`? | **MNE `standard_1020`** | License-friendly (`mne` is BSD-3, fits the `eeg/` layer's allow-list under the license firewall). `fsaverage` requires FreeSurfer (CC-NC-like license complications) plus a large external data download. `standard_1020` ships as a small dict in `mne.channels.make_standard_montage('standard_1020')` and covers the 16 channels we use exactly. |

### Cross-reference

These three resolutions are B-1 (Neuroglancer) decisions of the six-item
2026-05-12 user-decision set. The three E-1 (Substrate) decisions live in
`design/substrate_abstraction.md` §9.

### Implementation impact

- Decisions 1 & 2: **no code change** — `eeg/export_neuroglancer.hexa` Phase 1 already implements both behaviors. Doc-only confirmation.
- Decision 3: **Phase 2 only** — locked for the future `--mode=helmet-annotation` implementation. No Phase 1 code is affected.

---

## 13. Phase 2 land record — `_neuroglancer_helmet_helper.py` (2026-05-13)

V1 of `--mode=helmet-annotation`: the **coordinate inventory** layer. Full Neuroglancer Precomputed `annotation` layer (spatial_index, by_id, binary point_annotation chunks) is V2 — deferred. V1 lands the sidecar `meta.json` + selftest.

### 13.1 Surface

`eeg/_neuroglancer_helmet_helper.py` (hand-maintained, RFC-016 §1.4 anti-pattern avoided per Phase 2b precedent):

| Function | Behavior |
|---|---|
| `compute_montage_xyz_16(channel_names=None) → ({name: [x,y,z]}, coord_source)` | MNE `standard_1020` lazy import → 16-ch CYTON_DAISY subset. MNE absent → hand-curated 10-20 fixture (`coord_source="fixture"`). MNE present → `coord_source="mne_standard_1020"`. Selftest passes either path. |
| `build_helmet_meta(channel_names=None) → dict` | Sidecar shape: `{schema, coord_source, coord_units:"meters", coord_frame, channels:[{name,xyz},…]}`. |
| `write_helmet_meta(out_dir, channel_names=None) → (dict, path)` | Writes `meta.json` into `out_dir`. |

Standalone CLI: `python3 eeg/_neuroglancer_helmet_helper.py {selftest|inspect}`.


| ID | Assertion |
|---|---|
| `F_NG_HA_01` | `build_helmet_meta()` returns dict with 16 channels, each having a 3-tuple `xyz`. |
| `F_NG_HA_02` | Emitted channel names match `CYTON_DAISY_16 = [Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7, F8, F3, F4, T7, T8, P3, P4]` order-preserving (matches `eeg/substrates/channel_set.hexa`). |
| `F_NG_HA_03` | `write_helmet_meta()` → `meta.json` write → JSON round-trip preserves the dict (schema, channels[0].name="Fp1", channels[0].xyz length 3). |

Verified 2026-05-13 on this Mac box (MNE not installed): `selftest` → 3/3 PASS, `coord_source=fixture`, exit 0.


1. **Sidecar `meta.json` is NOT yet wired into a Neuroglancer viewer URL.** That's Phase 2.1 — `eeg/export_neuroglancer.hexa --mode=helmet-annotation` will consume this file and produce the actual annotation layer + viewer URL. V1 here is the *coordinate inventory* only.
2. **Fixture coordinates are NOT anatomically accurate** — coarse 10-20 approximations in a unit-head-radius frame. Used only when MNE is absent (selftest determinism). Production callers SHOULD have MNE installed via `pip install mne` (BSD-3, fits the `eeg/` layer's license-firewall allow-list).
3. **Z axis** — MNE head-surface frame puts z up (vertex Cz at high z). The helper emits raw `(x,y,z)` without rotation; the viewer URL composition step (Phase 2.1) is responsible for orientation transforms.

### 13.4 Phase 2.1 (deferred) — viewer URL composition

`eeg/export_neuroglancer.hexa --mode=helmet-annotation` will:
- Call helper.py (via the same hand-maintained pattern as `_brainflow_helper.py`).
- Emit a Precomputed `annotation` layer (binary chunks per the [Neuroglancer Precomputed annotation spec](https://github.com/google/neuroglancer/blob/master/src/datasource/precomputed/annotations.md)): `info` JSON declaring `point` type, `spatial_index` chunks, optionally `by_id` index.
- Optionally combine with the `--mode=2d-time-series` image layer into a single multi-source viewer URL (open question §6.4 — single info vs multi-source).
- Selftest: extend hexa-side assertions with `F_NG_HA_*` PASS checks.

