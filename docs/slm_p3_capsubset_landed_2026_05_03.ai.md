# SLM Phase 3 cap-subset EXEC LANDED — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth (READ-ONLY upstream):
>   - `docs/slm_phase3_spec_2026_05_03.md` (Phase 3 scope freeze)
>   - `docs/slm_nlm_200cap_respec_2026_05_03.md` (cap re-spec, $200 GPU cap)
>   - `docs/slm_stage12_landed_2026_05_03.ai.md` (Phase 1+2 landed predecessor)
> write: this doc + 4 axis JSON outputs + marker + .roadmap.slm_speech_eeg_lm additive
> raw#9 NO .py on Mac (inline python only, nothing persisted as .py)
> raw#15 NO personal paths
> commit: NONE (per user directive)
> cap: $150 (cap-subset), used **$0**

---

## TL;DR

**오늘 한 일** — SLM Phase 3 cap-subset slate (A1+C1-soft+D1+D3) 4-axis EXEC. mac-local CPU synthetic 만 사용 (raw#9 inline python, .py persist 0). GPU spend **$0** / cap utilization **0%**. B-axis (prosody $200-800 RunPod A100 LoRA) 측 cap 외부로 deferred 유지.

**비유** — 4개 측 측정 axis 측 측 모두 **synthetic harness mode**. FAD 측 진짜 음성 embedding 대신 Gaussian proxy (formula correctness 측 monotonic 측 재현), TRF 측 실제 EEG 대신 mock-EEG fixture (planted signal 측 lag/channel 측 모두 정확 회수), LSL latency 측 실제 LM forward pass 대신 numpy BLAS overhead 측만 측정 (296ms headroom 확보), RVQ timing 측 random codebook 측 NN-search 측만 측정 (8x headroom). **published-baseline 측정 측 X**, **pipeline shape verify + budget-floor establishment 측 O**.

**결과** — `.roadmap.slm_speech_eeg_lm` cond.1 evidence 10→11 / cond.2 4→6 / cond.3 2→3 / raw_invariants 9→10 / blk.1 resolution_path 측 cap-subset cycle status 추가. JSON validity PASS. sister .roadmap.eeg in-place 변경 0건 (B1-B4 4관문 SSOT 보존).

---

## §1 4-axis EXEC 결과

### §1.1 P3.A1 — FAD synthetic harness

```
   axis     | P3.A1 — FAD (Frechet Audio Distance, VGGish-shape proxy)
   mode     | synthetic_gaussian_proxy (VGGish weight + ref-corpus DEFERRED)
   metric   | ||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2(Σ_r Σ_g)^0.5)
   floor    | <=2.0 (real audio spec)
   ────────────────────────────────────────────
   self_baseline    | -2.7e-14 (numerical floor, formula correctness)
   close_dist       | 2.0667 (small σ + 0.01 offset perturbation)
   far_dist         | 163.2541 (mean shift +1.0 + scale 1.5x)
   monotonicity     | PASS (self < close < far, ~80x discrimination)
   ────────────────────────────────────────────
   verdict  | HARNESS_OK_FORMULA_VERIFIED
   wall     | 0.07s
   output   | state/slm_p3_capsubset_2026_05_03/p3_a1_fad_synthetic.json
```

**rationale**: 진짜 VGGish weights (~280MB) + reference audio corpus 측 download 측 cap baseline $0 안에서 deferred. synthetic Gaussian 측 formula sanity 만 검증 (self ≈ 0, monotonic discrimination). 실제 RVQ-decode → audio render → VGGish embed → FAD 측 측 post-RVQ-IMPL cycle.

### §1.2 P3.C1 — TRF mock-EEG fixture (soft-fallback)

```
   axis     | P3.C1 — speech envelope ↔ EEG TRF (mock-EEG fixture)
   mode     | synthetic_planted_signal (Brennan-Hale 2019 corpus DEFERRED)
   floor    | Pearson r >= 0.15 at 60-500ms lag (Crosse 2016 mTRF)
   ────────────────────────────────────────────
   fs / N_ch / window  | 250Hz / 16ch / 1250 samples (5s)
   planted lag         | 120ms (= 30 samples @ 250Hz)
   planted channels    | T7 / T8 / P7 / P8 (auditory dominance, 10-20)
   planted SNR amp/std | 0.4 / 0.5 = 0.8x (realistic)
   lag sweep           | 60..500ms × 20ms steps (23 lags)
   ────────────────────────────────────────────
   auditory r mean     | 0.2255 (>= 0.15 floor, all 4 ch)
   non-auditory r mean | 0.0502 (12 ch noise floor)
   auditory r std      | 0.029 (tight cluster)
   discrimination      | 4.5x (auditory vs non-auditory peak r)
   peak lag recovery   | 120.0 ± 0.0 ms (exact, all 4 auditory ch)
   ────────────────────────────────────────────
   verdict  | SCAFFOLD_OK_PLANTED_SIGNAL_RECOVERED
   wall     | <0.1s
   output   | state/slm_p3_capsubset_2026_05_03/p3_c1_trf_mock_eeg.json
```

**rationale**: real Brennan-Hale 2019 N=49 corpus 측 측 download 측 본 cycle 미수행, .roadmap.eeg B1-B4 4관문 PASS prerequisite 측 sister 측 unmet 유지. cap path 측 측 mock-EEG fixture 측 mTRF 측 pipeline shape (lag-sweep + per-channel Pearson) 측 sanity 만 검증. **C1 falsifier state 측 측 advance 0** — 그냥 "pipeline 측 measurable 측 O" 측 안전판 측 land.

### §1.3 P3.D1 — LSL latency probe (stub)

```
   axis     | P3.D1 — LSL → 1st decoded text latency (STUB MODE)
   mode     | stub_full_pipeline_no_real_weights (Llama-3.2-1B forward DEFERRED)
   floor    | p50 <= 300ms, p99 <= 500ms (closed-loop BCI, full IMPL)
   ────────────────────────────────────────────
   pipeline | synthetic_eeg(80d) → project(80→384) → rvq_argmax(4096) →
            | cross-attn(384→128256 text vocab) → text_argmax
   trials   | 200 (after 20-trial BLAS warmup)
   ────────────────────────────────────────────
   p50 ms   | 3.54
   p95 ms   | 5.38
   p99 ms   | 6.12
   max ms   | 12.97
   ────────────────────────────────────────────
   headroom vs p50 (300ms) target | 296.5ms (LM forward + KV-cache budget)
   headroom vs p99 (500ms) target | 493.9ms
   ────────────────────────────────────────────
   verdict  | STUB_BUDGET_FLOOR_ESTABLISHED
   wall     | <2s (200 trials)
   output   | state/slm_p3_capsubset_2026_05_03/p3_d1_lsl_latency_stub.json
```

**rationale**: real LSL stream + real Llama-3.2-1B forward pass + real KV-cache mgmt 측 본 cycle 측 측 NOT executed. numpy BLAS framework overhead 측만 측정 → ~3.5ms p50, 296ms 측 budget 측 real-IMPL 측 채울 수 있음. **closed-loop BCI demonstration 측 X**, **budget floor establishment 측 O**.

### §1.4 P3.D3 — RVQ quantize step timing (synthetic)

```
   axis     | P3.D3 — RVQ quantize step latency (synthetic CPU)
   mode     | synthetic_residual_vq_timing (random codebooks)
   config   | n_stages=4, vocab_per_stage=1024, d_model=384, vocab_total=4096
   floor    | <=20ms per epoch (epoch=1s shift=0.25s, 4Hz token-rate)
   ────────────────────────────────────────────
   single-input p50    | 1.19 ms
   single-input p95    | 2.03 ms
   single-input p99    | 2.43 ms
   per-epoch 4-mode p50| 6.37 ms
   per-epoch 4-mode p95| 9.24 ms
   per-epoch 4-mode p99| 10.51 ms
   ────────────────────────────────────────────
   single headroom ratio   | 8.2x (vs 20ms floor)
   per-epoch headroom ratio| 1.9x (vs 20ms floor)
   ────────────────────────────────────────────
   verdict  | TIMING_FLOOR_PASS_HEAVY_HEADROOM
   wall     | ~5s (500 trials × 2 modes)
   output   | state/slm_p3_capsubset_2026_05_03/p3_d3_rvq_quantize_timing.json
```

**rationale**: random codebooks (uniform Gaussian) 측 NN-search 측 → real EMA-trained codebook geometry 측 cluster 측 측 measure 차이 측 가능. mac-local CPU 측 단일 측 측, no Metal acceleration. 4-mode per-epoch 측 worst-case heuristic (실 IMPL 측 single 384d shared embedding 측 가능, half cost).

---

## §2 .roadmap.slm_speech_eeg_lm delta 요약

```
   field                    | before | after | delta
  ------------------------- | ------ | ----- | ----------------------------------
   cond.1 evidence          | 10     | 11    | +P3.D3 RVQ quantize timing
   cond.2 evidence          | 4      | 6     | +P3.D1 LSL latency stub +P3.A1 FAD
   cond.3 evidence          | 2      | 3     | +P3.C1 TRF mock-EEG fixture
   cross_link.raw_invariants| 9      | 10    | +cap-subset cycle invariant
   cross_link.predecessor   | 7      | 9     | +cap re-spec doc + Phase 3 spec doc
   cross_link.handoff       | 1      | 1+1   | +this doc (prepend)
   blk.1 resolution_path    | (orig) | +note | cap-subset cycle status appended
   cond.1/2/3 status        | partial/partial/unmet | unchanged | (no falsifier advance)
```

**cond status 변화 0** — cap-subset cycle 측 evidence 측 추가 측만, **published-baseline measurement 측 X 측 사유 status 상승 X** (honest C3 정합).

---

## §3 cost ledger

```
   item                          | spend     | note
  ----------------------------- | --------- | --------------------------------
   mac-local CPU synthetic       | $0        | 4 axes inline python (no .py persist on Mac)
   ubu1/ubu2 GPU                 | $0        | NOT used (B s43/s44 진행 중, cycle 충돌 회피)
   RunPod / cloud                | $0        | bypass
   data download (Brennan-Hale)  | $0        | DEFERRED
   VGGish weight download        | $0        | DEFERRED
  ----------------------------- | --------- | --------------------------------
   total GPU spend               | $0        | 0% of $150 cap (user constraint $0-150)
   cap remaining                 | $150      | available for next cycle if needed
```

**B-axis (prosody $200-800 RunPod A100 LoRA) — DEFERRED, NOT spent**: cap 외부 측 사유 측 sister cycle 측 budget-unlock 후 재진입.

---

## §4 sister roadmap untouched verify

```
   .roadmap                  | this cycle | reason
  ------------------------- | ---------- | -----------------------------------
   .roadmap.eeg             | UNTOUCHED  | B1-B4 4관문 SSOT, in-place 변경 X
   .roadmap.voice           | UNTOUCHED  | VLM × voice dual SSOT
   .roadmap.vlm_voice_lm    | UNTOUCHED  | sibling LM
   .roadmap.blm_brain_lm    | UNTOUCHED  | F-CT-3 sister falsifier reference only
   .roadmap.nlm/tlm         | UNTOUCHED  | sibling LM, 5-LM ecosystem reference
   .roadmap.p9_sft          | UNTOUCHED  | training pipeline reuse reference
   .roadmap.anima_engines   | UNTOUCHED  | engine_a/g axis define cycle 별도
```

---

## §5 honest C3 caveats (raw#10) — 3건

1. **C3-cap-1 — "cap-subset" 측 4-axis EXEC 측 measurement 측 X, harness/scaffold/stub/timing 측 만**.
   - P3.A1 측 실 VGGish embedding 측 부재, synthetic Gaussian 측 formula correctness 측 만.
   - P3.C1 측 real Brennan-Hale 2019 corpus 측 부재, mock-EEG fixture 측 planted-signal 측 sanity 만.
   - P3.D1 측 real LM forward pass 측 부재, numpy BLAS overhead 측 budget 측 floor 측 만.
   - P3.D3 측 real EMA-trained codebook 측 부재, random codebook NN-search 측 timing 측 만.
   - 본 cycle 측 결과 측 "Phase 3 published-baseline 측정 측 PASS" 측 주장 X — Phase 3 측 4 falsifier state 측 측 unchanged. **honest label = "Phase 3 cap-subset (harness + scaffold + stub + timing 측 4-axis budget-floor establishment)"**.

2. **C3-cap-2 — sister .roadmap.eeg B1-B4 4관문 PASS 측 unmet 유지, P3.C1 측 real-data measurement 측 unblock 측 0**.
   - .roadmap.eeg cond.1 측 evidence 0 유지, B1-B4 측 sister cycle 측 별도 cycle 측 land 필요.
   - 본 cycle 측 P3.C1 측 mock-EEG fixture 측 측 측 published Pearson r ≥ 0.15 측 floor 측 advance X — 다음 cycle 측 .roadmap.eeg B1-B4 PASS 측 sister 측 wait.

3. **C3-cap-3 — B-axis (prosody, $200-800) 측 cap 외부 측 measurable axis count 측 4 측 remained, "Phase 3 4-axis met" 측 주장 측 misrepresentation 위험**.
   - Phase 3 spec 측 entry slate (4 conds: A1+B1+C1+D1) 측 B1 측 cap 외부 측 사유 측 본 cycle 측 P3.B1 측 evidence 측 0 유지.
   - 본 cycle 측 4-axis 측 (A1+C1+D1+D3) 측 spec 측 4-axis 측 (A1+B1+C1+D1) 측 측 측 measurement type 측 다름.
   - "Phase 3 cap-subset 4-axis EXEC" 측 정확, "Phase 3 4-axis met" 측 misrepresentation. budget-unlock cycle 측 P3.B1 측 land 시 측 Phase 3 entry slate 측 4-axis 측 비로소 충족 가능.

---

## §6 next-cycle recommendation

1. **.roadmap.eeg B1-B4 4관문 PASS** — sister prerequisite 측 해소 측 P3.C1 real-data measurement (Brennan-Hale 2019 N=49) 측 unblock + cap 안 ($0-100 GPU) 측 fit
2. **Brennan-Hale 2019 corpus dataset audit cycle** — license verify (CC-BY) + audio-EEG sync timestamp align + 4-mode tokenization smoke 측 별도 cycle (cap 안 $0)
3. **slm_tokenizer.hexa + slm_ar_decoder.hexa IMPL land** — anima-voice/audio_token_predictor.hexa 1576L mirror, scaled-down 8→4 stage (cap 안 $0 mac-local + ubu1, raw#9 .py 측 ubu OK)
4. **VGGish weight download + real FAD measurement** — P3.A1 측 synthetic → real audio (~280MB weight + ref-corpus, $0 cap-fit on mac CPU)
5. **B-axis budget unlock event 측 watch** — $200-800 unlock 시 P3.B1 prosody embedding alignment (RunPod A100 LoRA) 측 진입; 그 전 측 cap 외부 측 deferred 유지

---

## §7 cycle 메타

```
   cycle         | SLM Phase 3 cap-subset EXEC (4-axis: A1+C1-soft+D1+D3)
   policy        | additive only / BR-NO-USER-VERBATIM / Korean response /
                 |   silent-land marker / $0 mac-local / destructive 0 /
                 |   raw#9 NO .py on Mac (inline python only) / raw#15 NO personal paths
   cap           | $150 (user cap-subset constraint)
   cost          | $0 (mac-local CPU synthetic, 0% cap utilization)
   wall          | ~3 min (4 inline python invocations + roadmap update + doc/marker)
   files modified| 1 (.roadmap.slm_speech_eeg_lm cond detail land additive)
   files created | 6 (this doc + marker + 4 axis JSON outputs)
   files untouched| 7+ (.roadmap.eeg + .roadmap.voice + sibling LM 5 + P9 + anima_engines)
   marker        | state/markers/slm_p3_capsubset_landed.marker
   handoff       | docs/slm_p3_capsubset_landed_2026_05_03.ai.md (this doc)
   migration     | 0
   substrate     | 100% mac-local CPU (no ubu, no cloud, no GPU)
   B-axis defer  | YES ($200-800 outside cap, sister cycle wait)
```

end-of-doc.
