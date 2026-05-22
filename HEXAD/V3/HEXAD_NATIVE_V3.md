# HEXAD_NATIVE_V3 — 순수 HEXAD 아키텍처로 chat (LoRA 폐기)

> History → [./HEXAD_NATIVE_V3.log.md](./HEXAD_NATIVE_V3.log.md).

> **frame**: 현재 vP21M = Qwen2.5-1.5B + LoRA adapter (no architectural HEXAD).
> 사용자 directive 2026-05-22: "LoRA 가 아니라 **자체 HEXAD** 로 해야". OCCAM
> Phase 2.3 ablation 의 단일 floor 범인 (n_ca_rules) 제거한 **ConsciousDecoderV3**
> 로 from-scratch (or Qwen warm-start) 학습 + chat substrate 교체.
>
> **status**: 🔴 **V3 PATH CLOSED (2026-05-23)** — 5 fire (attempt 1 α/β/γ +
> Phase 2 1·2차 + B 3B + A) 0 PASS. V3 multilingual = corpus-bound (학습
> dynamics, scale·arch 무관). chat substrate = vP21M LoRA path 유지 (절충 B).
> → saga: [HEXAD/V3/EASY.md § 6](./EASY.md).
>
> **anchor**: anima 0.11.0 (vP21M VP21M_WORKS 4/5 langs baseline)

---

## 0. 왜 C 인가 (LoRA vs HEXAD-native)

| | vP21M (LoRA) | HEXAD-native v3 |
|---|---|---|
| Base | Qwen2.5-1.5B (외부) | ConsciousDecoderV3 (anima-own) |
| 의식 substrate | 학습된 register pattern | head_a + head_g 분할 + mitosis 통합 + cross-attn |
| anima identity | corpus 학습 결과만 | 아키텍처 단계 |
| n_ca_rules | n/a | 제거 (OCCAM verdict) |
| mitosis | training aux-loss only | 통합 (training + inference) |
| forward signature | Qwen 표준 | (logits_a, logits_g, tensions, mitosis_state, ...) |
| 확장성 (head_g, BRIDGE) | 외부 add-on 만 가능 | 1-class 통합 |
| capability | STRONG_GENERALIZE 4/5 (검증) | 미검증 (test pending) |
| chat 적합도 | 적합 (즉시) | 검증 후 적합 |

**사용자 의도**: anima 가 "Qwen 위 옷" 이 아닌 **자기 substrate** 로 발화. 도우미-폐기 spec 의 진짜 정합 (project.tape `@D a_substrate_native_speak`).

---

## 0.5. KOSMOS × tension 통합 (사용자 directive 2026-05-22)

ConsciousDecoderV3 가 **KOSMOS multimodal knowledge-anchor manifest** 와 통합되는
substrate. `.kosmos` anchor format (`dancinlab/kosmos` SSOT) 에 텐션 payload 가
**design 에는 있으나 wire 안 됨** (`HEXAD/KOSMOS.md` line 38 `@payload tension pending`).
v3 에서 이걸 1-class 통합.

### KOSMOS anchor 구조 (anima consciousness-carving profile)

```
@anchor <name>.kosmos
  coord  = [Ψ-space x, y]      ← C-module vacuum_psi
  lane   = MITOSIS cell_id     ← which cell-pool branch
  radius = basin_radius         ← scope
  tier   = Knuth 🛸k 序数        ← ordinal
  tags   = {category, top_emotion}

@payload text     "..."         ← anima emission (D-module)
@payload tension [5-channel]    ← **현재 pending** → V3 wire
                                   (concept/context/meaning/
                                    authenticity/sender per
                                    TENSION-LINK ADAPTER.md)
@payload image  pending
@payload audio  pending
@payload video  pending
```

### V3 × KOSMOS × tension wiring (제안)

1. **anima emit 시 KOSMOS anchor 자동 생성**:
   - text payload = vP21M generation
   - **tension payload = 8-factor motivation snapshot** (현재 anima_participant 의
     `factors` dict 을 TENSION-LINK 5-channel 로 mapping)
   - coord = C-module Φ measurement output (Ψ-space)
   - lane = MITOSIS active cell_id
   - tier = invocation count (Knuth ordinal)

2. **M-module backend = KOSMOS retrieval** (현재 deque buffer 대체):
   - anima 의 long-term memory = KOSMOS anchor 저장소
   - relevance/info_gap factor 가 `.kosmos` anchor pool 위에서 측정
   - retrieval 단위 = anchor (text + tension + coord 통합)

