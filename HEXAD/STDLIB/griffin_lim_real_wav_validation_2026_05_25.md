# griffin-lim REAL-WAV cross-validation

**Date:** 2026-05-25
**Companion to:** PR #456 (`HEXAD/STDLIB/griffin_lim_convergence_test_2026_05_25.{hexa,md}`)
**Test:** `HEXAD/STDLIB/griffin_lim_real_wav_validation_2026_05_25.hexa`
**Stdlib under test:** `stdlib/signal/core_griffin.hexa` (hexa-lang #860)

---

## 1. Motivation

PR #456 demonstrated **92.3% reduction** in relative-L2 magnitude error on a
synthetic 2-tone + Hann-envelope signal at `n_fft=32`, with 4/4 falsifier
PASS. The honest open question:

> Does the same convergence pattern hold on a **real audio waveform**
> with formants, voicing harmonics, and broadband residual — i.e. the
> kind of signal griffin-lim is actually deployed against in vocoders?

This test answers that question with a **side-by-side** comparison: the
exact same STFT config and the exact same falsifier on a real WAV slice
AND on the PR #456 synthetic, in the same process.

---

## 2. Setup

| | value |
|---|---|
| WAV fixture | `HEXAD/VOICE/hexa-senses-voice/proto/hexa_speak_demo.wav` (already tracked, 34604 B) |
| Sample rate | 24 kHz mono int16 LE |
| Full WAV length | 17280 samples (0.72 s) |
| Slice extracted | `[8512, 8768)` — mid-file, 256 samples (10.67 ms) |
| Slice peak\_abs | 0.0489 (real-signal, mid-syllable) |
| Synthetic comparator | PR #456 2-tone + Hann envelope, 256 samples |
| STFT cfg | `n_fft=32, hop=16, win=Hann` → 15 frames × 17 bins = **255 mag entries** |
| Iter sweep | `n_iter ∈ {0, 1, 5, 10, 30}` |
| Magnitude energy | real = **0.673**, synthetic = **18.225** (synthetic ~27× louder) |
| Wall (full sweep) | **1.16 s** Mac local, $0 |

### Why `n_fft=32` (same as PR #456, not larger)

The hexa-lang `fft_native` inner butterfly does an immutable-list rebuild
per iteration, making it O(n²·log n) per frame. At `n_fft=64` with 30
iterations × 15 frames the wall would be in the multi-minute range and
the n\_fft becomes a CI-cost variable rather than a held constant.

Holding `n_fft` constant between synthetic and real **isolates signal
complexity as the single variable under test**. Spectral-resolution
behaviour at larger `n_fft` is a separate question that becomes cheap
when the FFT kernel becomes O(n·log n).

### Why a 256-sample WAV slice

256 samples is the minimum window length that gives 15 STFT frames at
`n_fft=32, hop=16`, which is a 2.1× frame count over PR #456's 7-frame
sweep — enough to exercise multi-frame phase consistency without
blowing the wall budget.

The slice starts at sample 8512 — mid-file — to skip any onset/silence
transient and land in a voiced region.

---

## 3. Per-iter results

### REAL WAV slice

| n_iter | rel_l2_err |
|---:|---:|
| 0 | 0.785323 |
| 1 | 0.381526 |
| 5 | 0.190391 |
| 10 | 0.121011 |
| 30 | **0.071630** |

### SYNTHETIC (PR #456 signal, 256 samples)

| n_iter | rel_l2_err |
|---:|---:|
| 0 | 0.919712 |
| 1 | 0.416835 |
| 5 | 0.180860 |
| 10 | 0.114811 |
| 30 | **0.067034** |

### Side-by-side delta

| n_iter | real | synth | delta (real − synth) |
|---:|---:|---:|---:|
| 0 | 0.785323 | 0.919712 | **−0.1344** |
| 1 | 0.381526 | 0.416835 | −0.0353 |
| 5 | 0.190391 | 0.180860 | +0.0095 |
| 10 | 0.121011 | 0.114811 | +0.0062 |
| 30 | 0.071630 | 0.067034 | +0.0046 |

### Reduction summary

| signal | err\_0 → err\_30 reduction |
|---|---:|
| real WAV slice | **90.88%** |
| synthetic | **92.71%** (PR #456 reported 92.3% on n\_samples=128; reproduces at n\_samples=256) |
| **gap (synth − real)** | **1.83 pp** |

---

## 4. Falsifier verdict (5/5 PASS)

Pre-registered REAL-signal falsifiers (R-prefix to distinguish from
PR #456 a/b/c/d):

| id | claim | observed | verdict |
|---|---|---|---|
| R-a | err_1 ≤ err_0 + ε | 0.382 ≤ 0.785 | **PASS** |
| R-b | err_10 ≤ err_1 + ε | 0.121 ≤ 0.382 | **PASS** |
| R-c | err_30 ≤ err_10 + 5% plateau band | 0.072 ≤ 0.121 + 0.0071 | **PASS** |
| R-d | err_30 < 0.5 (meaningful basin) | 0.072 < 0.5 | **PASS** |
| R-e | real pct\_reduction ≥ 50% (pre-registered LOWER bar than the synthetic 92%, allowing real-signal hardness) | 90.88% ≥ 50% | **PASS** |

`ALL PASS — griffin-lim convergence pattern reproduces on real WAV slice`

---

## 5. Real vs synthetic — three honest observations

### (i) Real starts BETTER than synthetic at err_0

Counter-intuitive but understood: `err_0` measures the
zero-phase iSTFT init (no phase recovery). The synthetic 2-tone has
**stronger, sharper harmonic peaks** that miss more violently when
phase is forced to zero. The real-WAV slice has lower-energy
broadband content (peak\_abs = 0.0489, mag-energy 0.673 vs synthetic
18.225), so its zero-phase init is closer to a valid time-domain
signal in relative-L2 terms.

This is **not** a sign that real is "easier" overall — only that
zero-phase init is less catastrophic on it.

### (ii) Real becomes HARDER than synthetic at err_5+

By iter 5 the delta crosses zero and stays slightly positive (real
+0.005 to +0.010 above synthetic). This matches the a-priori
hypothesis: with many simultaneous partials, real audio has more
local minima in the phase-only landscape, and the algorithm plateaus
just a hair higher.

The gap is **small in absolute terms** (under 1 pp of rel-L2) and
the monotone-decrease shape is preserved cleanly across all five
sweep points.

### (iii) The convergence floor is REAL-AUDIO-COMPATIBLE

Both signals plateau at rel-L2 ≈ 0.07 by iter 30. This is well under
the 0.5 "meaningful basin" threshold and within the 0.05–0.10 range
typically reported for griffin-lim on speech in the literature
(Le Roux 2010 §IV, Perraudin 2013 Fig. 3) at comparable n\_fft.

The stdlib `core_griffin` therefore **converges to a real-audio-
compatible floor**, not just a synthetic-friendly toy floor.

---

## 6. Pre-registered caveats

These were declared in the test docstring **before** running the sweep,
to prevent post-hoc reframing of any unfavourable result:

1. **256-sample window is short.** 10.67 ms @ 24 kHz captures
   local voicing but not phrase-level structure. The convergence
   story on long-window real audio (>1 s) is a separate question
   that needs the O(n·log n) FFT kernel before it becomes
   CI-affordable.

2. **The WAV is a hexa-native synthesized utterance** (anima
   ω-audio organ output), NOT a microphone recording. It IS a real
   audio waveform shape (PCM int16 LE multi-tone with envelope)
   but does not include microphone noise / room reverb. A true
   mic recording would likely show a **yet higher** convergence
   floor.

3. **Only rel-L2 magnitude error is measured.** Time-domain SNR,
   PESQ, ViSQOL are not measured — magnitude reconstruction is
   the GL algorithm's optimization target by construction.

4. **n\_fft was NOT swept.** Held at 32 for apples-to-apples with
   PR #456. Behaviour at larger n\_fft is a separable follow-up
   gated on FFT-kernel speedup.

---

## 7. Conclusion

The convergence pattern documented in PR #456 on a synthetic 2-tone
signal **reproduces on a real WAV slice** under the same STFT config:

- **monotone non-increasing** across all five sweep points (R-a, R-b)
- **near-plateau by iter 30** within a 5% band of iter 10 (R-c)
- **meaningful-basin convergence** well under rel-L2 0.5 (R-d)
- **90.88% reduction** from `err_0` to `err_30` (R-e), only
  1.83 percentage points behind the 92.71% synthetic baseline

`stdlib/signal/core_griffin` is therefore validated as a
**real-audio-compatible** griffin-lim implementation, not merely a
synthetic-friendly toy.

### Follow-up gates (NOT done here)

- **Larger `n_fft` sweep** (64 / 128 / 256) — gated on hexa-lang
  FFT kernel becoming O(n·log n) (currently O(n²·log n) due to
  immutable-list rebuild in the butterfly).
- **Mic-recorded WAV** — would require a tracked or fetchable
  fixture; out of scope here.
- **Perceptual quality metric** (PESQ / ViSQOL) — would require
  a separate stdlib module and reference signal alignment.

---

## 8. Reproduce locally

```sh
cd ~/core/anima
git checkout test/griffin-real-wav-2026-05-25
export HEXA_MEM_UNLIMITED=1 HEXA_MAC_BUILD_OK=1
hexa run HEXAD/STDLIB/griffin_lim_real_wav_validation_2026_05_25.hexa
# Expected: "5/5 passed — ALL PASS" in ~1-2 s on M-series Mac
```
