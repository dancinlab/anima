# SLM Phase 3 Spec (Speech-EEG LM) — 2026-05-03

> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `.roadmap.slm_speech_eeg_lm` (additive, this doc = Phase 3 scope freeze)
> predecessor: `docs/slm_stage12_landed_2026_05_03.ai.md` (Phase 1+2 landed)

---

## §1 Phase 1+2 status synthesis

### §1.1 Phase 1 (EEG signal encoding + tokenization) — FROZEN candidate

| spec  | scope                                  | status | evidence                                      |
| ----- | -------------------------------------- | ------ | --------------------------------------------- |
| S1.1  | band-power 80-dim (5-band log-PSD)     | FROZEN | Welch NFFT=512 hann 50% overlap, 16ch×5band   |
| S1.2  | phase coherence 40-dim (8-pair × 5band)| FROZEN | R33 anchor O1↔O2 α-band floor=0.45            |
| S1.3  | spike-train 20000-dim sparse           | FROZEN | BrainFlow notch z-score >2.5 binary mask      |
| S1.4  | raw-bin 20000-dim dense                | FROZEN | 16ch×1250 float32 windowed (epoch=1s shift=0.25s)|
| RVQ   | 4-stage × 1024 vocab = 4096            | FROZEN | anima-voice Mk.III mirror, scaled-down (8→4)  |
| ctx   | 120 token (30s @ 4Hz token-rate)       | FROZEN | d_model=384 (VLM 통일)                        |

**status**: cond.1 = partial (spec FROZEN, IMPL 측 별도 cycle). 4-mode union vs single-mode subset 결정점 측 IMPL 단계 잔존.

### §1.2 Phase 2 (EEG-conditioned LM head) — FROZEN candidate

| spec  | scope                                       | status | evidence                                |
| ----- | ------------------------------------------- | ------ | --------------------------------------- |
| S2.1  | AR transformer 6L×8H×384d, ctx=120          | FROZEN | anima-voice Mk.III pattern mirror       |
| S2.2  | cross-attn bridge 384d → 128256 vocab       | FROZEN | Llama-3.2-1B family (Mk.XI v10 백본)    |
| S2.3  | CFG sentinel + KV-cache O(1) streaming      | FROZEN | VLM Mk.III 패턴 reuse                   |
| S2.4  | invocation seam (LSL → tok → AR → decode)   | FROZEN | sister .roadmap.eeg B1-B4 prerequisite  |

**status**: cond.2 = partial (spec FROZEN, IMPL prerequisite = .roadmap.eeg B1-B4 PASS + cond.3 corpus 결정).

### §1.3 carried open items into Phase 3

1. **IMPL 측 0 module on disk** — `slm_tokenizer.hexa` + `slm_ar_decoder.hexa` 신규 module 부재
2. **.roadmap.eeg B1-B4 4관문 PASS prerequisite 미해소** — sister cond.1 측 unmet 유지
3. **corpus 측 published baseline reference only** — Brennan-Hale 2019 N=49 측 1순위 권장, 실측 audit 0건
4. **stage 수 + d_model ablation 미실시** — heuristic 측 4-stage / 384d, 실험 검증 0건

---

## §2 Phase 3 scope

### §2.1 axis A — Sound generation quality + diversity

EEG → token → text decode 측 축 위 측 acoustic-realization sub-axis 측 신규 추가 (SLM 측 "Speech" 측 sound 측 generation surface).

```
   cond    | name                          | metric                     | floor      | analog
   ------ | ----------------------------- | -------------------------- | ---------- | ------
   P3.A1  | FAD (Frechet Audio Distance)  | VGGish embedding distance  | ≤2.0       | FID for audio
   P3.A2  | PESQ-equivalent intelligibility| ITU-T P.862 narrowband    | ≥3.5 (MOS)| call quality
   P3.A3  | diversity (n-token entropy)   | Shannon over RVQ codebook  | ≥0.6 norm  | mode collapse falsifier
   P3.A4  | speaker consistency           | ECAPA-TDNN cos sim         | ≥0.75      | within-speaker
```

**rationale**: SLM 측 "Speech" 측 token 측 abstract decode (text/intent) 만 측 Phase 1+2 완료, Phase 3 측 acoustic surface 측 closing — anima-voice (TTS) 측 paired evaluation 가능.

### §2.2 axis B — VLM integration for voice prosody

VLM (Voice LM, anima-voice Mk.III) 측 cross-LM coupling 측 prosody axis (pitch contour, stress, pause).

