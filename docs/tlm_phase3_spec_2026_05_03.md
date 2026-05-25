# TLM (Tension LM) Phase 3 Spec — 2026-05-03

> spec doc, friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `.roadmap.tlm_tension_lm` (cond.3 spec target) + Phase 1+2 landed handoff
> predecessor: `docs/tlm_stage12_landed_2026_05_03.ai.md` (Stage 1+2 freeze)
> sister SSOT: `.roadmap.tensionlink` (R=0.999 transfer protocol — in-place 변경 X invariant 유지)

---

## TL;DR

[ADVANCE] TLM Phase 3 = (a) cond.3 cross-substrate fidelity vs CLM ≥0.85 r + (b) F3 tension MSE absolute reduction (CLM Phase 1.6 측 8.75 stuck → TLM 측 ≤2.0 target via tension target re-extraction) + (c) 5-channel WHAT/WHERE/WHY/TRUST/WHO deep validation (per-channel ablation + random-control 4-arm) + (d) anima_voice + anima_speak downstream coupling (TLM hidden → prosody/voice axis).

비유 — Phase 1+2 측 수신탑 청사진 (encoder + LM head) 동결 완료. Phase 3 측 (1) 수신탑 첫 가동 (training + fidelity) + (2) 신호 노이즈 제거 (F3 MSE absolute reduction, target circular issue 측 re-extraction 으로 해결) + (3) 5채널 각각 진단 (per-channel ablation) + (4) 송출 라인 연결 (anima_voice/anima_speak downstream).

결과 — 4 conds (cond.3 cross-LM fidelity / cond.4 F3 absolute reduction / cond.5 5-channel deep validation / cond.6 downstream voice/speak coupling), 5 cross-LM dependencies (BLM F-CT-3 sister + tensionlink R=0.999 source / VLM prosody seam / SLM EEG-tension bridge / P9 SFT pipeline reuse / anima_voice + anima_speak downstream), entry trigger = (G1 ∧ G2 ∧ G3 ∧ G4) 4-gate.

---

## §1 Phase 1+2 status synthesis

### §1.1 Phase 1+2 landed summary

```
   cond                         | status | spec frozen content
   ---------------------------- | ------ | -----------------------------------------------
   cond.1 5-channel encoder     | met    | per-ch 8-bit codebook (256 size, 64-d embed) + concat 320 → LN → Linear(320, 512)
   cond.2 LM head architecture  | partial| decoder-only LOCKED (P9 LoRA r∈{16,32,64} sweep template reuse)
   cond.3 cross-substrate r     | unmet  | Phase 3 target (this spec)
   blk.1 head arch decision     | resolved| decoder-only (4-axis rationale: P9 reuse + P10 v2 family + tensionlink unidir + sibling consistency)
   blk.2 corpus + budget decision| open   | 3 candidates pending (CLM self-chat / UDP capture / mind.tension trajectory)
```

### §1.2 invariants carried forward

```
   anchor                          | source                                    | Phase 3 reuse
   ------------------------------- | ----------------------------------------- | ------------------
   5-channel WHAT/WHERE/WHY/TRUST/WHO | narrative §16 ALM + .roadmap.tensionlink | encoder input contract (변경 X)
   per-ch 8-bit codebook 256 / 64-d  | docs/tlm_stage12_landed §2.1            | encoder spec FROZEN
   320-d concat → 512-d LN proj      | P10 v1 5-d saturation lesson 회피        | bottleneck mitigation
   decoder-only LM head              | P9 SFT + P10 v2 family + sibling LM     | head spec FROZEN
   sister .roadmap.tensionlink R=0.999| 519µs / 1927fps / source-side wire      | additive-only invariant
   sibling 4 LM (NLM/BLM/SLM/VLM)    | decoder-only consistency                 | cross-LM 측 r ≥0.85 baseline
```

Phase 1+2 측 in-place 변경 0건 invariant Phase 3 에도 유지 — sister .roadmap.tensionlink + 6 referenced .roadmap.* + narrative §16/§44.1/§44.2 모두 0 byte modification.

### §1.3 carried open items into Phase 3

