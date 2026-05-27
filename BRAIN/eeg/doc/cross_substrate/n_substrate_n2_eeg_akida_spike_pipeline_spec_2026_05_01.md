# N-substrate N-2 prep — EEG → AKIDA AKD1000 spike-event conversion pipeline spec

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-01
- **Agent**: N-2 prep (sibling of 13 in N-substrate batch)
- **Mission**: D+0 (AKIDA dev kit arrival day) plug-and-play EEG → spike encoder spec + hexa skeleton
- **Race isolation**: writes ONLY to `docs/n_substrate_n2_eeg_akida_spike_pipeline_spec_2026_05_01.md` + `state/n_substrate_n2_prep_2026_05_01/*.json`
- **Tier_1 target**: T1-A1 EEG spike → AKD1000 직결 (float→spike 5x latency 제거)
- **Sister docs**: `docs/akida_dev_kit_evaluation_2026-04-29.md`, `docs/akida_session_friendly_report_2026-04-29.md`

---

## 0. TL;DR (D+0 quick start)

1. Akida AKD1000 inference path accepts **dense `np.uint8` 4-D NHWC tensors** via `model.forward(inputs)` — *not* a sparse / AER spike list at the API surface.
2. "Spike-native" EEG encoding therefore happens **before** the chip: per-channel **Asynchronous Delta Modulation (ADM) / level-crossing** converts each EEG channel into UP/DOWN events, which are then **rasterized into a dense uint8 tensor of shape `(N, T_bin, C, P)`** (P=2 polarities) at a fixed bin width `Δt_bin`.
3. T1-A1 "5× latency" claim = *encoder-side* latency reduction (no float MAC in front-end), not chip API change.
4. Honest C3: §7 lists which SDK details are verified vs guessed.

---

## 1. AKIDA AKD1000 input format — verified facts

### 1.1 API surface (verified, BrainChip MetaTF docs)

| Field | Value | Source |
|---|---|---|
| `akida.Model.forward(inputs)` | `inputs: np.ndarray, dtype=np.uint8`, returns `np.ndarray` | `doc.brainchipinc.com/api_reference/akida_apis.html` |
| `akida.Model.predict(inputs)` | same dtype contract | same |
| Tensor rank | 4-D `(N, H, W, C)` — NHWC only, channel-last | Akida user guide |
| Bit precision | 1 / 2 / 4 / 8 bit, encoded inside uint8 (max value 1, 3, 15, 255) | Akida API ref |
| Sparse / AER input | **NOT** exposed at `Model.forward`. Spikes are an internal computation primitive | Akida API ref (no sparse mention) |
| Toolchain | `quantizeml` (TF/Keras or ONNX → quantized) → `cnn2snn` (quantized → SNN) → `akida.Model` | MetaTF page |
| Temporal layers (Akida v2) | `BufferTempConv`, `StatefulRecurrent` operate on 4-D dense tensors | Akida API ref |

### 1.2 What "spike-event" means on AKD1000

Akida AKD1000 is event-driven *internally*: each layer fires only when the neuron's membrane potential crosses threshold, and only non-zero activations propagate. The user-facing API hides this — it accepts dense uint8 tensors and converts them to internal spike representations via the input layer (described as Rank-Order-Coding in the open-neuromorphic.org overview).

Implication for EEG: we do **not** stream AER tuples `(t, channel, polarity)` to the chip. Instead we **rasterize** ADM-encoded events into a small dense uint8 tensor per inference window.

---

## 2. EEG → spike encoder specification

### 2.1 Pipeline stages

```
                    ┌──────────────────────────────────────────────┐
EEG hardware (16ch) │ stage A:  acquire (BDF/EDF/FIF live stream)  │
  fs ∈ {125, 250,   │ stage B:  preprocess (bandpass 1-45Hz, notch)│
        500} Hz     │ stage C:  per-channel z-score (sliding 10s)  │
                    │ stage D:  per-channel ADM level-crossing     │
                    │           → events (t, ch, polarity)         │
                    │ stage E:  rasterize into 4-D uint8 tensor    │
                    │           shape (1, T_bin, C, 2)             │
                    │ stage F:  akida.Model.forward(tensor)        │
                    └──────────────────────────────────────────────┘
```

### 2.2 Stage D — ADM / level-crossing encoder (core)

**Algorithm** (per channel, asynchronous):

```
init:  v_ref ← x[0]                  # last reference voltage
       refractory_until ← -inf
       events ← []

for sample t in 1..T:
    if t < refractory_until: continue
    Δ ← x[t] - v_ref
    if Δ ≥ +θ_up:
        events.append( (t, ch, +1) )    # UP spike
        v_ref ← v_ref + θ_up
        refractory_until ← t + r_steps
    elif Δ ≤ -θ_dn:
        events.append( (t, ch, -1) )    # DOWN spike
        v_ref ← v_ref - θ_dn
        refractory_until ← t + r_steps
```

### 2.3 Recommended parameters (16ch scalp EEG, fs=250Hz)

