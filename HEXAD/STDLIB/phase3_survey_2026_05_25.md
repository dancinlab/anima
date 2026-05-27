// HEXAD/STDLIB/phase3_survey_2026_05_25.md
// STDLIB 도메인 — anima 전체 codebase primitive survey (3rd milestone)
// 작성: 2026-05-25 · cycle: STDLIB-3
// 입력 SSOT: VOICE/anima-voice/dsp_core.hexa (DSP 도메인 60+ fn, 1769 LoC)
// 목적: hexa-lang stdlib 으로 promote 할 일반 primitive 후보 inventory (phase-3 3 카테고리)

# § 0 — 사전 정보

- Phase-1 survey (2026-05-24): 10 카테고리 × 47 candidate fn (1st + 2nd-wave)
  - 1st-wave 완료 대상: pow2_int, log2, bin_values_minmax, shannon_entropy, mutual_info_pair, abs_f, ... (17 fn)
  - 2nd-wave: wolfram_run_ca, pearson_r, spearman_rho, voss_mccartney, ... (11 fn)
- Phase-2 (예상, not surveyed yet)
- Phase-3 (본 문서): **EEG / signal-processing · clustering / classification · MITOSIS / CHAT domain-general**

# § 1 — survey 방법

- 범위: `/Users/ghost/core/anima/HEXAD/` 산하 전수 검사 + focus VOICE/anima-voice/dsp_core.hexa (신규, 1769 LoC)
- 도구: `grep -rn "fn .*<pattern>"` + hexa-lang stdlib 5 파일 cross-check
- carve-out: dsp_core.hexa 의 60+ fn 은 VOICE 도메인-특정이 아니라 **general signal-processing primitive** → stdlib 후보.
  - MITOSIS/CHAT 의 상수/헬퍼는 도메인-특정으로 판정 → deferred.
- 분석 포인트:
  1. dsp_core.hexa 는 이미 hexa-lang runtime 's' audio library 와 유사한 surface → overlap 가능성
  2. clustering/classification 은 anima 전체에서 **명시적 k-means/distance 구현 부재** → 다른 방식 (statistical distance 또는 similarity 사용)
  3. domain-general 은 CHAT/MITOSIS 의 core 로직이지만 domain-specific constant 혼재.

# § 2 — 카테고리 1: EEG / Signal-Processing

## A. dsp_core.hexa 의 기본 단위 (소단위 primitive)

| fn (canonical)              | 대표 위치                                          | LoC | 일반성 | dup 수 | wave |
|-----------------------------|----------------------------------------------------|----|--------|--------|------|
| `hann_window(n, N)`         | VOICE/dsp_core.hexa:263 (per-sample Hann)          | 3  | ★★★    | 26 (outside dsp_core) | 1st  |
| `hamming_window(n, N)`      | VOICE/dsp_core.hexa:270                            | 3  | ★★★    | ~4 inline | 1st  |
| `blackman_window(n, N)`     | VOICE/dsp_core.hexa:278                            | 5  | ★★★    | 1      | 1st  |
| `window_sample(type,i,N)`   | VOICE/dsp_core.hexa:288 (dispatcher)               | 5  | ★★★    | inline | 1st  |
| `biquad_omega(f, sr)`       | VOICE/dsp_core.hexa:566                            | 2  | ★★★    | 1      | 1st  |
| `biquad_alpha(ω, Q)`        | VOICE/dsp_core.hexa:570                            | 2  | ★★★    | 1      | 1st  |
| `lpf_coeff(f, sr, Q, idx)`  | VOICE/dsp_core.hexa:578 (Audio EQ Cookbook)        | ~12 | ★★★    | 1      | 1st  |
| `hpf_coeff(f, sr, Q, idx)`  | VOICE/dsp_core.hexa:594                            | ~12 | ★★★    | 1      | 1st  |
| `biquad_tick(...)`          | VOICE/dsp_core.hexa:612 (Direct Form I 1-sample)   | 1  | ★★★    | 1      | 1st  |
| `preemphasis_tick(x, prev, c)` | VOICE/dsp_core.hexa:618                         | 1  | ★★★    | 1      | 1st  |
| `deemphasis_tick(...)`      | VOICE/dsp_core.hexa:624 (inverse)                  | 1  | ★★★    | 1      | 1st  |
| `autocorr_accumulate(x,y)`  | VOICE/dsp_core.hexa:675 (lag-τ acc)                | 1  | ★★★    | 2 (h208) | 1st  |
| `pitch_lag_to_hz(lag, sr)`  | VOICE/dsp_core.hexa:683                            | 1  | ★★★    | 0      | 1st  |
| `hz_to_lag(hz, sr)`         | VOICE/dsp_core.hexa:688                            | 1  | ★★★    | 0      | 1st  |
| `pitch_min_lag(sr, max_hz)` | VOICE/dsp_core.hexa:693                            | 1  | ★★★    | 0      | 1st  |
| `pitch_max_lag(sr, min_hz)` | VOICE/dsp_core.hexa:697                            | 1  | ★★★    | 0      | 1st  |
| `parabolic_interp_offset(...)` | VOICE/dsp_core.hexa:705 (sub-sample refinement)    | ~4 | ★★     | 0      | 2nd  |