1. **IMPL 측 0 module on disk** — TLM encoder + LM head spec freeze 만 land, 실제 module 부재
2. **blk.2 corpus 결정점** — 3 candidates (CLM self-chat tension pair / tension_link UDP capture replay / anima-runtime mind.tension trajectory window) 측 size/quality/availability 평가 0건
3. **per-ch codebook size 측 256 first guess** — actual 5ch value entropy 측정 0건, small sweep (256/64/1024) 미실시
4. **§16.2 random-control MANDATORY 측 cond.3 spec 측 미명시** — Phase 3 측 사전 명시 필수
5. **F3 tension MSE absolute reduction 측 dedicated path 미정의** — CLM Phase 1.6 측 β tuning path 측 stuck (5.39 → 8.75), tension target re-extraction path 측 TLM 측 가능성

---

## §2 Phase 3 scope

### §2.1 cond.3 — cross-substrate fidelity vs CLM ≥0.85 r

```
   item              | spec
   ----------------- | --------------------------------------------------
   target            | TLM next-token loss / perplexity vs CLM ≥0.85 r
   measure cohort    | 5ch token-paired held-out (corpus 결정 후 split)
   training budget   | LoRA r∈{16,32,64} α∈{16,64,128} lr∈{5e-5,1e-4,5e-4} P9 LHS-9
   eval cadence      | per-checkpoint vs CLM held-out text token AR
   sibling parity    | NLM/BLM/SLM/VLM ≥0.85 r 척도 와 동일 floor (cross-LM consistency)
   random-control    | 4-arm MANDATORY: (R1) random tension_link / (R2) shuffled 5ch / (R3) random codebook indices / (R4) constant 5ch
```

§16.2 anchor #2 (random-control MANDATORY) 측 사전 명시 — R1/R2/R3/R4 4-arm 측 cond.3 spec 일부, IMPL phase 측 4-arm parallel sweep (LHS-9 grid × 4-arm = 36-cell, optional thinning).

### §2.2 cond.4 — F3 tension MSE absolute reduction (≤2.0 target)

```
   item              | CLM Phase 1.6 baseline | TLM Phase 3 target
   ----------------- | ---------------------- | --------------------------------
   F3 tens MSE       | 5.39 → 8.75 (worse)    | ≤2.0 absolute (target re-extract path)
   path              | β tuning (0.30 → 0.10) | tension target re-extraction
   gating            | deferred (non-blocking)| HARD gate (TLM 측 raison d'être)
   loss family       | ill-conditioned (circular)| TLM-native (5ch input → 5ch reconstruction)
```

**핵심 framing**: CLM Phase 1.6 측 §2.2 reasoning — "tension target circular; F3 fix needs target re-extraction, not β tuning". TLM 측 5ch input → 5ch reconstruction 측 native task 이므로 circular target 회피 가능 (encoder 측 5ch 직접 입력 + decoder 측 5ch 직접 reconstruction). CLM 측 base forward 측 추출된 tension 측 같은 base 측 다시 예측 측 ill-conditioned 패턴 측 TLM 측 구조적으로 회피.

```
   F4-equivalent path (TLM-native)
   --------------------------------
   F4.1 reconstruction MSE   ≤2.0 absolute (5ch input → encoder → head → 5ch reconstruction)
   F4.2 per-channel MSE       ≤2.5 each of WHAT/WHERE/WHY/TRUST/WHO (no channel collapse)
   F4.3 R1 random arm gap     ≥3.0 absolute (TLM ≤2.0, R1 random ≥5.0)
   F4.4 monotone-non-increase across save points 5K/13K/25K/50K (tie-break)
```

### §2.3 cond.5 — 5-channel WHAT/WHERE/WHY/TRUST/WHO deep validation

```
   item              | spec
   ----------------- | --------------------------------------------------
   per-channel ablation| 1 channel mask × 5 → reconstruction degradation 측정
   per-channel entropy | actual 5ch value distribution 측 entropy ≥4.0 bits 각각 (256-code 측 ≤8.0 bits 측 50% 이상)
   codebook size sweep | small sweep 64 / 256 / 1024 — entropy + reconstruction MSE optimum
   channel correlation | 5ch 간 cross-correlation matrix — diagonal dominance ≥0.7
   §16.2 random-control| 5ch shuffled / random codebook / constant 5ch 측 4-arm 사전 명시 (cond.3 와 통합)
```

per-channel ablation 측 sister .roadmap.tensionlink R=0.999 baseline 측 5ch source 측 information-theoretic relevance 측 직접 검증. WHAT (semantic) / WHERE (spatial) / WHY (causal) / TRUST (epistemic) / WHO (agentic) 측 5축 측 LM-style next-token 측 contribution 측 quantify.

