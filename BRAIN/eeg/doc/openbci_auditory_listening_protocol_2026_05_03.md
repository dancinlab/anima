# OpenBCI 16ch Auditory Listening Capture Protocol — 2026-05-03

> sister respect: anima-eeg cycle parallel; this doc is spec-only, no code commit
> commit: NONE (per user directive)
>
> READ-ONLY upstreams:
>   - `anima-eeg/protocols/mu_rhythm.hexa` (block-design pattern)
>   - `anima-eeg/protocol/p300_auditory_oddball.hexa` (audio cue + helper pattern)
>   - `anima-eeg/lsl_capture.hexa` (LSL inlet + meta sidecar)
>   - `anima-eeg/protocols/berger_session_audio.hexa` (say-cue + collect.hexa wrapper)
>   - `tool/anima_phi_v3_canonical.hexa` (Φ★ formula SSOT)
>   - `docs/slm_phase3_spec_2026_05_03.md` (P3.C1 — TRF auditory ROI; r ≥ 0.15 floor)
>   - `docs/slm_p3_capsubset_landed_2026_05_03.ai.md` (synth-fixture lag/channel reference)
>   - `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` (Φ★_EEG proxy spec)

---

## TL;DR

OpenBCI 16ch Cyton+Daisy auditory listening paradigm — 5-10 min naturalistic
audio-book / podcast stimulus, LSL streaming, sentence/word-onset trigger
markers, real-time Φ proxy stream (200 ms windows, sample-partition
log|Cov| matching `anima_phi_v3_canonical`). Falsifier
**F-EEG-AUDITORY-1: bronze-tier Pearson r ≥ 0.10** between speech envelope and
auditory ROI EEG (T7/T8/P7/P8) at fixed-lag 100 ms. Replaces ZuCo silent-reading
baseline (SLM C1 FAIL r=0.030 ≪ 0.15) with the modality-matched protocol the
ROI was designed for.

This document is **specification + script skeleton only**. No actual capture
executed (need physical hardware + user-on-head). No commit.

---

## §1 Paradigm design rationale (vs ZuCo silent-reading mismatch)

### §1.1 Why ZuCo failed at C1

ZuCo 1.0/2.0 corpus is **silent natural reading** (eye-tracking + EEG fixation-
locked windows on Wikipedia / movie reviews). The auditory ROI we tested
(T7/T8/P7/P8 — bilateral superior temporal gyrus / supramarginal) is **not
preferentially recruited** by silent reading; visual word-form area (VWFA,
left fusiform near T5/PO7) and inferior frontal cortex carry the bulk of the
silent-reading signal. Pearson r=0.030 against a speech-envelope-style proxy
therefore reflects **paradigm/ROI mismatch**, not Φ★ failure.

The auditory ROI was selected on the design assumption of **continuous
narrative listening** (Brennan-Hale 2019 N=49 audiobook reference, Crosse 2016
mTRF baseline). Under that paradigm, T7/T8/P7/P8 carry well-documented
speech-tracking signal at 60-500 ms TRF lags with literature r ≈ 0.10-0.30
range (single-subject; Crosse 2016 tab. 2; Brennan-Hale 2019 fig. 3).

### §1.2 What this paradigm provides

| design knob          | choice                                          | rationale                                    |
|----------------------|-------------------------------------------------|----------------------------------------------|
| stimulus modality    | natural speech audio (audiobook / podcast)      | activates T7/T8/P7/P8 by design              |
| duration             | 5-10 min single block, no condition switching   | TRF needs ≥ 5 min per Crosse 2016 tab. 1     |
| subject knowledge    | one familiar + one unfamiliar text             | familiarity contrast = optional B-axis hook  |
| trigger markers      | chapter/sentence/content-word onsets            | both stim-locked (P3) and continuous (TRF)   |
| sampling             | 125 Hz (LSL outlet) or 250 Hz (BrainFlow direct)| matches Cyton+Daisy native                   |
| reference            | SRB2 / BIAS earlobe (white/black)               | mu_rhythm.hexa standard                      |

### §1.3 Stimulus spec (frozen)

- **PRIMARY**: LibriSpeech-test-clean random ~7 min concatenated chapter
  (CC-BY 4.0; verified by user beforehand), 16 kHz mono WAV.
- **SECONDARY (familiarity contrast, optional)**: a podcast clip the subject
  has previously heard (user-supplied .wav or .mp3 → afconvert to 16 kHz mono).
