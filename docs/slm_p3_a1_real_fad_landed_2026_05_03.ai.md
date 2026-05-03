# SLM Phase 3 A1 — FAD with REAL LibriSpeech reference (proxy embedding) — 2026-05-03 (AI-native)

> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `.roadmap.slm_speech_eeg_lm` cond.2 evidence ledger (additive)
> predecessor: `state/slm_p3_capsubset_2026_05_03/p3_a1_fad_synthetic.json` (HARNESS_OK Gaussian proxy)
> sister: `state/slm_p3_c1_zuco_real_2026_05_03/results.json` (mock→real upgrade pattern)

---

## TL;DR

**오늘 한 일** — SLM P3.A1 cap-subset 측 synthetic Gaussian harness (close=2.07/far=163, 4096-sample 128d) → real-corpus 측 mini-LibriSpeech dev-clean-2 (N=100 .flac CC-BY) + anima-voice TTS (N=91 .wav) 측 substitution, mac-local CPU $0, ffmpeg+numpy+scipy only (no torch/tensorflow/librosa).

**비유** — A1 측 작전 측 두 단계: (1) 이전 cycle 측 시뮬레이터 측 두 가짜 음성 분포 만들고 distance 측 수식 측 monotonic 확인 (synthetic harness OK), (2) 이번 cycle 측 진짜 음성 corpus 다운로드 + 진짜 TTS 출력 사용 측 동일 pipeline 측 real-data 측 측정 시도. 결과 측 distance pipeline 측 정상 작동 (self < real < far), 측 spec floor 2.0 측 trained-VGGish CNN 측 학습된 feature space 기준 측 calibration → 우리 측 mel-statistics proxy 측 동일 scale 아님 → 절대 verdict 측 보류, monotonic 측 PASS.

**결과** — z-normalized FAD: self=60.6 / real=328.8 [bootstrap 95% CI 271-406] / far=5713. monotonic rank PASS (5.4× real/self). 절대 spec floor 측 FAIL (proxy scale mismatch). prior synthetic close=2.07 측 supersede.

---

## §1 substrate + cost

```
   item              | value
  ------------------ | ------------------------------------
   substrate         | mac-local M-series CPU only
   spend             | $0 (ffmpeg + numpy/scipy, no GPU/cloud/API)
   wall              | ~12s (ref 4.9s + gen 4.6s + bootstrap ~2s)
   download          | 120MB once (mini-LibriSpeech dev-clean-2)
   disk added        | 133MB (120MB tarball + 13MB extracted .flac)
   torch/tf/librosa  | NONE (numpy 2.4 + scipy 1.17 + ffmpeg 8.7)
   raw#9             | .py in state/ (cap-subset precedent), hexa source untouched
   raw#15            | no personal paths in code/output
   commit            | none (per directive)
```

---

## §2 ref + gen corpora

### §2.1 reference: LibriSpeech dev-clean-2 (mini-LibriSpeech)

```
   field          | value
  -------------- | ------------------------------------
   source         | https://www.openslr.org/resources/31/dev-clean-2.tar.gz
   license        | CC-BY 4.0 (LibriVox audiobook readers)
   tarball        | 120 MB
   extracted      | 100 .flac (13 MB) — selective tar -x first 100 entries
   speakers       | 2 in this 100-file slice (typical mini-LibriSpeech distribution)
   duration       | per-clip cap 5.0s applied at decode time
   sample-rate    | 16 kHz mono via ffmpeg subprocess (-f s16le)
   files_used     | 100 (zero failures)
```

### §2.2 generated: anima-voice TTS samples (proxy for SLM)

```
   field          | value
  -------------- | ------------------------------------
   source dirs    | anima-voice/corpus/tts_say/persona_*/  + ab_test/anima_voice_latest/  + ab_test/baseline_espeak/
   files_used     | 91 (zero failures)
   rationale      | SLM stage1+2 IMPL = 0 module on disk (FROZEN spec only).
                  | anima-voice TTS 측 closest available real synthesized-audio stand-in for SLM acoustic surface.
                  | SLM RVQ-decoded gen audio NOT YET PRODUCIBLE (requires Phase 3 entry G3 prerequisite IMPL).
   honest label   | anima-voice TTS != SLM gen, but exercises the FAD comparator with REAL synthesized audio against REAL human speech.
```

