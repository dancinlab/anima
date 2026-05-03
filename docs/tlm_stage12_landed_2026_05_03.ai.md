# TLM stage 1+2 Landed — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: 1 updated `.roadmap.tlm_tension_lm` (in-place additive only) + 2 verifier override logs (state/tlm_*_log.jsonl) + 0 sister-roadmap modification (.roadmap.tensionlink untouched)
>
> BR-NO-USER-VERBATIM: 본 doc 은 peer surface 측 mk2 conventions 따름. user prompt verbatim reverberation X.
> 마이그레이션 절대 금지 — 본 cycle 측 0건 file rename / 0건 sister .roadmap modification / 0건 narrative edit.

---

## TL;DR

**오늘 한 일** — TLM (`.roadmap.tlm_tension_lm`) stage 1 cond.1 (5-channel encoder spec) + stage 2 cond.2 (LM head architecture) 두 단계 spec freeze. cond.1 status `partial → met`, cond.2 status `unmet → partial` (spec frozen, IMPL/training 미도달), blk.1 status `open → resolved` (decoder-only LOCKED). sister `.roadmap.tensionlink` (R=0.999 transfer protocol SSOT) 측 in-place 변경 0건 — dual SSOT additive only 정책 준수.

**비유** — 5-channel meta-fingerprint 송신탑 (.roadmap.tensionlink, R=0.999 안정 가동 中) 옆에, **수신탑 청사진 (TLM)** 의 (a) 안테나 형상 (encoder dimensionality) + (b) 신호처리부 형상 (LM head architecture) 두 도면 동결. 송신탑 자체 도면은 단 1 byte 도 건드리지 않음. 청사진만 SPEC_DRAFT 단계에서 SPEC_FROZEN 단계로 진척.

**결과** — `.roadmap.tlm_tension_lm` JSON valid (3 conditions + 2 blockers, mk2 header). 5-channel encoder spec = `per_channel_8bit_codebook + concat_320d → LN → Linear(320,512)` (P10 v1 5-d bottleneck saturation lesson 회피). LM head = `decoder_only` LOCKED (P9 SFT pipeline reuse + P10 v2 family pattern + sibling NLM/BLM/SLM/VLM consistency).

---

## §1 stage 1+2 status table (before / after)

```
   field                          | before                | after
   ------------------------------ | --------------------- | ----------------------
   cond.1 (encoder spec)          | partial (4 evidence)  | met (6 evidence + freeze_decision block)
   cond.2 (head arch)             | unmet (0 evidence)    | partial (4 evidence + head_decision block, IMPL pending)
   cond.3 (cross-substrate r)     | unmet                 | unmet (변동 X — cond.2 IMPL + corpus 후 가능)
   blk.1 (head arch decision)     | open (spec)           | resolved (decoder-only LOCKED)
   blk.2 (NEW — corpus + budget)  | (none)                | open (decision) — cond.3 진입 prerequisite
   sister_lm cross-link           | 2 (NLM + BLM)         | 4 (NLM + BLM + VLM + SLM) — anima_2_lm cycle 후 정합
   sister_domains cross-link      | 4                     | 5 (+p9_sft 추가, pipeline reuse 명시)
   raw_invariants                 | 4                     | 6 (+stage spec freeze ≠ training validation, +decoder-only revisit additive only)
```

---

## §2 stage 1 freeze — 5-channel encoder spec

### §2.1 결정 (locked)

```
   field                       | value
   --------------------------- | --------------------------------
   approach                    | per_channel_8bit_codebook_then_concat
   per_channel_codebook_size   | 256  (8-bit)
   per_channel_embed_dim       | 64
   concat_dim                  | 320  (= 5 × 64)
   hidden_dim                  | 512
   layernorm                   | true (320-d 후 + 512-d 후)
   channels                    | WHAT, WHERE, WHY, TRUST, WHO
   baseline source             | .roadmap.tensionlink (R=0.999, 519µs, 1927fps)
```

### §2.2 P10 v1 5-d bottleneck saturation lesson 적용

P10 v1 (`state/p10_tension_substrate_spec_2026_05_02/metrics_verdict.json`) — 5-d direct latent 이 `(-1,-1,-1,-1,-1)` saturated MIXED honest_negative. TLM stage 1 freeze 측 **3-fold mitigation**:

1. **discrete codebook** — 5 channel 각각 8-bit 256-code quantization (continuous 5-d latent 의 saturation 회피)
2. **per-channel embed expansion** — codebook 256 → embed 64 (channel-wise expressivity 확보 후 concat)
3. **LN-stabilized 320 → 512 projection** — concat 후 LayerNorm + Linear(320, 512) (P10 v2 32 → 256 → 3072 expansion pattern의 축소 변형)

