# anima 2 *LM Roadmap Landed (VLM + SLM) — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: 2 new `.roadmap.*` (additive only) + 41 existing untouched + BG-AN-LM3 emit pair
>
> **terminology note (added 2026-05-03 cite cleanup cycle)** — 본 doc 의 원래 표기는 "anima-speak axis / Mk.III / 부서" 였음. 사용자 directive (speak -> voice 일괄 변경) 에 따라 conceptual term + on-disk dir 모두 `anima-voice` 로 통일됨. on-disk dir 506 file rename anima-speak/ -> anima-voice/ 는 본 cycle 시작 시점에 이미 다른 process 에 의해 staged 상태였음 (separate git commit 권장). 새 SSOT roadmap: `.roadmap.vlm_voice_lm` + `.roadmap.voice`.

---

## TL;DR

**오늘 한 일** — BG-AN-LM3 emit (anima 측 2 신규 *LM 후보 fan-out) 받아서, anima-voice axis 측 **VLM (Voice LM)** + anima-eeg axis 측 **SLM (Speech-EEG LM)** 두 개 mk2 `.roadmap.*` 신규 land. 양쪽 모두 sister .roadmap (`.roadmap.voice` / `.roadmap.eeg`) 측 in-place 변경 0건, additive only. anima-voice Mk.III audio_token_predictor (1576L raw#9 already-landed) + anima-eeg Phase 4 9-module wrapper (already-landed) 측 LM-style reframing.

**비유** — 기존에 7명 신입사원 (NLM/TLM/BLM 신규 + ELM/MLM/OLM/WLM absorbed) 입사 끝났는데, 회사 부서 audit 결과 anima-voice 부서 (Mk.III vocoder 부장) + anima-eeg 부서 (Phase 4 9-module 팀) 측 LM-style 후속 헤드 2명 추가 입사 필요 발견. 두 명만 신규 사원증 (.roadmap.*) 발급, 기존 부서장(.roadmap.voice / .roadmap.eeg) 측 사원 명부 변경 0건.

**결과** — 41 → 43 .roadmap.* (+2). 2/2 JSON valid, 모두 mk2 header 형식 (peer perspective + sister_lm cross-link 5명 + raw_invariants 5건 + ai_native_handoff). ALM 동기 1명 (.roadmap.n51_alm_tension) 측 closed status 보존 (cleanup 정합).

---

## §1 BG-AN-LM3 emit 분석 (VLM/SLM disambiguation)

```
   *LM   | full name              | 위치 후보                               | 비고
  ------ | ---------------------- | --------------------------------------- | --------
   VLM   | Voice LM               | .roadmap.vlm_voice_lm                   | NEW (sister .roadmap.voice)
   SLM   | Speech-EEG LM          | .roadmap.slm_speech_eeg_lm              | NEW (sister .roadmap.eeg)
```

**중요 disambiguation 2건**:

1. **VLM = Voice LM (NOT Vision LM)** — BG-AN-LM3 emit context 측 anima-voice axis sister 명시. 향후 Vision LM 후보 land 시 e.g., `.roadmap.vislm_vision_lm` 별도 namespace 권장.

2. **SLM = Speech-EEG LM (NOT Small LM)** — BG-AN-LM3 emit context 측 anima-eeg measurements sister 명시. industry 측 "SLM = Small Language Model" 통상이지만 본 cycle 측 EEG-conditioned LM 측 name 결정. 향후 "Small LM" 후보 land 시 e.g., `.roadmap.smlm_small_lm` 별도 권장.

---

## §2 신규 2 .roadmap.* 한 줄 요약

```
   .roadmap                       | kind    | status | 핵심 한 줄
   ------------------------------ | ------- | ------ | ----------------------
 1 vlm_voice_lm                   | domain  | active | anima-voice Mk.III audio_token_predictor 위 LM-style head (sister .roadmap.voice)
 2 slm_speech_eeg_lm              | domain  | active | anima-eeg Phase 4 9-module measurement 위 EEG-conditioned LM head (sister .roadmap.eeg)
```

---

## §3 신규 트랙 detail (subagent / audit-bot 직접 reference 용)

### §3.1 vlm_voice_lm

```
   verdict     | SPEC_PHASE_BASELINE_PARTIAL
   evidence    | anima-voice/audio_token_predictor.hexa 1576L raw#9 Mk.III
               |   (AR + 8-stage RVQ delayed pattern + CFG + KV-cache O(1) streaming)
               | anima-voice/intent_encoder.hexa cross-attention memory interface
               | anima-voice/anima_voice.hexa Stage 2 wrapper (audio_token_predictor caller)
               | anima-voice/rvq_codebook.hexa indices → latent → vocoder downstream
               | BT-SPEAK-02 streaming AR audio + Law 49 Phi-checkpoint anchor
   ledger      | anima-voice Mk.III 측 already-landed + .roadmap.voice cond.2/cond.3 sister
   cost        | $0 spec → training $300-1500 (LoRA path on audio-text corpus, P9 SFT reuse)
   blocker     | intent-text bridge 384d → text vocab projection 결정점
   sister_lm   | nlm + tlm + blm + slm (5-LM ecosystem)
   sister_rdm  | .roadmap.voice (tool-ization SSOT, in-place 변경 X)
```

### §3.2 slm_speech_eeg_lm

```
   verdict     | SPEC_PHASE_BASELINE_PARTIAL
   evidence    | anima-eeg/collect.hexa 341L raw#9 wrapper (BrainFlow + .npy v1.0)
               | anima-eeg/realtime.hexa 708L raw#9 (LSL stream + bandpower)
               | anima-eeg/calibrate.hexa 627L raw#9 (impedance + sampling rate)
               | anima-eeg/closed_loop.hexa 811L raw#9 (selftest 11/11 PASS)
               | anima-eeg/dual_stream.hexa 694L raw#9 (selftest 10/10 PASS,
               |   pearson_r_phi_alpha=-0.00283672 falsifiable null)
               | anima-eeg/experiment.hexa 483L raw#9 (4 protocols orchestrator)
               | SSOT 4-way alignment (validate.hexa + eeg.hexa + README + config.json brain_like 85.6)
   ledger      | anima-eeg Phase 4 measurement 측 already-landed + .roadmap.eeg B1-B4 4관문 sister
   cost        | $0 spec → training $500-2500 (LoRA path on EEG-text paired corpus, P9 SFT reuse)
   falsifier   | F-CT-3 (EEG ↔ TRIBE BOLD r ≥0.5) sister (BLM cond.3 측 동일 anchor)
                 + EEG ↔ text alignment ≥0.5 + cross-substrate ≥0.85 r
   blocker     | EEG signal → token vocab quantization scheme 결정 (RVQ vs VQ-VAE vs raw bin)
                 + EEG-text paired corpus dataset slice (imagined speech BCI N-limited risk)
   sister_lm   | nlm + tlm + blm + vlm (5-LM ecosystem)
   sister_rdm  | .roadmap.eeg (B1-B4 4관문 SSOT, in-place 변경 X)
```

---

## §4 5-7 caveats (raw#10 honest C3) — 5건

1. **C1 — VLM 측 `.roadmap.voice` 와 dual SSOT (race risk)** — 기존 `.roadmap.voice` (tool-ization SSOT, voice tool registry 등록 + invocation seam + cross-component verification 3-cond) + 신규 `.roadmap.vlm_voice_lm` (LM head reframing) 측 두 SSOT 동시 land. 향후 audio token vocab + intent-text bridge spec update 시 양쪽 location update 필요. BG-AN-LM3 (`.roadmap.tlm_tension_lm` × `.roadmap.tensionlink` 측 동일 패턴) 와 같은 race 패턴.

2. **C2 — SLM 측 `.roadmap.eeg` 와 dual SSOT + B1-B4 4관문 prerequisite** — `.roadmap.eeg` cond.1 (B1-B4 4관문 PASS) 측 prerequisite, SLM cond.2 invocation seam 측 B1-B4 PASS 후 가능. dual SSOT race 와 prerequisite block 동시 risk.

3. **C3 — VLM/SLM 측 disambiguation cost** — VLM ≠ Vision LM (Voice LM), SLM ≠ Small LM (Speech-EEG LM) 측 industry-conflict naming. 향후 Vision LM / Small LM 후보 land 시 `vislm_vision_lm` / `smlm_small_lm` 별도 namespace 권장 (본 cycle 측 미수행, additive only). future *LM mapping audit cycle 측 cleanup 권장.

4. **C4 — VLM intent-text bridge 384d bottleneck risk (TLM 5d sister lesson)** — anima-voice Mk.III 측 d_model=384 bridge dim, intent-text projection 측 결정점. p10 v1 5d bottleneck saturated lesson (TLM cond.1 측 동일 risk anchor) 적용 권장. 384d 측 5d 보다 ample 하지만 text vocab (32k-128k) 측 projection 측 information bottleneck risk.

5. **C5 — SLM EEG-text paired corpus 측 published baseline weak** — imagined speech BCI dataset 측 small N (typical N=10-30 subjects), training 측 N-limited risk. cross-substrate fidelity ≥0.85 r 측 baseline (TLM/NLM/BLM/VLM 동일 척도) 달성 측 N-limited 측 boundary edge fragility (S7 N=11 PASS_TIGHT 측 sister lesson).

---

## §5 file index (relative to /Users/ghost/core/anima/)

### 신규 2 .roadmap.*

```
.roadmap.vlm_voice_lm
.roadmap.slm_speech_eeg_lm
```

### handoff doc + marker

```
anima/docs/anima_2_lm_vlm_slm_landed_2026_05_03.ai.md  (이 파일)
anima/state/markers/anima_2_lm_vlm_slm_landed.marker
```

### 본 cycle 이 reference 만 한 파일 (변경 X)

```
.roadmap.voice                          (tool-ization SSOT, sister VLM)
.roadmap.eeg                            (B1-B4 4관문 SSOT, sister SLM)
.roadmap.nlm_neuromorphic_lm            (sibling LM, 5-LM ecosystem)
.roadmap.tlm_tension_lm                 (sibling LM, 5-LM ecosystem)
.roadmap.blm_brain_lm                   (sibling LM + EEG cross-link)
anima-voice/audio_token_predictor.hexa  (1576L raw#9 Mk.III, VLM baseline)
anima-voice/intent_encoder.hexa         (cross-attention memory, VLM baseline)
anima-voice/anima_voice.hexa             (Stage 2 wrapper, VLM baseline)
anima-voice/rvq_codebook.hexa           (downstream codebook, VLM baseline)
anima-eeg/collect.hexa                  (341L raw#9, SLM baseline)
anima-eeg/realtime.hexa                 (708L raw#9, SLM baseline)
anima-eeg/calibrate.hexa                (627L raw#9, SLM baseline)
anima-eeg/closed_loop.hexa              (811L raw#9, SLM baseline)
anima-eeg/dual_stream.hexa              (694L raw#9, SLM baseline)
anima-eeg/experiment.hexa               (483L raw#9, SLM baseline)
docs/anima_3_lm_landed_2026_05_03.ai.md (BG-AN-LM3 predecessor handoff, untouched)
```

---

## §6 7-element friendly summary (사용자 view, ASCII)

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [+]2 NEW .roadmap.*  41 -> 43  zero modification
   2. analogy             | anima-voice Mk.III vocoder 부장 + anima-eeg Phase 4 팀 위에
                            LM-style 후속 헤드 2명 추가 입사 (사원증 발급)
   3. core 결과            | 2/2 JSON valid, mk2 peer perspective + sister_lm 5-LM cross-link
   4. 마이그레이션 0          | 41 기존 .roadmap.* + sister .roadmap.voice/eeg + anima-voice/eeg
                            disk artifacts 모두 0 byte modification
   5. handoff path         | 본 ai.md doc = 다음 subagent / audit cron 의 reference SSOT
   6. 다음 step             | (1) VLM intent-text bridge 384d → text vocab projection 결정
                           | (2) SLM EEG token quantization scheme 결정 (RVQ/VQ-VAE/raw bin)
                           | (3) .roadmap.eeg B1-B4 4관문 PASS 진척 watch (SLM cond.2 prerequisite)
                           | (4) .roadmap.voice cond.2 invocation seam 진척 watch (VLM cond.2 prerequisite)
                           | (5) future Vision LM / Small LM 후보 시 별도 namespace (vislm/smlm)
   7. cost                 | $0 mac-local enforced, destructive 0
```

---

## §7 marker file path

`anima/state/markers/anima_2_lm_vlm_slm_landed.marker`

(silent-land 방지 — handoff doc + 2 .roadmap.* 양쪽 land + marker emit 의 3-way attestation)

---

## §8 5-LM ecosystem snapshot (post-cycle, 7 *LM mapping 확장)

```
   *LM   | full name              | .roadmap                        | sister axis              | status
  ------ | ---------------------- | ------------------------------- | ------------------------ | --------
   ELM   | Embryonic LM           | .roadmap.n22_levin_xenobot      | xenobot substrate        | absorbed
   MLM   | Mycelium LM            | .roadmap.n23_slime_mycelium     | slime/mycelium substrate | absorbed
   OLM   | Octopus LM             | .roadmap.n24_octopus_iit_excl.  | octopus IIT exclusion    | absorbed
   WLM   | World LM               | .roadmap.w1_anima_as_substrate  | anima self substrate     | absorbed
   NLM   | Neuromorphic LM        | .roadmap.nlm_neuromorphic_lm    | .roadmap.akida           | active (BG-AN-LM3 pre)
   TLM   | Tension LM             | .roadmap.tlm_tension_lm         | .roadmap.tensionlink     | active (BG-AN-LM3 pre)
   BLM   | Brain LM               | .roadmap.blm_brain_lm           | .roadmap.i1_tribev2_pr   | active (BG-AN-LM3 pre)
   VLM   | Voice LM               | .roadmap.vlm_voice_lm           | .roadmap.voice           | active (THIS cycle)
   SLM   | Speech-EEG LM          | .roadmap.slm_speech_eeg_lm      | .roadmap.eeg             | active (THIS cycle)
```

**총합** — 9 *LM ecosystem (4 absorbed + 3 BG-AN-LM3 pre + 2 THIS cycle). ALM 동기 1명 (`.roadmap.n51_alm_tension`) 측 closed status 별도 처리.

---

## §9 next-cycle recommendations (impl 미수행, 별도 cycle)

1. **VLM intent-text bridge architecture freeze** — 384d bridge → text vocab (32k-128k) projection 측 결정점 (cond.1 → blocker resolution). p10 v1 5d bottleneck 측 sister lesson 적용.

2. **SLM EEG token quantization scheme freeze** — RVQ (anima-voice Mk.III pattern) vs VQ-VAE vs raw bin 3-mode 中 1 결정 (cond.1 → blocker resolution). R33 O1↔O2 channel pair frozen 측 reuse 결정.

3. **`.roadmap.voice` 측 sister-back-reference 추가** — `.roadmap.voice` cross_link.sister_lm = `vlm_voice_lm` 추가 권장 (current = additive only, dual SSOT race 완화).

4. **`.roadmap.eeg` 측 sister-back-reference 추가** — `.roadmap.eeg` cross_link.sister_lm = `slm_speech_eeg_lm` 추가 권장 (current = additive only, dual SSOT race 완화).

5. **mk2 schema 측 `sister_lm` field formalization** — BG-AN-LM3 cycle 측 informal cross-link, 본 cycle 측 5-LM ecosystem (nlm/tlm/blm/vlm/slm) 측 cross-link 확장. 별도 mk2 spec extension proposal cycle 권장.

6. **Vision LM / Small LM namespace pre-reserve** — VLM/SLM 측 industry-conflict naming 측 disambiguation cost 발생, 향후 `.roadmap.vislm_vision_lm` / `.roadmap.smlm_small_lm` 별도 namespace pre-reserve 권장.

7. **VLM × SLM cross-link audit** — anima-voice Mk.III audio_token_predictor + anima-eeg Phase 4 dual_stream pearson_r_phi_alpha=-0.00283672 측 falsifiable null 측 cross-substrate fidelity ≥0.85 r 측 baseline 측 audio ↔ EEG 측 cross-modal alignment 측 별도 axis 권장 (BLM × SLM 측 EEG 공통 substrate 와 동일 패턴).