- **AVOID**: music (different ROI — Heschl auditory cortex specifically, not
  STG language network) and white noise (no envelope structure → TRF degenerate).

---

## §2 Capture protocol — step-by-step

```
   step  | action                                       | gate/output
   ──────────────────────────────────────────────────────────────────────────────
   0     | dock OpenBCI Cyton+Daisy + UltraCortex Mark  | board powered, dongle in
         | IV; insert dongle; attach earlobe SRB2/BIAS  |
   1     | impedance check (16 ch < 100 kΩ)             | hexa run anima-eeg/
         |                                              | impedance_check.hexa
         |                                              | --check --port <PORT>
         |                                              | → ledger jsonl
   2     | OpenBCI GUI launch; Cyton+Daisy select;      | GUI status = STREAMING
         | Networking widget → LSL outlet "obci_eeg1",  |
         | TimeSeriesFilt; START STREAM                 |
   3     | preflight: LSL stream resolves               | hexa run anima-eeg/
         |                                              | lsl_capture.hexa
         |                                              | --capture --source
         |                                              | obci_eeg1 --seconds 5
         |                                              | → 5s smoke .npy
   4     | run capture wrapper                          | hexa run anima-eeg/
         |                                              | protocols/auditory_
         |                                              | listening_5min.hexa
         |                                              | --run --port <PORT>
         |                                              | --stim <wav>
         |                                              | --duration 300
   5     | wrapper:                                     | (a) write trigger jsonl
         |   (a) say -v Yuna "준비. 5초 후 시작"        | (b) shape (16, samples)
         |   (b) afplay <stim.wav> & ; LSL pull start   |     .npy + .meta.json
         |   (c) trigger inject every sentence boundary | (c) trigger_log.jsonl
         |   (d) wall-clock duration sleep              |     {ts_utc, sample_idx,
         |   (e) terminate; save .npy + sidecar         |     stim_offset_s, type}
   6     | post: real-time φ proxy stream               | state/eeg_recordings/
         |       (200 ms windows, K=8 partitions)       | auditory_listening_<ts>/
         |                                              | phi_stream.jsonl
   7     | quality control gates (§5)                   | qc_report.json
         |                                              | PASS|FAIL
   8     | F-EEG-AUDITORY-1 falsifier                   | falsifier.json
         |                                              | r_envelope_T7P7_lag100ms
         |                                              | ≥ 0.10 → bronze tier PASS
```

### §2.1 Output directory layout

```
state/eeg_recordings/auditory_listening_<utc_ts>/
├── raw.npy                   # (16, n_samples) float32, LSL inlet capture
├── raw.meta.json             # stream_name, channel_count, sample_rate_*, ...
├── stimulus.wav              # exact bytes of audio played (sha256 in meta)
├── trigger_log.jsonl         # {ts_utc, sample_idx, stim_offset_s, type, label}
├── phi_stream.jsonl          # {window_idx, t_start_s, phi_star, k=8 partitions}
├── envelope.npy              # (n_samples,) Hilbert-envelope of stimulus, fs-aligned
├── qc_report.json            # impedance, line-noise, blink, retention
└── falsifier.json            # F-EEG-AUDITORY-1 verdict + per-channel r table
```

### §2.2 Script skeleton


#### Option A — .hexa wrapper (macOS local, recommended)

`anima-eeg/protocols/auditory_listening_5min.hexa`

```
let SCHEMA = "anima-eeg/auditory_listening_5min/1"

let DEFAULT_DURATION_S    = 300        // 5 min (cap; --duration 600 for 10)
let DEFAULT_STIM          = ""         // path to mono 16kHz .wav
let DEFAULT_VOICE         = "Yuna"
let DEFAULT_LSL_SOURCE    = "obci_eeg1"
let DEFAULT_OUTPUT_ROOT   = "state/eeg_recordings"
let DEFAULT_CHANNEL_COUNT = 16
let DEFAULT_SAMPLE_RATE   = 125
let DEFAULT_PHI_WIN_MS    = 200
let DEFAULT_PHI_K_PART    = 8

// pattern mirrors berger_session_audio.hexa run-plan + lsl_capture.hexa subprocess
fn print_run_plan(...)        // pre-flight summary
fn say_cue(voice, text)       // shells out: say -v Yuna '...'
fn play_stim_bg(wav, log)     // shells out: afplay '<wav>' &> '<log>' &
fn lsl_pull_bg(src, sec, out) // delegates anima-eeg/lsl_capture.hexa --capture
fn inject_triggers(...)       // writes trigger_log.jsonl per sentence onset table
fn compute_phi_proxy(npy_path, win_ms, k_part, out_jsonl)
fn evaluate_f_eeg_auditory_1(npy_path, env_npy, lag_ms, roi_chans) -> bool
fn emit_sentinel()            // __EEG_AUDIT_LISTEN__ <PASS|FAIL> r=<float>
```