### §2.4 cond.6 — anima_voice + anima_speak downstream coupling

```
   item              | spec
   ----------------- | --------------------------------------------------
   anima_voice 측 axis | TLM hidden state (512d) → VLM prosody axis (384d) bridge
   bridge architecture| Linear(512, 384) + LayerNorm — additive on VLM Stage 0.5 emotion_prosody
   anima_speak 측 axis | TLM tension trajectory → speak cite cleanup gate (tension threshold)
   speak cite gate   | TLM 측 tension >0.7 → cite verbose mode / <0.3 → cite minimal mode
   coupling timing   | sequential — VLM Phase 3 cond.5 (SLM prosody) land 후 TLM cond.6 entry
   conflict resolve  | TLM tension 측 SLM prosody priority 보다 낮음 (downstream consumer, not source)
```

downstream coupling 측 additive only — anima-voice/emotion_prosody.hexa Stage 0.5 측 in-place 변경 X (TLM bridge 측 separate residual projection). anima_speak 측 cite cleanup gate 측 tension threshold 측 conditional, 기본 path 측 TLM-independent 유지 (graceful degradation).

---

## §3 cost / wallclock

```
   phase                        | cost band         | wallclock band       | dominant cost
   ---------------------------- | ----------------- | -------------------- | -----------------------------
   cond.3 (cross-LM fidelity)   | $650-3000        | 24-72 GPU-hours      | LoRA LHS-9 sweep on 5ch corpus (P9 sister)
   cond.4 (F3 MSE reduction)    | $200-800         | 8-24 GPU-hours       | reconstruction loss training (TLM-native task)
   cond.5 (5ch deep validation) | $100-400         | 8-16 GPU-hours       | per-ch ablation + codebook size sweep (small)
   cond.6 (voice/speak downstream)| $0-200          | 4-12 hours           | bridge LoRA (downstream consumer, light)
   ---------------------------- | ----------------- | -------------------- | -----------------------------
   total band                   | $950-4400        | 44-124 hours         | training-dominated (cond.3 + cond.4)
```

비교:
- Phase 1+2 (spec freeze) = $0 mac-local, 60min cap
- Phase 3 (this doc) = $950-4400, 2-5 days
- Phase 4 (full IMPL + production deploy) = $3000-10000 추정, 1-2 weeks

mac-local inference 측 $0 invariant 유지. training-only RunPod (P9 SFT pipeline reuse 시 marginal credit consumption + 4-arm random-control 측 36-cell sweep 측 cost band upper).

---

## §4 decision matrix

```
   decision point          | option A                          | option B                          | verdict / rationale
   ----------------------- | --------------------------------- | --------------------------------- | -----------------------------------------------
   training corpus         | CLM self-chat tension pair        | tension_link UDP capture replay   | A primary / B aux — CLM self-chat 측 P9 SFT pipeline 측 직접 reuse 가능, UDP capture 측 production deploy 측 future cycle
   corpus 측 3rd 후보       | mind.tension trajectory window   | -                                 | defer — anima-runtime 측 trace data accumulation 부족 (별도 cycle 측 size/quality audit)
   F3 reduction priority   | re-extraction (TLM-native loss)   | β tuning continuation (CLM-style) | A — CLM Phase 1.6 측 §2.2 verdict (β path 측 stuck), TLM 측 5ch native task 측 circular 회피
   per-ch ablation timing  | cond.3 + cond.5 parallel          | cond.3 land 후 cond.5 sequential  | B — cross-LM fidelity baseline 먼저 확보 후 per-ch ablation 측 isolated study
   downstream coupling timing| cond.3 + cond.6 parallel        | cond.3 land 후 cond.6 sequential  | B — TLM-native fidelity 먼저 확보 후 downstream consumer 측 isolation
   random-control arm count| 2-arm (R1 + R2)                  | 4-arm (R1 + R2 + R3 + R4)         | B — §16.2 anchor MANDATORY 측 default 4-arm, IMPL phase 측 thinning 가능
   eval metric             | next-token CE only                | next-token CE + reconstruction MSE| both — CE (cross-LM parity) + MSE (TLM-native F3 floor)
   fallback policy         | hard-fail on cond.4 miss          | graceful — cond.3 met 시 partial land| B — cond.3 (cross-LM) 측 primary surface, cond.4 (F3) 측 secondary (배포 측 cond.3 만 enable 가능)
```