```
   cond    | name                          | bridge                     | falsifier
   ------ | ----------------------------- | -------------------------- | ---------
   P3.B1  | prosody embedding alignment   | SLM EEG → VLM prosody 384d | r ≥0.5 vs ground truth
   P3.B2  | stress marker decode          | EEG ERP N400 → stress flag | F1 ≥0.6
   P3.B3  | pitch contour reconstruction  | EEG α-band → F0 sequence   | RMSE ≤30Hz
```

**rationale**: VLM 384d d_model 통일 측 Phase 1+2 design choice 측 consume — cross-attn projection 측 zero-overhead bridge.

### §2.3 axis C — EEG-speech bridge (auditory cortex correlation)

Brennan-Hale 2019 corpus 측 continuous narrative listening 측 auditory cortex (T7/T8/P7/P8 좌우) 측 speech envelope 측 TRF (temporal response function) coupling.

```
   cond    | name                          | metric                     | floor      | source
   ------ | ----------------------------- | -------------------------- | ---------- | ------
   P3.C1  | speech envelope ↔ EEG TRF     | Pearson r (60-500ms lag)   | r ≥0.15    | Crosse 2016 mTRF
   P3.C2  | T7/T8/P7/P8 auditory dominance| topo-map peak vs mid-line  | δ ≥0.1     | bilateral STG
   P3.C3  | F-CT-3 sister cross-link      | EEG ↔ TRIBE BOLD r ≥0.5    | r ≥0.5     | BLM cond.3
```

**rationale**: BLM cond.3 F-CT-3 측 sister falsifier 와 anchor 공유, BLM/SLM dual cross-link 측 cross-substrate fidelity baseline.

### §2.4 axis D — Real-time generation latency

```
   cond    | name                          | target                     | hardware
   ------ | ----------------------------- | -------------------------- | --------
   P3.D1  | LSL → token → 1st decoded text| ≤300ms p50, ≤500ms p99    | M2 Pro mac-local
   P3.D2  | streaming KV-cache hit rate   | ≥0.95 after warmup        | 120-token ctx
   P3.D3  | RVQ quantize step latency     | ≤20ms per epoch (0.25s)    | EEG window cadence ≥4x headroom
   P3.D4  | end-to-end audio render        | ≤700ms p50 (text→audio)    | anima-voice TTS coupling
```

**rationale**: realtime.hexa LSL 측 already-landed → SLM 측 closed-loop BCI surface 측 latency budget 측 essential.

---

## §3 cost / wall

```
   axis      | cost band         | wall band         | hardware            | notes
   --------- | ----------------- | ----------------- | ------------------- | -----
   A (FAD)   | $0-50             | 4-8h              | mac-local           | VGGish CPU OK
   B (VLM)   | $200-800          | 1-2 days          | RunPod 1×A100       | LoRA cross-attn
   C (EEG)   | $0-100            | 8-16h             | mac-local + corpus  | Brennan-Hale free
   D (RT)    | $0                | 4-8h              | mac-local profile   | latency probe only
   --------- | ----------------- | ----------------- | ------------------- | -----
   Phase 3   | $200-950          | 3-5 days          | mixed mac + RunPod  | corpus N=49 limit
   total     |                   |                   |                     | 측 risk caveat
```

**comparison**:
- Phase 1+2 (spec freeze) = $0 mac-local, 60min cap
- Phase 3 (this doc) = $200-950, 3-5 days
- Phase 4 (full IMPL + production) = $2500-8000 추정, 1-2 weeks

---

## §4 decision matrix