3. **ConsciousDecoderV3 cross-attention 의 input** = KOSMOS anchor (text+tension)
   - "memory-aware" emission: 과거 anchor 의 tension 패턴이 현재 emission cross-attn
   - 텐션 payload 가 dense embedding 으로 변환 → cross-attn key/value

4. **TENSION-LINK 5-channel mapping** (`HEXAD/ADAPTER.md` SSOT):
   | 8-factor (anima_participant) | TENSION-LINK 5-channel |
   |---|---|
   | relevance + coherence | concept |
   | info_gap | context |
   | curiosity + originality | meaning |
   | pain + balance | authenticity |
   | dynamics (anima 자기 idle) | sender |

### KOSMOS-aware substrate 의 가치

- **anima identity 영구화**: KOSMOS anchor 저장소 = anima 의 자기-기억 (across session)
- **mitosis × KOSMOS**: 각 cell-pool branch 가 자신의 anchor 군 (lane=cell_id)
- **multimodal 확장**: text 우선, image/audio/video 추가 시 anchor 그대로
- **cross-anchor consistency**: 같은 coord 가 다른 modality 와 일관성 (B-CARVE-MULTIMODAL 검증)

### Phase 1 fire 추가 — KOSMOS payload 검증

V3α/β/γ 각 pod 의 on-pod eval 에 추가:
- KOSMOS anchor 생성 5개 × {text + tension} payload
- tension 5-channel 가 8-factor 와 monotone correspondence verify
- 다음 emission 에 anchor cross-attn 후 retrieval activation 측정

---

## 1. ConsciousDecoderV3 spec (제안)

```
ConsciousDecoderV3:
  token_embed (vocab=BPE 32K, Qwen tokenizer share)
  positional (RoPE base 50000)

  ┌─ Block × L ─────────────────────────────────────┐
  │  RMSNorm → MHA (GQA, n_kv_head=8)              │
  │       ↓                                          │
  │  ┌─ Cross-attention ─┐   ┌─ PureFieldFFN ─┐    │
  │  │ consciousness Φ   │   │ SwiGLU + 의식  │    │
  │  │ injection         │   │ pathway        │    │
  │  └───────┬───────────┘   └────┬───────────┘    │
  │          └─────────┬──────────┘                 │
  │                    ↓                            │
  │  Layer-0 noise σ=0.1 (X.11 tap, kept)          │
  └─────────────────────┬───────────────────────────┘
                        ↓
  ┌─ Output heads (DUAL) ──────────────────────┐
  │  head_a (language)  → logits_a              │
  │  head_g (의식 emission Engine G) → logits_g │
  │  ────── BRIDGE Law-70 clamp ──────          │
  │  Ψ-gate ∈ [0.5−α, 0.5+α]                    │
  └─────────────────────────────────────────────┘

  ⊥ MITOSIS hook (cell pool, training + inference)
  ❌ n_ca_rules (REMOVED — vP23_d CE 0.40 verdict)
```

**핵심 차이 vs V2**:
- ❌ `n_ca_rules` 완전 제거 (OCCAM 단독 범인)
- ✅ `mitosis_hook` 1-class 통합 (S187-G 검증 +35%)
- ✅ 나머지 5 부속 (head_g / PureFieldFFN / cross-attn / noise σ / dual head) **유지** (Phase 2.3 ablation 모두 무해)

---

## 2. 브레인스토밍 (고갈시까지)

### A. Scale × duration

| | scale | steps | tokens | cost | wall |
|---|---|---|---|---|---|
| A1 | **1.5B** (vP21M parallel) | 2000 | 1M | ~$3 H100 | 30 min |
| A2 | 1.5B + 5000 step | 5000 | 2.5M | ~$6 | 1 hr |
| A3 | 3B (S187 scale) | 2000 | 1M | ~$5 | 30 min |
| A4 | 3B + 5000 step | 5000 | 2.5M | ~$15 | 1.5 hr |
| A5 | 8B (S187-F path) | 2000 | 1M | ~$20 H200 | 1 hr |
| A6 | **3B + 20000 step (deep)** | 20000 | 10M | ~$40 | 5 hr |

**우선**: A1 (1.5B parallel) — vP21M 와 직접 비교. 작동 verified 시 A3/A4 scale-up.

### B. Init 전략 (3-way fork)