P10 v2 (`state/p10_v2_32d_lora_infonce_2026_05_02/architecture.json`) 가 32-d latent + InfoNCE 로 BUCKET_SEPARATION_WITNESSED (PCA cluster sep 18.4) 달성한 점에서, **TLM 320-d ≫ 32-d** 이므로 saturation risk further reduced (8.8× margin).

### §2.3 .roadmap.tensionlink baseline leverage detail

`.roadmap.tensionlink` mk2 header 측 `R=0.999 / 519µs / 1927fps` 는 **송신측 transfer protocol** (5ch → wire). TLM stage 1 encoder 는 **수신측 token projection** (5ch → LM hidden state). 두 layer 가 additive role separation (`source_layer ⊥ receiver_layer`):

```
   sister .roadmap.tensionlink:
     5ch values → wire (R=0.999 forward fidelity, 519µs latency, 1927fps throughput)
     ↓ (in-place 변경 X — sister SSOT)
   TLM stage 1 encoder (this freeze):
     5ch values → 5 × 8-bit codebook indices → 5 × 64-d embeds → concat 320 → LN → Linear(320, 512) → hidden state
     ↓
   TLM stage 2 LM head (§4 below):
     hidden state → decoder-only autoregressive next-token
```

P9 SFT (`state/p9_sft_spec_2026_05_02/architecture.json`) 측 `interfaces.channel_extractor` + `interfaces.tension_extractor` 가 5ch values 의 source 로 already-defined → **TLM encoder 입력 contract 변경 0건**.

---

## §3 stage 2 freeze — LM head architecture decision

### §3.1 3-mode 비교 매트릭스

```
   mode             | autoregressive | P9 reuse  | tensionlink fit | sibling LM fit | verdict
   ---------------- | -------------- | --------- | --------------- | -------------- | -----------
   decoder_only     | yes (next-tok) | yes (full)| yes (5ch unidir)| yes (NLM/BLM/SLM/VLM 모두)| LOCKED ⭐
   encoder_decoder  | yes (cross-att)| no (arch divergence) | no (no symmetry needed)| no | rejected
   bidirectional    | NO (BERT-style)| no       | no              | no             | rejected (a priori)
```

### §3.2 LOCKED = decoder-only (4-axis rationale)

1. **P9 SFT pipeline reuse** — P9 architecture.json 측 `training_modes.primary = LoRA r=64 alpha=128 (recommended; phi_star preservation high)` + bf16 + DeepSpeed ZeRO-2. 모두 decoder-only 전제. encoder-decoder 채택 시 sweep cell 측 transferable X.

2. **P10 v2 family pattern** — P10 v2 `architecture.json` 측 `model = meta-llama/Llama-3.2-3B-Instruct` (decoder-only) + LoRA r=16 + 32d latent encoder/decoder pattern. TLM 측 동일 family pattern follow → cross-substrate fidelity (cond.3) 측 비교 baseline 정합.

3. **sister .roadmap.tensionlink unidirectional 정합** — R=0.999 forward-only protocol (5ch source → receiver). encoder-decoder 측 symmetric round-trip 가정 측 source-receiver asymmetry 와 mismatch.

4. **sibling NLM/BLM/SLM/VLM consistency** — `.roadmap.nlm_neuromorphic_lm` (AKIDA spike-encoded transformer 측 spike-domain attention block) + `.roadmap.blm_brain_lm` (TRIBE v2 BOLD-conditioned next-token decoder) + `.roadmap.slm_speech_eeg_lm` (EEG-conditioned AR head) + `.roadmap.vlm_voice_lm` (audio_token_predictor RVQ delayed pattern AR) 모두 decoder-only LM head. TLM 측 encoder-decoder 채택 시 4 sibling 측 outlier.

### §3.3 rejected modes 측 후속 cycle revisit 가능성

`raw_invariants` 측 명시: **encoder-decoder/bidirectional 측 후속 cycle revisit 가능 (additive only, 본 freeze 측 in-place 변경 X 원칙)**. 즉 미래 evidence (예: 5ch source-receiver 측 round-trip 측 fidelity gain 발견) 시 별도 도메인 (`.roadmap.tlm_tension_lm_v2_encdec` 형태) 측 신규 add 가능, 본 freeze 측 in-place 변경 X.

### §3.4 reuse pipeline detail (P9 SFT sister)