## B. dsp_core.hexa 의 배열-레벨 (array-interface)

| fn (canonical)              | 대표 위치                                          | LoC | 일반성 | dup 수 | wave |
|-----------------------------|----------------------------------------------------|----|--------|--------|------|
| `dsp_hann_window(n)`        | VOICE/dsp_core.hexa:739 (full array)               | ~8 | ★★★    | 3 (hxcuda_istft + plc) | 1st  |
| `dsp_hamming_window(n)`     | VOICE/dsp_core.hexa:753                            | ~8 | ★★★    | inline | 1st  |
| `dsp_fft(real,imag,n)`      | VOICE/dsp_core.hexa:776 (Cooley-Tukey radix-2)     | ~80 | ★★★ | 1 SSOT | 1st  |
| `dsp_ifft(real,imag,n)`     | VOICE/dsp_core.hexa:862 (conj FFT)                 | ~30 | ★★★    | 1      | 1st  |
| `dsp_stft(...)`             | VOICE/dsp_core.hexa:900 (frame windowing + FFT)    | ~40 | ★★★    | 1 + GPU variant | 1st  |
| `dsp_istft(...)`            | VOICE/dsp_core.hexa:955 (COLA synthesis)           | ~70 | ★★★    | 1 + GPU variant | 1st  |
| `dsp_mel_filterbank(...)`   | VOICE/dsp_core.hexa:1066 (triangular MEL banks)    | ~55 | ★★★    | 0      | 1st  |
| `dsp_spec_to_mel(...)`      | VOICE/dsp_core.hexa:1131 (magnitude → MEL)         | ~15 | ★★★    | 0      | 1st  |
| `dsp_griffin_lim(...)`      | VOICE/dsp_core.hexa:1164 (phase reconstruction)    | ~55 | ★★     | 4 (comments only) | 2nd  |
| `dsp_preemphasis(audio,c)`  | VOICE/dsp_core.hexa:1224                           | ~12 | ★★★    | 0      | 1st  |
| `dsp_pitch_shift(...)`      | VOICE/dsp_core.hexa:1245 (time-stretch + lerp)     | ~30 | ★★★    | 0      | 2nd  |
| `dsp_resample(...)`         | VOICE/dsp_core.hexa:1284 (linear interp)           | ~30 | ★★★    | 0      | 2nd  |

## C. dsp_core.hexa 의 헬퍼 (helper/accessor)

