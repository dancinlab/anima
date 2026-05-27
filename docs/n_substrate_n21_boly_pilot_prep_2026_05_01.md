# N-21-E — Boly 2017 Pilot Kit Integration Spec

**Agent:** N-21-E Boly pilot kit
**Date:** 2026-05-01
**Mission:** Assemble a $0 measurement kit (webcam + OpenBCI + LSL) so the user can begin the 7-day Boly 2017 bistable pilot at any time.
**Predecessor:** `docs/n_substrate_n21_boly_webcam_fallback_2026_05_01.md` (verdict = GazeRecorder/GazeCloudAPI VIABLE-DEGRADED, 5–13 pp accuracy gap).
**Race-isolated outputs:**
- `docs/n_substrate_n21_boly_pilot_prep_2026_05_01.md` (this file)
- `state/n_substrate_n21_boly_pilot_prep_2026_05_01/{checklist,falsifiers,preflight,verdict}.json`
**Off-repo kit (HEXA-only repo constraint):** `~/n21_boly_kit/` (5 source files + README)

---

## 1. Boly 2017 Protocol — Stimulus Choice & Schedule

### Stimulus selection: rotating Necker cube (with Honest C3)

| Candidate | Decision | Reason |
|---|---|---|
| Binocular rivalry (orig. Boly stack) | NO | Requires mirror stereoscope; not feasible on a single laptop screen |
| Bistable plaid (Boly 2017 paper actual) | NO (deferred) | WebGL gratings doable but more eng-time; no improvement over Necker for OKN-only readout in pilot |
| Motion-induced blindness | NO | Switches too rare (~30 s ISI) — would inflate session length 3x |
| **Rotating Necker cube + slow drift** | **YES** | Single 2D SVG, induces clear OKN slow-phase reversal, ~5–15 s switch interval, no special hardware |

**Honest C3:** This is a *stimulus deviation* from Boly 2017 (we replace bistable plaid with Necker cube). Both are bistable percepts producing OKN-coupled oculomotor signatures (Frassle et al. 2014, Naber et al. 2011), so qualitative phenomenology is shared, but quantitative decoder accuracy is not directly comparable to Boly's 88%. We label our pilot as a *Boly-like* paradigm and report the substitution explicitly.

### 7-day session schedule

| Day | Sessions | Per-session length | Total/day |
|---|---|---|---|
| 1–7 | 3 | 20 min stimulus + 3 min pre-cal + 3 min rest x2 + 11 min validation = 60 min | 75 min wall-clock incl. setup |

Per-session breakdown (enforced by `daily_runner.sh` countdown):
1. `00:00–03:00` — 9-point gaze calibration + drift-correction fixation
2. `03:00–23:00` — Stimulus block A (counterbalanced first)
3. `23:00–26:00` — Rest
4. `26:00–46:00` — Stimulus block B
5. `46:00–49:00` — Rest
6. `49:00–60:00` — Post-trial validation grid (drift QC)

Total recording per pilot = 21 sessions × 40 min stimulus = **14 h stimulus** + 7 h paratrial.

### OKN-based covert switch decoder

* Slow-phase velocity = differentiated gaze.x, low-passed below 2 Hz, quick-phase saccades (>200 px/s) rejected as NaN.
* Rolling 1.5-s median sign of slow-phase velocity = perceived rotation direction.
* Switch event = sign reversal sustained ≥1 sample with refractory ≥ 2 s.
* Hit window = ±1.5 s vs subject overt keypress (F=front-dominant, B=back-dominant).
* Pass gate: accuracy ≥ 75 % (Boly research-grade benchmark = 88 %; our budgeted gap = 5–13 pp per fallback verdict).

---

## 2. Hardware Checklist