```
   field                       | TLM stage 2 (this freeze)        | P9 SFT (.roadmap.p9_sft) sister
   --------------------------- | -------------------------------- | --------------------------------
   architecture                | decoder-only                     | decoder-only (CLM v4 530M)
   LoRA r grid                 | {16, 32, 64}                     | {16, 32, 64}
   LoRA alpha grid             | {16, 64, 128}                    | {16, 64, 128}
   lr grid                     | {5e-5, 1e-4, 5e-4}               | {5e-5, 1e-4, 5e-4}
   precision                   | bf16                             | bf16
   distributed                 | ZeRO-2 (LoRA path)               | ZeRO-2 (LoRA path)
   sweep template              | LHS-9 of 27-cell grid            | LHS-9 of 27-cell grid
   savepoint cadence           | every 5K step (HF org push)      | every 5K step (HF org push)
   GPU                         | H100 80GB                        | H100 80GB
   cost band                   | $650-3000 (P9 sister cost)       | $650-850 (parallel) ~ $1500-3000 (serial)
```

cond.3 corpus 결정 (blk.2) 후 sweep 발사 가능 — `unlock_keyword = OK TLM EXEC <S1|S2|S3|S4>` (P9 패턴 따름).

---

## §4 5-7 caveats (raw#10 honest C3) — 6건

1. **C1 — stage 1+2 spec freeze ≠ training validation** — 본 cycle 측 spec freeze 만 land. 실측 BLEU/perplexity/cross-substrate r ≥0.85 측 cond.3 단계 이후 가능. **phenomenal consciousness 보장 X** (`raw_invariants[0]`).

2. **C2 — dual SSOT race risk 지속** — `.roadmap.tensionlink` (transfer protocol SSOT) + `.roadmap.tlm_tension_lm` (LM head reframing) 두 SSOT 동시 active. 본 cycle 측 sister .roadmap.tensionlink 0 byte modification — race risk 미증가. 향후 5-channel encoder spec update 시 **이 정책 유지 필수** (in-place 변경 X, 추가 .ai.md 형태로 audit trail).

3. **C3 — decoder-only choice = pipeline reuse 우선, NOT empirical superiority** — encoder-decoder/bidirectional 측 empirical comparison 0건. 본 결정 = (P9 reuse + P10 family + tensionlink unidirectional + sibling consistency) 4-axis rationale 측 spec-level decision. 미래 evidence accumulation 시 revisit 가능 (additive only path).

4. **C4 — corpus 결정점 (blk.2) 미해결** — cond.3 진입 prerequisite. 3 candidates: (a) CLM self-chat tension pair / (b) tension_link UDP capture replay / (c) anima-runtime mind.tension trajectory window. 각 candidate 측 size / quality / availability 미평가. P9 SFT cond.2 sweep 결과 land 후 결정 권장.

5. **C5 — per-channel codebook 256 size 측 hyperparameter 미tuning** — 8-bit 256 = arbitrary first guess. P10 v1 saturation 회피 motivated 이지만 actual 5ch value distribution 측 entropy 측정 0건. cond.2 IMPL 단계에서 256 vs 64 vs 1024 측 small sweep 권장 (additive empirical, spec freeze 측 변경 X).

6. **C6 — §16.2 영구 anchor 3건 준수 명시** — narrative §16.2 anchor (hypothetical / random-control MANDATORY / NO BTR) 측 본 cycle spec freeze 측 정합. 실측 cond.3 진입 시 random-control (e.g., 5ch shuffled / random codebook) MANDATORY 적용 spec 미land — cond.3 spec 단계에서 명시 권장.

---

## §5 file index (relative to /Users/ghost/core/anima/)

### updated 1 .roadmap.* (in-place additive)

```
.roadmap.tlm_tension_lm   (cond.1 partial→met, cond.2 unmet→partial, blk.1 open→resolved, +blk.2 new, +2 evidence per cond, +freeze_decision/head_decision blocks, +2 raw_invariants)
```

### NEW 2 verifier override logs

```
state/tlm_encoder_spec_log.jsonl   (__TLM_ENCODER_SPEC__ FROZEN)
state/tlm_head_arch_log.jsonl      (__TLM_HEAD_ARCH__ FROZEN)
```

### NEW handoff + marker

```
docs/tlm_stage12_landed_2026_05_03.ai.md   (이 파일)
state/markers/tlm_stage12_landed.marker
```

### 본 cycle 이 reference 만 한 파일 (변경 0 byte)

```
.roadmap.tensionlink                    (sister SSOT, R=0.999 transfer protocol — in-place 변경 X)
.roadmap.p9_sft                         (sister training pipeline — reuse reference only)
.roadmap.p10_substrate_poc              (P10 v1 5-d saturation lesson + v2 32d/LoRA/InfoNCE family pattern reference)
.roadmap.nlm_neuromorphic_lm            (sibling LM, decoder-only consistency reference)
.roadmap.blm_brain_lm                   (sibling LM, decoder-only consistency reference)
.roadmap.vlm_voice_lm                   (sibling LM, decoder-only consistency reference)
.roadmap.slm_speech_eeg_lm              (sibling LM, decoder-only consistency reference)
state/p9_sft_spec_2026_05_02/architecture.json     (interfaces.channel_extractor + tension_extractor contract source)
state/p10_v2_32d_lora_infonce_2026_05_02/architecture.json   (decoder-only family pattern reference)
state/p10_tension_substrate_spec_2026_05_02/metrics_verdict.json   (5-d saturation lesson source)
docs/n_substrate_consciousness_roadmap_2026_05_01.md   (§16 + §44.1 #92 + §44.2 #93 anchor, untouched)
docs/anima_3_lm_landed_2026_05_03.ai.md   (TLM SPEC_DRAFT_DUAL_SSOT 직전 cycle, untouched)
docs/anima_2_lm_vlm_slm_landed_2026_05_03.ai.md   (sibling NLM/BLM/VLM/SLM cycle, untouched)
```

