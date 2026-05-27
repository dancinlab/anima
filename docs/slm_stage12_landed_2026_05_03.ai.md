# SLM Stage 1+2 Spec Landed (Speech-EEG LM) — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `.roadmap.slm_speech_eeg_lm` (in-place additive cond detail land, 1 entry; sister .roadmap.eeg untouched)
> predecessor: `docs/anima_2_lm_vlm_slm_landed_2026_05_03.ai.md` §3.2 (SLM v0 spec, BG-AN-LM3 fan-out)

---

## TL;DR

**오늘 한 일** — BG-AN-LM4 audit cycle. SLM (Speech-EEG LM) 측 stage 1 (EEG signal encoding + tokenization) + stage 2 (EEG-conditioned LM head) 측 spec FROZEN candidate land. cond.1 partial 유지 (4-mode spec 측 land 완료, IMPL 단계 결정점 잔존), cond.2 unmet→partial 상승 (LM head spec FROZEN candidate). blocker.1 측 EEG-text paired corpus 4 candidate audit 완료 (Brennan-Hale 2019 N=49 narrative listening 1순위 권장).

**비유** — 이전 cycle 측 SLM 측 신입 사원증(.roadmap.slm_speech_eeg_lm) 발급만 끝낸 상태였는데, 이번 cycle 측 사원 측 직무 기술서 (stage 1: EEG 측 어떻게 token 으로 자를지 + stage 2: 그 token 측 위에 어떻게 next-word 예측 할지) 측 두 장 첨부. 부서장(.roadmap.eeg) 측 사원 명부 변경 0건, 직무 기술서 측 sister VLM (anima-voice Mk.III) 직무 기술서 측 거의 그대로 축소판 (8-stage RVQ → 4-stage RVQ).

**결과** — `.roadmap.slm_speech_eeg_lm` cond.1 evidence +3 / cond.2 status partial 상승 + spec evidence +4 / cond.3 corpus candidate evidence +1 / raw_invariants 6→9 (+3) / blk.1 resolution_path 측 corpus 4-candidate audit detail update. JSON validity PASS (3 cond + 1 blocker + 9 invariant). sister .roadmap.eeg in-place 변경 0건 (B1-B4 4관문 SSOT 보존).

---

## §1 stage 1 spec FROZEN candidate — EEG signal encoding + tokenization

### §1.1 EEG signal encoding 4-mode (S1.1-S1.4)

```
   mode    | name           | dim per epoch | source                                    | use case
  ------- | -------------- | ------------- | ----------------------------------------- | --------
   S1.1   | band-power     | 80            | 16ch × 5band log-PSD (delta/theta/        | resting/coarse
          |                |               |   alpha/beta/gamma) Welch NFFT=512        |   state classify
          |                |               |   hann 50% overlap                        |
   S1.2   | phase coherence| 40            | 8-pair × 5band Welch coherence            | bilateral binding
          |                |               |   (Fp1↔Fp2/F3↔F4/C3↔C4/P3↔P4/             |   + R33 anchor
          |                |               |    O1↔O2/F7↔F8/T7↔T8/P7↔P8)               |
   S1.3   | spike-train    | 20000 sparse  | BrainFlow notch z-score >2.5 binary       | fine event
          |                |               |   16ch × 1250 sample binary mask          |   detection
   S1.4   | raw-bin        | 20000 dense   | 16ch × 1250 float32 windowed              | full info
          |                |               |   (epoch=1s shift=0.25s)                  |   downstream
  ------- | -------------- | ------------- | ----------------------------------------- | --------
   union  | 4-mode pre-quant ~40240-dim
```

### §1.2 R33 anchor frozen — O1↔O2 α-band coherence

- **frozen pair**: O1↔O2 (occipital, Berger 1929 eyes-closed dominant)
- **method**: Welch NFFT=512 hann 50% overlap, 8-12Hz band-mean
- **floor**: ≥0.45 (Schartner 2017 conscious-state)
- **falsifier**: 코히런스<0.45 → REJECT, fall-back P3↔P4→Pz↔Cz
- **source**: `anima-clm-eeg/docs/eeg_arrival_impact_5fold.md` §4

### §1.3 tokenization scheme — RVQ (anima-voice Mk.III mirror, scaled-down)

```
  RVQ scheme (frozen candidate)
   ┌─────────────────────────────────────┐
   │  vocab_size  = 1024 per stage       │
   │  n_stages    = 4                    │  (VLM 8-stage 축소판)
   │  d_model     = 384                  │  (VLM 통일)
   │  ctx         = 120 token            │  (30s @ 4Hz token-rate)
   │  epoch       = 1s, shift = 0.25s    │  (token-rate = 1/0.25 = 4Hz)
   │  vocab_total = 4 × 1024 = 4096      │
   └─────────────────────────────────────┘
```