| Item | Owned? | Note |
|---|---|---|
| Mac laptop with built-in webcam ≥720 p, 30 Hz | Yes (assumed) | M-series arm64 verified for BrainFlow 5.21.0 universal2 dylibs |
| OpenBCI Cyton + Daisy 16-ch board | Yes | per mission brief |
| OpenBCI BLE/USB serial dongle | Yes | `/dev/cu.usbserial-*` auto-detected by `openbci_lsl.py` |
| Cyton USB cable | Yes | included with board |
| Saline / gel + electrode paste | Verify before Day 1 | ~$15 if depleted |
| Optional: chinrest for head stabilization | Recommended | Boly used hardware head-fix; absence is C3 risk for high gaze drift |

Electrode setup target: **<10 min**, impedance < 30 kΩ on ≥12/16 channels (raw#71 falsifier F-N21E-4).

---

## 3. Software Checklist

| Component | Source | Install command | Verified |
|---|---|---|---|
| Python 3.11+ | system | already installed (3.14.4 detected) | YES (Mac arm64) |
| `pylsl` | PyPI | `pip3 install pylsl` | YES — universal2 wheel (pylsl 1.18.2) |
| `brainflow` | PyPI | `pip3 install brainflow` | YES — universal2 wheel includes both x86_64 + arm64 dylib slices (libBoardController.dylib confirmed Mach-O universal binary 2026-05-01) |
| `pyxdf` | PyPI | `pip3 install pyxdf` | available |
| `numpy` | PyPI | `pip3 install numpy` | YES (2.4.3 detected) |
| LabRecorder.app | https://github.com/labstreaminglayer/App-LabRecorder/releases | manual `.dmg` install | NOT pre-installed; user-side blocker #2 |
| GazeCloudAPI | https://api.gazerecorder.com/ | browser script tag (no install); free signup may be required for higher rate-limits | user-side blocker #1 (we did NOT sign up) |
| OpenBCI GUI (optional) | https://openbci.com/downloads | only needed for impedance check; BrainFlow does the streaming | optional |

---

## 4. Time-Sync Protocol (LSL = Lab Streaming Layer)

Three streams converge on the LSL clock:

| Stream | Source | Rate | Latency to LSL clock |
|---|---|---|---|
| `BolyMarkers` | `lsl_marker_relay.py` (HTTP <- browser) | irregular (markers ~0.1–30 Hz) | ~3–10 ms HTTP roundtrip; bridge timestamp captured at `local_clock()` at receipt; browser `performance.timeOrigin+now()` carried in payload for retroactive lag estimate |
| `OpenBCI_EEG` | `openbci_lsl.py` (BrainFlow chunk push) | 125 Hz (Cyton+Daisy interlace) | sub-ms (in-process) |
| Gaze (carried as marker) | GazeCloudAPI `OnResult` callback | 30 Hz | dominant: ~30–60 ms cloud roundtrip per fallback verdict |

End-to-end gaze ↔ EEG sync:

```
gaze ----30Hz---> browser ----HTTP----> relay ----LSL----+
                                                          |
OpenBCI ----BrainFlow----> openbci_lsl.py ----LSL----+    +--> LabRecorder XDF
                                                     |
LabRecorder writes both with shared LSL local_clock --+
```

Worst-case net jitter on a gaze sample: **45 ms** (GazeCloudAPI cloud) + **<10 ms** (HTTP relay) = **<55 ms** vs EEG. OKN slow-phase has a ~1 Hz native frequency, so 55 ms = 5 % of a cycle — well within decoder tolerance.

Falsifier F-N21E-1 watches for drift > 100 ms within session.

---

## 5. Daily Session Protocol (User-Readable)

### Once per pilot (one-time setup, ~30 min)
1. `pip3 install pylsl brainflow pyxdf numpy`
2. Download + install LabRecorder.app
3. Sign up at https://api.gazerecorder.com/ (free non-commercial)
4. Run smoke test:
   ```
   python3 ~/n21_boly_kit/openbci_lsl.py --board synthetic --duration 10
   python3 ~/n21_boly_kit/analyze_session.py --synthetic
   ```
   Expect `pass_75pct: true` (verified 2026-05-01: synthetic decoder = 6/6 = 100 %).

### Each day (60 min sessions × 3 = 180 min stimulus per day, ~225 min wall-clock)
1. Apply OpenBCI cap, gel/saline electrodes — target ≤10 min, impedance <30 kΩ on ≥12/16 ch
2. `bash ~/n21_boly_kit/daily_runner.sh`
3. Open LabRecorder, click Update, verify both streams visible, set save path, click Start
4. In browser: click CALIBRATE (9-point), then START
5. View rotating Necker cube; press **F** when front-face dominant, **B** when back-face dominant
6. Follow runner's countdown (it prints next-event timer)
7. After 60 min: stop LabRecorder, Ctrl-C runner, repeat ×3 across the day with ≥1 h breaks
8. End of day:
   ```
   python3 ~/n21_boly_kit/analyze_session.py recordings/dayN_session_M.xdf \
       --out recordings/dayN_session_M.metrics.json
   ```

User-time/day = ~225 min (3 × 75 min including setup) ≈ **3 h 45 min/day for 7 days**.

---

## 6. Pre-Flight Self-Test (Phase 3) Results

| Check | Result | Evidence |
|---|---|---|
| GazeCloudAPI signup link reachable | UNVERIFIED (we did not sign up) | URL shape `https://api.gazerecorder.com/GazeCloudAPI.js` referenced in WebGazer fallback verdict §6 |
| `pylsl` Mac arm64 wheel | PASS | `pylsl-1.18.2-py2.py3-none-macosx_11_0_universal2.whl` downloaded clean |
| `brainflow` Mac arm64 wheel | PASS | `brainflow-5.21.0-py3-none-any.whl` (30 MB) ships native dylibs, `libBoardController.dylib` = Mach-O universal binary [x86_64 + arm64], `libonnxruntime_arm64.dylib` present |
| Synthetic dry-run of `analyze_session.py` | PASS | 6 reports, 6 detected, 6 hits, 0 false-pos, accuracy = 1.0, `pass_75pct = true` |
| End-to-end pipeline (synth gaze → decoder) | PASS | see above |
| Real gaze + real EEG capture | NOT-RUN | hardware in user's possession, $0 budget excludes our running it |

---

## 7. Pilot Scaling Spec (Phase 4)

| Stage | N | Target | Decision rule |
|---|---|---|---|
| **N=1 (user self)** | 1 | accuracy ≥ 75 % across ≥21 sessions | If pass → recruit N=5; if fail → escalate |
| **N=5** | +4 volunteers | accuracy ≥ 75 % median, ≥3/5 individuals | Web-based + non-invasive OpenBCI = IRB-light (institutional consent form, no medical procedure) |
| **Escalation if N=1 fails** | — | — | Either (a) buy Pupil Core $2–3 k as cited in fallback verdict §3, or (b) redesign protocol (e.g., switch to overt-only paradigm) |

If **N=5 hits ≥75 %**, this becomes the public-facing N-21 reproduction. If only N=1 succeeds and N=5 fails, the pilot is reported as a single-subject case study with explicit Limitations.

---

## 8. Pre-Registered raw#71 Falsifiers (5)

| ID | Falsifier | Threshold | Detection |
|---|---|---|---|
| **F-N21E-1** | Gaze ↔ EEG sync drift exceeds 100 ms within a single session | drift > 100 ms | `analyze_session.py` computes browser→LSL lag from marker payload `browser_ts` vs `server_lsl`; flag if max-min > 0.1 |
| **F-N21E-2** | Webcam framerate drops below 25 Hz under typical room lighting | mean fps < 25 over any 5-min stretch | `bistable.html` writes `gaze;...;state=...` markers — count per second offline |
| **F-N21E-3** | OKN decoder accuracy < 60 % on synthetic test | acc < 0.60 | If `analyze_session.py --synthetic` ever returns `decoder.accuracy < 0.60`, pipeline is broken |
| **F-N21E-4** | OpenBCI signal quality fails wear test (impedance > 30 kΩ on >4 channels) | >4 / 16 channels bad | OpenBCI GUI impedance check during setup; abort day if fails |
| **F-N21E-5** | GazeCloudAPI non-commercial license blocks our research use (paywall, rate-limit, ToS exclusion) | any blocking ToS clause | Manual review of GazeCloudAPI ToS at signup; if blocked, must escalate to (a) WebGazer.js (FAILs OKN spec), (b) Pupil Core $2–3 k, or (c) switch to GazeRecorder local SDK Windows-only |

---

## 9. Off-Repo Kit Files

| Path | Bytes | Role |
|---|---|---|
| `~/n21_boly_kit/bistable.html` | ~7.4 KB | Necker cube + GazeCloudAPI + LSL marker emit |
| `~/n21_boly_kit/lsl_marker_relay.py` | ~3.5 KB | HTTP→LSL bridge (browser cannot push LSL directly) |
| `~/n21_boly_kit/openbci_lsl.py` | ~4.1 KB | BrainFlow→LSL bridge (Cyton+Daisy 16-ch, 125 Hz) |
| `~/n21_boly_kit/analyze_session.py` | ~10 KB | XDF reader + OKN decoder + accuracy score (synthetic & real) |
| `~/n21_boly_kit/daily_runner.sh` | ~2.8 KB | One-shot launcher, 60-min countdown |
| `~/n21_boly_kit/README.md` | ~3.5 KB | User-facing daily protocol |

---

## 10. Top 3 User-Side Blockers

1. **GazeCloudAPI signup** — free non-commercial; user must visit https://api.gazerecorder.com/ once. If their ToS for our use-case is unclear, falsifier F-N21E-5 fires (escalation cost: $2–3 k Pupil Core).
2. **LabRecorder.app install** — separate `.dmg` download; not pip-installable. Single-click install but it is a manual step.
3. **Electrode prep** — Cyton+Daisy 16-channel saline application takes 8–12 min the first time. Skin oils + hair = high impedance on temporal channels; raw#71 F-N21E-4 catches this.

---

## 11. ETA

| Milestone | When | Notes |
|---|---|---|
| Kit ready | NOW (2026-05-01) | spec + 5 source files + README all written; synthetic dry-run PASS |
| First-day pilot start | T+1 day after user installs LabRecorder + signs up for GazeCloudAPI | both are 5-min user actions |
| Day 1 of 7 | T+1 to T+1+1d | 75 min wall-clock |
| Day 7 (final session) | T+8 d | total ~26 h user time across 7 days |
| Decoder analysis | T+8 d (same evening) | per-session JSON metrics rolled up |
| Verdict (N=1 ≥75 % decision) | T+8 d | gates expansion to N=5 |

Worst-case escalation (Pupil Core purchase + ramp): T+8 d failure → +14 d hardware procurement → +7 d new pilot = **T+29 d** if everything fails.

---

## 12. Honest C3

* Necker cube ≠ binocular plaid; perceptual switch dynamics differ in detail. Decoder accuracy is *not* directly comparable to Boly's 88 %.
* Webcam OKN is 5–13 pp below research-grade per fallback verdict §4.
* GazeCloudAPI is closed-source; reproducibility risk for external groups (mitigated by also documenting WebGazer.js path even though it FAILed our spec — others can re-derive).
* `make_synthetic()` in the analyzer encodes idealized OKN; real human OKN has irregular intervals, fixational microsaccades, and head-roll noise. Synthetic dry-run PASS does not guarantee real-data PASS.
* No hardware was tested by this agent; verification limited to wheel + dylib architecture inspection.

---

## Sources
- Predecessor verdict: `docs/n_substrate_n21_boly_webcam_fallback_2026_05_01.md`
- BrainFlow 5.21.0: https://pypi.org/project/brainflow/
- pylsl 1.18.2: https://pypi.org/project/pylsl/
- LabRecorder: https://github.com/labstreaminglayer/App-LabRecorder
- GazeCloudAPI: https://api.gazerecorder.com/
- Necker-cube OKN coupling: Frassle et al. 2014 (J Neurosci 34:1738), Naber et al. 2011 (J Vis 11:6)
- LSL primer: https://labstreaminglayer.org/