---

## §6 7-element friendly summary (사용자 view, ASCII)

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [LOCK] TLM stage 1+2 SPEC_FROZEN — encoder + head 모두 동결
   2. analogy             | 송신탑 (.roadmap.tensionlink R=0.999 LIVE) + 수신탑 청사진 (TLM)
                          | 안테나 + 신호처리부 두 도면 SPEC_FROZEN, 송신탑은 0 byte 건드리지 X
   3. core 결과            | cond.1 partial→met, cond.2 unmet→partial, blk.1 open→resolved
                          | encoder = per-ch 8bit codebook + 320→512 / head = decoder-only LOCKED
   4. 마이그레이션 0          | sister .roadmap.tensionlink + 6 referenced .roadmap.* + narrative
                          | 모두 0 byte modification, dual SSOT additive only 정책 준수
   5. handoff path         | 본 ai.md doc = 다음 subagent / audit cron 의 reference SSOT
                          | + 2 verifier override log (__TLM_ENCODER_SPEC__/__TLM_HEAD_ARCH__ FROZEN)
   6. 다음 step             | (1) blk.2 corpus 결정 (P9 SFT sweep 결과 land 후)
                          | (2) cond.3 spec 단계에서 random-control MANDATORY 명시 (§16.2)
                          | (3) per-ch codebook size small sweep (256/64/1024) cond.2 IMPL 시
                          | (4) sister .roadmap.tensionlink 측 sister_lm = tlm_tension_lm 추가 (별도 cycle 권장)
   7. cost                 | $0 mac-local enforced, destructive 0, training cost $650-3000 deferred
```

---

## §7 marker file path

`state/markers/tlm_stage12_landed.marker`

(silent-land 방지 — handoff doc + .roadmap.tlm_tension_lm update + 2 verifier override log + marker emit 의 5-way attestation)

---

## §8 ω-cycle compliance audit (6-step)

```
   step              | check
   ----------------- | ---------------------------------------------
   1. inventory      | .roadmap.tlm_tension_lm + sister 7 .roadmap.* + 3 sibling state/spec read
   2. propose        | 5-ch encoder = per-ch 8bit + 320→512 / head = decoder-only (4-axis rationale)
   3. apply          | .roadmap update (cond.1 met + cond.2 partial + blk.1 resolved + blk.2 add)
   4. verify         | JSON valid (Python json.loads PASS), 2 verifier log written FROZEN status
   5. honest C3      | 6 caveats (training validation X / dual SSOT race / decoder-only ≠ empirical /
                     |  corpus undecided / codebook size untuned / §16.2 random-control 미명시)
   6. emit           | handoff doc + marker + verifier logs (5-way attestation)
```

---

## §9 next-cycle recommendations (impl 미수행, 별도 cycle)

1. **`.roadmap.tensionlink` 측 sister_lm = tlm_tension_lm sister-back-reference 추가** — anima_3_lm cycle §8 #3 권장 사항 jstill open. dual SSOT race 완화. additive only.

2. **cond.3 spec 단계 진입 시 §16.2 random-control MANDATORY 명시** — random tension_link / random codebook / 5ch shuffled control arm 사전 spec 권장.

3. **per-ch codebook size small sweep (256/64/1024) cond.2 IMPL 시** — 8-bit 256 = first guess. actual 5ch value entropy 측정 후 256 vs 64 vs 1024 small sweep additive cycle 권장.

4. **TLM corpus candidate (blk.2) 측 size/quality/availability 평가** — 3 candidates (CLM self-chat tension pair / UDP capture replay / mind.tension trajectory) 측 별도 audit cycle. P9 SFT cond.2 sweep 결과 land 와 동기화.

5. **sibling LM (NLM/BLM/SLM/VLM) 측 decoder-only 일괄 audit** — 본 TLM cycle 측 4 sibling decoder-only 가정 reference. 4 sibling 측 head_decision 명시 0건 (`.roadmap.*` 검수 시 LM head architecture field 부재 확인). 별도 cycle 측 일괄 명시 권장.