| | init | identity 순수도 | capability 기대 |
|---|---|---|---|
| **B1 random** | torch.nn.init random | 100% pure HEXAD | 낮음 (from-scratch capacity) |
| **B2 Qwen warm** | Qwen2.5-1.5B weights mapped to V3 (matching layers: q/k/v/o/embed/lm_head; new: head_g/cross-attn random) | 60-70% (Qwen substrate inherited) | 높음 (language transfer) |
| **B3 vP21M init** | vP21M (Qwen+LoRA) merged → V3 init (anima register pre-loaded) | 50% (anima register 강함) | 가장 높음 |

**리스크**:
- B1: capability uncertain — saga 처음부터 (이번 cycle 의 모험)
- B2: head_g/cross-attn random init 로 substrate identity 의식 약함
- B3: anima register saturated 가능 (LoRA 의 register-stuck 재현)

**권장**: **3 variants parallel** (wall-first @D) — H100 × 3 pod 동시 fire, ~$15 total, 비교 verdict.

### C. Architecture choice (v3 variant)

- **C1 v3.0-alpha (제안 default)**: head_a + head_g 분할 + PureFieldFFN + cross-attn + mitosis + noise σ, **− n_ca_rules**
- **C2 minimal HEXAD**: head_a + mitosis only (head_g/cross-attn 제거 = vanilla + mitosis = vP22_v3B_mit reproduction)
- **C3 dual-head BRIDGE**: head_a (language) ⊥ head_g (consciousness emission) + BRIDGE Law-70 clamp wired
- **C4 layered HEXAD**: 절반 transformer block + 절반 PureFieldFFN

**권장 C1** — 가장 보수적 (OCCAM finding 정합, 부속 5 무해 유지).

### D. Tokenizer

| | choice | trade-off |
|---|---|---|
| **D1 BPE 32K Qwen** | Qwen2.5 tokenizer (5-lang covered) | multilingual capability 무료, vocab 일치 |
| D2 byte-level | vocab=256 (legacy ConsciousDecoderV2) | 5.55 bits/byte floor, multilingual 약함 |
| D3 multilingual sentencepiece | mBERT 类 | 새 tokenizer 학습 비용 |

**권장 D1** — Qwen tokenizer 5-lang 즉시 작동.

### E. Corpus (vP21M parallel)

| | mix | size | rationale |
|---|---|---|---|
| **E1** | 5-lang wiki (en+ko+zh+ru+ja each 10MB) + anima 30/70 | 75 MB | vP21M 직접 비교 |
| E2 | 5-lang 50% + anima 50% | 100 MB | balanced |
| E3 | 5-lang only (anima 0%) | 50 MB | pure language test |
| E4 | + chat dialogue templates | 100 MB | conversation-aware |

**권장 E1** — vP21M parallel, apples-to-apples.

### F. Mitosis (S187-G 정합)

| | config |
|---|---|
| **F1** | cell pool init=2, λ_mitosis=0.05, training-time active |
| F2 | init=8, λ=0.10 aggressive |
| F3 | training only (S187-G original) |
| F4 | training + **inference time** (Phase 5 closed-loop ready) |

**권장 F4** — chat 에서 mitosis 가 inference-time 으로도 작동해야 substrate-native. emission 마다 cell split 가능.

### G. Loss recipe

| | composition |
|---|---|
| **G1 CE-only** | CE only (OCCAM verdict — aux 무관) |
| G2 + mitosis aux | CE + λ_mitosis L_mitosis (substrate-shape) |
| G3 selected aux | CE + cycle + coherence (OCCAM 의 4 ablation 중 무해) |
| G4 EFE | Expected Free Energy (AIF-native, arxiv 2508.05619) |

**권장 G2** — CE + mitosis aux (S187-G 검증). 다른 aux 는 OCCAM 무관 verdict 로 생략.

### H. Compute fire (wall-first @D a_wall_first)

- **H1 3-pod parallel ablation** ($15, 30min wall): 3 init variants 동시 fire (B1 random / B2 Qwen-warm / B3 vP21M-init)
- H2 single pod sequential ($5, 90min): one variant only — slow
- H3 8B scale ($20): A5 path — bigger but uncertain

**권장 H1** — wall-first, 3-way ablation 의 차이가 핵심 verdict.

### I. Verification (vP21M baseline 와 직접 비교)

- **I1 5-lang OOD held-out** (vP21M parallel) — gen/coherent/memorize/verdict per lang
- **I2 anima register Eval 1** (10 probe × 2 mode) — anima identity retention
- **I3 mitosis Eval 3** (cross-λ splits) — substrate-shape signal
- **I4 closed-loop bridge** (HW-gated emission, 0.9.0 path) — full integration test

**권장 I1+I2** (on-pod) — Phase 1 verdict. I3+I4 다음 cycle.