#### Option B — `.py` on ubu1 only

If real-time Φ proxy must run on ubu1 (BLAS-heavy log-det K=8 loop in 200 ms
budget), ship a single helper:

`anima-eeg/scripts/realtime_phi_proxy.py`
@resolver-bypass(reason="ubu1 numpy + scipy real-time loop; macOS terminal

```
# inputs: --raw <.npy> (16,N) float32 ; --fs <Hz> ; --win-ms 200 ; --k 8
# outputs: phi_stream.jsonl (one row per window) matching anima_phi_v3_canonical
# formula: HID_TRUNC = N//2 = 8 ; sample-partition × K=8 ; min over partitions
```

---

## §3 Auditory ROI mapping for OpenBCI 10-20 (Cyton+Daisy 16ch)

Taken from `anima-eeg/docs/cyton_daisy_wiring_diagram_2026_05_03.md` and
`anima-eeg/docs/full_helmet_health_view_design_2026_04_28.md`. UltraCortex
Mark IV 16-channel default holes (no electrode swap required):

```
            Fp1●  Fp2●                              ← prefrontal (blink monitor)
       F7●  F3●  Fz·  F4●  F8●                      ← frontal (F7/F8 = lat. STG ant.)
   T7●      C3●  Cz·  C4●      T8●                  ← central + temporal (T7/T8 = STG)
       P7●  P3●  Pz●  P4●  P8●                      ← parietal (P7/P8 = lat. parietal,
            O1●  O2●                                       Pz = midline reference)
                                                    ← occipital (μ-immune control)

   SRB2 → A1 (left earlobe, white)                  ← reference
   BIAS → A2 (right earlobe, black)                 ← driven ground
```

### §3.1 Cyton+Daisy channel → 10-20 mapping (canonical)

| board pin | channel idx | 10-20 site | ROI role                          |
|-----------|-------------|------------|-----------------------------------|
| Cyton N1P | 1           | Fp1        | blink artifact monitor            |
| Cyton N2P | 2           | Fp2        | blink artifact monitor            |
| Cyton N3P | 3           | C3         | sensorimotor control (μ-immune)   |
| Cyton N4P | 4           | C4         | sensorimotor control (μ-immune)   |
| Cyton N5P | 5           | P7         | **AUDITORY ROI (left lat. parietal / STG)**  |
| Cyton N6P | 6           | P8         | **AUDITORY ROI (right lat. parietal / STG)** |
| Cyton N7P | 7           | O1         | occipital baseline (visual ctrl)  |
| Cyton N8P | 8           | O2         | occipital baseline (visual ctrl)  |
| Daisy N1P | 9           | F7         | inferior frontal (lang. ant. STG) |
| Daisy N2P | 10          | F8         | inferior frontal (lang. ant. STG) |
| Daisy N3P | 11          | F3         | dlPFC (attention control)         |
| Daisy N4P | 12          | F4         | dlPFC (attention control)         |
| Daisy N5P | 13          | T7         | **AUDITORY ROI (left STG core)**  |
| Daisy N6P | 14          | T8         | **AUDITORY ROI (right STG core)** |
| Daisy N7P | 15          | P3         | parietal (working mem ctrl)       |
| Daisy N8P | 16          | P4         | parietal (working mem ctrl)       |
| —         | (Cz)        | Pz         | midline reference (vertex-adjacent control); **Cz hole left empty if Pz used as midline ROI** |

Note on Pz vs Cz: SLM P3.C1 spec mentions Pz as part of the "auditory dominance"
ROI (`slm_phase3_spec_2026_05_03.md` P3.C2 row). UltraCortex Mark IV default
montage assigns the midline hole to Cz, not Pz. **Choice frozen here**: use
Cz electrode but **report it as midline-control**, not auditory-ROI; the
4-electrode auditory ROI = `{T7, T8, P7, P8}` only. Adding Pz requires a
hole-swap (out of scope for this protocol; documented in `electrode_helper_rich.hexa`).

### §3.2 Auditory ROI definition (frozen pre-registration)

**ROI_AUDITORY = `{T7, T8, P7, P8}` = channels {13, 14, 5, 6}** (1-indexed,
Cyton+Daisy ordering above).

Bilateral STG / lateral parietal → speech envelope tracking (Crosse 2016;
Brennan-Hale 2019; Di Liberto 2015). **No occipital, no frontal, no central**
in primary ROI — those serve as **null-channel control** for F-EEG-AUDITORY-1.

---

## §4 Real-time Φ proxy stream computation

### §4.1 Match to `anima_phi_v3_canonical`

SSOT formula (`tool/anima_phi_v3_canonical.hexa`):

```
   X ∈ R^(N × h_dim)         # N = sample window size, h_dim = top-variance trunc
   Σ = cov(X)                 # h_dim × h_dim covariance
   φ_whole = log|Σ|           # log-determinant of full covariance
   for k in 1..K:             # K random sample-partitions of N rows
       split rows → S_a ∪ S_b
       Σ_a = cov(X[S_a]) ;  Σ_b = cov(X[S_b])
       φ_k = log|Σ_a| + log|Σ_b|
   Φ★ = min_k(φ_whole - φ_k)
```

### §4.2 EEG-side adaptation (200 ms windows, 16 ch)

Match P9 / N3 substrate-bridge convention:

| param      | value                  | rationale                             |
|------------|------------------------|---------------------------------------|
| input X    | R^(N × h_dim)          | N = samples in 200 ms window          |
| N          | 25 @ 125 Hz / 50 @ 250 Hz | wide enough for cov ≻ 0           |
| h_dim      | 16 → top-var trunc 8   | matches `HID_TRUNC = N//2` convention |
| K          | 8                      | matches CLM/N3 fixture                |
| window step| 100 ms                 | 50% overlap, smoother stream          |
| filter     | 1-50 Hz BP + 60 Hz notch | mu_rhythm.hexa frozen chain         |
| output     | one jsonl row per window | {idx, t0_s, phi_star, phi_whole, phi_k_min, k_partitions[8]} |

### §4.3 Stream-mode pipeline

Three viable executions (pick one per cycle):

1. **Offline** — capture finishes → `.venv-eeg/bin/python` post-processing on
   `raw.npy`. Simplest, most robust. **Recommended for first session.**
2. **Near-real-time** — `lsl_capture.hexa` writes `.npy` chunks every 1 s;
   sidecar `realtime_phi_proxy.py` (ubu1) tails the chunk dir and emits
3. **True-real-time** (closed-loop) — direct BrainFlow ingest in
   `closed_loop.hexa`, in-process numpy. Out of scope for this protocol; would
   conflict with OpenBCI GUI single-port owner constraint. Defer to a separate
   cycle if needed.

### §4.4 Optional CLM Φ★ comparison hook

If `state/clm_170m_phi_baseline_*` is present, emit a side-by-side table at
end of run:

```
   {window_idx, t_start_s, phi_eeg_star, phi_clm_star_nearest_match, |Δ|/φ_clm}
```

Pass criterion (lifted from `p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` §3):
`|Φ★_CLM − Φ★_EEG| / Φ★_EEG ≤ 0.30` on ≥ 80% of windows. **Not** the primary
falsifier of this cycle (that's F-EEG-AUDITORY-1 below); this is a probe.

---

## §5 Quality control gates

All gates evaluated post-capture, written to `qc_report.json`, sentinel emitted:

```
   gate              | check                                    | hard threshold
   ──────────────────────────────────────────────────────────────────────────────
   QC1 impedance     | impedance_check.hexa pre-session ledger  | all 16 ch < 100 kΩ
                     | (existing module — anima-eeg/             | (Z >= 100 kΩ on any
                     | impedance_check.hexa)                    | ROI ch → ABORT)
   QC2 line noise    | 50 Hz peak / 8-12 Hz peak ratio          | < 1.5 across ROI
                     | (Welch PSD per channel, 2 s nperseg)     | (KR grid; 60 Hz for US)
   QC3 blink         | Fp1/Fp2 amplitude > 100 µV peaks /min    | < 30 / min
                     | this is heuristic, not proper ICA)       |
   QC4 LSL retention | F_LSL_03 (lsl_capture.hexa) sample ratio | ≥ 0.80
   QC5 stim sync     | trigger_log.jsonl first sample_idx       | within ± 50 ms of
                     | matches afplay launch + lag-correction   | wall-clock cue
   QC6 nan/saturation| any ROI ch with > 1% samples at ±187500  | 0% saturation
                     | µV (24-bit ADC rail) → flag              | required
```

Gate failure → `qc_report.json.verdict = "FAIL"` and falsifier short-circuits
to **NULL** (not FAIL — distinguish hardware fault from biological null).

KR vs US grid: **default 50 Hz notch (Korea grid)**. US users override with
`--notch-hz 60`. Match `mu_rhythm.hexa` precedent (`NOTCH_HZ = 60.0`) **only
if** the session is on a US-grid pod; for the user's local Seoul setup, 50 Hz
is correct.

---

## §6 Pre-registered falsifier — F-EEG-AUDITORY-1 (bronze tier)

```
   id        | F-EEG-AUDITORY-1
   tier      | BRONZE (single-subject N=1, single-session)
   stimulus  | <stim.wav> sha256-locked into trigger_log.jsonl
   metric    | Pearson r between Hilbert-envelope of stim.wav and ROI EEG
             |   amplitude at fixed lag = 100 ms
             |   (Crosse 2016 mTRF: peak typically 60-200 ms, T7/T8/P7/P8)
   ROI       | mean(channels {T7, T8, P7, P8}) — 4-channel z-scored avg
   bandpass  | 1-12 Hz (delta+theta+alpha; speech-tracking band per
             |   Di Liberto 2015 fig. 4)
   pass      | r ≥ 0.10 on the auditory ROI 4-ch mean
             | AND r_aud > 2 × max(r_O1, r_O2, r_C3, r_C4)
             |   (specificity vs occipital/sensorimotor null)
   fail      | r < 0.10 OR aud ≤ 2 × null
   null      | QC1-6 fail short-circuit (hardware fault, not biology)
```

### §6.1 Literature anchor for r ≥ 0.10 floor

| reference                        | corpus / N      | reported r          | ROI                          |
|----------------------------------|-----------------|---------------------|------------------------------|
| Crosse 2016 mTRF tab. 2          | natural speech / N=10 | r ≈ 0.10–0.30  | Fz, Cz, T7, T8 (group avg)   |
| Brennan-Hale 2019 fig. 3         | audiobook / N=49 | r ≈ 0.05–0.20      | bilateral STG (source recon) |
| Di Liberto 2015 fig. 4           | natural speech / N=8 | r ≈ 0.08–0.25  | T7/T8/P7/P8 (sensor space)   |
| SLM P3.C1 mock-fixture (planted)| synthetic       | r = 0.226 (planted)  | T7/T8/P7/P8 (4-ch mean)      |

**Bronze r ≥ 0.10** is the conservative single-subject single-session lower
bound across these references. Silver tier (r ≥ 0.15) matches the SLM Phase 3
spec floor (`slm_phase3_spec_2026_05_03.md` P3.C1). Gold tier (r ≥ 0.20)
matches Crosse 2016 group-average. **This protocol pre-registers bronze
only**; silver/gold left as cycle-exit upgrades if N=3+ sessions accumulate.

### §6.2 Why bronze and not silver

- N=1 single-session noise floor is ~2× group-average (literature). r=0.10 on
  one subject ≈ r=0.15 group average after pooling.
- OpenBCI Cyton 24-bit ADC + dry electrodes (UltraCortex Mark IV) → 1.5-2× SNR
  penalty vs. Brennan-Hale's BioSemi 64-ch wet system. Documented in
  `anima-eeg/docs/cyton_first_real_session_2026_05_03.md`.
  being present.

---

## §7 Hardware setup checklist

Before invoking the wrapper:

- [ ] OpenBCI Cyton+Daisy assembled; battery > 50% (or USB power)
- [ ] UltraCortex Mark IV positioned; chinstrap snug; Cz hole at vertex (50%
      nasion-inion AND 50% earlobe-earlobe per 10-20)
- [ ] All 16 + 2 ear electrodes in their named holes (see §3.1 table)
- [ ] Saline drops on T7/T8/P7/P8 (auditory ROI) + F7/F8 (high-hair sites)
- [ ] SRB2 white wire on left earlobe; BIAS black wire on right earlobe
- [ ] Dongle inserted; serial port matches `/dev/cu.usbserial-DP04WGIQ` (verify
      with `ls /dev/cu.usbserial-*`)
- [ ] OpenBCI GUI launched; Cyton (live, 16ch) selected; **STOP STREAM** before
      Networking widget config (avoid race)
- [ ] Networking widget → LSL → outlet name `obci_eeg1`, type `EEG`, data
      type `TimeSeriesFilt`, channels 16, sample rate 125 → Start LSL
- [ ] OpenBCI GUI **START STREAM** (top-of-window button) — both LSL and GUI
      visualization now live
- [ ] Headphones on subject (over-ear preferred; speakers OK in quiet room).
      Volume calibrated to comfortable level (~65 dB SPL — speech conversational)
- [ ] Stimulus .wav located at `<stim>` path; sha256 recorded
- [ ] Subject seated, eyes open, instructed: "5분 동안 이야기를 자연스럽게
      들어주세요. 중간에 질문은 없어요. 눈은 한 점에 부드럽게 고정."

---


1. **N=1 single-session bronze tier — generalization claim = zero.**
   F-EEG-AUDITORY-1 PASS at r ≥ 0.10 on this protocol verifies that *this user
   on this day with this Mark IV cap* shows speech-envelope tracking in the
   pre-registered ROI. It says **nothing** about (a) other subjects (no IRB,
   N=1 user-research only), (b) cross-session repeatability (need ≥ 3 sessions
   for test-retest r), (c) cross-ROI specificity beyond the 2× null check
   (could be picking up jaw-EMG bleed at T7/T8 — see §8.2 below). Anchor:
   `slm_phase3_spec_2026_05_03.md` C4 explicitly flags N=49 as "absolute
   floor" for LM-training; N=1 here is purely substrate-validation.

2. **OpenBCI GUI ↔ LSL transport ≠ phenomenal-tier closed-loop.**
   here verbatim: LSL adds 5-50 ms transport latency; sample dropout possible
   (F_LSL_03 enforces ≥ 80% retention, not 100%). The Φ proxy stream §4 is
   therefore **near-real-time** (~1 s lag for stream-mode, ~0 s for offline).
   **No claim** that the running Φ★ value is causally driving anything within
   one window — that requires direct BrainFlow ingest + closed-loop.hexa, out
   of scope. Also: T7/T8 are **immediately above the temporalis muscle** —
   jaw clench / lip movement during silent listening contaminates the auditory
   ROI with EMG broadband power. `anima-eeg/protocols/jaw_clench_emg_v2_8ch.hexa`
   F_JAW_01/03 documents this exact bleed. Subject must keep jaw relaxed; if
   subvocalizing the audiobook content, **F-EEG-AUDITORY-1 r elevation may
   be EMG, not neural speech tracking**. Mitigation: post-hoc check that
   60-100 Hz power in T7/T8 stays within 1 SD of pre-stim baseline.

3. **Φ★ proxy on EEG ≠ Φ★ on CLM hidden-state — substrate-bridge claim is
   correlational only, not identical.** The `anima_phi_v3_canonical` formula
   is representation-level invariant (same math runs on CLM hidden states,
   organoid spike-rates, EEG channel covariance). But the *units and
   interpretation* differ: CLM φ★ is computed on `R^(N=16 prompts × h_dim=128)`
   discrete forward-pass states; EEG φ★ here is `R^(N=25-50 samples × 8 trunc
   ch)` continuous time-series covariance. **Same algorithm, different
   distribution**. The §4.4 cross-substrate comparison (|Δ|/φ ≤ 0.30 from
   p9_paradigm_b spec) is the falsifier for substrate-equivalence — and it is
   a probe in this cycle, **not** the primary falsifier. Treat phi_stream.jsonl
   as a within-session feature, not a cross-substrate identity claim, until
   the §4.4 probe accumulates ≥ 80% pass rate across multiple sessions.

---

## §9 Outputs from this cycle

- **THIS DOC**: `docs/openbci_auditory_listening_protocol_2026_05_03.md`
  (spec + script skeleton + falsifier registration)
- **NOT WRITTEN this cycle** (deferred to actual capture cycle):
  - `anima-eeg/protocols/auditory_listening_5min.hexa` (script)
  - `anima-eeg/scripts/realtime_phi_proxy.py` (ubu1 helper)
  - `state/eeg_recordings/auditory_listening_<ts>/...` (capture artifacts)
- **NO COMMIT** per user directive
- **NO HARDWARE INVOCATION** — needs physical session

Next cycle entry trigger: user reports "ready to capture" + impedance
ledger shows ROI channels < 100 kΩ in a recent (< 24 h) impedance_check ledger
entry.