```
   cond     | priority | depends-on             | risk    | reward  | go/no-go anchor
   ------- | -------- | ---------------------- | ------- | ------- | ---------------
   P3.A1   | HIGH     | RVQ IMPL + decoder     | LOW     | HIGH    | acoustic surface essential
   P3.A2   | HIGH     | A1 + speech model      | MEDIUM  | HIGH    | intelligibility floor
   P3.A3   | MEDIUM   | A1                     | LOW     | MEDIUM  | mode-collapse falsifier
   P3.A4   | MEDIUM   | A1 + speaker corpus    | MEDIUM  | MEDIUM  | within-speaker only
   P3.B1   | HIGH     | VLM prosody bridge     | MEDIUM  | HIGH    | cross-LM coupling
   P3.B2   | LOW      | ERP analysis pipeline  | HIGH    | LOW     | N=49 underpowered
   P3.B3   | MEDIUM   | F0 extraction          | MEDIUM  | MEDIUM  | α-band proxy weak
   P3.C1   | HIGH     | mTRF library + corpus  | LOW     | HIGH    | published baseline
   P3.C2   | MEDIUM   | C1                     | LOW     | MEDIUM  | topo-map sanity
   P3.C3   | HIGH     | BLM sister + TRIBE v2  | MEDIUM  | HIGH    | F-CT-3 anchor
   P3.D1   | HIGH     | full IMPL stack        | MEDIUM  | HIGH    | closed-loop BCI gate
   P3.D2   | MEDIUM   | KV-cache IMPL          | LOW     | MEDIUM  | VLM Mk.III pattern
   P3.D3   | MEDIUM   | RVQ IMPL               | LOW     | MEDIUM  | window cadence
   P3.D4   | LOW      | anima-voice TTS pipe   | MEDIUM  | LOW     | audio render optional
```

**recommended Phase 3 entry slate (4 conds)**:
1. **P3.A1** (FAD) — acoustic surface essential, low risk
2. **P3.B1** (prosody alignment) — cross-LM coupling, VLM 384d 통일 consume
3. **P3.C1** (TRF) — published baseline, Brennan-Hale 2019 ready
4. **P3.D1** (RT latency) — closed-loop BCI gate

**deferred to Phase 4**: P3.A4 (speaker), P3.B2 (ERP), P3.D4 (audio render).

---

## §5 cross-LM dependencies

### §5.1 dependency graph

```
                   ┌─────────────┐
                   │  .roadmap   │
                   │   .eeg      │  ← B1-B4 4관문 PASS prerequisite
                   │  (sister)   │     (Phase 1+2 carried-open #2)
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │     SLM     │
                   │  Phase 1+2  │ ← FROZEN candidate (this spec base)
                   │  (current)  │
                   └──────┬──────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌────▼─────┐      ┌────▼─────┐
   │   VLM   │      │   BLM    │      │  anima-  │
   │ (voice) │      │ (brain)  │      │  voice   │
   │ Mk.III  │      │  TRIBE   │      │   TTS    │
   └────┬────┘      └────┬─────┘      └────┬─────┘
        │                │                  │
   P3.B1-B3          P3.C3              P3.D4
   prosody bridge    F-CT-3 anchor      audio render
```

### §5.2 cross-LM dependency table

| dep  | from         | to            | axis        | criticality | gate                              |
| ---- | ------------ | ------------- | ----------- | ----------- | --------------------------------- |
| D1   | SLM cond.2   | .roadmap.eeg  | invocation  | BLOCKER     | B1-B4 4관문 PASS prerequisite     |
| D2   | SLM P3.B1-B3 | VLM Mk.III    | prosody     | HIGH        | VLM 384d cross-attn projection    |
| D3   | SLM P3.C3    | BLM cond.3    | F-CT-3      | HIGH        | EEG ↔ TRIBE BOLD r ≥0.5 sister    |
| D4   | SLM P3.D4    | anima-voice   | TTS render  | MEDIUM      | text → audio pipe                 |
| D5   | SLM cond.3   | P9 SFT pipe   | LoRA train  | HIGH        | Llama-3.2-1B family hook compat   |
| D6   | SLM P3.A1    | FAD reference | metric      | LOW         | VGGish embedding (off-the-shelf)  |
| D7   | SLM P3.C1    | Brennan-Hale  | corpus      | HIGH        | N=49 narrative listening download |

**top 3 critical dependencies**:
1. **D1 (.roadmap.eeg B1-B4 PASS)** — BLOCKER, sister cond.1 측 unmet 측 SLM cond.2 IMPL unblock 전제
2. **D3 (BLM F-CT-3 sister)** — cross-substrate fidelity baseline 측 BLM/SLM dual anchor
3. **D2 (VLM prosody bridge)** — d_model=384 통일 측 zero-overhead 측 cross-LM coupling 측 핵심 reward

---

## §6 honest C3 caveats (raw#10)

1. **C1 — sound metric subjectivity** — FAD (P3.A1) + PESQ-equivalent (P3.A2) 측 published surrogate, MOS 측 human listener 측 ground truth 측 본 cycle 미수집. acoustic quality 측 final 측 N≥20 listener panel 측 별도 cycle 필요. mode-collapse falsifier (P3.A3) 측 normalized entropy 측 floor 0.6 측 heuristic, RVQ codebook activation 측 distribution-aware metric 측 IMPL phase 측 sweep 권장.