**rationale RVQ vs alternatives**:
- **RVQ (선정)** — anima-voice Mk.III audio_token_predictor 1576L raw#9 already-landed pattern reuse, 4-stage = 8-stage 측 EEG bandwidth 측 절반 (audio 16kHz vs EEG 250Hz, 64x slower → stage 절반 균형)
- VQ-VAE (탈락) — separate encoder/decoder train 필요, P9 SFT pipeline mismatch
- raw bin (탈락) — 20000-dim dense AR 측 ctx blow-up, vocab discretization 측 부재

---

## §2 stage 2 spec FROZEN candidate — EEG-conditioned LM head

### §2.1 architecture (S2.1-S2.4)

```
   spec    | name              | detail                                              | source
  ------- | ----------------- | --------------------------------------------------- | --------
   S2.1   | AR transformer    | 6-layer × 8-head × 384d (anima-voice Mk.III mirror) | VLM
          |                   | ctx=120, EEG token in → next EEG token out          |   pattern
   S2.2   | cross-attn bridge | EEG embedding 384d → text vocab projection          | Mk.XI
          |                   | Llama-3.2-1B family vocab = 128256                  |   v10
   S2.3   | CFG + KV-cache    | classifier-free guidance sentinel +                 | VLM
          |                   | KV-cache O(1) streaming (VLM Mk.III 패턴 reuse)    |   reuse
   S2.4   | invocation seam   | anima-eeg/realtime.hexa LSL stream →                | sister
          |                   | SLM tokenizer (cond.1) →                            |   .roadmap
          |                   | SLM AR decoder (S2.1) →                             |   .eeg
          |                   | text/intent decode (1-cycle E2E PASS)               |   B1-B4
```

### §2.2 invocation seam ASCII

```
                   stage 1                  stage 2
 ┌──────────────┐ ┌────────────────┐  ┌─────────────────┐  ┌──────────┐
 │ anima-eeg    │ │ SLM tokenizer  │  │ SLM AR decoder  │  │ text /   │
 │ realtime.hexa│→│ (4-mode union  │ →│ (6L×8H×384d AR  │ →│ intent   │
 │ LSL stream   │ │  RVQ 4096vocab)│  │  + CFG + KV-cache)│  │ decode   │
 │ 16ch×1250Hz  │ │ ctx=120 tokens │  │  ↓ cross-attn    │  │ (Llama-  │
 └──────────────┘ └────────────────┘  │  vocab=128256    │  │  3.2-1B  │
                                       └─────────────────┘  │  vocab)  │
                                                             └──────────┘
                  ↑                     ↑
           cond.1 FROZEN          cond.2 FROZEN
            candidate              candidate
                                       ↑
                              .roadmap.eeg cond.1
                              B1-B4 4관문 PASS
                              prerequisite
```

---

## §3 blk.1 corpus candidate audit — 4 candidates

```
   #  | dataset                              | N subj | type           | risk    | rank
  --- | ------------------------------------ | ------ | -------------- | ------- | ----
   1  | Brennan-Hale 2019 narrative listening| 49     | continuous     | LOW-MED | 1순위
      | (continuous speech-EEG paired,       |        |   speech-EEG   |         |  권장
      |  Alice in Wonderland audiobook)      |        |   paired       |         |
   2  | KaraOne                              | 12     | imagined       | MEDIUM  | 2순위
      | (imagined phoneme/word, U Toronto)   |        |   phoneme/word |         |
   3  | MOABB benchmark suite                | varies | aggregator     | LOW     | infra
      | (multi-dataset BCI software framework)|       |   (multi-DS)   |         |  reuse
   4  | BCI Competition III/IV               | <10    | imagined       | HIGH    | 3순위
      | (imagined speech, classic BCI)       |        |   speech       |         |
```

**1순위 권장 = Brennan-Hale 2019** (N=49 continuous narrative listening) — 측 사유:
- N=49 측 imagined speech BCI <10 subj 측 5x 큼
- continuous (not trial-based) → AR LM head 측 자연 fit (sequence prediction)
- speech-EEG paired ground truth 측 audiobook timestamp align
- license open (CC-BY 일반)

**vendoring 절대 금지** (P9 vendored 측 패턴 답습 X):
- 모든 EEG corpus 측 published baseline reference only
- training data 측 user-provided path 측 입력만 허용 (CLI flag `--corpus-path` 등)
- repo 內 corpus binary commit 0건

---

## §4 .roadmap.slm_speech_eeg_lm delta 요약

```
  cond     | before                       | after                                   | delta
  ------- | ---------------------------- | --------------------------------------- | -----
  cond.1  | partial / blocker_reason:    | partial / blocker_reason:               | +3 evidence
          |   tokenization scheme +      |   IMPL 단계 4-mode union vs single-     | +S1.1-S1.4
          |   R33 reuse 결정점          |   mode subset 결정점 (post-cond.2)      |   spec land
  cond.2  | unmet                        | partial                                 | status 상승
          | blocker_reason: cond.1 +    | blocker_reason: cond.1 FROZEN 확정 +   | +4 evidence
          |   .roadmap.eeg PASS         |   .eeg PASS + cond.3 corpus 결정 후    | +S2.1-S2.4
          |                              |   IMPL 가능                             |   spec land
  cond.3  | unmet                        | unmet                                   | +1 evidence
          |                              |                                         |   (corpus 4
          |                              |                                         |   candidate)
  blk.1   | desc: RVQ vs VQ-VAE vs raw  | desc: 4 candidate audited:              | corpus
          |   bin 결정점 + corpus small  |   Brennan-Hale 1순위 / KaraOne 2순위 / | candidate
          |   N risk                     |   MOABB infra / BCI Comp 3순위          | audit done
  raw_inv | 6 invariants                 | 9 invariants (+stage 1 spec +stage 2    | +3
          |                              |   spec +corpus vendoring 금지)          |
```