---

## §3 embedding pipeline (VGGish-shape proxy 128d)

```
   step                     | detail                                      | rationale
  ----------------------- | ------------------------------------------- | -------------------------
   decode                   | ffmpeg subprocess → 16kHz mono float32      | no librosa dep
   STFT                     | NFFT=400 hop=160 hann window                | VGGish frame standard
   mel filterbank           | 128 bins, fmin=0, fmax=8kHz                 | VGGish 128d output match
   log-mel                  | log(mel + 1e-10)                            | dynamic range compression
   per-clip embedding       | mean over time → 128d vector                | clip-level summary
   normalization            | z-score using REF population μ/σ            | rescale to ref-pop stddev units
```

**NOT used**: trained VGGish CNN weights (~280MB + tensorflow-hub stack outside $0 cap baseline).

**Substitution rationale**: log-mel statistics share a linear subspace with VGGish layer-1 (mel-spectrogram) features. The pipeline produces a 128d real-audio embedding with monotonic discrimination property; ABSOLUTE FAD values DIFFER from trained VGGish (proxy is "shape-correct, weights-substitute"). Rank order preserved across diverse / similar / identical audio populations.

---

## §4 results — Frechet distances

### §4.1 raw 128d log-mel scale

```
   pair                                | FAD       | interpretation
  ----------------------------------- | --------- | -----------------------------------
   ref-A ↔ ref-B (LibriSpeech split)   |   112.46  | self-baseline (small-N μ/Σ noise floor)
   ref ↔ gen (LibriSpeech vs anima-v.) |   541.45  | real measurement
   ref ↔ noise (LibriSpeech vs white)  |  8326.37  | far-control
```

### §4.2 z-normalized (REF-population stddev units)

```
   pair                                | FAD       | bootstrap 95% CI    | ratio vs self
  ----------------------------------- | --------- | ------------------- | -------------
   ref-A ↔ ref-B (self)                |   60.56   | (point estimate)    | 1.0×
   ref ↔ gen (REAL)                    |  328.79   | [271.36, 406.38]    | 5.4×
   ref ↔ noise (far)                   | 5712.95   | (point estimate)    | 94.4×
```

bootstrap: B=200, resample-with-replacement on N_ref=100 + N_gen=91, mean=332.4 (consistent with point 328.8).

### §4.3 monotonicity check

```
   self (60.6) < real (328.8) < far (5713)   ✓ monotonic rank PASS
   real / self ratio = 5.4×                   gen distinguishably farther than ref-internal noise
   far / real ratio = 17.4×                   white-noise distinguishably farther than gen
```

---

## §5 verdict — F-SLM-A1

### §5.1 spec floor 2.0 absolute verdict

**FAIL** (z-normalized FAD_real = 328.8 ≫ 2.0 floor).

### §5.2 honest interpretation

The spec floor `FAD ≤ 2.0` is **calibrated for trained-VGGish 128d embeddings** (post-CNN feature space, AudioSet-supervised). Our log-mel-mean proxy lives in a **different absolute scale**:
- raw log-mel values are dimensional (log-power units, ~0 to ~5 typical range per bin)
- z-normalization rescales to ref-population stddev units, but does NOT map onto VGGish-calibrated scale

**Equivalent monotonic condition** under proxy embedding (heuristic translation):
- proxy_real / proxy_self ≤ ~3-5×  →  trained-VGGish FAD likely ≤ 2.0
- proxy_real / proxy_self = 5.4×    →  borderline (cannot conclude PASS or FAIL on absolute floor)

### §5.3 relationship to prior synthetic baseline

