# Webcam Eye-Tracker Paradigm — Design Doc (2026-04-28, C19)

## Purpose (C19)
Provide **Mac-built-in-webcam-based gaze + ocular metrics** so EEG features
(LZ76, engagement_index, drowsy_index, alpha attenuation) can be cross-modal
correlated against ocular ground truth (gaze position, blink rate, fixation
duration, saccade rate, pupil/iris-size proxy).

C19 = "where are you looking, and how often are you blinking?" — cross-modal
ocular paradigm that complements:
- T2 (daily_life_context_labeling): WHAT app
- B11 (behavioral_correlates_logger): HOW HARD you work
- C19 (this): WHERE you look + ocular state

## Differentiation table
| Axis | T2 | B11 | C19 |
|------|----|-----|-----|
| Modality | active_app, audio | keyboard/mouse/scroll | webcam (face + iris) |
| Granularity | discrete labels | continuous behavioral rates | gaze (x,y) per 30 ms |
| EEG join | label-conditional means | Pearson r | gaze ↔ alpha; blink ↔ drowsy |
| Window | 5 s flag | 5-min sliding | 30 Hz sample, 1-min aggregate |
| Privacy | audio level only, no content | rates only, no positions | 68/468 landmarks only, NO image |

NO Claude / LLM / remote inference. Mac local only.
MediaPipe FaceMesh (468-pt). User must explicitly grant Camera permission and
launch the calibration session; the agent never auto-launches the camera.

## Five ocular metrics (30 Hz, 1-min aggregate)
| # | Metric | Method | Privacy invariant |
|---|--------|--------|-------------------|
| 1 | `gaze_x_screen_pct, gaze_y_screen_pct` | iris-center vector → 9-pt-calibrated screen mapping; emit only normalized [0..1000] x1000 | NO image / NO face encoding stored |
| 2 | `blink_rate_per_min` | EAR (eye-aspect-ratio) < 0.20 detection (Soukupová 2016); count blinks in 60 s window | NO eyelid imagery, count only |
| 3 | `fixation_duration_avg_ms` | I-DT (dispersion-threshold) algorithm: gaze stays within 1° dispersion ≥ 100 ms ⇒ fixation; average duration over window | derived only |
| 4 | `saccade_rate_per_min` | velocity > 30°/s threshold (Salvucci 2000 I-VT); count over window | derived only |
| 5 | `pupil_dilation_proxy_x1000` | iris bounding circle radius normalized by inter-canthal distance (lighting-dependent honest C3 caveat) | NO absolute pixel sizes |

9-point screen calibration BEFORE every session:
- 4 corners + 4 edge-midpoints + 1 center (total 9 fixation targets)
- Each target: 1.5 s fixation, last 1.0 s averaged for mapping
- Per-axis affine fit `screen = a*iris_x + b*iris_y + c` (least-squares, fixed-point)
- Acceptance: residual ≤ 5° visual angle (≈ 5% screen at 50 cm viewing distance)
- F5 falsifier: residual > 5° ⇒ session aborts (calibration_fail)

- H1 `blink_rate_per_min ↔ drowsy_index` Pearson r ≥ +0.30
  (Stern 1994 — blink-rate-drowsiness coupling)
- H2 `fixation_duration_avg_ms ↔ engagement_index` Pearson r ≥ +0.30
  (long fixations ↔ deep engagement / cognitive load)
- H3 `saccade_rate_per_min ↔ alpha_power_attenuation` Pearson r ≥ +0.20
  (Berger 1929 — alpha desynchronizes with active visual exploration)
- N ≥ 1 hour of paired EEG+gaze; r ≥ 0.30 minimum meaningful.
- r < 0.10 cumulative across N ≥ 100 1-min windows ⇒ relationship absent (F4).

## Sampling
- 30 Hz native Mac webcam (FaceTime HD class — std 30 fps).
- 1 frame → 1 landmark sample → 1 gaze (x,y) point.
- 1-min aggregate window emits one JSONL row.

```json
{
  "ts": "2026-04-28T13:42:00Z",
  "gaze_x_screen_pct_x1000": 512,
  "gaze_y_screen_pct_x1000": 480,
  "blink_rate_per_min": 16,
  "fixation_duration_avg_ms": 280,
  "saccade_rate_per_min": 90,
  "pupil_dilation_proxy_x1000": 320,
  "calibration_residual_deg_x1000": 2400,
  "schema": "anima/eye_tracker/1"
}
```
Stored at: `state/eye_tracker_audit/<UTC-date>_gaze.jsonl`