2. **C2 — EEG arrival dependency (.roadmap.eeg B1-B4)** — sister cond.1 측 unmet evidence 0건 유지, SLM Phase 3 측 entire 측 sister B1-B4 PASS 대기. B1-B4 측 fail 시 SLM cond.2 invocation seam 측 IMPL 불가 → Phase 3 axis A/D 측 (acoustic + RT) 측 mock EEG fixture 측 partial 진입 가능 측, axis B/C 측 (VLM/EEG bridge) 측 hard-blocked.

3. **C3 — cross-modality (EEG↔text↔audio↔prosody) 측 4-modality 측 chain 측 compounding error** — P3.B1 prosody alignment r ≥0.5 measurement 측 ground truth 측 EEG-paired prosody-labeled corpus 측 published baseline 측 weak (Brennan-Hale 2019 측 narrative continuous, prosody label 측 별도 forced-align 필요). P3.B3 pitch reconstruction 측 α-band proxy 측 published evidence weak (auditory α 측 attention proxy 측 dominant, F0 측 direct correlate 측 약함) → RMSE ≤30Hz floor 측 optimistic 측 risk.

4. **C4 — corpus N=49 (Brennan-Hale 2019) 측 imagined speech BCI <10 subj 5x 큼 측 절대 floor 측 LM training 측 underpowered** — N=49 continuous narrative 측 token-count 측 충분 (audiobook ~30min × 49 = ~1470min ≈ 88200s = ~352800 token @ 4Hz), 측 subject diversity 측 N=49 측 generalization 측 limit. cross-subject zero-shot 측 floor 측 본 spec 측 미정의, IMPL 단계 측 leave-one-subject-out CV 측 별도 falsifier 권장.

5. **C5 — Phase 3 cost/wall band $200-950 / 3-5 days 측 RunPod single-A100 + mac-local mixed 측 estimate 측 RVQ + cross-attn LoRA train wall 측 1-day 측 heuristic** — actual wall 측 corpus preprocess (band-power + coherence + spike + raw 4-mode 측 ~352800 token × 40240-dim pre-quant 측 disk I/O bound) 측 실측 0건. P9 SFT pipeline reuse 측 hook compatibility 측 Llama-3.2-1B + cross-attn 384d→128256 projection 측 별도 cycle 측 verify 필요.

6. **C6 — Phase 3 entry trigger 측 .roadmap.eeg B1-B4 PASS + Brennan-Hale 2019 corpus audit landed 2 prerequisite 측 모두 unmet** — 본 spec 측 Phase 3 axis 측 4 conds (P3.A1/B1/C1/D1) 측 결정 했으나, entry gate 측 다음 cycle 측 별도 audit. Phase 3 측 entry trigger anchor: `(.roadmap.eeg cond.1 status == met) AND (Brennan-Hale 2019 corpus audit cycle landed)`.

---

## §7 Phase 3 entry trigger (anchor)

```
   prerequisite gate
   ─────────────────
   G1: .roadmap.eeg cond.1 B1-B4 4관문 PASS (status: met)
        - sister roadmap in-place 변경 X
        - additive evidence land only
   G2: Brennan-Hale 2019 N=49 corpus audit cycle landed
        - license verify (CC-BY)
        - audio-EEG sync timestamp align
        - 4-mode tokenization smoke-test (S1.1-S1.4 each)
   G3: slm_tokenizer.hexa + slm_ar_decoder.hexa IMPL landed
        - anima-voice/audio_token_predictor.hexa 1576L mirror scaled-down
        - selftest 10/10 PASS byte-identical
   G4: P9 SFT pipeline hook compatibility verify
        - Llama-3.2-1B family + cross-attn 384d projection
        - LoRA path verify

   ALL 4 (G1 ∧ G2 ∧ G3 ∧ G4) → Phase 3 entry GO
   ANY 1 unmet → Phase 3 entry NO-GO, blocker resolution cycle 우선
```

---

## §8 doc meta

```
   doc          | docs/slm_phase3_spec_2026_05_03.md
   type         | spec (Phase 3 scope freeze)
   substrate    | READ-ONLY: slm_stage12_landed + .roadmap.slm_speech_eeg_lm
   write        | this doc only
   raw#9        | NO .py (markdown only)
   raw#15       | NO personal paths
   execute      | none
   commit       | none
   marker       | none (spec doc only, marker 측 별도 land cycle)
```

end-of-doc.