---

## §5 caveats (raw#10 honest C3) — 5건

1. **C1 — spec FROZEN candidate, IMPL 측 별도 cycle 필요** — stage 1 + stage 2 spec 측 frozen 표기 했으나 disk 측 module 구현 0건. cond.1/cond.2 상태 측 partial 유지 사유. IMPL = `slm_tokenizer.hexa` + `slm_ar_decoder.hexa` 신규 module 필요 (별도 land cycle).

2. **C2 — sister .roadmap.eeg cond.1 B1-B4 4관문 PASS prerequisite 미해소** — `.roadmap.eeg` cond.1 측 unmet 유지, evidence 0건. SLM cond.2 invocation seam 측 B1-B4 PASS 후 가능. .roadmap.eeg in-place 변경 금지 directive 측 본 cycle 정합 (additive only).

3. **C3 — corpus 4 candidate 측 published baseline reference only, 본 cycle 측 dataset download/verify 0건** — Brennan-Hale 2019 N=49 측 1순위 권장 했으나 실측 N + license + audio quality 측 본 cycle 미검증. cond.3 training 측 corpus 결정 후 별도 audit cycle 필요.

4. **C4 — 4-stage RVQ 측 anima-voice 8-stage 측 절반 산정 측 heuristic** — audio 16kHz vs EEG 250Hz 64x slower → stage 절반 = 4-stage 측 EEG bandwidth 측 적정 추정 했으나 실험적 검증 0건. IMPL 단계 측 stage 수 측 sweep 필요 (2/4/6/8 stage 4-mode 각각 reconstruction loss 측 비교).

5. **C5 — d_model=384 통일 측 VLM 측 design choice 측 답습 측 EEG 측 적정성 미검증** — VLM 측 audio token 측 dense info → 384d 충분, EEG 측 sparse + low-bandwidth → 384d 측 over-parameterized 가능성. 256d / 192d / 128d 측 ablation 측 IMPL 단계 권장.

---

## §6 next-cycle recommendation

1. **.roadmap.eeg B1-B4 4관문 PASS** — sister prerequisite 해소, SLM cond.2 IMPL unblock
2. **Brennan-Hale 2019 corpus dataset audit** — N=49 측 실측 + license + audio-EEG sync timestamp + windowing 측 별도 audit cycle
3. **slm_tokenizer.hexa + slm_ar_decoder.hexa IMPL land** — anima-voice/audio_token_predictor.hexa 1576L mirror, scaled-down (8-stage→4-stage)
4. **stage 수 sweep + d_model ablation** — IMPL 단계 측 2/4/6/8 stage × 128/192/256/384 d_model 측 16-cell matrix
5. **P9 SFT pipeline reuse 검증** — LoRA path on Llama-3.2-1B (Mk.XI v10 백본 family 공유) + SLM cross-attn bridge 측 P9 hook compatibility 확인

---

## §7 sister roadmap untouched verify

```
   .roadmap                  | this cycle | reason
  ------------------------- | ---------- | ------
   .roadmap.eeg             | UNTOUCHED  | B1-B4 4관문 SSOT, in-place 변경 금지 directive
   .roadmap.voice           | UNTOUCHED  | VLM × voice dual SSOT, sister cycle 별도
   .roadmap.vlm_voice_lm    | UNTOUCHED  | VLM stage 1+2 측 별도 cycle 권장
   .roadmap.blm_brain_lm    | UNTOUCHED  | F-CT-3 sister falsifier reference only
   .roadmap.nlm/tlm/blm     | UNTOUCHED  | sibling LM, 5-LM ecosystem reference only
   .roadmap.p9_sft          | UNTOUCHED  | training pipeline reuse reference only
```

---

## §8 cycle 메타

```
   cycle         | BG-AN-LM4 (SLM stage 1+2 spec freeze + corpus audit)
   policy        | additive only / BR-NO-USER-VERBATIM / Korean response /
                 |   silent-land marker / $0 mac-local / destructive 0
   cap           | 60min (under)
   cost          | $0 mac-local
   files modified| 1 (.roadmap.slm_speech_eeg_lm cond detail land additive)
   files created | 2 (this doc + marker)
   files untouched| 6+ (.roadmap.eeg + .roadmap.voice + sibling LM 5 + P9)
   marker        | state/markers/slm_stage12_landed.marker
   handoff       | docs/slm_stage12_landed_2026_05_03.ai.md (this doc)
   migration     | 0 (마이그레이션 절대 금지 directive 정합)
```

end-of-doc.