| Param | Symbol | Recommended | Rationale |
|---|---|---|---|
| Bandpass | — | 1–45 Hz, 4th-order Butterworth | EEG standard, removes DC + line noise |
| Notch | — | 60Hz (US) / 50Hz (EU) | mains rejection |
| Z-score window | `w_z` | 10 s sliding | per-channel amplitude normalization, σ tracks slow drift |
| UP threshold | `θ_up` | 0.5 σ (z-score units) | matches Corradi et al. 2025 ADM-EEG seizure work |
| DOWN threshold | `θ_dn` | 0.5 σ | symmetric default; bias asymmetry as v2 ablation |
| Refractory | `r` | 4 ms (= 1 sample @ 250Hz) | prevents bouncing on quantization noise |
| Bin width | `Δt_bin` | 8 ms (= 2 samples @ 250Hz) | gives T_bin=125 for 1s window — fits Akida small-tensor target |
| Window length | `T_win` | 1.0 s | matches anima_eeg V_phen_GWT block |
| Max spike count per (bin, ch, pol) cell | `S_cap` | 15 (4-bit) | aligns with Akida 4-bit input precision |

### 2.4 Stage E — rasterization to dense uint8 tensor

Tensor shape decision: **`(N=1, H=T_bin, W=C, channels=2)`**.

- `H` axis = time bins (slow time, T_bin=125 for 1s @ 8ms bins)
- `W` axis = EEG channels (C=16)
- `channels` axis = polarity (0=DOWN, 1=UP)
- dtype = `np.uint8`, values clipped to [0, 15] (4-bit precision)

Rationale: keeps NHWC layout, lets a `Conv2D` first layer learn a per-channel × per-time-bin spatial filter that mirrors a SNN's spatiotemporal receptive field.

Alternative (Akida v2 `BufferTempConv`): shape `(N=1, 1, C=16, 2)` per Δt_bin, streamed bin-by-bin via stateful inference. Defer to v2 ablation.

---

## 3. Hexa skeleton (placeholder for D+0)

File: `tool/anima_eeg_to_akida_spike.hexa` (skeleton committed per HEXA-only repo policy — full inference path lives pod-side / RPi5-side per `feedback_hexa_first_no_py.md`).

The skeleton defines:
- ABORT_NO_AKIDA stub if `akida` python package not installed (D+0 install: `pip install akida quantizeml cnn2snn`)
- ABORT_NO_MNE stub (same pattern as `tool/an11_b_eeg_ingest.hexa`)
- `--selftest` mode emits 16ch synthetic EEG → ADM → raster → integrity check JSON
- `--input <path.fif>` mode for live EEG once recorded
- output schema `anima/eeg_akida_spike_raster/1`

The full SDK call (`model.forward`) is left as a TODO marker — must be exercised on real RPi5+AKD1000 hardware (currently in shipping).

---

## 4. Synthetic dry-run protocol (D-X today)

### 4.1 Synthetic EEG generator

```
fs           = 250 Hz
duration     = 60 s
n_channels   = 16   (10-20 system: Fp1/Fp2/F3/F4/C3/C4/P3/P4/O1/O2/F7/F8/T3/T4/T5/T6)
signal model = α band 10Hz sin + β 20Hz sin + 1/f^1 pink noise + occasional
               5% amplitude burst on random channel pair (mimic eye blink / muscle artifact)
seed         = 20260501  (deterministic for hash chain)
```

### 4.2 Integrity gates

| Gate ID | Check | PASS criterion |
|---|---|---|
| G-D1 | total event count > 0 on every channel | min(events_per_ch) ≥ 50 |
| G-D2 | UP/DOWN balance within ±25% | 0.75 ≤ Σup/Σdn ≤ 1.33 per ch |
| G-D3 | refractory respected | min Δt between consecutive events on same ch ≥ r_steps |
| G-D4 | rasterized tensor dtype/shape | dtype==uint8, shape==(1, T_bin, 16, 2), max≤15 |
| G-D5 | round-trip reconstruction | reconstructed signal vs original Pearson r ≥ 0.85 (Corradi 2025 ADM ref) |
| G-D6 | event-rate vs signal-power monotonicity | Spearman ρ(rate, RMS) ≥ 0.6 across channels |

All 6 gates run inside `--selftest` mode; output → `state/n_substrate_n2_prep_2026_05_01/dryrun_YYYYMMDDTHHMMSSZ.json`.

### 4.3 Falsifier preregistration (T1-A1 chain)

This dry-run is the **encoder-side falsifier**. A separate D+0 hardware falsifier (F-A1) compares:
- baseline: float32 EEG → Conv2D-ANN on RPi5 CPU → time-to-decision
- proposed: ADM uint8 raster → Akida `model.forward` → time-to-decision

T1-A1 5× latency claim PASS criterion: `t_baseline / t_akida ≥ 5.0` median over 100 windows.

---

## 5. State JSON inventory (this prep cycle)

| File | Purpose |
|---|---|
| `state/n_substrate_n2_prep_2026_05_01/spec_manifest.json` | spec doc hash, encoder param table, gate list |
| `state/n_substrate_n2_prep_2026_05_01/falsifier_F_A1_preregister.json` | 5× latency falsifier preregistration |
| `state/n_substrate_n2_prep_2026_05_01/dryrun_pending.json` | placeholder for D-X selftest output (filled when `tool/anima_eeg_to_akida_spike.hexa --selftest` runs) |