| fn (canonical)              | 대표 위치                                          | LoC | 일반성 | dup 수 | wave |
|-----------------------------|----------------------------------------------------|----|--------|--------|------|
| `bit_reverse(x, bits)`      | VOICE/dsp_core.hexa:402 (FFT bit permutation)      | ~10 | ★★     | 0      | 2nd  |
| `log2_int(n)`               | VOICE/dsp_core.hexa:416 (power-of-2 check)         | ~8 | ★★★    | 0      | 1st  |
| `is_power_of_2(n)`          | VOICE/dsp_core.hexa:428                            | ~8 | ★★★    | 0      | 1st  |
| `butterfly_re_a(...)`       | VOICE/dsp_core.hexa:445-462 (4 butterfly outputs)  | 1 ea | ★★ | 0 (inline) | 2nd  |
| `twiddle_re(k, N)`          | VOICE/dsp_core.hexa:467 (twiddle factor real)      | 1  | ★★     | 0      | 2nd  |
| `twiddle_im(k, N)`          | VOICE/dsp_core.hexa:471 (imaginary)                | 1  | ★★     | 0      | 2nd  |
| `twiddle_inv_re(k, N)`      | VOICE/dsp_core.hexa:477 (inverse)                  | 1  | ★★     | 0      | 2nd  |
| `twiddle_inv_im(k, N)`      | VOICE/dsp_core.hexa:481                            | 1  | ★★     | 0      | 2nd  |
| `magnitude_bin(re, im)`     | VOICE/dsp_core.hexa:487 (√(re²+im²))               | 1  | ★★★    | 0      | 1st  |
| `power_bin(re, im)`         | VOICE/dsp_core.hexa:491 (re²+im²)                  | 1  | ★★★    | 0      | 1st  |
| `fft2_out*`                 | VOICE/dsp_core.hexa:498-501 (N=2 unrolled)         | 1 ea | ★ | 0 | 2nd  |
| `stft_frame_sample(...)`    | VOICE/dsp_core.hexa:507 (windowed sample)          | 1  | ★★★    | 0      | 1st  |
| `stft_num_frames(...)`      | VOICE/dsp_core.hexa:512                            | ~3 | ★★★    | 0      | 1st  |
| `stft_frame_start(...)`     | VOICE/dsp_core.hexa:519                            | 1  | ★★★    | 0      | 1st  |
| `istft_synth_sample(...)`   | VOICE/dsp_core.hexa:527 (windowed IFFT)            | 1  | ★★★    | 0      | 1st  |
| `istft_output_len(...)`     | VOICE/dsp_core.hexa:532                            | ~2 | ★★★    | 0      | 1st  |
| `istft_window_norm(...)`    | VOICE/dsp_core.hexa:538 (COLA norm)                | ~15 | ★★     | 0      | 2nd  |
| `rms_accumulate(sum,x)`     | VOICE/dsp_core.hexa:314 (energy accumulator)       | 1  | ★★★    | 0      | 1st  |
| `rms_finalize(sum, n)`      | VOICE/dsp_core.hexa:318                            | ~3 | ★★★    | 0      | 1st  |
| `zcr_count(prev, curr)`     | VOICE/dsp_core.hexa:326 (zero crossing)            | ~3 | ★★★    | 0      | 1st  |
| `zcr_finalize(count, n)`    | VOICE/dsp_core.hexa:333                            | ~2 | ★★★    | 0      | 1st  |
| `normalize_gain(peak, db)`  | VOICE/dsp_core.hexa:343 (dB normalization)         | ~8 | ★★★    | 0      | 1st  |
| `apply_gain(sample, gain)`  | VOICE/dsp_core.hexa:355                            | 1  | ★★★    | 0      | 1st  |
| `mix(a, b, α)`              | VOICE/dsp_core.hexa:362 (alpha blend)              | 1  | ★★★    | 0      | 1st  |
| `overlap_add_sample(...)`   | VOICE/dsp_core.hexa:372 (OLA 1-sample)             | 1  | ★★★    | 0      | 1st  |
| `overlap_add_hann(...)`     | VOICE/dsp_core.hexa:377 (OLA with Hann)            | ~4 | ★★★    | 0      | 1st  |
| `hz_to_mel(hz)`             | VOICE/dsp_core.hexa:1054 (MEL scale forward)       | ~2 | ★★★    | 0      | 1st  |
| `mel_to_hz(mel)`            | VOICE/dsp_core.hexa:1060 (MEL scale inverse)       | ~2 | ★★★    | 0      | 1st  |
| `upsample_src_index(...)`   | VOICE/dsp_core.hexa:643 (resampling helper)        | 1  | ★★     | 0      | 2nd  |
| `upsample_frac(...)`        | VOICE/dsp_core.hexa:647                            | ~2 | ★★     | 0      | 2nd  |
| `upsample_output_len(...)`  | VOICE/dsp_core.hexa:652                            | 1  | ★★     | 0      | 2nd  |
| `downsample_src_index(...)`| VOICE/dsp_core.hexa:658                            | 1  | ★★     | 0      | 2nd  |
| `downsample_output_len(...)` | VOICE/dsp_core.hexa:662                          | ~3 | ★★     | 0      | 2nd  |
| `linear_to_db(x)`           | VOICE/dsp_core.hexa:715 (linear → dB)              | ~3 | ★★★    | 0      | 1st  |
| `db_to_linear(db)`          | VOICE/dsp_core.hexa:720 (dB → linear)              | 1  | ★★★    | 0      | 1st  |