- I1 NEVER store webcam frames / images (RAM-only, free()'d after landmark extract)
- I2 NEVER store face encodings / embeddings (no identity vector)
- I3 Store ONLY 68 (dlib) or 468 (MediaPipe) landmark coords as transient
       in-memory buffers; even those are reduced to the 5 aggregate metrics
       before any disk write
- I4 NEVER persist iris pixel patches / scleral patches
- I5 Output JSONL contains ONLY the 5 metrics + ts + schema (no raw landmarks)
- I7 Camera light-on indicator visible during entire session (Mac hardware-enforced)

- F1 Mac webcam permission denied ⇒ helper exits with `camera_denied` code
  (NOT silent fallback to fake data); selftest with --mode `permission_denied`
  asserts `error="camera_denied"` in row.
- F2 lighting < 30 lux (synth `low_light` mode) ⇒ landmark detection fail
  ⇒ helper emits `error="landmark_fail"`, all 5 metrics are -1 sentinel
  (not zeroes — refuses to fabricate).
- F3 user wears glasses / iris occluded (synth `iris_occluded` mode) ⇒
  pupil_dilation_proxy_x1000 = -1, other 4 metrics still emitted.
- F4 privacy leak audit: helper output JSONL must NEVER contain literal
  substrings `frame`, `image`, `face_encoding`, `landmark`, `iris_patch`,
  `pixel`, `embedding`, base64 PNG/JPEG headers (`iVBORw0KGgo`, `/9j/4`).
- F5 calibration fail: synth `cal_fail` mode forces residual > 5° ⇒ helper
  emits `error="calibration_fail"`, session aborts (no further metrics).
- F7 EAR sanity: synth `eyes_closed` mode (EAR < 0.20 sustained 60 s) ⇒
  blink_rate_per_min = 60 (full-window blinking ≡ closed) AND
  fixation_duration_avg_ms = -1 (no valid fixations when eyes closed).

## Implementation
- `anima-eeg/tool/eye_tracker_webcam.hexa` — orchestration, arg parsing,
  selftest with synthetic gaze trajectories, 7 falsifiers, calibration runner,
  tick polling. ~150 LoC.
  (OpenCV `cv2.VideoCapture(0)` or MediaPipe FaceMesh), extracts landmarks
  in-memory, computes 5 metrics, prints JSONL to stdout. NEVER writes images.
  Real-mode requires `pip install opencv-python mediapipe`; not bundled (NO
  network at runtime — user installs once).
- Cadence: launchd plist `StartInterval=60` (1-min window) — but **user-
  explicit-load only**. NEVER auto-loaded by agent. User runs:
  ```
  hexa run anima-eeg/tool/eye_tracker_webcam.hexa --calibrate
  hexa run anima-eeg/tool/eye_tracker_webcam.hexa --tick
  ```

## RAW compliance
(real vs synth, lighting caveat, glasses caveat) · own 5 (genus + 4
frameworks + 7 falsifiers + counter-example + privacy invariants 7).

`webcam-gaze-ocular-cross-modal-eeg-tracker`

## Frameworks (own-5 ≥ 2)
- Soukupová & Čech 2016 — EAR (eye-aspect-ratio) blink detection
- Salvucci & Goldberg 2000 — I-VT / I-DT fixation/saccade classification
- Stern, Boyer, Schroeder 1994 — blink-rate ↔ drowsiness coupling
- Pope, Bogart, Bartolome 1995 — engagement index, EEG ↔ ocular bridge
- Berger 1929 — alpha attenuation during active visual exploration

**Eyes-closed sleep / unattended monitor** session: gaze (x,y) undefined,
blink_rate_per_min ≈ 60 (collapsed lid ≡ continuous "blink" by EAR threshold),
fixation_duration_avg_ms = -1 (sentinel — no valid fixations), saccade_rate
≈ 0, pupil_dilation_proxy = -1.

EEG drowsy_index must spike here. If EEG drowsy_index remains low while gaze
helper signals "eyes closed full minute," the EEG montage is suspect, not the
gaze logger. Conversely, if EEG says drowsy but gaze helper says active
saccading + low blink_rate, drowsiness is mental-only (engaged but tired) —
both signals honestly retained, no automatic reconciliation.

## User action plan (calibration session)
```bash
# 1. one-time setup (user terminal, agent does NOT auto-run)
pip install opencv-python mediapipe numpy

# 2. grant Camera permission to Terminal.app (System Settings > Privacy > Camera)

# 3. calibrate (9-point, ~14 s)
$HEXA_LANG/hexa.real run anima-eeg/tool/eye_tracker_webcam.hexa --calibrate

# 4. tick (one 1-min polling cycle, append to today's ledger)
$HEXA_LANG/hexa.real run anima-eeg/tool/eye_tracker_webcam.hexa --tick

# 5. selftest (synthetic, no camera needed — for CI / verification)
$HEXA_LANG/hexa.real run anima-eeg/tool/eye_tracker_webcam.hexa --selftest

$HEXA_LANG/hexa.real run anima-eeg/tool/eye_tracker_webcam.hexa --falsifiers
```
