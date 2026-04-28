# Sleep tracking overnight protocol — anima T14 (NREM/REM staging gold standard)

**Date frozen**: 2026-04-28
**Owner**: search5599@proton.me (N=1 first-night pilot, raw#91 honest C3)
**Linked SSOT files**:
- runner: `anima-eeg/tool/sleep_tracker.hexa`
- helper: `/tmp/sleep_staging_helper.py` (transient, raw#37)
- recordings: `state/sleep_recordings/<date>_overnight.npy`
- audit: `state/sleep_audit/<date>_staging.jsonl` (append-only, per-30s epoch)
- raw: 9, 10, 12, 37, 65, 71, 82, 91, own5

---

## 1. Rationale (raw#12 frozen design)

Sleep is the **gold-standard reference** for consciousness measurement (Schartner
2017 SEEG NREM/REM paradoxical Lempel-Ziv). Within-subject overnight EEG provides
**within-night state contrasts** (Wake → N1 → N2 → N3 → REM) that cannot be
obtained from any waking baseline. A single night yields ~480 × 60s segments
(8h) clustered into 5 stages, providing dense LZ76 distribution per stage in
one session.

**Goal**: produce per-stage LZ76 averages (Wake > REM > N1 > N2 > N3 expected
ordering) as N=1 reference distribution. NOT generalized — pilot only.

## 2. Frozen criteria (raw#12)

- **N=1 first night = pilot only** (no generalization, raw#91 honest C3)
- **AASM 30s-epoch standard** (Iber 2007 manual)
- **HMM 5-state hidden states** (Wake / N1 / N2 / N3 / REM)
- LZ76 ordering invariant: `mean(Wake) > mean(REM) > mean(N1) > mean(N2) > mean(N3)`
- Recording duration: 8 hours nominal (22:00 → 06:00)
- Sampling: 125 Hz × 16 ch (Cyton+Daisy native)

## 3. Pre-sleep protocol (21:00–22:00)

1. **Helmet mount**: 16 ch saline-soaked sponges, ear-clip references
2. **Saline reapplication** (8h dry-out mitigation): generous saline at 21:30
   so all 16 channels start GREEN at 22:00 lights-out
3. **Impedance check**: `impedance_check.hexa` real-Z scan, require 16/16 GREEN
   (Z < 50 kΩ, raw#82 darwin-native)
4. **Resting baseline**: 60 min eyes-closed (lights low) — provides Wake
   reference distribution
5. **Mac AC connect**: wall power required (battery insufficient for 8h)
6. **caffeinate -i** background process (prevents Mac display sleep from
   suspending USB; explicit user-launched, not auto)
7. **Final safety check**: user verbally confirms saline tolerance + helmet
   pressure tolerable for 8h (own5 user-safety gate)

## 4. Recording (22:00 → 06:00)

- **Segment**: 60s contiguous, 480 segments per night
- **Sampling**: 125 Hz × 16 ch float32 → ~1.92 MB per segment, ~921 MB per night
  (raw .npy uncompressed; design budget 2.4 GB allows headroom)
- **Continuous**: no gaps; segment boundaries align to wall-clock minute
- **Background process**: `nohup hexa.real run sleep_tracker.hexa --record &`
  (foregrounded user terminal closes — survives via nohup)
- **USB stay-awake**: caffeinate -i prevents kernel USB suspend
- **Battery fallback**: AC required; `pmset -g batt` polled at boot, abort if
  not on AC

## 5. Post-sleep (06:00+)

1. **Final impedance**: drift measurement vs. 21:30 baseline
2. **HMM staging**: 30s-epoch per-channel α/θ/δ/β bandpower → 5-state HMM
   inference (helper Python: scipy + sklearn HMM)
3. **Per-stage LZ76**: average LZ76 per stage from 60s segment to 30s epoch
   alignment (each segment contributes to 2 epochs)
4. **Audit JSONL**: one row per 30s epoch with `{epoch_idx, ts_iso, stage,
   alpha_x1000, theta_x1000, delta_x1000, beta_x1000, eog_movement,
   lz76_x1000, hmm_posterior_x1000}`

## 6. HMM 5-state design (AASM standard)

| State | EEG signature | EOG | LZ76 expected |
|---|---|---|---|
| Wake  | α dominant (eyes closed), low δ | active | 0.70–0.90 |
| N1    | θ dominant, vertex sharp waves   | slow rolling | 0.50–0.70 |
| N2    | spindles 12–14 Hz + K-complexes | minimal | 0.40–0.60 |
| N3    | δ > 75 µV slow waves > 20% epoch | none | 0.20–0.40 |
| REM   | low-amplitude mixed-freq, sawtooth | rapid eye movement | 0.60–0.85 |

**Feature vector** (per 30s epoch, 6 dims):
- α power (8–13 Hz), θ (4–8), δ (0.5–4), β (13–30)
- EOG movement (Fp1–Fp2 differential RMS)
- spindle density (12–14 Hz transient count)

**HMM**: 5 hidden states, Gaussian emissions, transition matrix initialized
from AASM canonical table (e.g. Wake→N1 0.05, N1→N2 0.30, N2→N3 0.10, REM
typically follows N2/N3, etc.). EM convergence required (max 50 iter, tol 1e-3).

## 7. raw#71 — 5+ falsifiers

- **F1 artifact > 30%**: if > 30% of 8h is artifact (helmet slip, RMS rail),
  abort staging — pilot night discarded
- **F2 USB disconnect**: if `pyserial` reports drop > 5s during recording,
  segment marked invalid; if > 10 segments invalid, abort night
- **F3 HMM convergence fail**: if EM does not converge in 50 iter or any
  stage has < 5 epochs, staging marked NON_APPLICABLE
- **F4 single-state collapse**: if any one stage occupies > 90% of epochs,
  staging is degenerate — falsified
- **F5 LZ76 reversed ordering**: if `mean(N3) > mean(Wake)` or any inversion
  in expected `Wake > REM > N1 > N2 > N3` chain, falsified — pilot retracted
  per raw#91 honest C3

## 8. Implementation

- `anima-eeg/tool/sleep_tracker.hexa` (~200 LoC, --selftest synthetic 8h
  5-state HMM simulation, --record live mode dispatches to /tmp helper)
- `/tmp/sleep_staging_helper.py` (scipy bandpower + sklearn-style 5-state
  Gaussian HMM, transient per raw#37)
- launchd plist (raw 99 hive init absorption — DEFERRED to second night;
  first night = nohup foregrounded for monitoring)

## 9. Safety checklist (own5 — user must confirm)

- [ ] Saline allergy: NONE (user confirmed self-history)
- [ ] Helmet 8h pressure: tolerable (test 1h dry-run prior nights — required
      before first overnight)
- [ ] Mac AC connected + power adapter cable secured
- [ ] No critical morning meeting (allows 06:00 wake without alarm bias)
- [ ] Sleeping partner notified (helmet noise/light minimal)
- [ ] Saline bottle on bedside (auto-reapply if wake mid-night)

## 10. Tonight's start command (after safety checklist)

```bash
# 21:00 — helmet mount + saline
$HEXA_LANG/hexa.real run anima-eeg/impedance_check.hexa

# 21:30 — re-saline + 60 min resting baseline
$HEXA_LANG/hexa.real run anima-eeg/eeg_recorder.hexa --duration 3600

# 22:00 — overnight start (8h)
caffeinate -i nohup $HEXA_LANG/hexa.real run \
  anima-eeg/tool/sleep_tracker.hexa --record \
  --duration-sec 28800 \
  --out-dir state/sleep_recordings \
  > state/sleep_audit/$(date +%Y%m%d)_boot.log 2>&1 &
echo $! > state/sleep_audit/sleep_tracker.pid

# 06:00 — post-sleep staging
$HEXA_LANG/hexa.real run anima-eeg/tool/sleep_tracker.hexa --stage \
  --recording state/sleep_recordings/$(date +%Y%m%d)_overnight.npy \
  --audit state/sleep_audit/$(date +%Y%m%d)_staging.jsonl
```

---

**Honesty C3** (raw#91): N=1 first-night pilot — generalisability bounded.
Stage means may differ from population norms; the test of validity is the
**ordering invariant** (F5), not absolute LZ76 values.