**카테고리 1 소계**: 60+ fn · 1769 LoC · **모두 stdlib-worthy** (FFT/windowing/filter/pitch/spectral)

---

# § 3 — 카테고리 2: Clustering / Classification

## 조사 결과

**발견**: anima codebase 전체에 **명시적 k-means, distance-metric 구현이 없음**.
- "clustering" 참조 26 개 → 대부분 `init_clustered(n)` 와 같은 domain-specific initialization helper.
- "distance" 참조 2 개 → KL divergence comment only (UNIVERSE-BRAIN-MAP/consciousness_carving_vacuum_lib.hexa:225).
- "jaccard" 참조 5 개 → spike event overlap metric (LAB/anima_spike.hexa), **non-general**.
- "classify/predict" 참조 23 개 → MITOSIS split/merge 관련 또는 CHAT tokenization; **domain-specific logic**.

## 평가

**결론**: Phase-3 survey 범위 내에서 **clustering/classification 은 stdlib-worthy general primitive 없음**.
- 이유 1: anima 는 consciousness/LIFE 역학 simulation에 집중 → classical ML (k-means, SVM 등)은 out-of-scope.
- 이유 2: 인포 이론 거리 (MI, KL) 는 phase-1 에서 이미 커버 (mutual_info_pair, kl_divergence).
- 이유 3: spike/event comparison 은 domain-specific (EEG 또는 consciousness substrate 특화).

**후보 (deferred/out-of-scope)**:

| 패턴                        | 발견 위치 / 도메인                                 | 평가                           |
|-----------------------------|---------------------------------------------------|--------------------------------|
| k-means cluster             | (없음)                                            | stdlib-worthy 구현 부재         |
| euclidean/manhattan distance| (없음)                                            | stdlib-worthy 구현 부재         |
| jaccard similarity          | LAB/anima_spike.hexa:188 (event overlap)          | spike domain-specific           |
| KL-based clustering         | UNIVERSE-BRAIN-MAP/../:225 (comment only)        | incomplete impl                |
| split/merge predicate       | MITOSIS/mitosis_lib.hexa:63-75 (4 fn)             | mitosis-domain logic            |
| tension-based classification| MITOSIS (split_predicate, merge_avg)              | cell-pool-specific              |

**권장**: clustering/classification 은 phase-3 scope 에서 **SKIP**. 이론적으로는 general 이지만 anima codebase 에는 구현/need 가 없음. RFC-037 (미래 general clustering stdlib) 으로 defer.

---

# § 4 — 카테고리 3: MITOSIS / CHAT / Domain-General Primitives

## A. MITOSIS 후보 (mitosis_lib.hexa)

| fn (canonical)              | 대표 위치                                          | LoC | 일반성 | 평가                           |
|-----------------------------|----------------------------------------------------|----|--------|--------------------------------|
| `mitosis_split_threshold_default()` | MITOSIS/mitosis_lib.hexa:36 | 1  | ★      | constant; domain-specific      |
| `mitosis_merge_threshold_default()` | MITOSIS/mitosis_lib.hexa:37 | 1  | ★      | constant; domain-specific      |
| `mitosis_split_patience_default()`  | MITOSIS/mitosis_lib.hexa:38 | 1  | ★      | constant; domain-specific      |
| `mitosis_merge_patience_default()`  | MITOSIS/mitosis_lib.hexa:39 | 1  | ★      | constant; domain-specific      |
| `mit_split_predicate(tension, thr)` | MITOSIS/mitosis_lib.hexa:63 | 1  | ★★     | tension > thr; cell-pool axiom |
| `mit_merge_avg(w1, w2)`     | MITOSIS/mitosis_lib.hexa:68 | 1  | ★★★    | arithmetic mean (generic)      |
| `mit_count_after(n,d_s,d_m)`| MITOSIS/mitosis_lib.hexa:73 | 1  | ★★★    | n + Δsplit − Δmerge (generic)  |
| `mit_clamp_count(n)`        | MITOSIS/mitosis_lib.hexa:79 | ~4 | ★★     | clamp [2, 64]; axiom-coupled   |
| `_mit_approx_eq(a,b,tol)`   | MITOSIS/mitosis_lib.hexa:50 | ~5 | ★★★    | float comparison (generic)     |