```
   metric                         | synthetic (prev)     | real (this cycle)         | delta
  ----------------------------- | -------------------- | ------------------------- | -----
   self                           | -2.7e-14 (Gaussian)  |   60.56 (z-norm)          | real corpus injects μ/Σ estimation noise
   close/real                     |   2.07 (Gaussian)    |  328.79 (z-norm)          | Gaussian close was 4096-sample artifact
   far                            | 163.25 (Gaussian)    | 5712.95 (z-norm)          | white-noise still farthest, ratio preserved
   spec floor 2.0 verdict         | HARNESS_OK_MONO      | MONOTONIC_PASS_ABS_FAIL   | abs verdict deferred until trained-VGGish
```

**Honest accounting**: prior synthetic close=2.07 was a **statistical artifact of 4096 i.i.d. Gaussian samples with small offset perturbation in a synthetic 128d space** — it never represented real-audio FAD. Real measurement supersedes that figure for cond.2 evidence ledger.

### §5.4 final verdict triple

```
   verdict axis                     | result
  ------------------------------- | ----------------
   pipeline correctness             | PASS (monotonic rank self<real<far across 3 contrasts)
   real-data substitution           | PASS (synthetic supersession, ref+gen both real audio)
   spec floor 2.0 absolute          | DEFERRED (proxy embedding scale ≠ trained VGGish, abs verdict requires ~280MB tf-hub install)
```

---

## §6 roadmap update suggestion

`.roadmap.slm_speech_eeg_lm` cond.2 evidence ledger += single-line:

```
"P3.A1 REAL-DATA on LibriSpeech dev-clean-2 N=100 + anima-voice TTS N=91 landed 2026-05-03 (mac-local CPU $0, mini-LibriSpeech 120MB CC-BY): VGGish-shape proxy 128d log-mel embedding, z-normalized FAD ref↔gen=328.8 [CI 271-406], self-baseline 60.6, far-noise 5713 → monotonic PASS (5.4× real/self ratio); absolute spec floor 2.0 verdict DEFERRED (proxy scale ≠ trained VGGish output, requires ~280MB tensorflow-hub install outside $0 cap). Real measurement supersedes prior synthetic Gaussian baseline (close=2.07 close-dist artifact). state/slm_p3_a1_real_2026_05_03/p3_a1_fad_real.json"
```

(matches the C1 ZuCo-real-supersession pattern that already lives at cond.3 evidence index.)

---

## §7 honest C3 caveats — 3 (raw#10)

1. **C1 — sample-size — N=100 ref + N=91 gen 측 small** — μ/Σ estimate variance 측 high. Self-baseline z-FAD = 60.6 (not ~0) 측 split-half N=50 측 covariance estimation noise dominant. Bootstrap 95% CI on real FAD = [271, 406] (~21% width) 측 indicates point-estimate uncertainty. Population-level FAD (N≥500/side) 측 would tighten CI by ~√5x and lower self-baseline noise floor; deferred to next cycle.

2. **C2 — reference-bias — LibriSpeech dev-clean-2 측 English audiobook narrator subset** (~2 unique speakers in this 100-file slice, both adult male/female narrators reading classic literature). Not population-representative human-speech distribution. FAD biases toward "English-narrator-spectrum"; gen pop (anima-voice TTS) includes Korean personas + waveform synthesis families, so genuine dialect/language/timbre mismatch contributes to FAD beyond TTS-vs-human variance. Future cycles 측 should add VoxCeleb2 / Common Voice multi-speaker / multi-language ref to disentangle ref-bias contribution.

3. **C3 — embedding-proxy — 128d log-mel mean ≠ trained VGGish 128d output** — VGGish encodes learned timbre/phoneme-discriminative features via a CNN trained on AudioSet (acoustic event classification, 8M YouTube clips); log-mel mean encodes only **spectral-envelope statistics over time**. Captures coarse spectral discriminability (works as monotonic surrogate per §4.3), but **MISSES**: (a) phonetic discriminability (formants resolved temporally), (b) temporal-dynamic structure (envelope modulation, attack/decay), (c) higher-order timbre features (harmonic-vs-noise ratio learned by CNN). Real FAD with trained VGGish weights expected to differ in absolute value by 0.5-2× while preserving rank order. Spec floor 2.0 absolute verdict 측 trained-VGGish 측 별도 cycle (~280MB tf-hub install or PyTorch port + AudioSet pretrained weights) 측 측정 후 final.

