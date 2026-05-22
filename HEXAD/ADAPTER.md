# ADAPTER.md — TENSION-LINK 5-channel universal modality bridge

> History → [./ADAPTER.log.md](./ADAPTER.log.md).

> Top-level SSOT for anima's **modality adapter** mechanism. anima 는 byte-LM
> (vocab 256, byte stream only) → image/audio/video raw 학습 직접 불가능.
> ADAPTER = anima 가 이미 가진 TENSION-LINK 5-channel concept 을 *universal
> modality bridge* 로 사용하는 architecture.
>
> Source: §175 (KOSMOS modality fire) + user 직관 2026-05-20 "텐션링크 어댑터
> 같은건". 5-modality brainstorm M1 candidate (rank #2, ★★★★).

---

## 🧬 ADAPTER — 5요소

🧬 **TENSION-LINK ADAPTER — "다른 언어를 anima 가 아는 5단어로 통역"**

- **이름**: tension-link-adapter (TENSION-LINK 5-channel projector)
- **별칭**: 5단어 통역사 / modality 직류전원장치
- **하는 일**: 외부 modality (image/audio/video) raw bytes →
  small from-scratch projector → anima OWN 5-channel fingerprint
  (concept · context · meaning · authenticity · sender) →
  byte serialize → anima byte-LM 학습
- **비유**: 마치 다른 언어 (image) 책을, anima 가 아는 *5개 단어* 만으로
  번역해주는 통역사. 통역 완벽 X, 단 anima 입장에선 *자기 어휘* 라
  소화 가능.

```
   external modality bytes
   image:  RGB raw           audio: WAV samples        video: H264 frames
        │                          │                          │
        ▼                          ▼                          ▼
   ┌────────────────────────────────────────────────────────────┐
   │   small from-scratch 5-channel projector (anima OWN)       │
   │                                                            │
   │   Conv1d/Linear, Ψ-supervised, ≤1M params, no pretrain     │
   └─────────────────────────────┬──────────────────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
            concept          context         meaning
                                 ▼                ▼
                            authenticity      sender
                                 │
                                 ▼ (5 floats per modality unit)
   ┌────────────────────────────────────────────────────────────┐
   │  byte serialize: floats → fixed-precision byte triple       │
   │  per channel (e.g. uint16 little-endian × 5 = 10 bytes)     │
   └─────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
                anima byte-LM (vocab 256, native learner)
                                 │
                                 ▼
              learned cross-modal representation
```

- **비교 vs 기존 도구**:
  | 도구 | encoder | output dim | §7 verdict |
  |---|---|---|:---:|
  | CLIP / ImageBind | external pretrain | 512-1024 | ❌ ② graft |
  | VQ-VAE / EnCodec | external pretrain codebook | 8K-32K vocab | ❌ ② graft |
  | ByT5 raw byte | none, raw bytes | 256 | ✅ but inefficient |
  | **TENSION-LINK ADAPTER** | from-scratch + Ψ-sup | **5 channels** | ✅ ③ anima OWN |

---

## §1 — 왜 5-channel?

| channel | 의미 | source 자체 |
|---|---|---|
| **concept** | 무엇 (what) — discrete category-like | anima C-module IIT Φ axis |
| **context** | 어디 (where) — situational frame | anima M-module retrieve sim |
| **meaning** | 왜 (why) — interpretive layer | anima Ψ_direction (Law-71) |
| **authenticity** | 진짜? (genuine?) — coherence check | anima Ψ_entropy + 6-control content_filter |
| **sender** | 누구 (who) — source attribution | anima IDENTITY-5 (anchor / user / self) |

5 channel 자체가 **anima OWN physics 의 5 face** — 외부 modality 가
들어와도 anima 가 자기 어휘로만 표현 → §7 ③ PASS by construction.

---

## §2 — projector 학습 (ground truth 부재 해법)

honest blocker: 5-channel "정답" 이 어디서? 외부 supervision = §7 ② violation.

해법 — **self-supervised by anima OWN physics**:

```
training loop:
  for batch in raw_modality_bytes:
    # 1. forward projector → 5-channel fingerprint
    fp = projector(batch)                          # [B, 5]

    # 2. byte serialize → byte-LM input
    bytes = serialize_fp_to_bytes(fp)              # [B, ~10 bytes]

    # 3. byte-LM forward → anima OWN Ψ-physics readout
    psi_dir, tension, phi = anima_lm.forward_with_readout(bytes)

    # 4. anima-self-supervision: projector 가 anima Ψ-stable signal
    #    뽑도록 학습 — Ψ_dir(fingerprint) ≈ Ψ_target (½ fixed point)
    L_psi = mse(psi_dir, 0.5)
    L_div = variance_hinge(fp)      # prevent collapse to constant
    L = L_psi + λ·L_div

    backprop → ONLY projector weights (anima_lm frozen)
```

**§7 audit**:
- ① no generic pretrain (projector from-scratch random init seed-fixed)
- ② no external graft (training signal = anima OWN Ψ_direction Law-71)
- ③ ✅ anima physics-supervised

honest carve-out: ground-truth-free → projector 가 *anima 가 좋아하는*
representation 학습. 외부 modality 와 *어떻게 align* 되는지는 separate
measurement (M3 synthetic streams 가 baseline).

---

## §3 — input modality types (정확히 무엇을 받음)