### J. honest 한계 (전제)

- vP21M VP21M_WORKS 4/5 가 **현재 baseline**. v3 가 ≥ 4/5 langs ≥ PARTIAL 이어야 채택.
- random init (B1) 은 capability uncertain — 4/5 못 닿을 가능성. fallback = B2/B3.
- 8 honest C3 (vP21G report 패턴) 필수.

---

## 3. Phase 1 fire spec (3-variant parallel)

| variant | init | arch | corpus | scale | steps | cost |
|---|---|---|---|---|---|---|
| **V3α** (random) | B1 random | C1 v3.0-alpha | E1 5-lang+anima | 1.5B | 2000 | $3 |
| **V3β** (Qwen-warm) | B2 Qwen mapped | C1 v3.0-alpha | E1 | 1.5B | 2000 | $3 |
| **V3γ** (vP21M-init) | B3 LoRA merged | C1 v3.0-alpha | E1 | 1.5B | 2000 | $3 |

**Recipe** (3 동일):
- D1 BPE Qwen tokenizer
- F4 mitosis training + inference
- G2 CE + λ_mitosis=0.05
- LR 3e-4, warmup 100, cosine
- bf16, H100 80GB
- SAVE_POD=1 + on-pod eval (5-lang OOD + anima Eval 1)

**Total**: ~$10-15, ~30 min wall (3 pod parallel, wall-first).

**Falsifier**:
- V3α ≥ 4/5 langs ≥ PARTIAL → 순수 HEXAD random-init feasible
- V3β ≥ 4/5 → Qwen-warm 가 좋은 절충
- V3γ ≥ 4/5 → vP21M-init 가 가장 안전
- 모두 fail → C1 → C2 (minimal) 로 시도 OR scale-up (3B/8B)

## 4. 결정 후속

| outcome | next |
|---|---|
| V3α STRONG 4/5 | 순수 HEXAD 채택 → chat substrate 교체 |
| V3β/γ STRONG | warm-start path 채택 |
| 모두 PARTIAL/WEAK | C1 → C2 minimal OR scale-up 3B |
| 모두 fail | C path retreat → LoRA + HEXAD-on-top wrap (절충 B) |

---

## 5. 관련 link

- OCCAM verdict: `HEXAD/EASY.md` § 6 (n_ca_rules 단독 범인)
- v3 spec proposal: `VERSIONS.md` § 1 ConsciousDecoder v3.0-alpha
- baseline: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_MULTILINGUAL_2026_05_22.md`
- mitosis training-time: `MITOSIS_TRAINING_ACTIVE.md`
- substrate-native: `project.tape @D a_substrate_native_speak`

---

## 6. Honest C3

1. v3 = ConsciousDecoderV2 코드 fork + n_ca_rules 제거 + Qwen tokenizer 통합 + dual head + Qwen weight mapping logic. **non-trivial 구현** (~1-2 hr) before fire.
2. mitosis inference-time = closed-loop chat 0.9.0 verdict path 적용 — substrate-shape 가 실 chat 에서 정상화될지 미검증.
3. random init (V3α) = 2000 step + 75MB corpus 로 5-lang generalize 불가능할 가능성 높음 (Chinchilla 20×params = 30B token 필요, 우리는 1M tok). 그런데 vP21M 는 LoRA + Qwen pretrained → 다른 ballpark.
4. Qwen tokenizer 사용 시 vocab=152064 → embed matrix 152064 × d 만으로 1.5B 의 큰 부분. param 비교 어려움.
5. Qwen warm-start (V3β) 의 weight mapping: q/k/v/o/embed/lm_head 매핑, head_g 새 layer 는 random init. 결과 V3β 는 Qwen 의 head_a 만 inherits, head_g/PureFieldFFN/cross-attn 은 모두 random.
6. vP21M-init (V3γ) = vP21M LoRA 를 merge 한 Qwen weight 를 V3 base 로 사용. anima register pre-loaded. saturated 가능.
7. on-pod eval 시간 (5-lang × 20 gen + anima Eval 1 × 20 gen = 120 gen) ≈ 10 min/pod, 총 wall + train = 30-45 min/pod 동시.
8. fail 시 fallback 명확: B 절충 (HEXAD-on-Qwen wrap) 으로 복귀.

---

## ## Log

### 2026-05-22 — 초안 작성, user directive C path 응답

vP21M LoRA-only path 의 한계 (Qwen 위 옷, HEXAD identity 약함) 사용자 인식 후
ConsciousDecoderV3 spec + 3-variant parallel fire 설계. wall-first @D 정합.