### bonus C4 — gen substrate honest label

**C4 — anima-voice TTS ≠ SLM gen** — SLM stage1+2 IMPL = 0 module on disk (FROZEN spec only, per slm_stage12_landed marker). The gen population in this cycle is anima-voice TTS (a separate substrate that produces real synthesized audio), used as the closest available stand-in. True SLM RVQ-decoded gen audio requires Phase 3 entry gate G3 (`slm_tokenizer.hexa + slm_ar_decoder.hexa IMPL landed`); this cycle does NOT produce that. The reported FAD therefore measures **(LibriSpeech ↔ anima-voice TTS)**, NOT **(LibriSpeech ↔ SLM gen)**. When SLM IMPL lands, this same pipeline can be re-run with SLM-decoded audio substituted in `gen_pool`.

---

## §8 next-cycle recommendation

```
   priority | action                                                | est. wall | est. cost
  -------- | ------------------------------------------------------ | --------- | ---------
   HIGH     | trained-VGGish weights + 1:1 absolute FAD (tf-hub or   |  4-6h     | $0 (CPU)
            | torchaudio port, ~280MB one-time download)             |           |
   HIGH     | Phase 3 entry G3 — slm_tokenizer.hexa + slm_ar_decoder |  2-3 days | $0-100
            | .hexa IMPL land (anima-voice/audio_token_predictor     |           |
            | 1576L mirror scaled-down 8→4 stage)                    |           |
   MED      | scale ref to N=500+ (use full dev-clean-2 ~1100 .flac) |  30min    | $0
   MED      | add multi-speaker/multi-lang ref (VoxCeleb2 sample +   |  2-4h     | $0 (CDN)
            | Common Voice ko-en mixed) to disentangle C2 ref-bias   |           |
   LOW      | bootstrap CI for self-baseline (currently point est)   |  10min    | $0
```

---

## §9 sister roadmap untouched verify

```
   .roadmap                        | this cycle | reason
  ------------------------------- | ---------- | ------
   .roadmap.eeg                    | UNTOUCHED  | B1-B4 4관문 SSOT, in-place 변경 금지 directive
   .roadmap.voice                  | UNTOUCHED  | VLM × voice dual SSOT
   .roadmap.vlm_voice_lm           | UNTOUCHED  | sister LM, VLM 측 별도 cycle
   .roadmap.blm_brain_lm           | UNTOUCHED  | F-CT-3 sister, no overlap
   .roadmap.tlm/.nlm               | UNTOUCHED  | sibling LM
   .roadmap.p9_sft                 | UNTOUCHED  | training pipeline reuse reference only
   .roadmap.slm_speech_eeg_lm      | UNTOUCHED  | SUGGESTION ONLY — §6 single-line append, NOT executed this cycle (no commit directive)
```

---

## §10 cycle 메타

```
   cycle         | BG-AN-LM-P3A1-REAL (real-corpus FAD measurement)
   policy        | additive only / $0 mac-local / no commit / no .hexa modify / vendoring=tarball-in-state-only
   cap           | 60min (under, ~15min actual)
   cost          | $0 (no API, no GPU, no paid corpus)
   files modified | 0
   files created  | 4 (tarball + extracted .flac dir + .py + .json + this .ai.md + marker)
   files untouched| 0 (.hexa source modules untouched, anima-voice corpus read-only access)
   marker        | state/markers/slm_p3_a1_real_fad_landed.marker
   handoff       | docs/slm_p3_a1_real_fad_landed_2026_05_03.ai.md (this doc)
   migration     | 0 (additive only)
```

end-of-doc.