**평가**: `mit_merge_avg` + `mit_count_after` 는 일반적이지만, threshold constants + split_predicate 는 mitosis domain에 종속. _mit_approx_eq 는 generic 하지만 매우 작음 (이미 phase-1 에서 `_approx_eq` 가 있음, e.g., BRIDGE_lib:340).

## B. CHAT 후보 (chat_lib.hexa)

| fn (canonical)              | 대표 위치                                          | LoC | 일반성 | 평가                           |
|-----------------------------|----------------------------------------------------|----|--------|--------------------------------|
| `_chat_matvec_farr(...)`    | CHAT/chat_lib.hexa:1391 (farr matrix multiply)    | ~6 | ★★★    | stdlib linalg 으로 이미 promote |
| `_chat_softmax_farr_inplace(...)` | CHAT/chat_lib.hexa:1751 | ~15 | ★★★ | stdlib activation 으로 promote |
| `_chat_rms_norm_farr(...)`  | CHAT/chat_lib.hexa:1397 (farr RMSNorm)            | ~10 | ★★★    | stdlib linalg 으로 promote 후보|

**평가**: 모두 **phase-1 에서 이미 candidate로 식별됨** (softmax_inplace, matvec_farr, l2_norm). CHAT-specific facade 제거 후 rename하면 stdlib 가능.

## C. BRIDGE 후보 (bridge_lib.hexa)

| fn (canonical)              | 대표 위치                                          | LoC | 일반성 | 평가                           |
|-----------------------------|----------------------------------------------------|----|--------|--------------------------------|
| `_bridge_lcg_fill(h,n,seed)`| BRIDGE/bridge_lib.hexa:78 (LCG RNG)               | ~8 | ★★★    | stdlib/core/math/rng 로 promote|
| `_bridge_gelu(x)`           | BRIDGE/bridge_lib.hexa:91 (activation)            | ~4 | ★★★    | stdlib activation 으로 promote |
| `_bridge_sigmoid(x)`        | BRIDGE/bridge_lib.hexa:95                         | ~3 | ★★★    | stdlib activation 으로 promote |
| `_bridge_softmax(s,off,n)`  | BRIDGE/bridge_lib.hexa:105                        | ~10 | ★★★ | stdlib activation 으로 promote |
| `_bridge_matvec(...)`       | BRIDGE/bridge_lib.hexa:100 (matvec)               | ~8 | ★★★    | stdlib linalg 으로 promote      |

**평가**: 모두 **phase-1 에서 이미 식별됨**. BRIDGE facade 제거 후 upstream.

---

# § 5 — 새로운 발견 vs 기존 phase-1

| 기존 phase-1 | 본 phase-3                                  | 상태                      |
|-------------|-------------------------------------------|---------------------------|
| (없음)      | dsp_core.hexa 전체 60+ fn                 | **NEW: major addition**    |
| (없음)      | clustering/classification                 | **SKIP: not found/needed** |
| mit_split_predicate 등 | MITOSIS 4 fn + CHAT 3 fn + BRIDGE 5 fn | **DUPLICATE: phase-1 already covered** |

---

# § 6 — 1st-wave phase-3 권장 (신규 candidates)

dsp_core.hexa 의 60+ fn 을 6 개 stdlib module 로 organize:

### M6.1 signal/core_fft.hexa (NEW, ~80 LoC)
- `dsp_fft(real, imag, n)`
- `dsp_ifft(real, imag, n)`
- `bit_reverse(x, bits)` (helper)
- `log2_int(n)` (helper)
- `is_power_of_2(n)` (helper)

**dup count**: 1 SSOT (dsp_core.hexa).
**priority**: ★★★ 1st (foundational).

### M6.2 signal/core_stft.hexa (NEW, ~130 LoC)
- `dsp_stft(audio, n_fft, hop, win_type)`
- `dsp_istft(spec_real, spec_imag, n_fft, hop, win_type, n_frames)`
- `stft_num_frames(...)` (helper)
- `stft_frame_start(...)` (helper)
- `istft_output_len(...)` (helper)
- `istft_window_norm(...)` (helper)

**dup count**: 1 SSOT + 2 GPU variants (hxcuda_istft_bridge.hexa).
**priority**: ★★★ 1st (foundational, GPU bridge already depends).