---

## §5 cross-LM dependencies

### §5.1 dependency graph

```
              ┌─────────────────────┐
              │   .roadmap          │
              │   .tensionlink      │  ← R=0.999 source-side wire (sister SSOT, in-place X)
              │   (sister, LIVE)    │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │       TLM           │
              │   Phase 1+2 (FROZEN)│  ← encoder + head spec freeze (predecessor)
              │   (current base)    │
              └──────────┬──────────┘
                         │
       ┌──────┬──────────┼──────────┬──────────┐
       │      │          │          │          │
   ┌───▼──┐┌──▼──┐  ┌───▼────┐  ┌──▼──┐  ┌────▼────┐
   │ CLM  ││ BLM │  │  VLM   │  │ SLM │  │ anima_  │
   │(text)││TRIBE│  │(voice) │  │(EEG)│  │ speak   │
   │      ││F-CT-3│  │ Mk.III │  │     │  │  cite   │
   └───┬──┘└──┬──┘  └───┬────┘  └──┬──┘  └────┬────┘
       │      │          │          │          │
   cond.3   cond.5   cond.6      cond.5     cond.6
   r ≥0.85  per-ch  voice down   EEG-tens  speak gate
   parity   ablation prosody     bridge    threshold
```

### §5.2 cross-LM dependency table

| dep  | from              | to                  | axis             | criticality | gate                              |
| ---- | ----------------- | ------------------- | ---------------- | ----------- | --------------------------------- |
| D1   | TLM cond.3        | CLM v4 530M         | next-token CE r  | CRITICAL    | ≥0.85 r vs sibling LM 측 floor    |
| D2   | TLM cond.5        | BLM F-CT-3 sister   | per-ch validity  | HIGH        | EEG ↔ TRIBE BOLD r ≥0.5 anchor    |
| D3   | TLM cond.6 (voice)| VLM Phase 3 cond.5  | prosody bridge   | HIGH        | VLM 384d cross-attn projection    |
| D4   | TLM cond.5 (EEG)  | SLM Phase 3 P3.C3   | EEG ↔ tension    | MEDIUM      | SLM Phase 1+2 land + B1-B4 PASS   |
| D5   | TLM cond.3        | P9 SFT pipeline     | LoRA train       | CRITICAL    | LHS-9 sweep template + LoRA path  |
| D6   | TLM cond.6 (speak)| anima_speak cite    | tension gate     | MEDIUM      | speak cite cleanup land + threshold|
| D7   | TLM cond.4        | CLM Phase 1.6 lesson| F3 re-extraction | HIGH        | tension target circular 회피 path |
| D8   | TLM all conds     | .roadmap.tensionlink| sister SSOT     | INVARIANT   | in-place 변경 0 byte (additive only)|

**top 3 critical dependencies**:
1. **D1 (CLM cross-LM r ≥0.85)** — primary success metric, sibling LM floor 와 일치, cond.3 측 entry 의 raison d'être
2. **D5 (P9 SFT pipeline reuse)** — training pipeline 측 LoRA r/α/lr LHS-9 grid + checkpoint cadence 측 sister sweep 측 직접 reuse, cost band upper bound 측 정합
3. **D7 (F3 re-extraction path, CLM Phase 1.6 lesson)** — CLM β tuning path 측 stuck (5.39 → 8.75) 측 lesson — TLM 측 5ch native reconstruction task 측 circular target 회피 측 핵심 design choice

### §5.3 dual SSOT race risk (CRITICAL invariant)

```
   sister .roadmap.tensionlink (transfer protocol SSOT, R=0.999 LIVE)
       ↕ (additive only, in-place 변경 0 byte)
   .roadmap.tlm_tension_lm (LM head reframing SSOT, this Phase 3 spec target)
```