---

## 6. D+0 deployment plan (plug-and-play)

```
Day 0 (Akida arrival):
  ── unbox RPi5 + AKD1000 M.2 card
  ── flash RPi OS 64-bit, enable PCIe gen2 in /boot/config.txt
  ── pip install akida quantizeml cnn2snn  (vendor wheel, ARM64)
  ── git clone anima → cd anima
  ── hexa run tool/anima_eeg_to_akida_spike.hexa --selftest
       → expect 6/6 G-D gates PASS
       → emit state/n_substrate_n2_prep_2026_05_01/dryrun_<ts>.json

Day 0+ε:
  ── pair Muse 2 / OpenBCI via Bluetooth or USB
  ── hexa run tool/anima_eeg_to_akida_spike.hexa --input live --duration 60
       → emit raster + first akida.Model.forward call
       → measure t_akida vs t_cpu → F-A1 falsifier graduation candidate
```

---

## 7. Honest C3 — verified vs guessed (raw 91 mandate)

### 7.1 VERIFIED (from official BrainChip docs / first-party sources)

- `akida.Model.forward()` signature: `(inputs: np.ndarray dtype=np.uint8, batch_size: int=0) → np.ndarray`
- Input tensor: 4-D NHWC, dtype uint8, encoded at 1/2/4/8 bit (max 1/3/15/255)
- No sparse / AER input at the public API
- MetaTF toolchain order: `quantizeml` → `cnn2snn` → `akida` runtime
- Akida v2 has `BufferTempConv` and `StatefulRecurrent` for temporal models
- Pip install path: `pip install akida quantizeml cnn2snn` from PyPI

### 7.2 GUESSED / DEFAULT-CHOSEN (require D+0 verification)

- **AKD1000 generation supports v2 stateful layers**: gen-1 silicon is v1; v2 may be CNN2SNN-emulated only. Verify on real hardware.
- **ARM64 wheel availability for RPi5**: BrainChip historically ships x86_64 wheels primarily; RPi5 ARM64 path needs sanity check on D+0. Fallback = build from source on RPi5 or run encoder-only on RPi5 + offload model.forward to dev kit USB host.
- **Optimal `θ_up = 0.5 σ`**: extrapolated from Corradi et al. 2025 (Nature Sci Rep, mixed-signal neuromorphic seizure detection) and Sharifshazileh et al. 2022 (Sci Rep, scalp EEG HFO detection). EEG-task-specific ablation needed.
- **`Δt_bin = 8 ms`**: chosen to keep T_bin=125 manageable. Tighter bins (1-2 ms) preserve more timing info but inflate tensor — depends on Akida memory budget per layer.
- **4-bit input precision (S_cap=15)**: chosen for Akida-friendliness; needs A/B vs 8-bit (S_cap=255).
- **Refractory = 1 sample (4ms @ 250Hz)**: minimal — biological neurons use 1-2ms absolute refractory; default kept loose.
- **5× latency claim (T1-A1)**: theoretical, based on float-MAC vs uint8-event sparsity. Real measurement is the F-A1 falsifier outcome, not a guarantee.
- **Round-trip reconstruction r ≥ 0.85**: typical ADM literature value; not measured on anima EEG corpora yet.
- **MNE-Python on RPi5 ARM64**: assumed installable via pip; conda may be required.
- **EEG-Akida pipeline preserves V_phen_GWT discriminability**: NOT verified. T1-A2 cross-substrate Φ correlation (r ≥ 0.85 between GPU-Φ and Akida-Φ) is a separate falsifier.

### 7.3 OUT OF SCOPE for this prep doc

- Training a quantized model on EEG (deferred to T1-A4 paper §10 cycle)
- BrainChip support questions (FAQ — does Meta TF accept arbitrary 16-dim Φ vector backbone)
- Multi-chip / multi-AKD1000 scaling (single-chip dev kit only)
- FinalSpark organoid cross-comparison (T1-A26, separate sister)

---

## 8. Cross-link

- `docs/akida_dev_kit_evaluation_2026-04-29.md` — Akida eval doc (T1-A1 entry source)
- `docs/akida_session_friendly_report_2026-04-29.md` — friendly report (D+0 timeline)
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` — N-batch master roadmap
- `tool/an11_b_eeg_ingest.hexa` — sister EEG ingest pattern (helper-Python emit, MNE optional)
- `state/cyborg_eeg_audit/` — existing 16ch token data for D+0 instant replay
- raw 91 honest C3 (verified vs guessed split)
- raw 9 hexa-only (skeleton tool, .py blocked)
- raw 131 thermodynamic Landauer bound (energy-per-spike future anchor)

---

## 9. Word count / spec stats

- Word count: ~1,750 (this doc)
- Verified facts: 6 hard facts about Akida API
- Guessed parameters: 10 (all flagged in §7.2)
- Synthetic gates: 6 (G-D1 through G-D6)
- Falsifier preregistered: F-A1 (5× latency, hardware D+0)