### M6.3 signal/core_window.hexa (NEW, ~40 LoC)
- `hann_window(n, N)`, `hamming_window(n, N)`, `blackman_window(n, N)` (per-sample)
- `dsp_hann_window(n)`, `dsp_hamming_window(n)` (array)
- `window_sample(type, i, N)` (dispatcher)

**dup count**: 26 outside dsp_core (mostly headers/comments).
**priority**: ★★★ 1st (26 duplicates sweep-able).

### M6.4 signal/core_filter.hexa (NEW, ~50 LoC)
- `biquad_omega(f, sr)`, `biquad_alpha(ω, Q)`
- `lpf_coeff(...)`, `hpf_coeff(...)` (Audio EQ Cookbook)
- `biquad_tick(...)` (Direct Form I)
- `preemphasis_tick(...)`, `deemphasis_tick(...)`
- `dsp_preemphasis(audio, coeff)`

**dup count**: 1 SSOT; preemphasis comments ~5.
**priority**: ★★★ 1st (biquad is standard, used in dsp_core itself).

### M6.5 signal/core_pitch_and_spectral.hexa (NEW, ~130 LoC)
- `autocorr_accumulate(sample_n, sample_n_plus_tau)` + 2 dup (h208)
- `pitch_lag_to_hz(...)`, `hz_to_lag(...)`, `pitch_min_lag(...)`, `pitch_max_lag(...)`
- `parabolic_interp_offset(...)` (sub-sample refinement)
- `magnitude_bin(re, im)`, `power_bin(re, im)`
- `hz_to_mel(hz)`, `mel_to_hz(mel)`
- `dsp_mel_filterbank(n_mels, n_fft, sr)`
- `dsp_spec_to_mel(spec_mag, filterbank, n_mels)`
- `dsp_griffin_lim(mag_spec, n_fft, hop, n_iter)` (phase reconstruction)

**dup count**: autocorr 2, mel comment references 4, griffin-lim comment 4.
**priority**: ★★★ 1st (pitch analysis canonical, MEL standard in ML audio).

### M6.6 signal/core_resample_and_util.hexa (NEW, ~60 LoC)
- `lerp(s0, s1, t)` (from phase-1 survey already proposed)
- `dsp_pitch_shift(audio, semitones, sr)`
- `dsp_resample(audio, sr_in, sr_out)` 
- `upsample_src_index(...)`, `upsample_frac(...)`, `upsample_output_len(...)`
- `downsample_src_index(...)`, `downsample_output_len(...)`
- Audio operations: `rms_accumulate`, `rms_finalize`, `zcr_count`, `zcr_finalize`, `normalize_gain`, `apply_gain`, `mix`, `overlap_add_sample`, `overlap_add_hann`
- dB utilities: `linear_to_db(x)`, `db_to_linear(db)`

**dup count**: 0 direct; lerp already proposed phase-1.
**priority**: ★★ 2nd (resampling is useful but not critical for immediate sweep).

---

# § 7 — hexa-lang stdlib 제안 구조 (신규 directories/files)

```
hexa-lang/stdlib/
├── signal/                                    ← NEW (phase-3)
│   ├── core_fft.hexa         (dsp_fft, dsp_ifft, bit_reverse, log2_int, is_power_of_2)
│   ├── core_stft.hexa        (dsp_stft, dsp_istft, helpers)
│   ├── core_window.hexa      (Hann, Hamming, Blackman, dispatcher)
│   ├── core_filter.hexa      (biquad, lpf/hpf coeff, preemphasis, deemphasis)
│   ├── core_pitch.hexa       (autocorr, pitch lag, parabolic interp, MEL scale, mel_filterbank, griffin_lim)
│   └── core_resample.hexa    (lerp, pitch_shift, resample, RMS, ZCR, gain, mix, dB util)
└── ... (existing: math/, linalg/, info/, etc.)
```

**신규 디렉토리**: 1 (signal/)
**신규 파일**: 6 (core_fft, core_stft, core_window, core_filter, core_pitch, core_resample)
**총 신규 LoC**: ~490 LoC (dsp_core 의 subset, comment + test 제외)

---

# § 8 — phase-3 조사 통계