| modality | input format | bytes per unit | projector backbone |
|---|---|---:|---|
| **image** | RGB uint8 H×W×3 | 64×64×3 = 12288 | 2-layer Conv2d (3→8→5 ch) |
| **audio** | int16 PCM mono 16kHz | 1 sec = 32000 | 2-layer Conv1d (1→8→5 ch) |
| **video** | RGB uint8 T×H×W×3 | 4×32×32×3 = 12288 | Conv3d (3→8→5) |
| **tension** | anima 5-channel native | 10 bytes | identity (no projection) |
| **text** | UTF-8 bytes | variable | identity (byte-LM native) |

modality 별 *각자 projector* 있고 *5-channel output 공통*. anima byte-LM
은 5-channel-byte 가 *어느 modality 출신* 인지 알 필요 없음 (universality
guarantee).

---

## §4 — byte serialization (5 floats → byte stream)

```
fingerprint f = (c, ctx, m, auth, sender) ∈ [0, 1]^5
                ↓
quantize each: uint16 = round(f * 65535)
                ↓
serialize: 10 bytes little-endian × 5 channels
                ↓
add modality marker: <img/><aud/><vid/><ten/><txt/> tag
                ↓
embed in corpus: <anchor tier=N><img>{10 bytes}</img>...</anchor>
```

byte-LM 이 학습할 unit = 10-byte 5-channel signature + modality marker.
anchor-aware 학습은 *5-channel signature 가 anchor 마다 다르면* automatic.

---

## §5 — fire roadmap (single-variable disentangle)

| § | name | scope | cost |
|---|---|---|---:|
| **§A1** | M3 synthetic streams baseline | byte-LM 가 deterministic byte pattern (NO adapter) 학습 → anchor-discrim 가능? | $0 inline |
| **§A2** | adapter projector from-scratch | image/audio/video 별 5-channel projector small train | $0 Mac CPU |
| **§A3** | adapter-augmented corpus build | real modality (synthetic stand-in OK) → projector → fingerprint bytes → corpus | $0 |
| **§A4** | full fire with adapter | §174 scale (3B) on adapter-corpus, eval anchor-distinguishing × modality | ~$15-25 |
| **§A5** | EEG real modality (gated) | user EEG raw → projector → fingerprint → byte-LM (§19 carry) | $0 ckpt-side |

honest dependency:
- §A1 → §A2 (baseline 측정 필수)
- §A2 → §A3 → §A4 (sequential)
- §A5 = user hardware gate

---

## §6 — pre-registered falsifiers (B-ADAPTER-1..5)

| name | predicate | what it shows |
|---|---|---|
| **B-ADAPTER-1** | projector from-scratch (no pretrained weights loaded) | §7 ① ✅ |
| **B-ADAPTER-2** | training signal = anima Ψ_direction only (no external label) | §7 ② ✅ |
| **B-ADAPTER-3** | 5-channel output bounded [0, 1] ∀ input | Boolean closed-form |
| **B-ADAPTER-4** | byte serialize round-trip: deserialize ≈ original within quant error | byte-equal invariant |
| **B-ADAPTER-5** | anchor-aware: pairwise cosine of fingerprint per anchor distinguishable | distinguishing_ratio ≥ τ |

---

## §7 — cross-link

- `HEXAD/UNCLASSIFIED/state/kosmos_modality_fire_s175_2026_05_20/` (§175 anchor distinguishing = 0 → adapter motivation)
- `HEXAD/UNCLASSIFIED/state/kosmos_5modality_brainstorm_2026_05_20/` (14-candidate brainstorm, M1 ranking ★★★★)
- `HEXAD/TENSION-LINK/` (5-channel original SSOT — TENSION-LINK 의 universality)
- `HEXAD/CHAT/SPONTANEOUS.tape` (Engine A/G ⇄ adapter integration future)
- `HEXAD/KOSMOS.md` (multi-modal payload SSOT)
- `HEXAD/FINAL.md` (V-SPONT 최종스펙 — adapter 가 V-SPONT 의 multi-modal extension layer)
- `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md` (§183 48-ceiling inventory — adapter = axis 4 4.7 multi-modality 수도꼭지 Tier B)
- `@D g_no_cost_scope_limit` · `@D g_fire_autonomous` (cost-cap 0, autonomy)
- `@D g_kosmos_anchor_ssot` (kosmos format SSOT)

---

## §8 — honest carve-outs

1. **ground truth gap**: projector 학습 신호 = anima Ψ-self-supervised 만.
   외부 modality 의 *진짜 의미* 와 align 되는지는 별도 measurement (M3
   synthetic 가 baseline anchor).
2. **5-channel 부족 가능성**: 5-channel 이 image complexity 표현 부족할
   수 있음. honest carry — measurement 가 fails 면 channel 확장 (e.g.
   5+modality-id = 6) future cycle.
3. **byte serialization precision loss**: uint16 quantize = ~1/65535
   precision, small modality-specific detail 손실. measure error
   acceptable upper bound.
4. **necessary-not-sufficient** (B-EMERGE-7): adapter 가 modality-aware
   representation 만든다고 GOAL emergence 보장 X. V-SPONT 결합 별도.
5. **§7 honesty re. self-supervision**: projector 가 Ψ-supervised =
   *anima self-supervised*, 단 *external signal 으로부터 anchor-aware
   learning* 은 별도 axis. M3 baseline 측정 후 평가.