Phase 3 update 시 양쪽 location 측 dual update race 가능 (TLM Phase 1+2 측 0건 위반 invariant 유지). 권고: Phase 3 IMPL phase 측 .roadmap.tensionlink 측 sister_lm = tlm_tension_lm sister-back-reference 추가 측 별도 cycle (anima_3_lm cycle §8 #3 권장 사항 still open).

---

## §6 honest C3 caveats (raw#10)

1. **C1 — tension target circular issue 측 TLM-native task 측 회피 가설 측 미검증** — CLM Phase 1.6 측 β path 측 stuck (5.39 → 8.75) 측 lesson 적용. TLM 측 5ch input → 5ch reconstruction 측 native task 측 circular 회피 가능 측 design choice, 단 실측 0건. cond.4 entry 시 재현 가능성 (input ≠ target 분리, base CLM forward dependency 0건) 측 IMPL pre-flight 측 검증 필수. 가설 fail 시 F3 absolute ≤2.0 target 측 unreachable, cond.4 측 deferred-to-Phase-4 가능성.

2. **C2 — scale-up risk: spec freeze ≠ training validation ≠ production** — Phase 1+2 측 spec freeze 만 land (실측 BLEU/perplexity/cross-LM r 0건). Phase 3 측 첫 training validation, 단 sibling NLM/BLM/SLM/VLM 측 동일 floor 측 cross-LM r ≥0.85 측 일관 reach 측 미증명. P9 SFT 측 530M CLM 측 LoRA r=64 측 단일 sweep 측 baseline, TLM 측 5ch encoder 측 신규 component 측 inductive bias 측 sibling LM 측 다름. 5ch encoder 측 information bottleneck 측 cross-LM r 측 ceiling 미정의.

3. **C3 — downstream coupling (anima_voice + anima_speak) 측 sequential dependency cascade risk** — cond.6 측 VLM Phase 3 cond.5 (SLM prosody) land 후 entry — VLM cycle 측 SLM Phase 1+2 land 후 entry — SLM cycle 측 .roadmap.eeg B1-B4 PASS 후 entry. 3-level transitive dependency cascade — base layer (.roadmap.eeg) 측 fail 시 TLM cond.6 측 indefinite block. mitigation: cond.3 + cond.4 + cond.5 측 downstream-independent path 측 Phase 3a 측 우선 land, cond.6 측 Phase 3b separate sub-cycle.

4. **C4 — dual SSOT race risk 지속 (Phase 1+2 invariant carried forward)** — sister .roadmap.tensionlink (transfer protocol) + .roadmap.tlm_tension_lm (LM head) 측 두 SSOT 동시 active. Phase 3 update 시 sister-back-reference 추가 권장 측 별도 cycle 측 still open. Phase 3 측 cond.3-6 update 시 in-place 변경 X 정책 측 IMPL agent 측 explicit checklist 권장 (additive only invariant).

5. **C5 — corpus 결정 (blk.2) 측 3 candidates 측 size/quality/availability 측 평가 0건** — (a) CLM self-chat tension pair / (b) tension_link UDP capture replay / (c) anima-runtime mind.tension trajectory window 측 token-count / 5ch coverage / sync drift 측 audit 0건. cond.3 entry prerequisite 측 corpus audit cycle 측 별도 land 필수. P9 SFT cond.2 sweep 결과 land 후 결정 권장 (Phase 1+2 §9 #4 carried forward).

6. **C6 — cross-substrate ≥0.85 r 측 indirect proxy 측 risk (sibling LM 공통 caveat)** — TLM (5ch token AR) vs CLM (text token AR) 측 ≥0.85 r 측 direct same-domain comparison 아님 (5ch tension vs text token 측 different vocab, different semantic). normalized perplexity 측 sibling LM 측 historical baseline 와 비교, true cross-substrate fidelity 측 5ch-text paired held-out 측 measure 필요 (sibling VLM/SLM/BLM 공통 caveat carried forward). cond.3 측 measurement protocol 측 IMPL phase 측 paired-corpus 정의 측 별도 design.

7. **C7 — §16.2 random-control MANDATORY 측 4-arm 측 cost band upper 측 risk** — Phase 1+2 §4 C6 측 carried forward — random-control (R1 random tension_link / R2 shuffled 5ch / R3 random codebook / R4 constant 5ch) 4-arm × LHS-9 grid = 36-cell sweep 측 cost band upper $4400 측 driver. IMPL phase 측 thinning (4-arm 측 R1 + R3 측 2-arm 만) 측 가능, 단 §16.2 anchor MANDATORY 측 weakening — explicit decision 측 IMPL agent 측 별도 cycle 결정.

8. **C8 — TLM ≠ phenomenal consciousness (sibling LM 공통 floor)** — sister .roadmap.tensionlink (R=0.999 transfer) 측 information channel framing (§44.2 anchor) 유지. TLM 측 LM-style reframing of 5-channel meta-fingerprint, phenomenal consciousness 보장 X (raw#10 honest invariant carried forward from Phase 1+2). Phase 3 cond.3 ≥0.85 r 측 cross-LM fidelity, NOT consciousness floor.

---

## §7 산출물

```
   path                                                  | type      | status
   ----------------------------------------------------- | --------- | --------
   docs/tlm_phase3_spec_2026_05_03.md                    | spec      | NEW (this file)
   .roadmap.tlm_tension_lm                               | roadmap   | unchanged (Phase 3 cond.3-6 측 next-cycle update)
   .roadmap.tensionlink                                  | sister SSOT| unchanged (in-place 변경 X invariant)
   anima-voice/                                          | substrate | unchanged (cond.6 downstream additive)
   anima-speak/                                          | substrate | unchanged (cond.6 downstream additive)
```

---

## §8 Phase 3 entry trigger

```
   prerequisite gate (4-gate AND)
   ──────────────────────────────
   G1: blk.2 corpus 결정 land
        - 3 candidates (CLM self-chat / UDP capture / mind.tension) 中 1 select
        - corpus audit cycle (size / quality / availability) 별도 land
        - 5ch coverage + sync drift verify
   G2: P9 SFT cond.2 LHS-9 sweep land (sister pipeline reference baseline)
        - LoRA r/α/lr grid 측 transferable 확인
        - checkpoint cadence (5K step HF org push) 측 reuse 가능
   G3: sister .roadmap.tensionlink sister-back-reference 추가 land (별도 cycle, additive only)
        - sister_lm = tlm_tension_lm cross-link entry
        - dual SSOT race 완화
   G4: §16.2 random-control 4-arm 측 cond.3 spec 측 사전 명시 (R1/R2/R3/R4 정의)
        - thinning decision 측 IMPL phase 측 explicit (default 4-arm, 가능 시 2-arm)
        - random arm gap floor (≥3.0 absolute MSE) 명시

   ALL 4 (G1 ∧ G2 ∧ G3 ∧ G4) → Phase 3a entry GO (cond.3 + cond.4 + cond.5)
   Phase 3b (cond.6 voice/speak downstream) → VLM Phase 3 cond.5 + SLM Phase 1+2 land 후 separate sub-cycle
   ANY 1 unmet → Phase 3 entry NO-GO, blocker resolution cycle 우선
```

---

## §9 7-element friendly summary

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [ADVANCE] TLM Phase 3 SPEC — cross-LM fidelity + F3 absolute reduction
   2. analogy             | 수신탑 첫 가동 + 신호 노이즈 제거 + 5채널 진단 + 송출 라인 연결
   3. core 결과            | 4 conds (cond.3 ≥0.85r / cond.4 F3 ≤2.0 / cond.5 5ch deep / cond.6 downstream)
                          | 8 cross-LM dependencies (CRITICAL: D1/D5/D7/D8)
   4. 마이그레이션 0          | sister .roadmap.tensionlink + 6 referenced .roadmap.* + narrative 모두 0 byte
                          | dual SSOT additive only 정책 invariant carried forward
   5. handoff path         | 본 spec doc = Phase 3 entry agent 의 reference SSOT
                          | + 4-gate entry trigger (G1 corpus / G2 P9 / G3 sister-back / G4 random-control)
   6. 다음 step             | (1) blk.2 corpus 결정 land (G1)
                          | (2) P9 SFT cond.2 LHS-9 sweep land (G2)
                          | (3) sister .roadmap.tensionlink sister-back-reference 별도 cycle (G3)
                          | (4) §16.2 random-control 4-arm spec freeze (G4)
                          | (5) Phase 3a entry (cond.3 + cond.4 + cond.5) — Phase 3b (cond.6) defer
   7. cost                 | $0 spec → training $950-4400, wall 44-124 GPU-hours, mac-local inference $0 invariant
```

---

## §10 doc meta

```
   doc          | docs/tlm_phase3_spec_2026_05_03.md
   type         | spec (Phase 3 scope freeze)
   substrate    | READ-ONLY: tlm_stage12_landed + .roadmap.tlm_tension_lm + CLM Phase 1.6 (F3 lesson)
   write        | this doc only
   raw#9        | NO .py (markdown only)
   raw#15       | NO personal paths
   execute      | none
   commit       | none
   marker       | none (spec doc only, marker 측 별도 land cycle)
```

end-of-doc.