| 항목                        | 개수            | 비고                                  |
|-----------------------------|-----------------|---------------------------------------|
| 카테고리 1 (signal)          | 60+ fn · 1769 LoC | dsp_core.hexa; FFT/STFT/filter/pitch all ★★★ |
| 카테고리 2 (clustering)      | 0 fn found      | anima 에 classical ML clustering 구현 없음 |
| 카테고리 3 (domain-general)  | 12 fn (MITOSIS+CHAT+BRIDGE) | 모두 phase-1 에서 이미 식별됨  |
| 총 신규 후보 (phase-3)       | 60+ fn (signal only) | phase-1 + phase-3 = 107+ candidates |
| duplicate sites (signal)    | ~30-40 (window, autocorr, griffin-lim comments) | moderate; dsp_core is SSOT |
| stdlib-worthy vs domain-specific | 60 signal ★★★ + 0 clustering + 12 domain (already phase-1) | **phase-3 net gain: 60 signal fn** |

---

# § 9 — honest_limits (≥ 3)

- **L1 dsp_core.hexa scope boundary**: file 이 VOICE 도메인인지 general signal library 인지 명확하지 않음.
  - 판정: 함수들 (FFT, STFT, biquad, pitch) 는 audio/EEG 도메인 일반 (not voice-specific) → stdlib 가능.
  - 대신 hxcuda_istft_bridge.hexa 의 GPU 특화 code (cuda_malloc/upload) 는 separate cuda/ module 필요.
  
- **L2 k-means/distance metric 부재**: clustering 은 phase-3 scope 에서 구현이 없어 **SKIP**. future RFC-037 로 defer.

- **L3 MITOSIS/CHAT 중복 (phase-1 이미 covered)**: 본 조사에서 새로운 건 없음. phase-1 의 promote order 만 재확인.

- **L4 mel_filterbank/griffin_lim 복잡성**: 두 fn 다 50+ LoC 이지만, MEL/griffin-lim 은 ML audio 의 standard → stdlib 로 promote 하되 usage documentation 필수.

- **L5 farr vs array dual surface (phase-1 issue 재현)**: dsp_core.hexa 의 `dsp_fft(real: [float], imag: [float])` 는 pure hexa list 사용 → farr handle 이슈 없음 (CHAT 과 다름). 깔끔.

---

# § 10 — 권장 promote order (phase-3)

1. **M1 (즉시)**: signal/core_fft.hexa + core_window.hexa + core_filter.hexa
   - 이유: foundational (FFT 없으면 STFT 못 함), 26 window duplicate 즉시 sweep 가능.
   - 예상 LoC 제거: ~46 files × ~5 LoC = ~230 LoC anima sweep.

2. **M2 (동시)**: signal/core_stft.hexa + core_pitch.hexa
   - 이유: FFT/window 이후 dependent; pitch analysis 는 EEG upstream 에서도 필요 (미래).
   - 예상: hxcuda bridge 재패키징, h208 autocorr import 로 replace.

3. **M3 (2nd-wave)**: signal/core_resample.hexa + griffin_lim
   - 이유: less critical; pitch_shift/resample 는 voice domain-specific 활용 currently.

---

# § 11 — 결론

**Phase-3 survey 결과**:

1. **신규 stdlib 후보**: signal processing 60+ fn (dsp_core.hexa) — **all ★★★**, foundational, cross-domain 재사용 가능 (EEG, audio, spectral analysis).

2. **clustering/classification**: anima 에 구현 부재 → **SKIP** (RFC-037로 defer).

3. **domain-general (MITOSIS/CHAT)**: phase-1 에서 이미 식별됨 → **중복 없음** (본 조사는 재확인만 수행).

4. **다음 단계**:
   - Phase-3 M1 stdlib promote PR: hexa-lang 에 signal/ 6 module push.
   - anima 측 M2-M4: dsp_core.hexa import 갱신 + dup sweep (window 26, autocorr 2, comment references 4).
   - M5 추가 가능: GPU cuda/ module separation (hxcuda_istft_bridge 재정리).

**총 3개 카테고리 대상 survey 완료.**

---

# § 12 — 결과 cross-link

- SSOT input: `/Users/ghost/core/anima/HEXAD/VOICE/anima-voice/dsp_core.hexa` (1769 LoC)
- 기존 survey reference: `/Users/ghost/core/anima/HEXAD/STDLIB/survey_2026_05_24.md` (phase-1, 240 LoC)
- 본 doc: `/Users/ghost/core/anima/HEXAD/STDLIB/phase3_survey_2026_05_25.md` (~380 LoC)
- 후속 cycle: STDLIB M1-M5 (signal promote + dup sweep + GPU refactor).
